# The agent roster

Which agent to deploy, at which step, and what stops it being confidently wrong.

## The one rule

**An agent with no gate is a confident guesser.** Every producing agent below is paired with
something that can *fail* it: a script with an exit code, a measured token, a written constraint, or
a named human. **Build the gate before the agent that feeds it** — an ungated agent produces work
someone has to review by hand, which is slower than doing it.

Step numbers refer to `process/RUNBOOK.md`.

| Column | Means |
|---|---|
| **Deploy** | The runbook step(s) it runs at |
| **Gate** | What can fail its output |
| **Fails at** | What it gets *confidently* wrong. The most useful column here |
| **Status** | ✅ has a working gate today · ⚠️ gate is partial · ⛔ no gate yet — don't deploy unsupervised |

---

## What already exists in BrandCommand — don't rebuild it

Three agents are live, with a **critic pattern already implemented**: `agent_runs` carries a
`critic_score` and `critic_feedback` per output, and `agent_learnings` accumulates reinforced
findings per brand. That is the same idea as the gates in this file, built first and running in
production.

| Agent | Produces | Model | Scored? |
|---|---|---|---|
| **`campaign-director`** | `campaign_plan` | Sonnet / Gemini 2.5 Pro | **never** |
| **`campaign-launcher`** | 13 asset types — `linkedin_post`, `landing_page`, `blog`, `call_script`, `email_blast`, `direct_mail`, `ad_copy`, `video_script`, `case_study`, `one_pager`, `presentation`, `lead_magnet` | Sonnet / Gemini 2.5 Pro | mostly |
| **`crm-ops`** | `crm_audit` | Gemini 2.5 Pro | n/a |

**Reuse these, don't duplicate them.** `campaign-launcher` already writes landing-page copy, case
studies, video scripts and blogs — which overlaps the Copywriter agent below. The right split:
`campaign-launcher` for campaign assets, the Copywriter agent for *site* pages where the `<h1>` has
to answer a keyword from the baseline. Same skill, different gate.

### The critic scores say something worth acting on

Mean score by asset type, from live runs:

| Asset | Mean | Worst | n |
|---|---|---|---|
| `video_script` | 88.0 | 88 | 3 |
| `email_blast` | 87.8 | 87 | 5 |
| `linkedin_post` | 87.2 | 81 | 27 |
| `direct_mail` | 84.7 | 81 | 7 |
| `landing_page` | 84.0 | 69 | 9 |
| `one_pager` | 83.3 | 81 | 3 |
| `call_script` | 82.7 | 72 | 7 |
| `case_study` | 82.5 | 82 | 2 |
| `ad_copy` | 80.6 | 73 | 5 |
| `presentation` | 71.0 | 71 | 1 |
| **`blog`** | **67.4** | **56** | 7 |

**Blog is the worst asset type by eighteen points** — 67.4 against 85.1 for everything else, and it
has never once scored above 79.

That matters more than it looks. `process/seo-baseline.md` found that **blog posts drive 82% of
QBS's organic traffic**, and `verticals/office-technology.md` found the same category-wide. So **the
one asset that produces the traffic is the one the system produces worst** — measured by QBS's own
critic, not by opinion.

Two consequences: blog is where a dedicated agent earns the most, and no blog should ship on a
score under 80 until that changes.

### Three defects in the existing setup

1. **`campaign-director` output is never scored.** Every `campaign_plan` row has
   `critic_score: null`. The plan that everything downstream is generated *from* is the one thing
   nothing checks. That is the highest-leverage gate to add anywhere in the stack.
2. **`lead_magnet` and some `ad_copy` runs have a null score too** — the critic doesn't run
   consistently, so a null means "not checked", not "fine".
3. **The learning loop reinforces zero-signal findings.** The one row in `agent_learnings` reads:

   > *"B has the highest reply rate: 0%"* — `confidence: 1`, `times_reinforced: 4`

   A learning that the best variant is the one at 0% is worse than no learning, and maximum
   confidence means it will be trusted. **It needs a minimum-sample gate** before a finding is
   written, and confidence should scale with sample size rather than defaulting to 1.

### Model discipline

Runs are split across `claude-sonnet-4`, `gemini-2.5-pro` and `google/gemini-2.5-pro` — two
spellings of one model — for the *same* asset types. That makes the critic scores hard to attribute:
you cannot tell whether a 56 on a blog is the prompt or the model. **Normalise the identifier and
record it, then the scores become an A/B test you already paid for.**

