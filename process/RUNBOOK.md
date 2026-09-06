# The runbook

**Eight production phases. Step 1 to 28, in order**, from "we should talk to them" to "launched and
on retainer."

Everything else in this repo explains *why*. This file is *what to do next*. If you read one file,
read this one, and open the others when a step points you at them.

Legend — ⚡ scripted (minutes) · ✋ our hands · ⏳ waiting on the client · 🚦 a gate that can fail

## The eight phases, and how they map to what we sold

The six phases on the website-services page are **commercial** — they own the dates and the client
sees them. These eight are **production** — they own the work. They are not the same list and
conflating them is how estimates go wrong.

| Production phase | Sold phase | Days |
|---|---|---|
| **1 · Diagnose** | 01 Information Gathering | 1–10 |
| **2 · Direction** | 02 Planning | 10–20 |
| **3 · Structure & content** | 03 Wireframing · 04 Content | 20–50 |
| **4 · Build theme, templates, modules** | 05 Design & Build | 45–60 |
| **5 · Build the website** | 05 Design & Build | 55–75 |
| **6 · Run the agents against it** | 06 Test & Review | 70–85 |
| **7 · Launch** | 06 Launch | 85–90 |
| **8 · Optimise** | post-launch | ongoing |

**Phase 4 is the one that was missing.** The nine themes plus a re-skin covers a *standard* site.
The Revolution build needed **29 custom modules, 7 sections and 10 page templates** — a phase the
earlier version of this runbook had no step for, which is exactly why its hour model was optimistic.

---

# Phase 1 · Diagnose — days 1–10

### 1 ⚡ Diagnose their current site
```bash
node scripts/verify.mjs https://<their-domain>
```
**Done when:** you have their failure list. Two minutes, and it's the diagnosis you open with.

### 2 ⚡ Pull the SEO baseline
The four Semrush pulls in `process/seo-baseline.md`.
**Done when:** monthly organic traffic, real top pages, and a striking-distance keyword with volume
are written into the brief. **That traffic number is what the engagement gets measured against.**
New client → **create the Semrush project today**; the crawl takes hours.

### 3 ⚡ Measure their brand
`firecrawl_scrape`, `formats: ["branding"]`, on their site plus two or three competitors.
**Done when:** you have the real accent hex. Never eyeball it off a logo.

### 4 ✋🚦 Confirm the platform can hold the build
Client's HubSpot tier, **and the page cap**. HubSpot's free tier caps site pages at **30**; a
50-page Transform is impossible on it. Also confirm who is paying for the subscription.
**Done when:** the tier is recorded and the page count fits. Finding this in week nine is a refund
conversation.

### 5 ✋ Write the brief
`brands/<slug>.md` from the template. Fill **every** section — each is consumed later. Especially
the **entity facts** (legal name, canonical URL, logo URL, `sameAs`), the **tier**, the **soft
offer**.
**Vertical client?** Load the kit too — `verticals/office-technology.md` for a dealer.
**Done when:** no `<placeholders>` remain.

### 6 ✋ Ask for everything the client owes, once, today
Logo **light and dark**, photography, the gated asset, case-study permissions, portal access.
**Every ask gets an owner and a date.**
**Done when:** the asset rows exist with owners. **The highest-leverage ten minutes in the runbook**
— this is what decides 90 days versus 130.

### 7 ✋ Four questions
Ground · register (which three themes) · the promise in their words · lane.
**Done when:** the promise is in the brief **verbatim**.

---

# Phase 2 · Direction — days 10–20

### 8 ✋ Pick three of nine
Rules in `themes/catalogue.md`: ground from the **brief, not taste** · safe / stretch / wildcard ·
typeface to reading load · never two with the same ground and typeface class.

### 9 ⚡🚦 Render the three
```bash
python3 scripts/mockup.py --client "<Company>" \
    --themes "Quantum <A>,Quantum <B>,Quantum <C>" \
    --accent "#RRGGBB" --brief brands/<slug>.md \
    --roles "The safe one|The stretch|The wildcard" \
    --rationales "<why A>|<why B>|<why C>" --out /tmp/<slug>.html
```
**Gate:** it enforces the selection rules. A warning means the *set* is wrong.
**Done when:** screenshotted at 1440 **and 390**, and looked at. Its first run ever produced three
near-identical options; only looking caught it.

