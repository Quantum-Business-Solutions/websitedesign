# Guardrails

The accumulated "always / never" list. **Read this before generating any design work** — it's the
highest-value file here, because it's the only one that encodes decisions rather than observations.

A rule earns a place here only if it generalizes past the site it came from. Anything true of just
one reference stays in that entry's prose in `design/references.md`.

## Never

- No purple-to-blue gradient heroes on white. The single most recognizable AI-generated tell.
- No Inter as a default just because it's safe. If Inter is the right call, it should be a call.
- No three-equal-feature-card row as the section after the hero.
- No generic glassmorphism applied to every surface.
- No emoji as section markers.
- No centered long-form body copy — centering is for short display text only.
- Don't soften a tight radius into pill-shaped cards globally. Mixed radii can be deliberate
  (Linear runs 2px surfaces against fully-rounded buttons); a uniform `rounded-lg` everywhere is
  the tell.
- Don't number sections `01 / 02 / 03` unless the content is genuinely sequential.

## Always

- Reserve the accent for links and the primary CTA. If everything is accented, nothing is.
- Pick the neutral deliberately — a grey biased slightly toward the accent hue reads chosen; a pure
  mid-grey reads inherited.
- Pair a display face against a distinct body face. One family at one weight is the boilerplate
  signature. A condensed heading over a regular body (Orbit Media) is a cheap, effective move.
- Let the typeface do brand work. Söhne over a system sans is a large part of why Stripe reads
  bespoke rather than bootstrapped.
- State the design read before building: page kind, audience, aesthetic family. Guessing the
  direction is what produces slop.
- Build wide before going deep — several distinct directions first, then iterate the chosen one.
  Don't one-shot.
- Size body copy for the reading it actually requires. 15–16px is a default, not a decision;
  Basecamp runs 20px and GOV.UK 19px because both expect to be *read*. Long-form B2B copy at 15px
  is a legibility choice made by accident.
- Treat "no color" as an available direction. Vercel carries a whole page on type and a near-black
  accent. Reaching for a palette isn't automatically the richer choice.
- Match register to audience breadth. A broad or procedural audience wants the GOV.UK register —
  zero radius, maximum contrast, one unmistakable action — and most "sophisticated" styling is
  optional there.

- **Never composite text with `opacity`.** Use `color-mix()` instead. Opacity-composited text
  failed WCAG contrast measurement during the Revolution build — the computed value isn't what the
  checker sees, and it isn't auditable. This one cost real rework.

## Matching the medium to the reference

- **Don't approximate a render.** If a reference's quality comes from 3D rendering — soft shadows,
  ambient occlusion, beveled edges, material response — flat SVG or CSS polygons will not get close.
  They produce SmartArt: flat slabs, dead flat-fill "metal", and a diagram look. Either use a medium
  that can actually light a surface (WebGL, or a real Blender/Spline render) or pick a different
  concept. A footnote admitting the output is flat does not make shipping it acceptable.
- Corollary: decide the medium *before* building, from what the reference depends on. Getting this
  wrong wastes the whole build, not just the finish.
- **A hand-written shader is not a render pipeline.** Upgrading flat SVG to a raymarched SDF fixed
  the geometry and still produced a butter-stick core and soap-bar segments — because the gap was
  never bevels or shadows, it was materials, HDRI lighting, global illumination, and art direction.
  Those are craft disciplines, not parameters to tune.
- **Stop after two failed attempts and switch to briefing.** If two honest passes at an asset both
  miss, further iteration is burning the reviewer's patience, not converging. Write the
  art-direction brief for someone who owns the medium — that's the deliverable at that point.
- Arbitrary decoration is a tell. If a mark can't answer "what does this represent," cut it — small
  accent dots and rings sprinkled on surfaces read as filler, because they are.

## Reading measured tokens

- A radius like `33554400px` means "fully rounded" (browser-computed), not a literal value. Read it
  as `9999px`.
- Fractional type sizes (`55.87px`) mean a fluid/responsive scale measured at one viewport. Read
  them as ratios, not authored numbers.
- Extractors mislabel state colors as base colors. GOV.UK's `link: #FFDD00` is its focus highlight;
  Vercel's `link: #9A050F` doesn't match the visible treatment at all. Sanity-check a color against
  the site before building on it.

## Sourcing

- Ingest **live sites**, not gallery images. A shipped site has survived real content, long copy,
  and responsive breakpoints; a concept shot hasn't.
