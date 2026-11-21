#!/opt/homebrew/bin/python3
"""Export every completed paper run to review/p1-results/rows.csv with the
columns the analysis needs to be reproduced from the export alone: lane,
variant, case_id, rep, label, source, family, batch, p_true.

    scripts/export-rows.py
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
FLOW = HERE / "runs"
OUT = HERE / "review" / "p1-results" / "rows.csv"
sys.path.insert(0, str(HERE / "scripts"))
import importlib.util
spec = importlib.util.spec_from_file_location("ap", HERE / "scripts" / "analyze-p1.py")
ap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ap)

LANES = [("Opus 5.5", "baseline"), ("Opus 5.5", "v3"), ("Fable 5.1", "v6"), ("Sonnet 5.5", "v4"),
         ("Haiku 5.5", "v5"), ("SWE-2 High", "v1"), ("DeepSeek Flash", "v2"),
         ("Fable 5.1 rerun", "v7"), ("Haiku 5.5 inline", "v8"), ("Sonnet 5.5 inline", "v9")]  # the last three only when they have rows


def main():
    sources, labels = ap.case_sources()
    families = ap.claim_families(sources)
    n = 0
    with OUT.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["lane", "variant", "case_id", "rep", "label", "source", "family", "batch", "p_true"])
        for lane, v in LANES:
            for r in ap.read_jsonl(FLOW / v / "results.jsonl"):
                if r.get("status") != "ok":
                    continue
                cid = r["prompt_id"]
                batch = "2026-10-12" if v == "baseline" and r["rep"] == 0 else "2026-10-17" if v in ("baseline", "v1", "v2", "v3", "v4", "v5", "v6") else "2026-10-18" if v in ("v7", "v8") else "2026-11"
                w.writerow([lane, v, cid, r["rep"], labels[cid], sources[cid], families[cid], batch, r["grade"]["p_true"]])
                n += 1
    print(f"{OUT}: {n} rows")


if __name__ == "__main__":
    main()
