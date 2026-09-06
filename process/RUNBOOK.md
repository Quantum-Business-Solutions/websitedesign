# The runbook

**Step 1 to step 24, in order, from "we should talk to them" to "launched and on retainer."**

Everything else in this repo explains *why*. This file is *what to do next*. If you only ever read
one file, read this one, and open the others when a step points you at them.

Each step says: **who**, **what**, **the command if there is one**, and **done when**.

Legend — ⚡ scripted (minutes) · ✋ our hands · ⏳ waiting on the client · 🚦 a gate that can fail

---

## Phase 01 · Information gathering — days 1–10

### 1 ⚡ Diagnose their current site
```bash
node scripts/verify.mjs https://<their-domain>
```
**Done when:** you have their failure list — contrast, tap targets, `og:image`, schema, mobile.
This is the diagnosis you open the conversation with, and it costs two minutes.

### 2 ⚡ Pull the SEO baseline
The four Semrush pulls in `process/seo-baseline.md`: `domain_rank`, `domain_organic_unique`,
`domain_organic`, and the site audit if a project exists.
**Done when:** you have their monthly organic traffic, their real top pages, and a striking-distance
keyword with its volume. **Write the traffic number down. Everything gets measured against it.**
**If they're a new client, create the Semrush project today** — the crawl takes hours.

### 3 ⚡ Measure their brand
`firecrawl_scrape` with `formats: ["branding"]` on their site, plus two or three competitors.
**Done when:** you have their real accent hex. Never eyeball it off a logo.

### 4 ✋ Write the brief
`brands/<slug>.md` from `brands/_template.md`. Fill **every** section — each one is consumed by a
later step, and a gap here is a blocked step in week six. Especially: the **entity facts** (legal
name, canonical URL, logo URL, `sameAs`), the **tier**, and the **soft offer**.
**Done when:** the template has no `<placeholders>` left. If they have no gateable asset, that is a
scope item — raise it now.
**Vertical client?** Load the vertical kit too — `verticals/office-technology.md` for a dealer.

### 5 ✋ Ask for everything the client owes, once, today
Logo (light **and** dark), photography, the gated asset, case-study permissions, HubSpot access.
**Every ask gets an owner and a date.**
**Done when:** the asset rows exist with owners. This step is why builds hit 90 days or 130 — it is
the highest-leverage ten minutes in the whole runbook.

### 6 ✋ Four questions, one conversation
Ground (light/dark) · register (which three themes) · the promise, in their words · lane.
**Done when:** the brief records the promise **verbatim**. It is the one thing you cannot infer.

---

## Phase 02 · Planning — days 10–20

### 7 ✋ Pick three of nine
Selection rules in `themes/catalogue.md`: ground filtered by the **brief, not taste** · one safe,
one stretch, one wildcard · match the typeface to the reading load · never two with the same ground
and typeface class.
**Done when:** three named themes with a one-line rationale each.

### 8 ⚡🚦 Render the three directions
```bash
python3 scripts/mockup.py --client "<Company>" \
    --themes "Quantum <A>,Quantum <B>,Quantum <C>" \
    --accent "#RRGGBB" --brief brands/<slug>.md \
    --roles "The safe one|The stretch|The wildcard" \
    --rationales "<why A>|<why B>|<why C>" \
    --out /tmp/<slug>.html
```
**Gate:** it enforces the selection rules. A warning means the *set* is wrong — fix it, don't
override it.
**Done when:** you've screenshotted it at 1440 **and 390** and looked. Its first run ever produced
three near-identical options; only looking caught it.

### 9 ✋ Present, and let them choose
`process/pitch-presentation.md`. Main page first — the evidence — then the three.
**Done when:** the choice **and why, in their words**, is in the brief. The rejected two are worth
as much as the winner.

### 10 ✋ Build the URL map
Every page with traffic (step 2) gets a row: old URL → new URL → 301.
**Done when:** no trafficked page lacks a destination. Skipping this is how a redesign deletes the
only traffic they have.

### 11 ✋ Set up the plan and the page records
Plan from the tier template — six phases, library tasks. **One record per page**, per
`process/clientcommand.md`.
**Done when:** N page records exist, each with a template, an owner and an asset list.

---

## Phase 03 · Wireframing — days 20–35

### 12 ✋ Section every page
Pick the module order from the 57. **This is the wireframe** — an inventory choice, not a drawing.
The persuasion modules are the argument: `pain-bridge` → `is-this-you` → `cost-of-inaction` →
`two-futures` → `why-now`.
**Done when:** every page record has a section list. Check card counts against the balance table in
`design/guardrails.md` **now**, while it's free to change.

### 13 ⏳ Get the structure signed off
**Done when:** they've agreed the page list and section order in writing. **Attach a default:** "no
reply by Friday means we proceed as drafted."

