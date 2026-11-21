# v5: Orrery finding-precision eval

144 cases scored (52 kept, 92 refuted), 416 rep rows, 16 failed attempt(s) in errors.jsonl (not in the means).

| metric | value |
|---|---|
| recall (kept scored real at p≥0.5) | 87.2% (95% CI 75.5%–93.8%) |
| specificity (refuted scored not-real at p≥0.5) | 92.6% (95% CI 85.3%–96.4%) |
| AUROC of p_true (kept vs refuted) | 0.967 |
| Brier (lower is better) | 0.072 |
| bare verdict agreement (true=1, partial=0.5, false=0) | 84.1% |
| mean p_true on kept / on refuted | 0.75 / 0.13 |
| rep-to-rep spread of p_true (mean, max) | 0.09, 0.60 |
| all: correct on ≥1 of k=2/3 reps / on every rep (144 cases) | 95.1% (95% CI 90.3%–97.6%) / 84.7% (95% CI 78.0%–89.7%) |
| all: correct by majority of reps / split cases / split cases outvoted | 91.7% (95% CI 86.0%–95.2%) / 15 / 5 |
| kept: correct on ≥1 of k=2/3 reps / on every rep (52 cases) | 92.3% (95% CI 81.8%–97.0%) / 80.8% (95% CI 68.1%–89.2%) |
| kept: correct by majority of reps / split cases / split cases outvoted | 88.5% (95% CI 77.0%–94.6%) / 6 / 2 |
| refuted: correct on ≥1 of k=2/3 reps / on every rep (92 cases) | 96.7% (95% CI 90.8%–98.9%) / 87.0% (95% CI 78.6%–92.4%) |
| refuted: correct by majority of reps / split cases / split cases outvoted | 93.5% (95% CI 86.5%–97.0%) / 9 / 3 |
| mean latency / tool calls / cost per rep | 41 s / 4.4 / $0.008 |
| total reported cost | $3.21 |

## Refuted cases (specificity, one line each)