---

## Squad 1 · Intake — days 1–10

### Diagnostic agent
**Role:** Produce the measured failure list for a prospect's current site — the thing you open the
conversation with.
**Expertise:** WCAG 2.2 AA, Core Web Vitals, the mobile floors, structured-data validity.
**Deploy:** step 1 · **Tools:** `scripts/verify.mjs` · **Gate:** exit code ✅
**Fails at:** contrast over a hero image or a scrim — axe reports that as *incomplete*, not a
violation, and the harness currently drops incompletes. Treat a clean contrast result on an
image-backed hero as unproven.

### SEO baseline agent
**Role:** Establish the number the engagement gets measured against.
**Expertise:** Semrush report shapes, striking-distance analysis, branded-vs-commercial keyword
separation.
**Deploy:** step 2 · **Tools:** Semrush MCP · **Gate:** the four pulls exist in the brief ⚠️
**Fails at:** reading branded traffic as demand. On a dealer, most volume is the company's own name
plus job seekers — see `verticals/office-technology.md`. It will also quote a Semrush thematic score
as if it meant coverage; it doesn't.

### Brand extraction agent
**Role:** Measure the client's real design tokens rather than eyeballing them off a logo.
**Expertise:** Firecrawl `branding` output, roled-colour interpretation.
**Deploy:** step 3 · **Gate:** every value traceable to a measurement — **no invented hexes** ✅
**Fails at:** extractors mislabel *state* colours as base colours. Two token files in this repo prove
it (`stripe.json` has its text colours swapped; `linear.json` reports black on black). Always
sanity-check against the live page.

### Competitive intelligence agent
**Role:** Establish what the category actually looks like, so differentiation is deliberate.
**Deploy:** step 3 · **Gate:** two or three competitors genuinely ingested ⚠️
**Fails at:** treating the client's self-declared competitors as the real set. Use
`semrush_competitors` as well as what they said.

### Brief agent
**Role:** Assemble `brands/<slug>.md` so every later step has its input.
**Deploy:** step 8 · **Gate:** no `<placeholders>` remain, and a human has read it ⚠️
**Fails at:** filling a gap with something plausible. **A visible gap is correct output**; a
confident half-sentence is not.

---

## Squad 2 · Direction — days 8–20

### Direction agent
**Role:** Choose three of the nine — safe, stretch, wildcard.
**Expertise:** `themes/catalogue.md` selection rules; ground filtered by the brief, not taste.
**Deploy:** step 10 · **Gate:** `mockup.py` exits non-zero on a set-level violation ✅
**Fails at:** picking by aesthetic preference. Ground comes from the brief — the rule that would
have caught the Revolution "Ink" mistake.

### Mockup agent
**Role:** Render the three directions and publish the pitch.
**Deploy:** step 11 · **Tools:** `scripts/mockup.py`, Artifact
**Gate:** exit code, plus screenshots at 1440 **and** 390 that a human looks at ✅
**Fails at:** shipping without looking. Its own first run produced three near-identical options.

---

## Squad 3 · Content — days 20–50 · the long pole

### Information architecture agent
**Role:** Pick the module order per page from the 57. This *is* the wireframe.
**Expertise:** the module inventory; the persuasion sequence `pain-bridge` → `is-this-you` →
`cost-of-inaction` → `two-futures` → `why-now`.
**Deploy:** step 16 · **Gate:** card-grid balance at three widths ✅
**Fails at:** inventing a layout instead of choosing from the inventory. Also: when a grid orphans,
ask first whether the odd item is *different in kind* — often it is, and it should span
(`design/patterns.md`).

### Copywriter agent
**Role:** *Site* page copy — distinct from BrandCommand's `campaign-launcher`, which owns campaign
assets. **The highest-value agent to build**, and the live critic scores agree: `blog` averages
**67.4** against 85.1 for every other asset type, while blog posts drive 82% of organic traffic. — 15 of the 43 page hours, and the only
remaining "AI slop" tell now that design is systematised.
**Expertise:** the three P's; the client's own language; the target keyword per page.
**Deploy:** step 18 · **Gate:** placeholder text and heading structure ✅ · the three P's and
keyword alignment ⛔ *human reads it*
**Fails at:** genericness that passes every automated check. One `<h1>`, no placeholders, real
words — and copy that could belong to any company in the category. **That failure has no gate. Read
it.**
- **Hard rule:** no em dashes, ever, in anything the visitor reads. The gate fails the page on one (`no em dashes in copy`). Rewrite with a comma, a colon or a new sentence.

