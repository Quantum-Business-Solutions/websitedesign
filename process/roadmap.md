# What would make this world class

The process now works. This is what separates *works* from *world class*, ordered by leverage.

The distinction matters: the first three items below are things whose absence will eventually cost
real money or a client. The rest are what compounds.

---

## 1 · Get the nine themes into source control

**Status 2026-09-06: built.** `themes/source/` holds all nine (2,835 files); `reskin.py export` refreshes, `reskin.py drift` exits 1 if the portal moved.

**The biggest structural risk in the whole system, and nothing currently mitigates it.**

The nine themes exist **only** in HubSpot portal `20682069`. This repo holds their derived tokens
and nothing else — no theme HTML, no `quantum.css`. Which means:

- **No diff, no review, no rollback.**
- **No way to detect that someone edited one of the nine in Design Manager** — the repo's single
  loudest "never", one accidental save away from changing every client's site, with no audit trail.
- "Fix the nine at source" is a live edit rather than a reviewable change.

Revolution's client theme is in git. The product line isn't.

**Build:** `reskin.py export --theme <name>` for all nine, committed. Then `reskin.py drift` to diff
live against committed, run weekly. A day's work, and it turns the most dangerous operation in the
system into a pull request.

## 2 · Score every page, not just pass/fail

**Status 2026-09-06: built.** `verify.mjs` prints `SCORE n/100`, appends `verify-out/scores.jsonl`, exits 1 under 80.

`verify.mjs` answers *did it pass*. It cannot answer *is it getting better*.

BrandCommand already solved this for campaign assets — `agent_runs.critic_score`, 0–100, per
output. Adopt the same scale for website pages and you get, for free:

- A **quality trendline** per client and per agent
- The ability to say "our tenth build scored 91, our first scored 74" — which is the only honest
  proof that a process is improving
- **Attribution**: which agent, which model, which prompt produced the low scores

The existing scores already earned their keep: they identified blog as eighteen points worse than
everything else, which no amount of reading would have surfaced.

**One caveat to fix while adopting it:** normalise the model identifier. Runs are currently split
across `claude-sonnet-4`, `gemini-2.5-pro` and `google/gemini-2.5-pro` — two spellings of one model
— for the same asset types, so a 56 on a blog can't be attributed to prompt or model. Fix that and
the scores become an A/B test already paid for.

## 3 · Close the loop from shipped to converted

**Status 2026-09-06: skeleton built, no data yet.** `scripts/converted.py pull|learn` and `data/README.md`. It writes nothing until a pattern clears the sample floor — which is the point.

**Everything in this repo optimises for passing a gate. Nothing measures whether the thing worked.**

We know which modules exist, which order they went in, and what the page scored. We have no idea
which ones **converted**. So taste is still opinion with good hygiene.

The data is already in HubSpot: form submissions, meeting bookings, and page views per URL. Joining
it to the section order we recorded per page gives the thing nobody in this category has:

> *"On dealer homepages, `pain-bridge` above the fold converted at 3.1% against `is-this-you` at
> 1.8%, n=6 sites."*

**Build:** per-page conversion pulled monthly, joined to the page record's section list, written to
`agent_learnings` **with a minimum sample size.** That last clause is not optional — BrandCommand
currently holds a learning asserting that the best variant is the one with a 0% reply rate, at
maximum confidence.

This is the item that changes what QBS *is*: a shop with evidence rather than a shop with taste.

---

## 4 · Make the judgement steps delegable

**Status 2026-09-06: written.** `process/decisions.md` — eight decision rules.

**15 of the 37 runbook steps are 🏢 QBS.** At any real volume, that is the ceiling — and most of
those steps are judgement that lives in one head.

Some are already written as rules and are genuinely delegable: the three-of-nine selection rules,
the card-grid table, the contrast floors, the mobile floors. Those are the model.

These are not, and each is a decision someone makes by feel:

- What makes a wildcard **good** rather than padding
- When a theme defect is worth **fixing at source** versus living with
- When a build needs **Phase 4** at all
- What counts as "**could belong to any company in the category**"
- When to **walk away** from a scope

