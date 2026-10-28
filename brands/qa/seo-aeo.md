# SEO and AEO audit: Van Ausdall & Farrar staging build

Audited 2026-10-28 against https://50498425.hs-sites.com (live, cache-busted) and the local build (`scripts/vaf_build.py dry`, overrides applied). Audit only: no repo file other than this report and `seo-aeo.json` was changed; no git, no HubSpot writes. Machine-readable copy: `brands/qa/seo-aeo.json`.

**Counts:** 45 findings: 3 blocker, 19 major, 23 minor.

**Scope crawled (live, Playwright plus curl):** /, /about, /contact, /partners, /solutions, the four pillars, /services/managed-it, /locations/indianapolis, /locations/fort-wayne, /case-studies/star-financial, /blog (all 29 listing pages), 3 posts, all 335 source blog slugs, 216 internal link and og:image targets, robots.txt, sitemap.xml. Redirect map sampled (25 rows) and fully checked for loops and chains.

## 10 most important fixes

1. Stop emitting Organization and LocalBusiness JSON-LD on every page; keep Organization on home or about only (preview.py schema_blocks).
2. Assign the VAF listing template to /blog and replace the placeholder intro (blog settings; vaf-blog-listing.html).
3. Fix the 47 blog posts that 404 at their source slug (HubSpot collapsed '--') and the 4 draft posts; make the import idempotent.
4. Delete duplicate blog posts (5 titles x3, 4 titles x2) and add real per-post blog rows to the redirect map; drop the 36 self-redirect rows.
5. Rewrite legacy links inside 139 imported posts (242 links, 59 paths not in the redirect map) and re-host the 33 press-release PDFs.
6. Redeploy the four pillars from the local overrides (live is stale) and link them from home, header and footer; they have one inbound link today.
7. Add pillar and sibling links to /services/managed-it (and the other service pages) and point its breadcrumb at the pillar.
8. Put the full NAP (6430 E 75th Street, Indianapolis, IN 46250) in the footer on every page.
9. Rewrite home and pillar H1, title and meta from intent, and add a visible 40 to 60 word direct answer at the top of each (recommended text below).
10. Fix blog BlogPosting: one block only, with dateModified, publisher logo and author; remove ?hsLang=en from internal links (307 hop on every link).

## Recommended title, meta description, H1, first-screen answer and buyer questions

Titles end with the full brand (22 characters), leaving 38 for the lead term, so each is 56 to 60 characters. Descriptions are 137 to 153 characters, benefit first, with a reason to click and no unsourced numbers. Each direct answer is 40 to 60 words and uses only facts already on the site; the 'largest' claim needs a named source before it is published (SEO-022).

### Home (/)

- **Title (56):** Office Technology in Indianapolis | Van Ausdall & Farrar
- **Meta description (153):** Managed IT, business phone systems, copiers and document workflow from one Indianapolis partner since 1914. Start with a free 10 to 15 minute assessment.
- **H1 (65):** Indianapolis office technology, from one local partner since 1914
- **Direct answer for the first screen (46 words):** Van Ausdall & Farrar is Indiana's largest full-service office technology provider, privately owned in Indianapolis since 1914. We run managed IT and cybersecurity, business phone systems, copiers and managed print, document management and AI consulting under one agreement, with offices in Indianapolis, Fort Wayne and Evansville.
- **8 buyer questions to answer in the first screen or FAQ:**
  1. Who is the largest office technology provider in Indiana, and who owns it?
  2. Can one company handle my IT, phones, copiers and documents?
  3. What does managed IT cost for a company my size?
  4. How fast do you respond when something breaks?
  5. Can you take over from my current IT, phone or copier vendor?
  6. What happens in the free Technology Strength Assessment?
  7. Do you serve my city outside Indianapolis?
  8. Who have you helped, and what did they save?

### Information pillar (/solutions-information)

- **Title (60):** Managed IT and Security, Indianapolis | Van Ausdall & Farrar
- **Meta description (146):** Managed IT, 24/7 security monitoring, cloud and backup for Indianapolis businesses, from one local team with a vCIO. Start with a free assessment.
- **H1 (63):** Managed IT, cybersecurity and cloud for Indianapolis businesses
- **Direct answer for the first screen (48 words):** Van Ausdall & Farrar's Information pillar is managed IT, cybersecurity, cloud, backup and physical security from one Indianapolis team. A virtual CIO plans your technology, a security operations center monitors it around the clock, and one monthly agreement replaces separate vendors. Start with the free Technology Strength Assessment.
- **8 buyer questions to answer in the first screen or FAQ:**
  1. What is included in managed IT services?
  2. How is managed IT different from IT support?
  3. How is managed IT priced, and what do I get for the money?
  4. Do you work alongside our internal IT person?
  5. What is a vCIO, and do we need one?
  6. Do you monitor security around the clock, and what happens in an incident?
  7. Can you move our servers to the cloud and back them up?
  8. What do we get in the first 30 days?

### Communication pillar (/solutions-communication)

- **Title (59):** Business Phone Systems, Indianapolis | Van Ausdall & Farrar
- **Meta description (146):** Business phone systems, VoIP and unified communications from Mitel, RingCentral and 8x8, installed and supported statewide. Get a free assessment.
- **H1 (72):** Business phone systems and unified communications for Indiana businesses
- **Direct answer for the first screen (50 words):** Van Ausdall & Farrar designs, installs and supports business phone systems and unified communications, which put voice, chat, email and video meetings in one application on any device. We sell Mitel, RingCentral and 8x8 and have deployed more than 4,000 systems since 1983, with a vendor-certified service fleet across Indiana.
- **8 buyer questions to answer in the first screen or FAQ:**
  1. Which business phone system is right for my office: Mitel, RingCentral or 8x8?
  2. Cloud, on-premises or hybrid phone system: which should we choose?
  3. How much does a business phone system cost?
  4. Can remote staff use the system on their own devices?
  5. What happens to our phones if the internet or power goes down?
  6. Can you support several offices and a contact center?
  7. Who services the system after installation, and how fast?
  8. Can we keep our numbers and carrier when we switch?

### Process pillar (/solutions-process)

