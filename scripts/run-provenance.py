#!/opt/homebrew/bin/python3
"""Trial count and budget for every paper run, read from the run outputs.

A result reported from one trial, or without the turn and time ceiling it ran
under, cannot be compared with another lane's result. This step states both
for each run and exits 1 when any run lacks either, so a table built on an
unrecorded run fails before it reaches the paper.

    scripts/run-provenance.py [--flow DIR] [--out FILE]

Trials come from the `rep` field of each ok row in <run>/results.jsonl.
Budgets come from <flow>/budgets.json, one entry per run directory:

    {"v7": {"max_turns": 40, "timeout_s": 1800, "source": "v7.log argv"}}

`max_turns` and `timeout_s` are required (use 0 for "no ceiling");
`file_budget_bytes`, `max_output_tokens` and `context_tokens` are optional.
`source` says where the numbers were read from. The approved harness files
are not read or changed.
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
FLOW = HERE / "runs"
REQUIRED = ("max_turns", "timeout_s", "source")
OPTIONAL = ("file_budget_bytes", "max_output_tokens", "context_tokens")


def read_jsonl(path):
    rows = []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def run_dirs(flow):
    return sorted(p for p in flow.iterdir() if (p / "results.jsonl").is_file())


def trials(rows):
    """Per-case trial counts over ok rows: (cases, min, max)."""
    per_case = Counter()
    seen = set()
    for r in rows:
        if r.get("status") != "ok" or "rep" not in r:
            continue
        key = (r["prompt_id"], r["rep"])
        if key not in seen:
            seen.add(key)
            per_case[r["prompt_id"]] += 1
    if not per_case:
        return 0, 0, 0
    return len(per_case), min(per_case.values()), max(per_case.values())


def budget_problems(entry):
    if entry is None:
        return ["no budgets.json entry"]
    return [f"missing {k}" for k in REQUIRED if k not in entry]


def describe(run, budgets):
    meta = {}
    if (run / "run.json").is_file():
        meta = json.loads((run / "run.json").read_text())
    n, lo, hi = trials(read_jsonl(run / "results.jsonl"))
    entry = budgets.get(run.name)
    problems = budget_problems(entry)
    if n == 0:
        problems.insert(0, "no ok rows with a rep field")
    return {"run": run.name, "lane": meta.get("lane", "?"), "model": meta.get("model", "?"),
            "cases": n, "trials": f"{lo}" if lo == hi else f"{lo}-{hi}",
            "budget": entry or {}, "problems": problems}


def fmt_budget(b):
    if not b:
        return "-"
    parts = [f"turns {b['max_turns']}" if "max_turns" in b else None,
             f"timeout {b['timeout_s']}s" if "timeout_s" in b else None]
    parts += [f"{k} {b[k]}" for k in OPTIONAL if k in b]
    return ", ".join(p for p in parts if p)


def table(rows):
    out = ["| run | lane | model | cases | trials/case | budget | status |",
           "|---|---|---|---|---|---|---|"]
    for r in rows:
        status = "ok" if not r["problems"] else "MISSING: " + "; ".join(r["problems"])
        out.append(f"| {r['run']} | {r['lane']} | {r['model']} | {r['cases']} | {r['trials']} "
                   f"| {fmt_budget(r['budget'])} | {status} |")
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--flow", type=Path, default=FLOW)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args(argv)
    bpath = args.flow / "budgets.json"
    budgets = json.loads(bpath.read_text()) if bpath.is_file() else {}
    rows = [describe(r, budgets) for r in run_dirs(args.flow)]
    if not rows:
        print(f"no run directories with results.jsonl under {args.flow}", file=sys.stderr)
        return 1
    text = table(rows)
    if args.out:
        args.out.write_text(text)
    sys.stdout.write(text)
    bad = [r["run"] for r in rows if r["problems"]]
    if bad:
        print(f"{len(bad)} of {len(rows)} runs lack a trial count or budget: {', '.join(bad)}",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
