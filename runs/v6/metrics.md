# v6: Orrery finding-precision eval

144 cases scored (52 kept, 92 refuted), 144 rep rows, 0 failed attempt(s) in errors.jsonl (not in the means).

| metric | value |
|---|---|
| recall (kept scored real at p≥0.5) | 100.0% (95% CI 93.1%–100.0%) |
| specificity (refuted scored not-real at p≥0.5) | 90.2% (95% CI 82.4%–94.8%) |
| AUROC of p_true (kept vs refuted) | 0.983 |
| Brier (lower is better) | 0.054 |
| bare verdict agreement (true=1, partial=0.5, false=0) | 88.2% |
| mean p_true on kept / on refuted | 0.90 / 0.15 |
| mean latency / tool calls / cost per rep | 50 s / 5.5 / $0.467 |
| total reported cost | $67.21 |

## Refuted cases (specificity, one line each)

| case | p_true | correct |
|---|---|---|
| 0819-sign-release-exit | 0.15 | 1 |
| 0819-theme-toggle-name | 0.35 | 1 |
| 0927-jsonld-csp | 0.05 | 1 |
| 0927-indent-outside-pre | 0.90 | 0 |
| 0927-unlisted-feed-leak | 0.04 | 1 |
| 0819-sitemap-missing-blog | 0.05 | 1 |
| 0819-infra-los-angeles | 0.85 | 0 |
| squint-ec53337-upside-down | 0.08 | 1 |
| squint-ec53337-byte-order-constant | 0.15 | 1 |
| squint-ec53337-index0-primary | 0.12 | 1 |
| squint-c7ea926-vp8x-not-picture | 0.08 | 1 |
| squint-c7ea926-vp8x-flag-clear-safe | 0.90 | 0 |
| squint-c7ea926-zero-length-picture | 0.08 | 1 |
| squint-f4890dd-pdf-shrink-memory | 0.40 | 1 |
| squint-f4890dd-job-mode-stored | 0.04 | 1 |
| squint-c7ea926-icc-torn-chain | 0.85 | 0 |
| squint-ec53337-hdr-highlight-clamp | 0.15 | 1 |
| squint-f4890dd-heif-readmits-avif | 0.08 | 1 |
| squint-f4890dd-animated-keeps-one-frame | 0.06 | 1 |
| squint-f4890dd-unicode-landsonsource | 0.10 | 1 |
| tbm-96d7b9d-jsonld-csp | 0.05 | 1 |
| tbm-96d7b9d-unlisted-feed-leak | 0.04 | 1 |
| squint-f4890dd-strip-identical-done | 0.30 | 1 |
| tbm-96d7b9d-pre-indent | 0.25 | 1 |
| cookie-tab-b8635c1-stale-txshape | 0.12 | 1 |
| cookie-tab-cb74f3a-open-amount-override | 0.05 | 1 |
| tbm-96d7b9d-localecompare-lang | 0.80 | 0 |
| cookie-tab-cb74f3a-base58-cook-suffix | 0.03 | 1 |
| cookie-tab-cb74f3a-split-balance | 0.04 | 1 |
| cookie-tab-3cbeedc-memo-pipe-injection | 0.04 | 1 |
| cookie-tab-cb74f3a-null-memo-drops | 0.05 | 1 |
| cookie-tab-cb74f3a-live-check-missing | 0.03 | 1 |
| cookie-tab-3cbeedc-wrapped-cook-trapped | 0.04 | 1 |
| cookie-tab-cb74f3a-fragment-stale-pay | 0.55 | 0 |
| cookie-tab-3cbeedc-usdtoraw-subunit | 0.15 | 1 |
| orthodoxprayers-af4e178-headers-miss-pages | 0.92 | 0 |
| cookie-tab-3cbeedc-second-memo-prefilter | 0.20 | 1 |
| orthodoxprayers-af4e178-indented-selector | 0.08 | 1 |
| A-cache-porcine-fonts | 0.04 | 1 |
| orthodoxprayers-af4e178-no-focus-ring | 0.15 | 1 |
| A-charset-home | 0.03 | 1 |
| orthodoxprayers-af4e178-opening-dead-rule | 0.04 | 1 |
| A-dup-font-porcine | 0.02 | 1 |
| A-heading-projects | 0.03 | 1 |
| A-alt-working-log | 0.03 | 1 |
| A-search-index-list | 0.03 | 1 |
| A-blog-cleanup | 0.08 | 1 |
| A-pre-light-essentialism | 0.04 | 1 |
| A-readme-check-ports | 0.03 | 1 |
| A-dls-lazy-lead | 0.05 | 1 |
| A-empty-link-ordinals | 0.03 | 1 |
| A-ai-escaping | 0.05 | 1 |
| B-headers-onion-glued | 0.03 | 1 |
| A-headers-older-sections | 0.04 | 1 |
| B-manifest-guard-gap | 0.08 | 1 |
| B-headers-cache-coverage | 0.04 | 1 |
| B-build-stamp-skips | 0.03 | 1 |
| B-check-readme-unrun | 0.05 | 1 |
| B-blog-raw-html | 0.04 | 1 |
| B-build-feed-empty | 0.04 | 1 |
| B-npmrc-comment | 0.03 | 1 |
| B-poap-vault-tabs | 0.06 | 1 |
| B-youtube-relme | 0.04 | 1 |
| B-search-focus-trap | 0.05 | 1 |
| B-home-heading-outline | 0.03 | 1 |
| B-pendulum-names | 0.04 | 1 |
| C-onion-search-count | 0.80 | 0 |
| C-guard-no-dupes | 0.08 | 1 |
| C-pendulum-button-count | 0.80 | 0 |
| C-eth-duplicate-card | 0.08 | 1 |
| C-tailwind-marfa | 0.04 | 1 |
| C-stamp-list-ai | 0.04 | 1 |
| C-speaking-origin-raw | 0.05 | 1 |
| C-feed-build-clock | 0.20 | 1 |
| C-mirrors-check-host-only | 0.04 | 1 |
| C-ai-dates-rendered | 0.25 | 1 |
| C-dls-alt | 0.15 | 1 |
| C-readme-never-run | 0.08 | 1 |
| C-frontmatter-date-direction | 0.04 | 1 |
| D-ai-wins-http | 0.03 | 1 |
| D-ai-unescaped-summary | 0.03 | 1 |
| D-ai-links-ci-403 | 0.03 | 1 |
| D-feed-subject-raw | 0.03 | 1 |
| D-search-index-unlisted | 0.04 | 1 |
| D-blog-related-silent | 0.05 | 1 |
| D-version-css-silent | 0.04 | 1 |
| D-sign-release-sec-argv | 0.03 | 1 |
| D-speaking-raw-html | 0.06 | 1 |
| D-readme-raw-slug | 0.03 | 1 |
| D-onchain-check-tzkt | 0.03 | 1 |
| D-manifest-build-clock | 0.04 | 1 |
| D-me-webp-cache | 0.03 | 1 |

## Kept cases scored below 0.5

none
