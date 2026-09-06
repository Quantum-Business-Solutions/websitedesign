# The runbook

**Eight production phases, 37 steps, in order** — from "we should talk to them" to "launched, on
retainer, and calibrated."

Everything else in this repo explains *why*. This file is *what to do next, and whose job it is*.

## Who owns each step

Every step carries one owner. This is the column that stops work sitting idle because nobody knew
it was theirs.

| Tag | Means | Notes |
|---|---|---|
| 🤖 **AI** | An agent or a script does it | Always gated — see `process/agents.md`. An ungated agent step is a confident guess |
| 🏢 **QBS** | A Quantum human | Judgement, relationships, or a decision an agent shouldn't make |
| 🤖→🏢 **AI, QBS reviews** | Agent produces, a human signs off before it goes further | The default for anything client-facing |
| 👤 **CLIENT** | Theirs. We ask, chase, and give it a date | The critical path. Never assume it's in flight |
| 🔒 **APPROVAL** | Blocks until a **named** person says yes | Portal writes, spend, going live |
| 🚦 **GATE** | An artifact can fail it — exit code or a written check | Not an opinion |

**Two rules that decide whether a date holds**, both from `process/SCHEDULE.md`:
**start every 👤 wait on day one**, and **give every 👤 approval a default that ships**
("no reply by Friday and we proceed as drafted").

## The eight phases

The six phases on the website-services page are **commercial** — they own the dates and the client
sees them. These eight are **production**. They are not the same list.

| Production phase | Sold phase | Days |
|---|---|---|
| **1 · Diagnose & scope** | 01 Information Gathering | 1–10 |
| **2 · Direction** | 02 Planning | 8–20 |
| **3 · Structure & content** | 03 Wireframing · 04 Content | 20–50 |
| **4 · Build theme, templates, modules** | 05 Design & Build | 30–60 |
| **5 · Build the website** | 05 Design & Build | 50–75 |
| **6 · Run the agents against it** | 06 Test & Review | 65–85 |
| **7 · Launch** | 06 Launch | 85–90 |
| **8 · Optimise & calibrate** | post-launch | ongoing |

---

# Phase 1 · Diagnose & scope — days 1–10

### 1 🤖 Diagnose their current site
`node scripts/verify.mjs https://<their-domain>` — two minutes, and it's the diagnosis you open with.
**Done:** their failure list exists.

### 2 🤖 Pull the SEO baseline
The four Semrush pulls in `process/seo-baseline.md`.
**Done:** traffic, top pages and a striking-distance keyword are in the brief. **That traffic number
is what the engagement gets measured against.** New client → **create the Semrush project today**;
the crawl takes hours.

### 3 🤖 Measure their brand
`firecrawl_scrape`, `formats: ["branding"]`, on their site plus two or three competitors.
**Done:** the real accent hex. Never eyeball it off a logo.

### 4 🏢🚦 Confirm the platform can hold the build
Client's HubSpot tier, **their portal id**, and the page cap. Free tier caps site pages at **30**; a
50-page Transform is impossible on it. Record `pages_allowed` **and** `pages_planned`.
**Done:** planned ≤ allowed, or the scope changed. Finding this in week nine is a refund
conversation.

### 5 🏢 Inventory what already works on their site — and what breaks if we touch it
Chat widget · booking tool · review widgets · payment or e-commerce · call tracking · marketing
pixels · any embedded third-party app.
**Done:** a list, each marked keep / rebuild / drop. **Breaking a working integration at cutover is
the most common self-inflicted launch failure**, and it is invisible unless someone writes the list.

### 6 🏢🔒 Settle the commercial and legal frame
- **Tier and scope** signed. Change-order trigger agreed in writing (step 34).
- **Who owns what at the end.** "Nine themes, all yours, no licences" is a sales claim — make sure
  the contract says the same about the clone, the copy we write, and the generated imagery.
- **Licensing:** fonts (the nine use open-licence faces; a client-specified paid face is a real
  cost), stock photography, and commercial rights on anything generated.
- **Named approvers, both sides.** Who signs off design, copy, and go-live for them; who approves
  portal writes and spend for us. `process/qa-findings.md` flagged that "needs approval" appears in
  seven places with no person named. Fix it here, per engagement.
