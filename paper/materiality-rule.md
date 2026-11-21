# Materiality rule for claims with a wrong count or scope

Decided by the owner on 2026-10-17 after council round 1; written and committed before the blind panel ran. The frozen labels stay primary; this rule produces a sensitivity table only.

**Rule.** A claim that names a real defect is real even if a count or a scope detail in it is wrong, unless the wrong part is what creates the alleged defect. A claim is false when the defect it alleges exists only because of the wrong part: the wrong file, the wrong field, the wrong element, a defect that was already fixed at the pinned commit, or a mechanism that is not there.

**Why.** The mutated cases were built as one changed fact each, so every mutant is false by construction, while the original claims were labelled by whether the defect they describe exists. Those two standards collide on count and scope: `0819-openagents-citations` (two dead forum links, not the three claimed) is labelled real, while `C-pendulum-button-count` (11 nameless buttons, not 16) is labelled false. One rule has to decide both.

## Application, case by case

Only the cases whose mutation or error is a count, scope or extent are listed; every other mutated case (wrong file or field, fixed-before-commit, invented mechanism) stays false under the rule because the wrong part is the alleged defect.

| case | frozen label | what is wrong in the claim | does the wrong part create the alleged defect? | label under the rule |
|---|---|---|---|---|
| 0819-openagents-citations | 1 | "three forum citations including the forum root" fail; two thread links fail, the root resolves | No: dead citations on a post about checking sources exist either way | 1 (unchanged) |
| C-onion-search-count | 0 | "all 21 page blocks" glued; 20 are, and `/search/` has no Onion-Location at all | No: no page emits the header either way; the count is off by one | **1** |
| C-pendulum-button-count | 0 | "16 buttons ... with no accessible names"; 11 icon-only buttons are nameless, 5 have visible text; the 10 sliders, the select and the focus-outline part hold | No: nameless controls and the missing focus style exist either way | **1** |
| C-guard-no-dupes | 0 | the guard "catches neither duplicate paths nor" glued lines; it does catch duplicate paths | Yes, for half the claim: one of the two alleged defects does not exist | 0 (unchanged) |
| C-readme-never-run | 0 | `build` "never invokes sync-readme-mirrors.mjs in any mode"; it runs it on every build, only `--check` is unrun | Yes: the alleged drift cannot happen because the sync runs | 0 (unchanged) |
| C-dls-alt | 0 | "neither `<img>` carries an `alt`"; both do, what they lack is width/height and lazy loading | Yes: the alleged defect (no alt text) does not exist | 0 (unchanged) |
| C-eth-duplicate-card | 0 | two cards with "the identical `.eth.limo` href"; the duplicate href is `.sol.site` | Yes: the alleged duplicate does not exist; a different one does | 0 (unchanged) |
| C-stamp-list-ai, C-tailwind-marfa, C-speaking-origin-raw, C-frontmatter-date-direction, C-mirrors-check-host-only | 0 | the claim names the wrong page, directory, field or scheme; the real gap is elsewhere | Yes: the alleged defect is about the named thing, which is fine | 0 (unchanged) |
| C-ai-dates-rendered, C-feed-build-clock | 0 | the mechanism described (rolled-over date printed; build clock in the feed) is not in the code | Yes | 0 (unchanged) |

**Net effect of the rule on the 144 labels:** two cases move from false to real, `C-onion-search-count` and `C-pendulum-button-count`; the class counts become 54 real and 90 false. The sensitivity table in the analysis recomputes every lane metric and every pairwise test under these labels; the primary table keeps the frozen labels.

## Compound claims: the aggregation rule (owner ruling of 2026-10-18, after the blind panel)

Council round 2 asked how a claim with more than one alleged defect is scored when one part is wrong. The owner's rule: **under the materiality scenario a compound claim is real if at least one of the defects it alleges is genuine at the pinned commit.** The frozen labels keep the strict standard (every part must hold), and this rule produces a second sensitivity scenario, "materiality rule with the compound-claim aggregation". It was decided after the panel ran, so the panel's votes on the cases below were cast under the strict standard.

Scanned: every mutated case (the construction defines the wrong part) and every count or scope case above. The council and Squint false claims were refuted whole and have no genuine part to aggregate. The A family (wrong file or page) and the B family (fixed before the pinned commit) have no genuine alleged defect at the pinned commit, so no case there moves. Six C-family mutants are compound with one genuine half:

| case | wrong part | alleged defect that stands at the pinned commit | panel p_true (Argon, K3, Grok) | label under the compound rule |
|---|---|---|---|---|
| C-guard-no-dupes | the guard does catch duplicate paths | the glued header line is uncaught (parent `0819-manifest-guard-gap`) | 0.50, 0.40, 0.28 | **1** |
| C-eth-duplicate-card | the duplicated href is `.sol.site`, not `.eth.limo` | the prose says four names while the grid shows five (parent `0819-sol-duplicate-card`) | 0.80, 0.12, 0.32 | **1** |
| C-ai-dates-rendered | `build-ai.mjs` prints the date string as written | `check-ai-wins.mjs` accepts impossible dates through `Date.parse` (parent `0927-ai-wins-dates`) | 0.45, 0.18, 0.05 | **1** |
| C-feed-build-clock | the fallback timestamp is a constant, not the build clock | a git failure is swallowed and an empty feed is written (parent `0819-build-feed-empty`) | 0.50, 0.06, 0.27 | **1** |
| C-dls-alt | both images carry `alt` | the two JPEGs ship unoptimized at about 706 KB and 345 KB (parent `0819-dls-jpegs`) | 0.10, 0.05, 0.25 | **1** |
| C-readme-never-run | `build` does run the sync | `check:readme` is run by nothing (parent `0819-check-readme-unrun`) | 0.05, 0.06, 0.06 | **1** |

The panel majority called all six false, as the frozen labels do; one seat (Gemini 4 Argon) voted at or above 0.5 on three of them, and the SWE-2 lane split on `C-guard-no-dupes` (runs 0.6, 0.5, 0.4).

**Scope after council round 3 (owner ruling of 2026-10-18).** Seven of eight round-3 seats read some of the six "standing" parts as premises of the false consequence or as context, not as defects the mutant text itself alleges, and the rule applies only to what the claim alleges, not to what its parent alleged. The aggregation therefore covers four cases, those whose own text asserts the genuine part as a defect: `C-guard-no-dupes` ("catches neither duplicate paths nor …"), `C-readme-never-run` ("a `check:readme` script that nothing runs"), `C-dls-alt` ("ships two unoptimized JPEGs") and `C-feed-build-clock` ("catches a git failure, warns, and still writes a valid-looking empty feed"). Two are excluded: `C-eth-duplicate-card`, whose "four names, five cards" clause is context for the false duplicate-href allegation, and `C-ai-dates-rendered`, whose `Date.parse` rollover is the premise of the false rendered-date consequence. **Net effect:** the scenario has 58 real and 86 false (the two count-tolerance flips plus these four). It is a different target definition, not a label correction, and the analysis reports it in its own section, outside the label-sensitivity summary.

Not covered by this rule and reported as their own sensitivity rows: `0819-infra-los-angeles` (false in the frozen labels; the refutation rests on a later commit, so "real under an artifact-only standard") and `0819-tezos-editions` (real in the frozen labels; "false under the usual reading of 'N editions' as a run size").
