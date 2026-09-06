# The SEO baseline: what to pull from Semrush, and what it means

We have Semrush, with **13 projects** already configured — QBS plus twelve clients. That makes an
evidence-based traffic baseline a ten-minute job per client instead of guesswork, and it turns
"we'll improve your SEO" into "here are the four pages to fix and what they're worth."

This file is the method, worked through on QBS's own domain so the numbers are real.

---

## The four pulls, in order

Run these in Phase 01 Information Gathering, before the interview. They cost API units, so don't
re-run what you already have.

| # | Report | Toolkit | Question it answers |
|---|---|---|---|
| 1 | `domain_rank` | overview | How much organic traffic exists today? The **baseline** |
| 2 | `domain_organic_unique` | organic | Which pages earn it? Usually not the ones the client thinks |
| 3 | `domain_organic` | organic | Which keywords, at what position, at what difficulty? The **quick wins** |
| 4 | `info` (site audit) | siteaudit | What's technically broken? Needs a project ID |

Discovery pattern for all of them: call the toolkit tool → `get_report_schema` → `execute_report`.
Site audit needs `list_projects` first to get the project ID.

---

## Worked example: thequantumleap.business

### 1. The baseline

```
Organic keywords: 153    Organic traffic: 146/mo    Traffic value: $348/mo
Semrush rank: 3,234,724  Paid keywords: 0
```

146 organic visits a month. That's the honest starting number, and it's the one to write down —
**you cannot prove an optimisation window worked without it.**

### 2. Which pages earn it — the finding that reframes everything

| Page | Keywords | Traffic | Share |
|---|---|---|---|
| `/blog/lead-scoring-criteria-healthcare-industry` | 3 | 67 | **45.9%** |
| `/blog/msp-sales-team-structure-best-practices` | 1 | 34 | **23.3%** |
| `/connectandsell-the-definitive-guide` | 12 | 13 | 8.9% |
| `/` (home) | 12 | 12 | 8.2% |
| `/blog/how-to-evaluate-auto-dialers…` | 9 | 11 | 7.5% |
| `/blog/msp-marketing-successful-strategies-for-2026` | 30 | 6 | 4.1% |
| `/blog/how-to-build-a-sales-friendly-website` | 1 | 2 | 1.4% |

**Blog posts drive 82% of organic traffic. No service page earns any.**

> And BrandCommand's critic scores `blog` at **67.4** — worst of eleven asset types by eighteen
> points. The asset that produces the traffic is the one we produce worst. See
> `process/agents.md`.

The remaining 18% is the homepage (8.2%) and `/connectandsell-the-definitive-guide` (8.9%) — and
that second one is a guide, not a service page. Every actual service page earns zero.

The page that *sells websites* — `/website-services`, the most designed page on the site — earns
**zero organic traffic.** It isn't in the top fifteen. Nor are `/revops-services` or
`/sales-blitz-as-a-service`: they appear with one keyword and no visits.

Two consequences, and they're the reason this file exists:

- **Beautiful service pages don't generate traffic; articles do.** Service pages convert traffic
  that arrives from somewhere else. Both matter — but they are different jobs, and only one of them
  is a design job.
- **The blog is the traffic engine, and it's a Growth-tier line item.** "Blog setup" starts at
  $9,950. So a **Launch client at $4,950 buys a beautiful site with no traffic engine at all.**
  That is not a reason to discount Launch — it's a reason to *say so in the pitch*, honestly:
  Launch is a conversion surface for traffic you already have. If a client has no traffic and no
  blog, Launch will not fix it, and selling it as though it will produces an unhappy client in
  month four.

### 3. The quick wins — striking distance

Positions **11–20** are the money. A page at 11 is on page 2, getting almost nothing, one or two
places from page 1 where clicks actually happen. Sort by volume, filter to low difficulty:

| Keyword | Pos | Volume | KD | Page |
|---|---|---|---|---|
| `msp marketing strategy` | **11** | 590 | 11 | `/blog/msp-marketing-…-2026` |
| `msp marketing ideas` | **11** | 480 | 12 | same page |
| `marketing strategy for msp` | 14 | 390 | 22 | same page |
| `marketing strategies for msp` | **11** | 260 | 14 | same page |
| `best marketing agencies for msps` | 20 | 90 | 6 | same page |
| `hubspot chat` | 33 | 1,000 | 38 | `/resources/how-to-set-up-hubspot-chatflows…` |

**One page is parked at positions 11–14 across four keywords worth ~1,720 monthly searches, at
difficulty 11–22** — three of them at position 11 (1,330 searches) plus one at 14. It earns 6
visits. It has 30 ranking keywords and converts almost none of them
into traffic, because page 2 is invisible.

Moving that single page into the top five is worth more than every other SEO task on the domain
combined. It needs no new content — it needs the existing page improved: depth, internal links,
title and intent match.

Contrast it with `/blog/lead-scoring-criteria-healthcare-industry`: **3 keywords, position 1, 67
visits.** Fewer keywords, far more traffic. **Position beats coverage.** A page ranking first for
three terms beats a page ranking eleventh for thirty. Consolidate and push one page up rather than
spraying new posts.

Also worth noticing: `sales-ready website` sits at position 7 with **difficulty 1**, and
`fractional cso services` at 7 with **difficulty 1**. Difficulty 1 and not in the top three means
nobody is trying. Those are afternoons, not projects.