### Claims agent
**Role:** Verify that every number on the page traces to a source.
**Expertise:** the `proof_points` block in the brief.
**Deploy:** step 19 · **Gate:** ⛔ **none automated — this is a human step with an agent assisting**
**Fails at:** this is the failure. Ask an agent for a first-call fix rate it cannot find and it will
write "98%". One `<h1>`, no placeholders, contrast fine, **exit 0** — and the client publishes a
fabricated SLA. **The only step in the process with legal exposure.**

### Compliance content agent
**Role:** Draft privacy policy, terms, cookie-consent copy, form consent language, and the
accessibility statement.
**Deploy:** step 21 · **Gate:** 🔒 **the client's counsel sees the legal text.** We draft; they own
it ⚠️
**Fails at:** writing jurisdiction-specific legal text with confidence. It drafts a starting point,
never a final position.

---

## Squad 4 · Build — days 30–75

### Theme agent
**Role:** Clone, re-skin, split the accent, write the client's `Organization` schema — one pass.
**Expertise:** the native-direction block; the twelve tokens; `accent_ink` / `accent_lift`.
**Deploy:** steps 22–23 · **Tools:** `scripts/reskin.py`
**Gate:** four blocking contrast ratios; refuses to touch the nine; refuses a portal mismatch ✅
**Hard limits:** 🔒 never `--apply` without the change table approved by the named person from step 6.
Never the QBS token against a client portal.
**Fails at:** nothing much — this is the best-gated agent in the set. But it does **not** fix the
header and footer, and it will report so on every run.

### Module developer agent
**Role:** Build the modules the section list needs and the 57 don't have.
**Expertise:** HubL, the `quantum-faq` pattern — derived from the module's own fields, `|escapejson`,
schema in the module that renders the content.
**Deploy:** step 25 · **Gate:** the gate at step 31, plus a human reading the field definitions ⚠️
**Fails at:** dropping the thing that made the original work. Revolution's `process-steps` module
lost its `produces` field and its outcomes band in the port — the diagram shipped, the argument
didn't.

### Template agent
**Role:** Page templates.
**Deploy:** step 26 · **Gate:** every page renders; `all-modules.html` renders them all ⚠️
**Fails at:** assuming `layoutSections` populated by API will render. Settle that question first —
it decides whether this step costs 8 hours or 40.

### Page build agent
**Role:** Build the pages: real content, correct image handling, featured images.
**Deploy:** step 27 · **Gate:** `verify.mjs` ✅
**Fails at:** forgetting the featured image, which makes `og:image` absent and every social share a
bare link. It's missing on 31 of 41 pages of QBS's own site.

---

## Squad 5 · Assets

### Art direction agent — stills
**Role:** Hero and section imagery.
**Expertise:** `design/prompts.md` — name the material not the look, specify the light rig, name a
renderer, demand blank faces.
**Deploy:** step 28 · **Tools:** Higgsfield MCP, `fal.ai` fallback
**Gate:** **blank surfaces** so every label stays real HTML text; then `verify.mjs` for `srcset`,
dimensions and `og:image` ⚠️
**Fails at:** two things, both earned here. **Don't approximate a render** — flat SVG or CSS polygons
where the reference is 3D produce SmartArt. And **stop after two failed attempts** and write a brief
instead of iterating a third time.
**Cost discipline:** check `balance`, preflight with `get_cost`, and render for the **chosen**
direction only.

### Video agent
**Role:** Hero background loops, brand films, explainers, testimonial cutdowns.
**Expertise:** Seedance / Higgsfield video models; aspect and duration per placement; a still poster
frame that carries the message on its own.
**Deploy:** step 28, **only when the direction calls for it.** A hero video is a real performance
cost and often the wrong answer.
**Gate:** the video QA agent below ⚠️
**Fails at:** generating video with **baked-in text** (unreadable by search, untranslatable,
un-editable), generating in the wrong aspect for the placement, and generating before the direction
is chosen. Also: video is the single biggest LCP risk on a page — it must never be the LCP element.