**Done:** both names written into the brief.

### 7 👤 Ask for everything the client owes — once, today
Logo **light and dark** · photography · the gated asset · case-study permissions · portal access ·
**their process deck** (the highest-return ask in the call — `design/patterns.md`) · **DNS and
current-host access**.
**Every ask gets an owner and a date.**
**Done:** the asset rows exist with owners. **The highest-leverage ten minutes in the runbook** — it
decides 90 days versus 130.

### 8 🤖→🏢 Write the brief
`brands/<slug>.md` from the template. Every section is consumed later.
**Vertical client?** Load the kit too — `verticals/office-technology.md` for a dealer.
**Done:** no `<placeholders>` remain, and a human has read it.

### 9 🏢 The four questions
Ground · register · **the promise, in their words** · lane.
**Done:** the promise is in the brief verbatim. It is the one input that cannot be measured or
inferred, which is why it is 🏢 and not 🤖.

---

# Phase 2 · Direction — days 8–20

### 10 🤖→🏢 Pick three of nine
Rules in `themes/catalogue.md`: ground from the **brief, not taste** · safe / stretch / wildcard ·
typeface to reading load · never two with the same ground and typeface class.

### 11 🤖🚦 Render the three
```bash
python3 scripts/mockup.py --client "<Company>" \
    --themes "Quantum <A>,Quantum <B>,Quantum <C>" \
    --accent "#RRGGBB" --brief brands/<slug>.md \
    --roles "The safe one|The stretch|The wildcard" \
    --rationales "<why A>|<why B>|<why C>" --out /tmp/<slug>.html
```
**Gate:** exits non-zero on a set-level rule violation, and warns if a direction's accent text won't
clear the build gate.
**Done:** screenshotted at 1440 **and** 390, and looked at.

### 12 🏢 Present it
`process/pitch-presentation.md`. Main page first — the evidence — then the three.

### 13 👤🔒 They choose
**Done:** the choice **and why, in their words**, in the brief. Attach a decision date.

### 14 🤖→🏢 Build the URL map
Every trafficked page from step 2: old URL → new URL → **301**. Include WordPress oddities —
`/?p=123`, feed URLs, category and tag archives, attachment pages.
**Done:** no trafficked page lacks a destination.

### 15 🏢 Open the plan and the page records
Plan from the tier template. **One record per page** — `process/clientcommand.md`.
**Done:** N page records exist with template, owner and asset list.

---

# Phase 3 · Structure & content — days 20–50

### 16 🤖→🏢 Section every page
Module order from the 57, plus the vertical kit. **This is the wireframe** — an inventory choice,
not a drawing.
**Done:** every page record has a section list, and card counts check against the balance table in
`design/guardrails.md` — **now**, while it's free to change.

### 17 👤🚦 Structure signed off
**Done:** page list and section order agreed in writing. **Default that ships.**

### 18 🤖→🏢 Draft copy, grounded not generated
Every `<h1>` answers a **real keyword** from step 2. Three P's above the fold. Their language from
step 3. **Site pages are the Copywriter agent; campaign assets are BrandCommand's
`campaign-launcher`** — same skill, different gate.
**Score it.** Write a critic score to `agent_runs` the way BrandCommand already does for campaign
assets. **Nothing ships under 80.** Live scores say `blog` averages 67.4 against 85.1 for every
other asset type — and blog posts drive 82% of organic traffic, so this is the single most valuable
number in the system to move.
**Done:** no page could belong to another company in the category, and every page is scored.

### 19 🏢🚦 Verify every number on the page
**Every figure a client site claims is theirs to confirm** — years in business, technician count,
response time, first-call fix rate, devices under management. An agent that cannot find a number
will write a plausible one, and no automated gate catches it.
**Done:** every numeral on every page traces to a source in the brief, with who supplied it and
when. **This is the only step here with legal exposure.**

### 20 👤🚦 Copy approved
Its own step because it's the biggest schedule risk in the engagement. **Batch it** — two scheduled
reviews, not a trickle. **Default that ships.**

### 21 🤖→🏢 Compliance content
Privacy policy · terms · cookie-consent banner (HubSpot has the tooling) · form consent language ·
**accessibility statement**. The last one is both a sellable deliverable and a liability position,
and nobody in this category has one.
**Done:** drafted, and **the client's counsel has seen the privacy policy and terms.** We draft;
they own the legal text.

