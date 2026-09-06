# QA findings — 2026-09-03

Four QA agents audited this repo in parallel: internal consistency, independent re-verification
against the live portal and site, an end-to-end process walkthrough, and a technical fact-check of
the SEO/AEO claims against primary sources.

Everything below was **verified**, not asserted. Where a claim this repo made turned out to be
wrong, it says so. Two findings invalidated an architectural premise and are fixed; several
client-facing promises turned out to be unsellable as written.

---

## The two that changed the architecture

### 1. `theme.colors` is wired to nothing. The "six-value re-skin" was five dead fields.

**Verified directly.** Across every file in the nine themes, `theme.colors` is referenced **zero
times** — not in `css/quantum.css` (which contains no HubL at all, no `{{` anywhere), not in
`base.html`, not in the partials, not in any of the 57 `module.html` files, not in `quantum.js`.
Every colour is a hardcoded hex.

So setting `colors.gold` in the theme editor **changed nothing on the rendered page.** The entire
"six values per theme" model in `process/reskin.md` — and the Firecrawl-token mapping table built
on it, and the tier definitions that rest on it — described a mechanism that was not connected.

**The real surface**, found by reading `quantum.css`:

```
:root                                     base --q-* tokens (identical in all nine)
[data-theme="dark"] / [data-theme="light"] the mode palettes
[data-qdir="clean"] … [data-qdir="void"]   ALL NINE directions, in EVERY theme's CSS
/* ===== NATIVE DIRECTION: <Theme> ===== */
  :root, [data-theme="dark"], [data-theme="light"] { … }   ← pins this theme's direction
```

The nine themes are **one stylesheet with nine presets**, and a native-direction block selects
which. That block is twelve custom properties in one contiguous place — so re-skinning is *more*
tractable than the fields story suggested, not less.

Two consequences worth stating plainly:

- **Typefaces ARE re-skinnable.** `--q-serif` and `--q-sans` are in the native block.
  `themes/catalogue.md` said "to change the typeface you change theme, which is the point" — that
  was true of `fields.json` and false of the product.
- **Whatever re-skinning has been delivered was done by editing CSS**, not fields. The documented
  process did not describe what actually happens.

**Fixed:** `scripts/reskin.py` patches the native-direction block. `process/reskin.md` rewritten.

### 2. The "mode bug" was real but its consequence was wrong

All nine do default `appearance.mode: dark`. But the native-direction block sits **last, at equal
specificity**, and assigns the same palette to `:root`, `[data-theme="dark"]` and
`[data-theme="light"]`. So it wins, and **the light themes render light.**

Measured `--bg` per theme: Flagship / Void / Signal / Converter `#080b12`; Clean `#ffffff`; Press
`#f7f4ec`; Paper `#f4efe4`; Journal `#fbfaf6`; Showcase `#ffffff`. Correct, every one.

So *"Clean, Press, Paper, Journal and Showcase render dark out of the box"* — repeated in six files
and called a trap in five — **was false.** `mode` still drives the `.only-dark` / `.only-light` logo
visibility rules, so it isn't inert and should still be set. But "always set it explicitly" was
advice with almost no payoff, and we were treating a vestigial field as a critical bug.

---

## New defects the tooling found

### 3. All five light themes fail WCAG AA on button text

`scripts/reskin.py audit` measures `--cta-fg` against `--q-gold`:

| Theme | Accent | CTA text | Contrast | AA (4.5:1) |
|---|---|---|---|---|
| Flagship / Void / Signal / Converter | `#c4a44a` | dark | **8.2:1** | pass |
| Clean / Paper / Journal / Showcase | `#9a7d3f` | `#fffdf7` | **3.9:1** | **fail** |
| Press | `#a9812f` | `#fffdf7` | **3.5:1** | **fail** |

Near-white text on a mid-tone gold. This is every primary button on every light-theme site, and it
is a genuine accessibility failure sitting in the product line right now. The four dark themes are
fine.