### Video QA agent
**Role:** Gate every video before it reaches a page. Separate from the video agent on purpose —
nothing should approve its own output.
**Checks:**
- **Never autoplays with sound.** Muted, `playsinline`, and a visible pause control
- **A `poster` frame exists** and reads correctly on its own, because most visitors see only that
- **Not the LCP element** — the poster is an image and the video loads after
- **Duration and file size** appropriate to a background loop (seconds, not minutes)
- **Correct aspect per breakpoint**, and no letterboxing on mobile
- **Captions or a transcript** for anything with speech — WCAG 1.2.2, and it is also indexable text
- **No baked-in text** in the frame
- **`prefers-reduced-motion` respected** — a looping background must be stoppable
**Deploy:** step 31–32 · **Gate:** ⛔ **not yet implemented in `verify.mjs`.** Manual today; the
checks above are the spec for building it.
**Fails at:** passing a video that looks fine on a fast desktop and destroys mobile LCP.

### Asset optimisation agent
**Role:** `srcset` / `<picture>`, intrinsic dimensions plus `height:auto`, format and compression,
`fetchpriority` on the hero, lazy below the fold.
**Deploy:** step 27–28 · **Gate:** `verify.mjs` responsive-images and dimensions checks ✅
**Fails at:** adding `width`/`height` while an inline CSS `height:100%` overrides the derived aspect
ratio, which reserves nothing. Needs `height:auto` too.

---

## Squad 6 · Search — AEO and SEO

### AEO / SEO expert agent
**Role:** Everything that decides whether the site is found and cited.
**Expertise, and the honest version of it:**
- **Structured data:** derived from module fields, `|escapejson`, `Organization` on the home or
  about page **only** (site-wide is what produced "ORGANIZATION 9 valid" in our own audit),
  `WebSite` home-page only, `BreadcrumbList` site-wide
- **What still earns a visible rich result:** `Event` unreservedly. `BreadcrumbList` desktop-only
  since Jan 2025. `Product`/`Offer` needs a single-product page. `Article` is an enhancement, not a
  rich result. `Service` earns nothing visible. **FAQ rich results were fully retired 7 May 2026**
- **What actually moves AEO**, per Google's own May 2026 guidance: markup that agrees with visible
  text · genuinely useful non-commodity content · off-site brand presence · real author attribution.
  **Structured data is explicitly *not* required** for generative AI search
- **Technical:** `nosnippet` also blocks AI Overviews · the retrieval crawlers are `OAI-SearchBot`,
  `Claude-SearchBot`/`Claude-User` and `PerplexityBot` (**not** `GPTBot` or `ClaudeBot`, which are
  training) · `Google-Extended` governs Gemini training, not AI Overviews · Search Console's
  Generative AI report is the only first-party AI-visibility data that exists
**Deploy:** steps 18 (keyword alignment), 21, 31, and monthly at 37
**Gate:** `verify.mjs` JSON-LD parse and the `--expect-org` assertion ✅ · keyword alignment ⛔
**Fails at:** **overclaiming.** It will offer FAQ rich results, sell `Service` schema as a visible
win, promise a ranking position, and cite `llms.txt`. Read `process/structured-data.md` before
deploying it, and never let it promise a *position* — sell the inputs.

---

## Squad 7 · QA — the loop

These review across a build. Their value is that **they are not the agent that produced the work.**

### Accessibility agent
**Deploy:** step 31 · **Tools:** axe-core at 390/768/1440, plus the mobile floors
**Gate:** exit code ✅ · **Fails at:** dropping axe's `incomplete` results, which is exactly where
contrast-over-imagery lives.

