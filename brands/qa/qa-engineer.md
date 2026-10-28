# QA engineer report: Van Ausdall & Farrar staging site

Site: https://50498425.hs-sites.com (live staging). Source audited: themes/vaf (css/vaf.css, js/vaf.js, modules/*.module). Date: 2026-10-28.

Scope: home in full detail, then /about, /contact, /partners, /solutions, /solutions-information, /solutions-communication, /solutions-process, /services/managed-it, /locations/indianapolis, /case-studies/tippecanoe-school-corporation, /blog, /blog/data-discovery-and-classification at 1440, 1024 and 390 wide. Chromium (WebM hero video). Every finding below was verified in a browser; screenshots and measurements are in /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/.

## Method
- Slow scroll of each page so scroll-reveal runs, viewport-sized screenshots (/tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/<page>_<d|t|m>/NN.png, contact sheets in sheets/) viewed one by one for home, and for the other pages at 1440 plus the measured problems at 1024 and 390.
- In-page measurement (measure.js, extras.js): horizontal overflow, text-box vs button-box centring, heading line counts and orphans, heading and lead alignment per section, card row heights, image natural vs rendered size, tap targets, font sizes, contrast (WCAG ratio for every text node), overlaps, header and bottom-bar geometry.
- Network and console on every load, every internal and external href fetched (194 distinct), in-page anchor jump test, Tab key walk (42 stops on home), mobile menu open test.
- To separate "live is old" from "source is wrong", the local css/vaf.css was injected in place of the live template_vaf.min.css and the home page re-measured.

## Read this first
1. **The live stylesheet is behind the repo.** Commit b691aa1 ("center buttons, stop orphan words, fix hero service card", css lines 868-875) is not in the live template_vaf.min.css (76 KB live vs 81 KB local). The client complaints about button text not centred and one-word last lines are mostly this. With the local CSS injected, hero card buttons are centred (dx 0) and home desktop orphan paragraphs go from 7 to 1. Findings affected carry deploy_status = fixed_locally_pending_deploy. Deploy first, then re-test.
2. **Three blockers remain after that deploy** (QE-01 invisible mobile Call pill, QE-02 invisible stats on /about, QE-03 /blog on the wrong theme). QE-01 is still broken with the local CSS.
3. Alignment, repeated layout and heading length are source problems, not deploy lag. The alt-background left-align rule (vaf.css 861-864) is the cause of the flip-flopping headings.

