# The Website Design Process

This is not a new process. QBS already **sells** one, publicly, at
[thequantumleap.business/website-services](https://www.thequantumleap.business/website-services) —
six phases, 90 days, three fixed-price packages. That page is the contract. Everything in this repo
exists to execute it faster and better, not to replace it.

So this file does two things: records the sold process verbatim, and maps each phase to the tooling
that actually does the work.

---

## The 90 days, as sold

Rendered on the live site by the `quantum-process-flow` module (Quantum Void). Phases overlap
deliberately — content writing starts before wireframes are signed off, design starts before content
is finished.

| # | Phase | Days | What the client is buying |
|---|---|---|---|
| 01 | **Information Gathering** | 1–10 | Understanding the business, audience and goals |
| 02 | **Planning** | 10–20 | Site structure, technology, timeline |
| 03 | **Wireframing** | 20–35 | Layout and functionality agreed before design |
| 04 | **Content Writing** | 30–50 | SEO-friendly copy in the brand voice |
| 05 | **Design & Build** | 45–75 | Conversion-focused design, refined on feedback |
| 06 | **Test, Review & Launch** | 75–90 | Cross-device testing, review, monitored launch |

**Then it doesn't stop.** The site is sold as growth-driven design: launch through the 90 days, then
optimise monthly on real behaviour, heatmaps and conversion data — instead of rebuilding every two
or three years. Monthly reviews, A/B tests, content updates, CRO, analytics reporting.

SEO is in from phase one, not bolted on: technical SEO, on-page, schema, Core Web Vitals, pillar
pages.

### Patrick's internal sequence

The same process stated operationally rather than commercially: map outcomes → plan content → align
to SEO strategy → wireframe → design layout and branding → create mockups → build templates → test →
launch. Same shape, one extra beat worth keeping — **map outcomes before content.** The commercial
phase 01 says "understand the business"; the internal version says decide what the site is *for*
first. That's the step that becomes the brief.

---

## Where the tooling lands

The repo's job is to collapse phases 02–05 from weeks of hand work into a day of reviewed output.

| Phase | Tooling | Output |
|---|---|---|
| 01 Information Gathering | `/website <company>` step 1 — `list_brands`, `firecrawl_scrape` with `formats:["branding"]` on their site and two or three competitors, then the four-question interview | Measured tokens, category read |
| 01 Information Gathering | **`process/seo-baseline.md` — the four Semrush pulls.** Traffic baseline, which pages actually earn it, striking-distance keywords, site audit | The number we're measured against, and the evidence that sells the tier |
| 01 → 02 | `brands/<slug>.md` from `brands/_template.md` | **The brief.** Client-stated constraints, which outrank house defaults |
| 02 Planning | `themes/catalogue.md` selection rules — three of nine, safe / stretch / wildcard, ground filtered by the brief | Three named directions |
| 02 Planning | **URL migration map.** Every page earning traffic today gets a 301 to its new home. A redesign that changes blog URLs without 301s destroys the only traffic the client has | Old → new URL map |
| 03 Wireframing | The 57 shared modules *are* the wireframe vocabulary. Pick section order from the module inventory rather than drawing boxes | Section order per page |
| 04 Content Writing | The three P's test in `process/checklist.md`. When a hero fails it, the fix is usually a missing persuasion module — `pain-bridge`, `is-this-you`, `cost-of-inaction` — not new adjectives | Copy that passes the gate |
| 05 Design & Build | `process/reskin.md` — clone the theme, six values. Higgsfield for hero imagery per `design/prompts.md`. `/impeccable polish`, `design-taste-frontend` | Re-skinned clone in HubSpot |
| 06 Test, Review & Launch | `process/checklist.md` end to end, `/impeccable audit`, mobile-width screenshot loop, `process/launch-standards.md` launch gate | Signed-off build |
| Post-launch | `process/seo-baseline.md` monthly re-pull — trend, next striking-distance win, audit regressions. This is what makes growth-driven design falsifiable | Monthly report against the baseline |
| Post-launch | Growth-driven design. New reference → `design/inbox.md`. Rule that generalises → `design/guardrails.md` | A faster next build |

Phase 03 is the one that changed most. Wireframing used to mean drawing layouts; with a fixed
57-module library it means **choosing from an inventory**, which is both faster and why the delivered
site is genuinely editable — every page is a `dnd_area`, so the client reorders the sections they
signed off on.

---

## The SOW front end

The three published packages are the SOW. Don't scope from scratch — pick the tier, then vary only
page count and copy depth. Rendered live by `quantum-pricing-matrix`.

| | **Launch** | **Growth** *(most popular)* | **Transform** |
|---|---|---|---|
| Price | **$4,950** one-time | **$9,950** one-time | **$14,950** one-time |
| Quantum theme | One theme, as-is | Tailored to your brand | Full design system |
| Pages | up to 8 | up to 20 | up to 50 |
| Copywriting | Polish pass | Conversion copywriting | Page-by-page rewrite |
| Mobile and speed pass | ✓ | ✓ | ✓ |
| Timeline | ~90 days | ~90 days | ~90 days |
| Schema and AEO stack | — | ✓ | ✓ |
| Blog setup | — | ✓ | ✓ |
| Priority support | — | ✓ | ✓ |
| Conversion architecture, offers, CTAs | — | — | ✓ |
| Analytics and grader baseline | — | — | ✓ |
| Post-launch optimisation window | — | — | ✓ |

Anything outside the tiers is a scoped custom build — Revolution's $50k full engagement is that,
and its $7.5–10k HubSpot Starter option is a Launch/Growth hybrid.

**What the tiers actually price is re-skin depth**, and that maps exactly onto `process/reskin.md`:

- **Launch** — a theme as-is. No clone needed; use the theme, set `appearance.mode` explicitly.
- **Growth** — clone and re-skin. The six values. This is the standard operation.
- **Transform** — clone, re-skin, and extend. If the extension is structural, fix the theme **at
  source** so all nine benefit. Resist per-client structural forks.

Two commercial lines worth repeating in every pitch, because both are true and neither is common:
**"nine themes, one design system, all yours — no licences, no lock-in"** and **"editable by your
team"** — the latter is a verified fact about `dnd_area`, not a promise.

---

## Upstream: the Quantum Brand Breakthrough

$7,500, six phases, sold separately. If a client has no brand to build against, this is the
engagement that produces one — and it is the *right* answer when the brief has nothing to design
against.

Discover → Position → Identity → **Systemize** → Launch → Govern

Phase 4 Systemize is where it meets this repo: the brand becomes HubSpot themes, email and proposal
templates. Phase 6 Govern is quarterly review and AI-visibility monitoring. That's the differentiator
from a pure branding agency — the deliverable is a live system, not a PDF.

---

## Two things the live page has wrong

Both are cheap to fix and both are client-facing.

1. **It says "47 modules each." The real number is 57.** Verified against
   `/cms/v3/source-code/published/metadata/{theme}/modules`: Press, Clean and Signal each have 57.
   Void has 61 — its four extras are `quantum-assistant` (the Ask Quantum widget),
   `quantum-growthmodel`, `quantum-pricing-matrix` and `quantum-process-flow`. The public number
   undersells the product by ten modules.
2. **The theme copy positions Void as "our flagship look"** while a separate theme is *named*
   Flagship. Both descriptions are accurate — Void is the live site, Flagship is the Fraunces
   theme — but the word does double duty and reads as a contradiction in a list of nine.

The nine themes' grounds and typefaces on the live page match `themes/catalogue.md` exactly. That
part is sound.