### Performance agent
**Deploy:** step 31 · **Expertise:** LCP, **INP** (the likely real weak spot on HubSpot — jQuery in
the head, and it's a *portal setting* not a theme fork), CLS, the font `@import` chain.
**Gate:** CLS ✅ · LCP and INP ⚠️ — use PageSpeed Insights for real field timing.

### Quality / craft agent
**Role:** `process/checklist.md` end to end, `design/guardrails.md` line by line, **and it looks at
the screenshots.**
**Deploy:** step 32 · **Gate:** ⛔ human judgement, by design
**Its one instruction:** *report what you see, not what was intended.* This repo's own history is the
argument — two hand-coded graphics shipped with a written note admitting they were flat, because
nobody looked.

### Fact-check agent
**Role:** Every client-facing claim about **external** behaviour — search, platforms, standards —
against a dated primary source.
**Deploy:** step 32 · **Gate:** a citation with a date, or **UNVERIFIABLE**. Never an invented one ✅
**Justified by result:** a fact-check pass on this repo found the FAQ deprecation three years stale,
the searchbox retirement off by a year, "302s don't pass authority" as folklore Google reversed in
2016, an *inverted* AEO priority list, and four places overstating a Google penalty that doesn't
exist.

### Conversion agent
**Role:** Two paths per page — a hard offer and a soft offer — inside `<main>`, not the footer.
**Deploy:** step 31–33 · **Gate:** `verify.mjs`, now scoped to `<main>` ✅
**Fails at:** counting a site-wide footer as an on-page offer. That was a real bug here.

### Adversarial verifier
**Role:** Try to disprove each finding the others produced.
**Deploy:** step 32 · **Why:** it's what stops a review being a list of plausible-sounding
non-problems. Cheap, and it has already earned its place in this repo.

---

## Squad 8 · Launch and after

### Migration / redirect agent
**Role:** The URL map and the 301s. Includes WordPress oddities — `/?p=123`, feeds, category and tag
archives, attachment pages.
**Deploy:** steps 14 and 35 · **Gate:** ⚠️ every trafficked page has a destination; **301 not 302**
**Fails at:** missing the patterns that don't appear in a sitemap. On our own domain, articles are
82% of organic traffic — losing their URLs costs more than the build is worth.

### Launch readiness agent
**Role:** Walk the pre-flight list — TTL dropped, rollback written, 301s spot-checked, integrations
re-tested, staging removed, no stray `noindex`, sitemap resubmitted.
**Deploy:** step 35 · **Gate:** 🔒 going live is the client's call ⚠️

### Monitoring agent
**Role:** The 48-hour watch — 404 spike, forms actually arriving, coverage errors, live CWV.
**Deploy:** step 36 · **Gate:** 48 hours clean ⚠️

### Reporting / calibration agent
**Role:** Monthly Semrush re-pull against the baseline, the next striking-distance target, audit
regressions — **and record actual hours per station.**
**Deploy:** step 37 and monthly
**Why it matters most:** every hour figure in this repo is an estimate. **This agent is the only
thing that changes that.**

---

## Deployment map

| Step | Agents |
|---|---|
| 1–3 | Diagnostic · SEO baseline · Brand extraction · Competitive intelligence |
| 4–7, 9 | *none — 🏢 QBS and 👤 CLIENT* |
| 8 | Brief |
| 10–11 | Direction · Mockup |
| 12–13, 15 | *none* |
| 14 | Migration / redirect |
| 16 | Information architecture |
| 17, 20 | *none — 👤 CLIENT approval* |
| 18 | Copywriter · AEO/SEO (keyword alignment) |
| 19 | Claims *(human-led)* |
| 21 | Compliance content · AEO/SEO |
| 22–23 | Theme |
| 24 | *none — 🏢 QBS* |
| 25–26 | Module developer · Template |
| 27–28 | Page build · Art direction · Video · Video QA · Asset optimisation |
| 29–30 | *none — 🏢 QBS* |
| 31 | Accessibility · Performance · Conversion · AEO/SEO |
| 32 | Quality · Fact-check · Adversarial verifier |
| 33–36 | Launch readiness · Monitoring |
| 37 | Reporting / calibration |

## Build order for the agents themselves

1. **The gates first.** Most exist. Don't add an agent until its gate does.
2. **Copywriter** — biggest bottleneck, clearest partial gate.
3. **Video QA** — the spec above is written; implement it in `verify.mjs` before the video agent
   ships anything to a client page.
4. **AEO/SEO** — small, and it closes a sold promise.
5. **Quality + fact-check** — cheap, and both have already proved their worth here.
6. **Module developer and page build** — last, because they write to a live portal.

## Three things no agent does alone

1. **A write to a live portal.** Propose-then-confirm, with a **named** human yes.
2. **A claim about the client.** Any number on their site is theirs to confirm.
3. **A claim about what Google does.** A dated primary source, or UNVERIFIABLE.
