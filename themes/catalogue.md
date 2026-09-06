# The nine Quantum themes

Hand-built HubSpot themes on portal `20682069`. Each is a complete site kit, not a page:
**19 HTML files** — 16 page templates (home, interior, pricing, case study, casestudy-index, blog
listing and post, contact, landing, event, playbook, thank-you, all-modules, 404, search,
password-prompt) plus `layouts/base.html` and two partials — with shared CSS, JS and 57 modules.

Void is the exception at **59** templates: it carries the live QBS site's per-page shells.

> Earlier versions of this file said "21 templates." That was wrong — verified by counting. 21 is
> only reachable by counting `quantum.css` and `quantum.js` as templates.

**These are the product.** Client website options are three of these nine, re-skinned to the
client's brand — not designs generated from scratch. That's what makes the output reliably good:
you start from something already built well instead of from a model's average.

## The nine

Each theme's identity is its **ground** (light or dark) and its **heading typeface**. The layout
system is shared, so the typeface does the character work — which means you pick a theme partly
*for* its typeface.

Body type is *nearly* shared: `--q-sans` is Inter in Press, Clean and Showcase and DM Sans in the
other six.

| Theme | Ground | Headings | Reads as | Reach for it when |
|---|---|---|---|---|
| **Flagship** | Dark | Fraunces | Established, expensive, confident | Top-end professional services; the client wants to look like the incumbent |
| **Void** | Dark | Instrument Serif | Sophisticated, restrained, brand-forward | Design-conscious buyers; elegance over energy |
| **Signal** | Dark | Poppins | Tech-forward but approachable | SaaS, product, AI — friendly rather than austere |
| **Converter** | Dark | Space Grotesk | Technical, developer-credible | Platforms, data, infrastructure. **See the caution below.** |
| **Clean** | Light | Open Sans | Maximum clarity, zero personality | Broad or non-technical audiences; procedural content; accessibility-first |
| **Press** | Light | Playfair Display | Editorial, traditional-premium | Consultancies, law, finance, heritage brands |
| **Paper** | Light | Spectral | Long-form, considered, literary | Content-heavy sites; thought leadership |
| **Journal** | Light | Newsreader | Journalistic, credible, text-forward | Research, reports, media, anything evidence-led |
| **Showcase** | Light | Bricolage Grotesque | Contemporary creative, design-aware | Agencies, portfolios, creative services |

Four dark (Flagship, Void, Signal, Converter) · five light (Clean, Press, Paper, Journal, Showcase).

