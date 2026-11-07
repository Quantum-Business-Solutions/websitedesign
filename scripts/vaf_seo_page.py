#!/usr/bin/env python3
"""Client-facing SEO and AEO scorecard page for ClientCommand: where each page started, what the audit said to change,
what was done, and where it stands. Reusable: reads brands/<brand>.seo-compare.json (scripts/vaf_seo_compare.py) and writes markdown.

    python3 scripts/vaf_seo_page.py > brands/vanausdall.seo-scorecard-page.md
"""
import collections, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "brands/vanausdall.seo-compare.json"), encoding="utf-8"))
OLD, NEW = D["old_summary"], D["new_summary"]
SHORT = {
    "Add a five-question FAQ marked up as FAQPage": "FAQ",
    "Add question-form H2s that an assistant can quote (what, how much, is it)": "question headings",
    "Add Service schema (or Article on case studies) declaring what the page offers": "Service markup",
    "Add Indianapolis or the service city to the title": "city in title",
    "Add Review or AggregateRating schema from real Google reviews": "reviews",
    "Write at least 300 words of body copy; 600 to 900 for a service page": "thin copy",
    "Give every image descriptive alt text": "image alt text",
    "Deepen to 600 words or more": "deeper copy",
    "Structure the page with at least two H2 sections": "H2 structure",
    "Write a 70 to 160 character meta description that answers the query": "meta description",
    "Retitle to 30 to 60 characters": "title length",
}
GRADE = lambda s: "A" if s >= 85 else "B" if s >= 70 else "C" if s >= 55 else "D" if s >= 40 else "F"
pairs = D["pairs"]
recs = collections.Counter(r for p in pairs for r in p["old"]["recommendations"])
by_new = {}
for p in pairs:
    by_new.setdefault(p["new_url"], []).append(p)
mx = lambda a, b: f"{a} to {b}"

o = []
w = o.append
w(f"""# SEO and AEO scorecard: where each page started, what we changed, where it stands

Every page was scored on the same 17 checks before and after: title, city in title, meta description, one H1, H2 structure, question headings, word count and depth, FAQ markup, Service or Article markup, LocalBusiness markup, review markup, image alt text, internal links, canonical, share image and a form or phone number. The old site was crawled on 8 September 2026 ({OLD['pages']} pages). The rebuild was scored live on 29 October 2026 ({NEW['pages']} pages; the old pages that merged are redirected to their nearest new page).

## The headline

The average page score went from **{OLD['avg_score']}** to **{NEW['avg_score']}** out of 100. On the old site {OLD['grades']['A']} pages earned an A and {OLD['grades']['D'] + OLD['grades']['F']} were a D or an F. On the rebuild every page earns an A.

| Measure | Old site | Rebuild |
|---|---|---|
| Average score | {OLD['avg_score']} | {NEW['avg_score']} |
| Pages graded A | {OLD['grades']['A']} | {NEW['grades']['A']} |
| Pages graded D or F | {OLD['grades']['D'] + OLD['grades']['F']} | 0 |
| Pages with FAQ markup | {OLD['faq']} | {NEW['faq']} |
| Pages with Service markup | {OLD['service']} | {NEW['service']} |
| Pages with breadcrumb markup | {OLD['breadcrumb']} | {NEW['breadcrumb']} |
| Pages with customer-comment (Review) markup | {OLD['review']} | {NEW['review']} |
| Titles naming the city | {OLD['city_in_title']} | {NEW['city_in_title']} |
| Pages under 300 words | {OLD['thin']} | {NEW['thin']} |
| Pages with a question heading | {OLD['question_headings']} | {NEW['question_headings']} |
| Images missing alt text | {OLD['images_no_alt']} | {NEW['images_no_alt']} |

## What we told you in September

The original analysis (Semrush and a live crawl, 8 September 2026) found:

- vanausdall.com ranked for 365 keywords and earned about 1,081 organic visits a month. About 80 percent of the keywords were searches for the company name, and the home page carried 85 percent of the traffic.
- The four closest Indiana competitors earned 1,555 to 2,094 visits a month from 1,058 to 2,711 keywords. The gap was missing pages, not authority: VAF's Authority Score was 21 against 24 to 27.
- The most valuable local searches, "managed it services indianapolis" (1,000 a month) and "it support indianapolis" (880 a month), did not show VAF in the top 100.
- The old site had FAQ markup on 4 pages, Service markup on 3, no breadcrumb or review markup, 68 pages under 300 words, and 170 images without alt text.
- In AI answers VAF was absent for "best managed it services indianapolis" and for the "largest office technology provider in Indiana" claim it makes on its own home page.

## What the audit said to change, and what we did

| What the audit said | Pages flagged | What we did | Status |
|---|---|---|---|
| Add a five-question FAQ with FAQPage markup | {recs[list(SHORT)[0]]} | A FAQ with matching markup on every page. {NEW['faq']} of {NEW['pages']} pages. | Done |
| Add question headings an assistant can quote | {recs[list(SHORT)[1]]} | Question headings on {NEW['question_headings']} of {NEW['pages']} pages; the few utility pages without one are forms and policies. | Done |
| Add Service markup, or Article on case studies | {recs[list(SHORT)[2]]} | Service markup on {NEW['service']} service and city pages, Article markup on the {NEW['article']} case studies. | Done |
| Put the city in the title | {recs[list(SHORT)[3]]} | {NEW['city_in_title']} of {NEW['pages']} titles name the city. | Done |
| Write real copy where pages were thin | {recs[list(SHORT)[5]]} | No page under 300 words. Eight utility pages stay under 600 on purpose; padding them would hurt. | Done |
| Give every image alt text | {recs[list(SHORT)[6]]} | Every image has descriptive alt text. | Done |
| Add Review markup from real reviews | {recs[list(SHORT)[4]]} | Review markup on {NEW['review']} pages, from VAF's own after-service survey comments (word for word). No ratings are invented. | Needs VAF: Google reviews |
| Titles, descriptions and headings | 9 | Unique titles under 60 characters and descriptions under 160 on every page. One H1 per page. | Done |

## By page type

| Type | Old (pages, average) | Rebuild (pages, average) |
|---|---|---|""")
for t, v in sorted(OLD["by_type"].items()):
    n = NEW["by_type"].get(t, {})
    w(f"| {t} | {v['pages']}, {v['avg']} | {n.get('pages', 0)}, {n.get('avg', '')} |")
