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
