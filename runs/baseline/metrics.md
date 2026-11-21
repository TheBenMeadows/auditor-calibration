# baseline: Orrery finding-precision eval

130 cases scored (52 kept, 78 refuted), 390 rep rows, 0 failed attempt(s) in errors.jsonl (not in the means).

| metric | value |
|---|---|
| recall (kept scored real at p≥0.5) | 96.2% (95% CI 87.0%–98.9%) |
| specificity (refuted scored not-real at p≥0.5) | 95.7% (95% CI 88.7%–98.5%) |
| AUROC of p_true (kept vs refuted) | 0.996 |
| Brier (lower is better) | 0.032 |
| bare verdict agreement (true=1, partial=0.5, false=0) | 92.9% |
| mean p_true on kept / on refuted | 0.85 / 0.09 |
| rep-to-rep spread of p_true (mean, max) | 0.04, 0.50 |
| all: correct on ≥1 of k=3 reps / on every rep (130 cases) | 98.5% (95% CI 94.6%–99.6%) / 93.1% (95% CI 87.4%–96.3%) |
| all: correct by majority of reps / split cases / split cases outvoted | 96.2% (95% CI 91.3%–98.3%) / 7 / 3 |
| kept: correct on ≥1 of k=3 reps / on every rep (52 cases) | 100.0% (95% CI 93.1%–100.0%) / 92.3% (95% CI 81.8%–97.0%) |
| kept: correct by majority of reps / split cases / split cases outvoted | 96.2% (95% CI 87.0%–98.9%) / 4 / 2 |
| refuted: correct on ≥1 of k=3 reps / on every rep (78 cases) | 97.4% (95% CI 91.1%–99.3%) / 93.6% (95% CI 85.9%–97.2%) |
| refuted: correct by majority of reps / split cases / split cases outvoted | 96.2% (95% CI 89.3%–98.7%) / 3 / 1 |
| mean latency / tool calls / cost per rep | 46 s / 4.3 / $0.147 |
| total reported cost | $57.16 |

## Refuted cases (specificity, one line each)

| case | p_true | correct |
|---|---|---|
| 0819-sign-release-exit | 0.10 | 1 |
| 0819-theme-toggle-name | 0.10 | 1 |
| 0927-jsonld-csp | 0.05 | 1 |
| 0927-unlisted-feed-leak | 0.04 | 1 |
| 0927-indent-outside-pre | 0.20 | 1 |
| 0819-infra-los-angeles | 0.82 | 0 |
| 0819-sitemap-missing-blog | 0.04 | 1 |
| tbm-96d7b9d-jsonld-csp | 0.05 | 1 |
| tbm-96d7b9d-unlisted-feed-leak | 0.05 | 1 |
| tbm-96d7b9d-localecompare-lang | 0.73 | 0 |
| tbm-96d7b9d-pre-indent | 0.32 | 0.6666666666666666 |
| cookie-tab-b8635c1-stale-txshape | 0.06 | 1 |
| cookie-tab-cb74f3a-split-balance | 0.04 | 1 |
| cookie-tab-cb74f3a-open-amount-override | 0.05 | 1 |
| cookie-tab-cb74f3a-null-memo-drops | 0.05 | 1 |
| cookie-tab-cb74f3a-base58-cook-suffix | 0.03 | 1 |
| cookie-tab-cb74f3a-live-check-missing | 0.02 | 1 |
| cookie-tab-3cbeedc-wrapped-cook-trapped | 0.03 | 1 |
| cookie-tab-3cbeedc-memo-pipe-injection | 0.04 | 1 |
| cookie-tab-cb74f3a-fragment-stale-pay | 0.41 | 0.6666666666666666 |
| cookie-tab-3cbeedc-second-memo-prefilter | 0.06 | 1 |
| cookie-tab-3cbeedc-usdtoraw-subunit | 0.07 | 1 |
| orthodoxprayers-af4e178-headers-miss-pages | 0.18 | 1 |
| orthodoxprayers-af4e178-no-focus-ring | 0.11 | 1 |
| orthodoxprayers-af4e178-opening-dead-rule | 0.04 | 1 |
| orthodoxprayers-af4e178-indented-selector | 0.05 | 1 |
| A-charset-home | 0.03 | 1 |
| A-heading-projects | 0.04 | 1 |
| A-alt-working-log | 0.03 | 1 |
| A-cache-porcine-fonts | 0.04 | 1 |
| A-dup-font-porcine | 0.02 | 1 |
| A-search-index-list | 0.03 | 1 |
| A-readme-check-ports | 0.04 | 1 |
| A-blog-cleanup | 0.07 | 1 |
| A-dls-lazy-lead | 0.07 | 1 |
| A-pre-light-essentialism | 0.05 | 1 |
| A-empty-link-ordinals | 0.03 | 1 |
| A-ai-escaping | 0.07 | 1 |
| B-headers-onion-glued | 0.04 | 1 |
| B-manifest-guard-gap | 0.07 | 1 |
| B-blog-raw-html | 0.06 | 1 |
| A-headers-older-sections | 0.04 | 1 |
| B-build-stamp-skips | 0.03 | 1 |
| B-build-feed-empty | 0.05 | 1 |
| B-headers-cache-coverage | 0.05 | 1 |
| B-check-readme-unrun | 0.05 | 1 |
| B-search-focus-trap | 0.04 | 1 |
| B-npmrc-comment | 0.04 | 1 |
| B-pendulum-names | 0.05 | 1 |
| B-poap-vault-tabs | 0.06 | 1 |
| B-home-heading-outline | 0.04 | 1 |
| B-youtube-relme | 0.04 | 1 |
| C-guard-no-dupes | 0.08 | 1 |
| C-onion-search-count | 0.37 | 1 |
| C-tailwind-marfa | 0.03 | 1 |
| C-stamp-list-ai | 0.04 | 1 |
| C-pendulum-button-count | 0.48 | 0.3333333333333333 |
| C-eth-duplicate-card | 0.11 | 1 |
| C-ai-dates-rendered | 0.11 | 1 |
| C-speaking-origin-raw | 0.04 | 1 |
| C-mirrors-check-host-only | 0.05 | 1 |
| C-frontmatter-date-direction | 0.05 | 1 |
| C-feed-build-clock | 0.11 | 1 |
| C-dls-alt | 0.05 | 1 |
| C-readme-never-run | 0.05 | 1 |
| D-ai-wins-http | 0.05 | 1 |
| D-ai-links-ci-403 | 0.04 | 1 |
| D-ai-unescaped-summary | 0.04 | 1 |
| D-speaking-raw-html | 0.06 | 1 |
| D-feed-subject-raw | 0.03 | 1 |
| D-blog-related-silent | 0.05 | 1 |
| D-sign-release-sec-argv | 0.04 | 1 |
| D-search-index-unlisted | 0.04 | 1 |
| D-version-css-silent | 0.04 | 1 |
| D-manifest-build-clock | 0.05 | 1 |
| D-readme-raw-slug | 0.03 | 1 |
| D-onchain-check-tzkt | 0.04 | 1 |
| D-me-webp-cache | 0.04 | 1 |

## Kept cases scored below 0.5

| case | p_true |
|---|---|
| 0927-squint-signed-claim | 0.42 |
