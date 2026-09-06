# Scheduling

Who does what, when, and what has to be true before each thing can start. The 28 steps in
`process/RUNBOOK.md` are the *order*; this is the *calendar*.

Built on one number from `process/clientcommand.md`: a build is **weeks of work spread across months
of waiting.** So scheduling is not about compressing our work — it's about starting the waits as
early as possible and never being the reason something is idle.

---

## The two rules that decide whether a date holds

**1 · Start every wait on day one.** Client-owed assets, copy approval slots, portal access,
their process deck. Each is a multi-day wait that only starts when you ask. Asking on day one and
day thirty produces the same amount of our work and a five-week difference in delivery.

**2 · Every approval carries a default that ships.** *"No reply by Friday and we proceed as
drafted."* Without it a wait has no end and no owner. With it, silence becomes a decision.

Those two rules move more calendar than any tooling in this repo.

## The week-one contract

Everything below happens in the first five working days, regardless of tier. Front-loading is the
entire schedule strategy.

| Day | What | Why it must be day one |
|---|---|---|
| 1 | `verify.mjs` on their site · Semrush pulls 1–3 | Free, and it's the diagnosis |
| 1 | **Create the Semrush project** | The crawl takes hours; pull 4 is blocked until it finishes |
| 1 | **Confirm HubSpot tier and the page cap** | Free tier caps site pages at 30. Finding this in week nine is a refund conversation |
| 1 | **Request every client-owed asset**, each with an owner and a date | The longest wait in the engagement |
| 1 | **Ask for their process deck** | The highest-return question in discovery — `design/patterns.md` |
| 2 | Brand measurement · competitor scrapes · write the brief | Feeds everything |
| 3 | The four questions · pick three of nine | — |
| 4 | Render and present the three directions | Mockups are minutes now, so there is no reason to wait |
| 5 | **Book the two copy-review slots, in their calendar, now** | An unbooked review is an unbounded wait |

By end of week one you should hold: a diagnosis, a baseline, a brief, three directions, and dates on
every client dependency.

## The phase calendar

Days are calendar days from kickoff. Phases overlap deliberately.

| Phase | Days | Blocked by | Blocks |
|---|---|---|---|
| 1 Diagnose | 1–10 | nothing | everything |
| 2 Direction | 8–20 | the brief | the theme build |
| 3 Structure & content | 20–50 | direction chosen | the page build |
| **4 Theme, templates, modules** | 30–60 | **section list, not copy** | the page build |
| 5 Build the website | 50–75 | Phase 4 **and** approved copy | the gate |
| 6 Agent loop | 65–85 | a **staging URL** | launch |
| 7 Launch | 85–90 | gate clean, 301s ready | — |
| 8 Optimise | 90+ | a written baseline | the retainer |

### Three dependencies people get wrong

- **Phase 4 does not wait for copy.** It needs the *section list* from step 13, not approved words.
  Starting the theme build at day 30 instead of day 50 is twenty days of parallelism, free.
- **Phase 6 needs a staging publish**, because draft HubSpot pages redirect to a login and no gate
  can read them. Schedule the staging publish as a task, not an afterthought.
- **Assets block Phase 5, not Phase 6.** A page can't reach *built* without them. Chase from week
  one.

## Batch by station, not by client

The operational move that makes concurrency work: **one person does one station across several
clients.** Sectioning four clients in a morning is far cheaper than context-switching through four
whole builds.

A workable weekly shape:

| | Focus |
|---|---|
| Mon | New-business day — diagnoses, baselines, mockups, outbound |
| Tue | Sectioning and copy drafting, all clients |
| Wed | Theme and module work (Phase 4), all clients |
| Thu | Page building (Phase 5), all clients |
| Fri | Gates, agent loops, human review — **and chase every overdue client asset** |

Friday matters most: it's the gate day *and* the chase day, and it sets up whether next week has
work ready.

## WIP limits

A line without limits becomes many half-finished builds and every date slips together.

| Station | Limit | Why |
|---|---|---|
| Phase 4 (theme build) | **1 client** | It's the deepest work and the easiest to half-finish |
| Phase 5 (page build) | 2 clients | — |
| *Copy approved* (waiting) | no limit | It's a queue, not a station — but every item needs a date |
| Phase 6 (agent loop) | 2 clients | Needs a human to look, and looking doesn't scale |

**Nothing enters a station until something leaves it.**

## The four weekly numbers

| Metric | Read it as |
|---|---|
| **WIP per station, all clients** | Where the pile-up is. Sitting at *copy approved* = client latency; at *built* = ours |
| **Age of the oldest item per station** | A page stuck three weeks is invisible in a phase view and obvious here |
| **Client-owed assets overdue** | The most actionable report in the system |
| **Actual hours per station** | Replaces the estimates. **The model is only useful once it's calibrated** |

## Capacity, honestly

Per `process/clientcommand.md`, one person's work-only ceiling is roughly **16 concurrent Launch,
8 Growth, or 3 Transform.** Do not plan to that. Plan to about **half**, because:

- Phase 4 has a WIP limit of one, and it is unavoidable on any non-standard build
- Phase 6 needs a human to look, every time
- Client latency is unevenly distributed — three clients going quiet in the same week is normal

**And Phase 4 is not in the hour model yet.** The Revolution build needed 29 modules, 7 sections and
10 templates — plausibly another 58 hours, which would roughly double a build. Until actuals are
recorded, treat any quote on a build needing custom modules as provisional.

## What to do when a date is going to slip

In this order:

1. **Name which station it's stuck in and who owns it.** "The project is late" is not diagnosis.
2. **If it's a client wait, invoke the default.** That's what the default is for.
3. **If it's ours, check the WIP limits** — usually a limit was broken upstream.
4. **Cut scope, not the gate.** Fewer pages ships; an ungated page shouldn't. `verify.mjs` passing
   is not the negotiable part.
5. **Tell the client early, with the station named.** A specific cause and a new date is a very
   different conversation from a slipped launch.
