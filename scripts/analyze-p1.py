#!/opt/homebrew/bin/python3
"""P1 analysis per paper/analysis-plan.md, recomputed from the raw run rows.

Reads each lane's results.jsonl and errors.jsonl under runs,
derives case correctness and Brier from p_true and the label (never from the
stored grade fields), checks them against the grade fields, and writes
analysis.json and analysis.md to runs/analysis/.

    scripts/analyze-p1.py [--fast]     (--fast: 2,000 bootstrap draws instead of 10,000)
"""
import collections
import itertools
import json
import math
import random
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
FLOW = HERE / "runs"
CASES = FLOW / "cases-paper-144.json"
MUTATED = HERE / "sources" / "mutated-cases.json"
OUT = FLOW / "analysis"
LANES = {  # lane -> variants pooled into it, in the order they ran
    "Opus 5.5": ["baseline", "v3"],
    "Fable 5.1": ["v6"],
    "Sonnet 5.5": ["v4"],
    "Haiku 5.5": ["v5"],
    "SWE-2 High": ["v1"],
    "DeepSeek Flash": ["v2"],
}
THRESHOLD = 0.5
SEED = 20261017
BOOT = 2000 if "--fast" in sys.argv else 10000
SIGNFLIPS = 20000
EXACT_MAX = 20          # enumerate 2^k sign assignments when k non-zero family differences <= this
SINGLE_RUN_DRAWS = 200  # one completed run per case, redrawn this many times, for pairs with a one-run lane
INFRA_MARKERS = ("unrecognized_model", "save_health")
# Council claims that restate an original claim (found by text comparison in council round 1).
RESTATEMENTS = {"tbm-96d7b9d-pre-indent": "0927-indent-outside-pre", "tbm-96d7b9d-jsonld-csp": "0927-jsonld-csp",
                "tbm-96d7b9d-unlisted-feed-leak": "0927-unlisted-feed-leak"}
# Cases whose refutation rests on evidence outside the pinned files (a dependency, a live
# header default, a rendered image, dead URLs, intended behaviour); council round 2.
OUTSIDE_FILES = {"cookie-tab-cb74f3a-fragment-stale-pay", "orthodoxprayers-af4e178-headers-miss-pages",
                 "squint-c7ea926-icc-torn-chain", "squint-ec53337-upside-down", "tbm-96d7b9d-localecompare-lang",
                 "tbm-96d7b9d-pre-indent", "0819-foundation-dead", "0927-dead-links-2025"}
# Label sensitivity scenarios (paper/materiality-rule.md and the owner's rulings of
# 2026-10-17). The frozen labels stay primary; each scenario recomputes every lane.
MATERIALITY = {"C-onion-search-count": 1, "C-pendulum-button-count": 1}
# Compound claims (more than one alleged defect) whose mutant text itself alleges a second
# defect that is genuine at the pinned commit; real under the owner's existential aggregation
# (rulings of 2026-10-18, scope narrowed after council round 3; materiality-rule.md).
COMPOUND = {"C-guard-no-dupes": 1, "C-feed-build-clock": 1, "C-dls-alt": 1, "C-readme-never-run": 1}
LABEL_SCENARIOS = {
    "0819-infra-los-angeles as real (artifact-only standard)": {"0819-infra-los-angeles": 1},
    "0819-tezos-editions as false ('N editions' = run size)": {"0819-tezos-editions": 0},
    "materiality rule: count tolerance": MATERIALITY,
    "all four flips at once (LA, Tezos, count tolerance)": {"0819-infra-los-angeles": 1, "0819-tezos-editions": 0, **MATERIALITY},
}
# A different target definition, not a label correction: reported in its own section.
TARGET_SCENARIOS = {
    "existential aggregation over compound claims alone": COMPOUND,
    "count tolerance plus existential aggregation over compound claims": {**MATERIALITY, **COMPOUND},
    "the four flips plus existential aggregation": {"0819-infra-los-angeles": 1, "0819-tezos-editions": 0, **MATERIALITY, **COMPOUND},
}


def read_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def exact_mean(values):
    """Mean of the reported decimals, computed exactly. Models report p_true as
    short decimals; a binary float sum can make two equal means differ in the last
    bit, which turns a true AUROC tie into a strict comparison."""
    return float(Fraction(sum(Fraction(Decimal(repr(x))) for x in values), len(values)))


def case_sources():
    cases = json.loads(CASES.read_text())["cases"]
    sources, labels = {}, {}
    for c in cases:
        src = c.get("source", "original")
        sources[c["id"]] = "squint" if c.get("repo") == "mdws-org/squint" else src
        labels[c["id"]] = c["label"]
    return sources, labels


def claim_families(sources):
    """Resampling unit for the bootstrap and the sign-flips: an original claim with
    every mutated case derived from it and every council restatement of it; any
    other case is its own family. Refuses to run without the mutant parent map."""
    if not MUTATED.exists():
        raise SystemExit(f"family map needed: {MUTATED} is missing (derived_from per mutated case)")
    mc = json.loads(MUTATED.read_text())
    parent = {c["id"]: c["derived_from"] for c in (mc["cases"] if isinstance(mc, dict) else mc) if c.get("derived_from")}
    parent.update(RESTATEMENTS)
    return {cid: parent.get(cid, cid) for cid in sources}


def load_lane(variants):
    rows, errors = [], []
    for v in variants:
        rows += [r for r in read_jsonl(FLOW / v / "results.jsonl") if r.get("status") == "ok"]
        errors += read_jsonl(FLOW / v / "errors.jsonl")
    return rows, errors


def classify_errors(errors, done):
    """Attempted failures by class, and the (case, rep) slots still missing a row;
    a missing slot takes the class of its final attempt."""
    infra = model = 0
    last_kind = {}
    for e in errors:
        kind = "infrastructure" if any(m in str(e.get("error", "")) for m in INFRA_MARKERS) else "model"
        if kind == "infrastructure":
            infra += 1
        else:
            model += 1
        last_kind[(e["prompt_id"], e["rep"])] = kind
    missing = {"infrastructure": [], "model": []}
    for slot, kind in sorted(last_kind.items()):
        if slot not in done:
            missing[kind].append(slot)
    return {"attempts": {"infrastructure": infra, "model": model}, "missing": missing}


def limit_rows(variants):
    """Rows of these variants that met a limit recorded in budgets.json.
    cut: a completed row with a stop reason other than end_turn, a wall clock at or
    past timeout_s, or an output at or past max_output_tokens. turn_ceiling: a
    completed row whose turn count is at or past max_turns (0 = no ceiling).
    not_ok: rows the runner itself marked truncated, which no lane table includes."""
    budgets = json.loads((FLOW / "budgets.json").read_text())
    cut, ceiling, not_ok, most_turns, flags = set(), set(), 0, 0, []
    for v in variants:
        b = budgets.get(v, {})
        flags.append(b.get("max_turns", 0))
        for r in read_jsonl(FLOW / v / "results.jsonl"):
            if r.get("status") != "ok":
                not_ok += 1
                continue
            slot = (r["prompt_id"], r["rep"])
            turns = r.get("num_turns") or 0
            most_turns = max(most_turns, turns)
            out = (r.get("usage") or {}).get("output_tokens") or 0
            if (r.get("stop_reason") != "end_turn" or (b.get("timeout_s") and (r.get("latency_s") or 0) >= b["timeout_s"])
                    or (b.get("max_output_tokens") and out >= b["max_output_tokens"])):
                cut.add(slot)
            elif b.get("max_turns") and turns >= b["max_turns"]:
                ceiling.add(slot)
    return {"cut": sorted(cut), "turn_ceiling": sorted(ceiling), "not_ok": not_ok,
            "most_turns": most_turns, "turn_flags": sorted(set(flags))}