## What passed
- No horizontal overflow on any tested page at 1440, 1024 or 390 (docW equals viewport everywhere).
- No console errors; the only warning is a headless WebGL fallback notice. No broken or empty images (0 on all pages). No stretched images (all object-fit cover/contain, aspect ratio intact).
- No uneven card heights in any row (grid stretch works); no 4xx/5xx sub-resource responses.
- Forms render and all inputs are labelled (HubSpot fields 48px high).
- Keyboard focus: a 2px blue outline shows on all 42 tab stops on home (3.3:1 on the dark hero, passes the 3:1 UI minimum). Skip link present.
- Anchor links (/about #why, case-study TOC): none land under a header; they land 200 to 230px down because the header does not stick (QE finding on sticky).
- Hero video plays from WebM, loops, muted, pause button present.
- Mobile menu opens, all 39 links are at least 44px tall.

## Notes (not counted as bugs)
- Pillar pages /solutions-information, /solutions-communication, /solutions-process and the /solutions card wall look like the older build (5-line H1 "Information Technology Services for Indianapolis Businesses", legacy blurbs such as "Data Quality vs. Data Quantity" with raw "Tags: ... Posted in:" text and the heading and body swapped, 36 cards with titles cut mid-word like "...Tool Servi"). Noted only, as instructed.
- Social links (Facebook, Instagram) return 400/429 to a script because of login walls; they were not treated as broken.
- The live blog has 29 listing pages; only page 1 and one post were audited.

## Findings

### BLOCKER

**QE-01** | all pages | 390 (and any width <=767)
- Selector: `.pv-sticky .b (nav.pv-sticky > a.b "Call VAF")`
- What: The mobile bottom bar has two pills. The right one ("Call VAF") is white text on a white background, so it is an empty white pill. Visitors on phones cannot see or find the call button on any page.
- Evidence: Computed in Chromium: background rgb(255,255,255), color rgb(255,255,255), box 181x48 at x=199,y=786. --chrome-bg resolves to #fff outside the dark hero. Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_m/05.png (right pill blank). Still broken with the local vaf.css loaded in place of the live sheet.
- Fix: themes/vaf/css/vaf.css line 578: `.pv-sticky .b{background:var(--chrome-bg);color:#fff}` -> `.pv-sticky .b{background:#0f1e33;color:#fff}` (same fix already used for `.pv-sl > button` near line 847).

**QE-02** | /about | 1440, 1024, 390
- Selector: `section.vaf-stats.q-tone-dark .pv-stat > b and > span`
- What: The four stat cards (1914, 93.4, SOC 2, 57,000) are white text on cream cards, so the numbers and captions are invisible. A dark band shows four blank cream boxes.
- Evidence: Computed contrast 1.07:1 (fg rgb(255,255,255) on bg rgb(250,247,239)), font 50px. Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/about_stats.png and /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/about_d/00.png (top-right tile). Contrast script found 8 failing elements on /about d and m, 0 on every other page.
- Fix: themes/vaf/css/vaf.css line 811 gives every .pv-stat `background:var(--card)` while line 139 forces white text in .q-tone-dark. Add `.q-tone-dark .pv-stat{background:rgba(255,255,255,.06);box-shadow:none}` (or fix in themes/vaf/modules/vaf-stats.module/module.css).

**QE-03** | /blog | 1440, 1024, 390
- Selector: `body.hs-elevate-* header/footer, h1.hs-elevate-h1, h2.hs-elevate-card--blog__heading`
- What: The blog listing is not on the VAF theme. It renders HubSpot default "Elevate": header menu "Home / Products / Pricing / Blog / Company" with a "Get started" button, placeholder copy "A brief introductory description of your blog and the topics covered at a high level...", a dark-navy Elevate footer with LinkedIn/Facebook/X/Instagram/TikTok icons and "Privacy Policy / Legal", and generic social links to facebook.com and twitter.com. Individual posts do use the VAF header and footer.
- Evidence: Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/blog_d/00.png. DOM classes hs-elevate-*. linkcheck: https://www.facebook.com and https://www.twitter.com on /blog. The local template themes/vaf/templates/vaf-blog-listing.html exists but is evidently not the live listing template.
- Fix: HubSpot Settings > Website > Blog > Templates: set Listing template to the one built from themes/vaf/templates/vaf-blog-listing.html (layout themes/vaf/templates/layouts/vaf-base.html) and replace the placeholder description.

### MAJOR

**QE-04** | / (home) | 1440
- Selector: `section#articles .vr__link (blog card 1)`
- What: The first card in "Latest from the VAF blog" links to a URL that returns 404.
- Evidence: GET /blog/print--copy-solutions-where-document-workflows-start?hsLang=en = 404. The real post is /blog/print-copy-solutions-where-document-workflows-start (double hyphen typo). Found by fetching all 194 distinct internal and external hrefs from 13 pages.
- Fix: brands/vanausdall.overrides.home.json (and brands/vanausdall.blog.json): fix the slug to print-copy-solutions-where-document-workflows-start, then rebuild the home page; field lives in themes/vaf/modules/vaf-related.module card link defaults.

**QE-05** | all pages (verified on /, /about, /contact, /partners, /solutions, /services/managed-it, /case-studies/..., /blog/...) | 1440, 1024, 390
- Selector: `header.q-header`
- What: The header is declared position:sticky but does not stick. It scrolls away with the page. The JS that folds the utility bar after 80px, and html{scroll-padding-top:130px}, assume a header that stays, so in-page anchors land 200 to 230px below the top of the viewport.
- Evidence: At scrollY=2500 the header rect top is -2500 (bottom -2418) at 1440 and 390. Cause: header.q-header sits inside two wrapper divs (div.hs_cos_wrapper > div) that are exactly the header height (82px), so sticky has no room to travel. Anchor test: target top = 204..230px after click (case study #the-objective, #the-strategy). Still true with local CSS.
- Fix: themes/vaf/css/vaf.css near line 147: add `.hs_cos_wrapper:has(> .q-header), div:has(> .hs_cos_wrapper > .q-header){display:contents}` or make the wrapper itself sticky; then lower html{scroll-padding-top} (line 228) to the real header height.

**QE-06** | / (home), /partners, /about, /contact, /solutions, /services/managed-it | 1440
- Selector: `.q-section.q-bg-alt .pv-center, .vaf-head (vaf.css 861-864) plus module heads`
- What: Section headings flip between centered and left-aligned with no logic. Left vs centered follows the background colour, not the content. Home at 1440 reads C L C C C C C L C L C C L C C L: Checklist (alt) left, Flow (alt) centered, Case cards (alt) left, Map (alt) left, FAQ (alt) centered, Contact left. /partners alternates Center, Left, Center, Left for Information, Communication, Print, Process partners. /about has 7 of 12 section heads left. The header element on the checklist has class pv-center but renders left. This is the "headings left that should be centered and vice versa" complaint.
- Evidence: Measured text position vs .q-container centre per section (extras.js). Home 1440 sequence: hero L, wheel C, checklist L (offset -263px), ba C, flow C, hot C, seal C, case cards L (-392), tabs C, map L (-348), voices C, CTA C, articles L (-356), film C, FAQ C, contact L (-445). /partners: cards C, cards L*, cards C, cards L* (* = alt bg). At 1024 the same sections are all centered because the rule starts at min-width:1025px, so the layout jumps at 1025. Screenshots /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_d/02.png, 09.png, 11.png and /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/partners_d/00.png.
- Fix: themes/vaf/css/vaf.css lines 861-864 (`@media(min-width:1025px){.q-section.q-bg-alt > .q-container > .pv-center,.q-section.q-bg-alt .vaf-head{align-items:flex-start;text-align:left;...}}`): delete it. Pick one rule: intro heads centered; left only inside true split layouts (vaf-map, vf-ct form, vaf-detail). Make vaf-related head (themes/vaf/modules/vaf-related.module/module.css) and vaf-resources/vaf-services heads follow the same rule.

**QE-07** | / (home), /contact, /about, /solutions, /services/managed-it, /locations/indianapolis | 1440
- Selector: `section.vaf-wheel, .vaf-ba, .vaf-flow, .vaf-hot, .vaf-seal, .vaf-tabs, .vf-vid, .vaf-related x2`
- What: The same layout repeats section after section. 10 of 18 home sections use the identical stack: eyebrow, centered 2-line H2, centered grey lead, then a wide widget. Two vaf-related bands are identical (left H2 + right small lead + 3 image cards, both on the alt background): "Results on the record" and "Latest from the VAF blog". /contact stacks three left-H2-plus-right-lead card grids in a row (Where to go next, Industries we serve, Our offices). /services/managed-it and /locations/indianapolis reuse the same cards > proof > ba > flow > detail > testimonials > FAQ > form spine as the home page.
- Evidence: Section signature table from extras.js (home_d_x.json). Background rhythm on home: white, white (partners), white (wheel), alt, dark, white, alt, white, dark, alt, white, alt, white, white (CTA), alt, white, alt, white. Screenshots /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/contact_d/00.png, /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/contact_d/01.png, /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_d/09.png vs 14.png.
- Fix: Vary the module mix in the page content (brands/vanausdall.overrides.home.json and the other page overrides): merge the two vaf-related bands into one tabbed or 2-up block, move one of them to a dark or image band, alternate widget side (wheel left/card right, then card left/visual right) in themes/vaf/modules/vaf-wheel.module, vaf-hotspots.module, vaf-tabs.module, and give vaf-cta a coloured band.

**QE-08** | / (home) | 1440, 390 | status: fixed_locally_pending_deploy
- Selector: `section.vaf-hero .fcard.b .links a (Request support, Order supplies, IT support, Call (317) 634-2913)`
- What: The four quick-link buttons inside the "Already a customer?" hero card are boxes with left-aligned text, not centered. On desktop the label sits 3 to 24px left of centre; on mobile the 296px wide boxes put the label 69 to 100px left of centre. "Call (317) 634-2913" wraps to two lines inside a 144px box at 1440. They use a 10px radius while every other button is a pill (999px). The hero ghost link has a different height (44px) than the primary CTA (52px).
- Evidence: Measured text bbox centre vs button box centre: dx -3, -9.4, -24.2, -9.1 at 1440; -79, -85.4, -100.2, -69 at 390; lines=2 for the Call link at 1440. Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_d/00.png. THIS IS FIXED IN LOCAL SOURCE (commit b691aa1, css lines 868-872: justify-content:center;text-align:center;white-space:nowrap): loaded the local vaf.css into the live page and re-measured, dx=0 and lines=1. The live template_vaf.min.css (76 KB) predates that commit (local is 81 KB).
- Fix: Deploy themes/vaf/css/vaf.css (commit b691aa1) to HubSpot. Also set border-radius:999px for `.pv-lh .fcard.b .links a` in vaf.css line 656 if pills are wanted.

**QE-09** | / (home), /solutions, /partners, /about, /contact, /services/managed-it | 1440, 1024, 390 | status: fixed_locally_pending_deploy
- Selector: `p.q-lead, p.vf-chk__intro, p.vf-chk__msg, .vaf-hero .fcard p, section.vaf-hot p.q-lead, li`
- What: Single-word last lines (orphans) on lead paragraphs. Home: "Center." (four pillars lead), "each." (floor plan lead), "eighty." (checklist lead), "to." (checklist card message), "5." (hero card "...7 to 5."). Count of 2+ line paragraphs ending in one word, live: home 7, /solutions 24, /partners 11, /about 6, /contact 3, solutions-process 6.
- Evidence: extras.js paragraph orphan scan (data/*_d_x.json). Screenshots /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_d/01.png, 02.png, 05.png. Local vaf.css adds `p,li,.q-lead,.vc__copy,.fcard p{text-wrap:pretty}` (line 874); with local CSS injected the desktop home count drops from 7 to 1 and mobile still has 4 (stacked address cards, testimonial, contact lead). Not on live yet.
- Fix: Deploy vaf.css line 873-874 (text-wrap:pretty); extend the selector list with `.vf-chk__msg,.vf-faq__a,.vr__copy,.vaf-hot p,.vaf-wheel p,.vf-ct p` and `address,.vaf-locations p` for the cases still orphaning.

**QE-10** | / (home) | 390
- Selector: `section.pv-lh.vaf-hero h1.q-h1`
- What: The home H1 wraps to 4 lines on a phone ("Everything / your business / runs on, under / one roof."), 3 lines at 1440 and 1024. The H1 on other pages is 3 to 5 lines: /about 3 (1440) and 4 (390); /services/managed-it 4 lines at all widths; /locations/indianapolis 4 lines at 1440 and 1024; /solutions-information 5 lines at 1440 and 390 (older-build pillar, note only).
- Evidence: Measured line counts: h1 42px in a 350px column (mobile), 66.24px in a 621px (home) or 562px (split hero) column at 1440. Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_m/00.png and /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/services_managed-it_d/00.png.
- Fix: themes/vaf/css/vaf.css line 805/822: `.q-h1{font-size:clamp(40px,4.6vw,68px)}` and mobile `.q-h1{font-size:42px}`: cap at 34px under 480px (clamp(30px,8.4vw,36px)), and for `.vaf-hero--split .vaf-hero__copy` (themes/vaf/modules/vaf-hero.module/module.css) widen the copy column or drop to clamp(36px,3.6vw,56px) so H1 stays at 3 lines max.

**QE-11** | / (home), /about, /services/managed-it, /case-studies/tippecanoe-school-corporation | 390
- Selector: `h2.q-h2 (wheel, vf-chk__h, vaf-ba, vaf-flow, vaf-faq__heading, vcs__h)`
- What: Section H2s run to 3 lines on mobile: home "Information, communication, print and process, from one partner", "Six questions from the Technology Strength Assessment", "Drag to see what changes when the office has one number to call", "Four stages, and every one of them hands you something"; /about "From an Edison dealership to Indiana's largest office technology provider"; /services/managed-it "Drag to compare break-fix IT with a managed partnership". The case study H2 class vcs__h is 4 lines at 390 and 5 lines at 1440 (a full sentence used as a heading).
- Evidence: Measured 3 lines at 27.3px in a 350px column (home 4 headings), vcs__h 42px in a 487px column = 5 lines at 1440, 28px = 4 lines at 390. Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/home_m/01.png and /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/case-studies_tippecanoe-school-corporation_d/00.png.
- Fix: themes/vaf/css/vaf.css line 838-841: `.q-section .q-h2{font-size:clamp(30px,3.1vw,44px)!important}` and the mobile override `clamp(26px,7vw,32px)` -> `clamp(22px,6vw,27px)`; shorten the long headings in brands/vanausdall.overrides.*.json (keep under ~48 characters); for the case study set `.vcs__h{font-size:clamp(26px,2.6vw,36px);max-width:none}` in themes/vaf/modules/vaf-casestudy.module/module.css.

**QE-12** | / (home), /about, /solutions | 1024
- Selector: `h3.vr__title (vaf-related, vaf-resources cards)`
- What: Card titles in the 3 and 4 column card rows wrap to 3 lines at 1024 and leave one-word last lines: "Tippecanoe School / Corporation", "Print & Copy Solutions: Where Document Workflows Start" (3 lines), "Data Discovery and Classification: Find Your Sensitive Data" (3), "Limit the Use of My Sensitive Personal Information" (3), "Software Drivers and Documentation Downloads" (3, orphan Downloads). The /solutions page has 10 headings of 3+ lines at 1024.
- Evidence: Measured width 241px at 20px bold at 1024, 20px/1.3. /solutions at 1024 = 10 headings >=3 lines. Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/home_t/04.png.
- Fix: themes/vaf/modules/vaf-related.module/module.css line 14 `.vr__title{font-size:20px}` -> `font-size:clamp(17px,1.9vw,20px);text-wrap:balance`, and switch the grid to 2 columns between 768 and 1100px.

**QE-13** | /blog/data-discovery-and-classification | 1440, 1024, 390
- Selector: `article body a[href] (7 links)`
- What: The blog post contains 7 internal links that 404: /ai, /document-management, /information/managed-it-services, /network-security, /get-started, /blog/it-solutions-for-healthcare-hipaa-technical-safeguards, and the PDF /pdf/pr/2026/202609%20Data%20Discovery%20and%20Classification.pdf (the "View Full Press Release (PDF)" button).
- Evidence: Fetch status 404 for each (data/links.json). Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/blog_data-discovery-and-classification_d/00.png shows the PDF button and inline links.
- Fix: brands/vanausdall.blog.json / brands/vanausdall.blog-enrich.json: rewrite the legacy internal links to live URLs (/solutions-information, /services/managed-it, /services/cybersecurity, /contact, /services/document-management, /services/ai-consulting) and upload the PDF to HubSpot Files or drop the button.

**QE-14** | /blog | 1440
- Selector: `article cards (hs-elevate-card--blog)`
- What: Page 1 of the blog shows the same post three times ("Print & Copy Solutions: Where Document Workflows Start", slugs ...start, ...start-1, ...start-2), one of them as the featured hero card. The listing shows 29 pages, so more duplicates are likely.
- Evidence: Hrefs on /blog: /blog/print-copy-solutions-where-document-workflows-start, ...-start-1, ...-start-2. Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/blog_d/00.png.
- Fix: HubSpot Blog posts: unpublish or 301 the two duplicates (-1 and -2); check brands/vanausdall.blog-import.state.json for double imports.

**QE-15** | all pages with the footer (verified /, /about, /partners, /solutions) | 1440, 1024, 390
- Selector: `.q-footer .q-footer-legal (css line 342)`
- What: The copyright and Privacy / Terms / Cookie row has no side padding. At 1440 it starts at x=60 while the rest of the footer content starts at x=100; at 1024 and 390 the copyright text is flush against the left screen edge (x=0) and the Cookie link runs to the right edge.
- Evidence: Measured: legal container x=60,w=1320 (content columns x=100) at 1440; at 1024 legal items start x=0; at 390 first item x=0 and "Terms of service" x~5. Cause: `.q-footer-legal{...padding:18px 0 22px}` overrides the .q-container padding. Screenshots /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/home_t/05.png (bottom-right tile), /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/home_m/07.png.
- Fix: themes/vaf/css/vaf.css line 342: change `padding:18px 0 22px` to `padding:18px 40px 22px` (and `padding-left:20px;padding-right:20px` inside the max-width:767px block).

**QE-16** | / (home), /services/managed-it | 1440, 1024
- Selector: `section.vaf-flow .vaf-flow__out`
- What: In the four-stage stepper, the "Produces" block is bottom-aligned (margin-top:auto). Stage 4 ("Alerts handled before they become tickets") has a two-line value, so its dashed divider and PRODUCES label sit 21px higher than stages 1 to 3 and the four columns do not line up.
- Evidence: .vaf-flow__out heights 52, 52, 52, 73px; tops y=5361, 5361, 5361, 5340 at 1440. Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_d/05.png.
- Fix: themes/vaf/modules/vaf-flow.module/module.css line 89: replace `.vaf-flow.is-js .vaf-flow__out{margin-top:auto}` with `margin-top:0` and give the button `min-height` or use grid rows `grid-template-rows:subgrid` so the divider aligns; or set `.vaf-flow__out{min-height:76px}`.

**QE-17** | all pages with a mobile menu | 390, 1024
- Selector: `a.q-mnav-cta (mobile menu "Schedule a consultation")`
- What: The open mobile menu CTA is near-black text on the blue pill, which fails contrast. Everywhere else the button label is white.
- Evidence: Computed color rgb(11,13,16) on rgb(42,113,175) = about 3.8:1 at 16px/600. Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/menu_390.png.
- Fix: themes/vaf/css/vaf.css line 258/183: `.q-mnav-cta{color:var(--cta-fg)!important}` is overridden inside the panel; add `.q-mnav-panel > a.q-mnav-cta{color:#fff!important}` after line 184.

### MINOR

**QE-18** | / (home) | 1440
- Selector: `section.vaf-map .q-container`
- What: The offices map section has dead space. The heading and lead sit top-left, the three office cards are pushed to the bottom right of a tall map column, leaving about 430px of empty area at top right.
- Evidence: Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_d/11.png (cards start at y=537, heading block ends at y=300). Section height 1138px.
- Fix: themes/vaf/modules/vaf-map.module/module.css: align `.vaf-map__list` with `align-self:start` (top) or switch to a 2-column grid with the map on one side and heading + list stacked on the other.

**QE-19** | / (home), /about | 1440
- Selector: `section.vaf-testimonials + section.vaf-cta; section.vf-vid + FAQ`
- What: Two adjacent white sections (testimonials then the playbook CTA) have no divider or band, so there is about 220px of empty white space and the CTA floats with no container.
- Evidence: testimonials gapBot 110px + cta gapTop 110px; CTA section 491px tall with transparent background. Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_d/13.png.
- Fix: themes/vaf/css/vaf.css `.q-section.pv-cta`/themes/vaf/modules/vaf-cta.module/module.css: give the CTA a tinted or dark band (background var(--bg-alt) or navy) and reduce padding to 72px.

**QE-20** | / (home), /services/managed-it | 1440, 1024
- Selector: `section.vaf-partners (marquee) to next section`
- What: Large empty gap under the partner logo marquee: about 206px from the "Pause scrolling" link to the next eyebrow at 1440 and 1024 (152px at 390), because the partners section has 70px bottom padding followed by 110px top padding on the next section.
- Evidence: Measured pause button bottom to next eyebrow top = 206px. Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_d/01.png.
- Fix: themes/vaf/modules/vaf-partners.module/module.css: reduce padding-bottom to 24px, or give the next section a negative margin-top.

**QE-21** | / (home) | 1440
- Selector: `section.vaf-ba .vaf-ba__label ("DRAG TO COMPARE")`
- What: The slider divider line runs through the "DRAG TO COMPARE" label ("DRAG TO | COMPARE"), cutting the text.
- Evidence: Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_d/04.png at y~880.
- Fix: themes/vaf/modules/vaf-beforeafter.module/module.css: give the label `position:relative;z-index:3` above the divider or move it below the handle.

**QE-22** | / (home) | 1440
- Selector: `section.vaf-seal .vs__card (8 cards, 4 columns)`
- What: Card titles are one line in some cards and two in others ("Square feet of headquarters" vs "Years of IT / experience on staff"), so body text starts at different heights across the same row and the last card has extra empty space.
- Evidence: Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_d/08.png (row 2: body text starts at y=727 in cards 1-3 and y=704 in card 4).
- Fix: themes/vaf/modules/vaf-seal.module/module.css: give the title `min-height:2.6em` (two lines) or use subgrid rows so the body paragraph aligns.

**QE-23** | / (home) | 1440, 1024
- Selector: `section.vaf-tabs .vaf-tabs__panel`
- What: At 1024 the industry tabs keep a 300px vertical tab column beside the panel, so the panel text column is only about 260px next to a 219px image. At 1440 the Education panel leaves a large empty area under the image (image 352x263 in a 900px panel).
- Evidence: Measured panel 604px wide, image 219x163 at 1024; panel 900px, image 352x263 at 1440. Screenshots /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/home_t/03.png, /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_d/10.png.
- Fix: themes/vaf/modules/vaf-tabs.module/module.css: switch to the horizontal pill-tab layout (as on mobile) at max-width:1100px, and align the image to the vertical centre of the panel.

**QE-24** | / (home) | 1024
- Selector: `section#hero (vaf-hero) at 1024`
- What: The hero is 1284px tall at 1024 (1700px at 390): the two cards stack under the copy, so the first screen shows only the headline and the cards are a second screen away.
- Evidence: Section heights 767px (1440), 1284px (1024), 1700px (390). Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/home_t/00.png.
- Fix: themes/vaf/css/vaf.css line 659 (`@media(max-width:1024px){.pv-lh .q-container{grid-template-columns:1fr...}}`): keep 2 columns down to 900px, or hide the second card (.fcard.b) under 768px.

**QE-25** | / (home), all pages with the quick bar | 1440, 1024
- Selector: `.pv-sl (button "Already a customer?")`
- What: The fixed "Already a customer?" pill at bottom-left sits on top of page text at every scroll position. It hides the start of the Sources line in the seal section, the first line of the testimonial attribution, and the first footer column text.
- Evidence: Fixed at x=18,y=844,197x48. Screenshots /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_d/08.png (Sources line cut), 12.png (attribution), 17.png.
- Fix: themes/vaf/css/vaf.css pv-sl rules (line ~847): add `.pv-sl{left:auto;right:18px}` or collapse it to an icon-only 48px circle, and add padding-bottom to .q-section so text clears it.

**QE-26** | / (home) | 390
- Selector: `section.vf-chk .vf-chk__bar (0 of 6)`
- What: On mobile the checklist progress pill "0 of 6" is sticky and floats over the checklist rows, just above the bottom bar, covering the question text beneath it.
- Evidence: Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_m/05.png and /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/home_m/01.png (pill over "Does your company have a formal...").
- Fix: themes/vaf/modules/vaf-checklist.module/module.css: place the progress bar at the top of the list with `position:sticky;top:0` under the header, or only show it after the first check.

**QE-27** | all pages with a HubSpot form (/, /contact, /partners, /solutions-*, /services/managed-it, /locations/indianapolis, /case-studies/...) | 1440, 390
- Selector: `form .hs-button.primary.large`
- What: The form submit button is a rounded rectangle (6px radius) while all other CTAs are pills (999px), and it is a different weight of blue block against the pill "Call" button next to it.
- Evidence: Computed border-radius 6px, 581x48 (1440). The CSS rule `.q-form .hs-button{border-radius:999px}` (line 804) does not match the .vf-ct / .vf-lf wrappers. Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_d/17.png.
- Fix: themes/vaf/css/vaf.css line 804: add `.vf-ct .hs-button,.vf-lf .hs-button,.vf-ct input[type=submit],.vf-lf input[type=submit]{border-radius:999px}`.

**QE-28** | / (home), /about, /solutions | 390
- Selector: `button.vaf-hot__pin, footer a, .vr__link, input.vf-chk__in, a (breadcrumb Home)`
- What: Tap targets under 44px on mobile: hotspot pins 34 to 39px, every footer link 34px tall (about 30 links), breadcrumb links 24px, checklist checkbox 28px, card text links (.vr__link) 24px (the whole card is clickable through a ::after overlay, so those are mitigated). Footer social buttons are 44x40.
- Evidence: Measured by tap scan (data/home_m.json): vaf-hot__pin 38x38 / 34x34 x7; footer links 161x34 and 350x34; breadcrumb "Home" 39x24; vf-chk__in 28x28.
- Fix: themes/vaf/modules/vaf-hotspots.module/module.css `.vaf-hot__pin{min-width:44px;min-height:44px}` (draw the visible circle smaller); themes/vaf/css/vaf.css `.q-footer-links a{display:flex;min-height:44px;align-items:center}`; breadcrumb link `padding:10px 4px`.

**QE-29** | all pages | 390
- Selector: `.q-eyebrow, .vaf-flow__out-l, .vaf-flow__k, .vaf-wheel__k, .pv-cap, .vr__tag, .q-footer-head, .pv-legal-item, form labels`
- What: Text below 14px on mobile: eyebrows and tags 13px, "PRODUCES" label 11.5px, card kickers 12px, "Pause scrolling" 12.5px, footer column heads 12.5px, copyright and legal links 13px, form field labels 13px, SVG wheel labels 12px.
- Evidence: Font-size scan at 390: 12 to 13.5px on 20+ selectors on home (data/home_m.json smallText). 11.5px is the smallest (.vaf-flow__out-l, also at 1440).
- Fix: themes/vaf/css/vaf.css: set `.q-eyebrow,.vr__tag,.pv-cap{font-size:14px}` under 768px and themes/vaf/modules/vaf-flow.module/module.css line 30 `.vaf-flow__out-l{font-size:12.5px}` to 13px+.

**QE-30** | / (home), /services/managed-it | 390
- Selector: `a.q-btn (hero primary CTA), button.vaf-ba__sw.is-on`
- What: On mobile the hero primary button label wraps to 2 lines ("Take the Technology Strength / Assessment") inside a 72px pill, and the before/after toggle "Today, in most offices" wraps to 2 lines in a 44px pill.
- Evidence: Measured hero CTA 350x72, lines=2; vaf-ba__sw.is-on 170x44, lines=2. Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_m/00.png.
- Fix: themes/vaf/css/vaf.css line 33 `.q-btn{padding:16px 32px}` -> `padding:16px 20px` under 480px, and themes/vaf/modules/vaf-beforeafter.module/module.css `.vaf-ba__sw{padding:0 14px;font-size:13px}` or shorten the label to "Today".

**QE-31** | all pages | 390
- Selector: `body / .q-footer (bottom)`
- What: At the end of every mobile page a white strip (about 90px) shows under the footer, because padding for the fixed bottom bar uses the page background (white) while the footer is pale blue.
- Evidence: Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/home_m/07.png (white band under footer). docH 24368 vs footer end.
- Fix: themes/vaf/css/vaf.css line 292 area (`html{scroll-padding-bottom:72px}` and the mobile bottom-bar padding): apply the padding inside .q-footer (padding-bottom:88px) instead of on body.

**QE-32** | / (home), all pages | 1440, 1024, 390
- Selector: `section.pv-lh.vaf-hero img.vaf-hero__poster`
- What: The hero poster image is upscaled: natural 1097x617 shown at 1440x767 (1.31x), 780x438 at 1024 shown 1024x1284, 297x167 at 390 shown 390x1700. It is hidden by the video and scrim on desktop, but is soft for visitors whose video does not start (reduced motion, data saver).
- Evidence: img naturalWidth vs rendered width from the image scan. Requested hs-fs variants use width=1050 / 2100 but the file is hero-poster-2.jpg, 1097px wide.
- Fix: Upload a 2400x1000 poster in HubSpot Files (hero-poster-2.jpg) and set it in the home page vaf-hero module image field (brands/vanausdall.asset-map.json).

**QE-33** | /contact | 1440
- Selector: `section.vaf-resources "Where to go next" cards`
- What: Several solution cards have no description text (Managed IT Services Indianapolis, Copier Sales and Lease), so the card shows a large blank gap between the title and the "Open the page" link, and cards in the same row look uneven in content.
- Evidence: Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/contact_d/00.png (bottom-right tile).
- Fix: brands/vanausdall.content.json / overrides: add a one-sentence description to each card; or hide the description line and shrink card height with `.vr__card{min-height:0}` in themes/vaf/modules/vaf-resources.module/module.css.

**QE-34** | /partners | 1440
- Selector: `section.vaf-cards .pv-card (partner logo cards)`
- What: Partner card logos are inconsistent: Kofax and EFI have no logo, so their titles sit higher than neighbouring cards; Sophos, Square 9 and Microsoft logos are tiny and Ricoh sits in a black box; Fortinet and Elevate differ in visual weight.
- Evidence: Screenshots /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/partners_d/00.png and 01.png (Kofax and EFI cards, Square 9, Sophos).
- Fix: themes/vaf/modules/vaf-cards.module/module.css: give the logo slot a fixed `height:44px;display:flex;align-items:center` so cards without a logo keep the space, and normalise logo files in brands/vanausdall.asset-map.json (transparent PNG, same visual height).

**QE-35** | /about | 1440
- Selector: `section.vaf-tl .vtl__item (timeline)`
- What: The 7-item timeline renders as a row of 4 then a row of 3, so the second row ends early and the last slot is empty on the right.
- Evidence: Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/about_d/00.png (bottom-left tile): 1994, 2006, Today in the left 3 of 4 columns.
- Fix: themes/vaf/modules/vaf-timeline.module/module.html: pick columns from the item count (7 -> 1 horizontal scroll rail, or 4+3 centred), as the contract requires ("no orphan card in a last row").

**QE-36** | /about | 1440
- Selector: `section.vaf-resources "More from Van Ausdall & Farrar" (11 cards)`
- What: The last row of cards (2 cards) is centred while the rows above are 3 across and left aligned, so the final cards sit offset from the grid edges.
- Evidence: Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/about_d/02.png (cards at x=216 and x=507 while the grid starts at x=69).
- Fix: themes/vaf/modules/vaf-resources.module/module.css: use `justify-content:start` for the last row or `grid-template-columns:repeat(auto-fit,minmax(...))` with `justify-items:stretch`.

**QE-37** | /case-studies/tippecanoe-school-corporation, /blog/data-discovery-and-classification | 1440, 1024
- Selector: `h1.vf-art__h1; byline`
- What: The article H1 leaves one orphan word ("Corporation") on mobile and at 1440 uses a 820px column; the post byline shows the full time stamp "Oct 17, 2026, 12:00:00 PM".
- Evidence: h1 2 lines with orphan Corporation at 1440 and 390 (data/case-studies_*.json); byline text in blog post screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/blog_data-discovery-and-classification_d/00.png.
- Fix: themes/vaf/templates/vaf-blog-post.html: format the date with `|format_date("MMM d, yyyy")`; add `text-wrap:balance` to `.vf-art__h1` in themes/vaf/modules/vaf-article.module/module.css.

**QE-38** | / (home), all pages with the footer | 1024, 390
- Selector: `.q-footer-links.pv-two (Solutions column)`
- What: The footer Solutions column is two sub-columns whose rows do not line up (first starts 7px lower, wrapped items get uneven gaps, "Business phone systems" and "Copiers and printers" touch). At 1024 the columns are squeezed to 1 or 2 words per line ("Cloud / services", "Backup and / recovery", "Managed / print").
- Evidence: Screenshot /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/sheets/home_t/05.png (bottom-right tile) and /tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_eng/shots/home_d/18.png.
- Fix: themes/vaf/css/vaf.css `.q-footer-links.pv-two` and footer grid: `grid-template-columns:1.2fr 2fr 1.2fr 1.2fr 1fr` at 1024 and a uniform `gap:10px` plus `align-content:start` on both sub lists.

**QE-39** | all pages with a form | 1440, 1024, 390
- Selector: `script[src*=hsforms] (js.hsforms.net/forms/embed/v2.js)`
- What: The HubSpot forms script is requested twice and one request is aborted on every page that has a form (ERR_ABORTED). Forms still render and submit, so this is only wasted work.
- Evidence: requestfailed: https://js.hsforms.net/forms/embed/v2.js net::ERR_ABORTED on 11 of 13 pages; a successful second request follows (counters.gif OK).
- Fix: themes/vaf/modules/vaf-leadform.module/module.html and vaf-contact.module: remove the manual <script src=...v2.js> tag; the {% form %} tag already loads it.

**QE-40** | /blog | 390
- Selector: `a.hs-elevate-blog-listing__pagination-link`
- What: Blog pagination links are tiny: page numbers 11x18px and "Previous/Next" 9x28px on mobile; the first page number 44x18.
- Evidence: Tap scan on /blog at 390 (data/blog_m.json).
- Fix: Resolved when the blog listing is moved to the VAF template; give pagination links `min-width:44px;min-height:44px` in the new template css.

## Counts by severity
- Blocker: 3
- Major: 14
- Minor: 23
- Total: 40

## Top 10 fixes (in order)
1. QE-01: Fix the invisible mobile "Call VAF" pill (vaf.css line 578).
2. QE-02: Fix white-on-cream stat cards on /about (vaf.css line 811 vs 139).
3. QE-03: Put /blog on the VAF listing template (currently HubSpot Elevate with placeholder copy).
4. QE-08: Deploy the local "polish pass" CSS (commit b691aa1): centred buttons and text-wrap:pretty are not on live.
5. QE-06: Remove the alt-background left-align rule (vaf.css 861-864) and set one heading alignment policy.
6. QE-07: Break up the repeated centred-header-plus-widget stack and the duplicated vaf-related bands.
7. QE-10: Cap H1 and mobile H2 sizes so headings stop at 2 to 3 lines.
8. QE-11: Shorten long H2 copy and shrink mobile H2 size (vaf.css 838-841); fix 5-line case study H2.
9. QE-04: Fix the home blog card 404 slug and the 7 dead links in the blog post.
10. QE-05: Make the header actually sticky (wrapper divs are header-height) and fix scroll-padding.
