# The SEO and AEO analysis: the method, the pulls, the ranking, the page

`process/seo-baseline.md` is the four-pull baseline. This is the full analysis: what a prospect
sees on the hub before they have chosen a direction, and what the engagement is measured against
at 30, 60 and 90 days. Worked through on Van Ausdall & Farrar (2026-09-08); the numbers below are
theirs.

**Time budget: 25 minutes of a subagent, 5 minutes to render.** Two subagent passes, at most
12 and 14 Semrush reports, then `scripts/seo_report.py` turns the two JSON files into the report
and `preview.py` puts the top findings on the hub. Nothing is hand-typed twice.

---

## Why this earns the meeting

Brian Courtney (VAF) said it on 1 September: the president has noticed the company not
appearing in search, competitors are outpacing them, and the current partner sends reports but
no advice. The analysis answers all three in numbers before anyone asks, and it names the
competitor who is winning (Leap, number 1 for `managed it services indianapolis`, 1,000 a month).
That is the difference between "we do SEO" and "here is what it is costing you".

## Pass one: the baseline (12 Semrush reports)

| # | Report | Toolkit | Question it answers |
|---|---|---|---|
| 1 | `domain_rank` | overview | Traffic, keywords, value. **The baseline** |
| 2 | `domain_organic` (top 50 by traffic) | organic | Which terms, at what position. Branded share |
| 3 | `domain_organic_unique` | organic | Which pages earn it. Usually the home page and one blog post |
| 4 | `domain_organic_organic` | organic | Who competes. Keep only the same-category, same-state domains |
| 5 to 8 | `domain_rank` for four competitors | overview | Their traffic and keyword footprint against the client's |
| 9 | `domain_domains` gap, client vs two strongest | organic | Terms they rank for and the client does not |
| 10 | `phrase_these` on the head terms | keyword | Volume, difficulty, CPC for the terms the pages will target |
| 11 to 12 | `backlinks_overview`, client and two competitors | backlinks | Whether authority is the gap or pages are |

Firecrawl in the same pass: scrape the home page (title, H1, schema, og:image, scripts, lazy
loading, forms), the sitemap (URL count, patterns, PDFs), and two live SERPs for the head terms.

## Pass two: depth (14 Semrush reports)

| # | Report | Question |
|---|---|---|
| 1 to 7 | `phrase_related` per pillar seed | The cluster each page has to answer, with volumes |
| 8 to 11 | `phrase_questions` per pillar | The questions that become FAQ items, marked up as `FAQPage`. **This is the AEO half** |
| 12 to 13 | `domain_organic_unique` for two competitors | Which URL patterns earn: service pages, city pages, blog |
| 14 | `backlinks_refdomains` for the client | The strongest referring domains, to know what is defensible |

Firecrawl in pass two: a page-level audit of ten client pages (title length, city in title, meta
length, H1, H2 count, schema types, FAQ present, og:image, word count); the same for the two
competitors' money pages plus pricing, reviews and form-above-fold; eight live SERPs phrased the
way a buyer asks an assistant; `robots.txt` for AI crawler rules and the sitemap declaration; a
reviews search to see which sources and ratings appear next to the name.

## The ranking rubric

Every finding gets one of four severities, decided by what it costs, not by how technical it is:

| Severity | Test |
|---|---|
| **Critical** | Leads or the headquarters market are being lost today, or a competitor already owns the client's core term |
| **High** | A term with real volume and low difficulty has no page, or a whole page type earns nothing |
| **Medium** | A page exists and underperforms for a fixable reason: title, schema, thin copy, query-string URLs |
| **Low** | Hygiene that costs a little every month: og:image, meta length, crawler rules |

Each finding is four sentences: **evidence** (with the number), **impact** (what it costs),
**action** (what the build or the 90-day plan does), and a title under 70 characters. Ten to
fourteen findings, ranked by impact. The top five go on the hub; all of them go on the report.

## The output contract

Two JSON files, one per pass. `scripts/seo_report.py` renders whatever exists, so a partial pull
still produces a page.