def case_table(rows, labels, threshold=THRESHOLD, failed_wrong=(), pick=None):
    """case id -> per-case aggregates, derived from p_true and the label only.
    pick: function(case id, rows) -> one row, for a single-run view.
    failed_wrong: (case, rep) slots scored as wrong with no p_true."""
    by = collections.defaultdict(list)
    for r in rows:
        by[r["prompt_id"]].append(r)
    table, mismatches = {}, 0
    for cid, rs in by.items():
        if pick is not None:
            rs = [pick(cid, rs)]
        label = labels.get(cid, rs[0]["meta"]["label"])
        ps = [float(r["grade"]["p_true"]) for r in rs]
        right = [1.0 if (p >= threshold) == (label == 1) else 0.0 for p in ps]
        if threshold == THRESHOLD and pick is None:
            mismatches += sum(1 for r, k in zip(rs, right) if float(r["grade"]["correct"]) != k)
        extra = sum(1 for c, _ in failed_wrong if c == cid)
        right_all = right + [0.0] * extra
        table[cid] = {
            "label": label, "p": exact_mean(ps), "correct": sum(right_all) / len(right_all),
            "brier": sum((p - label) ** 2 for p in ps) / len(ps), "reps": len(rs),
            "any": max(right_all), "all": min(right_all),
            "disagree": 1 if 2 * (len(right_all) - sum(right_all)) > len(right_all) else 0,
        }
    return table, mismatches


def clopper_pearson(k, n):
    """Exact binomial interval by bisection on the binomial tail."""
    if not n:
        return (math.nan, math.nan)

    def cdf(x, p):  # P(X <= x)
        return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, x + 1))

    def solve(target, fn):  # fn increases with p; find p with fn(p) = target
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if fn(mid) > target:
                hi = mid
            else:
                lo = mid
        return (lo + hi) / 2
    lower = 0.0 if k == 0 else solve(0.025, lambda p: 1 - cdf(k - 1, p))   # P(X >= k) = 0.025
    upper = 1.0 if k == n else solve(0.975, lambda p: 1 - cdf(k, p))       # P(X <= k) = 0.025
    return (lower, upper)


def auroc(pos, neg):
    """Mann-Whitney AUROC with ties counted 0.5, by average ranks (equal to the
    pairwise sum of 1 / 0.5 / 0 over every positive-negative pair)."""
    if not pos or not neg:
        return math.nan
    allv = sorted([(x, 1) for x in pos] + [(y, 0) for y in neg])
    i, n, rank_sum = 0, len(allv), 0.0
    while i < n:
        j = i
        while j < n and allv[j][0] == allv[i][0]:
            j += 1
        rank_sum += (i + 1 + j) / 2 * sum(lab for _, lab in allv[i:j])
        i = j
    return (rank_sum - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


def metrics_of(table, ids=None):
    cs = [table[c] for c in (ids if ids is not None else table) if c in table]
    pos = [c for c in cs if c["label"] == 1]
    neg = [c for c in cs if c["label"] == 0]
    rk, sk = sum(c["correct"] for c in pos), sum(c["correct"] for c in neg)
    return {
        "cases": len(cs), "real": len(pos), "false": len(neg),
        "recall": rk / len(pos) if pos else math.nan, "recall_k": rk,
        "specificity": sk / len(neg) if neg else math.nan, "specificity_k": sk,
        "accuracy": (rk + sk) / len(cs) if cs else math.nan,
        "auroc": auroc([c["p"] for c in pos], [c["p"] for c in neg]),
        "brier": sum(c["brier"] for c in cs) / len(cs) if cs else math.nan,
    }


FABLE_RERUN = "v7"  # Fable 5.1's second run on the 60-case draw (analysis-plan.md, 2026-10-18)


def fable_variability(rows_by_lane, labels):
    """The pre-specified descriptive comparison on the rerun cases: Fable's two runs
    against every three-run lane's pairs of runs. Returns None until v7 has rows."""
    second = [r for r in load_lane([FABLE_RERUN])[0]]
    if not second:
        return None
    first = {r["prompt_id"]: r for r in rows_by_lane["Fable 5.1"]}
    sec = {r["prompt_id"]: r for r in second}
    drawn = [c["id"] for c in json.loads((FLOW / "cases-fable-rerun60.json").read_text())["cases"]]
    ids = [c for c in drawn if c in first and c in sec]

    def right(r, cid):
        return (float(r["grade"]["p_true"]) >= 0.5) == (labels[cid] == 1)
    both = sum(1 for c in ids if right(first[c], c) and right(sec[c], c))
    either = sum(1 for c in ids if right(first[c], c) or right(sec[c], c))
    flips = sum(1 for c in ids if right(first[c], c) != right(sec[c], c))
    out = {"drawn": len(drawn), "completed_both": len(ids), "missing": sorted(set(drawn) - set(ids)),
           "fable": {"both": both / len(ids), "both_k": both, "both_ci": clopper_pearson(both, len(ids)),
                     "either": either / len(ids), "flips": flips,
                     "mean_abs_dp": sum(abs(float(first[c]["grade"]["p_true"]) - float(sec[c]["grade"]["p_true"])) for c in ids) / len(ids)},
           "lanes": {}}
    for lane, rows in rows_by_lane.items():
        if lane == "Fable 5.1":
            continue
        by = collections.defaultdict(dict)
        for r in rows:
            by[r["prompt_id"]][r["rep"]] = right(r, r["prompt_id"])
        pair_rates, flip_rates, every, anyr, n = [], [], 0, 0, 0
        for c in ids:
            reps = by.get(c, {})
            if not reps:
                continue
            n += 1
            vals = list(reps.values())
            every += all(vals)
            anyr += any(vals)
            pairs = [(reps[a], reps[b]) for a, b in itertools.combinations(sorted(reps), 2)]
            if pairs:
                pair_rates.append(sum(1 for x, y in pairs if x and y) / len(pairs))
                flip_rates.append(sum(1 for x, y in pairs if x != y) / len(pairs))
        out["lanes"][lane] = {"cases": n, "pair_both": sum(pair_rates) / len(pair_rates) if pair_rates else math.nan,
                              "pair_flip": sum(flip_rates) / len(flip_rates) if flip_rates else math.nan,
                              "every": every / n if n else math.nan, "any": anyr / n if n else math.nan}
    out["fable"]["flip_rate"] = flips / len(ids)
    return out


def consistency(table):
    out = {"short": sum(1 for c in table.values() if 1 < c["reps"] < 3)}
    for name, keep in (("all", None), ("real", 1), ("false", 0)):
        multi = [c for c in table.values() if c["reps"] > 1 and (keep is None or c["label"] == keep)]
        out[name] = {"n": len(multi),
                     "any": sum(c["any"] for c in multi) / len(multi) if multi else math.nan,
                     "every": sum(c["all"] for c in multi) / len(multi) if multi else math.nan}
    return out


def family_bootstrap(table, families, rng, ids=None):
    """Percentile intervals for the lane metrics, resampling claim families. A
    recall or specificity cell with no failures (or none right) gets the exact
    binomial interval instead, since the percentile bootstrap is degenerate there."""
    ids = [c for c in (ids if ids is not None else table) if c in table]
    byfam = collections.defaultdict(list)
    for c in ids:
        byfam[families[c]].append(c)
    fams = list(byfam)
    draws = collections.defaultdict(list)
    kept = 0
    for _ in range(BOOT):
        sample = [c for f in rng.choices(fams, k=len(fams)) for c in byfam[f]]
        cs = [table[c] for c in sample]
        pos = [c for c in cs if c["label"] == 1]
        neg = [c for c in cs if c["label"] == 0]
        if pos and neg:
            kept += 1
            draws["recall"].append(sum(c["correct"] for c in pos) / len(pos))
            draws["specificity"].append(sum(c["correct"] for c in neg) / len(neg))
            draws["accuracy"].append(sum(c["correct"] for c in cs) / len(cs))
            draws["auroc"].append(auroc([c["p"] for c in pos], [c["p"] for c in neg]))
            draws["brier"].append(sum(c["brier"] for c in cs) / len(cs))
    ci = {"kept": kept, "families": len(fams)}
    for k, v in draws.items():
        v.sort()
        ci[k] = (v[int(0.025 * len(v))], v[min(len(v) - 1, int(0.975 * len(v)))])
    m = metrics_of(table, ids)
    for key in ("recall", "specificity"):
        n = m["real"] if key == "recall" else m["false"]
        k = m[f"{key}_k"]
        if n and (k == 0 or k == n):
            ci[key] = clopper_pearson(int(round(k)), n)
            ci[f"{key}_method"] = "Clopper-Pearson (degenerate bootstrap)"
    return ci


def per_source(table, sources):
    out = {}
    for cid, c in table.items():
        s = out.setdefault(sources.get(cid, "?"), {"real": [0, 0.0], "false": [0, 0.0]})
        key = "real" if c["label"] == 1 else "false"
        s[key][0] += 1
        s[key][1] += c["correct"]
    return {src: {k: (v[1] / v[0] if v[0] else None, v[0]) for k, v in d.items()} for src, d in out.items()}


def signflip(diffs_by_family, n_cases, rng, exact_max=EXACT_MAX, draws=SIGNFLIPS):
    """Two-sided paired sign-flip p on the mean per-case difference, flipping whole
    claim families: exact enumeration up to exact_max non-zero families, Monte Carlo above."""
    d = [x for x in diffs_by_family if x != 0]
    if not n_cases:
        return math.nan, math.nan, "none"
    obs = sum(diffs_by_family) / n_cases
    if not d:
        return obs, 1.0, "exact"
    if len(d) <= exact_max:
        hits = sum(1 for s in itertools.product((1, -1), repeat=len(d))
                   if abs(sum(a * b for a, b in zip(s, d)) / n_cases) >= abs(obs) - 1e-12)
        return obs, hits / 2 ** len(d), "exact"
    hits = 0
    for _ in range(draws):
        s = sum(x if rng.random() < 0.5 else -x for x in d) / n_cases
        if abs(s) >= abs(obs) - 1e-12:
            hits += 1
    return obs, (hits + 1) / (draws + 1), "mc"


def family_diffs(ta, tb, ids, families):
    byfam = collections.defaultdict(float)
    for c in ids:
        byfam[families[c]] += ta[c]["correct"] - tb[c]["correct"]
    return list(byfam.values())


def auroc_family_bootstrap(ta, tb, shared, families, rng, draws_n=None):
    """Paired difference in AUROC with a claim-family bootstrap interval and two
    two-sided p-values: 'tail' = twice the smaller share of draws on either side of
    zero (the plan's definition, the percentile interval's inversion); 'centred' =
    the share of draws at least as far from the observed difference as zero is
    (the reflected bootstrap test). The two disagree when the draws are skewed."""
    byfam = collections.defaultdict(list)
    for c in shared:
        byfam[families[c]].append(c)
    fams = list(byfam)
    diff = auroc([ta[c]["p"] for c in shared if ta[c]["label"] == 1], [ta[c]["p"] for c in shared if ta[c]["label"] == 0]) \
        - auroc([tb[c]["p"] for c in shared if tb[c]["label"] == 1], [tb[c]["p"] for c in shared if tb[c]["label"] == 0])
    draws = []
    for _ in range(draws_n or BOOT):
        sample = [c for f in rng.choices(fams, k=len(fams)) for c in byfam[f]]
        pa = [ta[c]["p"] for c in sample if ta[c]["label"] == 1]
        na = [ta[c]["p"] for c in sample if ta[c]["label"] == 0]
        pb = [tb[c]["p"] for c in sample if tb[c]["label"] == 1]
        nb = [tb[c]["p"] for c in sample if tb[c]["label"] == 0]
        if pa and na and pb and nb:
            draws.append(auroc(pa, na) - auroc(pb, nb))
    draws.sort()
    n = len(draws)
    lo, hi = draws[int(0.025 * n)], draws[min(n - 1, int(0.975 * n))]
    neg = sum(1 for x in draws if x < 0)
    pos = sum(1 for x in draws if x > 0)
    zero = n - neg - pos  # draws at exactly zero (both lanes at the same AUROC) count half on each side
    small = min(neg, pos) + zero / 2
    tail_floored = small == 0  # no draw on the small side: p is below the test's resolution of 2/n
    p_tail = 2 / n if tail_floored else min(1.0, 2 * small / n)
    c_hits = sum(1 for x in draws if abs(x - diff) >= abs(diff))
    p_centred = 1 / n if c_hits == 0 else min(1.0, c_hits / n)
    return {"diff": diff, "ci": (lo, hi), "p": p_tail, "p_floored": tail_floored, "p_centred": p_centred,
            "p_centred_floored": c_hits == 0, "zero_share": zero / n, "small_tail": small, "kept": n, "families": len(fams)}


def holm(pvals):
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    adj, running = [None] * len(pvals), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(pvals) - rank) * pvals[i]))
        adj[i] = running
    return adj


