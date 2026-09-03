# websitedesign

How QBS builds websites that don't look AI-generated — the methodology, the accumulated taste, and
the guardrails. Give it a company name, get three grounded directions, the same reliable way each
time.

**This repo is not a builder.** It's the layer that decides what good looks like. The building
happens in BrandCommand and HubSpot.

## Start here

```
/website <company name or URL>
```

Gathers evidence, asks **four** questions, then builds in one pass. Two lanes:

- **Lane A — full site.** Three of the nine Quantum themes, re-skinned to the client's brand,
  recorded in BrandCommand, shipped to HubSpot.
- **Lane B — signature page.** A scroll-driven experience via the `scroll-craft` skill.

Full steps in `.claude/commands/website.md`. Reasoning in `process/build-sequence.md`.

**Scoping comes first.** QBS sells a six-phase, 90-day process at three fixed prices — Launch
$4,950 / Growth $9,950 / Transform $14,950 — published at
[thequantumleap.business/website-services](https://www.thequantumleap.business/website-services).
Pick the tier, then build. `process/website-design-process.md` records it and maps every phase to
the tooling that does the work. Options get presented as **one main page, then three** —
`process/pitch-presentation.md`.

## The nine themes are the product

`themes/catalogue.md` — nine hand-built HubSpot themes, 21 templates each, identified by ground
(light/dark) and heading typeface. Client options are **three of these nine re-skinned**, not designs
generated from scratch. That's what makes the output reliably good: you start from something already
built well rather than from a model's average.

Re-skinning is six values per theme — see `process/reskin.md`.

## Layout

| Path | What it is |
|---|---|
| `process/website-design-process.md` | **The process QBS sells** — six phases, 90 days, three packages. Start here when scoping. |
| `themes/catalogue.md` | **The nine themes**, what each is for, and the selection rules. |
| `process/pitch-presentation.md` | How options get shown: one main page, then three. |
| `process/reskin.md` | How a client's brand gets onto a theme. Six values. |
| `process/checklist.md` | Pre-ship checklist. Nothing reaches a client without it. |
| `process/build-sequence.md` | The methodology, in order, with the reasoning. Read once. |
| `design/guardrails.md` | Always/never. **Read before generating any design work.** |
| `design/references.md` | Live-site references, why each is here. |
| `design/tokens/*.json` | Values **measured** off live pages. Only measured, never hand-written. |
| `design/prompts.md` | Generation prompts that worked, with model and settings. |
| `design/inbox.md` | Drop URLs here, then run `/design-ingest`. |
| `design/SCHEMA.md` | The ingest contract — slug rule, file shapes, failure handling. |
| `brands/<client>.md` | Per-client brief. Client-stated constraints live here and **outrank house defaults**. |

## The two habits that do the work

**1. Build wide.** Three genuinely distinct directions, never one design with tweaks. This is
already the house pattern — Revolution's Signature / Ink / Press, each with a one-line rationale and
a full token set. Comparison is what makes the client's choice real, and it's what stops the model
settling into its defaults.

**2. Write the brief first.** Most slop comes from designing with nothing to design *against*, so
the model reaches for the average. A brief also catches contradictions early: Revolution's brief
surfaced that Direction 2 "Ink" is near-black, weeks after Tom explicitly asked to avoid heavy black
backgrounds. Nothing was checking one against the other until it was written down.

## Where this sits alongside the rest of the stack

Keeping the boundaries straight is what stops this becoming another silo:

| Tool | Its job | System of record for |
|---|---|---|
| **This repo** | Methodology, taste, guardrails | How we work, what good looks like |
| **BrandCommand** | Production builder, pushes to HubSpot | `brand_profiles`, `website_projects`, `builder_pages` |
| **Claude Design** | Brand-specific design systems from assets, Figma, GitHub | Component systems |
| **`qbs-atlas-page-builder`** | HubSpot atlas-theme mechanics | Live pages |
| **Impeccable** (plugin) | Craft and anti-slop critique — `/impeccable critique`, `audit` | — |
| **`design-taste-frontend`** | Reads the brief, steers off LLM defaults | — |
| **`scroll-craft`** | Scroll-driven signature pages; interviews, builds, screenshots its own scroll | Lane B output |
| **Higgsfield** | Hero imagery and video | Generated assets |

Client work lives in **BrandCommand**, not here. This repo holds the method; that holds the
projects.

## Known gaps

Worth being explicit about, because both are places quality currently leaks:

1. **The nine themes default to the wrong mode.** All of them ship `appearance.mode: dark`,
   including the five light ones — so Clean, Press, Paper, Journal and Showcase render dark out of
   the box, contradicting their own descriptions. Worth fixing at source; until then, always set
   `mode` explicitly.
2. **Figma is not an input yet.** Clients hand over Figma files (Revolution did), and Figma's API
   exposes real fills, type styles and variables — more precise than scraping a rendered page.
   Adding the Figma MCP would make client-supplied designs a first-class source.
3. **No automated clone-and-reskin.** `process/reskin.md` documents the operation but it's still run
   by hand. Scripting it is the next real efficiency gain — and it's what Phase 05 of the sold
   process is currently spending days on.
4. **The live website-services page advertises "47 modules each." It's 57.** Verified against the
   source-code metadata API. Client-facing, undersells the product, cheap to fix.

## Setup

Skills in `.claude/skills/` load automatically. Impeccable is a user-scope plugin, installed once
and shared across projects:

```bash
claude plugin marketplace add pbakaus/impeccable
claude plugin install impeccable@impeccable
claude plugin update impeccable        # currently v4.1.3
```

`scroll-craft` is a third-party skill, pinned in `skills-lock.json` rather than vendored. Reinstall
it on a fresh clone:

```bash
npx skills add https://github.com/nateherkai/scroll-craft
```