`<slug>-seo.json`: `summary_stats` (four `[value, label]` pairs), `competitors`, `opportunities`,
`technical`, `backlinks`, `implications`.

`<slug>-seo-deep.json`: `clusters`, `questions`, `competitor_pages`, `backlinks`, `page_audit`,
`competitor_audit`, `ai_visibility`, `robots`, `reviews`, `findings`.

Both files are kept in `brands/` as the record (`<slug>.seo.json`, `<slug>.seo-deep.json`), and
the markdown companions beside them. The rendered page lives in the client repo as
`seo-report.html`, linked from the hub's Search section.

```bash
python3 scripts/seo_report.py --basic brands/<slug>.seo.json --deep brands/<slug>.seo-deep.json \
    --client "<Client>" --domain <domain> --accent "#RRGGBB" --as-of "8 September 2026" \
    --prepared-for "<Name>" --out /path/to/<client-repo>/seo-report.html
```

The content file's `pitch.search` block carries `report_href`, `today_stats`, `today`, `after`,
`keep` and, when the deep pass exists, `findings` (the top five, copied from the JSON at build
time). The hub renders the findings as ranked cards above the today/after lists.

## What the analysis must never do

- Estimate a number a tool did not return. Write "not pulled".
- Call something broken without opening it. The VAF form "placeholder" was a hidden honeypot
  field; the real finding was no CRM integration.
- Promise rankings or traffic. Promise the inputs and the re-measurement.
- Recommend a direction. The analysis ranks problems; the client chooses the design.
- Mark up self-published testimonials as `Review` or `AggregateRating`.

## The VAF worked example, in numbers

- 1,081 organic visits a month, 365 keywords, about 80% branded, home page 85% of traffic.
- Four Indiana competitors at 1,555 to 2,094 visits from 1,058 to 2,711 keywords. Authority Score
  21 against 24 and 27, so authority is level and pages are the gap.
- `managed it services indianapolis` 1,000 a month, KD 29: Leap number 1, VAF not in the top 100.
  `managed print services` 4,400 a month, KD 16, and `copier lease` 2,400, KD 19: no VAF page.
- `business phone systems` 9,900 a month at position 25 through a Fort Wayne city page, with no
  competitor in the top 100.
- 324 of 586 sitemap URLs are `blog?p=` query-string posts; one Organization schema block and
  nothing else; og:image a stock file.
- Leap's copier brand at 9 for `copier lease indianapolis`, VAF at 10.

## What would make it better next time

1. **Semrush project on day one.** Site Audit and Position Tracking need a project; without them
   the technical half is Firecrawl only.
2. **Search Console access before the meeting.** Impressions and AI Overview appearances are
   first-party; everything above is modelled.
3. **Google Business Profile insights.** For a multi-office dealer, the map pack is most of the
   local volume and none of it shows in Semrush.
4. **A competitor page teardown per pillar**, not per company: their managed IT page against ours,
   their copier page against ours, word for word.
5. **Re-run monthly, automatically.** The two passes are subagent prompts; a routine that re-runs
   them on the first of the month and diffs the findings is the retainer's evidence.

## Added 8 September: the whole-site half

The two passes above sample ten pages. The full analysis now also crawls every page (171 for
VAF), scores each with `scripts/site_audit.py`, and renders three more sections on the report:
**Why the competitors are winning** (a side-by-side schema and depth table against the two
strongest competitors), **Highest leverage moves** (five, each tagged build or plan), and
**Whole site, every page**. A blog sample (40 posts, same parser) and a social and entity check
(sameAs, YouTube, LinkedIn, Google Business Profile, via Firecrawl search when the sandbox cannot
load the profiles) each get a section with stats, findings and actions. The report renderer takes
`--full` and `--csv-href` for the whole-site block; the blog and social blocks live in the deep
JSON as `blog` and `social`. See `process/page-for-page.md` for how the same score is applied to
the build so the hub can show today against the rebuild, page by page.
