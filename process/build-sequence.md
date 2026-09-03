# Build sequence

The repeatable path from "client wants a website" to "shipped and it doesn't look AI-generated."

Follow it in order. Most slop comes from skipping step 1 (no brief, so the model defaults) or step 5
(nobody checked before it shipped).

**This file is rationale, and it is authoritative over nothing.** Where it disagrees with another
document, the other document wins. The authority order is:

1. **`process/website-design-process.md`** — commercials, phases, dates, tiers
2. **`.claude/commands/website.md`** — the operational steps, and what runs in what order
3. **`process/checklist.md`** + `launch-standards.md` + `structured-data.md` — the gates
4. **this file** — why the shape is what it is

Read it once for the reasoning, then work from the three above.

---

## 1. Write the brand brief — before any design

`brands/<client>.md`, from the template. Sources, in descending order of authority:

1. **What the client actually said.** Direct constraints beat inference. Revolution's *"lighter
   background, orange/white/gray, no heavy black, straightforward not whimsical font, tiled
   layout"* is worth more than any amount of taste library.
2. **Their existing brand assets** — logo, palette, type, photography. If a Figma file exists, it's
   the most precise source available: real fills, type styles, spacing, variables.
3. **Their current site**, ingested via `/design-ingest` for measured tokens.
4. **Their competitors**, same way, to know what the category looks like and what to avoid.

No brief, no build. This is the step that prevents the model reaching for its defaults.

## 2. Ground in the library

- Read `design/guardrails.md`. Hard constraints, not suggestions.
- Read `design/references.md` and pull the token files for anything matching the page type or
  register. Measured values port straight into a theme; prose is judgement.
- Where the brief and the library conflict, **the brief wins.** A house guardrail is a default, not
  an override on a paying client's stated preference.

## 3. Build wide — never one-shot

Produce **three** genuinely distinct directions — safe, stretch, wildcard — not one design plus
tweaks. Three is the house number: two reads as a coin flip, four or more and nobody chooses. The
selection rules that make three genuinely distinct are in `themes/catalogue.md`; the shape they get
presented in is `process/pitch-presentation.md`.

Put them side by side and pick with the client. This is the single highest-leverage habit: choosing
between real options beats iterating blindly toward "make it more premium."

## 4. Refine the chosen direction

Now go deep on one. Three variants of the body/layout, pick, then tune type, colour, spacing.
Generate hero imagery at this stage, not before — see `design/prompts.md`.

## 5. The anti-slop gate — required before ship

Run **all three**, and fix what they surface:

- `node scripts/verify.mjs <url> --expect-org "<Client>"` — the automated gate: a11y, Core Web
  Vitals, schema entity, `og:image`, lazy-loading, placeholder text, conversion paths, broken links
- `/impeccable critique` — UX and hierarchy review
- `/impeccable audit` — accessibility, responsive, performance
- Re-read `design/guardrails.md` and check the build against it line by line

`process/checklist.md` is the full gate and supersedes this list — it has eight items to these
three, including the structured-data and launch standards that postdate this file.

If the page trips a guardrail, it doesn't ship. This gate is the difference between a house style
and a hope.

## 6. Ship to the platform

QBS sites ship on **HubSpot**, on one of the nine Quantum themes — see `themes/catalogue.md` for the
set and `process/reskin.md` for the clone-and-re-skin operation. For atlas-theme pages specifically,
the `qbs-atlas-page-builder` skill has the `layoutSections` mechanics, `dnd_area` naming and the
PATCH-plus-push-live flow.

There is no hand-translation step. The themes are already HubSpot-native: 57 shared modules, every
page a `dnd_area`. A design doesn't stop at a Tailwind config — it lands as six field values on a
cloned theme.

## 7. Feed what you learned back

- New reference worth keeping → `design/inbox.md`, then `/design-ingest`.
- A rule that generalises past this client → `design/guardrails.md`.
- A prompt that worked → `design/prompts.md`, with model and settings.

A library that only gets read decays. This step is what makes the next build faster than this one.

---

## Where this fits alongside the other tools

Keeping these straight prevents duplicated effort:

| Tool | Its job |
|---|---|
| **This repo** | Taste, guardrails, process. The layer that decides *what good looks like*. |
| **Claude Design** | Brand-specific design systems from descriptions, assets, Figma or GitHub. |
| **BrandCommand** | Production builder — `website_projects`, `builder_pages`, pushes to HubSpot. |
| **`qbs-atlas-page-builder`** | The HubSpot atlas-theme mechanics. |
| **Impeccable / taste-skill** | Craft execution and anti-slop critique. |

This repo is deliberately **not** a builder. It's the spine the builders should be reading from.
