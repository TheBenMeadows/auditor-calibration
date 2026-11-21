# Orrery finding-precision eval: inputs for review

59 cases: 52 kept findings (label 1), 7 refuted claims (label 0). Each case is the claim as a worker raised it, stripped of evidence and verdict. The auditor gets the claim, the commit and the paths; it is told the live site has changed and to verify against the commit through GitHub.

Audited commits: 0819 = `7f50013b094028da0b9630b5972971ecd16e3d68`, 0927 = `96d7b9d`.

| id | tags | label | where |
|---|---|---|---|
| 0819-headers-onion-glued | security, 0819 | 1 | `_headers` |
| 0819-manifest-guard-gap | source, 0819 | 1 | `scripts/build-manifest.mjs`, `_headers` |
| 0819-blog-raw-html | security, 0819 | 1 | `scripts/build-blog.mjs` |
| 0819-commit-trailers | governance, 0819 | 1 | `git history of main (list_commits / get_commit)` |
| 0819-headers-cache-coverage | perf, 0819 | 1 | `_headers`, `blog/media/`, `experiments/`, `projects/poap-saver/` |
| 0819-dls-jpegs | perf, 0819 | 1 | `experiments/dls/index.html`, `experiments/dls/HEw3HB0WoAAHoBW.jpeg`, `experiments/dls/rzVCLxC8.jpg` |
| 0819-essentialism-png-aspect | perf, 0819 | 1 | `art/essentialism/index.html`, `art/essentialism/essentialism-2022.png` |
| 0819-build-feed-empty | source, 0819 | 1 | `scripts/build-feed.mjs` |
| 0819-sign-release-exit | source, 0819 | 0 | `scripts/sign-release.sh` |
| 0819-build-stamp-skips | source, 0819 | 1 | `scripts/build-stamp.mjs` |
| 0819-frontmatter-unescaped | source, 0819 | 1 | `scripts/build-blog.mjs` |
| 0819-check-readme-unrun | source, 0819 | 1 | `package.json`, `scripts/sync-readme-mirrors.mjs`, `.github/workflows/` |
| 0819-npmrc-comment | source, 0819 | 1 | `.npmrc`, `package-lock.json` |
| 0819-pretext-unused | source, 0819 | 1 | `package.json`, `scripts/` |
| 0819-duplicate-font | perf, 0819 | 1 | `experiments/poap-vault/publicsans.woff2`, `fonts/publicsans-v1.woff2`, `_headers` |
| 0819-redirects-count-comment | source, 0819 | 1 | `_redirects` |
| 0819-blog-alt-empty | a11y, 0819 | 1 | `blog/posts/art-tech-highlights.md`, `blog/posts/podcasts-public-speaking.md`, `scripts/build-blog.mjs` |
| 0819-pendulum-names | a11y, 0819 | 1 | `experiments/pendulum/index.html`, `experiments/pendulum/` |
| 0819-dark-contrast | a11y, 0819 | 1 | `src/input.css`, `scripts/build-stamp.mjs`, `index.html`, `tailwind.config.js` |
| 0819-mirrors-pre-light | a11y, 0819 | 1 | `mirrors/index.html`, `src/input.css` |
| 0819-search-focus-trap | a11y, 0819 | 1 | `search.js`, `index.html` |
| 0819-content-language-meta | a11y, 0819 | 1 | `index.html`, `tech/index.html`, `mirrors/index.html`, `profiles/index.html` |
| 0819-home-heading-outline | a11y, 0819 | 1 | `index.html`, `experiments/index.html`, `projects/index.html` |
| 0819-reduced-motion | a11y, 0819 | 1 | `experiments/porcine/`, `experiments/etherhoo/`, `src/input.css`, `scripts/experiments-input.css` |
| 0819-theme-toggle-name | a11y, 0819 | 0 | `index.html`, `theme.js`, `src/input.css` |
| 0819-porcine-h1-triple | a11y, 0819 | 1 | `experiments/porcine/index.html`, `experiments/porcine/` |
| 0819-empty-md-link | a11y, 0819 | 1 | `blog/posts/art-tech-highlights.md` |
| 0819-poap-vault-tabs | a11y, 0819 | 1 | `experiments/poap-vault/index.html`, `experiments/poap-vault/app.js` |
| 0819-charset-late | source, 0819 | 1 | `essentialism/index.html` |
| 0819-youtube-relme | content, 0819, external | 1 | `index.html`, `profiles/index.html` |
| 0819-foundation-dead | content, 0819, external | 1 | `art/index.html`, `blog/posts/`, `index.html` |
| 0819-openagents-citations | content, 0819, external | 1 | `blog/posts/my-owner-asked-me-to-write-this-post-receipts-attached.md` |
| 0819-inpeak-links | content, 0819, external | 1 | `blog/posts/podcasts-public-speaking.md` |
| 0819-tech-only-image | content, 0819 | 1 | `tech/index.html`, `experiments/dls/`, `art/essentialism/`, `experiments/poap-vault/img/` |
| 0819-sol-duplicate-card | content, 0819 | 1 | `mirrors/index.html` |
| 0819-tezos-editions | content, 0819, external | 1 | `art/index.html`, `art/essentialism/index.html` |
| 0819-porcine-credit | content, 0819, external | 1 | `experiments/porcine/index.html` |
| 0819-sitemap-lastmod | content, 0819 | 1 | `sitemap.xml`, `scripts/`, `git history of main` |
| 0819-highlights-prose | content, 0819 | 1 | `blog/posts/art-tech-highlights.md` |
| 0927-speaking-no-way-in | content, 0927 | 1 | `index.html`, `blog/posts/podcasts-public-speaking.md`, `projects/index.html`, `profiles/index.html`, `sitemap.xml`, `scripts/build-speaking.mjs` |
| 0927-squint-signed-claim | content, 0927, external | 1 | `ai/wins.json`, `mdws-org/squint releases (v0.6.0)` |
| 0927-headers-new-sections | security, 0927 | 1 | `_headers`, `marfa/`, `art/essentialism/syntax/` |
| 0927-bitly-relative | content, 0927 | 1 | `blog/posts/podcasts-public-speaking.md` |
| 0927-empty-link-2025 | a11y, 0927 | 1 | `blog/posts/art-tech-highlights-2025.md` |
| 0927-syn-operator-contrast | a11y, 0927 | 1 | `art/essentialism/index.html`, `art/essentialism/syntax/`, `src/input.css` |
| 0927-build-stamp-list | source, 0927 | 1 | `scripts/build-stamp.mjs`, `scripts/build-speaking.mjs` |
| 0927-marfa-lazy-lead | perf, 0927 | 1 | `marfa/index.html`, `scripts/build-blog.mjs` |
| 0927-speaking-escaping | security, 0927 | 1 | `scripts/build-speaking.mjs` |
| 0927-speaking-cleanup | source, 0927 | 1 | `scripts/build-speaking.mjs` |
| 0927-ai-wins-dates | source, 0927 | 1 | `scripts/check-ai-wins.mjs` |
| 0927-mirrors-check-ports | source, 0927 | 1 | `scripts/check-mirrors-page.mjs`, `mirrors.json`, `mirrors/index.html` |
| 0927-tailwind-speaking | source, 0927 | 1 | `tailwind.config.js`, `scripts/build-speaking.mjs` |
| 0927-build-order-related | source, 0927 | 1 | `package.json`, `scripts/build-blog.mjs` |
| 0927-dead-links-2025 | content, 0927, external | 1 | `blog/posts/art-tech-highlights-2025.md` |
| 0927-jsonld-csp | security, 0927 | 0 | `index.html`, `_headers` |
| 0927-unlisted-feed-leak | source, 0927 | 0 | `scripts/build-feed.mjs`, `scripts/build-blog.mjs`, `scripts/build-search-index.mjs`, `blog/posts/art-tech-highlights-2025.md` |
| 0927-indent-outside-pre | source, 0927 | 0 | `scripts/build-blog.mjs` |
| 0819-sitemap-missing-blog | content, 0819 | 0 | `sitemap.xml`, `blog/posts/`, `scripts/build-blog.mjs` |
| 0819-infra-los-angeles | content, 0819, external | 0 | `infra/index.html` |