- **Title (59):** Document Workflow Solutions, Indiana | Van Ausdall & Farrar
- **Meta description (137):** Scan paper to searchable files, automate document workflows and outsource mail, print and records handling. Start with a free assessment.
- **H1 (73):** Document scanning, workflow and process automation for Indiana businesses
- **Direct answer for the first screen (50 words):** Van Ausdall & Farrar's Process pillar manages the daily flow of information through your company: document scanning and conversion in its secure Indianapolis center, content management, workflow automation, mail and print centers, and facilities services. Work can be done on site or off site under a documented chain of custody.
- **8 buyer questions to answer in the first screen or FAQ:**
  1. How does document scanning work, and how long does it take?
  2. Is scanning patient or customer records secure and HIPAA-ready?
  3. What happens to the paper after it is scanned?
  4. How is document scanning priced?
  5. What is the difference between document management and content management?
  6. Can you automate invoices, forms and approvals?
  7. Can you run our mail room, print room or reception for us?
  8. How do scanned records become searchable in the systems we already use?

### Print pillar (/services/copy-print-solutions)

- **Title (60):** Copier and Managed Print Indianapolis | Van Ausdall & Farrar
- **Meta description (149):** Copiers, multifunction printers and managed print services with same-day metro service. See where your print spend goes with a free print assessment.
- **H1 (72):** Copiers, printers and managed print services for Indianapolis businesses
- **Direct answer for the first screen (51 words):** Van Ausdall & Farrar sells, leases and services copiers and multifunction printers from Canon, Ricoh, Kyocera and HP, and runs managed print services that monitor your whole fleet and replenish supplies. Most Indianapolis metro service calls get same-day response. A free print assessment shows what you spend now before any quote.
- **8 buyer questions to answer in the first screen or FAQ:**
  1. Should we buy or lease a copier?
  2. How much does a copier lease cost per month?
  3. What are managed print services, and what will they save us?
  4. How fast is copier repair in Indianapolis?
  5. Which brands do you sell and service?
  6. Can you manage printers we already own?
  7. How do you keep print secure and compliant?
  8. What happens in the free print assessment?

## Findings

### Blocker (3)

**SEO-001** | all pages (verified on 13 of 13 non-blog pages crawled)  
What: Organization JSON-LD is emitted on every page and the headquarters LocalBusiness on 11 of them. House position (guardrails.md, Structured data) allows Organization on the home page or one about page only, WebSite on the home page only, and BreadcrumbList site-wide.  
Evidence: Live JSON-LD parsed from home, about, contact, partners, solutions, solutions-information, solutions-communication, solutions-process, services/copy-print-solutions, services/managed-it, locations/indianapolis, locations/fort-wayne and case-studies/star-financial: every one carries Organization @id https://www.vanausdall.com/#organization. Eleven (all except the two location pages, which carry their own LocalBusiness) also carry LocalBusiness @id .../#headquarters. The function docstring says it: 'Organization and the headquarters LocalBusiness on every page'. brands/vanausdall.seo-deep.md even reports 'every page now carries LocalBusiness and Organization' as a positive.  
Fix: scripts/preview.py schema_blocks() lines 812-855: emit the Organization and HQ LocalBusiness blocks only when page['file'] == 'index.html' (or about.html, one of the two, not both); WebSite stays index.html only; BreadcrumbList stays on every non-home page. scripts/vaf_build.py schema_html() calls it, so no second change is needed. Then rebuild all pages with scripts/vaf_build.py templates all.

**SEO-002** | /blog (HubSpot blog listing)  
What: The blog listing is not on the VAF template. It renders HubSpot default chrome and placeholder copy, which guardrails.md says must never ship.  
Evidence: Live /blog: nav reads 'Home, Products, Pricing, Blog, Company, Get started'; intro paragraph is 'A brief introductory description of your blog and the topics covered at a high level. Just one or two sentences should be just right.'; footer social icons link to bare linkedin.com, facebook.com, twitter.com, instagram.com, tiktok.com. No canonical tag, no og:image, no JSON-LD. Blog posts do load the VAF chrome, so only the listing template is unassigned.  
Fix: HubSpot Settings > Website > Blog > Templates: assign themes/vaf/templates/vaf-blog-listing.html as the listing template and set the blog description (also appears in the og/meta description). Re-run the guardrail gate (scripts/verify.mjs 'blog uses the theme') on /blog.

**SEO-003** | /blog/<slug> (47 of 335 imported posts)  
What: 47 posts dated on or before today are 404 at their source URL /blog/<source-slug>, and 4 more are future-dated drafts that also 404. HubSpot collapsed the double hyphens in the source slugs, so the live slug no longer matches the source slug the redirect map, home page and pillars link to.  
Evidence: Requested all 335 slugs from brands/vanausdall.blog.json at https://50498425.hs-sites.com/blog/<slug>: 284 return 200, 51 return 404. 47 of the 51 are dated 2026-10-22 or earlier and contain '--' or '---' in the source slug (e.g. print--copy-solutions-where-document-workflows-start is live at print-copy-solutions-where-document-workflows-start-2, healthcare-it-solutions-securing-patient-data--streamlining-operations, van-ausdall--farrar-celebrates-110-years-of-innovation, mitel-connect-client---answering-a-call). The other 4 (why-construction-firms-cant-escape-paper 2026-11-22, in-house-vs-outsourced-production-print-break-even 2026-11-15, it-solutions-for-healthcare-hipaa-technical-safeguards 2026-11-08, business-technology-simplified-a-century-of-innovation 2026-11-01) are state DRAFT in brands/vanausdall.blog-import.state.json, so they 404 until published.  
Fix: scripts/vaf_blog_import.py: normalise slugs (collapse runs of '-') before create and record the real slug; PATCH the 47 existing posts to the normalised slug, or add a redirect per post. Publish or schedule the 4 drafts. Update brands/vanausdall.blog.json slug values to the live slug so overrides, the home 'articles' section and pillar 'related' items link to URLs that exist.

### Major (19)

**SEO-004** | /blog (listing and posts)  
What: The same post is published more than once, each copy self-canonical, so the blog carries duplicate content and the listing shows the same title two or three times.  
Evidence: Listing pages /blog and /blog/page/1..29 hold 342 unique post URLs against 335 source posts. Titles repeated in the listing: 'Print & Copy Solutions: Where Document Workflows Start' x3, 'Print & Copy Solutions: Maximizing Efficiency and ROI' x3, 'Healthcare IT Solutions: Securing Patient Data & Streamlining Operations' x3, 'Modern Print & Copy Solutions for Business Efficiency' x3, 'Revolutionize Your Workplace: Modern Print & Copy Solutions Unleashed' x3, and four more titles x2. Example: /blog/print-copy-solutions-where-document-workflows-start, ...-1 and ...-2 each return 200 with a canonical pointing to themselves.  
Fix: HubSpot blog posts: delete the extra copies (keep the one whose slug you will redirect to); in scripts/vaf_blog_import.py make create idempotent by checking existing posts by normalised slug and title, not by exact slug. brands/vanausdall.blog-import.state.json shows the duplicate creates.