**Build:** write each as a decision rule with a worked example, the way `catalogue.md` does for
theme selection. A rule you can hand over is worth more than a judgement you can exercise.

## 5 · Price the actual cost driver

**Status 2026-09-06: estimated, not measured.** Per-unit Phase 4 estimates in `process/clientcommand.md`; the `layoutSections` afternoon still decides 8h vs 40h.

The tiers price **page count**. The cost driver is **Phase 4** — custom modules, sections and
templates — which is priced at nothing.

Revolution needed 29 modules, 7 sections and 49 templates. That is plausibly a second build's worth
of work inside one engagement, and no tier accounts for it.

**Build:** a Phase 4 line item with a per-module rate, and a rule for when it applies (the section
list needs something the 57 don't have). Then two model variants — *first build in a vertical*,
where the platform work is amortised or priced as investment, and *subsequent build*, which is the
belt.

Until then every quote on a non-standard build is provisional, and the repo should keep saying so.

## 6 · A module-level performance library

**Status 2026-09-06: schema only.** `data/pages.jsonl` records `sections` per page; `converted.py learn` groups on the first three. Needs shipped pages.

`design/references.md` records six external sites we admire. There is **no record of which of our
own pages performed.**

That's the compounding asset. Every build adds a data point: this vertical, this section order, this
hero treatment, this conversion rate. After ten builds you can open a dealer pitch with *"this
layout converts at X across six dealers"* — which is a claim no competitor can make and no amount of
design talent substitutes for.

Depends on item 3.

## 7 · Monitor the category continuously

**Status 2026-09-06: built, not armed.** `scripts/monitor.py plan --vertical office-technology` emits the Firecrawl monitor calls; `--apply --approved-by` records them. No live monitors yet.

We scrape competitors once, at brief time, and never again.

For a vertical where **six of ten clients are office technology**, continuous monitoring is cheap
and compounding: Firecrawl has `firecrawl_monitor_create`, Semrush has position tracking. Knowing a
competitor relaunched, or that a category keyword's difficulty dropped, is worth more in outbound
than in delivery.

**Build:** monitors on the top five competitors per vertical, a monthly digest, and a trigger into
`process/outbound-mockups.md` when a prospect's site materially changes — a relaunch is the worst
possible moment to pitch, and a *stale* site is the best.

## 8 · Give the process an owner and a cadence

**Status 2026-09-06: done.** Version stamp, owner and the monthly agenda are at the top and bottom of `RUNBOOK.md`.

Twenty documents, five scripts, and **no named owner and no review date.** That is how a good
process becomes a stale one — and this repo has already demonstrated the failure mode twice: claims
that were true when written and false three months later, caught only by an adversarial audit.

**Build:** one named owner. A monthly pass with a fixed agenda — run the QA agents, reconcile the
numbers against actuals, retire anything superseded. And a version stamp on `RUNBOOK.md`, because a
process without a version is one nobody can tell is out of date.

## 9 · An onboarding track

**Status 2026-09-06: written; catalogue pending.** `process/onboarding.md` — three builds, graduated permissions. The visual module catalogue still needs `all-modules.html` published on staging so it can be screenshotted.

`OPERATOR.md` is a checklist, not a curriculum. A new hire cannot run this today, and several steps
silently assume an AI agent is doing them.

**Build:** a first-build path — shadow one, run one with review, run one alone — and graduated
permissions, so `--apply` on a live portal is earned rather than granted. Plus the **visual module
catalogue** (`all-modules.html` already exists in every theme; screenshot it), because step 13 asks
someone to pick from 57 module *names*.

---

## If you do three

**1** (themes in git) because it is the risk. **2** (score every page) because it is nearly free and
it tells you whether any of this is working. **3** (shipped→converted) because it is the only one
that changes what the business is.

Items 4–9 are what a competitor cannot copy by hiring a good designer.

## And the two things that are still just waiting

- **One tracked build.** Every hour figure here is an estimate. Kelly replaces them with numbers.
- **The `layoutSections` question.** One afternoon decides whether Phase 4 costs 8 hours or 40 per
  build, and it changes both the pricing and the page-counting rule.
