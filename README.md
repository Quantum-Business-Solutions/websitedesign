# websitedesign

How QBS builds websites that don't look AI-generated — the methodology, the accumulated taste, and
the guardrails. Give it a company name, get three grounded directions, the same reliable way each
time.

**This repo is not a builder.** It's the layer that decides what good looks like. The building
happens in BrandCommand and HubSpot.

The methodology here is **agreed and in use.** What's still being built, and in what order, is
`process/roadmap.md`.

## Start here

```
/mockups <company>     three directions as a shareable page. Seconds. No HubSpot writes.
/build <company>       clone, re-skin, client schema, gate. Once, after they choose.
```

Mockups are **not** HubSpot clones — that was the mistake. `scripts/mockup.py` renders the three
directions from the themes' real cached tokens, so the accent and typefaces are exactly what ships, and the
clone happens once at the end. Three options used to be the expensive part of a pitch; now they're
free.

`/website` is the older combined command, kept for the full interview-to-ship path.

**The design system document** is generated, never hand-written, so it cannot drift from what
ships: `python3 scripts/designsystem.py --out /tmp/ds.html`. It sets all nine themes in their real
typefaces at their real colours, and carries the colour roles, the card-grid table and the
accessibility floors.

**Just tell me what to do, in order** → `process/RUNBOOK.md`. Eight production phases and 37 steps from
"we should talk to them" to "launched, on retainer and calibrated" — each tagged AI, QBS, CLIENT or
approval, with the command if there is one and what done looks like.

**Building a client site right now?** `process/OPERATOR.md` is one self-contained page — the build
order, the exact commands, and the five verified traps that have shipped or nearly shipped. Hand it
over instead of pointing anyone at this repo.

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

`themes/catalogue.md` — nine hand-built HubSpot themes, 19 files / 16 page templates each, identified by ground
(light/dark) and heading typeface. Client options are **three of these nine re-skinned**, not designs
generated from scratch. That's what makes the output reliably good: you start from something already
built well rather than from a model's average.

Re-skinning rewrites twelve CSS custom properties in one block — see `process/reskin.md`. (Not
`fields.json`: `theme.colors` is wired to nothing. `process/qa-findings.md` has the evidence.)

## Layout

| Path | What it is |
|---|---|
| `process/website-design-process.md` | **The process QBS sells** — six phases, 90 days, three packages. Start here when scoping. |
| `themes/catalogue.md` | **The nine themes**, what each is for, and the selection rules. |
| `process/pitch-presentation.md` | How options get shown: one main page, then three. |
| `process/reskin.md` | How a client's brand gets onto a theme. Twelve CSS tokens. |
| `process/seo-baseline.md` | **The Semrush method** — four pulls, what the numbers mean, client project IDs. |
| `process/launch-standards.md` | **The traffic-and-leads baseline.** Measured gaps, and the launch gate. |
| `process/structured-data.md` | Schema for SEO/AEO — what ships, what's missing, and a bug in all nine themes. |
| `process/checklist.md` | Pre-ship checklist. Nothing reaches a client without it. |
| `process/build-sequence.md` | The methodology, in order, with the reasoning. Read once. |
| `design/guardrails.md` | Always/never — including the card-grid balance rule. **Read before generating any design work.** |
| `design/references.md` | Live-site references, why each is here. |
| `design/tokens/*.json` | Values **measured** off live pages. Only measured, never hand-written. |
| `design/prompts.md` | Generation prompts that worked, with model and settings. |
| `design/inbox.md` | Drop URLs here, then run `/design-ingest`. |
| `design/SCHEMA.md` | The ingest contract — slug rule, file shapes, failure handling. |
| `process/RUNBOOK.md` | **Eight phases, 37 steps, with an owner on every step.** If you read one file, read this one. |
| `process/repos.md` | **Where client work lives.** Not a branch per client — and when a repo is warranted. |
| `process/SCHEDULE.md` | **The calendar** — week-one contract, phase dependencies, WIP limits. |
| `design/patterns.md` | **Patterns that shipped**, and why each one works. |
| `themes/architecture.md` | **What the nine should become** — proven on the live Revolution build. |
| `verticals/office-technology.md` | **Layer 2** — copier dealers and managed print. Six of ten clients. |
| `process/OPERATOR.md` | **Hand this to whoever is building.** Self-contained checklist + the five traps. |
| `process/outbound-mockups.md` | **Speculative mockups as outbound.** Free to render changes the funnel. |
| `process/agents.md` | **The agent roster** — 22 agents in 8 squads: role, expertise, which step, what gates it. |
| `process/clientcommand.md` | **The delivery chain** — catalogue → proposal → plan → page → asset → ticket. |
| `process/strategy.md` | **Is this the right process to dominate?** An honest answer. |
| `process/qa-findings.md` | **What a four-agent QA pass found**, verified. Read before trusting an older claim. |
| `scripts/designsystem.py` | Generates the **Website Design System** doc from the live tokens. |
| `themes/tokens.json` | The nine themes' real tokens, cached. Mockups need no portal access. |
| `scripts/mockup.py` | Three directions as one HTML file. Enforces the selection rules. |
| `scripts/themetokens.py` | Refresh `themes/tokens.json` from the portal. Read-only. |
| `process/roadmap.md` | **What to build next**, ordered by money per hour of effort. |
| `scripts/reskin.py` | Clone + re-skin + client schema in one pass. Read-only until `--apply`. |
| `scripts/verify.mjs` | The launch gate as a command. Exit 1 means it failed. |
| `brands/_template.md` | The brief template. Every field here is consumed by a later phase. |
| `.claude/commands/` | `/mockups` and `/build` (the entry points), `/design-ingest`, `/website` (legacy). |
| `brands/<client>.md` | Per-client brief. Client-stated constraints live here and **outrank house defaults**. |

