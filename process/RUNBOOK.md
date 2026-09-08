# The runbook

> **Version 2.1 · 2026-09-08 · Owner: Shawn Peterson · Next review: 2026-10-08**
> Version 2 folds in what Revolution, Kelly, Nexus, VanAusdall and Image 2000 taught us in one week. Section "What changed in version 2" at the bottom lists it; the steps below carry the changes inline.
> Reviewed monthly, on the agenda in *Owner and cadence* at the bottom. If today is past the review
> date, this document is unverified — read `process/qa-findings.md` for what tends to rot first.

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

### 2 🤖 Pull the search and AI-answer baseline
The scripted package in `process/seo-baseline.md`, version 2: every sitemap URL fetched and scored by
`scripts/seo_audit.py` (sixteen checks), the Semrush pulls for the client and each real competitor, six to
eight buyer queries fetched live from the client's city, the brand-plus-reviews query, the competitor money
pages parsed the same way, and `brands/<slug>.seo.json` written from `brands/_starter.seo.json`.
**Done:** `preview.py` renders `seo-report.html`, the every-page audit on the hub with today against the
build, `seo-audit-pages.csv` and `redirects.csv`. **The traffic number and the readiness average are what
the engagement gets measured against.** New client → **create the Semrush project today**; the crawl takes hours.

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

### 12b 🤖→🏢 Build the preview site
`/preview <client>`: `scripts/preview.py` renders every page of the site in all three directions
from `brands/<slug>.content.json`, plus the chooser hub (specs, our pick with reasons, compare,
every page, the plan, reply). Pushed to the client repo, live at `https://<slug>.vercel.app`,
`noindex`. Gate the recommended home page, the locations page and the blog listing; run the Copy
critic, Fact checker and Mobile reviewer on the hub and the home page. **The client gets the hub
URL only, and only after the gate and the agents pass.** Inputs: `process/INTAKE.md`.
The content file is written by `brands/<slug>.content.py` (constants in, JSON out); edit the script,
rerun it, rerun `preview.py`. Every rendered page must resolve its links from nested folders, so run
the link and image check (`node scripts/preview_check.mjs <dir>/<page>.html ...`, run from this repo) before the gate. Motion (count-up, hero
parallax, card tilt, logo marquee) is on by default and turns itself off under
`prefers-reduced-motion`; nothing on the page depends on it.

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
**Assign the blog templates first**: Settings → Website → Blog → the client's blog → Templates →
the clone's `blog-listing.html` and `blog-post.html`. The blog is set in blog settings, not in the
theme, so it is the page most likely to ship in a default template. Then the pages.
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
This is **Station A of `process/qa-process.md`**, and every check maps to a line in
`process/quality-standard.md`, the guarantee the client was given at step 6.
Every page also gets a **score out of 100** (correctness FAIL −8, quality FAIL −5, WARN −1.5).
**Nothing ships under 80**, and the run appends to `verify-out/scores.jsonl` — the trendline that
tells you whether builds are getting better, which pass/fail never could.

### 32 🤖→🏢 The agents that read what a script can't
Quality · fact-check · copy · AEO · adversarial verifier — `process/agents.md`. **Station B** of
`process/qa-process.md`, then **Station C**: a person opens every page on a real phone and signs it.
No em dashes anywhere a visitor reads (`design/guardrails.md`); the gate fails the page on one.
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
The gate's URL list always includes `/blog` and one post. A blog listing in the wrong template is
the most common "the site is live but looks broken" call.
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
**which module order the converting pages used.** Concretely: one line per shipped page in
`data/pages.jsonl` (schema in `data/README.md`), then `scripts/converted.py pull` at 30/60/90 days
and `converted.py learn` — which writes nothing until a pattern clears the sample floor. `agent_runs` and `agent_learnings` already exist
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

## Owner and cadence

**Owner:** Shawn Peterson. One person, by name, or it is nobody.

**Monthly, first working day, ninety minutes, fixed agenda:**

1. `python3 scripts/reskin.py drift` — did the nine themes move in the portal without a commit?
2. Run the QA agents (`process/qa-findings.md` has the last pass) against RUNBOOK, OPERATOR,
   clientcommand. Anything they catch gets fixed or retired that day — no "known issues" list.
3. Reconcile `process/clientcommand.md` hours against `data/pages.jsonl` actuals. Replace the
   estimate the moment there are three real builds behind it.
