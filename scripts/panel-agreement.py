#!/opt/homebrew/bin/python3
"""Blind-panel agreement with the owner's labels.

Reads the panel flow (panel): v1 = Gemini 4 Argon, v2 = Kimi K3,
v3-grok = Grok 4.7. A panel model's label is p_true >= 0.5. Reports Cohen's kappa
per seat against the owner, Fleiss' kappa across the three seats, the panel
majority against the owner (all cases, per source, and on the cases whose
refutation is visible in the pinned files), the number of exact-0.50 votes, and
every case where the panel majority disagrees with the owner.

    scripts/panel-agreement.py
"""
import collections
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
PANEL = HERE / "panel"
CASES = HERE / "runs" / "cases-paper-144.json"
SEATS = {"Gemini 4 Argon": "v1", "Kimi K3": "v2", "Grok 4.7": "v3-grok"}
FLAGGED = {"0819-infra-los-angeles", "0819-tezos-editions", "0819-openagents-citations"}
# The owner's refutation rests on evidence outside the pinned files (a dependency,
# a live header default, a rendered image, dead URLs, intended behaviour).
OUTSIDE_FILES = {"cookie-tab-cb74f3a-fragment-stale-pay", "orthodoxprayers-af4e178-headers-miss-pages",
                 "squint-c7ea926-icc-torn-chain", "squint-ec53337-upside-down", "tbm-96d7b9d-localecompare-lang",
                 "tbm-96d7b9d-pre-indent", "0819-foundation-dead", "0927-dead-links-2025"}
OUT = PANEL / "agreement.md"


def read_jsonl(p):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def cohen(a, b, ids=None):
    ids = sorted((set(a) & set(b)) if ids is None else (set(a) & set(b) & set(ids)))
    if not ids:
        return math.nan, 0, math.nan
    po = sum(1 for c in ids if a[c] == b[c]) / len(ids)
    pa1, pb1 = sum(a[c] for c in ids) / len(ids), sum(b[c] for c in ids) / len(ids)
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    if pb1 in (0.0, 1.0):  # one owner class only: kappa is 0 by construction, so it says nothing
        return math.nan, len(ids), po
    return ((po - pe) / (1 - pe) if pe < 1 else math.nan), len(ids), po


def fleiss(votes):
    rows = [v for v in votes.values() if len(v) == max(len(x) for x in votes.values())]
    n = len(rows[0])
    if n < 2 or not rows:
        return math.nan
    p1 = sum(sum(v) for v in rows) / (n * len(rows))
    pe = p1 ** 2 + (1 - p1) ** 2
    po = sum((sum(v) ** 2 + (n - sum(v)) ** 2 - n) / (n * (n - 1)) for v in rows) / len(rows)
    return (po - pe) / (1 - pe) if pe < 1 else math.nan