`reskin.py plan` now refuses to apply a re-skin that fails this gate.

### 4. The harness found accessibility failures on the live site

`node scripts/verify.mjs` on `/website-services`, at all three widths:

- **`aria-dialog-name`** — the "Ask Quantum" chat widget is a dialog with no accessible name, so a
  screen-reader user is dropped into an unlabelled dialog.
- **`link-in-text-block`** — links inside body copy are distinguishable from surrounding text by
  **colour alone**, which fails WCAG 1.4.1. Needs an underline or a non-colour cue.
- **Heading order skips h2 → h4.**

Two things worth noting about the same run. CLS measured **0.016** — well inside the 0.1 budget, so
the missing image dimensions have not actually cost anything on this page yet. And the run produced
a **false positive** on placeholder text: `\byour company\b` matched the legitimate line "Are AI
engines citing your company?" The pattern list was tightened to bracketed and template forms only.

### 5. The header and footer leak QBS's identity — visibly, and worse than the schema does

The repo framed `Organization` JSON-LD as the identity problem. But
`templates/partials/header.html` and `footer.html` hardcode QBS's **logo images**, LinkedIn,
Facebook and Instagram URLs, QBS nav links (`/outbound-sales`, `/zoominfo-as-a-service`, `/cas`), a
Quantum Academy enrolment link, and `Copyright © {{ year }} Quantum Business Solutions`.

A crawler has to be told about bad schema. A client notices their site carrying our logo in five
seconds. And both files are `templateType: global_partial` — **portal-scoped singletons**, so
per-client overrides are not a simple clone-and-edit. `reskin.py` reports the leak and explicitly
does **not** claim to fix it.

### 6. Eight of the nine themes have never rendered a live page

All 41 Void site pages plus the landing page use `Quantum Void/templates/mv-shell.html`. **Zero**
live pages use Flagship, Signal, Converter, Clean, Press, Paper, Journal or Showcase. The catalogue
calls the nine "published and sold"; eight are sold and unproven. A client's site would be the
first real test — which, combined with finding 3, is how a contrast failure reaches production.

### 7. Void's schema leak includes a person's name and email

Eight of the nine `base.html` files are byte-identical. **Void's is different** — a richer block
with `@id`, `logo`, a `founder` Person (**Shawn Peterson**, with LinkedIn) and a `contactPoint`
carrying **shawn@thequantumleap.business**. Void also emits `WebSite` + `SearchAction` and a HubL
`BreadcrumbList` that the other eight lack.

So a client site cloned from Void publishes Shawn's name and email as its own founder and sales
contact — and two rows of `structured-data.md`'s "missing" table were wrong for Void.

### 8. The `og:image` gap is 31 pages, not one

`launch-standards.md` treated it as a `/website-services` finding. From the pages API, **31 of 41**
Void pages have an empty `featuredImage` — including `/about-us`, `/contact-us`, `/pricing`,
`/technology` and every playbook page.

---

## Where this repo's own numbers were wrong