4. Read `verify-out/scores.jsonl`. If the median is falling, something upstream changed.
5. `converted.py learn` — read what cleared the floor, and what almost did.
6. Bump the version stamp at the top and the *next review* date. **A review that doesn't change the
   stamp didn't happen.**
7. Re-upload any process document that changed this month to the ClientCommand knowledge base
   (entry ids in `process/repos.md`). The repo is the source of truth; ClientCommand is where the
   team reads it.

Version numbers: patch for wording, minor for a step added or an owner changed, major when the phase
list changes. `git log -- process/RUNBOOK.md` is the changelog.

## If you only have an hour

The four that are correctness, not quality: **entity facts in the schema** (22) · **the
header/footer de-brand** (24) · **301s on trafficked URLs** (14, 35) · **`verify.mjs` passing** (31).


## What changed in version 2 (2026-09-08)

Five clients through the line in one week, three of them in a single day, showed where the process leaked. These are now the rules.

### One toolchain
The Python conveyor (`brands/<slug>.content.py` to `scripts/preview.py`) is the product. Revolution's Next.js path is retired for new clients; two things from it are being ported: the HubSpot theme pipeline (tokens generated from one source, pages built as drafts) and the measurement harness (true-compositing contrast, all routes at four widths, hub behaviour, page performance under CPU throttle, type scale). Until the port lands, run Revolution's `scripts/qa-contrast.mjs` logic against any translucent header by hand.

Two build facts from Revolution go in every plan: layout sections pushed through the HubSpot API do not render, so page content is baked into per-page templates; and the free HubSpot tier caps site pages at 30. Check the client's tier against the page count on the hub before the plan is presented.

### The standard package, version two
Every client starts from `brands/_starter.content.py`, which places the full signature set by default: layered hero with the network canvas and a 3D hero object, wheel, process chart on the home and every service page, before/after on every service page, seal, fleet rail, floor plan hotspots, scroll story, history rail, map (region per client), film slot, launcher, depth layer. Removing a module is a decision; adding one is not.

Rules that came from Shawn this week:
- No recommended direction unless we have a reason we can say out loud. Showcase first in the order. Run `preview.py` without `--recommend` and the hub shows "Your call".
- A direction may borrow another's typefaces (`brand.type_from`). Kelly runs Showcase in Clean's Open Sans.
- Floor plan hotspots on every client with a physical place. Generate the isometric with the client's rooms named, measure once, place the points.
- The history rail on every client with a founding date. Sourced years only; decades as honest placeholders, listed under To confirm.
- Reusable renders and models go to `library/` with a README line the same day. Check the library before generating.
- No em dashes anywhere client-facing. No exclamation marks. No unsourced response-time or pricing promises.