## 0819-headers-onion-glued

label 1 (kept), security, 0819; where: `_headers`

```
In `_headers`, 20 path blocks have their `Onion-Location` value glued onto the end of the `Cache-Control` line (no line break between them), so no `Onion-Location` header is emitted for any path and Tor Browser is never offered the onion mirror.
```

## 0819-manifest-guard-gap

label 1 (kept), source, 0819; where: `scripts/build-manifest.mjs`, `_headers`

```
The `_headers` guard in `scripts/build-manifest.mjs` catches duplicate paths but would not catch an indented header line that carries a second `name: value` pair glued onto it, so a header-merging regression passes the build.
```

## 0819-blog-raw-html

label 1 (kept), security, 0819; where: `scripts/build-blog.mjs`

```
`scripts/build-blog.mjs` defines a marked `RENDERER` with no `html` method and merges it onto marked's defaults, whose `html` renderer is a passthrough, so raw `<script>` or `<img onerror=…>` written into `blog/posts/*.md` reaches the generated page unescaped. The source comment near the renderer claims stray markup is escaped.
```

## 0819-commit-trailers

label 1 (kept), governance, 0819; where: `git history of main (list_commits / get_commit)`

```
Commits on `main` from `4b354e6` (2026-07-19) through `254484d` (2026-08-03) carry a `Co-Authored-By: Claude …` trailer, and many of them also carry a `Claude-Session:` URL in the message; commits after `254484d` carry neither.
```

## 0819-headers-cache-coverage

label 1 (kept), perf, 0819; where: `_headers`, `blog/media/`, `experiments/`, `projects/poap-saver/`

```
`_headers` cache rules apply only to the paths they name, so `/blog/media/**` images, `/art/essentialism/*`, every `/experiments/*/app.js` and `style.css`, `/projects/poap-saver/app.js` and the whole `/experiments/poap-vault/img/` set (over 700 WebP files) fall to the Pages default `max-age=0, must-revalidate` and are not browser-cacheable.
```