## Gorgeous is half the job

A site also has to be **found** and has to **capture**. `process/launch-standards.md` is the
measured baseline — what HubSpot gives us free (canonical, OG, sitemap, robots: don't rebuild
these), what the themes already get right, and the specific gaps that leak traffic and leads. It was
measured against QBS's own flagship page, so the findings are real: fonts loading through a CSS
`@import`, zero lazy-loaded images, no `og:image`, and no on-page conversion path on the page that
sells websites.

`process/structured-data.md` covers schema for SEO and AEO — including the worst bug in the set.

And `process/seo-baseline.md` is the evidence layer. We have Semrush with 13 projects already
configured, so a real traffic baseline is a ten-minute pull per client. Worked through on QBS's own
domain, it found that **blog posts drive 82% of organic traffic while the page that sells websites
earns zero**, and that one article is parked at positions 11-14 across four keywords worth ~1,720
monthly searches. That reframes what a website build is *for* — and it turns "we'll improve your
SEO" into a number the client can hold us to.

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

Worth being explicit about, because every one of these is a place quality currently leaks:

1. **All nine themes ship QBS's `Organization` schema on every page.** Hardcoded in
   `templates/layouts/base.html` — client sites declare themselves to be Quantum Business Solutions
   to every search engine and AI crawler. Re-skinning can't fix it: identity isn't a field. This is
   the most damaging gap on the list. Fix proposed in `process/structured-data.md`; needs approval
   before it touches the portal.
2. **The nine themes default to the wrong mode.** All of them ship `appearance.mode: dark` — but the
   native-direction block in `quantum.css` overrides both modes, so **the light themes do render
   light.** The field is vestigial for colour; it still drives `.only-dark` / `.only-light` logo
   visibility, so set it to match the ground. See `process/qa-findings.md`.
3. **Multi-location clients cannot be served.** No location/address/hours module exists in the 57,
   no `locations.html` template, and no `LocalBusiness` schema anywhere. For a practice group or
   dealer network, local visibility *is* the traffic. Out of tier until a `quantum-location` module
   exists — see `process/structured-data.md`.
4. **No CMS migration procedure.** Clients arrive on WordPress. Nothing covers content inventory,
   asset migration, the URL map, the DNS cutover window, or rollback — and "monitored launch" is a
   sold promise. The URL map is named as a Phase 02 output with no method behind it.
5. **Figma is not an input yet.** Clients hand over Figma files (Revolution did), and Figma's API
   exposes real fills, type styles and variables — more precise than scraping a rendered page.
   Adding the Figma MCP would make client-supplied designs a first-class source.
6. **The live website-services page advertises "47 modules each." It's 57.** Verified against the
   source-code metadata API. Client-facing, undersells the product, cheap to fix.

`process/roadmap.md` orders these and the rest by money per hour of build effort. The short version:
script the clone-and-reskin, make quality a command (`node scripts/verify.mjs`) instead of a discipline, and
productise the post-launch retainer — the first two are margin on fixed-price work, the third is the
annuity.

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
