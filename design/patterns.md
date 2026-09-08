# Patterns

Reusable page patterns, with **why each one works**. A pattern earns a place here only when it has
shipped and the reason it lands can be stated — otherwise it's a layout, and layouts live in the
module library.

Universal unless a pattern says otherwise. The vertical kits (`verticals/`) hold the
category-specific ones.

---

## The proprietary process

**Their process, staged, each stage naming what it produces, closed by the outcomes.**

The strongest section in the Revolution build, and it generalises to **any service business with a
process it can name** — consultancies, agencies, MSPs, accountants, contractors, clinics.

Its four rules, all four load-bearing:

### 1 · Take their process, don't invent one

From the build's own source comment:

> *"Revolution's own seven-step assessment and optimization process, taken from **their Managed
> Print Services deck rather than reinvented** — the six-stage Assess/Analyze/Design wheel is the
> generic industry version every competitor publishes, and **this one is theirs.**"*

Every competitor in a category publishes the same generic wheel. The client's *actual* internal
process is the differentiator, and it is **free** — they already have it, in a deck, and nobody has
ever put it on their website. **Ask for the deck in step 6 of the runbook.** This is the single
highest-return question in the discovery call.

### 2 · Every stage names what it PRODUCES, not what we do

Revolution's seven stages each carry an `out`:

| Stage | Produces |
|---|---|
| Physical Device Audit | Verified fleet inventory |
| Service & Cost Analysis | True cost-per-page model |
| Utilization & Volume Analysis | Utilization analysis |
| Stakeholder Interviews | **Requirements, on the record** |
| Workflow Review | Workflow map |
| Security Assessment | **Device risk register** |
| Recommendations & Implementation | Future-state design, implemented |

"We interview stakeholders" is effort. "**Requirements, on the record**" is an artifact the buyer
receives. That single move converts a process diagram from a description of our labour into a list
of things they get — and it costs one line per stage.

### 3 · Close with outcomes, or the whole thing reads as effort

> *"The six outcomes the deck attaches to the process. They are the answer to 'and then what' —
> **without them the seven steps read as effort rather than as something the organization
> receives.**"*

Complete visibility · data-driven insights · improved efficiency · cost savings · enhanced security ·
better outcomes. The band is not decoration; it is what makes the stages mean something.

### 4 · Make it loop, and it becomes the retainer argument

> *"It also ends where the wheel does: the engagement returns to stage one every quarter, which is
> **the difference between a managed program and a one-off procurement.**"*

A process that loops is a recurring engagement, stated visually. That's the retainer sold in a
diagram — see `process/strategy.md`, where the retainer is the actual business.

### And the layout detail worth stealing

> *"Seven items never divide evenly into a grid, so the seventh was always stranding itself on its
> own row. It is also the one that is **different in kind** — the first six are diagnosis, the
> seventh is the handoff — so it runs full width as the conclusion."*

That is the card-grid orphan rule in `design/guardrails.md`, solved the best of the three available
ways: **the odd card was made meaningful rather than tidied away.** Seven at three columns orphans;
6 + 1-full-width doesn't, *and* it's more truthful about the content. When a grid orphans, first ask
whether the odd item is different in kind. Often it is.

### ⚠️ The HubSpot module dropped the two things that make it work

`process-steps.module` fields: `tone`, `eyebrow`, `heading`, `steps{title, copy}`.

**No `produces` field. No outcomes band.** So porting it as-is ships the diagram and loses the
argument. Before reusing it, add:

- `produces` (text) per step — rule 2
- an `outcomes` group, `title` + `copy`, up to 6 — rule 3
- a `final_is_full_width` boolean — the layout detail above

Until then the richer version only exists in the Next.js preview (`components/Framework.jsx`), which
means the *review* previews are better than the thing that ships. That's backwards, and it's the
kind of drift `themes/architecture.md` warns about.

---

## The three-option pitch

One main page of measured evidence, then three directions. Full pattern in
`process/pitch-presentation.md`. Why it works: a prospect shown one design evaluates *you*; a
prospect shown three evaluates *the designs*, which is a much better question to have answered in
the room.

## The diagnosis opener

Open with what's measurably wrong with their current site — `verify.mjs` plus the four Semrush
pulls. Not an opinion, a measurement. Why it works: it is checkable, which makes everything after
it more credible. See `process/outbound-mockups.md`.

## Two conversion paths per page

A hard offer for the ready buyer, a soft offer for the 95% who aren't. Why it works: without the
soft one, everybody not buying today leaves unidentifiable — and that's most visitors.
`process/launch-standards.md`.

---

## The hotspot walk

**The buyer's own building, drawn once, with a marker on every place the engagement finds money,
risk or time. Tap a marker, read the finding and the figure, follow the link. Flip to After and
watch the things the engagement removes disappear.**

Shipped on Revolution Office (Home, Managed Print Services) on 2026-09-08. Kit, module and example
data in `library/patterns/hotspot-walk/`. It generalises to **any service that walks a site**:
managed print, MSPs, security, facilities, insurance risk surveys, accountants doing a books review.

Kelly Office Solutions' reference had the seed of this: an isometric office with numbered dots, one
per product line. That version says *"we sell things in these rooms."* The rules below turn it into
*"here is where your money hides,"* which is the version that sells.

### 1 · Every marker is a finding, never a product

"Copier room" is a place. "One device doing the work of three" is a finding. The card title is
always the finding; the service is the link at the bottom. A marker without a finding is a catalogue
entry and gets cut.

### 2 · Every card carries a figure from the client's own record

192 → 158 devices. 17× spread between the cheapest and dearest page in the same building. 20+ → 1–2
monthly tickets. 19 → 1 agreements. The figures came from the results ledger and the assessment
workbook, the same sources the rest of the site cites, so the map is proof restated spatially, not a
new claim. No figure, no marker.

### 3 · The illustration carries no words

All copy lives in the HTML cards. Search engines, answer engines and screen readers get seven
findings; the picture is decoration that could be swapped for a photograph tomorrow. Generated
illustrations put text on things unless told not to, so the prompt says it three ways.

### 4 · Before / After is the argument

Two or three small red × markers sit on the devices the design removes. Toggle to After and they
fade. That is the whole 192 → 158 story told on a floor plan in one gesture, and it is the moment
people play with in a demo. Without the toggle the section is a legend; with it, it is a claim.

### 5 · Place it right after the problem is named

On Revolution's Home it follows "why nobody has the number" and precedes the method. The reader has
just been told the cost is invisible; the map shows them where it is. On a service page it goes
straight under the hero.

### Layout detail worth keeping

Map left at 1.55fr, one card right, arrows and a counter that count only the numbered findings (the
× markers are excluded, or "1 / 10" confuses). Hover opens on a fine pointer, tap on touch. On phones
the cards stack under the map and the After view hides the removed-device cards rather than fading
them. Pins pulse on a staggered delay; the active pin goes ink-black so the eye finds it.

### ⚠️ Traps

- Restricted field names: HubSpot refuses a group child named `name`. Use `person_name`, `place`.
- Position by percentage, never pixels; the module sets `left`/`top` inline from the two numbers.
- Do not count on the illustration's own margins for composition. Generated scenes arrive with
  uneven cream space; the card container crops nothing, so position markers on the objects and let
  the margins be.