## 0819-dls-jpegs

label 1 (kept), perf, 0819; where: `experiments/dls/index.html`, `experiments/dls/HEw3HB0WoAAHoBW.jpeg`, `experiments/dls/rzVCLxC8.jpg`

```
`/experiments/dls/` ships two unoptimized JPEGs, `HEw3HB0WoAAHoBW.jpeg` (about 706 KB) and `rzVCLxC8.jpg` (about 345 KB), that together are over 95% of the page's weight; neither `<img>` carries `width`/`height` attributes and neither is lazy-loaded.
```

## 0819-essentialism-png-aspect

label 1 (kept), perf, 0819; where: `art/essentialism/index.html`, `art/essentialism/essentialism-2022.png`

```
`art/essentialism/index.html` declares `essentialism-2022.png` with `width="1200" height="900"` while the image file itself is square (1200×1200), so the browser reserves a 4:3 box and shifts layout on decode.
```

## 0819-build-feed-empty

label 1 (kept), source, 0819; where: `scripts/build-feed.mjs`

```
`scripts/build-feed.mjs` catches a git failure, warns, and still writes a valid-looking empty feed with a hardcoded `2026-01-01` timestamp instead of throwing, so a broken build produces a signed, manifest-hashed empty feed.
```

## 0819-sign-release-exit

label 0 (refuted), source, 0819; where: `scripts/sign-release.sh`

```
`scripts/sign-release.sh` folds stderr into stdout, pipes the publish step through `tail`, and never inspects the exit status, so if every relay rejects the release event the script prints the rejections and exits 0.
```

## 0819-build-stamp-skips

label 1 (kept), source, 0819; where: `scripts/build-stamp.mjs`

```
`scripts/build-stamp.mjs` skips a missing page with a warning and still exits 0, and nothing compares the number of pages stamped against the expected count.
```

## 0819-frontmatter-unescaped

label 1 (kept), source, 0819; where: `scripts/build-blog.mjs`

```
In `scripts/build-blog.mjs`, several front-matter fields (including `tags`, which is unconstrained) reach the page unescaped, and the `updated` field gets none of the `^\d{4}-\d{2}-\d{2}$` validation that `date` already has, landing raw in both the page and the Atom feed.
```

## 0819-check-readme-unrun

label 1 (kept), source, 0819; where: `package.json`, `scripts/sync-readme-mirrors.mjs`, `.github/workflows/`

