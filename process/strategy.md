# Is this the right process to dominate website building?

An honest answer, because the wrong answer here is expensive.

**The core bet is right. The positioning is wrong, and the product isn't finished.**

---

## What's genuinely defensible

Most agencies do one of two things: design from scratch (slow, inconsistent, margin-destroying) or
skin a marketplace template (fast, cheap-looking, licensed). QBS does neither. **Nine themes owned
outright, 57 shared modules, re-skinned per client** is a real third position — and "no licences, no
lock-in, you own it" is a true claim almost nobody else can make.

Three more things that are real:

- **Every page is a `dnd_area`** (12 of 16 templates). "Editable by your team" is verified, not a
  promise. Most agencies deliver a site the client must call them to change.
- **The site and the CRM are the same platform.** This is the actual moat, and it's the one thing a
  design shop cannot copy. A competitor can buy nine themes. They cannot be a HubSpot partner with
  ZoomInfo, Semrush and the CRM already wired.
- **Measurement discipline.** Writing the baseline down before touching anything, and being able to
  prove the delta, is rare and it's what generates referrals.

## Where the strategy is wrong

**"Website design" is a commodity, and commodities race to the bottom.** At $4,950–$14,950 against
Wix, Squarespace, WordPress shops and now AI site builders, price is the only axis and someone will
always be cheaper. You cannot dominate that.

**What you actually sell is the revenue system, and the website is the surface.** Reposition around
the thing nobody else has: *the website that's wired to your pipeline* — forms that land in the CRM
with attribution, meetings booked on a rep's calendar, lifecycle stages that move, content
targeting keywords you're already ranking eleventh for, and a monthly number proving it works.
That's not a website project. That's revenue infrastructure, and it prices like it.

Three consequences:

1. **The one-time fee is a foot in the door, not the business.** Twelve months of retainer on a
   $9,950 build is worth more than the build. The website-services page already promises monthly
   optimisation and there's no product behind it. That's the single biggest gap in the whole system —
   bigger than any theme defect.
2. **Launch at $4,950 is a trap as currently sold.** Our own Semrush data says blog posts drive 82%
   of organic traffic and blog setup starts at Growth. So Launch sells a conversion surface to
   someone who has no traffic to convert. Either say that plainly in the pitch, or stop selling it
   to clients without existing traffic.
3. **Stop competing on speed alone.** Speed is margin, not positioning — capture it internally, don't
   advertise it. "We build fast" invites "so does everyone."

## The tiers are mispriced, and Transform is the problem

Modelled per-page in `process/clientcommand.md`, the effective hourly rate is **$172 for Launch,
$171 for Growth, and $101 for Transform.** The premium tier is the worst business — fifty pages of
page-by-page rewrite earns 40% less per hour than the cheapest tier while occupying five times the
capacity. Price it at **$22–25k** or cut the allowance to 30 pages.

The same model says a **Growth build is ~58 hours across 90 sold days** — 13% work, 87% waiting on
the client. So the constraint on volume is latency, not our throughput, and the lever is running
many builds concurrently rather than each one faster. And a retainer at $2,500/month for 10 hours
is **$250/hour and $30,000/year per client** — 46% better than Growth, 2.5× Transform. That is the
arithmetic behind the point below.

## The product isn't finished, and that gates everything

You cannot dominate on a product line with defects in it. From `process/qa-findings.md`:

- **Five of nine themes fail WCAG AA on button contrast.** An accessibility defect, and in some
  procurement contexts a disqualifier.
- **All nine ship QBS's identity** in schema, header and footer.
- **Eight of nine have never rendered a live page.** They're sold and unproven; a client's site
  would be the first real test.

Fix these before scaling. Selling harder into a broken product line multiplies the problem.

---

## The world you described, and what it takes

> *"I come in and say hey build mockups for so-and-so and boom we're on our way. Then I say build
> the website in HubSpot now."*

That's exactly right, and it's now two commands:

```
/mockups <company>     → evidence, four questions, three directions as a shareable page.
                          Seconds. No HubSpot writes. Nothing to undo.
/build <company>       → clone, re-skin, client schema, gate. Once, after they choose.
```

**The insight that made this possible:** mockups should never have been HubSpot clones. Cloning
three 300-file themes into a live portal to show three directions is slow *and* commits the product
line before anyone agreed to anything. `scripts/mockup.py` renders the same three directions from
the themes' real cached tokens — so the colours and typefaces are what ships, not an approximation —
and the clone happens once, at the end.

That inverts the cost structure. Three options used to be the expensive part of the pitch. Now
they're free, which is what makes the main-page-plus-three shape sustainable on every deal.

### What still stands between you and "boom"

In order:

1. **Content.** Phase 04 is days 30–50 — the longest phase, and it has no method. Design is solved;
   nine themes and twelve tokens. **Copy is the whole remaining bottleneck**, and generic copy is
   now the only "AI slop" tell left. Ground it in the Semrush keywords, the competitor scrapes and
   the client's own language, with the persuasion modules as the outline.
2. **Fix the nine.** Contrast, identity, fonts, and the jQuery portal setting. One approved change,
   every past and future client benefits.
3. **A visual module catalogue.** `all-modules.html` already exists in every theme — screenshot it
   and Phase 03 wireframing (days 20–35) becomes an hour in a client meeting instead of two weeks.
4. **Migration and multi-location.** Both are hard blockers on real clients, and neither exists.
   Clients arrive on WordPress. Practice groups and dealer networks have twelve locations.
5. **The retainer product.** The data pipeline already exists. Wrap it.

### Two things worth building that aren't on the roadmap

**An automated pre-call audit, as the front of the funnel.** You already sell a website grader. The
`verify.mjs` harness plus the four Semrush pulls *is* an audit engine — point it at a prospect's
domain before the call and walk in with "you get N visits a month, one page is stuck at position 11
for keywords worth 1,700 searches, your buttons fail contrast, and 31 pages have no social image."
That's not a pitch, it's a diagnosis, and it sells the tier for you. Same engine, two revenue lines.

**A case-study engine.** Every finished build has a before baseline and an after number. The
`casestudy-*` modules already exist. Generating the case study from the measured delta turns
delivery into pipeline automatically — and proof is what compounds.

---

## The scoreboard to run this on

Not "sites shipped." These:

| Metric | Why |
|---|---|
| Days from kickoff to launch | Fixed price means every day saved is margin |
| Hours per build, by phase | Tells you where the process actually leaks |
| % of builds passing `verify.mjs` first time | Quality without a person watching |
| Retainer attach rate | The annuity. The number that decides whether this is a business or a job |
| Client's organic traffic delta at 90 / 180 days | The only proof that generates referrals |
| Builds per quarter per person | Whether the automation is real |

## The short version

The methodology is sound and unusually honest about itself. The two commands now do what you
described. **Three things decide whether this dominates:** finish the product line, make copy as
systematic as design, and build the retainer — because a website business that sells websites
competes on price, and one that sells a revenue engine doesn't.