These nine are **published and sold** — see the theme grid on
[thequantumleap.business/website-services](https://www.thequantumleap.business/website-services).
The grounds and typefaces on that page match this table exactly. Two notes on the public copy: it
calls Void "our flagship look" (accurate — Void is the live Quantum site) while a separate theme is
*named* Flagship, which reads as a contradiction in a list of nine; and the sales line worth
repeating is **"nine themes, one design system, all yours — no licences, no lock-in."**

## Selection rules

Show **three**, chosen so the client is picking between real alternatives rather than shades of one
idea.

1. **Ground is filtered by the brief, not by taste.** If the client asked for light — as Revolution
   did — the dark four are out. Full stop. This single rule would have caught the "Ink" mistake.
2. **One safe, one stretch, one wildcard.** Safe = closest to where the brand is now. Stretch =
   where you think it should go. Wildcard = a genuinely different register. All three safe is a
   wasted presentation; all three wild and the client picks nothing.
3. **Match the typeface to the reading load.** Long-form and evidence-heavy → Paper or Journal.
   Scannable and conversion-led → Clean, Signal, Showcase. Prestige and low word count → Flagship,
   Void, Press.
4. **Category-check against competitors.** Ingest two or three via `/design-ingest` first. If the
   whole category is dark-and-technical, a light editorial theme *is* the differentiator — and vice
   versa. Don't differentiate by accident.
5. **Never show two themes with the same ground and a similar typeface class.** Press and Journal
   are both light serifs; showing both wastes a slot.

### Caution: Converter

Space Grotesk is on the house watchlist in `design/guardrails.md` as an AI-default tell — it's one
of the two faces LLMs reach for automatically. Converter is still the right call when a genuinely
technical register is needed, but it's the theme most likely to read generic, so it needs the
strongest justification before it goes in a set of three.

## What's actually wrong with the theme set

Four verified defects. Details and evidence in `process/qa-findings.md`.

**1. All five light themes fail WCAG AA on button text.** `--cta-fg` on `--q-gold`:

| Theme | Contrast | AA needs 4.5:1 |
|---|---|---|
| Flagship · Void · Signal · Converter | 8.2:1 | pass |
| Clean · Paper · Journal · Showcase | 3.9:1 | **fail** |
| Press | 3.5:1 | **fail** |

Near-white text on a mid-gold. Every primary button on every light-theme site.

**2. All nine emit QBS's `Organization` JSON-LD** in `templates/layouts/base.html`, so a client site
declares itself to be Quantum Business Solutions. **Void's is worse** — it also carries a `founder`
Person and a `contactPoint` with a real name and email address.

**3. The header and footer hardcode QBS's identity** — logo, nav, social links, copyright. Visible
to the client in five seconds, and they're `global_partial`s, so not a clone-and-edit. See
`process/reskin.md`.

**4. Fonts load through a CSS `@import`** in all nine — one extra serial hop, and invisible to the
preload scanner.

### The mode field is vestigial, not broken

All nine default `appearance.mode: dark`. Earlier versions of this file called that a bug that made
the five light themes render dark. **That was wrong.** The native-direction block in `quantum.css`
sits last at equal specificity and assigns the same palette to `:root`, `[data-theme="dark"]` and
`[data-theme="light"]`, so it wins — and the light themes render light. Measured `--bg`:

`#080b12` for Flagship, Void, Signal, Converter · `#ffffff` Clean · `#f7f4ec` Press ·
`#f4efe4` Paper · `#fbfaf6` Journal · `#ffffff` Showcase. Correct, every one.

`mode` still drives the `.only-dark` / `.only-light` logo visibility rules, so set it to match the
ground or the client's logo shows the wrong variant. But it has no effect on colour.

### Eight of the nine have never rendered a live page

Every live QBS page uses Void's `mv-shell.html`. Flagship, Signal, Converter, Clean, Press, Paper,
Journal and Showcase are **sold and unproven** — a client build is that theme's first real test,
which is exactly how defect 1 would reach production. Gate every build with
`node scripts/verify.mjs`.

## Re-skin surface

Not `fields.json`. `theme.colors` is referenced in **zero** files across all nine themes — the five
colour fields are dead. The real surface is the twelve custom properties in the native-direction
block of `css/quantum.css`. See `process/reskin.md`, and run
`python3 scripts/reskin.py inspect --theme "<name>"` to read any theme's live values.

## The 57 shared modules

Every theme draws on the same module library, and **12 of the 16 page templates are a `dnd_area`**
— so delivered sites are genuinely drag-and-drop editable in HubSpot. The four that aren't are
`blog-listing` (a blog template), `password-prompt`, `system-404` and `system-search`: hardcoded
markup, which is correct for system pages.

> **57, not 47.** The live website-services page advertises "47 modules each." Verified against
> `/cms/v3/source-code/published/metadata/{theme}/modules`, Press, Clean and Signal each carry 57.
> The public number undersells the product by ten. Void carries **61** — its four extras are
> `quantum-assistant` (the Ask Quantum widget), `quantum-growthmodel`, `quantum-pricing-matrix` and
> `quantum-process-flow`, which are what render the packages table and the 90-day timeline on the
> live site. Those four are QBS's own; they don't ship to clients. The client reorders sections and edits copy
without touching code. Verified: `Quantum Press/templates/home.html` 

That matters commercially — "editable by your team" is a real deliverable, not a promise. Verified:
`Quantum Press/templates/home.html` is one `dnd_area "main"` holding **7** `dnd_section`s, each with
one named module. (An earlier version said 14; that came from a grep that counted
`{% end_dnd_section %}` too.)

**Persuasion modules** (the sales methodology, encoded):
`pain-bridge` · `is-this-you` · `cost-of-inaction` · `myth-reality` · `two-futures` · `why-now` ·
`before-after` · `comparison` · `feature-matrix`

These map onto the three P's in `process/checklist.md`: `pain-bridge` is Pain, `is-this-you` is
Person, `two-futures` and `why-now` carry Promise. When a hero fails the three-P test, the fix is
usually a missing module, not new copy.

**Proof:** `case-study` · `casestudy-grid` · `casestudy-hero` · `logo-strip` · `reviews` ·
`testimonial-slider` · `stats-band` · `stats-chart` · `metric-cards` · `team`

**Conversion:** `cta-band` · `cta-inline` · `sticky-cta` · `leadgen` · `multistep-form` ·
`gated-download` · `meetings` · `contact` · `pricing` · `pricing-toggle` · `roi-calculator` ·
`roi-estimator`

**Structure & content:** `hero` · `columns` · `feature-split` · `services-list` · `services-wheel` ·
`framework-rail` · `roadmap` · `timeline` · `chapter` · `tabs` · `rotator` · `toc` · `faq` ·
`integrations` · `pullquote` · `rich-text` · `image` · `video` · `spacer` · `announcement` ·
`mega-menu` · `blog-header` · `blog-listing` · `related-posts` · `resource-card` · `event-hero`

`quantum-roadmap` is the 90-day proven process — a gantt with accordions and a timeline axis.

## Other themes on the portal

Not part of the nine; don't offer them as client options.

| Path | What it is |
|---|---|
| `Quantum_Business_Theme_CTA9` (68) | Legacy QBS theme |
| `Quantum 2026` (28) · `Quantum Custom 2026` (8) | Earlier iterations |
| `atlas-theme child 2024` (4) | Atlas child — see `qbs-atlas-page-builder` |
| `ProPrint - Blogs Theme` (50) · `ProX child` (6) · `session copy` (40) | Third-party / inherited |
| `@marketplace` (455) | HubSpot marketplace themes |
| `Quantum_Quote_CTA9` (12) | QuoteCommand |
