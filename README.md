# websitedesign

How QBS builds websites that don't look AI-generated — the methodology, the accumulated taste, and
the guardrails. Give it a company name, get three grounded directions, the same reliable way each
time.

**This repo is not a builder.** It's the layer that decides what good looks like. The building
happens in BrandCommand and HubSpot.

## Start here

```
/new-website <company name or URL>
```

Resolves the brand, scrapes the current site and competitors for measured tokens, writes a brief,
produces three genuinely distinct directions, records them in BrandCommand, and shows them side by
side. Full steps in `.claude/commands/new-website.md`; the reasoning behind each in
`process/build-sequence.md`.

## Layout

| Path | What it is |
|---|---|
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
| **Higgsfield** | Hero imagery and video | Generated assets |

Client work lives in **BrandCommand**, not here. This repo holds the method; that holds the
projects.

## Known gaps

Worth being explicit about, because both are places quality currently leaks:

1. **No HubSpot output.** Directions stop at tokens and layout intent; someone still hand-translates
   into atlas modules, and that translation is unreviewed. Closing this is the highest-value next
   piece of work.
2. **Figma is not an input yet.** Clients hand over Figma files (Revolution did), and Figma's API
   exposes real fills, type styles and variables — more precise than scraping a rendered page.
   Adding the Figma MCP would make client-supplied designs a first-class source.

## Setup

Skills in `.claude/skills/` load automatically. Impeccable is a user-scope plugin, installed once
and shared across projects:

```bash
claude plugin marketplace add pbakaus/impeccable
claude plugin install impeccable@impeccable
claude plugin update impeccable        # currently v4.1.3
```
