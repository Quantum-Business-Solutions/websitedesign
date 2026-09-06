# Roadmap: what's worth building next

> **Status — 2026-09-03.** The methodology in this repo is **agreed and adopted.** Build order
> confirmed as **item 1** (scripted clone-and-reskin, carrying the item-5 theme fixes in the same
> approved change) then **item 2** (`scripts/verify.mjs`). Item 7 (the retainer) is the business-changing one
> and follows. The nine-theme writes to portal `20682069` still need explicit approval before they
> execute — propose-then-confirm, per the `qbs-hubspot-private-app` skill.

Ordered by **money per hour of build effort**, not by interest. The system is already good at
deciding what a site should look like. Everything below is about the three things that actually
convert that into profit: **delivery speed**, **provable quality**, and **recurring revenue**.

The economics to keep in view: the packages are **fixed price** ($4,950 / $9,950 / $14,950) over
**90 days**. At fixed price, every hour removed from delivery is margin, and every project finished
early is capacity for the next one. Quality that's *checkable* is what lets us go fast without the
rework that eats the margin back.

---

## 1. Script the clone-and-reskin — the single biggest win

**Today:** `process/reskin.md` is run by hand. Clone a theme in Design Manager, patch `fields.json`,
create pages from 16 page templates, wire the modules. Per direction. Times three.

**Build:** one script that takes a client slug, a theme name and an accent, and returns a preview
URL.

```
reskin.py plan --client "<client>" --theme "Quantum <Theme>" --accent "#..." --ground light
  → clone Quantum <Theme> → <Client> — <Theme>
  → rewrite the NATIVE DIRECTION block in css/quantum.css
  → PATCH base.html with the client's Organization schema   ← fixes the bug in the same pass
  → create pages from the 16 page templates
  → return preview URLs
```

**Why it's first:** it's the step repeated three times per project, it's pure mechanics with no
judgement in it, and it's the reason three options currently feel expensive. Get it to ten minutes
and the three-option pitch in `process/pitch-presentation.md` becomes free — which is the thing that
wins the deal.

It also makes the schema fix **structural** rather than a checklist item someone remembers.

---

## 2. `scripts/verify.mjs` — make quality a command, not a discipline

**Today:** `process/checklist.md` and `process/launch-standards.md` are human discipline. This
repo's own history is the argument: two hand-coded graphics shipped with a written note admitting
they were flat, because nobody looked. Discipline fails under deadline. Deadlines are when it
matters.

**Build:** a Playwright harness — Chromium is already installed here — that loads every page at
three widths and reports pass/fail on:

| Check | Tool | Catches |
|---|---|---|
| Screenshots at 390 / 768 / 1440 | Playwright | Everything visual, at the width clients actually use |
| Accessibility | axe-core | Contrast, labels, tap targets — **and legal exposure** |
| Core Web Vitals | Lighthouse | The LCP and CLS problems measured in `launch-standards.md` |
| JSON-LD validity + **whose name is in it** | parse `ld+json` | The nine-theme Organization bug |
| `og:image` present | head parse | Blank social cards |
| Lazy-loading, `width`/`height` | DOM scan | CLS and LCP contention |
| Placeholder text | regex | Lorem, "TODO", `example.com`, unfilled tokens |
| Broken links, orphan pages | crawl | The dead ends Semrush found |
| Forms actually submit | Playwright | The untested form that silently loses every lead |

Everything on that list is already documented as a manual check. Automating it costs one build and
pays on every project forever — and it's what lets a junior ship at senior quality.

**Sell it too.** This is the "Grade your Website" grader, pointed inward. Same engine, two revenue
lines: a lead magnet and an internal QA gate.

---

## 3. Kill the content bottleneck — it's the real long pole

Look at the phase durations: **Content Writing is days 30–50, and Design & Build is 45–75.** Design
is nine themes and twelve tokens; that problem is solved. **Copy is what the 90 days is actually spent
on**, and it's the least systematised part of the process.

**Build:** a copy pass that is *research-grounded* rather than generated from nothing —

- **Semrush keywords** (`process/seo-baseline.md`) decide what each page must rank for, so the `<h1>`
  matches real search intent instead of a slogan
- **Competitor scrapes** (Firecrawl) establish category language, and what to deliberately avoid
- **The client's own words** from the interview and their existing site — the fastest route to a
  voice that isn't generic
- **The persuasion modules as the outline**: `pain-bridge` → `is-this-you` → `cost-of-inaction` →
  `two-futures` → `why-now`. The section order *is* the argument, which is why a hero that fails the
  three-P test usually needs a missing module, not better adjectives

This is where "doesn't look like AI slop" is won or lost now. The design already doesn't. Generic
copy is the remaining tell.

---

## 4. The URL migration map — insurance against the expensive disaster

**Why:** on QBS's own domain, articles are **82% of organic traffic**. A redesign that changes blog
URLs without 301s deletes most of a client's traffic, and they will — correctly — blame us. One
occurrence costs more than this is worth building.