| Claim | Reality |
|---|---|
| "Each is 21 templates" | **19** `.html` files (16 page templates + `base` + 2 partials). Void has **59**. 21 is only reachable by counting CSS and JS as templates |
| "`home.html` is one `dnd_area` with **14** `dnd_section`s" | **7**. The 14 came from a naive grep that counted `{% end_dnd_section %}` too |
| "**Every** page is a `dnd_area`" | **12 of 16.** `blog-listing`, `password-prompt`, `system-404`, `system-search` are hardcoded markup. Defensible for system pages; not accurate as written, and the editability claim leaned on it |
| "All nine `Organization` blocks identical" | Eight identical; **Void differs materially** (finding 6) |
| "No `preconnect` or `preload` anywhere. **Zero.**" | Void's `base.html` has **two** preconnects, and the live page loads fonts by `<link>` from its own `headHtml`. The prescribed fix was already in place on the page it was measured against |
| The `@import` line quoted as "measured" | Was **Press's** (Playfair Display). The page measured was **Void** (Instrument Serif) |
| "No `<img>` has width/height" | **1 of 15 does** — a ZoomInfo tracking pixel. 14 of 14 *content* images have neither, so the CLS finding stands; the absolute doesn't |
| "The money page has **no** on-page conversion path" | No forms and no embeds — correct. But **10 occurrences** of a `meetings.hubspot.com/shawn-peterson` link across four CTAs. Off-page links, so the argument survives; the phrasing didn't |
| "66 temporary redirects against a 77-page crawl budget" | 99 crawled, 100 limit. "77" was a stray |
| "Service pages drive about 10%" | **No service page earns any.** The other 18% is the homepage and one guide |
| "position 11 across four keywords worth ~1,700" | **Positions 11–14.** Three at 11 (1,330 searches) plus one at 14 |
| "3–5 directions" (`build-sequence.md`) | Three everywhere else, and three is load-bearing |

**What held up exactly:** 57 modules per theme and 61 for Void, with the four extras named
correctly. `fields.json` byte-identical across all nine. Only `quantum-faq` emits structured data,
across 175 module files. The published six phases and day ranges, and all three package tiers,
**row-for-row verbatim**. The 82% blog-traffic figure. All nine grounds and typefaces.

---

## Where the SEO/AEO claims were stale or overstated

The engineering judgement was sound. The factual base was 1–3 years out of date in five places, and
the AEO section was contradicted by Google's own guidance.

### Corrections made

- **FAQ rich results are fully retired, not restricted.** We said "restricted Aug 2023 to
  government and health sites." Google **deprecated the feature entirely on 7 May 2026** —
  documentation removed, no longer testable in the Rich Results Test. Keeping `FAQPage` markup is
  harmless; **selling** it is not.
  Also a trap: do **not** migrate to `QAPage`. Google lists "an FAQ page written by the site itself
  with no way for users to submit alternative answers" as an *invalid use case*.
- **The sitelinks searchbox retired November 2024, not 2023** — and the conclusion was wrong.
  `WebSite` structured data still controls the **site name** shown in results, which is a live
  visible feature. It belongs in the earns-something list, on the **home page only**, not in
  `base.html`.
- **`Organization` belongs on the home page or one about page**, not site-wide. Google says so
  explicitly. Our proposed fix put it in `base.html` on every page — which is also why the Semrush
  audit reported "ORGANIZATION 9 valid."
- **We overstated the penalty for wrong markup, in four places.** "Drift is what Google penalises"
  has no source. What actually happens: Google **ignores** it, usually. At worst a page-level
  structured-data manual action, which costs rich-result eligibility and **does not affect
  ranking**. The premise "wrong is worse than none" still holds — but on the grounds that it is a
  documented guidelines violation ("don't misrepresent your ownership, affiliation, or primary
  purpose"), it forfeits knowledge-panel eligibility, and it corrupts the one thing `Organization`
  exists to do. Not on a ranking penalty that doesn't exist.
- **302s do pass authority.** Google reversed this in 2016. The real mechanism is worse for the
  client anyway: a 302 tells Google to keep the **old** URL canonical, so after a redesign the new
  URL may never replace it. The operational conclusion — convert them, 301 every changed URL — is
  unchanged. The reasoning was folklore.
- **Review markup: right rule, wrong scope.** Self-serving `Review`/`AggregateRating` under
  `Organization`/`LocalBusiness` is ineligible — correct. But first-party **customer reviews of a
  specific product** on a `Product` page are explicitly supported. The guardrail as written would
  have wrongly forbidden legitimate markup on an e-commerce client.
- **The AEO priority list was effectively inverted.** Google's May 2026 guide has a section titled
  "Mythbusting generative AI search," and three of our four factors appear in it on the wrong side:
  *"Structured data isn't required for generative AI search"*; *"chunking content"* is a myth;
  *"rewriting content just for AI systems"* is a myth. The **only** structured-data item Google
  names as helping is *"making sure your structured data matches the visible text"* — which was our
  #4 and should be our #1.
  The strongest measured signal is somewhere we weren't looking: **off-site brand presence.**
  Ahrefs, 75,000 brands: YouTube mentions ~0.74 correlation, branded web mentions 0.66–0.71,
  backlinks only 0.28–0.34. Schema wasn't a studied variable. The one study that does measure schema
  reports prevalence with no control group — and its own numbers show most AI-cited pages carry no
  `Organization` schema at all.

### Client-facing promises that are not achievable as written

1. **"Full schema set (Article, Service, Offer, Breadcrumb)"** as a Growth/Transform deliverable.
   On a services site: `Service` isn't in Google's search gallery at all and earns nothing visible;
   `Offer` on a three-tier pricing page won't produce a rich result (Google supports single-product
   pages, not category pages); `BreadcrumbList` is **desktop only** since Jan 2025 — while our own
   gate says "mobile scores, not desktop"; `Article` is an enhancement to a normal result, not a
   rich result, and has **no required properties**. Sell it as a machine-readable entity graph.
   Never as rich results.