---

# Phase 4 · Build theme, templates, modules — days 30–60

**The phase the nine themes don't cover alone.** Reference implementation: `themes/architecture.md`.
It needs the **section list** from step 16, *not* approved copy — so it starts at day 30, not 50.

### 22 🤖🔒🚦 Clone and re-skin, in the client's portal
```bash
python3 scripts/reskin.py plan --portal <CLIENT_PORTAL_ID> \
    --theme "Quantum <Theme>" --client "<Company>" \
    --accent "#RRGGBB" --ground <light|dark> \
    --org-name "<Legal name>" --org-url "https://<domain>" \
    --org-logo "<url>" --org-sameas "<linkedin>"
```
`CLIENT_HUBSPOT_TOKEN`, never ours. **Show the change table to the named approver from step 6 and
wait for an explicit yes**, then `--apply --approved-by "<name>"`.
**Gate:** four contrast ratios, blocking. It refuses to touch the nine in any portal.

### 23 🤖 Confirm the accent split took
`--accent-ink` (accent text on light) and `--accent-lift` (on dark) are derived automatically now.
A saturated brand accent used as a button **fill** will still warn at WCAG 1.4.11 — the remedy is a
1px border on accent-filled controls, not a different brand colour.

### 24 🏢🚦 De-brand the header and footer
They hardcode QBS's logo, nav, social links and copyright, and step 22 does **not** fix them. The
better fix, proven on Revolution: make them **field-driven modules**.
**Done:** `node scripts/verify.mjs` reports **no QBS branding left**. Nothing goes in front of a
client before this.

### 25 🤖→🏢 Build the modules the section list needs
Copy the `quantum-faq` pattern: derived from the module's own fields, `|escapejson`, schema in the
module that renders the content. For a dealer, most already exist in Revolution's 29 — **port, don't
rebuild** (`verticals/office-technology.md`).

### 26 🤖→🏢 Build the templates
**Settle `layoutSections` first** — Revolution had to bake content into per-page templates, but its
own tooling suggests the cause was a malformed cell tree since fixed. One afternoon decides whether
this phase costs 8 hours or 40.

---

# Phase 5 · Build the website — days 50–75

### 27 🤖→🏢 Build the pages
Real content. One `<h1>`. **Featured image on every page** or `og:image` is absent. Lazy below the
fold, `fetchpriority="high"` on the hero, `width`/`height` **plus `height:auto`**.

### 28 🤖 Generate and place the assets
Higgsfield MCP, `fal.ai` fallback. **Chosen direction only.** Generate **blank surfaces** so labels
stay real HTML text.
**Done:** every asset row filled. Chase the 👤 ones from step 7.

### 29 🏢 Wire the plumbing
Form notification routing — **who actually receives the lead** · autoresponders · the thank-you page
as a tracked conversion event · GA4 · Search Console · HubSpot tracking code · **the conversion
events we will report on**, named now so the baseline means something.
**Done:** a test submission reaches a named human.

### 30 🏢🚦 Publish to staging so the gate can read it
Draft pages redirect to a login, so nothing can gate them. Publish to
`<client-portal>.hs-sites.com` **with `noindex`** — an indexable staging copy is a crawlable
duplicate of their site.
**Done:** a URL `verify.mjs` can load.

---

# Phase 6 · Run the agents against it — days 65–85

### 31 🤖🚦 The automated gate
```bash
node scripts/verify.mjs <staging-url> --env staging --expect-org "<Client legal name>"
```
Exit 1 = not done. **A failure returns to the station that caused it**, not to step 1: contrast →
22/23 · placeholder text → 18 · card orphan → 16 · QBS branding → 24.

### 32 🤖→🏢 The agents that read what a script can't
Quality · fact-check · copy · AEO · adversarial verifier — `process/agents.md`.
**Halt on oscillation:** if two passes reverse each other, stop and name the conflict. The sticky-CTA
rule and the 25%-of-viewport ceiling genuinely conflict on a phone, and a loop left alone resolves
it by silently dropping a sold feature.
**Done:** clean twice running, **and a human has scrolled every page on a real phone.**

