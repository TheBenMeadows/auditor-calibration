#!/opt/homebrew/bin/python3
"""Assemble the paper's case file from the four sources.

    build-paper-cases.py [--rulings rulings.json] [--include-squint] --out cases-paper.json

Sources: cases.json (the 59 original cases, maintainer-ruled); the council-refuted
cases (measured refutations, label 0); the mutated-false cases (constructed,
label 0, a 20-case sample adjudicated by the maintainer); the fresh audit
claims (maintainer-ruled, labels from the rulings file). A fresh claim without
a ruling, or ruled "can't tell", is left out and counted. A mutated case whose
sampled adjudication disagreed with the author's label is left out and counted;
one ruled "can't tell" is kept with its constructed label but not counted as
adjudicated. A ruling carries the maintainer's blind label (initial_label) and
whether it was revised after the second-rater reveal; both ride on the case so
the paper can report them. Squint cases sit on commits that are not on GitHub
until pushed; they are excluded unless --include-squint is given.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = ROOT / "sources"
REFS = {"0819": "7f50013b094028da0b9630b5972971ecd16e3d68",
        "0927": "96d7b9d6b5f8b14dab6a342a83b3c3c4f0b6e324",
        "1007": "ca0b665264e45e7c3e76b04f90326e48c5336fdd"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rulings", default=str(SRC / "rulings.json"))
    ap.add_argument("--mutated", default=str(SRC / "mutated-cases.json"))
    ap.add_argument("--include-squint", action="store_true")
    ap.add_argument("--out", default=str(HERE / "cases-paper.json"))
    a = ap.parse_args()

    base = json.loads((HERE / "cases.json").read_text())
    rulings = json.loads(Path(a.rulings).read_text()) if Path(a.rulings).exists() else {}
    council = json.loads((SRC / "council-cases.json").read_text())
    # The full 53-case mutated set lived only in a job directory that was
    # deleted on 2026-10-11; unless it is restored, the 20 cases of the
    # adjudicated sample (kept in ruling-candidates.json) are the mutated set.
    mutated_path = Path(a.mutated) if Path(a.mutated).exists() else SRC / "mutated-sample-20.json"
    mutated = json.loads(mutated_path.read_text())
    print(f"mutated source: {mutated_path} ({len(mutated)} cases)")
    fresh = json.loads((SRC / "fresh-claims.json").read_text())
    skipped = Counter()
    cases = []

    def ruling_fields(r):
        return {"initial_label": r.get("initial_label", r.get("label")), "revised": bool(r.get("revised", False))}

    for c in base["cases"]:
        cases.append({**c, "source": "original"})

    for c in council:
        if c["repo"] == "mdws-org/squint" and not a.include_squint:
            skipped["council: squint (commits not on GitHub)"] += 1
            continue
        cases.append({k: v for k, v in c.items() if k != "refutation_private"} | {"source": "council"})

    for c in mutated:
        r = rulings.get(c["id"])
        decided = r is not None and r.get("label") is not None
        if decided and r["label"] != 0:
            skipped["mutated: maintainer disagreed with the author's label"] += 1
            continue
        if r is not None and not decided:
            skipped["mutated: sampled but ruled can't tell (kept, not adjudicated)"] += 1
        cases.append({k: v for k, v in c.items() if k != "why_false"}
                     | {"source": "mutated", "adjudicated": decided} | (ruling_fields(r) if decided else {}))

    for c in fresh:
        r = rulings.get(c["id"])
        if r is None:
            skipped["fresh: not yet ruled"] += 1
            continue
        if r.get("label") is None:
            skipped["fresh: ruled can't tell"] += 1
            continue
        cases.append({k: v for k, v in c.items() if k not in ("worker_confidence", "worker_evidence")}
                     | {"label": r["label"], "source": "fresh", "worker_confidence": c.get("worker_confidence")}
                     | ruling_fields(r))

    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids)), "duplicate case id"
    out = {"_comment": "Paper case set. label 1 = real finding, 0 = refuted. source = original|council|mutated|fresh. "
                       "Cases without repo/ref inherit repo and refs[audit].",
           "repo": base["repo"], "refs": base["refs"] | {"1007": {"sha": REFS["1007"], "audit": "fresh five-lens audit 2026-10-07"}},
           "cases": cases}
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n")
    by = Counter((c["source"], c["label"]) for c in cases)
    print(f"{len(cases)} cases -> {a.out}")
    for (src, lab), n in sorted(by.items()):
        print(f"  {src:9s} label={lab}: {n}")
    revised = [c["id"] for c in cases if c.get("revised")]
    print(f"  revised after the second-rater reveal: {len(revised)}" + (f" ({', '.join(revised)})" if revised else ""))
    for k, n in skipped.items():
        print(f"  skipped {n}: {k}")


if __name__ == "__main__":
    main()