### 10 ✋ Present; they choose
`process/pitch-presentation.md`. Main page first — the evidence — then the three.
**Done when:** the choice **and why, in their words**, is in the brief.

### 11 ✋ Build the URL map
Every trafficked page from step 2: old URL → new URL → **301**.
**Done when:** no trafficked page lacks a destination.

### 12 ✋ Open the plan and the page records
Plan from the tier template. **One record per page** — `process/clientcommand.md`.
**Done when:** N page records exist with template, owner and asset list.

---

# Phase 3 · Structure & content — days 20–50

### 13 ✋ Section every page
Module order from the 57 — plus the vertical kit if there is one. **This is the wireframe**: an
inventory choice, not a drawing. Persuasion order: `pain-bridge` → `is-this-you` →
`cost-of-inaction` → `two-futures` → `why-now`.
**Done when:** every page record has a section list, and card counts check against the balance table
in `design/guardrails.md` — **now**, while it's free to change.

### 14 ⏳🚦 Structure signed off
**Done when:** the page list and section order are agreed in writing. **Attach a default:** "no
reply by Friday means we proceed as drafted."

### 15 ✋ Draft copy, grounded not generated
Every `<h1>` answers a **real keyword** from step 2. Three P's above the fold. Their own language
from step 3.
**Done when:** no page could belong to another company in the category.

### 16 ⏳🚦 Copy approved
Its own step because it's the biggest schedule risk in the engagement. **Batch it** — two scheduled
reviews, not a trickle. **Default that ships.**
**Done when:** approved in writing, per page.

---

# Phase 4 · Build theme, templates, modules — days 45–60

**The phase the nine themes don't cover on their own.** Skip it only if the section list in step 13
is satisfied entirely by existing modules. Reference implementation:
`themes/architecture.md`.

### 17 ⚡🚦 Clone and re-skin the theme
```bash
python3 scripts/reskin.py plan --theme "Quantum <Theme>" --client "<Company>" \
    --accent "#RRGGBB" --ground <light|dark> \
    --org-name "<Legal name>" --org-url "https://<domain>" \
    --org-logo "<url>" --org-sameas "<linkedin>"
```
Show the table to whoever approves portal writes, **wait for a yes**, then
`--apply --approved-by "<name>"`.
**Gate:** four contrast ratios. It refuses to apply a failing re-skin and refuses to touch the nine.

### 18 ✋🚦 Split the accent, if the ground is light
A saturated accent that works as a button fill fails as text. Revolution's amber is **1.86:1 on
white**. Add `accent_ink` (accent text on light) and `accent_lift` (accent text on dark) —
`themes/architecture.md`.
**Done when:** accent text clears 4.5:1 *and* the button still reads as a button. **All five light
Quantum themes need this.**

### 19 ✋ De-brand the header and footer
They hardcode QBS's logo, nav, social links and copyright, and step 17 does **not** fix them. The
better fix, proven on Revolution: make them **field-driven modules**, not hardcoded partials.
**Done when:** nothing in the clone says Quantum Business Solutions. **Nothing goes in front of a
client before this.**

### 20 ✋ Build the modules the section list needs and the 57 don't have
Copy the `quantum-faq` pattern: derived from the module's own fields, `|escapejson` on every value,
schema in the module that renders the content. For a dealer, most of what you need already exists in
Revolution's 29 — **port them, don't rebuild them** (`verticals/office-technology.md`).
**Done when:** every section in step 13 maps to a real module.

### 21 ✋ Build the templates, and know the constraint
Per-page templates. **`layoutSections` populated via the API does not render** — the Revolution
build hit this and had to bake page content into per-page templates instead. Verify before relying
on programmatic `layoutSections`.
**Done when:** every page in the set has a template, and `all-modules.html` renders them all.

---

# Phase 5 · Build the website — days 55–75

### 22 ✋ Build the pages
Real content. No Lorem. One `<h1>`. **Featured image on every page** or `og:image` is absent and
every share renders a bare link. Lazy below the fold, `fetchpriority="high"` on the hero,
`width`/`height` **plus `height:auto`**.
**Done when:** every page record is at *built*.