### 33 🏢🚦 Test the money path yourself
Submit a form. Book a meeting. Confirm the CRM row, the thank-you page, the asset delivery. Share one
URL into Slack and look at the card.
**Done:** you received your own test submission.

### 34 🏢 Handle any scope change as a change order
Pages beyond the tier allowance, a new module, a location set. **Priced and approved in writing
before it's built**, per the trigger from step 6. On fixed price this is where the margin goes.

---

# Phase 7 · Launch — days 85–90

### 35 🏢🔒 Pre-flight, then go
- **Drop DNS TTL 48 hours ahead**, so a rollback is minutes not days
- **Rollback plan written**: the old site stays reachable for 30 days, and someone owns the decision
- 301s live and spot-checked **individually** on the top-traffic pages
- **Re-test every integration from step 5** on the live site
- Remove the staging publish; confirm those URLs 404
- No stray `noindex` or `nosnippet` — `nosnippet` also blocks AI Overviews
- Resubmit the sitemap in Search Console
**Done:** live, and the **pre-launch baseline is written down**. 🔒 Going live is the client's call.

### 36 🏢 Watch it for 48 hours
404 spike · form submissions actually arriving · Search Console coverage errors · Core Web Vitals on
the live site.
**Done:** 48 hours clean, or fixed.

---

# Phase 8 · Optimise & calibrate — ongoing

### 37 🏢→👤 Hand over, calibrate, and convert
**Write the actuals back.** Hours per station, critic scores per page, and — the one nobody does —
**which module order the converting pages used.** `agent_runs` and `agent_learnings` already exist
for this. A learning needs a **minimum sample** before it's written; BrandCommand currently holds one
that reinforces a 0% reply rate at maximum confidence, which is worse than no learning.
- **A recorded walkthrough**, not a live one. It scales, and it's what makes "editable by your team"
  true instead of a support queue.
- **Record actual hours per station** and replace the estimates in `process/clientcommand.md`.
  Every number in this repo is currently an estimate. **This step is the only thing that changes
  that.**
- **Case study from the measured delta.** Delivery becomes pipeline.
- **The retainer conversation** — a task with a date. $2,500/month at ten hours is $250/hr against
  $172 for the build.
- **Promote what you learned:** a rule → `design/guardrails.md` · a task → the library · a theme
  defect → **fix at source** so all nine benefit · a vertical pattern → `verticals/`.

---

## Ownership at a glance

| Owner | Steps | The pattern |
|---|---|---|
| 🤖 **AI** | 1, 2, 3, 11, 23, 28, 31 | Measurement, generation, gating. Cheap and repeatable |
| 🤖→🏢 | 8, 10, 14, 16, 18, 21, 25, 26, 27, 32 | Most of the build. An agent drafts, a human owns it |
| 🏢 **QBS** | 4, 5, 6, 9, 12, 15, 19, 24, 29, 30, 33, 34, 35, 36, 37 | Judgement, relationships, truth, and going live |
| 👤 **CLIENT** | 7, 13, 17, 20 | **All four are on the critical path.** Every one gets a date and a default |
| 🔒 **APPROVAL** | 6, 13, 22, 35 | Scope · direction · portal write · go-live |

**Read that client column again.** Four steps, and they gate roughly 87% of the calendar. Everything
in this repo about tooling is optimising the 13%.

## The seven things that make this fail

1. **No brief** (8) — the model reaches for its defaults and you get slop.
2. **Client-owed assets asked for late** (7) — ten minutes that decides 90 days versus 130.
3. **No default on an approval** (13, 17, 20) — an open-ended wait has no end and no owner.
4. **Skipping the de-brand** (24) — a client seeing our logo is the worst five seconds in the
   engagement.
5. **Forgetting the staging publish** (30) — you cannot gate a draft page, and the gate will happily
   report on a login screen.
6. **An unsourced number on a client page** (19) — the only failure here with legal exposure, and no
   automated gate catches it.
7. **Treating Phase 4 as free** (22–26) — custom modules are real work and the hour model still
   doesn't price them.

## If you only have an hour

The four that are correctness, not quality: **entity facts in the schema** (22) · **the
header/footer de-brand** (24) · **301s on trafficked URLs** (14, 35) · **`verify.mjs` passing** (31).
