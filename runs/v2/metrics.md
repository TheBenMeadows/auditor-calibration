# v2: Orrery finding-precision eval

107 cases scored (52 kept, 55 refuted), 314 rep rows, 118 failed attempt(s) in errors.jsonl (not in the means).

| metric | value |
|---|---|
| recall (kept scored real at p≥0.5) | 94.9% (95% CI 85.2%–98.3%) |
| specificity (refuted scored not-real at p≥0.5) | 89.1% (95% CI 78.2%–94.9%) |
| AUROC of p_true (kept vs refuted) | 0.981 |
| Brier (lower is better) | 0.062 |
| bare verdict agreement (true=1, partial=0.5, false=0) | 87.5% |
| mean p_true on kept / on refuted | 0.87 / 0.15 |
| rep-to-rep spread of p_true (mean, max) | 0.10, 0.68 |
| all: correct on ≥1 of k=2/3 reps / on every rep (105 cases) | 96.2% (95% CI 90.6%–98.5%) / 86.7% (95% CI 78.9%–91.9%) |
| all: correct by majority of reps / split cases / split cases outvoted | 92.4% (95% CI 85.7%–96.1%) / 10 / 4 |
| kept: correct on ≥1 of k=2/3 reps / on every rep (52 cases) | 98.1% (95% CI 89.9%–99.7%) / 92.3% (95% CI 81.8%–97.0%) |
| kept: correct by majority of reps / split cases / split cases outvoted | 94.2% (95% CI 84.4%–98.0%) / 3 / 2 |
| refuted: correct on ≥1 of k=2/3 reps / on every rep (53 cases) | 94.3% (95% CI 84.6%–98.1%) / 81.1% (95% CI 68.6%–89.4%) |
| refuted: correct by majority of reps / split cases / split cases outvoted | 90.6% (95% CI 79.7%–95.9%) / 7 / 2 |
| mean latency / tool calls / cost per rep | 116 s / 15.9 / $0.653 |
| total reported cost | $205.01 |

## Refuted cases (specificity, one line each)

| case | p_true | correct |
|---|---|---|
| 0819-sign-release-exit | 0.18 | 1 |
| 0819-theme-toggle-name | 0.16 | 1 |
| 0927-jsonld-csp | 0.03 | 1 |
| 0927-unlisted-feed-leak | 0.03 | 1 |
| 0927-indent-outside-pre | 0.88 | 0 |
| 0819-sitemap-missing-blog | 0.03 | 1 |
| 0819-infra-los-angeles | 0.57 | 0.3333333333333333 |
| squint-ec53337-index0-primary | 0.17 | 1 |
| squint-ec53337-upside-down | 0.04 | 1 |
| squint-ec53337-byte-order-constant | 0.43 | 0.6666666666666666 |
| squint-ec53337-hdr-highlight-clamp | 0.08 | 1 |
| squint-c7ea926-vp8x-not-picture | 0.13 | 1 |
| squint-c7ea926-vp8x-flag-clear-safe | 0.64 | 0.3333333333333333 |
| squint-c7ea926-zero-length-picture | 0.32 | 1 |
| squint-f4890dd-pdf-shrink-memory | 0.37 | 0.6666666666666666 |
| squint-c7ea926-icc-torn-chain | 0.86 | 0 |
| squint-f4890dd-job-mode-stored | 0.03 | 1 |
| squint-f4890dd-heif-readmits-avif | 0.05 | 1 |
| squint-f4890dd-animated-keeps-one-frame | 0.03 | 1 |
| squint-f4890dd-unicode-landsonsource | 0.07 | 1 |
| squint-f4890dd-strip-identical-done | 0.26 | 0.6666666666666666 |
| tbm-96d7b9d-jsonld-csp | 0.03 | 1 |
| tbm-96d7b9d-unlisted-feed-leak | 0.03 | 1 |
| tbm-96d7b9d-pre-indent | 0.90 | 0 |
| tbm-96d7b9d-localecompare-lang | 0.44 | 0.6666666666666666 |
| cookie-tab-b8635c1-stale-txshape | 0.04 | 1 |
| cookie-tab-cb74f3a-open-amount-override | 0.04 | 1 |
| cookie-tab-cb74f3a-split-balance | 0.04 | 1 |
| cookie-tab-cb74f3a-null-memo-drops | 0.04 | 1 |
| cookie-tab-cb74f3a-base58-cook-suffix | 0.02 | 1 |
| cookie-tab-cb74f3a-live-check-missing | 0.02 | 1 |
| cookie-tab-3cbeedc-memo-pipe-injection | 0.03 | 1 |
| cookie-tab-cb74f3a-fragment-stale-pay | 0.32 | 0.6666666666666666 |
| cookie-tab-3cbeedc-wrapped-cook-trapped | 0.04 | 1 |
| cookie-tab-3cbeedc-usdtoraw-subunit | 0.09 | 1 |
| cookie-tab-3cbeedc-second-memo-prefilter | 0.21 | 1 |
| orthodoxprayers-af4e178-headers-miss-pages | 0.16 | 1 |
| orthodoxprayers-af4e178-indented-selector | 0.05 | 1 |
| orthodoxprayers-af4e178-opening-dead-rule | 0.02 | 1 |
| orthodoxprayers-af4e178-no-focus-ring | 0.17 | 1 |
| A-cache-porcine-fonts | 0.02 | 1 |
| A-charset-home | 0.02 | 1 |
| A-alt-working-log | 0.02 | 1 |
| A-heading-projects | 0.02 | 1 |
| A-dup-font-porcine | 0.02 | 1 |
| A-search-index-list | 0.02 | 1 |
| A-pre-light-essentialism | 0.03 | 1 |
| A-blog-cleanup | 0.05 | 1 |
| A-readme-check-ports | 0.03 | 1 |
| A-dls-lazy-lead | 0.02 | 1 |
| A-ai-escaping | 0.06 | 1 |
| A-empty-link-ordinals | 0.02 | 1 |
| A-headers-older-sections | 0.02 | 1 |
| B-headers-onion-glued | 0.02 | 1 |
| B-manifest-guard-gap | 0.05 | 1 |

## Kept cases scored below 0.5

| case | p_true |
|---|---|
| 0819-tezos-editions | 0.23 |
| 0927-tailwind-speaking | 0.47 |