### 23 ⚡⏳ Generate and place the assets
Higgsfield MCP, `fal.ai` fallback. `design/prompts.md` has the working prompt. **Chosen direction
only.** Generate **blank surfaces** so labels stay real HTML text.
**Done when:** every asset row is filled. Chase the client-owed ones from step 6.

### 24 ✋🚦 Get it renderable
**Draft pages cannot be rendered anonymously** — HubSpot preview links redirect to a login, so no
gate can read them. **Publish temporarily to the `<portal>.hs-sites.com` staging subdomain.**
**Done when:** a URL exists that `verify.mjs` can actually load. Plan for this; it is not optional.

---

# Phase 6 · Run the agents against it — days 70–85

The loop. Each agent has a gate that can fail it — `process/agents.md`.

### 25 ⚡🚦 The automated gate
```bash
node scripts/verify.mjs <staging-url> --expect-org "<Client legal name>"
```
Exit 1 = not done. A11y at three widths, CLS, schema entity, card-grid balance, the mobile floors,
placeholder text, conversion paths, links.
**A failure returns to the station that caused it, not to step 1.** Contrast → step 17/18.
Placeholder text → step 15. Card orphan → step 13.

### 26 ✋🚦 The agents that read what a script can't
- **Quality agent** — `process/checklist.md` end to end, `design/guardrails.md` line by line, and
  **it looks at the screenshots.** Report what you *see*, not what was intended.
- **Fact-check agent** — every client-facing claim about search behaviour, against a dated primary
  source. Returns UNVERIFIABLE rather than inventing a citation.
- **Copy agent** — the three P's per page, `<h1>` against a real keyword.
- **AEO agent** — schema derived from module fields, `Organization` naming the client. Read
  `process/structured-data.md` first so it doesn't overclaim.
- **Adversarial verifier** — tries to disprove each finding, so the list isn't plausible noise.

**Done when:** the loop returns clean twice in a row, and **a human has scrolled every page on a
real phone.** The harness measures; it cannot tell you the design is wrong.

### 27 ✋🚦 Test the money path yourself
Submit a form. Book a meeting. Confirm it lands in the CRM, the thank-you page fires, the asset
arrives. Share one URL into Slack and look at the card.
**Done when:** you have received your own test submission.

---

# Phase 7 · Launch — days 85–90

### 28 ✋ Ship it
301s live and spot-checked **individually** on the top-traffic pages. GA connected, and connected to
the Semrush project. Search Console verified. No stray `noindex` or `nosnippet` — `nosnippet` also
blocks AI Overviews. Remove the staging publish.
**Done when:** live, and the **pre-launch baseline is written down**. No baseline, no proof.

---

# Phase 8 · Optimise — the part that's actually the business

- **Hand over.** Show them how to edit their own `dnd_area`s. Make "editable by your team" true and
  it cuts your support load.
- **Record actual hours per station** and replace the estimates in `process/clientcommand.md`. The
  model is only useful calibrated — and Phase 4 is the one most likely to be wrong.
- **Case study from the measured delta.** Delivery becomes pipeline.
- **The retainer conversation** — a task on the plan with a date, not a hope. $2,500/month at ten
  hours is $250/hr against $171 for the build.
- **Promote what you learned:** a rule → `design/guardrails.md` · a task → the library · a theme
  defect → fix it **at source** so all nine benefit · a vertical pattern → `verticals/`.

---

## The six things that make this fail

1. **No brief.** The model reaches for its defaults and you get slop.
2. **Client-owed assets asked for late.** Step 6 is ten minutes and it decides 90 days versus 130.
3. **No default on approvals.** An open-ended wait has no end.
4. **Skipping step 19.** A client seeing our logo on their site is the worst five seconds in the
   engagement.
5. **Forgetting step 24.** You cannot gate a draft page. Without a staging publish, Phase 6 is
   someone squinting at a logged-in browser.
6. **Treating Phase 4 as free.** Custom modules are real work and the hour model still doesn't
   account for them.

## If you only have an hour

The four that are correctness, not quality: **entity facts in the schema** (17) · **the
header/footer de-brand** (19) · **301s on trafficked URLs** (11, 28) · **`verify.mjs` passing**
(25).