2. **`FAQPage` as "the strongest AEO signal we ship."** Unsupported, and the feature is retired.
3. **The AEO score grader.** Google, in the same guide: *"Be wary of third-party tools that promise
   ranking success or claim to use 'internal' Google metrics. No third-party tool has access to our
   internal ranking or AI systems."* Our own Rule 1 — never quote a score without reading what's
   underneath it — applies to the score we **sell**, not just the ones we buy. We also quoted
   Semrush's "AI Search Score 94" uncritically two paragraphs after establishing that rule.
4. **"Core Web Vitals tuning is the single biggest available win."** Contradicted by our own
   measurement: Semrush performance **97/100**. The SEO file is right that the biggest win is the
   page parked at position 11.
5. **"Moving that page into the top five."** Position isn't a controllable output. Sell the inputs.

### Performance corrections

- **`@import` → `<link>` saves one serial hop, not two.** Three steps become two; the real win is
  **discovery by the preload scanner** instead of after `quantum.css` downloads. "Four round trips
  vs two" was wrong.
- **Self-hosting woff2 is not automatically better.** web.dev: *"the performance differences between
  these two options is less clear cut"* — the Web Almanac found third-party fonts sometimes render
  faster. Conditional on replicating subsetting. Measure before committing nine themes.
- **`display=swap` is the main cause of font CLS.** We praised it under "what the themes get right"
  and three sections later called CLS a ranking signal. Keep `swap` for display type; use
  `optional` or matched fallback metrics for body text.
- **Adding `width`/`height` will not fix CLS while the CSS sets `height:100%`.** An explicit CSS
  height overrides the attribute-derived aspect ratio. The fix needs `height:auto` or a container
  `aspect-ratio`. Our proposed fix would have reserved nothing.
- **INP is missing entirely.** Core Web Vitals are LCP, **INP**, CLS. On HubSpot this is the likely
  real weak spot: `standard_header_includes` injects jQuery. Disabling it or moving it to the footer
  is a **portal setting**, not a theme fork — a bigger, cheaper win than nine CSS edits.
- **`loading="lazy"` by default is risky without the above-the-fold toggle.** web.dev data: pages
  using lazy loading have *worse* median p75 LCP (3,546ms vs 2,922ms), because the fold gets
  misjudged. Also `lazy` + `fetchpriority="high"` together is pointless.

### Missing from the process entirely

- **Google Search Console.** The largest single omission. The **Generative AI performance report**
  (rolled out globally Aug 2026) is the *only* first-party AI-visibility data that exists. Selling
  an AEO Health Check without it has a hole in the middle of the product.