---

## Phase 04 · Content — days 30–50 · the long pole

### 14 ✋ Draft copy, grounded not generated
Every page: the `<h1>` answers a **real keyword** from step 2. Three P's above the fold — what
problem, am I the person, what's promised. Use their own language from step 3.
**Done when:** no page could belong to another company in the category.

### 15 ⏳🚦 Copy approved
Its own step because it's the biggest schedule risk in the engagement.
**Batch it** — two scheduled reviews, not a trickle. **Attach the default that ships.**
**Done when:** approved, in writing, per page.

---

## Phase 05 · Design & build — days 45–75

### 16 ⚡🚦 Clone and re-skin
```bash
python3 scripts/reskin.py plan --theme "Quantum <Theme>" --client "<Company>" \
    --accent "#RRGGBB" --ground <light|dark> \
    --org-name "<Legal name>" --org-url "https://<domain>" \
    --org-logo "<url>" --org-sameas "<linkedin>"
```
Read the table. **Show it to whoever approves portal writes and wait for a yes.** Then add
`--apply --approved-by "<name>"`.
**Gate:** four contrast ratios. It refuses to apply a failing re-skin, and refuses to touch the
nine.
**Done when:** `<Company> — <Theme>` exists in draft.

### 17 ✋ De-brand the header and footer
They hardcode QBS's logo, nav, social links and copyright, and step 16 does **not** fix them.
`process/reskin.md` has the two options.
**Done when:** nothing in the clone says Quantum Business Solutions. **Nothing goes in front of a
client before this.**

### 18 ✋ Build the pages
Real content. No Lorem. One `<h1>`. Featured image on **every** page or `og:image` is absent and
every share renders a bare link. Lazy below the fold, `fetchpriority="high"` on the hero,
`width`/`height` **plus `height:auto`**.
**Done when:** every page record is at *built*.

### 19 ⚡⏳ Generate the assets
Higgsfield MCP, `fal.ai` as fallback. `design/prompts.md` has the working prompt. **Chosen
direction only.** Generate **blank surfaces** so labels stay real HTML text.
**Done when:** every asset row is filled. Chase the client-owed ones from step 5.

---

## Phase 06 · Test, review, launch — days 75–90

### 20 ⚡🚦 Run the gate
```bash
node scripts/verify.mjs <preview-url> --expect-org "<Client legal name>"
```
Exit 1 = not done. Checks a11y at three widths, CLS, schema entity, card-grid balance, the mobile
floors, placeholder text, conversion paths, links.
**Done when:** exit 0. A failure goes back to the station that caused it, not to step 1.

### 21 ✋🚦 Look at it — mobile first
Open `verify-out/` screenshots. **Then load it on a real phone and scroll the whole thing.**
Then desktop. The harness measures; it cannot tell you the design is wrong.
**Done when:** you have personally scrolled every page on a phone.

### 22 ✋🚦 Test the money path yourself
Submit a form. Book a meeting. Confirm it lands in the CRM, the thank-you page fires, the asset
arrives. Share one URL into Slack and look at the preview card.
**Done when:** you've received your own test submission. A form nobody tested loses every lead
silently.

### 23 ✋ Launch
301s live and spot-checked on the top-traffic pages individually. GA connected, and connected to
the Semrush project. Search Console verified. No stray `noindex` or `nosnippet`.
**Done when:** live, and the **pre-launch baseline is written down**. No baseline, no proof.

---

## After launch — the part that's actually the business

### 24 ✋ Hand over, then convert
- Show them how to edit their own `dnd_area`s. "Editable by your team" is a real deliverable —
  make it true and it cuts your support load.
- Record the build's **actual hours per station** and replace the estimates in
  `process/clientcommand.md`. The model is only useful once it's calibrated.
- Generate the case study from the measured delta.
- **Have the retainer conversation.** It's a task on the plan with a date, not a hope. $2,500/month
  at ten hours is $250/hr against $171 for the build.
- Promote what you learned: a rule → `design/guardrails.md`, a task → the library, a theme defect →
  fix it **at source** so all nine benefit.

---

## The five things that make this fail

1. **No brief.** The model reaches for its defaults and you get slop.
2. **Client-owed assets asked for late.** Step 5 is ten minutes and it decides whether you finish in
   90 days or 130.
3. **No default on approvals.** An open-ended wait has no end. "No reply by Friday means we proceed."
4. **Skipping step 17.** A client seeing our logo on their site is the worst five seconds in the
   engagement.
5. **Nobody looked at it on a phone.** Steps 20 and 21 are different steps for a reason.

## If you only have an hour on a build

The four that are correctness, not quality: **entity facts in the schema** (step 16) ·
**the header/footer de-brand** (17) · **301s on trafficked URLs** (10, 23) · **`verify.mjs`
passing** (20).