def main():
    cases = {c["id"]: c for c in json.loads(CASES.read_text())["cases"]}
    for c in cases.values():  # the analysis reports Squint council cases as their own source
        if c.get("repo") == "mdws-org/squint":
            c["source"] = "squint"
    owner = {cid: c["label"] for cid, c in cases.items()}
    seat_labels, seat_p = {}, {}
    for seat, var in SEATS.items():
        rows = read_jsonl(PANEL / var / "results.jsonl")
        seat_labels[seat] = {r["prompt_id"]: 1 if float(r["grade"]["p_true"]) >= 0.5 else 0 for r in rows if r.get("status", "ok") == "ok"}
        seat_p[seat] = {r["prompt_id"]: float(r["grade"]["p_true"]) for r in rows if r.get("status", "ok") == "ok"}
    half = {seat: sum(1 for v in p.values() if v == 0.5) for seat, p in seat_p.items()}
    md = ["# Blind panel agreement with the owner's labels", "",
          "Each seat saw only the claim and the files the claim names at the pinned commit; a seat's label is p_true ≥ 0.5, so a 0.50 (\"could not tell\") counts as real. "
          "Agreement is between three models and the owner, who wrote or ruled on every label; it measures consistency under an artifact-only information ceiling, not correctness.", ""]
    md += ["| seat | cases | agree with owner | Cohen's kappa | votes at exactly 0.50 |", "|---|---|---|---|---|"]
    for seat, lab in seat_labels.items():
        k, n, po = cohen(lab, owner)
        md.append(f"| {seat} | {n} | {100 * po:.1f}% | {k:.3f} | {half[seat]} |")
    votes = {cid: [seat_labels[s][cid] for s in SEATS if cid in seat_labels[s]] for cid in cases}
    votes = {c: v for c, v in votes.items() if v}
    full = {c: v for c, v in votes.items() if len(v) == len(SEATS)}
    md += ["", f"Fleiss' kappa across the three seats on the {len(full)} cases all three labelled: {fleiss(full):.3f}", ""]
    maj = {c: 1 if 2 * sum(v) > len(v) else 0 if 2 * sum(v) < len(v) else None for c, v in votes.items()}
    decided = {c: m for c, m in maj.items() if m is not None}
    k, n, po = cohen(decided, owner)
    md += [f"Panel majority against the owner, all cases: {n} decided, agreement {100 * po:.1f}%, Cohen's kappa {k:.3f}; {sum(1 for m in maj.values() if m is None)} split or single-seat cases.", ""]
    md += ["| subset | n | agreement | kappa |", "|---|---|---|---|"]
    for src in ("original", "mutated", "council", "squint"):
        ids = [c for c in decided if cases[c]["source"] == src]
        k, n, po = cohen(decided, owner, ids)
        md.append(f"| {src} | {n} | {100 * po:.1f}% | {'n/a (one owner class)' if math.isnan(k) else f'{k:.3f}'} |")
    ids = [c for c in decided if c not in OUTSIDE_FILES]
    k, n, po = cohen(decided, owner, ids)
    md.append(f"| excluding the {len(OUTSIDE_FILES)} outside-files cases (all of them disputes, so the agreeing count is unchanged) | {n} | {100 * po:.1f}% | {k:.3f} |")
    # How the >= 0.5 convention cut: majority verdicts that change when a 0.50 vote counts as false instead.
    strict = {c: 1 if 2 * sum(1 for s in SEATS if seat_p[s].get(c, 0) > 0.5) > len(v) else 0 for c, v in votes.items()}
    flips = sorted(c for c in decided if strict[c] != decided[c])
    md += ["", f"Seat votes at exactly 0.50: {sum(half.values())} of {3 * len(cases)}. Counting 0.50 as false instead of real would change the panel majority on {len(flips)} cases: "
           + ", ".join(f"{c} (owner {owner[c]}, {'dispute → agreement' if strict[c] == owner[c] else 'agreement → dispute'})" for c in flips) + "."]
    md += ["", "## Cases where the panel majority disagrees with the owner", "",
           "| case | source | owner | panel votes (Argon, K3, Grok) | p_true | class |", "|---|---|---|---|---|---|"]
    for cid in sorted(decided, key=lambda c: (cases[c]["source"], c)):
        if decided[cid] != owner[cid]:
            ps = ", ".join(f"{seat_p[s].get(cid, float('nan')):.2f}" for s in SEATS)
            cls = ("owner-flagged, sensitivity row" if cid in FLAGGED else "materiality rule, sensitivity row" if cid in ("C-onion-search-count", "C-pendulum-button-count")
                   else "refutation outside the pinned files" if cid in OUTSIDE_FILES else "every vote within 0.02 of 0.50 (could not tell)" if all(abs(seat_p[s].get(cid, 0) - 0.5) <= 0.02 for s in SEATS) else "")
            md.append(f"| {cid} | {cases[cid]['source']} | {owner[cid]} | {votes[cid]} | {ps} | {cls} |")
    md += ["", "## Owner-flagged cases", "", "| case | owner | panel votes | p_true | majority dispute |", "|---|---|---|---|---|"]
    for cid in sorted(FLAGGED):
        md.append(f"| {cid} | {owner[cid]} | {votes.get(cid)} | " + ", ".join(f"{seat_p[s].get(cid, float('nan')):.2f}" for s in SEATS) + f" | {'yes' if decided.get(cid) != owner[cid] else 'no'} |")
    OUT.write_text("\n".join(md) + "\n")
    print("\n".join(md[:14]))
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
