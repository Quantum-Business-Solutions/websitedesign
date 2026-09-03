# The nine Quantum themes

Hand-built HubSpot themes on portal `20682069`. Each is 21 templates — a complete site kit, not a
page: home, interior, pricing, case study, blog listing and post, contact, event, playbook,
thank-you, 404, search, plus header/footer partials, CSS, JS and modules.

**These are the product.** Client website options are three of these nine, re-skinned to the
client's brand — not designs generated from scratch. That's what makes the output reliably good:
you start from something already built well instead of from a model's average.

## The nine

Each theme's identity is its **ground** (light or dark) and its **heading typeface**. Body type and
layout system are shared, so the typeface is doing the character work — which means you pick a theme
partly *for* its typeface.

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

## Known bug in the theme set

**All nine default to `appearance.mode: dark`** — including the five described as light themes.
Verified across every `fields.json`. So Clean, Press, Paper, Journal and Showcase render dark out of
the box, contradicting their own descriptions.

Two consequences:
- **Always set `mode` explicitly during re-skin.** Never rely on the default.
- The defaults are worth fixing at source so the theme set is honest about itself. Until then this
  is a trap for anyone using a light theme without re-skinning.

## Re-skin surface

Identical on all nine, which is what makes this automatable — see `process/reskin.md`:

| Field | Default (QBS's own) | Role |
|---|---|---|
| `appearance.mode` | `dark` | Ground. **Always set explicitly.** |
| `colors.gold` | `#c4a44a` | Primary accent — links, primary CTA |
| `colors.gold_bright` | `#d4ba6a` | Accent hover/active |
| `colors.void` | `#080b12` | Darkest ground |
| `colors.navy` | `#101725` | Mid surface, cards |
| `colors.paper` | `#fbfaf6` | Lightest ground |

Typefaces are **not** in the field surface — they're baked into each theme. To change the typeface
you change theme, which is the point: nine themes is the type system.

## The 57 shared modules

Every theme draws on the same module library, and **every page is a `dnd_area`** — so delivered
sites are genuinely drag-and-drop editable in HubSpot.

> **57, not 47.** The live website-services page advertises "47 modules each." Verified against
> `/cms/v3/source-code/published/metadata/{theme}/modules`, Press, Clean and Signal each carry 57.
> The public number undersells the product by ten. Void carries **61** — its four extras are
> `quantum-assistant` (the Ask Quantum widget), `quantum-growthmodel`, `quantum-pricing-matrix` and
> `quantum-process-flow`, which are what render the packages table and the 90-day timeline on the
> live site. Those four are QBS's own; they don't ship to clients. The client reorders sections and edits copy
without touching code. Verified: `Quantum Press/templates/home.html` is one `dnd_area "main"` with
14 `dnd_section`s, each holding one named module.

That matters commercially — "editable by your team" is a real deliverable, not a promise.

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
