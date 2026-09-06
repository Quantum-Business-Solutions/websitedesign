# The delivery chain: catalogue → proposal → plan → page → asset → ticket

How a website engagement is tracked in ClientCommand, standardised so every build looks the same and
the numbers mean something.

> **Status: specified, not wired.** The ClientCommand MCP was disconnected when this was written, so
> every tool name and field below is **from the tool listing, not verified against the live schema.**
> Anything marked ⚠️ must be confirmed before building. The *design* doesn't depend on that — the
> chain and the data model are the decisions; the plumbing is mechanical.

---

## The one idea that makes this work

**The page is the tracked unit, not the phase.**

A 20-page Growth build is not six phases. It's **20 pages × the same seven steps each**, plus a
launch. That single reframe is what makes everything else possible:

- **Hours become predictable.** "How long does a website take" is unanswerable. "How long does a
  page take" is a number you can measure and improve.
- **Scope drift becomes visible.** Page 21 on a 20-page tier is a change order, automatically, not
  an argument in week eight.
- **Progress becomes honest.** "Phase 04 in progress" tells you nothing. "14 of 20 pages have copy,
  3 are blocked on client photography" tells you everything.
- **Blockers surface early.** Assets are the number one schedule killer and they're all
  client-dependent. Tracked per page with an owner, they show up in week two instead of week nine.

Phases still exist — they're what we sold, and they own the dates. But they're a *reporting view*
over page states, not the thing being tracked.

---

## 1 · Service catalogue — the source of truth for what we sell

⚠️ `list_service_catalog`, `upsert_service_catalog_item`

Three items, matching what's published: **Launch $4,950 · Growth $9,950 · Transform $14,950**, plus
**Quantum Brand Breakthrough $7,500** and a custom line.

Each item carries its scope as *data*, not prose — because every downstream number depends on it:

| Field | Launch | Growth | Transform |
|---|---|---|---|
| Page allowance | 8 | 20 | 50 |
| Re-skin depth | clone, theme's own colours | clone + re-skin | clone + re-skin + extend at source |
| Copy depth | polish pass | conversion copywriting | page-by-page rewrite |
| Blog setup | no | yes | yes |
| Schema stack | no | yes ⚠️ **currently blocked** | yes ⚠️ |
| Post-launch window | no | no | yes |

**A page-counting rule has to live here**, because it's the most common scope fight: *one template
plus N data-driven instances counts as one page.* Twelve location pages off one template is one
page of build and twelve of content. Write it down before it's contested.

**And the exclusions belong here too**, as explicit non-scope: multi-location location pages, CMS
migration, and the schema stack until the theme fix lands. An exclusion in the catalogue becomes an
exclusion in every proposal automatically.

## 2 · Proposal — assembled, never written from scratch

⚠️ `create_web_template`, `list_web_templates`, `clone_web_template_to_proposal`,
`create_proposal_from_template`, `set_web_proposal_selected_services`, `publish_web_proposal`,
`get_web_proposal_share_link`, `send_proposal_for_signature`

**One web template per tier.** A proposal is the template plus selected catalogue items plus four
client-specific things — and those four are what make it land:

1. **The SEO baseline**, from `process/seo-baseline.md`. Their real traffic number, their top pages,
   and the striking-distance keywords. This is the difference between "we'll improve your SEO" and
   "you get 146 visits a month and one page is stuck at position 11 for keywords worth 1,700
   searches."
2. **The three directions** — the `scripts/mockup.py` artifact URL, embedded. They see the design
   before they sign.
3. **The promise**, in their own words, from the brief.
4. **The exclusions**, named plainly. Nobody has ever been annoyed by an exclusion they read before
   signing.

Proposals get **versioned and tracked**, not emailed — ⚠️ `save_web_proposal_version`,
`list_web_proposal_activity`, `get_proposal_analytics`. Knowing they opened it three times and
lingered on pricing is worth more than a follow-up guess.

## 3 · Won → plan, from a template

⚠️ `list_plan_templates`, `clone_plan_template_to_portal`, `create_plan`, `create_phase`,
`create_task`, `add_task_from_library`, `get_plan_hours`, `get_plan_summary`, `get_scope_drift`

**One plan template per tier**, whose phases are exactly the six we sold — same names, same day
ranges, so the plan and the proposal cannot drift:

| # | Phase | Days |
|---|---|---|
| 01 | Information Gathering | 1–10 |
| 02 | Planning | 10–20 |
| 03 | Wireframing | 20–35 |
| 04 | Content Writing | 30–50 |
| 05 | Design & Build | 45–75 |
| 06 | Test, Review & Launch | 75–90 |

Tasks come from the **task library** ⚠️ (`list_library_tasks`, `add_task_from_library`), so they're
identical on every build. That's the whole point of a standard: the tenth build runs the same as the
first, and the estimates get more accurate rather than starting over.

**Every task in the library should map to a line in `process/OPERATOR.md`.** If a task exists with no
checklist line behind it, one of the two is wrong.

Anything learned on a build that should apply to the next one → ⚠️ `promote_task_to_library`. That's
how the template improves instead of the knowledge staying in one person's head.

## 4 · Page tracking — the part you specifically asked about

This is the layer that doesn't exist yet in any form, and it's the highest-value piece.

⚠️ Needs a decision on where it lives: ClientCommand's own page/section tools
(`create_page_from_template`, `list_pages`, `get_page_state`, `set_page_lifecycle`,
`list_pages_needing_review`, `create_section`, `list_sections`) appear to model **client-portal**
pages rather than website pages. If they can carry website pages, use them. If not, this is a
`page_type` on plan tasks, or a small table. **Confirm before building** — but the model below holds
either way.

### One record per website page

| Field | Values | Why |
|---|---|---|
| **Template** | one of the 16 (`home`, `interior`, `pricing`, `case-study`, `blog-post`, `contact`, `landing`, `event`, `playbook`, `thank-you`, …) | Decides the section vocabulary and whether it's a `dnd_area` |
| **Counts against allowance** | yes / no (template instance) | The scope-drift trigger |
| **Section order** | list of module names from the 57 | **This is the wireframe.** Not a drawing |
| **Step** | the seven below | The actual status |
| **Owner** | per step | "In progress" with no name is not a status |
| **Assets required** | list, each with owner + state | The real blocker |
| **Target keyword** | from the Semrush baseline | Ties the page to the number it has to move |
| **Old URL → 301** | url pair | Traffic insurance |
| **Gate result** | `verify.mjs` pass / fail + date | Objective done |

### The seven steps

Every page moves through the same states. This *is* the process, per page:

1. **Briefed** — purpose, audience, target keyword agreed
2. **Sectioned** — module order chosen from the inventory *(this is Phase 03 wireframing)*
3. **Copy drafted** — passes the three P's
4. **Copy approved** — client signed off. **The most common stall point, so it's its own state**
5. **Built** — sections in HubSpot, real content, no placeholders
6. **Assets in** — hero, photography, gated asset all present
7. **Gated** — `verify.mjs` passes, screenshots reviewed at phone width

A page isn't done until 7. **"Built" is not "done"** — that conflation is how sites ship with
placeholder text and orphaned card rows.

### Why copy approval is its own state

Phase 04 is days 30–50, the longest phase, and it has no method — it's the biggest schedule risk in
the whole engagement. Splitting "drafted" from "approved" makes client-side delay *visible as
client-side delay* rather than as our slippage. That's worth having on record when a launch date
moves.

## 5 · Assets — tracked per page, with an owner

⚠️ `upload_portal_file`, `attach_portal_file`, `attach_portal_resource`, `list_portal_files`

Every asset row: what it is, which page needs it, **who owes it**, due date, state.

Asset classes and where they come from:

| Class | Source | Note |
|---|---|---|
| Logo (light + dark variants) | client | Both, or `.only-dark`/`.only-light` shows the wrong one |
| Photography | client, or scoped as stock | One set per location on a multi-site client. Unscoped, this is a month |
| Hero art | Higgsfield, `design/prompts.md` | **Chosen direction only.** Generate blank surfaces so labels stay real HTML |
| Gated asset | client, or scoped as a deliverable | **If they don't have one, that's a scope item** — surface it in Phase 01, not week ten |
| Case study content | client | Needs their customer's approval, which takes longer than anyone plans |

**Client-owed assets are the number one cause of blown dates**, and they're invisible until someone
asks. A weekly view of "assets overdue, by client" is the single most useful report in this system.

