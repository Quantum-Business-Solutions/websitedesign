# Van Ausdall & Farrar: launch checklist

Portal 50498425, theme "Van Ausdall and Farrar - Showcase". Staging: https://50498425.hs-sites.com/ (all pages and posts are noindex until launch day).

Owner key: **VAF** = Brian Courtney and the VAF team, **QBS** = Quantum Business Solutions.

## 1. Content sign-off (VAF, before anything else)

- [ ] Brian reviews every page on the sign-off sheet (`vaf-website-signoff` in ClientCommand) and marks each Approved or Changes needed.
- [ ] See `vanausdall.claims-verified.md`: what was checked against outside sources and what Brian still confirms (SOC 2 report and wording, ISO 27001 status, Evansville address and phone, partner authorizations, case study results).
- [ ] **Claims verification.** One consolidated list goes to Brian. Each line is approved or corrected: client names and case study results, dollar figures and percentages, counts of systems, devices or people, certifications (ISO 27001, SOC), awards, years in business, service-response times, hours.
- [ ] Leadership bios and titles confirmed. Steven Sigmon headshot supplied.
- [ ] Logos: Berry Global, Echo Engineering and Mid-City logos supplied or the cards stay name-only.
- [ ] Real photography supplied (building, technicians, devices, Customer Care Center). Until then the 3D illustrations and generated images stay.
- [ ] Testimonials: VAF supplies quotes with permission to publish (deferred, not a launch blocker).
- [ ] Four posts dated Nov 1, 8, 15 and 22 are on the old site too and are scheduled here. Pillar pages link to them, so either publish them early or hide those links until their dates.
- [x] 58 accidental duplicate blog posts deleted 29 Oct (all 335 originals kept). One blank placeholder draft ("Your Blog Post Title Here") remains for QBS to remove.

## 2. Forms, popup and tools (QBS, then VAF test)

- [ ] Contact form, support request, assessment, popup lead form: submit a test on each and confirm the contact lands in HubSpot with the right source.
- [ ] Notification emails go to the right VAF inboxes.
- [ ] Popup: shows after the configured delay, respects exclusions (policies, assessment), floating Free guide button works, PDF downloads with logo and all 27 tips.
- [ ] Technology Strength Assessment: complete a run, check score, roadmap and PDF.
- [ ] Follow-up workflow: who contacts a lead after the guide or assessment, and how fast.
- [ ] Consent banner and privacy policy link on every page.

## 3. SEO and AEO (QBS)

- [ ] One H1 per page, headings in order, no heading over two lines on desktop.
- [ ] Title (under 60 characters) and meta description (under 160) unique on every page and post.
- [ ] Canonical URLs point at the production domain, not hs-sites.com.
- [ ] Schema validates in Google Rich Results test: Organization, LocalBusiness, WebSite, BreadcrumbList, FAQPage, Service, Blog, BlogPosting.
- [ ] Open Graph and Twitter images present.
- [ ] Image alt text on every content image.
- [ ] Internal link check: no broken links, every page has related-page links.
- [ ] llms.txt in place and sitemap.xml lists only indexable pages.
- [ ] Blog posts keep their original publish dates.
- [ ] Re-run `scripts/vaf_seo_compare.py`, `scripts/vaf_schema_check.py` and `scripts/vaf_claims_audit.py` on the production domain after cutover; every page A, no schema problems.
- [ ] HubSpot's own blog JSON-LD and AMP output are off (done 29 Oct) so the theme's BlogPosting block is the only one.
- [ ] Refresh the NPS figure from the CEO Juice widget every quarter (92.8 on 29 Oct 2026).

## 4. Quality assurance (QBS)

- [ ] Visible-text sweep for build language: "preview", "stand-in", "migrated", "current site", "new site", "imported", "rebuilt". None may remain.
- [ ] Mobile (375 px), tablet (768 px), desktop (1440 px) screenshots of every main page.
- [ ] Chrome, Safari, Firefox, Edge. iOS Safari and Android Chrome.
- [ ] Sticky header stays on every page and scroll position.
- [ ] Footer map, directions link, click-to-call, mailto all work.
- [ ] Keyboard navigation and focus states. Colour contrast. Reduced-motion setting respected.
- [ ] Lighthouse: performance 85 or higher on mobile for home and one service page, accessibility 95 or higher.
- [ ] Print preview of a service page.

## 5. Go-live (QBS with VAF IT)

- [ ] Identify DNS owner and registrar. Lower TTL to 300 seconds one day ahead.
- [ ] Connect the production domain in HubSpot, set primary, confirm SSL.
- [ ] 301 redirect list (`vanausdall.redirects.csv`, 218 rows: every old page, seven retired pages, 47 blog slugs that lost a double hyphen) loaded in HubSpot and spot-checked. Remove self-redirect rows. Custom 404 page checked.
- [ ] Remove noindex from every page and post. Confirm robots.txt allows crawling.
- [ ] Submit sitemap to Google Search Console and Bing Webmaster Tools.
- [ ] Analytics and conversion events on: forms, calls, directions clicks, guide downloads.
- [ ] Email deliverability: SPF, DKIM, DMARC for the sending domain.
- [ ] Day-of sequence: freeze edits, final export of the old site, switch DNS, verify home, three service pages, a blog post, forms, popup.
- [ ] Rollback plan: old DNS records saved. Revert if forms or SSL fail and cannot be fixed within the hour.

## 6. After launch

- [ ] Claim and complete the Google Business Profile for each office; start asking 9 and 10 survey scorers for a Google review.
- [ ] Day 1, day 7, day 30: Search Console coverage, crawl errors, 404s, form submissions.
- [ ] **Rotate the HubSpot API token used for the build.** Confirm user access and two-factor sign-in.
- [ ] Editing training for VAF: pages, blog, HubDB tables for popup and assessment copy.
- [ ] Backup of the old site archived.
- [ ] 30-day review: rankings, leads from the guide and assessment, pages to expand.

## Case study customers

- [ ] Customers are described, not named, on every page, in schema and in llms.txt (`brands/vanausdall.customers.json`). Re-run the name check after any content change.
- [ ] The 18 old customer URLs redirect to the new descriptive URLs (in `vanausdall.redirects.csv`).
- [ ] Customer logo files still sit in HubSpot Files under `/vaf/case/` and are no longer used on any page; VAF decides whether to delete them.
- [ ] Six old design-manager templates under the customers' old names are unused; delete them after launch.
