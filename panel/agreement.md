# Blind panel agreement with the owner's labels

Each seat saw only the claim and the files the claim names at the pinned commit; a seat's label is p_true ≥ 0.5, so a 0.50 ("could not tell") counts as real. Agreement is between three models and the owner, who wrote or ruled on every label; it measures consistency under an artifact-only information ceiling, not correctness.

| seat | cases | agree with owner | Cohen's kappa | votes at exactly 0.50 |
|---|---|---|---|---|
| Gemini 4 Argon | 144 | 88.9% | 0.767 | 9 |
| Kimi K3 | 144 | 86.8% | 0.720 | 5 |
| Grok 4.7 | 144 | 88.2% | 0.747 | 9 |

Fleiss' kappa across the three seats on the 144 cases all three labelled: 0.739

Panel majority against the owner, all cases: 144 decided, agreement 91.0%, Cohen's kappa 0.810; 0 split or single-seat cases.

| subset | n | agreement | kappa |
|---|---|---|---|
| original | 59 | 93.2% | 0.711 |
| mutated | 52 | 94.2% | n/a (one owner class) |
| council | 19 | 78.9% | n/a (one owner class) |
| squint | 14 | 85.7% | n/a (one owner class) |
| excluding the 8 outside-files cases (all of them disputes, so the agreeing count is unchanged) | 136 | 96.3% | 0.922 |

Seat votes at exactly 0.50: 23 of 432. Counting 0.50 as false instead of real would change the panel majority on 9 cases: 0819-commit-trailers (owner 1, agreement → dispute), 0819-essentialism-png-aspect (owner 1, agreement → dispute), 0819-openagents-citations (owner 1, agreement → dispute), 0819-pretext-unused (owner 1, agreement → dispute), 0819-redirects-count-comment (owner 1, agreement → dispute), 0819-reduced-motion (owner 1, agreement → dispute), 0927-build-order-related (owner 1, agreement → dispute), 0927-squint-signed-claim (owner 1, agreement → dispute), B-check-readme-unrun (owner 0, dispute → agreement).

## Cases where the panel majority disagrees with the owner

| case | source | owner | panel votes (Argon, K3, Grok) | p_true | class |
|---|---|---|---|---|---|
| cookie-tab-cb74f3a-fragment-stale-pay | council | 0 | [1, 1, 0] | 0.95, 0.90, 0.32 | refutation outside the pinned files |
| orthodoxprayers-af4e178-headers-miss-pages | council | 0 | [1, 1, 1] | 0.95, 0.72, 0.55 | refutation outside the pinned files |
| tbm-96d7b9d-localecompare-lang | council | 0 | [1, 1, 1] | 0.95, 0.80, 0.86 | refutation outside the pinned files |
| tbm-96d7b9d-pre-indent | council | 0 | [0, 1, 1] | 0.05, 0.85, 0.95 | refutation outside the pinned files |
| B-check-readme-unrun | mutated | 0 | [1, 1, 1] | 0.50, 0.50, 0.52 |  |
| C-onion-search-count | mutated | 0 | [1, 1, 1] | 0.70, 0.82, 0.74 | materiality rule, sensitivity row |
| C-pendulum-button-count | mutated | 0 | [1, 1, 1] | 0.95, 0.78, 0.64 | materiality rule, sensitivity row |
| 0819-foundation-dead | original | 1 | [1, 0, 0] | 0.50, 0.45, 0.46 | refutation outside the pinned files |
| 0819-infra-los-angeles | original | 0 | [1, 1, 0] | 0.95, 0.90, 0.38 | owner-flagged, sensitivity row |
| 0819-tezos-editions | original | 1 | [0, 0, 0] | 0.45, 0.12, 0.22 | owner-flagged, sensitivity row |
| 0927-dead-links-2025 | original | 1 | [0, 0, 1] | 0.10, 0.15, 0.50 | refutation outside the pinned files |
| squint-c7ea926-icc-torn-chain | squint | 0 | [1, 0, 1] | 0.95, 0.38, 0.66 | refutation outside the pinned files |
| squint-ec53337-upside-down | squint | 0 | [0, 1, 1] | 0.02, 0.82, 0.88 | refutation outside the pinned files |

## Owner-flagged cases

| case | owner | panel votes | p_true | majority dispute |
|---|---|---|---|---|
| 0819-infra-los-angeles | 0 | [1, 1, 0] | 0.95, 0.90, 0.38 | yes |
| 0819-openagents-citations | 1 | [1, 1, 1] | 0.50, 0.50, 0.50 | no |
| 0819-tezos-editions | 1 | [0, 0, 0] | 0.45, 0.12, 0.22 | yes |