**Build:** pull the client's ranking pages from Semrush and their sitemap, diff against the new
sitemap, and emit a 301 map plus a hard **fail** on any page with traffic that has no destination.
Runs in Phase 02 as a plan, and again in Phase 06 as a gate.

Small build. Prevents the one mistake that turns a happy client into a refund.

---

## 5. Fix the nine themes at source

**The single reconciled list is in `themes/architecture.md`.** Awaiting approval. Specified across `process/structured-data.md` and
`process/launch-standards.md`; item 5 is specified in `themes/catalogue.md` and `process/reskin.md`.
The single reconciled list lives in `themes/architecture.md`; this is the summary:

1. **`seo` field group + fail-safe `Organization`** — stops nine themes asserting a false identity
2. **Fonts via `<link>` + `preconnect`, or self-hosted woff2** — removes the CSS `@import` chain;
   biggest Core Web Vitals win available
3. **`loading="lazy"` default with an above-the-fold toggle**, `fetchpriority="high"` on heroes
4. **`width`/`height` passthrough** on image modules
5. **The light-theme contrast failure** — `accent_ink` / `accent_lift`, per `themes/architecture.md`

One approved change, every past and future client benefits. This is the whole argument for never
forking themes per client, and it's cheap.

---

## 6. A visual module catalogue — the wireframing phase, collapsed

**The unlock is already there:** every theme ships `templates/all-modules.html`. Screenshot that page
per theme and you have a visual library of all 57 modules in nine skins, for free.

**Why it matters:** Phase 03 Wireframing is days 20–35. With a visual catalogue, wireframing becomes
*"pick these nine sections in this order"* in a client meeting — an hour, not two weeks. It also
makes the three-option pitch richer at no cost, and gives sales something to show without a designer
in the room.

---

## 7. Productise the retainer — this is where the actual money is

Everything above sells one-time work at $4,950–$14,950. **The annuity is post-launch.** The
website-services page already promises monthly optimisation, and only Transform includes a
time-bounded window. There's no recurring product.

The data pipeline for it already exists — `process/seo-baseline.md` re-pulled monthly gives the
trend, the next striking-distance keyword, and audit regressions. Wrap that in a monthly report plus
a fixed number of CRO/content hours and it's a retainer that costs little to deliver because the
analysis is automated.

Two reasons it's the highest-value item on this list even though it's last:

- **Recurring beats one-time.** Twelve months of retainer on a $9,950 build is likely worth more than
  the build.
- **It's how the promise gets kept.** "Continuously optimize based on real behaviour" is currently
  unfalsifiable. With a written baseline and a monthly pull, it's provable — and provable results are
  what generate referrals and case studies, which is what fills the pipeline.

---

## Also worth doing, lower down

- **Figma as an input.** Clients hand over Figma files (Revolution did). The API exposes real fills,
  type styles and variables — more precise than scraping a rendered page.
- **Structured intake → brief.** Phase 01 is days 1–10, mostly chasing assets and answers. A HubSpot
  form that populates `brands/<slug>.md` compresses it.
- **Accessibility as a sellable line item.** WCAG conformance is a real procurement requirement and
  a real liability. `axe-core` is already in item 2; the differentiator is offering a conformance
  statement rather than hoping nobody asks.
- **Reusable proof assets.** Logo strips, stats bands and case-study layouts get rebuilt per client.
  A proof kit per vertical would cut Phase 05.
- **Bound the revisions.** Phase 05 is sold as "refined with your feedback at every step" with no
  round cap, no change-order trigger and no meeting cadence written down anywhere. On fixed price
  that is where the margin goes. "Conversion architecture" now has a definition in
  `process/launch-standards.md` (offers mapped to funnel stage, two paths per page, sticky CTA,
  inline meetings, real thank-you page) — what it still lacks is a *quantity*.
- **Define "blog setup."** It's a Growth line item and the traffic engine, and no document says what
  it includes — instance, templates, authors, categories, how many seeded posts, written by whom.
  A client starting from zero content has no branch in the process at all.
- **Phase exit criteria.** Six phases with dates, an output column, and no definition of done.
  Phase 03 is sold as "layout agreed before design" with no agreement artifact; Phase 06's output is
  "signed-off build" with no signature.
- **Re-test the page-counting rule.** `process/clientcommand.md` decided it (one template plus N
  instances = one page), but if `layoutSections` really cannot be populated by API then N instances
  means N hand-written templates and the rule is a promise the platform cannot honour. Settle it.

---

## If only two get built

**Item 1** (scripted re-skin) and **item 2** (`scripts/verify.mjs`). Together they make the three-option pitch
cheap and the quality gate automatic — speed and provable quality, which are exactly the two things
a fixed-price business runs on. Item 5 rides along with item 1 for almost nothing.

Then **item 7**, because that's the one that changes the business rather than the delivery.
