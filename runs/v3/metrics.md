# v3: Orrery finding-precision eval

14 cases scored (0 kept, 14 refuted), 42 rep rows, 0 failed attempt(s) in errors.jsonl (not in the means).

| metric | value |
|---|---|
| recall (kept scored real at p≥0.5) | n/a |
| specificity (refuted scored not-real at p≥0.5) | 88.1% (95% CI 62.8%–97.0%) |
| AUROC of p_true (kept vs refuted) | n/a |
| Brier (lower is better) | 0.081 |
| bare verdict agreement (true=1, partial=0.5, false=0) | 86.9% |
| mean p_true on kept / on refuted | NaN / 0.18 |
| rep-to-rep spread of p_true (mean, max) | 0.08, 0.60 |
| all: correct on ≥1 of k=3 reps / on every rep (14 cases) | 92.9% (95% CI 68.5%–98.7%) / 85.7% (95% CI 60.1%–96.0%) |
| all: correct by majority of reps / split cases / split cases outvoted | 85.7% (95% CI 60.1%–96.0%) / 1 / 1 |
| refuted: correct on ≥1 of k=3 reps / on every rep (14 cases) | 92.9% (95% CI 68.5%–98.7%) / 85.7% (95% CI 60.1%–96.0%) |
| refuted: correct by majority of reps / split cases / split cases outvoted | 85.7% (95% CI 60.1%–96.0%) / 1 / 1 |
| mean latency / tool calls / cost per rep | 60 s / 3.1 / $0.129 |
| total reported cost | $5.43 |

## Refuted cases (specificity, one line each)

| case | p_true | correct |
|---|---|---|
| squint-ec53337-upside-down | 0.06 | 1 |
| squint-ec53337-index0-primary | 0.11 | 1 |
| squint-ec53337-byte-order-constant | 0.11 | 1 |
| squint-ec53337-hdr-highlight-clamp | 0.13 | 1 |
| squint-c7ea926-vp8x-not-picture | 0.05 | 1 |
| squint-c7ea926-vp8x-flag-clear-safe | 0.57 | 0.3333333333333333 |
| squint-c7ea926-zero-length-picture | 0.10 | 1 |
| squint-c7ea926-icc-torn-chain | 0.78 | 0 |
| squint-f4890dd-pdf-shrink-memory | 0.15 | 1 |
| squint-f4890dd-heif-readmits-avif | 0.10 | 1 |
| squint-f4890dd-job-mode-stored | 0.04 | 1 |
| squint-f4890dd-animated-keeps-one-frame | 0.07 | 1 |
| squint-f4890dd-unicode-landsonsource | 0.08 | 1 |
| squint-f4890dd-strip-identical-done | 0.11 | 1 |

## Kept cases scored below 0.5

none
