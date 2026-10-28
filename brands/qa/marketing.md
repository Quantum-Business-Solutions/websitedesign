# VAF website: marketing and conversion audit

Scope: live staging site https://50498425.hs-sites.com (checked 2026-10-28 with a cache-busting query), home in full at 1440 and 390 wide, plus /about, /partners, /contact, /solutions, /services/managed-it, /services/copy-print-solutions (live and local rebuild via `python3 scripts/vaf_build.py dry`), /locations/indianapolis, /case-studies/tippecanoe-school-corporation, /technology-strength-assessment, /blog, and four industry pages. Machine-readable findings: `brands/qa/marketing.json` (same ids). Nothing in the repo was edited except these two files; no git or HubSpot writes; no form was submitted.

Evidence files (screenshots and page text) are in the session scratchpad `/tmp/claude-0/-home-user-websitedesign/d80cf175-df55-553e-aaf9-081a1fd52f65/scratchpad/qa_mkt/`.

## Summary

**44 findings: 6 blocker, 23 major, 15 minor.**

The bones are strong: a clear brand promise, a real signature method (the Technology Strength Assessment), and unusually good proof (NPS 93.4 audited by CEO Juice, SOC 2, Mitel Gold, four numbered case studies). The site loses conversions in five places:

1. **The primary CTA overpromises.** The assessment is sold everywhere as 'ten to fifteen minutes online', but it is a callback form (F8). The header button is the secondary action (F9).
2. **Build and migration language reached visitors** on /solutions, /about, /case-studies and several proof blocks (F4 to F7).
3. **Proof is thin where buyers look for it**: first-name-only quotes recycled across pages, copier praise on IT pages, case studies with no named customer voice (F13 to F15).
4. **Objections go unanswered**: price, contract length, switching, downtime (F18, F19).
5. **Mobile is broken at the moment of intent**: the sticky 'Call VAF' button is white on white, and the Client Service Center is below the fold (F1, F16).

The em dash rule is clean: no em or en dashes appear in the visible text of every live page audited, in titles or meta descriptions, or anywhere in the merged page content and blog JSON (scanned for U+2014, U+2013 and ' -- ').

## Page scores (1 to 10)

| Page | Clarity | Proof | Conversion | What would make it a 10 |
|---|---|---|---|---|
| / (home) | 7 | 7 | 6 | Name the services and Indiana in the headline; one primary action in the hero; named, titled customer quotes; case results before the long interactive middle; objection FAQ (price, switching, contracts); real photography; page under 11,000px. |
| /about | 7 | 7 | 3 | A buyer CTA in the hero and a form before the careers CTA; delete the migration card dump; real HQ photo; attribute the Costco figure; leadership with photos and one named customer quote. |
| /partners | 6 | 6 | 4 | First-person voice (drop 'VAF says' and 'apologize'); attribute vendor claims (Gartner, 99.999%); one line on what each partner relationship means for the customer; assessment CTA tied to a pillar. |
| /contact | 6 | 5 | 5 | Form and a large tap-to-call button above the fold; three-step 'what happens next'; a reply time VAF has actually approved; consent line; topic captured as a real property; routes existing customers to support in one line. |
| /solutions | 5 | 4 | 4 | Delete the 57-card legacy dump; show twelve solutions only, each with one outcome line and a link; one named proof per pillar; a clear 'not sure where to start' path to the assessment. |
| /services/managed-it | 7 | 4 | 5 | Price model, contract term, switching steps and help desk response target answered on the page; a named customer IT quote (not copier praise); confirmed Sigmon quote; one proof device in the hero; a free phishing test as a soft offer. |
| /services/copy-print-solutions (live) | 4 | 4 | 4 | Publish the local rebuild; add the case study and calculator; fix the 30% claim. |
| /services/copy-print-solutions (local rebuild) | 7 | 6 | 7 | Remove '100+ Years' and 'Average' 30%; source the 30%; real Tippecanoe quote; fix the 404 article link; submit label 'Get your free print assessment' kept; add a lease-end-date qualifier. |
| /locations/indianapolis | 5 | 3 | 5 | A search-style headline ('Managed IT, copiers and business phones in Indianapolis'); Indianapolis customers and quotes; map, parking and entrance; same-day service proof tile; one form with a local promise. |
| /case-studies/tippecanoe-school-corporation | 7 | 5 | 5 | A named customer quote with title; before and after numbers with the timeframe; correct the 20% tile and the fleet math; a CTA that says 'Get the same assessment'; customer logo. |
| /technology-strength-assessment | 6 | 5 | 5 | A real self-scoring quiz or honest 'with an advisor' copy; one direction for the checklist; a sample scorecard image; single proof device; submit label that matches the promise. |
| /blog (index) | 2 | 2 | 1 | Assign the VAF listing template, write a real description, remove duplicate posts, add filters by pillar and a featured CTA to the assessment. |
| /industries/healthcare (bonus) | 6 | 6 | 5 | Healthcare-specific questions in place of the shared 'first ninety days'; a metric tile with a real number; a named quote from Johnson Memorial; a HIPAA statement VAF can stand behind. |

Scoring basis: clarity is the 5-second test and message hierarchy; proof is named, attributed, page-relevant evidence; conversion is one clear action, placement, form friction and microcopy.

## First 5 seconds on the home page

Today a visitor sees: eyebrow 'Business technology simplified, since 1914', H1 'Everything your business runs on, under one roof.', then a grey subhead that finally names IT, copiers, phones, document workflow and AI. The headline alone does not say what VAF sells, where, or to whom, and the hero then presents four actions (primary button, secondary link, an assessment card with a 'How it works' button, and a four-link Client Service Center card) beside four stat tiles. The promise is good; the first line hides it. See the rewrite below.

## Top 10 fixes, with replacement copy