w("""
## Also checked beyond the score

- **Structured data.** Every block parses. Organization, LocalBusiness, WebSite, FAQPage, Service, BreadcrumbList, Article, BlogPosting and Review are present where they belong, with no repeated declarations. Two gaps remain and both need VAF: the Evansville street address, and publish dates for the 18 case studies.
- **Blog.** 335 posts keep their original publish dates, each with a summary, breadcrumb and BlogPosting markup and links to the matching service pages. 233 carry a TL;DR and a FAQ whose markup matches the visible text; press releases, event notices and dated posts (about 100) were left as they were.
- **Redirects.** Every old page has a new address (see the redirect map page).
- **Figures.** 342 sentences with figures were checked against the old site: 332 match what VAF already published, 10 contain a number VAF has to confirm. The Net Promoter Score was corrected to the audited 92.8. The claim "Indiana's largest" was reworded to "one of Indiana's largest independently owned" because only that version has an outside source.

## What is left, and who does it

| Item | Why | Who |
|---|---|---|
| Review markup on the other pages | The only reviews VAF has are the after-service survey comments, shown on 31 pages. No Google reviews exist yet and we do not invent ratings. | VAF: claim the Google Business Profile and ask survey promoters for a review |
| Evansville street address | Not published anywhere we could find | VAF |
| Case study dates | Article markup works best with a publish date | VAF |
| Rankings and AI-answer baseline | Measured after launch so it reflects the live site | QBS, December |

## Page by page
""")
TYPES = [("service", "Service pages"), ("city", "Location pages"), ("company", "Company pages"), ("case study", "Case studies"), ("policy", "Policies")]
for t, label in TYPES:
    rows = sorted((p for p in pairs if p["new"] and p["new"]["type"] == t), key=lambda p: p["old_url"])
    w(f"\n### {label} ({len(rows)} old pages)\n")
    w("| Old page | New page | Before | What the audit said | Now |\n|---|---|---|---|---|")
    for p in rows:
        said = ", ".join(SHORT.get(r, r) for r in p["old"]["recommendations"]) or "nothing major"
        w(f"| {p['old_url']} | {p['new_url']} | {p['before']} ({GRADE(p['before'])}) | {said} | {p['after']} ({GRADE(p['after'])}) |")
print("\n".join(o))
