#!/opt/homebrew/bin/python3
"""Draw the cases for Fable 5.1's second run: a seeded random sample of 60 of the
144 cases, stratified by source and class with largest-remainder allocation
(ties broken by the seeded generator), written as a case file the runner accepts.

    scripts/draw-fable-rerun.py
"""
import collections
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FLOW = ROOT / "runs"
SRC = FLOW / "cases-paper-144.json"
OUT = FLOW / "cases-fable-rerun60.json"
N = 60
SEED = 20261018


def stratum(c):
    src = c.get("source", "original")
    if c.get("repo") == "mdws-org/squint":
        return "squint"
    if src == "original":
        return f"original-{'real' if c['label'] == 1 else 'false'}"
    if src == "mutated":
        return f"mutated-{c['id'][0]}"
    return src


def main():
    doc = json.loads(SRC.read_text())
    cases = doc["cases"]
    rng = random.Random(SEED)
    by = collections.defaultdict(list)
    for c in cases:
        by[stratum(c)].append(c)
    names = sorted(by)
    quota = {s: N * len(by[s]) / len(cases) for s in names}
    alloc = {s: int(quota[s]) for s in names}
    tiebreak = {s: rng.random() for s in names}
    for s in sorted(names, key=lambda s: (-(quota[s] - alloc[s]), tiebreak[s]))[:N - sum(alloc.values())]:
        alloc[s] += 1
    picked = []
    for s in names:
        picked += rng.sample(sorted(by[s], key=lambda c: c["id"]), alloc[s])
    order = {c["id"]: i for i, c in enumerate(cases)}
    picked.sort(key=lambda c: order[c["id"]])
    out = {k: v for k, v in doc.items() if k != "cases"}
    out["cases"] = picked
    out["note"] = f"Seeded stratified draw of {N} of the 144 cases for Fable 5.1's second run (scripts/draw-fable-rerun.py, seed {SEED})."
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    print({s: f"{alloc[s]}/{len(by[s])}" for s in names})
    print(f"{len(picked)} cases -> {OUT}")


if __name__ == "__main__":
    main()