- **`nosnippet` / `max-snippet`.** One stray directive silently zeroes AI Overviews and AI Mode
  eligibility. Belongs in the launch gate.
- **AI crawler user agents — and we'd have got them wrong.** The retrieval bots are
  `OAI-SearchBot` (not `GPTBot`, which is training-only), `Claude-SearchBot` and `Claude-User` (not
  `ClaudeBot`, which is training), and `PerplexityBot`. `Google-Extended` governs Gemini training,
  **not** AI Overviews.
- **`llms.txt` is a non-task** — name it as one so nobody sells it. Google ignores it; server logs
  show AI systems don't even request it.
- **Off-site brand presence, YouTube, content refresh cadence, `LocalBusiness` + Google Business
  Profile, an internal-linking standard, author bio pages.**
- **Terminology:** Google's position is that optimising for generative AI search *is* SEO, and it
  points its guidance-on-evaluating-third-party-SEO-advice page directly at AEO/GEO vendors.

---

## Process gaps

Ranked by what they'd cost. The full walkthrough used a 12-location dental group on Growth, on
WordPress, with no blog — chosen to stress what I suspected wasn't covered.

**Would break a delivery**

1. **Growth sells a schema stack the product cannot emit.** `BlogPosting`, `Article`, `Service`,
   `Offer`, `BreadcrumbList`, `Event`, `Person` are all missing from the themes, the fix is
   unapproved, and hand-writing JSON-LD is banned by our own guardrail. Either approve the source
   fix before the next Growth sale or mark the line item blocked.
2. **No CMS migration procedure.** Zero occurrences of WordPress, content inventory, DNS, cutover
   or rollback anywhere in the repo — while "monitored launch" is a sold promise. The URL map is
   named as a Phase 02 output with no method behind it.
3. **Multi-location cannot be served.** No location/address/hours module in the 57, no
   `locations.html`, no `LocalBusiness`. For a practice group or dealer network, local visibility
   *is* the traffic.
4. **The Launch tier was logically impossible.** It said "no clone needed," and the launch gate
   requires `mode` set and the schema naming the client — which on an un-cloned theme means editing
   one of the nine. **Fixed:** every tier clones.
5. **No named approver anywhere.** "Needs approval" appears in seven places without a person or
   role. "Signed-off build" has no definition of sign-off.
6. **No client platform prerequisite.** Growth includes blog setup and CRM-landing forms; nothing
   states what HubSpot subscription the client must hold, or who buys it.

**Would blow the 90 days**

7. **Phase 04 Content Writing has no method** — days 30–50, the long pole, and the process's whole
   coverage is a QA criterion.
8. **Revisions are unbounded.** "Refined with your feedback at every step" with no round cap, no
   change-order trigger, no meeting cadence.
9. **Page count vs 12 locations.** Growth is "up to 20"; that client needs 27+. No rule says whether
   one template plus N instances counts as one page or N.
10. **Semrush pull 4 is blocked for a new client** — no project exists, and the crawl takes hours.
    Start it on day one.

**Would reduce quality**

11. **`brands/_template.md` had no slot for six things other docs mandate writing there** — entity
    facts, the SEO baseline, the soft offer, the promise verbatim, the tier purchased, competitors
    ingested. Phase 05 consumed fields Phase 01 had nowhere to write. **Fixed.**
12. **`website_projects` cannot record `appearance.mode`** — the schema is a five-key jsonb with no
    mode and no theme path, so nothing links the row to the artifact.
13. **No documented way to onboard a new client into BrandCommand.** Step 1 starts with
    `list_brands` → `brand_profile_id`; a new client has none.
14. **No regulated-industry copy review.** No HIPAA, YMYL or E-E-A-T anywhere. For medical content,
    a named credentialed author is a *content* requirement, not a markup one.