1. **Fix the invisible mobile 'Call VAF' button (F1).** themes/vaf/css/vaf.css line 578: .pv-sticky .b{background:var(--navy,#0f1e33);color:#fff}. Label it 'Call (317) 634-2913' (content.json brand.sticky.secondary). Add a phone icon to the mobile header.
2. **Make the primary CTA honest and consistent (F8, F9).** Header button: 'Start with the assessment'. Hero primary: 'Get your Technology Strength Score'. Replace every 'ten to fifteen minutes online' with 'ten to fifteen minutes with an advisor' until a real quiz exists.
3. **Rewrite the home hero (F17).** Heading: 'One Indiana partner for <em>IT, phones, copiers and paper</em>.' Eyebrow: 'Indiana's largest full-service office technology provider, since 1914'. Primary 'Get your Technology Strength Score'. Secondary 'Talk to an Indianapolis expert'.
4. **Purge migration and reviewer language, and the legacy dumps (F4, F5, F6, F7).** Delete the 57-card section on /solutions (scripts/migrate_pages.py line 327) and the legal-page cards on /about (line 336). Reword the case-studies intro (content.py lines 889 and 892). Remove every 'from vanausdall.com' and 'Imported directly from' line.
5. **Theme the blog index and fix the 404 card (F2, F3).** Assign vaf blog-listing.html in HubSpot blog settings; description: 'Plain-English guidance on managed IT, security, copiers and print, phones and document workflow, from the Indiana team that has done it since 1914.' Home articles item 0 href -> blog/print-copy-solutions-where-document-workflows-start.html.
6. **Fix the forms: one real interest field, no prefilled textarea, a consent and reply line (F10, F11, F12).** Submit 'Talk to an expert' (general) or 'Start with my assessment' (assessment pages). Note: 'A person from the Indianapolis office replies. We use your details only to answer this request. Privacy policy. Prefer to talk? Call (317) 634-2913, Monday to Friday, 7:00am to 5:00pm.' Reply time only once VAF confirms it.
7. **Replace first-name testimonials with named, titled, matched ones (F13, F14).** Format: 'Name, Title, Organization, after a [service] call, [month year]'. One quote per service, matched to the page. Remove duplicate Elaine and 'The guy is totally awesome.' Confirm or drop the Steven Sigmon quote.
8. **Answer price, contract and switching on Managed IT and the home FAQ (F18, F19).** Home FAQ: 'What does it cost?' and 'How do we switch without downtime?' Managed IT FAQ: 'What does managed IT cost?', 'Are we locked in?', 'How do we switch from our current IT provider?', 'How fast do you respond to a ticket?' Placeholders marked [VAF to supply].
9. **Make the case study proof real (F15).** Customer-named quote with title, the 20% tile relabelled as the before-state, the $1M tied to a contract length, the 600 plus 200 versus 1,200 count checked, and a CTA 'Get the same assessment'.
10. **Make mobile and contact conversion work (F16, F20, F21).** Contact page: form and a big 'Call (317) 634-2913' button in the first screen; three-step next steps; Client Service Center link visible in the mobile first screen; About page gets a buyer CTA.

## Proposed rewrites

All copy below avoids em and en dashes and uses only facts already on record. Anything in square brackets needs VAF to supply or confirm; it must not ship as written.

### Home hero

Keys: `brands/vanausdall.overrides.home.json` > `index.html.sections[id=hero]` (showcase) and `[id=hero-light]` (clean); also `variants.press` if kept.

| Field | Replacement |
|---|---|
| eyebrow | Indiana's largest full-service office technology provider, since 1914 |
| heading | One Indiana partner for `<em>IT, phones, copiers and paper</em>`. |
| subhead | Van Ausdall & Farrar looks after the technology your office runs on, under one agreement and one Customer Care Center. Start with the Technology Strength Assessment and see what to eliminate, optimize and leverage. |
| primary.label | Get your Technology Strength Score |
| secondary.label | Talk to an Indianapolis expert |
| card_a | eyebrow 'Complimentary'; title 'Your Technology Strength Score'; body 'Information, print, process and communication, scored, with a written roadmap of what to eliminate, optimize and leverage.'; label 'See how it works' |
| card_b.body | Monday to Friday, 7:00am to 5:00pm. Requests are answered within 24 hours. |
| stats | 1914 Serving Indiana since; 93.4 Net Promoter Score, audited by CEO Juice; SOC 2 Certified service organization; 7 years Mitel Gold partner |

Why: it names the four things buyers search for (IT, phones, copiers, paper), says Indiana, keeps 'since 1914' as proof rather than the point, and reduces the hero to one primary action plus one human option. If the quiz is not built, set primary.label to 'Request your Technology Strength Assessment'.

### Top 3 CTAs

| # | Where | Today | Replacement | Key |
|---|---|---|---|---|
| 1 | Hero primary and header button | 'Take the Technology Strength Assessment' / header 'Schedule a consultation' | Hero: 'Get your Technology Strength Score'. Header: 'Start with the assessment' (href technology-strength-assessment.html). Consultation becomes a text link 'Talk to an expert' beside the phone number. | hero.primary in overrides.home.json; brand.cta in content.json |
| 2 | Every lead form submit | 'Schedule my consultation' (even under 'Start with the assessment') | General and contact pages: 'Talk to an expert'. Assessment pages: 'Start with my assessment'. Note under the button: 'A person from the Indianapolis office replies. We use your details only to answer this request. Privacy policy. Prefer to talk? Call (317) 634-2913.' | leadform.submit and .note; contact.submit and .note |
| 3 | Mobile sticky bar and case cards | 'Call VAF' (invisible) and 'Read more' | Sticky: 'Call (317) 634-2913'. Case cards: 'See how Tippecanoe cut 1,200 devices to 300', 'See the 90-day scanning project', 'See STAR Financial's results'. | brand.sticky.secondary; casecards.items[*] link label |

### Weakest section 1: /solutions legacy card dump

Delete the 57-card 'Every solution page, by pillar' section (`scripts/migrate_pages.py` line 327; `pages[file=solutions.html].sections[9]`). Replace with:

> **Free tools and guides**  
> Start with something you can use today.  
> Free phishing security test | Print cost calculator | 2026 CIO AI Playbook | Free print assessment

The remaining legacy URLs stay live or redirect; they do not need cards.

### Weakest section 2: /contact hero and 'what happens next'

Key: `brands/vanausdall.overrides.services.json` > `contact.html`.

> **Talk to a person at VAF.**  
> Tell us what you run and what is not working. We call you back to set a time. Existing customer? The Client Service Center is faster.  
> [Call (317) 634-2913]  [Existing customer? Get support]  
> (form in the right column)  
>  
> **What happens next**  
> 1. A person from the Indianapolis office reads your note and calls to set a time.  
> 2. If it is a new need, an advisor walks the Technology Strength Assessment with you.  
> 3. You get a written roadmap of what to eliminate, optimize and leverage.  
> Service request for a device you already have? The Client Service Center responds within 24 hours. [VAF to confirm the reply time for new inquiries before adding one.]

### Weakest section 3: home customer comments

Key: `overrides.home.json` > `sections[id=voices]`.

> **What customers wrote after a service call**  
> Comments collected by CEO Juice after service visits.  
> 'We always look forward to Jerome coming. He is kind and professional. We always know our problem will be resolved.' Stacy [Last initial], [Title], [Organization], after a copier service call, May 2026  
> [Add one quote per service from a named, permissioned customer: managed IT, phones, document conversion.]  
> Remove the second 'Elaine' quote and 'The guy is totally awesome.'

### Also rewrite: home seal band (internal language)

> **Eight facts you can check before you call.**  
> Each one has a source. Ask your advisor to show you.  
> Tile SOC 2: An independent audit of how we protect customer data. [VAF to confirm Type I or II and report period.]

### Also rewrite: Managed IT FAQ additions

Key: `content.json` > `pages[file=services/managed-it.html].sections[7]`.

> **What does managed IT cost?** One agreed monthly amount, based on the users and devices we manage and the security and support you choose. You see it in writing after the assessment, before you commit. [VAF to supply: typical range or what drives the price.]  
> **Are we locked in?** [VAF to supply: term, renewal and notice.]  
> **How do we switch from our current IT provider?** We start with the assessment and an inventory of what you run, then bring monitoring, backup and security online. [VAF to supply: password, vendor and documentation handover.]  
> **How fast do you respond to a help desk ticket?** [VAF to supply the managed IT target; the 24-hour figure on record is the Customer Care Center.]

## Buyer-journey fit

- **Awareness:** blog posts rank (the second-highest organic URL is a blog post) but have no in-article CTA (F29), and the blog index is unthemed (F2).
- **Consideration:** the pillar to service path works (wheel, nav, services pages) but the service pages repeat the same proof band and lack price, contract and switching content.
- **Decision:** proof is the weak link: unnamed quotes, narrative 'quotes' in case studies, no named customer voice. The consideration to decision step (case study to form) uses a mismatched submit label.
- **Existing customers:** well served on desktop (utility bar and launcher), under-served on mobile.
- **Recommended home order:** hero, partner logos, 'Is this you' checklist (with email capture), four pillars, NPS proof, case results, how an engagement runs, one-roof before and after, customer comments, industries (all eight visible), three offices, AI playbook, FAQ with objections, form. Cut the duplicate seal band, the office hotspots (they live on /solutions) and the film (move to About).

## Local and industry relevance

- Indianapolis is named in titles, but the Indianapolis office page has no local customer, quote, map or search-style headline (see finding on /locations/indianapolis).
- Industry pages exist for healthcare, government, manufacturing and insurance, but share one template with the same 'first ninety days' block; only healthcare and government carry a real number. Legal is not an industry on the site, though dictation and records work serve law firms.
- Public-sector buyers get Sourcewell cooperative purchasing and City of Anderson ($40,000 a year), which is the strongest local-government proof and deserves a hero-level tile on /industries/government.

## What a competitor does better

Verified on leapmanagedit.com (a regional Indianapolis MSP) on 2026-10-28:

- Named, titled, company-attributed testimonials with photos (for example 'Stu Kaplan, President, MAKUTA Technics').
- FAQ items that answer price ('flat, predictable monthly investment') and switching ('Is it difficult to switch our current IT support to LEAP?' with a concrete answer: documentation, password transfers, vendor coordination).
- A named proprietary process ('IT Master Plan') as the first step, plus a downloadable brochure as a low-commitment offer.
- A single contact form directly on the home page with a phone number beside it.

VAF already has a stronger named process (the Technology Strength Assessment), stronger audited proof, and a bigger footprint. What a national copier dealer or regional MSP typically does better, and what VAF's pages do not yet match, is: published price logic, an explicit switching story, named customer voices, and one unmistakable action. (The national-dealer comparison is a general expectation, not something I checked on a specific site in this audit.)

## Not verified

- What happens after a form submit (thank-you message or page, notification emails, whether an autoresponder fires). I did not submit forms, so the 'no autoresponder' promise is untested.
- The clean and press direction variants; the audit is of the live Showcase build and the local rebuild of copy-print only.
- Whether the Gartner, 99.999%, Costco and 'healthcare since 1914' statements are documented by VAF or the vendors.
- Whether the AI-generated imagery is labelled anywhere on the live site; none was visible in the screenshots.

## Findings

### Blocker (6)

**F1. all pages (mobile): sticky quick bar (.pv-sticky .b)**

- What: The mobile sticky bar's second button, 'Call VAF', is white text on a white pill: it is invisible. The only persistent tap-to-call on mobile does not work visually, and the mobile header has no phone icon.
- Evidence: Playwright at 390px after scrolling 1500px: 'Call VAF' computed color rgb(255,255,255) on background rgb(255,255,255), identical on /, /about, /contact, /services/managed-it, /technology-strength-assessment, /solutions. Screenshot scratchpad/qa_mkt/sticky_390.png. themes/vaf/css/vaf.css line 578: .pv-sticky .b{background:var(--chrome-bg);color:#fff} and --chrome-bg resolves to white in the light theme.
- Fix: CODE, not copy. themes/vaf/css/vaf.css line 578: change to .pv-sticky .b{background:var(--navy,#0f1e33);color:#fff}. Content: brand.sticky.secondary in brands/vanausdall.content.json (brand.sticky) from 'Call VAF' to 'Call (317) 634-2913'. Also add a tap-to-call icon button to the mobile header (vaf-header module).

**F2. /blog: blog listing template**

- What: The blog index is not themed: it renders HubSpot's default blog template with the wrong nav, a purple 'Get started' button, placeholder description text, no VAF logo or footer, and the featured post shown twice. This is the exact failure design/guardrails.md forbids. Individual posts do use the theme, so the listing template assignment is the gap.
- Evidence: Live /blog text: nav 'Home, Products, Pricing, Blog, Company'; description 'A brief introductory description of your blog and the topics covered at a high level. Just one or two sentences should be just right.'; footer 'Home Products Pricing Blog Company Privacy Policy · Legal · © 2026. All rights reserved.'; 'Print & Copy Solutions: Where Document Workflows Start' appears three times (featured, side card, and a third slug); pagination shows 29 pages. /blog/data-discovery-and-classification does load the VAF header and footer. Screenshots vp_blog_1440_00.png and vp_blog_1440_01.png.
- Fix: In HubSpot blog settings assign themes/vaf blog-listing.html (vaf-blog-listing.module) and blog-post.html; set the blog description to: 'Plain-English guidance on managed IT, security, copiers and print, phones and document workflow, from the Indiana team that has done it since 1914.' Delete the duplicate posts at slugs print-copy-solutions-where-document-workflows-start-1 and -2. Re-run verify.mjs on /blog.

**F3. / (home), /services/copy-print-solutions: latest articles cards**

- What: The first article card on the home page links to a 404. The same bad slug is in the local copy-print rebuild.
- Evidence: Home card href is /blog/print--copy-solutions-where-document-workflows-start (double hyphen); curl returned 404. The live post slug listed on /blog is print-copy-solutions-where-document-workflows-start. The local dry build of services/copy-print-solutions also contains 'blog/print--copy-solutions-where-document-wor...'.
- Fix: brands/vanausdall.overrides.home.json > index.html.sections[id=articles].items[0][3]: change 'blog/print--copy-solutions-where-document-workflows-start.html' to 'blog/print-copy-solutions-where-document-workflows-start.html'. Make the same change in brands/vanausdall.overrides.pillars.json (copy-print 'related' items) and fix the slug at the source in brands/vanausdall.blog.json.

**F4. /solutions: 'Every solution page, by pillar' resources section**

- What: Below the twelve solutions, the page dumps 57 legacy cards headed 'Every solution page, by pillar' with the build note 'Each page from the current site, rebuilt in the new templates with its FAQ and schema.' Many descriptions are cut mid-sentence and several are off-topic. It buries the 'twelve solutions' promise and reads as unfinished.
- Evidence: Live text: 57 'Open the page' links. Truncations: 'meet PCI requirements with Oak Si.', 'inside our 57,000-square-foot Indianapolis.', 'Windstream ... including cloud computing and.'. Mismatches: 'Cloud Voice & Text: Learn about dictation solutions based on industry.'; 'Scan Documents with Your i Phone'; 'Know Be4, Get Your Free Ransomware Simulator Tool Servi'; 'Mitel Connect Client Training Videos'. Page is 14,902px tall at 1440.
- Fix: scripts/migrate_pages.py line 327 (out['solutions.html'] resources section) and brands/vanausdall.overrides.pillars.json solutions.html: delete the section. Replace with a 4-card 'Free tools and guides' resources section: heading 'Free tools and guides', intro 'Start with something you can use today.', items: Free phishing security test, Print cost calculator, 2026 CIO AI Playbook, Free print assessment (href values already in the nav). Park the rest as redirects or footer links.

**F5. /about: 'More from Van Ausdall & Farrar' resources section**

- What: The About page ends with a section headed 'More from Van Ausdall & Farrar' whose intro is 'Every remaining page on the current site, kept and rebuilt.' It lists the Cookie Policy, Disclaimer, CPRA opt-out, Privacy Policy and Terms as cards with truncated one-line summaries. It is migration scaffolding, not buyer content, and it sits between the proof and the only CTA.
- Evidence: Live /about text: 'Every remaining page on the current site, kept and rebuilt.' Cards: 'Van Ausdall & Farrar believes in our customers, and we do everything we can to make sure you manage your business well using all of our.'; 'We value your privacy very highly. Please read this Cookie Policy carefully before using the https://www.vanausdall.com/ Website (the.'; same for Disclaimer, CPRA, Privacy, Terms, Customer Care App Privacy Policy.
- Fix: scripts/migrate_pages.py line 336 (out['about.html']) and brands/vanausdall.content.json pages[file=about.html].sections[10] (type resources): delete. Legal pages stay footer-only. Employee Benefits and Virtual Site Visit can be linked from the Careers page. Keep sections[11] (cta 'Work here') and add a buyer CTA above it (see the About CTA finding).

**F6. /case-studies: hero subhead and 'Every case study by industry' intro**

- What: Visitor-facing copy describes the site migration: 'the rest are one line each until the PDFs are migrated' and 'Each is published on vanausdall.com with a PDF today; the PDFs migrate into pages in the build.' A buyer reads this as an unfinished site and a reason to doubt the other 14 results.
- Evidence: Live /case-studies hero: 'Eighteen Indiana organizations, by industry. Four are written up in full here; the rest are one line each until the PDFs are migrated.' resources intro: 'Each is published on vanausdall.com with a PDF today; the PDFs migrate into pages in the build.'
- Fix: brands/vanausdall.content.py line 889 (hero subhead) and line 892 (resources intro); regenerate content.json. Replacement subhead: 'Eighteen Indiana organizations, by industry. Four are written up in full; the rest show the headline result.' Replacement intro: 'More Indiana organizations, with the result each one saw.'

### Major (23)

**F7. / , /services/managed-it, /healthcare, /about, /partners, case studies: self-referential 'vanausdall.com' and reviewer language**

- What: Several sections talk to a reviewer, not a buyer: they cite 'vanausdall.com' as the source of VAF's own claims, say 'Nothing here is aspirational', or describe the testimonials as 'Imported directly from our after-service surveys'. On VAF's own site, 'from vanausdall.com' is circular and weakens the proof it is meant to add.
- Evidence: Home seal intro: 'Each line is on vanausdall.com or in an audited third-party report today. Nothing here is aspirational.' and source line 'Sources: vanausdall.com (about, why VAF, copy print, support, document conversion pages), CEO Juice NPS report, SOC 2 certification as displayed on vanausdall.com.' Home voices heading: 'Imported directly from our after-service surveys'. Home film caption: "VAF's own film, from vanausdall.com". Managed IT: 'Everything below is on vanausdall.com today or in a certification we hold.' Healthcare: 'Every case study is published on vanausdall.com today.' Partners: 'VAF says it fully supports every product it recommends...' Case study attribution: 'Published case study, vanausdall.com'.
- Fix: brands/vanausdall.overrides.home.json sections: seal.intro -> 'Eight facts you can check before you call.'; seal.source -> 'NPS audited by CEO Juice. Ask your advisor for the SOC 2 and partner documentation.' [VAF to confirm documents can be shared]; voices.heading -> 'What customers wrote after a service call'; film.caption -> 'Filmed at our 75th Street headquarters.' Managed IT detail intro (content.json pages[file=services/managed-it.html].sections[5]) -> 'What you get, and what stands behind it.' Healthcare resources intro -> 'Healthcare customers VAF has worked with.' Partners detail (sections[8]) rewrite in first person: 'We fully support every product we recommend with our own local team, and we review our partnerships regularly.' Case study attribution -> 'Tippecanoe School Corporation and Van Ausdall & Farrar'.

**F8. /technology-strength-assessment, / (hero, checklist, flow), /solutions: primary CTA promise versus what happens**

- What: The Technology Strength Assessment is the primary CTA on every page and is promised as 'ten to fifteen minutes online', but there is no online assessment. 'Start the assessment' only scrolls to a contact form titled 'Request the full assessment' whose note says 'A technology advisor from the Indianapolis office replies to set it up.' 'Take the full assessment' links to /contact. The visitor expects an instant tool and gets a sales callback.
- Evidence: TSA page: hero 'Start the assessment' href=#assess; section id=assess is the 10-question sample checklist, which is local JS and captures nothing; its button 'Take the full assessment' href=/contact; form heading 'Request the full assessment', submit 'Request my assessment', note 'A technology advisor ... replies to set it up.' Home 'Is this you' card: 'Ten to fifteen minutes online, then a specialist walks it with you.' Home hero card: 'Take the assessment'. Solutions form note repeats 'online'.
- Fix: Two options. (1) Honest copy now: replace 'online' everywhere with 'with an advisor' and relabel CTAs 'Request your assessment': brands/vanausdall.content.json brand.sticky.primary, hero primary (index.html hero), checklist.cta_label, flow Assess 'when' ('10 to 15 minutes, then a visit'), and TSA hero 'Start the assessment' -> 'Request your assessment'. (2) Better: build a real self-scoring quiz (HubSpot multi-step form, 20 questions per pillar), show the score on screen, email the scorecard, and let the advisor follow up. The home 'Is this you' six-question widget is the natural entry: after 3 checks, show 'Email me the six answers and the full scorecard' with email only.

**F9. all pages: header CTA button and nav hierarchy**

- What: The persistent header button on every page is 'Schedule a consultation', the secondary action. The client brief says the assessment is the primary CTA everywhere and the consultation is secondary: 'Do not invert them.' 'Schedule' also implies a calendar booking, but the button goes to the /contact form where someone calls back.
- Evidence: Header button href=/contact on all 12 audited pages. brands/vanausdall.md client guardrail: 'The Technology Strength Assessment is the primary CTA on every page. "Schedule a consultation" is secondary.' Contact page hero primary is also the assessment, while the page is the contact page.
- Fix: brands/vanausdall.content.json brand.cta: set label 'Start with the assessment' and href 'technology-strength-assessment.html'. Move 'Schedule a consultation' to a text link beside the phone number in the utility bar, labelled 'Talk to an expert'. If a HubSpot meetings link exists, point 'Talk to an expert' at it; if not, do not use the word 'Schedule'.

**F10. all pages with the lead form (home, contact, TSA, solutions, services, industries, case studies, locations): form fields and prefill**

- What: Form friction and lead quality: four required fields (first, last, work email, company) plus phone and a free-text box; the free-text box 'What are you trying to fix?' arrives pre-filled with 'Topic: Managed IT and security' that the visitor must delete; and the 'What would you like to look at?' dropdown has no field name and is not part of the HubSpot form, so the interest is only text inside the message and cannot be used for routing or reporting.
- Evidence: Form markup on /contact: required inputs firstname, lastname, email, 0-2/name (Company); optional phone; <textarea name=message>Topic: Managed IT and security</textarea>; <select data-topic-select> sits outside the <form> with no name. themes/vaf/modules/vaf-contact.module/module.js line 44: state.prefix = 'Topic: ' + val. Same form id e84ef7ce-04f2-4fef-b539-4351bde13b48 on every page.
- Fix: In HubSpot add a dropdown property 'Interest' (Managed IT and security, Business phone systems, Copiers and managed print, Document management or conversion, AI consulting, Something else) to form e84ef7ce... and bind the select to it; stop prefixing the textarea (module.js line 44). Make Company optional on the first touch (derive it from the email domain) or keep it and drop 'Last name' to a single 'Name'. Textarea label: 'What are you trying to fix? (optional)', with a placeholder 'For example: our copier lease ends in March.'

**F11. all lead forms: consent and trust line near the submit button**

- What: No privacy or consent line, no 'what happens next' and no trust cue sits next to any form. The only privacy link on each page is the footer. Forms are the conversion point; the reassurance should be at the button.
- Evidence: On 12 audited pages the string 'privacy' appears once (footer link only). Home form footer reads only 'Or call (317) 634-2913, Monday through Friday, 7:00am to 5:00pm.' No inline legal consent block on the forms.
- Fix: vaf-contact and vaf-leadform modules, note field (home: brands/vanausdall.overrides.home.json sections[id=contact].note). Replacement note: 'A person from the Indianapolis office replies. We use your details only to answer this request. Privacy policy. Prefer to talk? Call (317) 634-2913, Monday to Friday, 7:00am to 5:00pm.' Add a one-line trust cue under the button: 'NPS 93.4, audited by CEO Juice. SOC 2 certified.'

**F12. /contact (and form microcopy sitewide): response-time promise**

- What: The contact page makes new promises that are not in the client brief and conflict with other pages: 'reads it the same business day', 'Same-day reply from a named person in Indianapolis', 'no autoresponder and no sales sequence', 'You keep the roadmap either way'. Every other page says only 'A person ... replies, not an autoresponder' with no time, while the service commitment on record is 24 hours. A HubSpot form normally fires a notification or confirmation, which can contradict 'no autoresponder'.
- Evidence: Live /contact 'What happens next' paragraph and bullets. brands/vanausdall.md: 'Print the service commitments exactly as VAF states them (24-hour response, same-day for most metro calls). Do not tighten or round them.' Source text: brands/vanausdall.overrides.services.json near line 10353.
- Fix: brands/vanausdall.overrides.services.json contact.html (detail 'What happens next', body and bullets). Until VAF confirms in writing, use only what is on record: 'A person from the Indianapolis office replies to set a time. Existing customers: the Client Service Center responds within 24 hours.' Add [VAF to confirm: reply time for new inquiries] and, if approved, 'We reply within one business day.' Remove 'no sales sequence' and 'You keep the roadmap either way' unless VAF signs off.

**F13. / , /about, /solutions, /services/managed-it, /services/copy-print-solutions, /locations/indianapolis, /industries/healthcare: testimonials**

- What: Customer proof is weak and recycled: first names only (no title, no company), the same eight or so comments reused across pages, 'Elaine' appears twice in the home set (same month), and almost all praise a copier technician ('Jerome', 'Brent', 'Mike'), yet they sit on the Managed IT, cybersecurity and healthcare pages. 'The guy is totally awesome.' appears on the home, solutions, Indianapolis and copy-print pages. A buyer cannot verify anyone, and an IT buyer finds nothing about IT.
- Evidence: Home voices: Elaine (June 2026), Teresa, Stacy, Megan, Elaine (June 2026, second quote). Managed IT: Elaine, Megan ('Brent is amazing'). Healthcare: Megan, Denise ('Mike is awesome'). Locations/Indianapolis: Denise, Teresa. Copy-print: Teresa, Rick, Megan. About: Elaine, Megan, Rick, Denise. Competitor check: leapmanagedit.com shows 'Stu Kaplan, President, MAKUTA Technics' and 'Bridget Slaughter, Real America' with photos.
- Fix: brands/vanausdall.overrides.home.json sections[id=voices].items and the testimonials sections on each page in brands/vanausdall.content.json. Collect 6 to 8 permissioned quotes as [Name, Title, Organization, Service used] from the 4 case-study customers plus the best survey respondents (a CEO Juice survey can ask 'May we quote you with your name and company?'). Attribution format: 'Elaine R., Office Manager, [Organization], after a copier service call, June 2026'. Show one quote per service, matched to the page (IT quote on Managed IT, phone quote on phones). Drop the duplicate Elaine and 'The guy is totally awesome.'

**F14. /services/managed-it: 'In our own words' proof quote**

- What: The only quote on the page is from VAF's own Director of IT, not a customer, and the text does not stand alone: 'We get to take that worry, that stress, the sleepless nights around IT and security, and let them focus on why they do what they do.' ('them' has no referent.) The client brief says to confirm the Steven Sigmon quote before it ships.
- Evidence: Live /services/managed-it 'IN OUR OWN WORDS' block, headline '24/7', attribution 'Steven Sigmon, Director of IT, Van Ausdall & Farrar'. brands/vanausdall.md: 'Steven Sigmon's quote is from the managed IT page; confirm before it ships.'
- Fix: brands/vanausdall.content.json pages[file=services/managed-it.html].sections[2] (proof). Either remove it, or confirm with Steve and rewrite with a complete sentence: value '24/7', text 'We take the worry about IT and security off our clients, so they can focus on the work they do.' Add a customer quote and a named customer outcome (see the testimonials finding).

**F15. /case-studies/tippecanoe-school-corporation (pattern repeats on /industries/*): case study quote and metrics**

- What: The 'quote' is not a quote: it is VAF's own narrative paragraph, attributed to 'Tippecanoe School Corporation case study, vanausdall.com'. No customer is named or quoted. The 'IT TIME 20%' tile sits under 'THE NUMBERS' as if it were a result, but 20% is the before-state. The $1M has no timeframe beyond 'life of the contract'. The fleet math reads 600+ single-function printers plus 200+ copiers (about 800) against '1,200 machines'.
- Evidence: Live case study text: 'IT staff was spending 20% of their time servicing print issues. The fleet held over 600 single-function printers and over 200 copiers.' and 'cutting overall equipment from 1,200 machines to just over 300 ... $1,000,000 in savings over the life of the contract.' Quote block attribution: 'Tippecanoe School Corporation case study, vanausdall.com'. Same pattern on /industries/healthcare ('BUDGET Under', 'Johnson Memorial Health case study, vanausdall.com') and /services/copy-print-solutions.
- Fix: brands/vanausdall.content.json pages[file=case-studies/tippecanoe-school-corporation.html].sections[1] (casestudy). Replace the metric tile label: 'IT time' value '20%' text 'of IT staff time had gone to print issues before VAF' and add a real result if one exists (for example hours returned). Ask Tippecanoe's IT lead for a one-sentence quote and use: quote '[Quote]' attribution '[Name], [Title], Tippecanoe School Corporation'. Add contract length so $1M reads as a rate. Confirm the 1,200 count against 600 plus 200 with VAF. Do not present narrative as a quotation.

**F16. / (mobile): Client Service Center placement and tap-to-call**

- What: On a 390px phone the Client Service Center card sits about 1,490px down the page (fold is 844px), the utility links are hidden, and the header has only a logo and a menu button. The client rule is that the Client Service Center links never move below the fold on mobile. Existing customers (a large share of visits) and new buyers who want to call both lack a visible phone action, made worse by the invisible sticky 'Call VAF'.
- Evidence: Playwright 390px: hero card links 'Request support' y=1486 and 'Order supplies' y=1538; the top utility links render with zero width; 'Already a customer?' launcher pill width 0 (hidden). brands/vanausdall.md: 'The Client Service Center links (support, supplies, IT support) never move below the fold on mobile.' Screenshots vp_home_390_00.png, vp_home_390_01.png.
- Fix: themes/vaf/css/vaf.css and vaf-header module: show a compact 'Customer? Get support' text link plus a phone icon in the mobile header; or keep the 'Already a customer?' pill visible on mobile and place it above the sticky bar. In brands/vanausdall.overrides.home.json sections[id=hero], reorder card_b above stats on max-width 767px. Contact page mobile hero ('just call') needs a visible 'Call (317) 634-2913' button.

**F17. / (hero): value proposition and hero action load**

- What: The home headline names no service, place or audience, so the 5-second test depends on the grey subhead: 'Everything your business runs on, under one roof.' The hero then offers four competing actions: a primary button, a secondary link, a 'How it works' button on the assessment card, and a four-link Client Service Center card, plus four stat tiles. The 'Start here' card duplicates the primary button and its own button is 'How it works', which is not a start action. The eyebrow 'START HERE' is blue on a light glass card over video and is hard to read.
- Evidence: Live H1: 'Everything your business runs on, under one roof.' Subhead names IT, copiers, phones, document workflow, AI and 'Indiana businesses'. Screenshot vp_home_1440_00.png: card_a 'Start here / The Technology Strength Assessment / How it works'; card_b 'Already a customer? ... Request support, Order supplies, IT support, Call (317) 634-2913'.
- Fix: brands/vanausdall.overrides.home.json sections[id=hero] (showcase) and [id=hero-light] (clean): eyebrow 'Indiana's largest full-service office technology provider, since 1914'; heading 'One Indiana partner for <em>IT, phones, copiers and paper</em>.'; subhead 'Van Ausdall & Farrar looks after the technology your office runs on, under one agreement and one Customer Care Center. Start with the Technology Strength Assessment and see what to eliminate, optimize and leverage.'; primary.label 'Get your Technology Strength Score'; secondary.label 'Talk to an Indianapolis expert'; card_a.label 'See how it works' with card_a.eyebrow 'Complimentary'; keep card_b but collapse it to one line on mobile.

**F18. / (FAQ and sitewide): objection handling: price, switching, contracts, downtime**

- What: The buyer's real objections are not answered anywhere on the pages audited: what it costs, how a switch works, whether there are long contracts, what happens to current vendors and leases, and what downtime to expect during cutover. The home FAQ has four questions (company size, taking over from another vendor, response speed, geography), and the switching answer is a one-word hedge: 'Usually.' A regional MSP competitor answers pricing and switching directly on its home page.
- Evidence: Home FAQ items: 'Do you only work with large companies?', 'Can you take over equipment or systems from another vendor?' (answer starts 'Usually.'), 'How fast do you respond?', 'Do you serve outside Indianapolis?'. Searches of home, contact, TSA and managed-it HTML for 'contract', 'switch', 'cancel', 'month-to-month' returned only the case study phrase 'life of the contract' and 'Monitoring switched on'. Competitor evidence: leapmanagedit.com FAQ answers 'How does pricing work' (flat monthly) and 'Is it difficult to switch our current IT support to LEAP?'.
- Fix: brands/vanausdall.overrides.home.json sections[id=faq].items: replace the second answer with 'The Technology Strength Assessment covers everything you run, whoever supplied it, and the roadmap says what to keep, what to eliminate and when. Tippecanoe School Corporation replaced more than 10 copy and print vendors with one. [VAF to supply: how existing leases and contracts are handled.]' Add two items. 'What does it cost?': 'The assessment is complimentary. Managed IT and print are quoted after it, as one agreed monthly amount you see in writing first. [VAF to supply: what drives the price.]' 'How do we switch without downtime?': '[VAF to supply: cutover steps for IT and phones.]' The flow already says 'Numbers ported' and 'Users trained before the technician leaves', which can be quoted.

**F19. /services/managed-it: pricing, contract and switching answers**

- What: The managed IT page, the highest-value service page, never explains how price works, what drives it, how long the agreement runs, how a switch from an existing provider works, or what the response commitment is for help desk tickets. It promises 'one predictable monthly cost' and 'One monthly number' without a range or the factors. Its four FAQ items are what is included, difference from IT support, co-managed, and what a vCIO is.
- Evidence: Live FAQ headings: 'What is included in managed IT services?', 'How is managed IT different from IT support?', 'Do you work with companies that already have an IT team?', 'What is a vCIO?'. Flow step 'Plan, Week 2' mentions 'Monthly scope and price' only inside the process. No occurrence of 'contract', 'term', 'cancel' or 'switch' on the page.
- Fix: brands/vanausdall.content.json pages[file=services/managed-it.html].sections[7] (faq). Add: 'What does managed IT cost?' 'One agreed monthly amount based on the users and devices we manage and the security and support you choose. You see it in writing after the assessment, before you commit. [VAF to supply: typical per-user range or drivers.]' 'Are we locked in?' '[VAF to supply: term, renewal, notice.]' 'How do we switch from our current IT provider?' 'We start with the assessment, inventory what you run, then bring monitoring, backup and security online. [VAF to supply: password, vendor and documentation handover steps.]' 'How fast do you respond to a help desk ticket?' '[VAF to supply: managed IT help desk response target.]'

**F20. /about: conversion path**

- What: The About page has no buyer CTA: the hero buttons are 'Why VAF' (an anchor) and 'Careers', there is no form on the page, and the closing CTA is 'Work here / See careers'. A visitor persuaded by more than a century of credibility has nowhere to go but the header button.
- Evidence: Live /about: forms=0; hero primary 'Why VAF', secondary 'Careers'; last section 'Work here ... See careers'.
- Fix: brands/vanausdall.content.json pages[file=about.html].sections[0] hero primary -> {label:'See what we can do for your office', href:'solutions.html'}, secondary -> {label:'Talk to an expert', href:'contact.html'}; add a leadform section before the 'Work here' CTA: heading 'Meet the team that will look after your office', submit 'Talk to an expert'.

**F21. /contact: form position, hero, and next-step block**

- What: The page whose only job is contact puts the form about 1,000px down the page behind a 110-word paragraph, and its hero primary button is the assessment, not the form. On a phone the hero shows 'just call' with no tap-to-call button. 'Our innovation experts' is filler.
- Evidence: 1440px first screen (vp_contact_1440_00.png): headline, subhead, two buttons, then blank space; the 'Let's talk' form is section 3 of 6 (page height 6,716px). The 'What happens next' block is one paragraph of about 110 words. Mobile screenshot vp_contact_390_00.png shows no phone button.
- Fix: brands/vanausdall.overrides.services.json contact.html. Hero: heading 'Talk to a person at VAF.'; subhead 'Tell us what you run and what is not working. We call you back to set a time. Existing customer? The Client Service Center is faster.'; primary 'Call (317) 634-2913' (tel:), secondary 'Existing customer? Get support'. Move the leadform into the hero's right column on desktop. Replace the paragraph with three steps: '1. A person from the Indianapolis office reads your note and calls to set a time. 2. New need: an advisor walks the Technology Strength Assessment with you. 3. You get a written roadmap of what to eliminate, optimize and leverage.' Submit label 'Talk to an expert'.

**F22. /services/copy-print-solutions (live): live page is stale**

- What: The live page still carries the old copy and unbranded title ('Copy Print Solutions in Indianapolis') with the old structure, while the local rebuild (python3 scripts/vaf_build.py dry services/copy-print-solutions) is materially better. Live also repeats 'Reduce costs by up to 30%' in the hero, section copy and FAQ with no source, and has no case study or calculator link.
- Evidence: Live title tag: 'Copy Print Solutions in Indianapolis'. Live hero: 'Reduce costs by up to 30% with Indianapolis copy print solutions...'. The dry build adds the Tippecanoe case study, print cost calculator and 'Get Your Free Print Assessment' as primary.
- Fix: Publish the rebuilt template: python3 scripts/vaf_build.py templates services/copy-print-solutions then pages services/copy-print-solutions. Fix the issues in the next finding first.

**F23. /services/copy-print-solutions (local rebuild): stat band and claims**

- What: The local rebuild's stat tiles break two client rules and contradict themselves: '100+ Years in Business' and 'our 100+ years of experience' (the client says never print a year count; say 'since 1914'), and '30% Average Printing Cost Reduction' directly under a hero that says 'up to 30%'. 'Average' turns an upper bound into a typical result and no source is given. The 'quote' on the case study is a narrative paragraph, and the testimonials heading is 'Imported directly from our after-service surveys'.
- Evidence: Dry build stats: [['100+','Years in Business'],['30%','Average Printing Cost Reduction'],['24/7','Proactive Support & Monitoring'],['25','Point Inspections on Every Call']]. leadform note: '...our 100+ years of experience implementing and managing secure technology solutions.' brands/vanausdall.md: 'Never print "112 years" or any year count. Say "since 1914".'
- Fix: brands/vanausdall.overrides.pillars.json services/copy-print-solutions.html stats: [['1914','Serving Indiana since'],['Up to 30%','Print cost reduction, per VAF assessments [VAF to supply source]'],['24 hr','Customer Care Center response'],['25','Points of inspection on every call']]. leadform.note: 'Partnering with us for copy and print gives you the flexibility to adjust as your business changes, with local service since 1914.' Remove 'Average'. testimonials.heading -> 'What customers wrote after a service call'.

**F24. / , /technology-strength-assessment, /services/managed-it, /industries/*: unverified process promises and inconsistent timelines**

- What: The engagement timeline changes by page and contains commitments that are not in the brief: Roadmap 'Week 2' (home, TSA), 'Week 1 / Week 2 / Weeks 3 to 4' (managed IT), 'Week one / Weeks two to four / Month two / Month three: first quarterly review' (every industry page), plus 'a specialist walks the office and confirms the answers', 'Every device, system and vendor inventoried', 'Options priced side by side'. The brief says to ask how the score is calculated and what the client receives; the deck has not been received.
- Evidence: Home flow: Assess '10 to 15 minutes, then a visit', Roadmap 'Week 2'. Managed IT flow: Assess 'Week 1', Plan 'Week 2', Onboard 'Weeks 3 to 4'. Healthcare, government, insurance and manufacturing: identical 'THE FIRST NINETY DAYS' block. brands/vanausdall.md: 'Deck received: no. Stages: Assess, Roadmap, Implement, Monitor (drafted from the site; theirs to replace).'
- Fix: brands/vanausdall.overrides.home.json sections[id=flow].steps[*].when and the matching flow in brands/vanausdall.content.json for TSA, managed IT and the industry 'first ninety days' detail sections. Replace dated promises with sequence only ('Then', 'After that') until VAF confirms: Assess -> 'First', Roadmap -> 'Next', Implement -> 'On a date you choose', Monitor -> 'Ongoing'. Mark any retained timing [VAF to confirm].

**F25. all service, industry, TSA, print-assessment and playbook pages: templated proof band repeated three times**

- What: Every inner page opens with the same proof package three times in the first screens: an image badge ('93.4 Net Promoter Score, independently audited'), a four-tile stat band (1914, 93.4, SOC 2, 4,000+ phone systems) and a ribbon ('SOC 2 certified', 'NPS 93.4, audited by CEO Juice', 'Mitel Gold'). It is the same on the print assessment, AI playbook and healthcare pages, so proof is neither page-specific (4,000 phone systems on a managed IT or copier page) nor persuasive through repetition.
- Evidence: Managed IT live text order: '93.4 Net Promoter Score, independently audited', '1914 ... 93.4 Net Promoter Score, audited ... SOC 2 ... 4,000+ Phone systems deployed since 1983', 'SOC 2 certified / NPS 93.4, audited by CEO Juice. World Class since 2019 / Mitel Gold, seven consecutive years'. Same block on /services/copy-print-solutions, /technology-strength-assessment, /print-assessment, /cio-ai-playbook, /industries/healthcare, /locations/indianapolis.
- Fix: scripts/vaf_map_a.py lines 53 to 59 (badge_value, badge_label, ribbon) and each page's hero stats in brands/vanausdall.content.json: keep one proof device per hero. Choose by page: managed IT -> 'SOC 2' and 'Fortinet Engaged Advanced Partner'; copy print -> '25-point inspection' and 'Same-day service for most metro calls'; phones -> 'Mitel Gold seven years' and '4,000+ systems'; healthcare -> '1.5 million files in 90 days'. Delete ribbon and badge where stats exist.

**F26. /locations/indianapolis: local proof and relevance**

- What: The Indianapolis page, the largest untapped local opportunity per the SEO baseline, has no Indianapolis customer, no local testimonial, no map or directions, and a generic headline. The two quotes are not about Indianapolis. The H1 'Indianapolis office technology from the headquarters up' says nothing a buyer is looking for (copier, IT support, phone systems near them).
- Evidence: Live text: H1 'Indianapolis office technology from the headquarters up'; hero stat tile 'Local / Technicians dispatched from this office'; testimonials Denise and Teresa with no location; no embedded map. brands/vanausdall.md SEO baseline: 'Indianapolis, the HQ market, does not appear in the top 50 for managed IT: the Indianapolis pages are the largest untapped local opportunity.'
- Fix: brands/vanausdall.overrides.locations.json locations/indianapolis.html sections[0]: heading 'Managed IT, copiers and business phones, <em>from our Indianapolis headquarters</em>'; subhead 'Our 57,000-square-foot headquarters at 6430 E 75th Street is where our Customer Care Center, service dispatch and secure Document Conversion Center sit. Call (317) 634-2913.' Add a Google map embed and parking and entrance note [VAF to supply]; name Indianapolis-area customers who consent (ask VAF which of the 18 case-study customers are in the metro); add a 'Same-day service for most metro calls' proof tile.

**F27. /industries/healthcare, /government, /insurance, /manufacturing-logistics: industry pages are one template**

- What: The industry pages share an identical 'first ninety days' block, an identical stat band and similar structure, so a healthcare administrator, a city clerk and an insurance agency read the same page with the nouns changed. Insurance and manufacturing have no number at all (only 'used VAF communications technology to keep customers on the line'); healthcare has a metric tile 'BUDGET: Under'. Headlines drift to jargon ('Eliminate, optimize, then compete.') and filler ('Manufacturing has advanced light years'). There is no legal vertical although VAF sells dictation and records work to that buyer.
- Evidence: Healthcare, government, insurance and manufacturing live text all contain 'Every [industry] engagement begins with the same three steps. First, the Technology Strength Assessment maps every device, contract, phone line and workflow...' and the same four bullets 'Week one ... Month three'. Healthcare metric tile BUDGET 'Under'. Industries nav lists eight verticals, none legal.
- Fix: brands/vanausdall.content.json pages[file=industries/*.html].sections: replace the 'first ninety days' detail with one buyer-specific question list, for example healthcare: 'Three questions healthcare leaders ask first: Where do patient records live? Who can print them? What happens to the phones when a clinic goes down?' Fix healthcare metric to '1.5M files, 90 days, 500+ boxes against an estimate of 100'. Add one named proof per vertical or say 'Ask for a reference'. Consider an /industries/legal page built only from dictation and records capabilities already sold.

**F28. /about, /locations/indianapolis: generated headquarters image presented as real**

- What: The About and Indianapolis hero images are AI-generated (asset gen-hq-1200.jpg), shown without a label, for a brand whose pitch is 'proof over hype' and a 57,000 sq ft building anyone can drive to. A regional competitor shows real staff and buildings. The client brief says one real HQ photo, technicians and the service fleet are the shoot.
- Evidence: Live about.html and locations_indianapolis.html reference //50498425.hs-sites.com/hubfs/vaf/assets/gen-hq-1200.jpg. The home page HTML also references gen-technician-1200.jpg. brands/vanausdall.overrides.home.json hero note: 'The photography here is generated for the preview and labelled as such; a shoot at the 75th Street headquarters ... replaces it in the build'.
- Fix: Asset map brands/vanausdall.asset-map.json: replace gen-hq-1200.jpg and gen-technician-1200.jpg with real photography of 6430 E 75th Street, a VAF technician and the service fleet before launch. Until then, do not publish these as the building. Use the existing careers film frames if real.

**F29. all blog posts: no in-article call to action**

- What: Blog posts (the brief's second-highest organic URL is a blog post) end with plain text ('start a conversation with our team') and no button or form. The blog (29 index pages) therefore captures no leads from organic traffic.
- Evidence: Live /blog/data-discovery-and-classification: document.forms.length = 0; the only CTAs are header, footer and sticky bar; the last paragraph is 'To find out what is exposed in your environment and who can see it, start a conversation with our team.'
- Fix: themes/vaf/modules/vaf-blog-post.module and the blog-post template: add a topic-matched CTA block after the body (security post -> Technology Strength Assessment; print post -> Free print assessment; phones post -> contact) and a short form. Replacement copy for the security posts: heading 'Not sure who can see your data?' body 'The Technology Strength Assessment checks your information, print, process and communication in ten to fifteen minutes.' button 'Get your Technology Strength Score'.

### Minor (15)

**F30. /: page length and repetition**

- What: The home page is about 16,600px tall at 1440 and 24,400px at 390 across 17 sections. 93.4 appears three times (hero stat, proof band, seal tile), 1914 four or more times, and the 'seal' band restates the hero. Case results and customer comments come after the long interactive middle.
- Evidence: Playwright scrollHeight 16,598 (1440) and 24,368 (390). Compose order for showcase in brands/vanausdall.overrides.home.json: hero, partners, wheel, is-this-you, proof, ba, flow, office, seal, casecards, markets, map, voices, playbook, articles, film, faq, contact.
- Fix: brands/vanausdall.overrides.home.json compose.showcase: hero, partners, is-this-you, wheel, proof, casecards, flow, ba, voices, markets, map, playbook, faq, contact. Remove seal, office (it lives on /solutions), film (move to About) and trim articles to 3. Target under 11,000px desktop.

**F31. all forms: generic and mismatched button labels**

- What: Submit buttons do not match the page promise: 'Schedule my consultation' sits under 'Start with the Technology Strength Assessment' (healthcare) and 'Want results like these? ... start with the assessment' (case study); the Solutions form button is 'Take the assessment'. Link microcopy is generic throughout: 'Read more', 'Open the page', 'LEARN MORE', 'Branch page', 'See the service'.
- Evidence: Submit values: home, contact, managed-it, copy-print, partners, locations, healthcare, case study 'Schedule my consultation'; solutions 'Take the assessment'; TSA and print assessment 'Request my assessment'; AI playbook 'Send me the playbook'.
- Fix: Per page, vaf-leadform.submit: contact and general pages 'Talk to an expert'; assessment-led pages 'Start with my assessment'. Case cards: 'See how Tippecanoe cut 1,200 devices to 300', 'See the 90-day scanning project', 'See STAR Financial's results'. Service cards: 'Explore managed IT', 'Explore business phones'. Location cards: 'Visit the Fort Wayne office'.

**F32. /cio-ai-playbook, /: lead magnet prominence and gating**

- What: The 2026 CIO AI Playbook is a strong lead magnet but is the 14th of 17 home sections, appears only as a nav sub-item, and its gate is the full sales form (four required fields plus a 'What are you trying to fix?' box on a download form). The free KnowBe4 tools are buried in the 57-card dump, and the print cost calculator appears only in the nav and footer.
- Evidence: Home order: playbook CTA after voices. /cio-ai-playbook form fields: firstname*, lastname*, email*, phone, 0-2/name*, message; submit 'Send me the playbook'.
- Fix: Move the playbook CTA to sit under 'Is this you' (section 4 or 5 of the home) as a secondary offer: heading 'Not ready for the assessment? Start with the AI playbook.' Reduce the playbook form to name, work email and company. Surface 'Free phishing security test' on the Managed IT page as a mid-page soft offer.

**F33. /technology-strength-assessment, /: assessment widget instructions contradict; duplicate FAQ**

- What: The home widget says 'Check the ones you cannot answer yes to' while the TSA widget says 'Check the ones you can answer yes to' and 'Check what is true today', so the score meaning flips between pages. The TSA FAQ asks the same question twice ('What does it cost?' and 'How much does it cost?').
- Evidence: Home checklist intro: 'Check the ones you cannot answer yes to. They are six of the eighty.' TSA: 'Check the ones you can answer yes to.' and 'Check what is true today.' FAQ headings 1 and 4: 'What does it cost?' / 'How much does it cost?'.
- Fix: brands/vanausdall.content.json pages[file=technology-strength-assessment.html].sections[4] (checklist assess).intro and .messages: use one direction on both pages: 'Check each one you can answer yes to.' Delete the duplicate FAQ item in sections[6].

**F34. / , /about, /partners: Gartner, 'highest standards' and Costco claims**

- What: Third-party claims are used as proof without attribution: 'Technology partners, including Gartner Magic Quadrant leaders' above the logo strip (the brief's proof list does not include it), the SOC 2 tile 'we meet the highest standards for protecting your data' (SOC 2 is an attestation report; 'highest standards' is an overclaim), 'Costco scores 79' on About, and Elevate '99.999% uptime reliability' on Partners (a vendor claim stated as fact).
- Evidence: Home logo caption; seal tile 'Our SOC for Service Organizations certification means we meet the highest standards for protecting your data.'; About NPS block 'Costco scores 79. The average US company scores 10.'; Partners Elevate card.
- Fix: brands/vanausdall.overrides.home.json partners.caption -> 'Technology partners'; seal item SOC 2 body -> 'An independent audit of how we protect customer data. [VAF to confirm Type I or II and report period.]' Add attribution 'Source: CEO Juice benchmark [year]' to the Costco figure or remove it. Elevate card -> 'AI cloud communications. Elevate states 99.999% uptime.'

**F35. /partners: voice**

- What: The partners page hero says 'it is uncommon that we have to apologize for a deficiency in our partners', which plants the idea of deficiencies, and the 'Local support' section uses a third-person 'VAF says it ...' construction that reads like a summary written by someone else.
- Evidence: Live hero: 'By representing the very best, it is uncommon that we have to apologize for a deficiency in our partners or our technology.' Detail: 'VAF says it fully supports every product it recommends with its own local team...'
- Fix: brands/vanausdall.content.json pages[file=partners.html].sections[0].subhead -> 'We only support the industry-recognized leaders in each area we serve, and we review our partnerships regularly.' sections[8].body -> 'We fully support every product we recommend with our own local team.'

**F36. site voice: buzzwords, filler and passive voice**

- What: A few phrases break the plain, confident register: 'innovation experts' (contact), 'World-class partnerships' (partners H1), 'ultra-secure' and 'state-of-the-art' (solutions cards), 'Experience you will profit from' (about), 'advanced light years' (manufacturing), 'Every line below is designed, installed, serviced and supported by VAF's own people' (passive), and 'Provide value-driven technology solutions' (mission, acceptable as a mission quote).
- Evidence: Live text on /contact, /partners, /solutions, /about, /industries/manufacturing-logistics.
- Fix: Plain replacements: 'innovation experts' -> 'advisors'; 'World-class partnerships, by pillar.' -> 'The vendors we stand behind, by pillar.'; 'Experience you will profit from' -> 'Experience that saves you money'; 'We design, install, service and support every line with our own people.'

**F37. /: 'A person answers' versus 24-hour response**

- What: The home Client Service Center card says 'A person answers. Monday to Friday, 7 to 5.' while the stated commitment is 'responds within 24 hours'. 'Answers' reads as a live answer. The client brief says print the commitments exactly as stated.
- Evidence: Home card_b.body: 'A person answers. Monday to Friday, 7 to 5.' Seal tile: 'Requests processed Monday through Friday, 7:00am to 5:00pm, and answered within 24 hours.'
- Fix: brands/vanausdall.overrides.home.json sections[id=hero].card_b.body -> 'Monday to Friday, 7:00am to 5:00pm. Requests are answered within 24 hours.'

**F38. /case-studies, /: STAR Financial figure wording**

- What: The 70% figure is 'Print cost savings at STAR Financial Bank' on the case-study index but 'Over 70% cost savings after five months' on the home card and case card. One of them is wrong.
- Evidence: Live /case-studies stat band: 'Print cost savings at STAR Financial Bank'. Home card: 'Over 70% cost savings after five months with Van Ausdall & Farrar.'
- Fix: brands/vanausdall.content.json pages[file=case-studies.html].sections[1] (stats) label and the home casecards item: use the wording in the published STAR case study; confirm with VAF.

**F39. /industries/healthcare: claim to verify**

- What: 'VAF has worked in and around healthcare since 1914' is a strong claim that is not in the brief's proof list and could be challenged by a hospital buyer.
- Evidence: Healthcare hero subhead; the same line appears on the /contact and /locations/indianapolis industry cards.
- Fix: brands/vanausdall.content.json pages[file=industries/healthcare.html].sections[0].subhead -> 'Reliable, protected information is patient safety. VAF scanned and indexed 1.5 million patient files for Johnson Memorial Health in 90 days.' unless VAF can document 1914.

**F40. / (markets tabs): default industry tab is Education**

- What: The industries block opens on Education and hides the other seven behind tabs, so a healthcare, government or manufacturing visitor sees the wrong vertical first and must discover the tabs.
- Evidence: Home live text shows only the Education body with the other eight labels as tabs.
- Fix: brands/vanausdall.overrides.home.json sections[id=markets]: add a lead line 'Pick your industry' and render all eight as cards linking to the industry pages, or default the tab by referrer.

**F41. / (desktop): 'Already a customer?' pill overlaps content**

- What: The fixed bottom-left launcher pill sits over body copy while scrolling (it covers the text of the seal tiles in the 1440 screenshot).
- Evidence: Screenshot vp_home_1440_07.png: pill overlaps the '250+' tile text.
- Fix: themes/vaf/css/vaf.css launcher: reduce to a 36px icon with label on hover, or hide after the hero.

**F42. / (hero, desktop): low contrast on the assessment card**

- What: 'START HERE' in blue on a translucent light card over video is hard to read and the card body text is grey on the video.
- Evidence: Screenshot vp_home_1440_00.png.
- Fix: themes/vaf/css/vaf.css hero card_a: raise the card to a solid navy fill with white text (the guardrails require color-mix, not opacity, for text).

**F43. all pages: no urgency or qualifying hook**

- What: There is no honest reason to act this quarter and no qualifying question in the form. Urgency without hype is available from real triggers VAF's buyers have.
- Evidence: No copy on audited pages references a lease end date, renewal window or deadline; the form has no 'when does your current agreement end' field.
- Fix: Add an optional form field 'When does your copier lease or IT agreement end?' (HubSpot date or dropdown: Within 6 months, 6 to 12 months, Not sure). Add to the print assessment: 'Your lease end date is the best time to compare. Start 6 months before it ends.' [VAF to confirm]. This is a qualifier, not a hype line.

**F44. / , /about: card images are generic stock, not customers**

- What: Case result cards use unrelated stock imagery (hands over charts, a nurse with a holographic interface, a finger touching app icons) instead of the customer, their logo or their building, which weakens 'on the record'.
- Evidence: Screenshot vp_home_1440_08.png: Tippecanoe, Johnson Memorial and STAR cards.
- Fix: brands/vanausdall.overrides.home.json sections[id=casecards].items[*][4]: replace with the customer logo on a neutral tile, or a real photo, once permission is obtained.
