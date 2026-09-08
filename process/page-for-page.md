# Page for page: score the client's site, rebuild every page, show the difference

Worked through on Van Ausdall & Farrar (2026-09-08). Before this, a preview was 50 to 60 pages
that stood in for the client's site. Now the preview has a counterpart for every URL the client
has, each one scored by the same script as the original, and the hub shows the two side by side.
The client sees their own page, the rebuilt page, and exactly what changed, for all of them.

**Time: about 40 minutes for a 170-page site, most of it unattended.**

## The four steps

1. **Crawl every page.** Sitemap minus blog query strings and PDFs, fetched with curl in
   parallel (16 at a time). Keep the HTML; everything downstream reads from disk.
2. **Score every page.** `scripts/site_audit.py --fetch-log ... --pages ...` runs seventeen
   checks and writes `brands/<slug>.seo-full.json` plus a CSV for the client repo. The same
   script with `--dir` scores a build, so the client's site and the rebuild are judged identically.
3. **Extract the copy and rebuild.** The crawl is parsed into `brands/<slug>.pages.json`
   (title, meta, H1, headings, paragraphs, bullets). `scripts/migrate_pages.py` maps every URL to
   a file in the build, turns the copy into hero, detail and FAQ sections, adds Service or Article
   schema and a form, and returns the 301 map. The content file decides what is `COVERED` by a
   hand-written page, what is `RETIRE`d, and what is migrated. `fix_title` and `fix_desc`
   normalise every page: 30 to 60 character titles with the city, 70 to 160 character metas.
4. **Score the build and show both.** Audit each option, write `brands/<slug>.build-audit.json`,
   rebuild. The hub's "Every page audited" section now renders one card per client URL: today's
   score, the build's score, each check side by side, a "what we did" list, and buttons for the
   live page and the new page in every option. `redirects.csv` in the client repo is the 301 map.

## The seventeen checks and their weights

FAQPage schema 14, Service or Article schema 10, at least 300 words 10, question-form headings 8,
title length 6, city in title 6, Review schema 6, meta length 5, one H1 5, two or more H2s 5,
depth over 600 words 4, LocalBusiness 4, alt text 4, form or click-to-call 4, internal links 3,
canonical 3, branded share image 3. Grades: A 85 and up, B 70, C 55, D 40, F below. The weights
favour what answer engines read, which is the point of the exercise.

## What the build does on every page, by default

- Organization schema with logo, description, sameAs, foundingDate and address, plus the
  headquarters LocalBusiness, on every page (`schema_blocks` in `preview.py`). Location pages
  carry their own LocalBusiness instead.
- A five-question FAQ marked up as FAQPage, with question-form H3s an assistant can quote.
- Service schema on service, industry and city pages; Article on case studies; BlogPosting on posts.
- A lead form and click-to-call, a self-referencing canonical, a branded share image.
- Titles and meta descriptions normalised by `fix_title` and `fix_desc`.

## What it deliberately does not do

- **No Review or AggregateRating schema** until the client has a Google review program.
  Self-published testimonials marked up as reviews break Google's guidelines. That is the six
  points between the build's 93 and 100, and the hub says so.
- **No rewriting of the client's copy** beyond em dashes, navigation residue and truncation at
  sentence ends. The migrated pages are their words in the new templates. Rewrites are the
  engagement, not the preview.
- **No invented facts in the FAQ.** Templated questions are answered from the page's own first
  paragraph or from facts already sourced in the brand file (phone, offices, NPS, founding year).

## Step five: the quality gate

The score is a grade; the gate is pass or fail. `scripts/quality_check.py --out <client-repo>
--domain <client domain>` re-reads every built page and checks the claims the hub makes: title
30 to 60 characters with the city, meta 70 to 160, one H1, two H2s, a question heading,
canonical, og:image, Organization and LocalBusiness JSON-LD that parses, FAQPage on every
non-policy page, Service on service, industry and city pages, Article on case studies and posts,
a form or tel link, ten internal links, no em or en dashes in visible text. It then checks that
every 301 target in `redirects.csv` exists in every option and that every link on the hub's page
cards resolves. Exit code 1 on any failure. Run it before every push; on VAF it caught 35 titles
of 61 to 67 characters that the score had let through as A grades.

Independent of the script, a Quality Agent (a subagent with the claim list and the file paths,
told to trust nothing and report discrepancies) does the same job with fresh eyes plus a browser
pass: console errors, horizontal overflow at 1440 and 390, FAQ toggles, and a read of migrated
copy for navigation residue and truncated sentences. Its prompt is in the session notes; the
pattern is "verify the claims, do not fix, report counts and file paths".

## Reuse for the next prospect

`site_audit.py` and `quality_check.py` are generic. `migrate_pages.py` is configured from the
content file: call `configure(brand={...}, city_words=(...), city_slugs={...})` with the client's
name, short name, state, headquarters city, site URL, meta tail sentence, proof points, service
line and assessment name before building. Every client-facing string in the module reads from
that block. The hub card renderer and the SEO report renderer read only the JSON files, so they
need no changes.

The whole sequence, for a new slug:

```bash
# 1 crawl (urls.txt from the sitemap, blog and PDFs filtered)
cat urls.txt | xargs -P 16 -I{} sh -c 'f=$(printf "%s" "{}" | md5sum | cut -c1-12); c=$(curl -sL -o pages/$f.html -w "%{http_code}" "{}"); echo "$c $f {}"' > fetch.log
# 2 score today
python3 scripts/site_audit.py --fetch-log fetch.log --pages pages --out brands/<slug>.seo-full.json --csv <client-repo>/seo-audit-pages.csv
# 3 extract copy (see the extraction snippet in this file's history), then build
python3 brands/<slug>.content.py && python3 scripts/preview.py ...
# 4 score the build and rebuild the hub
python3 scripts/site_audit.py --dir <client-repo>/clean --base <preview-url>/clean --out build_clean.json
```