def single_run_table(rows, labels, rng):
    """One completed run drawn at random per case; no fallback to a mean."""
    return case_table(rows, labels, pick=lambda cid, rs: rng.choice(rs))[0]


def compare(tables, families, rng, rows_by_lane, labels, ids=None, with_single=True, single_auroc_draws=0):
    """All lane pairs on shared cases (restricted to ids when given). Primary: AUROC
    by claim-family bootstrap. Secondary: accuracy, recall, specificity by
    family-level sign-flip. For a pair with a one-run lane, the three-run lane is
    also subsampled to one run per case (SINGLE_RUN_DRAWS times): the median
    secondary p, the share of draws surviving 0.05/15, and the single-run AUROC
    difference's median and 5-95% range, with the tail p on the median draw."""
    fams = {"auroc": [], "accuracy": [], "recall": [], "specificity": []}
    one_run = {lane for lane, t in tables.items() if max(c["reps"] for c in t.values()) == 1}
    npairs = len(list(itertools.combinations(tables, 2)))
    for a, b in itertools.combinations(tables, 2):
        ta, tb = tables[a], tables[b]
        shared = sorted(c for c in (set(ta) & set(tb)) if ids is None or c in ids)
        au = auroc_family_bootstrap(ta, tb, shared, families, rng)
        fams["auroc"].append({"a": a, "b": b, "n": len(shared), **au})
        for fam, keep in (("accuracy", None), ("recall", 1), ("specificity", 0)):
            sub = [c for c in shared if keep is None or ta[c]["label"] == keep]
            obs, p, method = signflip(family_diffs(ta, tb, sub, families), len(sub), rng)
            fams[fam].append({"a": a, "b": b, "n": len(sub), "diff": obs, "p": p, "method": method,
                              "nonzero_families": sum(1 for x in family_diffs(ta, tb, sub, families) if x != 0)})
        if with_single and (a in one_run) != (b in one_run):
            multi = b if a in one_run else a
            ps = collections.defaultdict(list)
            adiffs, aps = [], []
            singles = []
            for _ in range(SINGLE_RUN_DRAWS):
                tm = single_run_table(rows_by_lane[multi], labels, rng)
                sa, sb = (ta, tm) if multi == b else (tm, tb)
                singles.append((sa, sb))
                for fam, keep in (("accuracy", None), ("recall", 1), ("specificity", 0)):
                    sub = [c for c in shared if keep is None or sa[c]["label"] == keep]
                    ps[fam].append(signflip(family_diffs(sa, sb, sub, families), len(sub), rng, exact_max=12, draws=4000)[1])
                adiffs.append(auroc([sa[c]["p"] for c in shared if sa[c]["label"] == 1], [sa[c]["p"] for c in shared if sa[c]["label"] == 0])
                              - auroc([sb[c]["p"] for c in shared if sb[c]["label"] == 1], [sb[c]["p"] for c in shared if sb[c]["label"] == 0]))
                if single_auroc_draws:
                    aps.append(auroc_family_bootstrap(sa, sb, shared, families, rng, draws_n=single_auroc_draws)["p"])
            for fam in ("accuracy", "recall", "specificity"):
                v = sorted(ps[fam])
                fams[fam][-1]["single_run"] = {"p_median": v[len(v) // 2], "survive_share": sum(1 for p in v if p < 0.05 / npairs) / len(v)}
            order = sorted(range(len(adiffs)), key=lambda i: adiffs[i])
            med_i = order[len(order) // 2]
            sa, sb = singles[med_i]
            au1 = auroc_family_bootstrap(sa, sb, shared, families, rng, draws_n=min(BOOT, 4000))
            fams["auroc"][-1]["single_run"] = {"diff_median": adiffs[med_i], "diff_5_95": (adiffs[order[len(order) // 20]], adiffs[order[len(order) * 19 // 20]]),
                                               "p_tail_on_median_draw": au1["p"], "p_centred_on_median_draw": au1["p_centred"]}
            if aps:
                v = sorted(aps)
                fams["auroc"][-1]["single_run"].update({"p_median": v[len(v) // 2], "survive_share": sum(1 for p in v if p < 0.05 / npairs) / len(v),
                                                        "draws_per_bootstrap": single_auroc_draws})
    for rows in fams.values():
        for r, q in zip(rows, holm([r["p"] for r in rows])):
            r["p_holm"] = q
        if rows and "p_centred" in rows[0]:
            for r, q in zip(rows, holm([r["p_centred"] for r in rows])):
                r["p_centred_holm"] = q
    return fams


MUTATION_CLASSES = {"A": "re-targeted at a sibling file", "B": "already fixed at the pinned commit", "C": "one concrete fact changed", "D": "freestanding invented mechanism"}


def mutation_classes(tables, sources):
    """Specificity (mean case correctness) per false-claim class, per lane."""
    def cls(cid):
        if sources[cid] == "mutated":
            return f"mutated {cid[0]}"
        return sources[cid]
    out = {}
    for lane, t in tables.items():
        by = collections.defaultdict(list)
        for cid, c in t.items():
            if c["label"] == 0:
                by[cls(cid)].append(c["correct"])
        out[lane] = {k: (sum(v) / len(v), len(v)) for k, v in sorted(by.items())}
        rest = [t[c]["correct"] for c in t if sources[c] == "mutated" and c.startswith("C-") and c not in MATERIALITY]
        out[lane]["mutated C without count tolerance"] = (sum(rest) / len(rest), len(rest))
    return out


CAL_BINS = [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0001)]


def calibration(table):
    """Case-level reliability: per p_true bin, cases, mean p_true and the share that are real."""
    out = []
    for lo, hi in CAL_BINS:
        cs = [c for c in table.values() if lo <= c["p"] < hi]
        out.append({"bin": f"[{lo:.1f}, {min(hi, 1.0):.1f}{']' if hi > 1 else ')'}", "n": len(cs),
                    "mean_p": sum(c["p"] for c in cs) / len(cs) if cs else math.nan,
                    "real_share": sum(c["label"] for c in cs) / len(cs) if cs else math.nan})
    return out


def lane_cost(rows):
    """Harness-reported spend and per-run effort. The ccx lane's figure is the harness's own
    estimate at Anthropic list prices, not the provider's bill; the Devin lane reports 0.
    Every Claude Code run ends with one StructuredOutput call that returns the JSON verdict;
    the runner counts it as a tool call, so it is subtracted here for the Claude Code lanes."""
    n = len(rows)
    so = 0 if rows and rows[0].get("model", "").startswith("swe-") else 1
    return {"runs": n, "reported_cost_usd": sum(float(r.get("reported_cost_usd") or 0) for r in rows),
            "mean_latency_s": sum(float(r.get("latency_s") or 0) for r in rows) / n if n else math.nan,
            "mean_tool_calls": sum(max(0.0, float(r.get("tool_calls") or 0) - so) for r in rows) / n if n else math.nan,
            "verdict_agreement": sum(float(r["grade"].get("verdict_correct") or 0) for r in rows) / n if n else math.nan}


def disagreements(tables, sources):
    return {lane: sorted((cid, sources.get(cid), c["label"], round(c["p"], 3), c["reps"])
                         for cid, c in t.items() if c["disagree"])
            for lane, t in tables.items()}


def fmt(x, pct=True, nd=None):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n/a"
    return f"{100 * x:.1f}%" if pct else f"{x:.{nd or 3}f}"


def fmtp(p, floored=False):
    if p is None or (isinstance(p, float) and math.isnan(p)):
        return "n/a"
    if floored:
        return f"<{p:.4f}"
    return f"{p:.4f}" if p >= 0.0001 else "<0.0001"

# A Claude model in the SWE-2 condition (files inline, no tools); analysis-plan.md, 2026-10-19.
INLINE_LANES = {"Haiku 5.5": ["v8"], "Sonnet 5.5": ["v9"]}
INLINE_CONTRASTS = [("Haiku 5.5", "Haiku 5.5 inline"), ("Sonnet 5.5", "Sonnet 5.5 inline"),
                    ("Haiku 5.5 inline", "SWE-2 High"), ("Sonnet 5.5 inline", "SWE-2 High")]


def harness_decomposition(tables, rows_by_lane, families, labels, rng):
    """The pre-specified harness decomposition: per-lane rows for the inline lanes and
    the four planned paired contrasts (same model, condition differs; same condition,
    model differs), Holm within each metric across the contrasts that have data, plus
    the share of each tooled-versus-SWE-2 difference that the condition accounts for,
    with a claim-family bootstrap interval. Returns None until an inline lane has rows."""
    inline = {}
    for model, variants in INLINE_LANES.items():
        rows, errors = load_lane(variants)
        if rows:
            name = f"{model} inline"
            t, _ = case_table(rows, labels)
            inline[name] = {"rows": len(rows), "table": t, "metrics": metrics_of(t), "ci": family_bootstrap(t, families, rng),
                            "failures": classify_errors(errors, {(r["prompt_id"], r["rep"]) for r in rows}),
                            "cost": lane_cost(rows), "model": model}
    if not inline:
        return None
    alltab = {**tables, **{k: v["table"] for k, v in inline.items()}}
    fams = {"auroc": [], "accuracy": [], "recall": [], "specificity": []}
    for a, b in INLINE_CONTRASTS:
        if a not in alltab or b not in alltab:
            continue
        ta, tb = alltab[a], alltab[b]
        shared = sorted(set(ta) & set(tb))
        au = auroc_family_bootstrap(ta, tb, shared, families, rng)
        fams["auroc"].append({"a": a, "b": b, "n": len(shared), **au})
        for fam, keep in (("accuracy", None), ("recall", 1), ("specificity", 0)):
            sub = [c for c in shared if keep is None or ta[c]["label"] == keep]
            obs, p, method = signflip(family_diffs(ta, tb, sub, families), len(sub), rng)
            fams[fam].append({"a": a, "b": b, "n": len(sub), "diff": obs, "p": p, "method": method,
                              "nonzero_families": sum(1 for x in family_diffs(ta, tb, sub, families) if x != 0)})
    for rows in fams.values():
        for r, q in zip(rows, holm([r["p"] for r in rows])):
            r["p_holm"] = q
        if rows and "p_centred" in rows[0]:
            for r, q in zip(rows, holm([r["p_centred"] for r in rows])):
                r["p_centred_holm"] = q
    # Share of the tooled-lane-minus-SWE-2 gap accounted for by the condition:
    # (tooled - inline) / (tooled - SWE-2), per metric, bootstrap over claim families.
    shares = {}
    for model in INLINE_LANES:
        name = f"{model} inline"
        if name not in inline or model not in tables:
            continue
        tt, ti, ts = tables[model], inline[name]["table"], tables["SWE-2 High"]
        ids = sorted(set(tt) & set(ti) & set(ts))
        byfam = collections.defaultdict(list)
        for c in ids:
            byfam[families[c]].append(c)
        flist = list(byfam)

        def stats(sample):
            out = {}
            for key, metric in (("auroc", lambda t, cs: auroc([t[c]["p"] for c in cs if t[c]["label"] == 1], [t[c]["p"] for c in cs if t[c]["label"] == 0])),
                                ("accuracy", lambda t, cs: sum(t[c]["correct"] for c in cs) / len(cs)),
                                ("specificity", lambda t, cs: sum(t[c]["correct"] for c in cs if t[c]["label"] == 0) / max(1, sum(1 for c in cs if t[c]["label"] == 0)))):
                gap = metric(tt, sample) - metric(ts, sample)
                cond = metric(tt, sample) - metric(ti, sample)
                out[key] = (gap, cond, cond / gap if abs(gap) > 1e-9 else math.nan)
            return out
        point = stats(ids)
        draws = collections.defaultdict(list)
        for _ in range(min(BOOT, 4000)):
            sample = [c for f in rng.choices(flist, k=len(flist)) for c in byfam[f]]
            if not any(tt[c]["label"] == 1 for c in sample) or not any(tt[c]["label"] == 0 for c in sample):
                continue
            for key, (_, _, ratio) in stats(sample).items():
                if not math.isnan(ratio):
                    draws[key].append(ratio)
        shares[model] = {}
        for key, (gap, cond, ratio) in point.items():
            v = sorted(draws[key])
            shares[model][key] = {"gap": gap, "condition": cond, "share": ratio,
                                  "share_ci": (v[int(0.025 * len(v))], v[min(len(v) - 1, int(0.975 * len(v)))]) if v else (math.nan, math.nan), "draws": len(v)}
    return {"lanes": {k: {kk: vv for kk, vv in v.items() if kk != "table"} for k, v in inline.items()}, "contrasts": fams, "shares": shares}


def render(report):
    L = report["lanes"]
    md = ["# P1 analysis (recomputed from raw rows)", "",
          f"Primary endpoint: AUROC of p_true. Intervals and pairwise differences by claim-family bootstrap ({BOOT} draws; "
          f"{report['families']} families over 144 cases, the largest holding {report['largest_family']} cases). Pairwise AUROC p: "
          "'tail' (twice the smaller share of draws on either side of zero; the plan's definition, primary by the owner's ruling of 2026-10-18) "
          "with the reflected 'centred' p beside it. "
          f"Secondary: accuracy, recall, specificity by family-level paired sign-flip (exact up to {EXACT_MAX} non-zero families), Brier. "
          "Holm within each family across all 15 lane pairs. A run is right when (p_true ≥ 0.5) matches the label, so a reported 0.50 counts as a call of real; "
          "a case's p_true is the exact mean of its completed runs. Grade fields in the rows agree with the recomputation on every run "
          f"(mismatches: {sum(r['grade_mismatches'] for r in L.values())}).", ""]
    md += ["| lane | cases | (case, rep) slots attempted / completed | failed attempts (infra/model) | missing slots (infra/model) | AUROC [95% CI] | Brier | recall [95% CI] | specificity [95% CI] | accuracy |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for lane, r in L.items():
        m, ci, f = r["metrics"], r["ci"], r["failures"]
        att = r["rows"] + len(f["missing"]["infrastructure"]) + len(f["missing"]["model"])
        rc = f" ({ci['recall_method']})" if "recall_method" in ci else ""
        md.append(f"| {lane} | {m['cases']} | {att} / {r['rows']} | {f['attempts']['infrastructure']}/{f['attempts']['model']} | "
                  f"{len(f['missing']['infrastructure'])}/{len(f['missing']['model'])} | "
                  f"{fmt(m['auroc'], False)} [{fmt(ci['auroc'][0], False, 4)}, {fmt(ci['auroc'][1], False, 4)}] | {fmt(m['brier'], False)} | "
                  f"{fmt(m['recall'])} [{fmt(ci['recall'][0])}, {fmt(ci['recall'][1])}]{rc} | "
                  f"{fmt(m['specificity'])} [{fmt(ci['specificity'][0])}, {fmt(ci['specificity'][1])}] | {fmt(m['accuracy'])} |")
    md += ["", "Missing slots are attempted (case, rep) runs with no completed row: infrastructure failures the resume could not fill, and model "
           "failures (unparseable output, a forbidden tool), which stay missing by the plan. All 52 real findings are original audit claims; the "
           "92 false claims are 7 original, 52 mutated (39 derived from 29 original claims by one changed fact, 13 freestanding invented mechanisms), "
           "19 council and 14 Squint, so pooled specificity is mostly mutant rejection.", ""]
    md += ["## Within original claims (59 audit claims: 52 real, 7 false)", "",
           "| lane | AUROC [95% CI] | recall | specificity (7 cases; cases right, fractional over runs) | accuracy |", "|---|---|---|---|---|"]
    for lane, r in L.items():
        m, ci = r["original"]["metrics"], r["original"]["ci"]
        md.append(f"| {lane} | {fmt(m['auroc'], False)} [{fmt(ci['auroc'][0], False, 4)}, {fmt(ci['auroc'][1], False, 4)}] | "
                  f"{fmt(m['recall'])} | {fmt(m['specificity'])} ({m['specificity_k']:.2f}/7) | {fmt(m['accuracy'])} |")
    md += ["", "Within-original AUROC pairs, Holm-adjusted (tail p):", "", "| A | B | A−B | 95% CI | draws at zero | p | p (Holm) |", "|---|---|---|---|---|---|---|"]
    for r in report["original_comparisons"]["auroc"]:
        md.append(f"| {r['a']} | {r['b']} | {r['diff']:+.3f} | [{r['ci'][0]:+.4f}, {r['ci'][1]:+.4f}] | {fmt(r['zero_share'])} | {fmtp(r['p'], r.get('p_floored'))} | {fmtp(r['p_holm'], r.get('p_floored'))} |")
    md += ["", "With seven false claims the within-original AUROC is coarse: a draw that omits the one original false claim a lane misses puts both lanes at AUROC 1, so a large share of draws sit at exactly zero. "
           "Those draws count half on each side; a lower bound printed +0.0000 is that atom. The table has little power and ranks nothing."]
    md += ["", "## Consistency over runs (lanes with more than one run)", "",
           "| lane | cases with fewer than 3 runs | right on at least one run (all / real / false) | right on every run (all / real / false) |", "|---|---|---|---|"]
    for lane, r in L.items():
        c = r["consistency"]
        if c["all"]["n"]:
            md.append(f"| {lane} | {c['short']} | {fmt(c['all']['any'])} / {fmt(c['real']['any'])} / {fmt(c['false']['any'])} | "
                      f"{fmt(c['all']['every'])} / {fmt(c['real']['every'])} / {fmt(c['false']['every'])} |")
    md += ["", "## Per source (correctness on real findings / false claims, n)", ""]
    srcs = ["original", "mutated", "council", "squint"]
    md += ["| lane | " + " | ".join(srcs) + " |", "|---|" + "---|" * len(srcs)]
    for lane, r in L.items():
        cells = []
        for s in srcs:
            d = r["per_source"].get(s, {})
            real, false = d.get("real", (None, 0)), d.get("false", (None, 0))
            cells.append(" / ".join(f"{fmt(v[0])} ({v[1]})" if v[1] else "—" for v in (real, false)))
        md.append(f"| {lane} | " + " | ".join(cells) + " |")
    classes = sorted({k for v in report["mutation_classes"].values() for k in v})
    md += ["", "## Specificity by false-claim class (mean case correctness, n cases)", "",
           "Mutation classes: " + "; ".join(f"{k} = {v}" for k, v in MUTATION_CLASSES.items()) + ".", "",
           "| lane | " + " | ".join(classes) + " |", "|---|" + "---|" * len(classes)]
    for lane, d in report["mutation_classes"].items():
        md.append(f"| {lane} | " + " | ".join(f"{fmt(d[k][0])} ({d[k][1]})" if k in d else "—" for k in classes) + " |")
    md += ["", "## Calibration (case-level p_true bins: cases, mean p_true, share real)", "",
           "| lane | " + " | ".join(b["bin"] for b in next(iter(report["calibration"].values()))) + " |", "|---|" + "---|" * len(CAL_BINS)]
    for lane, bins in report["calibration"].items():
        md.append(f"| {lane} | " + " | ".join(f"{b['n']}: {fmt(b['mean_p'], False, 2)} / {fmt(b['real_share'], False, 2)}" if b["n"] else "0" for b in bins) + " |")
    md += ["", "## Cost and effort per lane (completed runs)", "",
           "| lane | runs | harness-reported spend (USD) | mean latency (s) | mean tool calls | bare-verdict agreement |", "|---|---|---|---|---|---|"]
    for lane, c in report["cost"].items():
        md.append(f"| {lane} | {c['runs']} | {c['reported_cost_usd']:.2f} | {c['mean_latency_s']:.1f} | {c['mean_tool_calls']:.1f} | {fmt(c['verdict_agreement'])} |")
    md += ["", "The Claude lanes bill the Anthropic API at the reported figure. The DeepSeek figure is the harness's estimate at Anthropic list prices, not the provider's bill. The SWE-2 lane ran on a free tier and reports 0. Bare-verdict agreement scores the verdict field (true 1, partial 0.5, false 0) against the label."]
    fv = report.get("fable_variability")
    if fv:
        f = fv["fable"]
        md += ["", f"## Run-to-run variability on the Fable rerun draw ({fv['completed_both']} of {fv['drawn']} cases with both Fable runs; specified before the run)", "",
               f"Fable 5.1: right on both runs {fmt(f['both'])} ({f['both_k']}/{fv['completed_both']}, Clopper-Pearson [{fmt(f['both_ci'][0])}, {fmt(f['both_ci'][1])}]); "
               f"right on at least one {fmt(f['either'])}; {f['flips']} cases change side of 0.5; mean |Δp_true| {f['mean_abs_dp']:.3f}."
               + (f" Missing: {', '.join(fv['missing'])}." if fv["missing"] else ""), "",
               "| lane | cases | mean over pairs of runs: right on both | right on every run | right on at least one |", "|---|---|---|---|---|"]
        for lane, m in fv["lanes"].items():
            md.append(f"| {lane} | {m['cases']} | {fmt(m['pair_both'])} | {fmt(m['every'])} | {fmt(m['any'])} |")
    md += ["", "## Sensitivity", "", "| lane | AUROC | Opus runs of 2026-10-17 only | failures scored wrong: recall / specificity (AUROC and Brier use completed runs only) | threshold 0.4: recall / spec | threshold 0.6: recall / spec | without the 8 outside-files cases: AUROC / recall / spec |", "|---|---|---|---|---|---|---|"]
    for lane, r in L.items():
        s = r["sensitivity"]
        o = s.get("opus_1017")
        w = s["without_outside_files"]
        md.append(f"| {lane} | {fmt(r['metrics']['auroc'], False)} | " + (f"AUROC {fmt(o['auroc'], False)}, recall {fmt(o['recall'])}, spec {fmt(o['specificity'])}" if o else "—") +
                  f" | {fmt(s['failed_wrong']['recall'])} / {fmt(s['failed_wrong']['specificity'])} | {fmt(s['t0.4']['recall'])} / {fmt(s['t0.4']['specificity'])} | {fmt(s['t0.6']['recall'])} / {fmt(s['t0.6']['specificity'])} | {fmt(w['auroc'], False)} / {fmt(w['recall'])} / {fmt(w['specificity'])} |")
    md += ["", "Opus pools two batches and two variants (baseline reps 1–2 and the Squint variant v3 ran on 2026-10-17; baseline rep 0 on 2026-10-12). On the same 130 non-Squint cases: " +
           "; ".join(f"{k}: AUROC {fmt(m['auroc'], False)}, recall {fmt(m['recall'])}, specificity {fmt(m['specificity'])}, Brier {fmt(m['brier'], False)}" for k, m in report["opus_batches"].items()) + "."]
    md += ["", "Rows at a recorded limit (`budgets.json`). The runner records a run stopped by the turn cap, the wall clock or the output cap as a failed attempt or a truncated row, "
           "never as a completed row, so the first two columns are a check on that; the third counts completed rows whose turn count is at or past the lane's turn flag.", "",
           "| lane | truncated rows left out of every table | completed rows ended by a limit (stop reason, wall clock, output cap) | completed rows at or past the turn flag | most turns in a row / turn flag | without the rows at a limit: cases, AUROC / recall / spec |", "|---|---|---|---|---|---|"]
    for lane, r in L.items():
        lim, w = r["limit_rows"], r["sensitivity"]["without_limit_rows"]
        flag = "/".join(str(x) if x else "none" for x in lim["turn_flags"])
        md.append(f"| {lane} | {lim['not_ok']} | {len(lim['cut'])} | {len(lim['turn_ceiling'])} | {lim['most_turns']} / {flag} | {w['cases']}, {fmt(w['auroc'], False)} / {fmt(w['recall'])} / {fmt(w['specificity'])} |")
    inline = report.get("inline_limit_rows") or {}
    if inline:
        md += ["", "Inline lanes (turn flag 3, no tools): " + "; ".join(
            f"{name}: {len(lim['turn_ceiling'])} completed rows at the turn flag, {len(lim['cut'])} ended by a limit, {lim['not_ok']} truncated" for name, lim in inline.items()) + "."]
    for key, title in (("inside_comparisons", f"Pairwise survivors without the {len(OUTSIDE_FILES)} outside-files cases (N=136, three-run tests, Holm within family)"),
                       ("failed_wrong_comparisons", "Pairwise survivors with failed runs scored wrong (three-run tests, Holm within family)")):
        md += ["", title + ": " + "; ".join(f"{fam}: " + (", ".join(f"{r['a']} vs {r['b']} ({r['diff']:+.3f}, Holm {fmtp(r['p_holm'], r.get('p_floored'))})" for r in rows if r["p_holm"] < 0.05) or "none")
                                            for fam, rows in report[key].items()) + "."]
    md += ["", "## Label sensitivity (frozen labels stay primary; every scenario is a post-hoc owner ruling)", "",
           "Scenario survivor lists are sensitivity reads with no adjustment across scenarios, p constructions or metric families. For a one-run-versus-three-run pair the three-run p is descriptive (†) and the per-case single-run median p is shown beside it.", ""]
    base_a = {(r["a"], r["b"]): r["p_holm"] for r in report["comparisons"]["auroc"]}
    base_floored = {(r["a"], r["b"]): r.get("p_floored") for r in report["comparisons"]["auroc"]}

    def surv_text(r):
        s = r.get("single_run")
        extra = f", single-run median p {fmtp(s['p_median'])}, {fmt(s['survive_share'])} of draws under 0.05/15" if s else ""
        return f"{r['a']} vs {r['b']} ({r['diff']:+.3f}, Holm {fmtp(r['p_holm'])}{'†' if s else ''}{extra})"
    robust = {fam: {(r["a"], r["b"]) for r in report["comparisons"][fam] if r["p_holm"] < 0.05 and not r.get("single_run")} for fam in ("auroc", "accuracy", "recall", "specificity")}

    def scenario_block(name, s, track):
        out = [f"### {name} ({s['real']} real / {s['false']} false)", "", "| lane | AUROC | Brier | recall | specificity | accuracy |", "|---|---|---|---|---|---|"]
        for lane, m in s["lanes"].items():
            out.append(f"| {lane} | {fmt(m['auroc'], False)} | {fmt(m['brier'], False)} | {fmt(m['recall'])} | {fmt(m['specificity'])} | {fmt(m['accuracy'])} |")
        changed = [f"{r['a']} vs {r['b']}: Holm {fmtp(base_a[(r['a'], r['b'])], base_floored[(r['a'], r['b'])])} → {fmtp(r['p_holm'], r.get('p_floored'))}" for r in s["comparisons"]["auroc"]
                   if (base_a[(r["a"], r["b"])] < 0.05) != (r["p_holm"] < 0.05)]
        out += ["", "AUROC pairs whose Holm verdict changes: " + ("; ".join(changed) if changed else "none") + ".", ""]
        for fam in ("auroc", "accuracy", "recall", "specificity"):
            if track:
                robust[fam] &= {(r["a"], r["b"]) for r in s["comparisons"][fam] if r["p_holm"] < 0.05}
            if fam == "auroc":
                continue
            surv = [surv_text(r) for r in s["comparisons"][fam] if r["p_holm"] < 0.05]
            out.append(f"{fam} survivors under this scenario: " + ("; ".join(surv) if surv else "none") + ".")
        return out + [""]
    for name, s in report["label_sensitivity"].items():
        md += scenario_block(name, s, True)
    md += ["Survivors under the frozen labels that also survive every label scenario (three-run pairs only): " +
           "; ".join(f"{fam}: " + (", ".join(f"{a} vs {b}" for a, b in sorted(v)) or "none") for fam, v in robust.items()) + ".", ""]
    md += ["## Target definition: existential aggregation over compound claims", "",
           "A different question from label error: if a compound claim counts as real whenever any defect its own text alleges is genuine at the pinned commit, "
           f"{len(COMPOUND)} mutants move ({', '.join(f'`{c}`' for c in COMPOUND)}; `materiality-rule.md`, compound claims). Every lane and the panel majority scored these claims mostly false, "
           "so this section measures sensitivity to the target definition, not a property of the lanes. Not part of the label-sensitivity summary above.", ""]
    for name, s in report["target_definition"].items():
        md += scenario_block(name, s, False)
    md += ["", "## Construction facts", "",
           f"A rule that scores every original claim real and every other claim false gets {report['source_rule']['right']}/{report['source_rule']['n']} = {fmt(report['source_rule']['accuracy'])} on the frozen labels. "
           + "Cases per repository (n, real): " + ", ".join(f"{k} ({v[0]}, {v[1]})" for k, v in report["repos"].items()) + ". The lanes see the repository name.", ""]
    one_run = {lane for lane, r in L.items() if r["consistency"]["all"]["n"] == 0}
    for fam, rows in report["comparisons"].items():
        md += ["", f"## {fam}: pairwise, Holm-adjusted" + (" (primary)" if fam == "auroc" else ""), ""]
        if fam == "auroc":
            md += ["| A | B | n | A−B | 95% CI (pointwise) | draws at zero | draws in the small tail | tail p | tail p (Holm) | centred p | centred p (Holm) | single-run: A−B median [5–95%]; tail p on the median draw; median tail p over draws; share of draws with p < 0.05/15 |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
            for r in rows:
                s = r.get("single_run")
                sr = (f"{s['diff_median']:+.3f} [{s['diff_5_95'][0]:+.3f}, {s['diff_5_95'][1]:+.3f}]; {fmtp(s['p_tail_on_median_draw'])}"
                      + (f"; {fmtp(s['p_median'])}; {fmt(s['survive_share'])}" if "p_median" in s else "")) if s else "—"
                md.append(f"| {r['a']} | {r['b']} | {r['n']} | {r['diff']:+.3f} | [{r['ci'][0]:+.4f}, {r['ci'][1]:+.4f}] | {fmt(r['zero_share'])} | {r['small_tail']:.0f} | "
                          f"{fmtp(r['p'], r.get('p_floored'))} | {fmtp(r['p_holm'], r.get('p_floored'))} | {fmtp(r['p_centred'], r.get('p_centred_floored'))} | {fmtp(r['p_centred_holm'], r.get('p_centred_floored'))} | {sr} |")
            md += ["", f"Intervals are pointwise percentile intervals, not simultaneous over the 15 pairs. Draws at exactly zero (both lanes at the same AUROC) count half on each side of the tail test. "
                   f"A p printed with '<' had no draw on the small side, so it is below the test's resolution of 2/{BOOT}; its Holm value inherits the mark. The tail p of a pair with k draws in the small tail carries "
                   f"Monte Carlo error of about 2·sqrt(k)/{BOOT} (13 draws: ±0.0007 on p, ±0.01 on a Holm value multiplied by 14). "
                   "The single-run column redraws one completed run per case for the three-run lane (200 draws): the median difference and its 5–95% range; the tail p of a 4,000-draw bootstrap on the median draw; "
                   "and, where present, the median tail p over the 200 draws (1,000-draw bootstraps) with the share of draws under the Bonferroni cut 0.05/15."]
        else:
            md += ["| A | B | n | A−B | non-zero families | p | p (Holm) | single-run p (median) | share of single-run draws with p < 0.05/15 (Bonferroni) |", "|---|---|---|---|---|---|---|---|---|"]
            for r in rows:
                s = r.get("single_run")
                mark = "†" if (r["a"] in one_run) != (r["b"] in one_run) else ""
                md.append(f"| {r['a']} | {r['b']} | {r['n']} | {r['diff']:+.3f} | {r['nonzero_families']} | {fmtp(r['p'])}{mark} | {fmtp(r['p_holm'])}{mark} | {fmtp(s['p_median']) if s else '—'} | {fmt(s['survive_share']) if s else '—'} |")
            md += ["", "† One run against three: the sign-flip is not exchangeable (a 0/1 score against thirds), so this p is descriptive and the single-run columns are the test for that pair. "
                   "The single-run p inside the 200 draws enumerates exactly up to 12 non-zero families and uses 4,000 Monte Carlo assignments above that, so its resolution is 1/4,001."
                   + (" Every family holds one real case, so the recall sign-flip equals the per-case sign-flip." if fam == "recall" else "")]
    hd = report.get("harness")
    if hd:
        md += ["", "## Harness decomposition (a Claude model in the SWE-2 condition: files inline, no tools; specified before the runs)", "",
               "| lane | runs | missing slots | AUROC [95% CI] | Brier | recall | specificity | accuracy | mean tool calls | reported spend |", "|---|---|---|---|---|---|---|---|---|---|"]
        for name, r in hd["lanes"].items():
            m, ci, f, c = r["metrics"], r["ci"], r["failures"], r["cost"]
            md.append(f"| {name} | {r['rows']} | {len(f['missing']['infrastructure']) + len(f['missing']['model'])} | {fmt(m['auroc'], False)} [{fmt(ci['auroc'][0], False, 4)}, {fmt(ci['auroc'][1], False, 4)}] | "
                      f"{fmt(m['brier'], False)} | {fmt(m['recall'])} | {fmt(m['specificity'])} | {fmt(m['accuracy'])} | {c['mean_tool_calls']:.1f} | {c['reported_cost_usd']:.2f} |")
        md += ["", "Planned contrasts, Holm within each metric across the contrasts with data:", "",
               "| A | B | n | AUROC A−B [95% CI] | tail p (Holm) | reflected p (Holm) | accuracy A−B (Holm) | recall A−B (Holm) | specificity A−B (Holm) |", "|---|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(hd["contrasts"]["auroc"]):
            sec = {fam: hd["contrasts"][fam][i] for fam in ("accuracy", "recall", "specificity")}
            md.append(f"| {r['a']} | {r['b']} | {r['n']} | {r['diff']:+.3f} [{r['ci'][0]:+.4f}, {r['ci'][1]:+.4f}] | {fmtp(r['p'], r.get('p_floored'))} ({fmtp(r['p_holm'], r.get('p_floored'))}) | "
                      f"{fmtp(r['p_centred'], r.get('p_centred_floored'))} ({fmtp(r['p_centred_holm'], r.get('p_centred_floored'))}) | "
                      + " | ".join(f"{sec[fam]['diff']:+.3f} ({fmtp(sec[fam]['p_holm'])})" for fam in ("accuracy", "recall", "specificity")) + " |")
        md += ["", "Share of the tooled-lane-minus-SWE-2 difference that the condition (files inline, no tools) accounts for, (tooled − inline) / (tooled − SWE-2), with a claim-family bootstrap interval:", "",
               "| model | metric | tooled − SWE-2 | tooled − inline | share [95% CI] | draws |", "|---|---|---|---|---|---|"]
        for model, d in hd["shares"].items():
            for key, v in d.items():
                md.append(f"| {model} | {key} | {v['gap']:+.3f} | {v['condition']:+.3f} | {fmt(v['share'], False, 2)} [{fmt(v['share_ci'][0], False, 2)}, {fmt(v['share_ci'][1], False, 2)}] | {v['draws']} |")
    md += ["", "## Disagreements (strict majority of completed runs contradicts the label)", "",
           "A case is listed when more than half of its completed runs fall on the wrong side of 0.5; its mean p_true can still sit on the label's side when the runs split (Opus `0819-openagents-citations`, runs 0.8/0.45/0.3).", ""]
    for lane, items in report["disagreements"].items():
        md.append(f"- {lane}: {len(items)} — " + ", ".join(f"{cid} ({src}, label {lab}, p {p})" for cid, src, lab, p, _ in items))
    return "\n".join(md) + "\n"


def main():
    sources, labels = case_sources()
    families = claim_families(sources)
    cases = json.loads(CASES.read_text())["cases"]
    rng = random.Random(SEED)
    tables, rows_by_lane = {}, {}
    fam_sizes = collections.Counter(families.values())
    report = {"lanes": {}, "bootstrap_draws": BOOT, "seed": SEED, "families": len(fam_sizes), "largest_family": max(fam_sizes.values())}
    original_ids = [c for c, s in sources.items() if s == "original"]
    inside_ids = [c for c in sources if c not in OUTSIDE_FILES]
    baseline_rep0 = {(r["prompt_id"], r["rep"]) for r in load_lane(["baseline"])[0] if r["rep"] == 0}
    for lane, variants in LANES.items():
        rows, errors = load_lane(variants)
        if not rows:
            continue
        done = {(r["prompt_id"], r["rep"]) for r in rows}
        failures = classify_errors(errors, done)
        table, mismatches = case_table(rows, labels)
        tables[lane], rows_by_lane[lane] = table, rows
        fw = [tuple(x) for x in failures["missing"]["model"]]
        sens = {
            "failed_wrong": metrics_of(case_table(rows, labels, failed_wrong=fw)[0]),
            "t0.4": metrics_of(case_table(rows, labels, threshold=0.4)[0]),
            "t0.6": metrics_of(case_table(rows, labels, threshold=0.6)[0]),
            "without_outside_files": metrics_of(table, inside_ids),
        }
        if lane == "Opus 5.5":
            later = [r for r in rows if (r["prompt_id"], r["rep"]) not in baseline_rep0]
            sens["opus_1017"] = metrics_of(case_table(later, labels)[0])
        limits = limit_rows(variants)
        at_limit = set(limits["cut"]) | set(limits["turn_ceiling"])
        sens["without_limit_rows"] = metrics_of(case_table([r for r in rows if (r["prompt_id"], r["rep"]) not in at_limit], labels)[0])
        report["lanes"][lane] = {
            "variants": variants, "rows": len(rows), "failures": failures, "limit_rows": limits,
            "grade_mismatches": mismatches,
            "metrics": metrics_of(table), "ci": family_bootstrap(table, families, rng),
            "original": {"metrics": metrics_of(table, original_ids), "ci": family_bootstrap(table, families, rng, original_ids)},
            "consistency": consistency(table), "per_source": per_source(table, sources), "sensitivity": sens,
        }
    right = sum(1 for c, s in sources.items() if (s == "original") == (labels[c] == 1))
    report["source_rule"] = {"right": right, "n": len(sources), "accuracy": right / len(sources)}
    repos = collections.defaultdict(lambda: [0, 0])
    for c in cases:
        repos[c.get("repo") or "TheBenMeadows/tbm"][0] += 1
        repos[c.get("repo") or "TheBenMeadows/tbm"][1] += c["label"]
    report["repos"] = {k: tuple(v) for k, v in repos.items()}
    # Each block draws from its own seeded stream, so a change in one block leaves the others' draws unchanged.
    report["comparisons"] = compare(tables, families, random.Random(SEED + 1), rows_by_lane, labels, single_auroc_draws=0 if BOOT < 10000 else 1000)
    report["original_comparisons"] = compare(tables, families, random.Random(SEED + 2), rows_by_lane, labels, ids=set(original_ids), with_single=False)
    report["inside_comparisons"] = compare(tables, families, random.Random(SEED + 3), rows_by_lane, labels, ids=set(inside_ids), with_single=False)
    fw_tables = {lane: case_table(rows_by_lane[lane], labels, failed_wrong=[tuple(x) for x in report["lanes"][lane]["failures"]["missing"]["model"]])[0] for lane in tables}
    report["failed_wrong_comparisons"] = compare(fw_tables, families, random.Random(SEED + 4), rows_by_lane, labels, with_single=False)
    opus_rows = rows_by_lane.get("Opus 5.5", [])
    non_squint = [c for c in sources if sources[c] != "squint"]
    report["opus_batches"] = {
        "2026-10-12 (baseline rep 0, 130 cases)": metrics_of(case_table([r for r in opus_rows if (r["prompt_id"], r["rep"]) in baseline_rep0], labels)[0], non_squint),
        "2026-10-17 (baseline reps 1-2, same 130 cases)": metrics_of(case_table([r for r in opus_rows if (r["prompt_id"], r["rep"]) not in baseline_rep0 and sources[r["prompt_id"]] != "squint"], labels)[0], non_squint),
    }
    for key, scenarios, base in (("label_sensitivity", LABEL_SCENARIOS, 10), ("target_definition", TARGET_SCENARIOS, 30)):
        report[key] = {}
        for i, (name, overrides) in enumerate(scenarios.items()):
            alt = dict(labels, **overrides)
            alt_tables = {lane: case_table(rows_by_lane[lane], alt)[0] for lane in tables}
            report[key][name] = {
                "overrides": overrides, "real": sum(1 for v in alt.values() if v == 1), "false": sum(1 for v in alt.values() if v == 0),
                "lanes": {lane: metrics_of(t) for lane, t in alt_tables.items()},
                "comparisons": compare(alt_tables, families, random.Random(SEED + base + i), rows_by_lane, alt),
            }
    report["mutation_classes"] = mutation_classes(tables, sources)
    report["calibration"] = {lane: calibration(t) for lane, t in tables.items()}
    report["cost"] = {lane: lane_cost(rows_by_lane[lane]) for lane in tables}
    report["fable_variability"] = fable_variability(rows_by_lane, labels)
    report["harness"] = harness_decomposition(tables, rows_by_lane, families, labels, random.Random(SEED + 50))
    report["inline_limit_rows"] = {f"{name} inline": limit_rows(variants) for name, variants in INLINE_LANES.items()
                                   if any((FLOW / v / "results.jsonl").exists() for v in variants)}
    report["disagreements"] = disagreements(tables, sources)
    OUT.mkdir(exist_ok=True)
    (OUT / "analysis.json").write_text(json.dumps(report, indent=1, default=str) + "\n")
    (OUT / "analysis.md").write_text(render(report))
    for lane, r in report["lanes"].items():
        print(f"{lane}: rows {r['rows']}, grade mismatches {r['grade_mismatches']}, missing {r['failures']['missing']}")
    print(f"-> {OUT / 'analysis.md'}")


if __name__ == "__main__":
    main()
