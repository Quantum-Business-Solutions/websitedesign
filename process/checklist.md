# Pre-ship checklist

Run end to end before anything reaches a client. Adapted from a 7-point process by **AIS (AI
Automation Society)** — the creator of the `scroll-craft` skill — cross-checked against what's
actually held up on QBS builds.

His framing was for bespoke standalone pages. QBS runs two lanes, and the checklist weights
differently across them, so each item says where it bites.

---

### 1. Brand guidelines — logo, colours, consistency

*Both lanes.* Every colour traceable to the brief or to measured tokens. No invented hexes. Logo at
correct clear-space, and legible on whichever ground the theme uses.

**Catch:** all nine themes ship `appearance.mode: dark` regardless of whether they're light themes.
Set it explicitly, every time.

### 2. The three P's — Pain, Person, Promise

*Both lanes, and the one that most often fails.* Above the fold, can a visitor answer: what problem
is this for, am I the person, and what's being promised? If the hero could belong to any company in
the category, it's not done.

This is the question the interview asks and cannot infer.

### 3. Scroll feedback and responsiveness

*Lane B primarily.* The visitor should feel they're driving. Scroll-linked motion, sections that
respond, state that changes under the wheel.

*Lane A caveat:* a HubSpot theme is a document, not a film. Don't bolt scroll theatrics onto a
multi-page site — it fights the CMS and ages badly. Save it for the signature page.

### 4. Inspiration from real sites, not thin air

*Both lanes.* Name the reference before you build. From `design/references.md`, or ingest a new one
via `/design-inbox` → `/design-ingest`.

**Take the technique, not the frame.** Cloning a competitor's page shape wholesale is how you end up
with their design and your logo. And per the sourcing rules in `design/guardrails.md`, gallery
images don't get stored here — ingest the live site.

### 5. Components — reuse, don't reinvent

*Lane B primarily.* 21st.dev for component prompts, motion-primitives for animated backgrounds. See
the sourcing routes in `design/references.md`.

*Lane A caveat:* **the nine themes already are the component system.** Importing outside components
into a theme fragments it. Fix the theme at source instead, so every future client benefits.

### 6. Mobile — actually look at it

*Both lanes.* Load it at phone width and scroll the whole thing. Most slop survives desktop review
and dies on mobile: hero type too large, tables overflowing, motion that stutters, tap targets too
small.

### 7. Verification loop — screenshot and iterate on what you see

*Both lanes.* Screenshot the build, look at it, fix what's actually wrong. Repeat.

This is the highest-value habit on the list, and it is the one most often skipped. In this repo's own
history: two hand-coded attempts at a 3D graphic shipped with a written note admitting they were
flat, when a single honest look would have said "this reads as SmartArt, wrong medium." Looking is
not optional, and neither is acting on what you see.

`scroll-craft` automates this — it screenshots its own scroll and verifies at every position.

**Also validate the structured data**, which no screenshot will show you:

- [Google Rich Results Test](https://search.google.com/test/rich-results) on home, one blog post,
  one case study, one interior page, pricing
- [validator.schema.org](https://validator.schema.org) for spec correctness
- **Read the rendered `<head>` and confirm the `Organization` block names the client.** All nine
  themes currently hardcode QBS's identity there — see `process/structured-data.md`. Until that's
  fixed at source, this check is the only thing standing between a client and a site that declares
  itself to be Quantum Business Solutions.

### 8. The launch gate — found and capturing, not just correct

*Both lanes.* Gorgeous is half the job. Full baseline in `process/launch-standards.md`:

- **PageSpeed Insights** on home, one interior, one blog post — **mobile** scores; desktop hides the
  real problems
- **Share one URL into Slack or LinkedIn** and look at the preview card. That's the `og:image`
  check, and it takes ten seconds
- **Submit a form and book a meeting yourself**, end to end — submission lands in the CRM, thank-you
  page fires, asset arrives
- **Two conversion paths on every page**: a hard offer for the ready buyer, a soft offer for the 95%
  who aren't ready today
- Lazy-loading below the fold, `fetchpriority="high"` on the hero, `width`/`height` on every image
- Analytics baseline captured **before** launch — no baseline, no way to prove the optimisation
  window worked
- **Every changed URL has a 301, not a 302.** Check the top-traffic pages from
  `process/seo-baseline.md` individually. On QBS's own domain, articles are 82% of organic traffic —
  losing their URLs in a redesign would cost more than the build is worth

---

## Then the tooling gate

- `/impeccable critique` — UX and hierarchy
- `/impeccable audit` — accessibility, responsive, performance
- `design/guardrails.md` — read line by line against the build

A direction that trips a guardrail does not go to the client. Failing the gate is cheap; a client
rejecting a direction is not.
