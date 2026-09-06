# Speculative mockups as an outbound motion

> *"So-and-so has an outdated website. Let's get the three options in front of them and build it out."*

This is the strongest strategic consequence of making mockups free, and it is a different business
from the one described in `process/strategy.md`.

## Why it works now and didn't before

Every agency says "we'd love to redesign your site." Nobody shows up with it **already done**.

The reason nobody does it is cost: speculative design work is a gamble against a low reply rate. But
`scripts/mockup.py` renders three directions from cached tokens in **seconds**, off a Firecrawl scrape
of the prospect's own site plus four Semrush pulls. Total marginal cost per prospect: **a few minutes
and no HubSpot writes.**

That changes the arithmetic completely. At near-zero cost per prospect, speculative work stops being
a gamble and becomes a volume channel — and it is a channel nobody else can run, because it depends
on owning nine finished themes and a scripted re-skin.

## What the prospect receives

The existing pitch artifact, unchanged: one main page plus three directions
(`process/pitch-presentation.md`). What makes it land cold rather than creepy is that **every claim
on the main page is measured, about them:**

- Their **real traffic number** — "you get 340 organic visits a month"
- Their **own top pages**, which is usually a surprise. Most owners think their service pages drive
  traffic; the data almost always says a blog post does
- A **striking-distance keyword** with its volume — "one page is at position 12 for a term with 800
  searches a month"
- Their **measured brand colours**, applied to all three directions, so it is visibly *their* site
- Named **competitors**, ingested, with one line on what the category looks like

Then three directions, in their colours, in real typefaces.

**The subject line writes itself and the credibility is pre-loaded.** They are not evaluating whether
we can design. They are choosing between three.

## Qualify before you render

Free to produce is not free to send — a badly targeted one wastes the reply. Three filters, all
measurable before any work:

1. **Their site is genuinely dated.** Run `verify.mjs` against it. A site with failing contrast, no
   `og:image`, unlazy images and no structured data gives you a diagnosis, not an opinion.
2. **There is traffic to protect.** `domain_rank` plus `domain_organic_unique`. A prospect with real
   organic traffic has something to lose and something to gain; a prospect with none needs content,
   which is a different sale — see the Launch-tier trap in `process/strategy.md`.
3. **They're a HubSpot fit.** Already on HubSpot, or on WordPress and complaining about it. The moat
   is that the site and the CRM are one platform; a prospect who doesn't want that isn't ours.

## The play, end to end

| Step | What happens | Cost |
|---|---|---|
| 1 | Pick a target list — `semrush_competitors` on existing clients finds lookalikes in a category we already understand | minutes |
| 2 | `verify.mjs` their current site → **the diagnosis** | 2 min |
| 3 | Four Semrush pulls → **the baseline** | 3 min |
| 4 | `firecrawl_scrape` `formats:["branding"]` → **their colours** | 1 min |
| 5 | `mockup.py` → three directions in their brand | 1 min |
| 6 | Publish, send the link | 1 min |
| 7 | Reply → the call is a **design review**, not a discovery call | — |

Step 7 is the whole point. A discovery call is us asking questions. A design review is them making
choices — a completely different conversation, and one that starts from "which of these" rather than
"why should we."

## Rules

1. **Never imply we were hired.** These are unsolicited concepts and the page should say so plainly.
   One line: *"Unsolicited — we build these to show what's possible. Nothing here is final."*
2. **Never reproduce their existing site.** Show *our* directions in *their* brand. Rebuilding their
   current design and calling it a redesign is the one version of this that reads as a stunt.
3. **The diagnosis must be accurate.** If `verify.mjs` says their contrast fails, quote the ratio. A
   wrong technical claim in a cold email is worse than no email — and it's the only part of this a
   prospect can check instantly.
4. **Don't send it to a competitor's client mid-engagement.** Judgement call, but the category is
   small.
5. **Cap the volume per category.** Nine themes means three-of-nine sets repeat. Sending near-identical
   direction sets to five firms in one town destroys the effect for all five.

## Where it fits the funnel

This sits **before** the catalogue → proposal → plan chain in `process/clientcommand.md`. A won
speculative pitch enters that chain at "proposal," with the brief and baseline already written —
which means the outbound work is not wasted even when the deal is slow: it *is* Phase 01.

That's the compounding property. Every speculative mockup that converts arrives with Phase 01
already done.
