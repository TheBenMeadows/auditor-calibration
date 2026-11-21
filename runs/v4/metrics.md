# v4: Orrery finding-precision eval

144 cases scored (52 kept, 92 refuted), 431 rep rows, 1 failed attempt(s) in errors.jsonl (not in the means).

| metric | value |
|---|---|
| recall (kept scored real at p≥0.5) | 94.9% (95% CI 85.2%–98.3%) |
| specificity (refuted scored not-real at p≥0.5) | 92.8% (95% CI 85.6%–96.5%) |
| AUROC of p_true (kept vs refuted) | 0.982 |
| Brier (lower is better) | 0.052 |
| bare verdict agreement (true=1, partial=0.5, false=0) | 89.5% |
| mean p_true on kept / on refuted | 0.83 / 0.11 |
| rep-to-rep spread of p_true (mean, max) | 0.07, 0.92 |
| all: correct on ≥1 of k=2/3 reps / on every rep (144 cases) | 95.1% (95% CI 90.3%–97.6%) / 91.0% (95% CI 85.2%–94.6%) |
| all: correct by majority of reps / split cases / split cases outvoted | 94.4% (95% CI 89.4%–97.2%) / 6 / 1 |
| kept: correct on ≥1 of k=2/3 reps / on every rep (52 cases) | 98.1% (95% CI 89.9%–99.7%) / 90.4% (95% CI 79.4%–95.8%) |
| kept: correct by majority of reps / split cases / split cases outvoted | 96.2% (95% CI 87.0%–98.9%) / 4 / 1 |
| refuted: correct on ≥1 of k=2/3 reps / on every rep (92 cases) | 93.5% (95% CI 86.5%–97.0%) / 91.3% (95% CI 83.8%–95.5%) |
| refuted: correct by majority of reps / split cases / split cases outvoted | 93.5% (95% CI 86.5%–97.0%) / 2 / 0 |
| mean latency / tool calls / cost per rep | 36 s / 2.9 / $0.053 |
| total reported cost | $22.72 |

## Refuted cases (specificity, one line each)