| case | p_true | correct |
|---|---|---|
| 0819-sign-release-exit | 0.11 | 1 |
| 0819-theme-toggle-name | 0.07 | 1 |
| 0927-jsonld-csp | 0.04 | 1 |
| 0927-unlisted-feed-leak | 0.04 | 1 |
| 0927-indent-outside-pre | 0.49 | 0.6666666666666666 |
| 0819-sitemap-missing-blog | 0.03 | 1 |
| 0819-infra-los-angeles | 0.93 | 0 |
| squint-ec53337-upside-down | 0.06 | 1 |
| squint-ec53337-index0-primary | 0.27 | 1 |
| squint-ec53337-byte-order-constant | 0.17 | 1 |
| squint-ec53337-hdr-highlight-clamp | 0.28 | 1 |
| squint-c7ea926-vp8x-not-picture | 0.13 | 1 |
| squint-c7ea926-vp8x-flag-clear-safe | 0.47 | 0.5 |
| squint-c7ea926-zero-length-picture | 0.21 | 1 |
| squint-c7ea926-icc-torn-chain | 0.60 | 0.3333333333333333 |
| squint-f4890dd-pdf-shrink-memory | 0.12 | 1 |
| squint-f4890dd-job-mode-stored | 0.03 | 1 |
| squint-f4890dd-heif-readmits-avif | 0.21 | 1 |
| squint-f4890dd-animated-keeps-one-frame | 0.05 | 1 |
| squint-f4890dd-unicode-landsonsource | 0.11 | 1 |
| squint-f4890dd-strip-identical-done | 0.22 | 1 |
| tbm-96d7b9d-jsonld-csp | 0.04 | 1 |
| tbm-96d7b9d-unlisted-feed-leak | 0.04 | 1 |
| tbm-96d7b9d-pre-indent | 0.72 | 0 |
| tbm-96d7b9d-localecompare-lang | 0.37 | 0.6666666666666666 |
| cookie-tab-b8635c1-stale-txshape | 0.08 | 1 |
| cookie-tab-cb74f3a-open-amount-override | 0.12 | 1 |
| cookie-tab-cb74f3a-split-balance | 0.07 | 1 |
| cookie-tab-cb74f3a-base58-cook-suffix | 0.03 | 1 |
| cookie-tab-cb74f3a-null-memo-drops | 0.04 | 1 |
| cookie-tab-cb74f3a-live-check-missing | 0.02 | 1 |
| cookie-tab-cb74f3a-fragment-stale-pay | 0.42 | 0.6666666666666666 |
| cookie-tab-3cbeedc-memo-pipe-injection | 0.04 | 1 |
| cookie-tab-3cbeedc-wrapped-cook-trapped | 0.03 | 1 |
| cookie-tab-3cbeedc-second-memo-prefilter | 0.33 | 0.6666666666666666 |
| cookie-tab-3cbeedc-usdtoraw-subunit | 0.06 | 1 |
| orthodoxprayers-af4e178-headers-miss-pages | 0.53 | 0.6666666666666666 |
| orthodoxprayers-af4e178-indented-selector | 0.04 | 1 |
| orthodoxprayers-af4e178-opening-dead-rule | 0.03 | 1 |
| A-cache-porcine-fonts | 0.03 | 1 |
| orthodoxprayers-af4e178-no-focus-ring | 0.50 | 0.6666666666666666 |
| A-charset-home | 0.03 | 1 |
| A-alt-working-log | 0.03 | 1 |
| A-heading-projects | 0.03 | 1 |
| A-dup-font-porcine | 0.03 | 1 |
| A-pre-light-essentialism | 0.05 | 1 |
| A-search-index-list | 0.03 | 1 |
| A-blog-cleanup | 0.10 | 1 |
| A-readme-check-ports | 0.04 | 1 |
| A-dls-lazy-lead | 0.04 | 1 |
| A-ai-escaping | 0.06 | 1 |
| A-empty-link-ordinals | 0.03 | 1 |
| A-headers-older-sections | 0.04 | 1 |
| B-headers-onion-glued | 0.03 | 1 |
| B-manifest-guard-gap | 0.27 | 1 |
| B-blog-raw-html | 0.05 | 1 |
| B-headers-cache-coverage | 0.05 | 1 |
| B-build-feed-empty | 0.03 | 1 |
| B-build-stamp-skips | 0.04 | 1 |
| B-check-readme-unrun | 0.04 | 1 |
| B-npmrc-comment | 0.03 | 1 |
| B-search-focus-trap | 0.04 | 1 |
| B-pendulum-names | 0.04 | 1 |
| B-poap-vault-tabs | 0.05 | 1 |
| B-youtube-relme | 0.04 | 1 |
| B-home-heading-outline | 0.03 | 1 |
| C-onion-search-count | 0.85 | 0 |
| C-guard-no-dupes | 0.28 | 1 |
| C-pendulum-button-count | 0.57 | 0.3333333333333333 |
| C-eth-duplicate-card | 0.09 | 1 |
| C-stamp-list-ai | 0.05 | 1 |
| C-tailwind-marfa | 0.03 | 1 |
| C-speaking-origin-raw | 0.03 | 1 |
| C-ai-dates-rendered | 0.08 | 1 |
| C-feed-build-clock | 0.12 | 1 |
| C-mirrors-check-host-only | 0.05 | 1 |
| C-dls-alt | 0.03 | 1 |
| C-frontmatter-date-direction | 0.04 | 1 |
| C-readme-never-run | 0.06 | 1 |
| D-ai-unescaped-summary | 0.04 | 1 |
| D-ai-wins-http | 0.04 | 1 |
| D-ai-links-ci-403 | 0.04 | 1 |
| D-speaking-raw-html | 0.03 | 1 |
| D-blog-related-silent | 0.04 | 1 |
| D-search-index-unlisted | 0.03 | 1 |
| D-feed-subject-raw | 0.04 | 1 |
| D-sign-release-sec-argv | 0.03 | 1 |
| D-version-css-silent | 0.05 | 1 |
| D-manifest-build-clock | 0.04 | 1 |
| D-onchain-check-tzkt | 0.03 | 1 |
| D-readme-raw-slug | 0.03 | 1 |
| D-me-webp-cache | 0.04 | 1 |

## Kept cases scored below 0.5

| case | p_true |
|---|---|
| 0819-redirects-count-comment | 0.20 |
| 0819-openagents-citations | 0.28 |
| 0819-inpeak-links | 0.33 |
| 0819-tezos-editions | 0.35 |
| 0819-sitemap-lastmod | 0.43 |