- Don't store scraped Dribbble content in this repo. Their API can't serve it anyway (every read
  endpoint is scoped to the authenticated user's own shots — no search or browse), and their terms
  are explicit: *"Scraping, copying, saving, or storing our data is strictly prohibited."* This
  library backs commercial client work, so treat that as binding. Browse galleries to **discover**,
  then ingest the real site.
- Never hand-write a value into `design/tokens/`. That directory is the boundary between measured
  and guessed, and it holds only measured. Observations go in prose.

## Structured data

- **Never hand-write JSON-LD into a rich-text block.** Derive it from the module's own fields, so
  markup and visible copy cannot drift. Drift means Google declines to show the rich result — and
  the block silently stops earning anything. Copy the `quantum-faq.module` pattern.
- **`|escapejson` on every interpolated value.** Without it, one apostrophe from a client silently
  invalidates the whole block.
- **Omit schema rather than guess it.** Absent markup is safe — a search engine infers the entity
  from the page. Wrong markup is a false statement in the one format engines are built to trust.
  This is why the nine themes hardcoding QBS's `Organization` is worse than shipping none.
- **Never mark up self-published testimonials with `AggregateRating` or `Review`.** Self-serving
  reviews are ineligible for review rich results and marking them risks a manual action. Leave
  `quantum-reviews` unmarked.
- **Don't promise rich results that no longer exist, and check the date before you assert one.**
  HowTo retired 2023. **FAQ retired entirely 7 May 2026** — not restricted, gone. The sitelinks
  searchbox went November **2024**, though `WebSite` still drives site names. Of the rest: only
  `Event` unreservedly earns a rich result; `BreadcrumbList` is desktop-only; `Product`/`Offer`
  needs a single-product page; `Article` is an enhancement, not a rich result; `Service` earns
  nothing visible. Sell "machine-readable entity graph," never "rich results."
- **Structured data is not an AEO lever.** Google: "structured data isn't required for generative AI
  search, and there's no special schema.org markup you need to add." The one thing that does help is
  markup **agreeing with the visible text**. Don't sell `FAQPage` as an AI-citation driver, and
  don't build `llms.txt` — Google ignores it.
- **Section-level schema belongs to the module that renders the content.** Delete the section,
  delete its markup — correct behaviour, free. **Site-level entity markup is the exception**:
  `Organization`, `BreadcrumbList` and `WebSite` describe the site, not a section, so they belong in
  `templates/layouts/base.html`. A site's identity cannot live in a block a client can delete.

## Typefaces on the watchlist

Two faces are LLM defaults — the ones a model reaches for when it has nothing to design against.
Neither is banned; both need a reason beyond "it looked right":

- **Inter** — the default sans of every AI-generated interface.
- **Space Grotesk** — the default "technical" face. This is why `Quantum Converter` carries a
  caution in `themes/catalogue.md`: it's the right call when a genuinely technical register is
  needed, and the theme most likely to read generic.

## Reading measured tokens — two live examples in this repo

The extractors mislabel, and the token files here prove it. Both of these are in
`design/tokens/` and neither is a bug in the file — the file records what was measured:

- **`stripe.json`** has `textPrimary: #533AFD` (the indigo accent) and `primary: #061B31` (the
  near-black body colour) — swapped relative to their roles. It also reports
  `body: 32px`, identical to its own `h2`, which is a fluid-scale artefact, not a real body size.
- **`linear.json`** has `textPrimary: #08090A` identical to `background: #08090A` — black on black,
  which is obviously not what the site renders.

Never port a token straight into a theme field. Look at the live page first.

## Card grids must balance. No orphan rows.

A section with six cards on the first row and two on the second reads as a mistake, because it is
one — nobody chose that, a `grid-template-columns` did. The last row of a card grid must be full, or
close enough that it reads as deliberate.

**The fix is almost always the column count, not the content.** Six cards is perfect at three
columns and bad at four. Four cards is perfect at four or two and bad at three. So change the grid
before you change the client's content.

### Safe counts, by column width

`+1 ORPHAN` is never acceptable. `weak` means lopsided — allowed only if the section genuinely
can't be another count.

| Cards | 4 col | 3 col | 2 col |
|---|---|---|---|
| **2** | — | — | 2×1 ✅ |
| **3** | — | 3×1 ✅ | +1 weak |
| **4** | 4×1 ✅ | **+1 ORPHAN** | 2×2 ✅ |
| **5** | **+1 ORPHAN** | +2 ok | +1 weak |
| **6** | +2 weak | 3×2 ✅ | 2×3 ✅ |
| **7** | +3 ok | **+1 ORPHAN** | +1 weak |
| **8** | 4×2 ✅ | +2 ok | 2×4 ✅ |
| **9** | **+1 ORPHAN** | 3×3 ✅ | +1 weak |
| **12** | 4×3 ✅ | 3×4 ✅ | 2×6 ✅ |

**12 is the only count that is clean at every width.** After that, 2 · 4 · 8 are clean at 4/2/1, and
3 · 6 · 9 are clean at 3.

### It has to hold at every breakpoint

This is the part that gets missed. A grid balanced on desktop can orphan on tablet, so the cascade
is part of the decision:

| Cards | Cascade |
|---|---|
| 3 or 9 | 3 → **1**. **Skip 2 columns entirely** — both orphan there |
| 4 or 8 | 4 → 2 → 1. **Skip 3** — 4 orphans at 3 |
| 6 | 3 → 2 → 1 |
| 12 | 4 → 3 → 2 → 1 |

### When the count is genuinely fixed

Five services is five services. Three options, in order of preference:

1. **Change the column count** so the remainder is at least half a row (5 at 3 columns is 3+2 — fine).
2. **Make the odd one deliberate.** A first card spanning two columns, or a last card spanning the
   remainder, reads as designed rather than as leftover. `grid-column: span 2` on one item.
3. **Change the count.** Merge two weak cards, or find a sixth. Often the right answer — a list
   padded to fill a grid is usually a list with a weak item in it.

What is never acceptable: leaving one card alone on a row beneath three or more.

### Checked automatically

`scripts/verify.mjs` measures actual rendered rows at 390 / 768 / 1440 and fails on an orphan, so
this rule does not depend on anyone remembering it.