## 6 · Hours and billing

⚠️ `push_plan_to_hubspot_tickets`, `push_task_to_hubspot_ticket`, `get_plan_hours`,
`materialize_tickets_into_plan`

Plan tasks push to HubSpot tickets so hours land where billing already looks — and the existing
`qbs-hubspot-ticketing` conventions apply. `get_plan_hours` against the tier's expected hours is the
margin number: on fixed price, hours per build is the *only* thing that decides whether the work was
profitable.

## 7 · The client-facing portal

⚠️ `create_portal`, `setup_new_portal`, `get_portal`, `get_portal_readiness`, `add_portal_note`

Give the client a portal showing: the three directions, their baseline number, page-by-page status,
and — most usefully — **what's blocked on them**. Two effects: it stops status-chasing emails, and it
makes client-side delay self-evident without anyone having to say so.

## 8 · Close the loop

- **Baseline → delta.** The pre-launch numbers are what the optimisation window is measured against.
- **Case study from the delta.** ⚠️ `generate_client_review`, `upsert_review_quote`, and the
  `casestudy-*` modules already exist. Every finished build has a before and an after — generating
  the case study from measured numbers turns delivery into pipeline automatically.
- **Retainer.** The plan template should *end* with the retainer conversation as a task, on a date.
  Otherwise the one-time fee is the whole relationship, which is the strategic problem named in
  `process/strategy.md`.
- **Promote what you learned** to the task library and to `design/guardrails.md`.

---

## The conveyor belt, and what actually limits it

A conveyor belt is the right model, and it's stricter than "a repeatable process." A line means:
**standard units, fixed stations, work moves while people stay put, and you measure throughput per
station so the bottleneck is a fact rather than an opinion.**

The page-as-unit model above *is* a line. Seven stations, one unit type, no unit moves backward.

But before optimising it, here's the arithmetic — and it says something surprising.

### A Growth build is about 58 hours of work

At 20 pages, with the tooling that now exists:

| Station | min/page | × 20 pages |
|---|---|---|
| Briefed | 10 | 3.3h |
| Sectioned | 15 | 5.0h |
| Copy drafted | 45 | 15.0h |
| Copy approved *(our effort)* | 5 | 1.7h |
| Built | 30 | 10.0h |
| Assets in | 15 | 5.0h |
| Gated | 10 | 3.3h |
| | **130** | **43.3h** |

Plus once-per-build: brief and the four Semrush pulls 6h · mockups 0.5h *(scripted)* · clone and
re-skin 0.3h *(scripted)* · de-QBS the header and footer 3h · URL map and 301s 2h · launch and
baseline 3h — **14.8h**.

**Total ≈ 58 hours ≈ 8 working days. Sold across 90 calendar days.**

### So the belt is not the constraint. Waiting is.

Work is **13%** of a 60-working-day window. **87% of the 90 days is latency** — waiting on copy
approval, waiting on photography, waiting on a logo file.

Three consequences, and they change what's worth building:

1. **Automating our 58 hours down to 45 changes nothing about the 90 days.** The bottleneck is
   outside the factory. This is the single most important thing to understand before spending
   another week on tooling.
2. **The scale unlock is concurrency, not speed.** On work alone, one person could carry roughly
   **16 concurrent Launch builds, 8 Growth, or 3 Transform.** Whether that actually happens is a
   *tracking* problem — you cannot hold eight builds in your head, which is precisely why page-level
   tracking is worth building.
3. **Attacking wait states beats attacking work.** Front-load every client-owed ask into week one.
   Batch copy approvals into two scheduled reviews instead of trickling pages. Give every approval a
   **default that ships if they don't respond** — that one policy converts a wait into a decision.

### Run the stations across clients, not the clients across stations

The operational change that makes it a belt: **one person does "sectioned" for four clients in a
morning**, rather than one person owning one client end to end. Same station, batched. Context
switching within a station is nearly free; between stations it isn't.

That's only possible if page state lives somewhere everyone can see. Which is the whole argument
for section 4.

### Measure stations, not phases

Phases own the dates. Stations own the flow. Four numbers, weekly:

| Metric | What it tells you |
|---|---|
| **WIP per station**, all clients | Where the pile-up is. Pages sitting at *copy approved* means client latency; at *built* means us |
| **Median hours per station-pass** | Whether the estimates above are real. Fix them with data after ten builds |
| **Critic score per page** | The quality trendline. BrandCommand already scores campaign assets 0-100 in `agent_runs`; website pages should use the same scale, and nothing ships under 80 |
| **Age of oldest unit per station** | A page stuck 3 weeks at one station is invisible in a phase view and obvious here |
| **Client-owed assets overdue** | The most actionable report in the system |

A **WIP limit per station** is what stops the line becoming twelve half-finished builds. Nothing
enters *built* until something leaves it.

### The pricing finding this exposes

Effective rate by tier, using the model above:

| Tier | Pages | Hours | $/hr | Concurrent per person |
|---|---|---|---|---|
| **Launch** $4,950 | 8 | 32 | **$155** | 14 |
| **Growth** $9,950 | 20 | 58 | **$172** | 8 |
| **Transform** $14,950 | 50 | 123 | **$121** | 4 |

**Transform is still the weakest of the three per hour** — and Phase 4 hits it hardest. Fifty pages of page-by-page rewrite is
enormous, and it earns 40% less per hour than Launch while occupying five times the capacity. Two
honest options: price it around **$22–25k**, or cut the page allowance to 30. Right now it is
selling the least profitable work hardest.

And for scale — a retainer at **$2,500/month for 10 hours is $250/hour**, 45% better than Growth and
**2× Transform**, at **$30,000/year per client** against a one-time $9,950. That is the number
behind `process/strategy.md`: the belt should end at a retainer, not at a launch.

### Price the actual cost driver: Phase 4

The tiers price **page count**. The cost driver is **Phase 4** — custom modules, sections and
templates — which is priced at nothing. Revolution needed 29 modules, 7 sections and 49 templates:
plausibly a second build's worth of work inside one engagement, and no tier saw it.

**The rule for when it applies:** map every section in step 16 to a module name. Any section with no
module in the 57 (plus the vertical kit) is Phase 4 work.

**The line item**, provisional until actuals exist:

| Unit | Estimate | Note |
|---|---|---|
| Custom module | 90 min | fields.json + module.html + module.css, `quantum-faq` pattern |
| Drag-and-drop section | 60 min | a pre-composed group of modules |
| Custom page template | 45 min | falls to ~10 min if `layoutSections` works — **settle that** |
| Header/footer as field-driven modules | 3 h | once per theme at source, then free |

Two model variants, because they are different businesses:

| | First build in a vertical | Subsequent build |
|---|---|---|
| Phase 4 | Full — the vertical kit doesn't exist yet | Near zero — port from the kit |
| Price it as | A custom line, **or** a product investment QBS eats knowingly | The belt |
| Revolution was | This | — |
| Kelly would be | Subsequent, if Revolution's 29 are ported first | — |

**The quote rule:** if the section list needs anything the kit doesn't have, the quote carries a
Phase 4 line or it is provisional. Say which.

> These are estimates, not measurements. **Track actuals from the first build** and replace them —
> the model is only useful once it's calibrated, and everything above changes if copy really takes
> 90 minutes a page rather than 45.

---

## Build order

Each step is useful on its own, so none of it has to wait for the rest:

1. **Service catalogue with the scope-as-data table**, including the page-counting rule and the
   exclusions. Everything else reads from it, and it's an afternoon.
2. **Three proposal templates.** Immediate leverage: proposals stop being written.
3. **Three plan templates** with the six phases and library tasks. Now every build runs the same.
4. **Page tracking.** The biggest piece and the biggest payoff. Needs the ⚠️ schema decision first.
5. **Asset tracking**, hung off pages.
6. **Ticket push and the hours-vs-tier report.** This is where you find out if the tiers are priced
   right — and after ten builds, whether Launch is profitable at all.

## What to verify when ClientCommand reconnects

- Do the page/section tools model website pages, or only client-portal pages?
- Does the service catalogue hold arbitrary scope fields, or a fixed shape?
- Can plan templates carry phases with day offsets, so the six sold phases survive cloning?
- Does the task library support per-task expected hours? (Needed for the margin number.)
- Are proposal analytics per-recipient or aggregate?
- Is there a first-class asset object, or are assets just portal files with naming conventions?

Answer those six and this becomes an implementation rather than a design.