| case | p_true | correct |
|---|---|---|
| 0819-sign-release-exit | 0.16 | 1 |
| 0819-theme-toggle-name | 0.12 | 1 |
| 0927-jsonld-csp | 0.04 | 1 |
| 0927-unlisted-feed-leak | 0.03 | 1 |
| 0927-indent-outside-pre | 0.13 | 1 |
| 0819-sitemap-missing-blog | 0.03 | 1 |
| 0819-infra-los-angeles | 0.88 | 0 |
| squint-ec53337-upside-down | 0.04 | 1 |
| squint-ec53337-index0-primary | 0.35 | 1 |
| squint-ec53337-byte-order-constant | 0.15 | 1 |
| squint-ec53337-hdr-highlight-clamp | 0.16 | 1 |
| squint-c7ea926-vp8x-not-picture | 0.10 | 1 |
| squint-c7ea926-vp8x-flag-clear-safe | 0.84 | 0 |
| squint-c7ea926-zero-length-picture | 0.12 | 1 |
| squint-c7ea926-icc-torn-chain | 0.36 | 0.6666666666666666 |
| squint-f4890dd-pdf-shrink-memory | 0.22 | 1 |
| squint-f4890dd-heif-readmits-avif | 0.12 | 1 |
| squint-f4890dd-job-mode-stored | 0.03 | 1 |
| squint-f4890dd-animated-keeps-one-frame | 0.06 | 1 |
| squint-f4890dd-unicode-landsonsource | 0.09 | 1 |
| squint-f4890dd-strip-identical-done | 0.10 | 1 |
| tbm-96d7b9d-jsonld-csp | 0.04 | 1 |
| tbm-96d7b9d-unlisted-feed-leak | 0.04 | 1 |
| tbm-96d7b9d-pre-indent | 0.41 | 0.6666666666666666 |
| tbm-96d7b9d-localecompare-lang | 0.61 | 0 |
| cookie-tab-b8635c1-stale-txshape | 0.06 | 1 |
| cookie-tab-cb74f3a-open-amount-override | 0.04 | 1 |
| cookie-tab-cb74f3a-split-balance | 0.04 | 1 |
| cookie-tab-cb74f3a-base58-cook-suffix | 0.02 | 1 |
| cookie-tab-cb74f3a-null-memo-drops | 0.04 | 1 |
| cookie-tab-cb74f3a-live-check-missing | 0.02 | 1 |
| cookie-tab-cb74f3a-fragment-stale-pay | 0.77 | 0 |
| cookie-tab-3cbeedc-memo-pipe-injection | 0.04 | 1 |
| cookie-tab-3cbeedc-wrapped-cook-trapped | 0.03 | 1 |
| cookie-tab-3cbeedc-second-memo-prefilter | 0.12 | 1 |
| cookie-tab-3cbeedc-usdtoraw-subunit | 0.05 | 1 |
| orthodoxprayers-af4e178-headers-miss-pages | 0.22 | 1 |
| orthodoxprayers-af4e178-indented-selector | 0.06 | 1 |
| orthodoxprayers-af4e178-opening-dead-rule | 0.04 | 1 |
| orthodoxprayers-af4e178-no-focus-ring | 0.06 | 1 |
| A-cache-porcine-fonts | 0.03 | 1 |
| A-charset-home | 0.02 | 1 |
| A-alt-working-log | 0.03 | 1 |
| A-heading-projects | 0.02 | 1 |
| A-dup-font-porcine | 0.02 | 1 |
| A-pre-light-essentialism | 0.03 | 1 |
| A-search-index-list | 0.04 | 1 |
| A-blog-cleanup | 0.04 | 1 |
| A-readme-check-ports | 0.03 | 1 |
| A-dls-lazy-lead | 0.04 | 1 |
| A-ai-escaping | 0.06 | 1 |
| A-empty-link-ordinals | 0.06 | 1 |
| A-headers-older-sections | 0.03 | 1 |
| B-headers-onion-glued | 0.03 | 1 |
| B-manifest-guard-gap | 0.07 | 1 |
| B-blog-raw-html | 0.03 | 1 |
| B-headers-cache-coverage | 0.03 | 1 |
| B-build-feed-empty | 0.03 | 1 |
| B-build-stamp-skips | 0.04 | 1 |
| B-npmrc-comment | 0.04 | 1 |
| B-check-readme-unrun | 0.03 | 1 |
| B-search-focus-trap | 0.06 | 1 |
| B-pendulum-names | 0.06 | 1 |
| B-poap-vault-tabs | 0.04 | 1 |
| B-youtube-relme | 0.03 | 1 |
| B-home-heading-outline | 0.03 | 1 |
| C-onion-search-count | 0.63 | 0 |
| C-guard-no-dupes | 0.07 | 1 |
| C-pendulum-button-count | 0.83 | 0 |
| C-eth-duplicate-card | 0.10 | 1 |
| C-stamp-list-ai | 0.03 | 1 |
| C-tailwind-marfa | 0.02 | 1 |
| C-speaking-origin-raw | 0.03 | 1 |
| C-ai-dates-rendered | 0.05 | 1 |
| C-mirrors-check-host-only | 0.04 | 1 |
| C-feed-build-clock | 0.35 | 1 |
| C-dls-alt | 0.08 | 1 |
| C-frontmatter-date-direction | 0.04 | 1 |
| C-readme-never-run | 0.03 | 1 |
| D-ai-unescaped-summary | 0.04 | 1 |
| D-ai-wins-http | 0.03 | 1 |
| D-ai-links-ci-403 | 0.04 | 1 |
| D-speaking-raw-html | 0.03 | 1 |
| D-search-index-unlisted | 0.03 | 1 |
| D-blog-related-silent | 0.03 | 1 |
| D-feed-subject-raw | 0.04 | 1 |
| D-sign-release-sec-argv | 0.04 | 1 |
| D-version-css-silent | 0.03 | 1 |
| D-manifest-build-clock | 0.03 | 1 |
| D-onchain-check-tzkt | 0.02 | 1 |
| D-readme-raw-slug | 0.03 | 1 |
| D-me-webp-cache | 0.02 | 1 |

## Kept cases scored below 0.5

| case | p_true |
|---|---|
| 0819-openagents-citations | 0.48 |
| 0819-tezos-editions | 0.30 |
| 0927-squint-signed-claim | 0.48 |