The intake stage is explicit and scripted, in this order, and it is the top of the production chart:
1. Scan the current website: `firecrawl_map` for the URL inventory, `firecrawl_scrape` of every top-level page, a note of the platform, the forms vendor, the cookie banner, broken links (Image 2000's Request a Quote linked to the home page) and any members-only links in public navigation.
2. Pull the search and AI-answer baseline (the version 2.1 package below): the page audit, the Semrush pulls, the live buyer queries, the competitor pages, the seo.json.
3. Measure the live home page: HTML weight, scripts, stylesheets, images without lazy loading, pinch-zoom blocked, schema present, LocalBusiness present.
4. Awards and press: the trade press profile (ENX, Industry Analysts), manufacturer award listings, the BBB record. These become the seal.
5. Brand assets: logo files at full size, colours read from the logo, partner and award badges, team photographs, any film.
6. Call notes and the proposal canvas, if there is one, read in full before a word is written.
7. Write the To confirm list as you go, not at the end.

Every client gets a design system page (`design-system.html`, generated) and the search and AI-answer package (`seo-report.html`, the every-page audit on the hub, the audit sheet and the redirect map), generated.

### QA, one gate
Add to `verify.mjs` as the next job: the true-compositing contrast probe, all routes at 390, 768, 1280 and 1440 with exactly one h1, hub behaviour, page performance under CPU throttle, and the type scale check. Already added this week: a hard error when a compose id matches no section, and axe rules for nested interactive, contrast and heading order. The local LCP failure is the sandbox blocking Google Fonts; mark it staging-only rather than ignoring it.

### Housekeeping that cost time
- Vercel projects are created by Shawn at intake, one per client, and connected to the client repo. The API can create a project but cannot link the repository. Live: kelly-office-solutions.vercel.app, image2000.vercel.app, van-ausdall.vercel.app, and Nexus from the Nexus repo at nexus-gold-beta.vercel.app/preview/.
- The exact preview command is recorded in the client repo README on the first push.
- Every session ends with the ClientCommand knowledge base entry for the client and, when a process changed, a re-upload of the changed process doc.
- Scripts: never kill a process by a pattern that appears in the calling command line. Playwright screenshots either abort font requests or wait for them, never both.
- Generated imagery is labelled on the page, every time, and is never described as the client's people or premises.

## What changed in version 2.1 (2026-09-08, evening)

Van Ausdall's hub showed what a client-facing search analysis should look like: ranked findings with evidence, cost and fix; the same page side by side with the competitors; every URL on the current site scored and set beside the page that replaces it; a redirect map. It was built by hand in one session. It is now generated for every client, and Kelly and Nexus carry it.

### The search and AI-answer package
Three files next to the content file, and one command:
- `brands/<slug>.audit.json`, written by `scripts/seo_audit.py live` from the sitemap URLs fetched to disk (`seo_audit.py fetch`). Sixteen checks per page, weighted to what answer engines read (FAQPage, Service or Article, LocalBusiness, question headings, depth), a score out of 100 and a grade. The same script scores the build (`seo_audit.py build`), so the hub shows today against the build page for page.
- `brands/<slug>.seo.json`, authored from `brands/_starter.seo.json` with the numbers from the pulls: hero tiles, thirteen ranked findings, the side-by-side table and verdict, five moves, blog and entity sections, competitors, keyword opportunities, clusters per service line, question keywords, the answer-engine scoreboard, crawlers, backlinks, reviews, the 90-day plan, the measures, the hub's today and after columns, the keep table, site-wide checks and the redirect overrides.
- `scripts/preview_seo.py`, called by `preview.py` when both files exist. Writes `seo-report.html`, `seo-audit-pages.csv`, `redirects.csv`, `seo-build-scores.json`, and hands the hub its Search and Every URL sections.

The pulls, in order (about forty minutes with the MCP tools): sitemap index and every child sitemap; `seo_audit.py fetch` then `live`; Semrush `domain_rank`, `domain_organic` (top 60 by traffic), `domain_organic_unique`, `domain_organic_organic`, `backlinks_overview`, `backlinks_refdomains` for the client; `phrase_organic` or `firecrawl_search` from the client's city for six to eight buyer queries plus the brand-and-reviews query; `domain_rank` and `backlinks_overview` for the four or five competitors those results name; `phrase_related` and `phrase_questions` per service line; `phrase_these` for the target list; robots.txt, llms.txt, the home page's scripts, forms vendor, tracking and schema; the competitor money pages fetched and parsed by `seo_audit.audit_html`. Semrush's own competitor list is a starting point only: for a brand with a common name it returns namesakes.

### What the build now does on every page
`preview.py` normalises every title to 30 to 60 characters with the brand and, where the schema block sets `title_city`, the service area, trying city-bearing forms first (`normalize_meta`); cuts every meta description to 160 at a sentence end; emits Organization (with legalName, foundingDate, sameAs, address, areaServed) and the headquarters LocalBusiness on every page from `schema.local`; Service schema on `services/*`, `industries/*`, `products/*`, `brands/*`; BlogPosting on `blog/*`; BreadcrumbList off the home page. Content files carry `schema.short_name`, `title_city`, `cities`, `area_served`, `meta_tail` and `local`. Every page needs a FAQ section; the content file adds one to any page without it. Kelly's build averages 93 with 54 of 55 A; Nexus 90 with 19 of 21 A. Review and AggregateRating are never marked up on self-published testimonials.

### Rules
- The baseline is pulled before the first word of copy, and the seo.json is written the same day as the pulls, while the numbers are fresh.
- Every number in the report is from a pull or the live HTML. Where a pull was not made, the cell says not pulled. No estimates.
- The findings are ranked by what they cost, each with evidence, cost and fix, and each fix is either in the build or on a named day of the plan.
- The redirect map covers every URL in the sitemap: rebuilt, merged, migrated (posts) or retired. Overrides for the money pages are written by hand; the rest is matched by slug.
- The same report is re-run at 30, 60 and 90 days against the same baseline, with `seo_audit.py live` on the launched site.