**SEO-005** | brands/vanausdall.redirects.csv  
What: The redirect map has no per-post blog rows. It holds one placeholder pattern row, which no redirect importer can evaluate, and a second placeholder row for images and PDFs.  
Evidence: 174 data rows, 171 page rows, none beginning /blog except the literal row '/blog?p=<slug>-<YYMMDD> -> /blog/<slug>' (note 'one rule per post, from the sitemap') and the literal row '"/images/..., /pdf/..." -> unchanged or re-hosted'. 335 blog posts and the press-release PDFs (see the PDF finding) need real rows.  
Fix: brands/vanausdall.redirects.csv and brands/vanausdall.redirects.json: generate one row per post from the old sitemap to the live HubSpot slug (use brands/vanausdall.blog-import.state.json after the slug fix), and remove the two placeholder rows.

**SEO-006** | brands/vanausdall.redirects.csv and .json  
What: 36 rows redirect a URL to itself. Imported into HubSpot URL mappings these are loops or are rejected; they are also pure noise.  
Evidence: CSV rows where Old URL == New URL: /, /about, /benefits, /case-studies and its 18 child pages, /contact, /downloads, /industries, /partners, six /policies/* pages, /solutions, /support, /technology-strength-assessment, /virtualsitevisit (36 rows; the JSON has the same 36 plus trailing-slash variants such as /about/ -> /about). No chains and no two-step loops were found: every non-identity target is itself not a source, and the sampled targets exist.  
Fix: brands/vanausdall.redirects.csv and brands/vanausdall.redirects.json: delete every row where Old URL equals New URL (keep trailing-slash handling as a HubSpot setting, not a row).

**SEO-007** | /blog/* (139 of 335 imported posts)  
What: Imported post bodies link to legacy vanausdall.com paths instead of the new URLs: 242 internal links across 139 posts. 98 distinct paths; 59 of them (85 links) are not in the redirect map at all, so they will 404 after launch even with the map applied.  
Evidence: Scan of bodyHtml in brands/vanausdall.blog.json. Most common: /information/managed-it-services (18), /information/data-security (15), /document-management (10), /communication (9), /print (8, not in map), /technology-strength-score (8, not in map), /process/document-conversion (4, not in map), /copy-print-management-solutions (4, not in map), /business-telephones, /information-management, /contact-us, /managed-it-solutions. Live proof from /blog/data-discovery-and-classification: links to /ai, /document-management, /network-security, /get-started, /information/managed-it-services all return 404 on staging.  
Fix: scripts/vaf_blog_import.py (body rewrite step) or a one-off pass over brands/vanausdall.blog.json bodyHtml: rewrite each legacy href to its final URL using brands/vanausdall.redirects.csv, and add rows to the map for the 59 unmapped paths (or retarget them to the nearest service page).

**SEO-008** | /blog/* (33 posts) and brands/vanausdall.redirects.csv  
What: The 'View Full Press Release (PDF)' links in 33 posts point to /pdf/pr/... files that do not exist on staging, and the redirect map only says 'unchanged or re-hosted'.  
Evidence: 33 distinct /pdf/ hrefs in bodyHtml. Live checks: /pdf/pr/2026/202608%20AI%20Workflow%20Automation.pdf, /pdf/pr/2026/202609%20Data%20Discovery%20and%20Classification.pdf and /pdf/mitel-gold-award.pdf all return 404.  
Fix: Upload the PDFs to HubSpot files and rewrite hrefs in brands/vanausdall.blog.json bodyHtml (or add a per-file row to brands/vanausdall.redirects.csv), then re-run scripts/vaf_blog_import.py.

**SEO-009** | /solutions-information, /solutions-communication, /services/copy-print-solutions, /solutions-process  
What: The live pillar pages are an older build than the local overrides. Three of four have different title and meta than the local build, and the live copies have no pillar-to-service links in the body.  
Evidence: Titles live vs local: solutions-information 'Information Technology, Indiana | Van Ausdall & Farrar' vs 'Information Technology Services Indianapolis | VAF'; solutions-communication 'Unified Communications, Indiana | Van Ausdall & Farrar' vs 'Business Phone Systems and Unified Communications | VAF'; copy-print 'Copy Print Solutions in Indianapolis' (36 chars) vs '... | Van Ausdall & Farrar'. Live solutions-communication meta is the raw first paragraph 'The workplace was historically composed of physical office space...'. Live pillar FAQs are the boilerplate 'Who is Information Technology for? / How much does Information Technology cost? / Where is Information Technology available?' and 'What is Information Technology?' is answered with cloud-migration text; local overrides replace them. Links inside <main>: live solutions-information, -communication, -process each have 2 (contact, assessment); local `vaf_build.py dry` output links 10 to 15 service pages each.  
Fix: Redeploy: scripts/vaf_build.py templates solutions-information solutions-communication solutions-process services/copy-print-solutions, then pages for the same slugs (brands/vanausdall.overrides.pillars.json is the source). Then re-crawl.

**SEO-010** | /solutions-information, /solutions-communication, /solutions-process, /services/copy-print-solutions  
What: The four pillar pages are orphaned from the main navigation and the home page. The only inbound link from any crawled page is the /solutions hub.  
Evidence: Searched href="/solutions-information", "/solutions-communication", "/solutions-process" and "/services/copy-print-solutions" across all 16 crawled live pages: each appears only in /solutions. The home page 'Four pillars' cards link Information to /services/managed-it, Communication to /services/business-phone-systems, Print to /services/copiers and Process to /services/document-management, skipping the pillars. The header menu and footer list services, not pillars.  
Fix: brands/vanausdall.overrides.home.json (cards 'pillars' items, wheel and hotspots hrefs): point the four pillar cards at the pillar pages. scripts/vaf_chrome.py footer 'SOLUTIONS' column and the header Solutions menu: add the four pillar links as the first entries.

**SEO-011** | /services/managed-it  
What: The service page has no links to its pillar or to the services it describes. Service-to-pillar and sibling links are missing.  
Evidence: Links inside <main> on live and in `vaf_build.py dry services/managed-it` output are only /, /solutions, /contact, /technology-strength-assessment. The copy names vCIO, security, backup, voice and cloud but links to /services/cybersecurity, /services/business-continuity, /services/cloud and /services/business-phone-systems are all absent, and there is no link to /solutions-information.  
Fix: brands/vanausdall.overrides.services.json key 'services/managed-it.html': add a 'related' section (compose list) linking solutions-information.html, services/cybersecurity.html, services/cloud.html, services/business-continuity.html, services/it-support.html with descriptive anchors; and change crumbs [1] from solutions.html to solutions-information.html.

**SEO-012** | / (home) and local pillar pages  
What: Home and pillar pages link to blog posts that 404 on staging.  
Evidence: Home 'Latest from the VAF blog' first card links /blog/print--copy-solutions-where-document-workflows-start (404; live slug differs). `vaf_build.py dry` shows pillars link 7 blog URLs that 404: copy-print -> in-house-vs-outsourced-production-print-break-even (draft), print--copy-solutions-maximizing-efficiency-and-roi, print--copy-solutions-where-document-workflows-start; solutions-information -> business-technology-simplified-a-century-of-innovation (draft), healthcare-it-solutions-securing-patient-data--streamlining-operations, it-solutions-for-healthcare-hipaa-technical-safeguards (draft); solutions-process -> why-construction-firms-cant-escape-paper (draft).  
Fix: brands/vanausdall.overrides.home.json (section 'articles') and brands/vanausdall.overrides.pillars.json (each 'related' section): replace with live slugs after the blog slug fix, or choose posts that return 200 (e.g. data-discovery-and-classification, digital-transformation-what-it-looks-like-mid-market, ai-workflow-automation).

**SEO-013** | /blog/<slug> posts (ai-workflow-automation, data-discovery-and-classification)  
What: Every post carries two BlogPosting blocks: the theme's own and HubSpot's automatic one. They disagree (author Organization vs Person, date-only vs full timestamp), and neither has dateModified; the HubSpot block has an empty publisher logo; the theme block has no publisher logo, no author URL.  
Evidence: Live ai-workflow-automation: block 1 (themes/vaf/templates/vaf-blog-post.html) = headline, description, datePublished '2026-09-17', image, author {Organization 'Van Ausdall & Farrar'}, publisher {Organization, no logo}; block 2 (HubSpot) = author {Person, url /blog/author/van-ausdall-and-farrar}, datePublished '2026-09-17T16:00:00.000Z', publisher {'logo': {'@type':'ImageObject'}} with no url. No dateModified anywhere. Block 1 description also carries a literal '&amp;'.  
Fix: themes/vaf/templates/vaf-blog-post.html head_extra: add dateModified ({{ content.updated|format_datetime('yyyy-MM-dd') }}), publisher.logo ImageObject with a real logo URL, author url, and apply striptags/unescape to description; then suppress HubSpot's automatic BlogPosting (blog Settings > Website > Blog > SEO) so one block remains. Verify with the Rich Results Test.

**SEO-014** | 13 locally authored blog guides (blog/what-is-a-vcio, blog/copier-lease-vs-buy-indianapolis, blog/what-managed-print-costs, blog/business-phone-systems-buyers-guide, blog/ai-acceptable-use-policy, blog/document-conversion-services-what-to-expect, blog/physical-intrusion-detection-systems and 6 more)  
What: The 13 answer-targeted guides written for the new site are in brands/vanausdall.content.json but are not published anywhere. They are excluded from site pages by vaf_build.py and are not in the blog import, so they 404.  
Evidence: https://50498425.hs-sites.com/blog/what-is-a-vcio, /blog/copier-lease-vs-buy-indianapolis, /blog/what-managed-print-costs all 404 (also 404 at the root). vaf_build.py lines 158-160 deliberately skip every blog/* page; none of the 13 slugs is in brands/vanausdall.blog.json. These target the question keywords in brands/vanausdall.seo-deep.md ('what is managed it services' 1,000/mo, 'how much does managed it services cost' 720, 'is it better to buy or lease a copier' 110).  
Fix: Add the 13 pages to brands/vanausdall.blog.json (slug, title, date, bodyHtml built from the article and faq sections) and import with scripts/vaf_blog_import.py, or create them as HubSpot blog posts; strip the hand-written schema key from each page in brands/vanausdall.content.json once the template emits BlogPosting.

**SEO-015** | all pages (footer)  
What: No full NAP in the footer or the body of most pages. The footer carries phone and email only; the address with city, state and ZIP appears on only 3 of 12 non-blog pages crawled.  
Evidence: Footer text on every page ends '(317) 634-2913, clientsuccess@vanausdall.com'; no street address. Full 'Indianapolis, IN 46250' appears on contact, locations/indianapolis and locations/fort-wayne only. Home shows '6430 E 75th Street' twice (map card, seal text) but never with city and ZIP together; about shows the street only. Phone is consistent, (317) 634-2913 everywhere, always with a tel: link.  
Fix: scripts/vaf_chrome.py footer block (line ~136-140) and the generated themes/vaf/modules/vaf-footer.module/module.html: add an <address> element 'Van Ausdall & Farrar, 6430 E 75th Street, Indianapolis, IN 46250' under the phone line; add the address to the brand fields (brands/vanausdall.content.json brand) and fields.json of vaf-footer.module.

**SEO-016** | / (home)  
What: The home H1 is brand voice, not search intent, and the first screen has no direct answer. 'Everything your business runs on, under one roof.' contains no category term, no city; the hero paragraph under it is 26 words and does not say who the company is or what it sells in a quotable sentence.  
Evidence: Live H1 and hero text. 'Indiana's largest full-service office technology provider' is stated only in the footer and meta, never in the first screen. brands/vanausdall.seo-deep.md records VAF as absent from AI answers for 'who is the largest office technology provider in Indiana' despite making the claim.  
Fix: brands/vanausdall.overrides.home.json: section 'hero' and 'hero-light' key 'heading' (and 'subhead'); keep the old line as the 'eyebrow'. Recommended text is in the Recommendations section of brands/qa/seo-aeo.md.

**SEO-017** | all key pages (home, pillars, managed-it, partners)  
What: No page has a visible TL;DR or direct 40 to 60 word answer to the buyer question it targets. The word count of the first paragraph after the H1 is 14 to 41 words and is descriptive, not an answer.  
Evidence: First paragraph after H1, in words: home 26, solutions 25, solutions-information 18, solutions-communication 36 (raw legacy paragraph), solutions-process 26, copy-print 22, managed-it 32, partners 41, star-financial 14. Only /about (50 words, who founded it and what it is today) fits. grep for 'TL;DR', 'key takeaways', 'in short', 'short answer', 'at a glance' returns no hits on any crawled page.  
Fix: Add a 'tldr' pattern: a first section (detail or hero 'subhead' key) in brands/vanausdall.overrides.home.json, brands/vanausdall.overrides.pillars.json, brands/vanausdall.overrides.services.json, using the recommended 40 to 60 word answers; for blog posts add it to the vaf-blog-post module.

**SEO-018** | /solutions-communication  
What: The H1 is the single word 'Communication', on both the live page and the local override. No search intent, no category term, no place.  
Evidence: Live and local H1: 'Communication'. The local title is 'Business Phone Systems and Unified Communications | VAF'.  
Fix: brands/vanausdall.overrides.pillars.json key 'solutions-communication.html' sections[hero].heading.

**SEO-019** | all internal links  
What: Every internal link on live pages carries ?hsLang=en and 307-redirects to the clean URL, adding a redirect hop to every crawl path and creating a second URL form for every page.  
Evidence: Home raw HTML has 154 of its 164 root-relative hrefs ending ?hsLang=en (e.g. /services/managed-it?hsLang=en); about 125 of 132; managed-it 115 of 122. curl -I 'https://50498425.hs-sites.com/contact?hsLang=en' returns HTTP/2 307 with location: https://50498425.hs-sites.com/contact. No hsLang string exists in themes/vaf, so it is added by HubSpot (multi-language or language setting).  
Fix: HubSpot Settings > Website > Languages: turn off multi-language URL parameters or set the default language so ?hsLang is not appended; check the page language field written by scripts/vaf_build.py cmd_pages ('language': 'en'). Re-crawl to confirm hrefs are clean.

**SEO-020** | /case-studies/star-financial  
What: Two Article blocks on one page that disagree, neither with datePublished, and a FAQ answer that does not answer its question.  
Evidence: Block 1 (hand-written in brands/vanausdall.content.json pages[case-studies/star-financial.html].schema): headline 'STAR Financial Bank: STAR achieved over 70% cost savings...', author and publisher Organization, no image, no date. Block 2 (module vaf-article): headline 'STAR Financial Bank', image, author, mainEntityOfPage, no publisher, no date. FAQ 'Which services did STAR Financial Bank use?' is answered 'STAR Financial Bank, based in Fort Wayne, Indiana, recognized its need for a new print partner...' which names no service. The FAQ answer 'What was the measurable result?' is the self-reference 'as published in the case study on vanausdall.com', and 'Can we get results like these?' asserts 'Every one of these engagements started with the free Technology Strength Assessment', an unsourced blanket claim repeated on all case-study pages.  
Fix: brands/vanausdall.content.json pages[file=case-studies/star-financial.html]: delete the hand-written schema key (all 18 case-study pages carry the same hand-written key); keep only the module Article from themes/vaf/modules/vaf-article.module/module.html and add datePublished, publisher; rewrite the faq items in the same page (or in the generator that builds them).

**SEO-021** | /solutions-information (live), /solutions-communication (live)  
What: Live pillar H2 headings and FAQ answers are legacy text lifted from other pages. A blog post title is a section heading, and 'What is Information Technology?' is answered with a paragraph about cloud migration.  
Evidence: Live solutions-information H2 'Data Quality vs. Data Quantity: Why More Isn't Always Better' sits in the main outline; FAQ 'What is Unified Communications?' is answered with a rambling paragraph that opens 'The end result? Many of us were using 3, 4, 5 and maybe even 6 different applications...' and never defines the term. Local overrides replace both.  
Fix: Resolved by the redeploy finding; also check brands/vanausdall.overrides.pillars.json 'faq' items are used (they are, local build).

**SEO-022** | /services/copy-print-solutions (and Organization description on every page)  
What: Claim 'cut printing costs up to 30%' has no named source, date or method, yet it is in the hero text, meta description, FAQ answer and Service JSON-LD description of the print pillar.  
Evidence: Local and live copy-print: hero text 'Reduce costs by up to 30%...', meta 'Cut printing costs up to 30% with a free print assessment' (local), FAQ 'What is managed print services? ... cut printing costs up to 30%', Service JSON-LD description. No source line, unlike the home page 'Sources:' footnote. 'Indiana's largest full-service office technology provider' is likewise stated in meta, Organization description and footer on every page with no named ranking.  
Fix: brands/vanausdall.overrides.pillars.json key 'services/copy-print-solutions.html' (hero subhead, faq item 3, description) : attribute ('typical savings reported by customers, source: ...') or remove; add a source line to the 'largest' claim on brands/vanausdall.overrides.home.json and about.

### Minor (23)

**SEO-023** | / (home)  
What: Title has the brand first and the primary term second; 53 characters. Recommended: 'Office Technology in Indianapolis | Van Ausdall & Farrar'.  
Evidence: Live title 'Van Ausdall & Farrar | Indianapolis Office Technology'. About ('About Van Ausdall & Farrar, Indianapolis') and Contact ('Contact Van Ausdall & Farrar, Indianapolis') have the brand mid-title rather than last.  
Fix: brands/vanausdall.content.json pages[index.html].title (home); pages[about.html].title and pages[contact.html].title.

**SEO-024** | 47 of 169 local pages including three pillars and case studies  
What: The brand suffix is the abbreviation 'VAF' on 47 pages, which no searcher types, and 'Indiana' is used where a city is the intent. Includes solutions-process and the local info/communication pillar titles.  
Evidence: 47 titles end '| VAF' (e.g. 'Business Process Management Solutions, Indiana | VAF', 'STAR Financial Bank case study, Indiana | VAF'). All titles are 30 to 60 characters except company-facts (69).  
Fix: brands/vanausdall.content.json and brands/vanausdall.overrides.pillars.json: change the suffix to '| Van Ausdall & Farrar' and shorten the lead term to fit 60 characters; company-facts title to <= 60 in brands/vanausdall.extra-pages.json.

**SEO-025** | /solutions  
What: Meta description is truncated mid-list and ends 'copiers, managed print, copier.'  
Evidence: Live and local meta (155 chars): 'Four pillars, twelve solutions, one partner: managed IT, cybersecurity, cloud, backup and recovery, business phone systems, copiers, managed print, copier.' The source description was cut at a word boundary, not rewritten. Also echoed in brands/vanausdall.llms.txt.  
Fix: brands/vanausdall.content.json pages[solutions.html].description.

**SEO-026** | /about  
What: Meta description is 116 characters (below 120) and has no reason to click.  
Evidence: Live meta: 'From a Thomas Edison Company distributorship in 1914 to Indiana's largest full-service business technology provider.'  
Fix: brands/vanausdall.content.json pages[about.html].description; suggest: 'From a 1914 Thomas Edison Company dealership to Indiana's largest full-service office technology provider. Meet the people and the history behind VAF.' (150)

**SEO-027** | 20 local pages (e.g. /case-studies/star-financial)  
What: The meta builder pads short descriptions with the brand line, so the brand appears twice and the page's own sentence is wasted; 15 local metas run over 155 characters.  
Evidence: Live star-financial meta: 'STAR achieved over 70% cost savings after five months with Van Ausdall & Farrar. Van Ausdall & Farrar, Indianapolis office technology since 1914.' Local final metas: solutions-communication 158, services/copy-print-solutions 160 (build trims to <= 158), 20 metas contain the brand twice, 4 are under 120. No duplicate titles or descriptions across the 169 local pages.  
Fix: scripts/vaf_build.py meta_desc() lines 207-215: do not append the tail when the description already contains the brand; cap at 155 not 158. Rewrite descriptions in brands/vanausdall.content.json for the case-study pages (benefit plus 'See how').

**SEO-028** | /services/managed-it (and other services pages)  
What: Section headings lower-case the acronym: 'What changes with VAF managed it services' and 'Questions we get about managed it services'.  
Evidence: Live H2s on /services/managed-it; the string is in brands/vanausdall.content.json lines 2257 and 2418.  
Fix: brands/vanausdall.overrides.services.json key 'services/managed-it.html' (heading of the 'cards'/'faq' sections): 'managed IT services'.

**SEO-029** | /solutions (hub) and 11 service pages  
What: Typos in titles and headings: 'Know Be4' (x6, brand is KnowBe4), 'Scan Documents with Your i Phone', 'Integrated Speech and Voice Recognition from Winscribe', long keyword-stuffed H3s ('Cloud VoIP & PBX Systems for Every Business').  
Evidence: /solutions has 81 H3 headings and 71 unique body links; H3s include 'Know Be4, Get Your Free Ransomware Simulator Tool Servi...' and 'Scan Documents with Your i Phone'. Source strings at brands/vanausdall.content.json lines 1844-1970.  
Fix: brands/vanausdall.overrides.services.json: set title for services/knowbe4-*.html and services/iphone-scanning.html; or add 'title' overrides in brands/vanausdall.overrides.pillars.json 'solutions.html'.

**SEO-030** | / (home), /solutions-process (live), /services/copy-print-solutions (live)  
What: A migration artifact is a visible H2: 'Imported directly from our after-service surveys'. It reads as a build note, has no keyword, and a reader sees 'imported'.  
Evidence: H2 on home and the testimonials section of the pillar pages. Source: brands/vanausdall.overrides.home.json line 905, brands/vanausdall.overrides.pillars.json line 970, brands/vanausdall.content.json line 1435.  
Fix: Those three keys: replace with 'What customers say after a service call' (already used on managed-it).

**SEO-031** | / (home)  
What: H3 outline is thin and generic. The four pillars appear as single-word H3s 'Information', 'Communication', 'Print', 'Process'; there is no question-style heading in the body, and the FAQ questions are <summary> elements, not headings.  
Evidence: Home outline: 1 H1, 17 H2, 40 H3. The FAQ module (themes/vaf/modules/vaf-faq.module/module.html) renders each question as <summary>, collapsed.  
Fix: brands/vanausdall.overrides.home.json section 'pillars' items headings -> 'Managed IT and security', 'Business phone systems', 'Copiers and managed print', 'Document workflow'; consider rendering the first three FAQ answers open (module field open_first).

**SEO-032** | all pages with FAQ (about, contact, home, partners, solutions, pillars, managed-it, locations, case-study)  
What: FAQPage question names contain a literal '&amp;', so the markup text differs from the visible text. The answer text is un-escaped correctly, the question is not. All 13 FAQ blocks match the visible Q and A otherwise.  
Evidence: Live about FAQ JSON: "name": "Who owns Van Ausdall &amp; Farrar?" and 'How long has Van Ausdall &amp; Farrar been in business?'; same on locations/indianapolis ('Who is Van Ausdall &amp; Farrar?'), case study and partners. FAQ rich results were retired 7 May 2026, so this is a consistency fix, not a ranking gain.  
Fix: themes/vaf/modules/vaf-faq.module/module.html line 14: add |replace('&amp;','&')|replace('&nbsp;',' ') to it.question exactly as the answer already does.

**SEO-033** | /locations/indianapolis, /locations/fort-wayne, /locations/evansville  
What: Hand-written LocalBusiness and Service JSON-LD for the location pages is stored as literal JSON in content.json, which the house position says never to hand-write; one value points at a preview host and Indianapolis has two LocalBusiness entities for the same office.  
Evidence: LocalBusiness image is https://van-ausdall.vercel.app/assets/hq-1200.jpg (200 today, but a preview host). Indianapolis carries LocalBusiness @id .../locations/indianapolis#office and, on every other page, .../#headquarters for the same address. Service provider is an inline Organization, not the @id. 12 other local blog pages use the same vercel.app image.  
Fix: brands/vanausdall.content.json pages[locations/*.html].schema: replace with module-derived output (a vaf-locations or vaf-map module field); until then change image to the hubfs asset URL and use '@id' for provider; merge Indianapolis #office into #headquarters.

**SEO-034** | all pages (Organization/LocalBusiness data)  
What: Values in the entity markup are guesses or unverified: priceRange '$$' is a code default, geo 39.887,-86.062 differs from the Google Maps pin for the business, logo points at the legacy site's /images/logo.png, and the business name appears in four forms.  
Evidence: scripts/preview.py line 833: hq.get('priceRange', '$$') default. The goo.gl short link in sameAs resolves to a Google Maps place at 39.8913151,-86.0559852 (about 0.7 km from the schema geo). Logo https://www.vanausdall.com/images/logo.png returns 200 today but belongs to the old site's file tree. Names: 'Van Ausdall & Farrar, Inc.' (schema), 'Van Ausdall & Farrar Indianapolis' (LocalBusiness), 'Van Ausdall & Farrar' (copy), 'VAF'. The sameAs LinkedIn URL has an unencoded '&'.  
Fix: scripts/preview.py schema_blocks(): drop priceRange unless supplied in brands/vanausdall.content.json schema.hq.priceRange; correct hq.lat and hq.lon from the verified pin; set schema.org_logo to the hubfs-hosted logo-600.png; percent-encode '&' as %26 in sameAs.

**SEO-035** | all pages  
What: Open Graph is incomplete: no og:type or og:site_name on pages; og:image:alt repeats the page title or the bare brand ('Van Ausdall & Farrar' on home); contact and partners share a 16:9 hero poster (1920x1080) as the share image.  
Evidence: Parsed og:* on all crawled pages: present og:title, og:description, og:image, og:image:width/height/alt, og:url; absent og:type and og:site_name (present only on blog posts and /blog). Every og:image URL resolves 200. Home og:image gen-technician-1200.jpg, contact and partners hero-poster-2.jpg.  
Fix: scripts/vaf_build.py og_image() (line 218) and cmd_pages body: add per-page share image (1200x630) and descriptive featuredImageAltText; add og:type website and og:site_name in themes/vaf/templates/layouts/vaf-base.html head.

**SEO-036** | /blog (listing) and blog posts  
What: Blog listing has no canonical, no og:image and no meta robots tag, and posts and listing carry no BreadcrumbList. The listing is covered only by the domain-level x-robots-tag: none header.  
Evidence: Live /blog: canonical missing, meta robots missing; /blog, /blog/ai-workflow-automation and /about all return 'x-robots-tag: none' (hs-sites domain header). Posts carry meta robots noindex, nofollow. Posts show a visible 'Home/Blog/News & Press' trail but no BreadcrumbList JSON-LD.  
Fix: At launch: remove NOINDEX from scripts/vaf_build.py and the blog headHtml (scripts/vaf_blog_import.py NOINDEX); add BreadcrumbList to themes/vaf/templates/vaf-blog-post.html head_extra; ensure canonical via the blog listing template.

**SEO-037** | /blog/ai-workflow-automation  
What: Post body has no subheadings and a time-stamped date. 857 words with zero H2 inside the article (the only H2 is the CTA 'Ready to talk it through?'), date shown as 'Sep 17, 2026, 12:00:00 PM', no TL;DR.  
Evidence: Live H outline: H1, H2 'Ready to talk it through?', H3 'What do you need today?'. data-discovery-and-classification has 4 content H2s. The /blog index repeats the tag list inside each link text.  
Fix: themes/vaf/modules/vaf-blog-post.module (date format: use 'MMM d, yyyy'); for imported posts add subheads and a summary bullet list via brands/vanausdall.blog.json bodyHtml; themes/vaf/templates/vaf-blog-listing.html: keep tags out of the anchor text.

**SEO-038** | /, /about, /locations/*, /services/*, /case-studies/*  
What: Image alt text: heroes reuse the H1 or a section heading as alt, industry cards use the bare industry name, and several content images have an empty alt.  
Evidence: solutions-information hero alt 'Information Technology', solutions-communication 'Unified Communications', copy-print 'Copy Print Solutions in Indianapolis', managed-it second image 'What you get, and what it rests on', star-financial hero 'STAR Financial Bank case study'. Home industry cards alt 'Education', 'Healthcare', etc.; home case-study and blog thumbnails alt ''; about careers-1200.jpg alt ''; star-financial healthcare-process-1200.jpg alt ''. scripts/vaf_build.py rhythm() writes the heading as alt when none is set. The about and locations hero alts are descriptive and good.  
Fix: brands/vanausdall.overrides.pillars.json and brands/vanausdall.overrides.services.json: set sections[hero].image.alt to a description of the picture; scripts/vaf_build.py rhythm() line ~108: stop defaulting alt to the heading and leave decorative images alt=''.

**SEO-039** | /contact, /case-studies/star-financial, /locations/*, /services/copy-print-solutions  
What: Repeated blocks inflate pages with the same copy: the 'Industries we serve' tab block (8 industry blurbs) appears on 5 pages including contact, and customer testimonials are recycled across home, solutions, managed-it, about, locations. Pairwise shingle overlap among distinct body copy is low (the highest is case-study vs contact at 26% containment, caused by this block).  
Evidence: Identical lines of 12+ words appear on 5 pages ('Banks and credit unions inherit expired leases...', 'Reliable, protected information is patient safety...', 'Schools are tasked with developing the brightest minds...'). Six-word shingle containment: star-financial vs contact 0.26, solutions vs copy-print 0.19, indianapolis vs fort-wayne 0.11.  
Fix: Remove the 'markets' tabs section from brands/vanausdall.overrides.* compose lists for contact.html and case-studies/*.html; pick distinct testimonials per page.

**SEO-040** | brands/vanausdall.llms.txt and scripts/vaf_launch_files.py  
What: An llms.txt is being generated, which guardrails.md says not to build (Google ignores it). Its descriptions are truncated copies of meta descriptions.  
Evidence: brands/vanausdall.llms.txt entries end mid-sentence: '...a roadmap of what to.', '...presses, finishing.', '...inside our 57,000-square-foot Indianapolis.', and repeat the truncated /solutions meta.  
Fix: scripts/vaf_launch_files.py: drop the llms.txt generator; delete brands/vanausdall.llms.txt.

**SEO-041** | /company-facts and /training  
What: company-facts, the page that carries the checkable facts, has no inbound link from any page or menu; /training is titled 'About, Indiana' and linked from /about with the anchor 'About'.  
Evidence: Inbound-link scan over all 169 local pages and the brand nav: only company-facts has zero inbound links (referenced only in brands/vanausdall.llms.txt). /about links /training with the anchor text 'About'; its title is 'About, Indiana | Van Ausdall & Farrar'.  
Fix: brands/vanausdall.overrides.home.json seal 'facts' footnote and brands/vanausdall.content.json pages[about.html] section 'Measured, not claimed': link to company-facts.html; brands/vanausdall.content.json pages[training.html].title and the about link label.

**SEO-042** | /locations/fort-wayne and /locations/indianapolis  
What: Some location FAQ items are not city-specific, which weakens them as self-contained local answers: the Fort Wayne FAQ includes 'How is managed IT different from IT support?', and the Indianapolis FAQ includes 'Who is Van Ausdall & Farrar?' and 'How much does it cost?'.  
Evidence: Fort Wayne FAQ has 7 questions, Indianapolis 7 (parsed from the live FAQPage blocks). The city-specific ones ('Where is VAF's Indianapolis office?', 'How fast is service in Indianapolis?', 'Which areas does the Fort Wayne office cover?') are good.  
Fix: brands/vanausdall.overrides.locations.json keys 'locations/fort-wayne.html' and 'locations/indianapolis.html' faq items: keep only city-specific Q and A.

**SEO-043** | /partners  
What: Partner logo tiles use the bare brand names as alt (acceptable) but the marquee duplicates each logo with an empty alt, so the DOM holds 68 images for 24 partners (24 empty-alt duplicates); H1 'World-class partnerships, by pillar.' has no category term.  
Evidence: Parsed images: 68 on partners (24 with an empty alt: the marquee duplicates), 67 on home (32 with an empty alt).  
Fix: brands/vanausdall.overrides.* partners section heading; H1 recommended: 'Technology partners behind VAF's IT, phone, print and document services'.

**SEO-044** | /robots.txt, /sitemap.xml (staging)  
What: Staging is correctly noindexed (meta robots noindex, nofollow on every page, plus x-robots-tag: none). robots.txt is the hs-sites default and sitemap.xml lists only /blog. Launch gate: remove both signals.  
Evidence: Parsed robots meta on 15 pages: 'noindex, nofollow' on all but /blog; sitemap.xml has 1 <loc>.  
Fix: scripts/vaf_build.py NOINDEX constant and scripts/vaf_blog_import.py NOINDEX; domain connection removes the header. Keep on the launch checklist.

**SEO-045** | /locations/indianapolis, /locations/fort-wayne  
What: The two location pages carry the service area text but not 40 to 60 word answers either; Fort Wayne and Indianapolis open with city facts (52 and 31 words) rather than the question 'Who services copiers and IT in <city>?'.  
Evidence: First paragraph: Fort Wayne 'Fort Wayne is Indiana's second most populous city, the Allen County seat at the meeting of the St. Joseph, St. Marys and Maumee rivers...'.  
Fix: brands/vanausdall.overrides.locations.json keys 'locations/fort-wayne.html', 'locations/indianapolis.html' hero subhead.

## Verified and passing

- Exactly one H1 on every crawled page (16 of 16 rendered pages; the 404 post shows the error H1).
- Canonical present and self-referencing on every page except /blog; og:title, og:description, og:image, og:url and twitter:card present; every og:image URL returns 200.
- Staging noindex: meta robots 'noindex, nofollow' on all pages except /blog, plus 'x-robots-tag: none' from the domain. Nothing else restricts indexing.
- No duplicate titles or meta descriptions across the 169 local pages. Titles are 30 to 60 characters on 168 of 169 (company-facts is 69).
- Phone (317) 634-2913 is identical on every page and always a tel: link. Contact, Indianapolis and Fort Wayne pages show a full address and match their LocalBusiness markup; Fort Wayne markup (1241 N Wells Street 46808, +1-260-432-1547) matches the visible text.
- All 13 FAQPage blocks have every question and answer present in the page DOM (collapsed <details>, not hidden by script). No FAQPage claims a Q or A that is not on the page.
- BreadcrumbList JSON-LD matches the visible breadcrumb trail on the pages that have one; no BreadcrumbList on the home page (correct). Blog posts and /blog lack it (SEO-036).
- Redirect map: all 171 page targets exist in the local build; 25 sampled targets all return 200 on staging; no chains and no two-step loops. Defects are the identity rows and the missing blog rows (see SEO-005, SEO-006).
- Internal links on the 15 crawled non-blog pages: no 404 targets from the nav, footer, or main body except blog URLs (SEO-003, SEO-012) and the legacy paths inside imported post bodies (SEO-007). No bare 'learn more' or 'click here' anchors found; the home 'See the service' anchors carry the pillar name in the link text.
- Em dashes: none in any crawled page text.

## Redirect map sample (25 rows, seed 7)

| Old URL | New URL | Target in local build | Target on staging | Identity row |
|---|---|---|---|---|
| /fort-wayne/network-infrastructure-in-fort-wayne-in | /locations/fort-wayne-network-infrastructure | yes | 200 | no |
| /columbus/business-telephone-systems-in-columbus-in | /locations/columbus-business-telephone-systems | yes | 200 | no |
| /information/managed-it-services | /services/managed-it | yes | 200 | no |
| /kiosk-demo | /solutions | yes | 200 | no |
| /bloomington/network-carrier-solutions-in-bloomington-in | /locations/bloomington-network-carrier-solutions | yes | 200 | no |
| /case-studies/aspire | /case-studies/aspire | yes | 200 | YES (loop) |
| /process/content-management | /services/content-management | yes | 200 | no |
| /case-studies/echo-engineering | /case-studies/echo-engineering | yes | 200 | YES (loop) |
| /industries/government-technology-solutions | /industries/government | yes | 200 | no |
| /south-bend/business-phone-systems-in-south-bend-in | /locations/south-bend-business-phone-systems | yes | 200 | no |
| /business-continuity-compliance | /services/business-continuity | yes | 200 | no |
| /policies/terms-of-service | /policies/terms-of-service | yes | 200 | YES (loop) |
| /contact | /contact | yes | 200 | YES (loop) |
| /best-in-class-partners | /partners | yes | 200 | no |
| /case-studies/city-of-anderson | /case-studies/city-of-anderson | yes | 200 | YES (loop) |
| /knowbe4/start-free-phishing-security-test | /services/knowbe4-start-free-phishing-security-test | yes | 200 | no |
| /knowbe4/free-phish-alert-button | /services/knowbe4-free-phish-alert-button | yes | 200 | no |
| /case-studies | /case-studies | yes | 200 | YES (loop) |
| /cyber-security-assessment | /services/cyber-security-assessment | yes | 200 | no |
| /case-studies/city-of-bloomington | /case-studies/city-of-bloomington | yes | 200 | YES (loop) |
| /process/managed-print-centers | /services/managed-print-centers | yes | 200 | no |
| /knowbe4/get-free-email-exposure-check | /services/knowbe4-get-free-email-exposure-check | yes | 200 | no |
| /business-security-systems | /services/business-security-systems | yes | 200 | no |
| /process/voice-processing | /services/voice-processing | yes | 200 | no |
| /case-studies/shiel-sexton | /case-studies/shiel-sexton | yes | 200 | YES (loop) |

Non-identity old URLs return 404 on staging because the redirects are not yet imported into HubSpot; that is expected until launch. 8 of the 25 sampled rows are identity rows (SEO-006).