```
`package.json` defines a `check:readme` script that nothing runs; the build runs the rewriting variant instead, and `readme.md` is not part of the published artifact, so the drift guard on the readme can never fail anything.
```

## 0819-npmrc-comment

label 1 (kept), source, 0819; where: `.npmrc`, `package-lock.json`

```
The comment in `.npmrc` claims no package in the dependency tree declares an install hook, but the lockfile's `fsevents` 2.3.3 entry declares one (optional, darwin-only), so the justification written next to `ignore-scripts=true` is false.
```

## 0819-pretext-unused

label 1 (kept), source, 0819; where: `package.json`, `scripts/`

```
`@chenglou/pretext` is declared in `package.json` but nothing in `scripts/` imports it, and `marked` is pinned two major versions behind the current release.
```

## 0819-duplicate-font

label 1 (kept), perf, 0819; where: `experiments/poap-vault/publicsans.woff2`, `fonts/publicsans-v1.woff2`, `_headers`

```
`experiments/poap-vault/publicsans.woff2` is byte-identical to `fonts/publicsans-v1.woff2` but served at a different URL, so it cannot share the cache entry and additionally inherits the default `max-age=0`.
```

## 0819-redirects-count-comment

label 1 (kept), source, 0819; where: `_redirects`

```
The comment in `_redirects` says the catch-all rule covers 763 files, but the number of files it actually covers is different, so the figure in the comment is stale.
```

## 0819-blog-alt-empty

label 1 (kept), a11y, 0819; where: `blog/posts/art-tech-highlights.md`, `blog/posts/podcasts-public-speaking.md`, `scripts/build-blog.mjs`

```
`blog/posts/art-tech-highlights.md` and `blog/posts/podcasts-public-speaking.md` each contain eleven bare `![](…)` images with no alt text, and both lack an `image_alt` front-matter field for their lead image, so about 25 content images ship with `alt=""`.
```

## 0819-pendulum-names

label 1 (kept), a11y, 0819; where: `experiments/pendulum/index.html`, `experiments/pendulum/`

```
`/experiments/pendulum/` has 11 buttons, 10 range sliders and a select with no accessible names (the visible labels are unassociated sibling spans), and its CSS sets `input[type=range]:focus { outline: none; }` with no replacement focus style.
```

## 0819-dark-contrast

label 1 (kept), a11y, 0819; where: `src/input.css`, `scripts/build-stamp.mjs`, `index.html`, `tailwind.config.js`