15. **"Blog setup" is never defined**, and a client starting from zero content has no branch.
16. **No phase exit criteria**, and `checklist.md` fires once, at the end.

**Also found:** the Space Grotesk watchlist that `catalogue.md` cited didn't exist in
`guardrails.md`; `/design-inbox` isn't a command; `build-sequence.md` predated five process docs and
cited none of them; `design-ingest.md` quoted the wrong inbox marker and would have filed entries
two sections too low; the only worked example in the repo (`revolution-office.md`) uses typefaces
that aren't in the nine, because it predates the methodology; `SCHEMA.md`'s "deterministic" slug
rule produces `gov-` for `gov.uk`; `stripe.json` has its text colours swapped and `linear.json` has
black on black, both unflagged; and QBS's own flagship page hand-pastes its `FAQPage` and `Service`
JSON-LD into per-page `headHtml` rather than using `quantum-faq` — the exact drift failure mode our
guardrail warns about, on our own site.

---

## Fixed in this pass

`scripts/reskin.py` repointed at the real CSS surface, with a contrast gate that refuses to apply a
failing re-skin · `process/reskin.md` rewritten · Launch tier now clones · every wrong number above
corrected · the SEO/AEO claims corrected against primary sources · the missing guardrail written ·
`brands/_template.md` given the six missing sections · the dangling command and marker references
fixed · `build-sequence.md` demoted to rationale with an explicit authority order.

## Still open

The theme-level fixes are still writes to portal `20682069` and still need approval — and the list
is now longer and better-argued than it was: the native-direction block is the real target, the
light-theme contrast failure is new and shipping, the header/footer leak is worse than the schema,
and INP/jQuery is a portal setting that may beat all of it. See `process/roadmap.md`.


---

## 2026-09-06 — two passes on the Kelly build and the theme fix

**Theme fix (pre-upload review of `scripts/themefix.py` output), seven findings, all fixed before upload:**
1. **Blocker.** Theme-level `fields.json` rejects text/image/menu fields. Brand and schema moved into
   three modules included from the global partials.
2. `require_js` for `quantum.js` had been dropped from the shared base — nine interactive modules
   would have gone dead. Restored (the new base patches the original head instead of replacing it).
3. The `color:var(--q-gold)` rewrite matched the tail of `border-color:`; anchored with a lookbehind.
4. `|replace('/$','')` is a literal replace in HubL; now `|regex_replace`.
5. Skip link had no target on four templates; the target is now a `#q-content` wrapper in base.html.
6. Dark `section_bg` bands on light themes have a pre-existing `--fg` problem (1.1:1). Not fixed here.
7. Breadcrumb names were not JSON-escaped; now `|tojson`.

**Kelly pitch page, fourteen findings, the ones that changed the tool:**
- The hero *subhead* was the brief's design read ("a regional office-technology dealer site for…")
  rendered under the client's headline. `--subhead` is now required.
- Accent text on light grounds used the fill color (2.3:1). The mock now uses the derived ink.
- Confidential detail (a revenue target, an internal hostname, source-system names) leaked onto a
  shareable page. Constraints render without their source tag; the growth target moved out of the
  rendered section of the brief.
- "What you told us, taken as binding" when nothing had been told. Retitled.
- 390px: table overflow, nav labels wrapping, an orphaned stat. Fixed in the mock CSS.
- Signal as a dark wildcard against a measured light category was a loophole, not an argument.
  Rule 5's typeface classes were refined (humanist sans vs display grotesque) so the vertical's own
  playbook — Clean / Showcase / Press — passes the selection check.
- "A+ BBB since 1960" cannot be true (letter grades date from 2009). "BBB-accredited since 1960."
- No recommendation, no findings, no hero render on the page. `--recommend` and `--findings` added;
  the recommended direction has a high-fidelity home page render.

**Still open from that pass:** the three preview panels share one layout and differ only in ground
and heading face — honest, but a per-theme hero treatment would show what Press does editorially.