### 4. The technical audit

Project `30166247`, 99 pages crawled (of ~374 in the sitemap — the crawl limit is 100, so **the
audit only sees a quarter of the site**).

```
Site Health 83%     AI Search Score 94
https 100 · internal SEO 100 · performance 97 · linking 93 · markups 100 · crawlability 92
5 errors · 132 warnings · 83 notices
```

Healthy overall. The four findings that matter:

**a) 17 of 24 checked pages carry no structured data at all.**
```
structuredData.groupByPages: { noItems: 17, valid: 7, invalid: 0 }
items: ORGANIZATION 9 valid · FAQ 5 · SITE_NAMES 2 · SITELINKS_SEARCH_BOX 2
```
Nothing invalid — what exists is correct. It's just missing from 71% of pages, which is exactly
what `process/structured-data.md` predicted from the source: one module of fifty-seven emits schema.

Note also that the ORGANIZATION markup is valid on 9 pages — that's the hardcoded QBS block, confirmed
live and indexable. On a client build those 9 valid blocks would all be naming the wrong company.

**b) Semrush's "markups: 100" score is measuring validity, not coverage.** A perfect markup score
alongside 17 pages with no markup at all. Don't hand a client a 100 and call schema done — read
`groupByPages`, not the thematic score.

**c) 66 temporary redirects out of 99 crawled URLs.** 73 of the 99 are redirects; only 26 return
200. So three-quarters of the 100-page crawl allowance is spent on URLs that aren't destinations. Temporary (302) redirects don't pass authority the way permanent
(301) ones do, and they burn crawl budget on URLs that aren't destinations. Converting the 66 to
301s is a settings-level fix with no design work.

**d) Google Analytics is not connected** (`gaStatus: NOT_CONNECTED`), and one page has **zero
internal incoming links** — orphaned, reachable only by sitemap.

Also: of 26 live pages, 17 have a canonical tag — so about 9 don't. HubSpot injects canonicals, so
these are worth checking individually rather than assuming a platform bug.

---

## The client projects

Already configured, so a baseline is one call each. All have `siteaudit` and `tracking`; a few add
more.

| Project | Domain | ID |
|---|---|---|
| Quantum Business Solutions | thequantumleap.business | `30166247` |
| DaVinci Laboratories | davincilabs.com | `2404557` |
| Nexus | nexusnt.com | `29671106` |
| Aztec Office | aztecoffice.com | `30543931` |
| Pacific Office Automation | pacificoffice.com | `27023205` |
| CCI Voice | ccivoice.com | `29958940` |
| OEM Connect | oemconnect.com | `29903134` |
| Pet Tech Labs | pettechlabs.com | `26682595` |
| CCG Marketing | ccgms.com | `29449457` |
| CCG Promo | ccgpromo.com | `29449458` |
| CCG Home | home.corpcomm.com | `29449429` |
| CCG Be Decorating | bedecorating.com | `29449459` |
| CCG Be Boxing | beboxing.com | `29449460` |

Re-run the `list_projects` report (inside the `projects_research` toolkit — it is a report name, not
a tool name) rather than trusting this table; projects get added.

**A new client has no project, so pull 4 is blocked on day one.** Pulls 1–3 work on any domain
without a project — run those first. Creating the site-audit project is a manual step in the Semrush
UI (Projects → Add new project → enter domain → enable Site Audit), and the crawl takes hours, so
**start it on day one of Phase 01** or the audit won't be ready when Phase 02 needs it. Check plan
headroom before promising it: 13 projects are already configured.

---

## What this changes in the process

### Phase 01 — the baseline becomes evidence, not a promise

Record in `brands/<slug>.md`:

- Organic traffic, keyword count, traffic value — **the number we're measured against**
- Top five pages by traffic, and whether they're articles or service pages
- Striking-distance keywords: position 11–20, volume > 100, difficulty < 30
- Site Health and the specific errors

Then the pitch stops being "we'll improve your SEO" and becomes *"you get 146 visits a month; one
blog post is stuck at positions 11-14 for four keywords worth ~1,720 searches; here's what fixing it is
worth."* That is a much easier thing to sell and a much easier thing to be held to.

### Phase 02 — traffic reality picks the page types

If the client's traffic comes from articles, the build has to protect the articles. **A redesign
that changes blog URLs without 301s destroys the only traffic they have** — which on this domain
would mean losing 82% of it. Check the top-pages report *before* planning the sitemap, every time.

### Phase 06 — the launch gate

- Every URL that changed has a **301** — not a 302
- Top-traffic pages re-checked post-launch; rankings held
- GA connected to the Semrush project so post-launch data has somewhere to land
- Baseline written down. **No baseline, no proof the optimisation window worked** — and the
  optimisation window is what Transform charges for

### Post-launch — where growth-driven design gets its inputs

Monthly: re-pull `domain_rank` for the trend, `domain_organic` filtered to positions 11–20 for the
next quick win, and the audit `info` for regressions. That's the data behind "continuously optimize
based on real behaviour" instead of an unfalsifiable claim.

---

## Two rules

1. **Never quote a Semrush thematic score to a client without reading what's underneath it.** The
   markups score here is 100 while 71% of pages have no markup. Scores measure validity; clients
   hear coverage.
2. **Write the baseline down before you touch anything.** It's the only thing that makes the
   post-launch work provable, and it takes one call.