```
In the dark theme, `text-neutral-600` (`#525252`) on black is about 2.69:1 and is used for links in the footer build line injected by `scripts/build-stamp.mjs` on most pages, and `--ink-soft: #737373` is about 4.43:1 and is used for running heads, section labels, post meta and table headers, so dark mode fails WCAG AA for text site-wide.
```

## 0819-mirrors-pre-light

label 1 (kept), a11y, 0819; where: `mirrors/index.html`, `src/input.css`

```
`mirrors/index.html` has a `bg-zinc-900` `<pre>` block that never receives a light-theme override, so in light mode its text is about 2.29:1 against its background.
```

## 0819-search-focus-trap

label 1 (kept), a11y, 0819; where: `search.js`, `index.html`

```
The search overlay declares `aria-modal="true"` but `search.js` has no Tab trap (it tracks `lastFocus` only), so keyboard focus escapes the dialog on the second Tab press.
```

## 0819-content-language-meta

label 1 (kept), a11y, 0819; where: `index.html`, `tech/index.html`, `mirrors/index.html`, `profiles/index.html`

```
Most pages carry `<meta http-equiv="content-language">`, which is an HTML5 validator error; `<html lang="en">` already covers it.
```

## 0819-home-heading-outline

label 1 (kept), a11y, 0819; where: `index.html`, `experiments/index.html`, `projects/index.html`

```
The home page's heading outline is `h1, h3, h3`: its two `.section-label` headings are `<h3>` where every other page uses `<h2>` for the same role.
```

## 0819-reduced-motion

label 1 (kept), a11y, 0819; where: `experiments/porcine/`, `experiments/etherhoo/`, `src/input.css`, `scripts/experiments-input.css`

```
There is no `prefers-reduced-motion` guard anywhere except one `scroll-behavior` rule: `/experiments/porcine/` runs three infinite CSS animations plus a 1 Hz blinker and `/experiments/etherhoo/` mutates two tables on 0.8 s and 3.5 s timers forever, with no pause control.
```

## 0819-theme-toggle-name

label 0 (refuted), a11y, 0819; where: `index.html`, `theme.js`, `src/input.css`

```
The theme toggle button has no accessible name when JavaScript is disabled: its visible label is set by CSS `::before` content, which does not enter accessible-name computation.
```

## 0819-porcine-h1-triple

label 1 (kept), a11y, 0819; where: `experiments/porcine/index.html`, `experiments/porcine/`

```
The `<h1>` on `/experiments/porcine/` uses glitch pseudo-elements whose CSS `content: attr(data-text)` is folded into the accessible name, so a screen reader announces the title three times.
```

## 0819-empty-md-link

label 1 (kept), a11y, 0819; where: `blog/posts/art-tech-highlights.md`

```
`blog/posts/art-tech-highlights.md` contains a stray empty markdown link `[]()` that renders as an anchor with no text, producing a nameless tab stop.
```

## 0819-poap-vault-tabs

label 1 (kept), a11y, 0819; where: `experiments/poap-vault/index.html`, `experiments/poap-vault/app.js`

```
The collection filters on `/experiments/poap-vault/` use `role="tab"` with no corresponding tabpanel and no arrow-key handling, so the tab semantics are unbuilt; they behave as filter buttons.
```

## 0819-charset-late

label 1 (kept), source, 0819; where: `essentialism/index.html`

```
`essentialism/index.html` places its `<meta charset>` beyond the first 1024 bytes of the document because a long comment sits above `<html>`, outside the window browsers use for encoding sniffing.
```

## 0819-youtube-relme

label 1 (kept), content, 0819, external; where: `index.html`, `profiles/index.html`

```
The `rel="me"` link to YouTube on the home page and on `/profiles/` points at `youtube.com/thebenmeadows`, which returns 404; the `@thebenmeadows` handle form of the URL is the one that resolves.
```

## 0819-foundation-dead

label 1 (kept), content, 0819, external; where: `art/index.html`, `blog/posts/`, `index.html`

```
Three deep links on the site cite foundation.app pages (North of Eden, ABC Art World sales, Based Blue Death), and foundation.app no longer serves those pages, so the sales claims they support now cite dead pages.
```

## 0819-openagents-citations

label 1 (kept), content, 0819, external; where: `blog/posts/my-owner-asked-me-to-write-this-post-receipts-attached.md`

```
In the receipts blog post, three OpenAgents forum citations (including the forum root) no longer resolve, on a post whose thesis is to check its sources; the GitHub issue links in the same post still resolve.
```

## 0819-inpeak-links

label 1 (kept), content, 0819, external; where: `blog/posts/podcasts-public-speaking.md`

```
Six links to inpeak.xyz on the podcasts post are unrecoverable: the domain now forwards to an unrelated company and strips the path.
```

## 0819-tech-only-image

label 1 (kept), content, 0819; where: `tech/index.html`, `experiments/dls/`, `art/essentialism/`, `experiments/poap-vault/img/`

```
`/tech/` states that the only image on the site is the profile photo, which is contradicted by another image on the same page and by the dls JPEGs, the essentialism PNG, hundreds of poap-vault WebPs and every blog card image.
```

## 0819-sol-duplicate-card

label 1 (kept), content, 0819; where: `mirrors/index.html`

```
`mirrors/index.html` renders two name cards with the identical `.sol` href, while the surrounding prose describes four names and the grid shows five.
```

## 0819-tezos-editions

label 1 (kept), content, 0819, external; where: `art/index.html`, `art/essentialism/index.html`

```
`/art/` and `/art/essentialism/` say "44 editions on Tezos"; on-chain the token's edition size is 44 but only 8 are minted, so the wording conflates run size with minted count.
```

## 0819-porcine-credit

label 1 (kept), content, 0819, external; where: `experiments/porcine/index.html`

```
On `/experiments/porcine/` the visible credit reads "James Cramer (@harttotelll)" but the link's href is the handle `@hardtotelll`, and that account's display name is James Kramer, so both the surname and the handle in the visible text are wrong.
```

## 0819-sitemap-lastmod

label 1 (kept), content, 0819; where: `sitemap.xml`, `scripts/`, `git history of main`

```
`sitemap.xml` has `lastmod` values that are stale against git history on most of its 23 URLs, omits `/search/` and `/essentialism/`, and still carries an `xml-sitemaps.com` generator comment, making it the one artifact in the repo no build script produces.
```

## 0819-highlights-prose

label 1 (kept), content, 0819; where: `blog/posts/art-tech-highlights.md`

```
`blog/posts/art-tech-highlights.md` has a date written as 4/18/2023 whose machine-readable form decodes to 2024-04-16, plus a broken list rendering and missing quotation marks in its prose.
```

## 0927-speaking-no-way-in

label 1 (kept), content, 0927; where: `index.html`, `blog/posts/podcasts-public-speaking.md`, `projects/index.html`, `profiles/index.html`, `sitemap.xml`, `scripts/build-speaking.mjs`

```
No page links to `/speaking/`: the home page, the blog index, the Podcasts & Public Speaking post, `/projects/` and `/profiles/` carry no `href="/speaking/"`, and `sitemap.xml` has no `/speaking` entry, while the `/speaking/` index links back to the podcasts post.
```

## 0927-squint-signed-claim

label 1 (kept), content, 0927, external; where: `ai/wins.json`, `mdws-org/squint releases (v0.6.0)`

```
The Squint entry in `ai/wins.json` says the release is "a signed disk image" and links Squint v0.6.0, but that release's notes say it is not notarized and the DMG is ad-hoc signed with no Team ID.
```

## 0927-headers-new-sections

label 1 (kept), security, 0927; where: `_headers`, `marfa/`, `art/essentialism/syntax/`

```
`_headers` has no entries for `/ai/`, `/marfa/` or `/speaking/*`, so those pages send no `Onion-Location` while every older section does, and `/marfa/title-card.pdf`, `/marfa/plastic-cactus-announcement.webp` and `art/essentialism/syntax/*.js` get no cache rule while comparable media get `max-age=604800`.
```

## 0927-bitly-relative

label 1 (kept), content, 0927; where: `blog/posts/podcasts-public-speaking.md`

```
`blog/posts/podcasts-public-speaking.md` writes `[Presentation & Resources](bit.ly/MayCCA)` with no scheme, so the rendered href is relative and resolves under the post's own path, where it 404s.
```

## 0927-empty-link-2025

label 1 (kept), a11y, 0927; where: `blog/posts/art-tech-highlights-2025.md`

```
`blog/posts/art-tech-highlights-2025.md` contains a stray `[](https://x.com/TheBenMeadows/status/1718291806855860616)` after a `[3](…)` link, which renders as an anchor with no text or label.
```

## 0927-syn-operator-contrast

label 1 (kept), a11y, 0927; where: `art/essentialism/index.html`, `art/essentialism/syntax/`, `src/input.css`

```
In the light theme on `/art/essentialism/`, the `--syn-operator` colour `#6f7883` sits on a white background (the card is transparent) at 12 px, which is about 4.48:1, just under the 4.5:1 AA threshold.
```

## 0927-build-stamp-list

label 1 (kept), source, 0927; where: `scripts/build-stamp.mjs`, `scripts/build-speaking.mjs`

```
`scripts/build-stamp.mjs` lists pages by hand and its "every page accounted for" check counts only that list, which omits `/marfa/`, `/speaking/` and the transcript pages, so those ship with no build stamp while `/ai/` and the blog are stamped.
```

## 0927-marfa-lazy-lead

label 1 (kept), perf, 0927; where: `marfa/index.html`, `scripts/build-blog.mjs`

```
`marfa/index.html` marks its lead image `loading="lazy"` although it sits directly under the h1 and one paragraph; `scripts/build-blog.mjs` deliberately never lazy-loads a post's lead image for that reason.
```

## 0927-speaking-escaping

label 1 (kept), security, 0927; where: `scripts/build-speaking.mjs`

```
`scripts/build-speaking.mjs` interpolates `audio_cid` and `registry.root` raw into `href` attributes and text, and the filename-derived slug raw into the index `href` and the output path (a transcript file named `...md` would write over the repository's root `index.html`); `origin` is escaped but its scheme is not checked, and the marked configuration passes `javascript:` links through.
```

## 0927-speaking-cleanup

label 1 (kept), source, 0927; where: `scripts/build-speaking.mjs`

```
The cleanup loop in `scripts/build-speaking.mjs` deletes any directory under `speaking/` that contains an `index.html` (except `transcripts/`), so a hand-made page placed there vanishes on the next build.
```

## 0927-ai-wins-dates

label 1 (kept), source, 0927; where: `scripts/check-ai-wins.mjs`

```
`scripts/check-ai-wins.mjs` validates dates with `Date.parse`, which rolls impossible dates over (`2026-02-30` becomes March 2), so an impossible date passes the guard and the card prints it as written.
```

## 0927-mirrors-check-ports

label 1 (kept), source, 0927; where: `scripts/check-mirrors-page.mjs`, `mirrors.json`, `mirrors/index.html`

```
`scripts/check-mirrors-page.mjs` strips the port and username from `ssh://`-style addresses before matching, and matches by substring, so changing the SSH port in `mirrors.json` while the page still prints `-p 2222` passes the check.
```

## 0927-tailwind-speaking

label 1 (kept), source, 0927; where: `tailwind.config.js`, `scripts/build-speaking.mjs`

```
`tailwind.config.js` scans `ai/` and `marfa/` for class names but not `speaking/**`, so a utility class used only on a transcript page would be purged from the stylesheet and ship unstyled.
```

## 0927-build-order-related

label 1 (kept), source, 0927; where: `package.json`, `scripts/build-blog.mjs`

```
`package.json`'s `build` runs `build-blog` before `build-speaking`, and `scripts/build-blog.mjs` resolves a post's `related:` pages by reading generated HTML, so a post with `related: [/speaking/]` fails a clean CI build.
```

## 0927-dead-links-2025

label 1 (kept), content, 0927, external; where: `blog/posts/art-tech-highlights-2025.md`

```
On the 2025 highlights post, the link to `opensea.io/TheBenMeadows/collected` returns 404 and `abcartworld.com` no longer resolves in DNS.
```

## 0927-jsonld-csp

label 0 (refuted), security, 0927; where: `index.html`, `_headers`

```
`index.html` adds an inline `<script type="application/ld+json">` block, and the CSP in `_headers` uses `script-src 'self'` with no `'unsafe-inline'` and no hash for that block, so browsers refuse it and the Person schema never reaches a crawler, with no visible symptom.
```

## 0927-unlisted-feed-leak

label 0 (refuted), source, 0927; where: `scripts/build-feed.mjs`, `scripts/build-blog.mjs`, `scripts/build-search-index.mjs`, `blog/posts/art-tech-highlights-2025.md`

```
The new `unlisted` post flag is filtered by the blog index, the blog feed and the search index, but `scripts/build-feed.mjs` is unchanged and reads the shared page list, so the unlisted 2025 highlights post enters the site release feed at `/feed.xml` and `/rss.xml` and reaches subscribers.
```

## 0927-indent-outside-pre

label 0 (refuted), source, 0927; where: `scripts/build-blog.mjs`

```
`indentOutsidePre` in `scripts/build-blog.mjs` evaluates `inPre` before updating it for the current line, so the line opening `<pre>` is indented and the line closing `</pre>` is not, leaving the outer tags of every multi-line code block misaligned in the HTML source.
```

## 0819-sitemap-missing-blog

label 0 (refuted), content, 0819; where: `sitemap.xml`, `blog/posts/`, `scripts/build-blog.mjs`

```
`sitemap.xml` is missing seven pages that exist on the site, all of them blog post routes, so those posts are undiscoverable through the sitemap.
```

## 0819-infra-los-angeles

label 0 (refuted), content, 0819, external; where: `infra/index.html`

```
`/infra/` says the anycast service is "served from Frankfurt and Los Angeles at once", but the page's own location list names Fremont, Frankfurt, Kansas City and Manchester; Los Angeles appears nowhere else, so one of the two statements is wrong.
```

