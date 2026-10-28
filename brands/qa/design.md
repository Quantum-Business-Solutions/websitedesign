# Design QA: VAF staging (Showcase direction)

Audited live at https://50498425.hs-sites.com on 2026-10-28, Playwright Chromium, 1440 and 390 wide, slow scroll so reveals ran. Home measured section by section; /about, /partners, /contact, /services/managed-it, /locations/indianapolis, /case-studies/tippecanoe-school-corporation, /blog and one post screenshotted and spot-measured. Nothing in the repo was edited except this file and design.json.

Counts: **3 blocker, 20 major, 24 minor** (47 findings). Machine-readable copy: `brands/qa/design.json`.

## What is already strong (verified, do not regress)
- One alignment axis per section: eyebrow, H2 and lead share text-align and left edge in every home section; button labels are centred (equal left/right padding on all pills); section padding is a consistent 110px (56px mobile).
- Fonts load as specified: Open Sans 400/600/700/800 for display, Inter 400-700 for UI; no horizontal scroll at 390 or 1440.
- Hero video plays (WebM), scrim is light, H1 white worst-case contrast 4.2:1 on 66px type (passes large-text AA); the section after the hero is the logo strip then a diagram, not three equal cards.
- Reveal motion (0.75s, 26px, 3 stagger steps) is smooth; reduced-motion pauses the video, stops the marquee and Ken Burns, and shows all reveals.
- Mobile has no overflow; flow diagram becomes a vertical timeline; managed-it, location and case-study pages carry real, well-cropped photography.
- Contrast measured on every text node outside the video: only the vaf-seal numerals fail.

## Findings

### Blocker

**D-001** | `all pages, <768px` | Sticky quick bar (vaf-quickbar)
- What: Second sticky pill ('Call VAF') is white text on a white pill: the phone CTA is invisible on every mobile page.
- Evidence: Measured at 390: .pv-sticky .b color rgb(255,255,255) on background rgb(255,255,255), contrast 1.0:1. Visible in every mobile screenshot as a blank white pill beside 'Take the assessment'. Cause: --chrome-bg is #ffffff in the reskin block but the rule assumes a dark chrome.
- Fix: themes/vaf/css/vaf.css line ~578: change `.pv-sticky .b{background:var(--chrome-bg);color:#fff}` to `.pv-sticky .b{background:#0f1e33;color:#fff}` (or `background:var(--navy)`). Same fix for `.pv-calc .big`, `.pv-hot`-style rules that use var(--chrome-bg) with white text.

**D-002** | `/blog` | Blog listing template
- What: The blog listing is not on the VAF theme: default HubSpot header (Home / Products / Pricing / Blog / Company, purple 'Get started'), default dark footer with no content, placeholder intro copy, purple accent, and the same post repeated three times in the featured slots.
- Evidence: DOM check: no vaf stylesheet loaded, no .q-header, no .q-footer, h1 font Inter, body class hs-blog-listing; intro reads 'A brief introductory description of your blog and the topics covered at a high level. Just one or two sentences should be just right.'; duplicate card titles 'Print & Copy Solutions: Where Document Workflows Start' x3. Violates guardrails 'Never ship a blog listing page that does not match the theme'. (The post page /blog/... IS themed.)
- Fix: In HubSpot Settings > Website > Blog > Templates assign themes/vaf/templates/vaf-blog-listing.html as the listing template (post template vaf-blog-post.html is already live). Fill the blog description (vaf-blog-listing.module field `intro`), set featured count to 1 so the same post is not repeated, and delete the stray default-template featured grid. Re-run the gate `blog uses the theme`.

**D-003** | `/about` | vaf-stats band (q-tone-dark)
- What: Dark stats band renders four cream cards with WHITE numerals and white labels, illegible (1.06:1).
- Evidence: Measured: .vaf-stats .pv-stat background rgb(250,247,239), b color rgb(255,255,255), span rgb(255,255,255). Screenshot shows four blank cream cards in a navy band. Cause: .q-tone-dark forces white text for .pv-stat b/span but only restyles .q-card, not .pv-stat (vaf.css 134-139) and .pv-stat keeps background:var(--card) (vaf.css 811).
- Fix: themes/vaf/css/vaf.css after line 139 add `.q-tone-dark .pv-stat{background:rgba(255,255,255,.08);box-shadow:none;border:1px solid rgba(255,255,255,.16)}`. Better: delete the band entirely on /about, because it repeats the four hero stats directly above it (see D-016).

### Major

**D-004** | `all pages` | Header
- What: Header is `position:sticky` but never sticks: its module wrapper is only 82px tall, so the header scrolls away. The `is-scrolled` util-bar collapse in vaf.js is dead code. No persistent navigation or CTA on long pages (home is 16,646px tall).
- Evidence: Home scrolled to 2500px: .q-header getBoundingClientRect().top = -2500, computed position sticky, parent DIV.hs_cos_wrapper height 82px. Same at 390 (top -3000). Screenshots at scroll 800 show no header.
- Fix: themes/vaf/css/vaf.css: add `.hs_cos_wrapper_type_module:has(> .q-header){display:contents}` (sticky then binds to .body-wrapper), or in themes/vaf/templates/layouts/vaf-base.html wrap the header partial in `<div class="vaf-hdr">` and give `.vaf-hdr{position:sticky;top:0;z-index:60}` as a direct child of .body-wrapper. Keep `.is-scrolled .pv-util{max-height:0}`.

**D-005** | `all pages (desktop)` | Mega menu 'Solutions' feature panel
- What: The right-hand feature panel text is clipped: 'Know your Technology St' and 'Ten to fifteen minutes. Information,' are cut off at the panel edge.
- Evidence: Hover screenshot at 1440: feat column ~272px wide, headline and paragraph overflow and are hidden by .pv-mega{overflow:hidden}. Cause: vaf.css line 824 `.q-header .q-nav a{white-space:nowrap}` (specificity 0,2,1) beats `.pv-mega .feat{white-space:normal}` (0,2,0), and the nowrap is inherited by .feat b and p.
- Fix: themes/vaf/css/vaf.css after line 824 add `.q-header .q-nav .pv-mega .feat,.q-header .q-nav .pv-mega .feat *{white-space:normal}`. Also align the panel to the container: `.pv-mega{width:min(1240px,calc(100vw - 32px))}` (currently x=130..1310 vs container 100..1340).

**D-006** | `/` | vaf-seal (dark commitments)
- What: Stat numerals fail contrast: #2a71af on #223043 is 2.59:1 (needs 3:1 even as large text). The numerals are the point of the cards.
- Evidence: Measured on all 8 cards (1914, 93.4, SOC 2, Gold, 250+, 25, 24 hr, 57,000), 42px/800, rgb(42,113,175) on rgb(34,48,67) = 2.59. Visible as dim blue-on-navy in screenshot.
- Fix: themes/vaf/css/vaf.css line ~137 (`.q-tone-dark .pv-seal .badge b{color:var(--q-gold)}`) change to `color:#7fb9ee` (about 6.3:1 on #223043). Also themes/vaf/modules/vaf-seal.module/module.css `.vaf-seal .badge b` if it sets its own colour.

**D-007** | `all pages` | Colour tokens (guardrail: no composited text)
- What: Roughly 60 text nodes use translucent rgba text colour instead of solid or color-mix(): the whole footer, utility bar, hero lead and stat captions. Passes numerically (6.0:1 to 6.2:1 on light, 8.8:1 to 13.7:1 on the hero) but violates the explicit 'never composite text with opacity, use color-mix()' rule and is not auditable.
- Evidence: Computed color rgba(0,0,0,.62) on .q-footer-links a, .q-footer-tag, .q-footer-legal, .pv-util a; rgba(255,255,255,.9/.82/.78/.8) on .pv-lh .q-lead, .pv-hero-stats span, .fcard p, .vaf-proof small. Source: --chrome-muted:rgba(0,0,0,.62) in vaf.css line 221; `.pv-lh .q-lead{color:rgba(255,255,255,.82)}` line 638; lines 641-642, 649, 658.
- Fix: themes/vaf/css/vaf.css line 221: `--chrome-muted:#585e68;` `--chrome-border:#dcdfe3;` (solid). Replace every `rgba(255,255,255,.7x/.8x)` text colour in the .pv-lh, .pv-hero-video, .pv-calc .big, .q-tone-dark blocks with `color-mix(in srgb,#fff 82%,var(--navy))` (opaque result). Leave alpha only on borders and backgrounds.

**D-008** | `/` | Hero eyebrow over video
- What: Eyebrow 'BUSINESS TECHNOLOGY SIMPLIFIED, SINCE 1914' (13px, light blue) falls to about 2.7:1 against the brightest video pixels behind it; median about 5:1, so it flickers in and out of legibility as the video plays.
- Evidence: Hid text, sampled hero frames at t=2.5/5/7.5s in the 100..548 x 197..213 box: p98 background luminance gives 2.77, 2.72, 2.63:1 for colour rgb(131,173,209); H1 white worst case 4.2:1 (passes large), lead 9.1:1.
- Fix: themes/vaf/modules/vaf-hero.module/module.css: eyebrow colour to #cfe3f7 (>=7:1 on the darkest scrim) and add `text-shadow:0 1px 12px rgba(8,20,36,.55)`; extend the left scrim stop 0..38% to 0.78 alpha behind the text column only (the `.bg::after` gradient is fine on the right where the video should stay visible).

**D-009** | `/` | Hero card 'Already a customer?'
- What: 'Call (317) 634-2913' wraps to two lines inside a 144px button while its three siblings are one line, so the 2x2 button grid is uneven; copy 'A person answers. Monday to Friday, 7 to 5.' leaves orphan '5.' on its own line.
- Evidence: Screenshot at 1440 above the fold; measured link widths 144px, 14px Inter, label 'Call (317) 634-2913' = 2 lines. Heading is H2 at 21px inside a 350px card.
- Fix: themes/vaf/css/vaf.css line 655: `.pv-lh .fcard.b .links{grid-template-columns:1fr 1fr}` add `.pv-lh .fcard.b .links a{white-space:nowrap;font-size:13.5px;padding:0 10px;justify-content:center}` and make the last (phone) link span both columns (`.links a:last-child{grid-column:1/-1}`). Copy: 'A person answers, Monday to Friday, 7am to 5pm.' (vaf-hero module field `card_b_copy`).

**D-010** | `/ (mobile), /services/managed-it, /locations/indianapolis` | H1
- What: Hero H1 wraps to 4 lines: home at 390 (42px, 'Everything / your business / runs on, under / one roof.'), managed-it at 1440 (64px, 'Your IT / department, / without the / overhead.') and Indianapolis (64px, 4 lines with 'technology' touching the right container edge). Home desktop is 3 lines. Guardrail: headings never wrap to 3 or 4 lines.
- Evidence: Measured H1 line counts: home 1440 = 3 (66.2px, width 621), home 390 = 4, /services/managed-it split hero = 4, /locations/indianapolis = 4 (text right edge x=1340 = container edge).
- Fix: themes/vaf/css/vaf.css line 803: `.q-h1{font-size:clamp(34px,4.6vw,68px)}` -> `clamp(32px,3.7vw,56px)` and `.vaf-hero--split .q-h1{max-width:none;font-size:clamp(32px,3.4vw,50px)}`; line 356 `.q-h1{max-width:16ch}` -> 20ch. Shorten copy: 'Your IT department, without the overhead' keeps 3 lines max at 50px; mobile `@media(max-width:480px){.q-h1{font-size:34px}}`.

**D-011** | `/ (and every page)` | Header logo
- What: Logo is a 202x40 raster displayed at 242x48 (1.2x upscale) and served at 1x, so it is soft on every retina screen; the footer copy sits on a tinted background with a visible white rectangle behind it.
- Evidence: Header img naturalWidth 202, rendered 242x48 (home). Footer img 182x36 shows a white box on #eef4fa in the 1440 and 390 screenshots.
- Fix: Upload an SVG (or PNG at 2x, 484x96 and 364x72) to HubSpot Files and point vaf-header.module field `logo` / vaf-footer.module field `logo` at it; set width/height attributes to the new ratio in themes/vaf/modules/vaf-header.module/module.html (hard-coded width="202" height="40"). Until then add `.q-footer img{mix-blend-mode:multiply}` in vaf.css line 349.

**D-012** | `/ and /partners` | Logo wall (vaf-partners marquee and vaf-cards logo cards)
- What: Logos are not uniform in optical size or quality: Ricoh is a black dealer badge in a rectangle, Sophos is a tiny gold-partner badge, Microsoft is just the words 'Microsoft Partner', Fortinet renders about 16px tall, Juniper and Square 9 are tiny, Datto is faint; everything is grayscale at opacity .9 so brand marks lose meaning. Files are served at width=150, so they upscale on retina (Canon 150x45 shown at 159x48).
- Evidence: 2x screenshot of the 24-logo wall (logos_2x.png): sizes visibly range from 16px to 48px marks; computed filter grayscale(1), mix-blend-mode multiply, opacity .9, height 48px for every img. On /partners the card logos show opaque white boxes (Sophos, Microsoft, Datto, Canon, Kyocera) and a black box (Ricoh) on the tinted cards; EFI Fiery and Kofax have no logo at all, so card titles sit at different heights.
- Fix: themes/vaf/modules/vaf-partners.module/module.css: replace fixed `height:48px` with a normalised box `img{max-height:40px;max-width:132px;width:auto;height:auto}` plus a per-logo `scale` field (0.7 to 1.4) in fields.json so wide wordmarks and square marks read equal. Re-source Ricoh, Sophos, Microsoft, Juniper, Square 9, Fortinet, Datto as trimmed transparent SVG/PNG >=300px wide in HubSpot Files (hubfs/vaf/partners/). vaf-cards.module/module.css `.vc__logo img{mix-blend-mode:multiply;height:36px;object-fit:contain;object-position:left}` and reserve the logo row height (`min-height:36px`) so titles align when a logo is missing. Raise grayscale logos to colour on hover.

**D-013** | `/` | vaf-map (service area)
- What: The 'Three offices' section is unbalanced and the map is crude: heading/lead sit top-left, the three office rows sit bottom-right, leaving an empty block of about 580x400px top-right. The Indiana outline is a rough polygon (jagged south edge, no Lake Michigan notch, slanted top), and 'Fort Wayne' and 'Evansville' labels run across the outline stroke.
- Evidence: 1440 screenshots (home1440_12/13): list cards start at y~836 of a 1138px section; map figure max-width 420px, centred in a 3-row grid. At 390 the labels collide with the outline too.
- Fix: themes/vaf/modules/vaf-map.module/module.css: make `.vaf-map__wrap{grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);align-items:start}` and move `.vaf-map__head` into the left column under which the list sits; set `.vaf-map__fig{max-width:520px;margin:0 0 0 auto;position:sticky;top:120px}` on the right. Replace the SVG path in module.html with a simplified real Indiana outline (Natural Earth admin-1, 60 points) and offset labels: `.vaf-map__pin text{transform:translate(14px,4px)}` with the Fort Wayne label anchored left of its pin.

**D-014** | `/` | vaf-related (case studies) and vaf-related (blog) thumbnails, vaf-tabs image
- What: Imagery is generic stock or clip-art and inconsistent: case studies use a handshake stock photo, a holographic-heart stethoscope image and a glowing-icons hand; the Education photo is reused in the case card AND the Industries panel on the same page; blog thumbnails mix neon hologram stock, a flat grey (#4a4a4a) server clip-art illustration, and photos. The grey clip-art is also the hero of the post 'Data Discovery and Classification' (right half content, left half empty).
- Evidence: Image inventory: team-1200.jpg used twice (y 8380 and y 9274); security-1200.jpg/networking-servers-computers.jpg render on #444 grey. /blog/data-discovery... hero 1000x561 is mostly empty grey.
- Fix: Replace with VAF-owned photography (HQ building, vans, techs at a customer site, Customer Care Center) in HubSpot Files and set per-card `image` fields in vaf-related.module; give every thumb one treatment: `.vr__img img{aspect-ratio:8/5;object-fit:cover}` plus `.vr__img::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,rgba(15,30,51,.35))}`. For posts without a photo use a branded fallback tile (navy #0f1e33 with the pillar icon), never a grey illustration. Fix `vaf-blog-post.module` hero to `object-fit:cover` with a minimum 16/9 crop.

**D-015** | `/` | Section rhythm (hero > ... > seal)
- What: A run of five consecutive sections share the same centred eyebrow + centred H2 + full-width object grammar (vaf-proof, vaf-ba, vaf-flow, vaf-hot, vaf-seal), and vaf-seal (8-card grid) is directly followed by vaf-related (3-card grid): two card-grid sections in a row. The 'alternate sections speak from the left' rule does not reach vaf-flow or vf-faq (both q-bg-alt, both centred), so only 5 of 16 headings are left-aligned.
- Evidence: Measured h2 text-align per section top to bottom: C, L(chk), C(proof), C(ba), C(flow, alt), C(hot), C(seal), L(related), C(tabs), L(map), C(testimonials), C(cta), L(related), C(vid), C(faq, alt), L(ct). The left-align selector in vaf.css line 862 only targets `> .q-container > .pv-center` and `.vaf-head`.
- Fix: themes/vaf/css/vaf.css line 862: extend selector to `.q-section.q-bg-alt .vaf-flow__head,.q-section.vaf-flow .pv-center,.q-section.vf-faq .pv-center`. Reorder in scripts/vaf_build.py rhythm(): move vaf-tabs between vaf-seal and vaf-related, and put the testimonials between vaf-hot and vaf-seal, so no two card grids or two centred dark/figure sections are adjacent. Add a `align` (left|center) dropdown to vaf-ba, vaf-hot, vaf-seal, vaf-proof field groups.

**D-016** | `/about` | vaf-stats duplicate + adjacent dark
- What: Immediately under the dark hero (which already shows 1914 / 93.4 / SOC 2 / 4,000+) a second dark band repeats the same four stats (with 57,000 replacing 4,000+): two navy blocks fuse into 1,200px of navy and the stats read twice in a row.
- Evidence: Screenshot p_about_s0: hero stats strip at y~890, then the vaf-stats band y 1008..1380 repeating the figures.
- Fix: Delete the vaf-stats section on /about (themes/vaf pages manifest in scripts/vaf_build.py) or change the hero to `vaf-hero--nocards` without `pv-hero-stats`. Keep one proof statement per page.

**D-017** | `/about` | vaf-resources ('More from Van Ausdall & Farrar')
- What: An 11-card grid lists legal and policy pages (Cookie Policy, Disclaimer, CPRA opt-outs, Privacy, Terms, App Privacy Policy) under the heading 'More from Van Ausdall & Farrar', with auto-excerpts truncated mid-sentence: 'Please read this Cookie Policy carefully before using the https://www.vanausdall.com/ Website (the.', 'operated by Van Ausdall &.', 'using all of our.'. Looks broken and buries the page's conversion.
- Evidence: Screenshot p_about_s5; card copy ends with dangling '(the.', '&.', 'of our.', 'third.' and every chip says ABOUT. 11 cards = 3+3+3+2 centred.
- Fix: Remove the section from /about or replace with 3 hand-written cards (Careers, Locations, Case studies) in vaf-resources.module with real `desc` text; policies already live in the footer legal row. Never auto-excerpt.

**D-018** | `/about` | vaf-leadership
- What: Leadership cards use initials in a gradient circle ('EG', 'SS') instead of portraits: reads as unfinished on the page that is about people.
- Evidence: Screenshot p_about_s3, 96px circles with initials only.
- Fix: themes/vaf/modules/vaf-leadership.module/fields.json: add `photo` (image) per person and render `.av img{object-fit:cover;border-radius:50%}`; source real headshots from VAF (Eric von Grimmenstein, Steven Sigmon). Show the initials only as a fallback.

**D-019** | `/contact` | Page structure
- What: The contact page buries its one job: the form is the third section, about 1,460px down; above it are a centred hero with a four-line lead and a nine-line 'what happens next' paragraph. Below it come a FAQ, 12 'Where to go next' cards, 8 industry cards, and two more detail/office sections: a site index, not a contact page. Two adjacent card-grid sections (12 + 8 cards).
- Evidence: Section order from DOM: hero(632) > detail(650) > vf-ct(856) > faq > resources(804) > resources(1089) > detail > locations. Resource cards 'Managed IT Services Indianapolis' and 'Copier Sales and Lease' have no description so heights/titles are uneven.
- Fix: Rebuild as a split hero (themes/vaf/modules/vaf-contact.module or vaf-leadform.module on the right, offices + hours + phone on the left) so the form is above the fold at 1440 and 390. Delete both vaf-resources sections on /contact; keep vaf-locations and FAQ. In vaf-resources.module make `desc` required or collapse the row.

**D-020** | `/services/managed-it` | vaf-proof + vaf-ba
- What: The 24/7 proof section and the before/after slider are both q-bg-alt and touch, so they form one 1,400px pale-blue block with no seam: breaks 'alternate the background'.
- Evidence: Section list: vaf-proof.q-bg-alt (top 1997, 562px) immediately followed by vaf-ba.q-bg-alt (top 2559).
- Fix: scripts/vaf_build.py rhythm(): when two adjacent sections resolve to the same tone, flip the second (`bg-alt` <-> white) and never flip a section to dark that is not tone-dark by design. Quick fix in vaf.css: `.q-bg-alt + .q-bg-alt{background:#fff}`.

**D-021** | `/case-studies/tippecanoe-school-corporation` | vaf-casestudy headline
- What: The dark 'The numbers' band sets the full summary sentence as an H2 that wraps to 5 lines at 40px ('New print and copier fleet reduced overall equipment count and provided $1M in savings.'); the same claim is also in the lede, the pull quote, the dark quote and the FAQ: four repeats.
- Evidence: Screenshot p_cs_s1: H2 block 420px wide, 5 lines; measured guardrail breach (max 2 lines).
- Fix: themes/vaf/modules/vaf-casestudy.module/module.css: `.vaf-casestudy .h{font-size:clamp(28px,2.6vw,36px);max-width:22ch}` and grid `1.15fr .85fr`; shorten the field value to '1,200 machines became 300, saving $1M.' Remove the duplicate in-prose pull quote.

**D-022** | `all pages (mobile)` | Footer legal row
- What: Copyright is flush against the left screen edge (x=0) and 'Privacy' ends at 384/390: the legal row has no gutter on mobile. On desktop it is 40px wider than the footer grid (x=60 vs 100) so the copyright and 'Cookie policy' do not align to the column edges. A 130px white strip also shows beneath the footer on mobile.
- Evidence: Measured at 390: copyright x=0, Privacy right edge 384; at 1440 legal row spans 60..1380 vs grid 100..1340. Cause: vaf.css line 342 `.q-footer-legal{...padding:18px 0 22px}` overrides .q-container's padding; `body{padding-bottom:130px}` line 579 exposes the white page background.
- Fix: themes/vaf/css/vaf.css line 342: `padding:18px 40px 22px` and `@media(max-width:767px){.q-footer-legal{padding:18px 20px 22px}}`; line 579: remove `body{padding-bottom:130px}` and instead `@media(max-width:767px){.q-footer{padding-bottom:96px}}`. Same 40px inset for `.pv-partners .q-container` (border line at 60..1380 vs content 100..1340).

**D-023** | `/ (home)` | Page length and repetition
- What: Home is 16,646px at 1440 (24,368px at 390) with 18 sections. The same facts repeat: 93.4 NPS appears in the hero stats, the proof numeral, the seal card and the testimonial lead; 1914 / SOC 2 / Mitel appear in hero stats AND the seal; 'Four pillars' is told twice (wheel, then hotspot floor plan) and the Education case study photo shows twice. Strong modules, but the page reads as a catalogue of every module.
- Evidence: Section list heights: hero 767, partners 271, wheel 1045, chk 952, proof 611, ba 902, flow 1167, hot 1351, seal 1016, related 833, tabs 863, map 1138, testimonials 1089, cta 491, related 885, vid 987, faq 703, ct 836.
- Fix: Cut to about 13 sections: drop the hero stat strip OR the vaf-seal (keep the numbers once, in vaf-proof as a 3-up count-up), merge wheel and hotspots into one ('Four pillars' wheel, hotspots on the floor plan as the detail view), remove vf-vid from the home (it lives on /about). Expected saving about 3,000px. Edit order in scripts/vaf_build.py page spec for '/'.

### Minor

**D-024** | `/` | vaf-partners strip spacing
- What: Dead space around the logo strip: 8px above, 70px below, then the next section's 110px top padding gives about 180px of white under the logos plus a floating 'PAUSE SCROLLING' link; the border-top rule runs 40px past the content edges.
- Evidence: Computed: .pv-partners padding 8px 0 70px, next section padding-top 110px. Rule spans x=60..1380 vs content 100..1340.
- Fix: themes/vaf/css/vaf.css line 366: `.pv-partners{padding:0 0 24px}`; `.pv-partners .q-container{padding-inline:40px}`; put the pause control inline right of the caption (vaf-partners.module/module.css).

**D-025** | `/ and /services/managed-it` | vaf-ba 'Drag to compare' pill
- What: The hint pill sits on the divider and the 2px divider line runs through the word 'COMPARE'.
- Evidence: Screenshot home1440_05 and p_managedit_s2: line crosses the pill text.
- Fix: themes/vaf/css/vaf.css line 753: `.pv-ba .hint{z-index:5}` (above .handle z-index 3) or move it to `bottom:14px;left:calc(var(--pos) + 24px)` so it follows the handle; add `background:#fff;padding:6px 12px;border-radius:999px`.

**D-026** | `/` | vaf-flow steps
- What: In the process diagram the 'Produces' divider for step 4 (Monitor) sits 20px higher than the other three (y 467 vs 487), so the four columns do not share a baseline.
- Evidence: Screenshot home1440_06: step 1-3 divider aligned, step 4 higher because its card has no 'selected' padding.
- Fix: themes/vaf/modules/vaf-flow.module/module.css: make `.node button` a grid with `grid-template-rows:auto auto auto 1fr` and give all four the same padding as the selected card (`padding:13px`).

**D-027** | `/` | vaf-testimonials
- What: Featured quote column ends at about y=480 while the right-hand letters run to y=780: roughly 300px of empty space under the lead quote, so the section looks lopsided. The lead quote itself is 5 lines at 36px.
- Evidence: Screenshot home1440_14.
- Fix: themes/vaf/css/vaf.css line 498: `.pv-tst-feature{align-items:stretch}` and add the author photo/logo plus the 'View all reviews' link at the bottom of the lead column (`.pv-tst-feature figure.lead{display:flex;flex-direction:column;justify-content:space-between}`); cap quote at `clamp(22px,2vw,28px)`.

**D-028** | `/` | pv-cta ('Is your business ready for AI in 2026?')
- What: Mid-page conversion moment is plain: white section, no eyebrow, no cover image of the playbook, one button, 491px of padding. It is the weakest section on the page and sits between two card grids.
- Evidence: Screenshot home1440_15.
- Fix: themes/vaf/modules/vaf-cta.module: add `tone` = dark and an `image` field (playbook cover mock); layout split 1.1fr/.9fr with eyebrow 'FREE PLAYBOOK'. CSS: `.vaf-cta--dark{background:var(--navy);color:#fff}` reusing the .q-tone-dark rules.

**D-029** | `/ and sub-pages` | Heading alignment axis
- What: Some sections have an eyebrow and others do not (vaf-related x2, vaf-map, vf-faq, vf-ct, pv-cta have none), so section openers differ in construction; the left/right 'heading + right-aligned lead at x=980' pattern in vaf-related sits on the baseline of the lead, not the heading.
- Evidence: Section audit: eb:null for related, map, cta, faq, ct. Within each section eyebrow, H2 and lead do share one alignment axis (measured, all consistent).
- Fix: Add an `eyebrow` field with a default to vaf-related.module, vaf-map.module, vf-faq (vaf-faq.module), vaf-cta.module and vaf-contact.module; align the right lead to `align-self:end` with the H2 baseline.

**D-030** | `all pages` | Type scale floor
- What: About 80 text nodes are 12 to 13px (eyebrows 13px, SVG wheel labels '01..04' 12px, vaf-ba labels 12px, flow caption 12px, hero stat captions 13px). Small uppercase tracked text at 12px is hard to read on blue.
- Evidence: Measured: 82 nodes <14px on home 1440; 12px in vaf-wheel, vaf-ba, vaf-flow, hot pop.
- Fix: themes/vaf/css/vaf.css: set a floor `--fs-label:13px` and raise `.pv-hot .pop .k,.pv-ba .k,.pv-sl .drawer .k` (12px) to 13px; wheel SVG `.lab` 13px -> 14px and numerals `font-size:13px`.

**D-031** | `/` | Card titles font mix
- What: Card h3s in vaf-seal (17px) and vaf-related/case and blog cards (20px) use Inter 700 while h3s in the wheel, tabs, flow, cards and detail use Open Sans 700/800: the display/UI pairing is applied inconsistently.
- Evidence: Measured h3 font families: Inter for 'Serving Indiana since 1914', 'Tippecanoe School Corporation', blog titles, 'Start here' card; Open Sans for 'Information', 'Five vendors', 'Education'.
- Fix: themes/vaf/modules/vaf-seal.module/module.css and vaf-related.module/module.css: add `h3,.vr__title{font-family:var(--q-serif);font-weight:700;letter-spacing:-.015em}`.

**D-032** | `all pages` | Card surface and radius system
- What: Three card fills and at least five radii are in play: cream #faf7ef cards on the home, blue-tint #eef4fa cards on service/location/contact pages, white cards on tinted sections; radii 12/14/16/20/22/24/28px and 6px form button vs 999px pills. Shadows differ (0 14px 36px vs 0 8px 24px vs 0 10px 26px).
- Evidence: Computed: .q-card 16px, .pv-seal .item 22px, .pv-tl2 .card 20px, .pv-hero-img 28px, .vc__card 16px; submit button radius 6px (live) vs `.q-form .hs-button{border-radius:999px}` declared in vaf.css 804.
- Fix: themes/vaf/css/vaf.css: define `--r-card:16px;--r-lg:24px;--sh-card:0 10px 30px rgba(0,5,69,.07)` and use them in .q-card, .pv-seal .item, .vc__card, .vr__card, .pv-tl2 .card; add `.q-form .hs-button,.q-form input[type=submit]{border-radius:999px!important}` (HubSpot form CSS currently wins).

**D-033** | `/partners, /contact` | Hero lead
- What: Centred long-form lead: 5 lines on /partners and 4 lines on /contact at about 640px, against 'no centred long-form body copy'.
- Evidence: Screenshots p_partners_s0, p_contact_s0.
- Fix: themes/vaf/modules/vaf-hero.module/module.css `.vaf-hero--centered .q-lead{max-width:56ch;text-wrap:pretty}` and trim copy to two lines, or left-align the lead.

**D-034** | `/ and sub-pages` | Orphans in leads and captions
- What: Single-word last lines: 'eighty.' (vf-chk lead), 'each.' (vaf-hot lead), 'to.' (checklist score card 'Check what you cannot answer yes to.'), '5.' (hero card), 'Center.' (wheel lead).
- Evidence: Screenshots home1440_02/03/07/09.
- Fix: Add `text-wrap:pretty` to `.q-lead,.pv-split p,.vf-chk__sc *` in vaf.css (line 233 region) and edit copy: 'Check any you cannot answer yes to. They are six of the eighty.' etc.

**D-035** | `/` | Hero mobile length
- What: On mobile the hero is 1,700px tall (H1, lead, CTA, 2x2 stats, card A, card B, 4 stacked buttons) before the partner logos; two cards push the first content section about 2.5 screens down.
- Evidence: Measured .pv-lh height 1700px at 390.
- Fix: themes/vaf/css/vaf.css line 659: `@media(max-width:767px){.pv-lh .fcard.a{display:none}.pv-lh .fcard.b .links{grid-template-columns:1fr 1fr}}`; the assessment CTA is already the primary button. Reduce `.pv-lh .q-container{padding-top:56px;padding-bottom:56px}` on mobile.

**D-036** | `/ (mobile)` | vaf-seal, vaf-flow, vaf-tabs
- What: Mobile stacks 8 single-column commitment cards (2,458px), a 1,942px vertical flow, and industry tabs whose chips clip ('Engineering and constructior') with no scroll cue.
- Evidence: Measured section heights at 390: seal 2458, flow 1942; tabs screenshot sheet390_4.
- Fix: vaf.css line 737: change to `@media(max-width:480px){.pv-seal{grid-template-columns:1fr 1fr;gap:12px}.pv-seal .item{padding:18px 16px}.pv-seal .badge b{font-size:30px}}`; tabs: `.pv-tabs [role=tablist]{mask-image:linear-gradient(90deg,#000 85%,transparent)}` plus snap scroll (vaf-tabs.module/module.css).

**D-037** | `/ (mobile)` | Headings
- What: Four H2s wrap to 3 lines at 390/27px ('Information, communication, print and process, from one partner'; 'Six questions from the Technology Strength Assessment'; 'Drag to see what changes when the office has one number to call'; 'Four stages, and every one of them hands you something'). Also H3 'Know your Technology Strength Score' 3 lines.
- Evidence: Measured line counts at 390.
- Fix: Copy trims in the page spec (scripts/vaf_build.py): 'Four pillars, one partner', 'Six questions from the assessment', 'One number to call. Drag to compare.', 'Four stages. Each hands you something.' Or `@media(max-width:480px){.q-section .q-h2{font-size:25px!important}}`.

**D-038** | `/ (mobile)` | Hotspot pins
- What: Pins are 34px (39px selected) on a 350px-wide floor plan: below the 44px tap size and close together (6/7/4/5 cluster).
- Evidence: Measured .vaf-hot__pin 34x34 at 390.
- Fix: themes/vaf/modules/vaf-hotspots.module/module.css: `@media(max-width:767px){.vaf-hot__pin{width:40px;height:40px}.vaf-hot__pin::before{content:"";position:absolute;inset:-6px}}` and rely on the numbered list below the image for navigation.

**D-039** | `/` | Reduced motion
- What: With prefers-reduced-motion: reduce the hero video is paused, marquee and Ken Burns are off, reveals are visible; but the hotspot pin pulse (`vafHotPulse`) still runs on 7 pins because the rule `.vaf-hot *{animation:none!important}` does not match ::before/::after pseudo-elements.
- Evidence: document.getAnimations() under reduced motion lists 7 running vafHotPulse animations.
- Fix: themes/vaf/modules/vaf-hotspots.module/module.css line 58: `.vaf-hot *,.vaf-hot *::before,.vaf-hot *::after{animation:none!important;transition:none!important}`. Audit other modules with pseudo-element animations the same way.

**D-040** | `/` | Launcher pill 'Already a customer?'
- What: Fixed bottom-left pill (x=18..215) overlaps left-aligned section text at 1440 while scrolling (seen over the vf-chk lead and footer logo). Competes with the mobile sticky bar's role on small screens (hidden <768, correct).
- Evidence: Screenshots home1440_02/03 show the pill covering text.
- Fix: themes/vaf/css/vaf.css line 777: `.pv-sl{left:auto;right:20px}` (right is free of content at 1440) and `bottom:20px`; keep the drawer opening leftward (`.pv-sl .drawer{left:auto;right:0}`).

**D-041** | `/ (hero)` | Hero poster
- What: The poster is 1097x617 stretched to 1440x767 (the requested 2100px was not produced), so the first frame before the video starts is soft; the video itself is 1280x720.
- Evidence: Measured naturalWidth 1097 vs rendered 1440.
- Fix: Upload a 2400x1000 JPG poster to HubSpot Files and set vaf-hero.module field `poster`; keep `preload="metadata"` and `width/height` attributes.

**D-042** | `/services/managed-it, /locations/indianapolis` | Split hero + proof stack
- What: Under the split hero the same trust facts stack three times: the floating image badge (93.4 or 'Local'), a four-stat strip (1914, 93.4, SOC 2, 4,000+ identical on every service and location page), then a 3-item dot ribbon, with about 100px of dead space above and below the ribbon.
- Evidence: Screenshots p_managedit_s0, p_loc_s0; ribbon sits y 1110 with 110px padding both sides.
- Fix: In scripts/vaf_build.py hero spec for service/location pages: drop the ribbon, vary the stat strip per page (managed IT: 24/7 SOC, help-desk response time), and set `.pv-ribbon{display:none}` as a stop-gap in vaf.css.

**D-043** | `all pages` | Breadcrumbs
- What: Breadcrumb treatment differs: service/location/about pages use a bordered .pv-crumbs bar directly under the header (49px); case study and blog post use the unbordered .pv-bc (192px from top, 60px gap), so the first heading sits at a different height per template.
- Evidence: Screenshots p_about_s0 vs p_cs_s0 vs p_post_s0.
- Fix: themes/vaf/templates/layouts/vaf-base.html and vf-article module: render the same `.pv-crumbs` component everywhere (vaf.css 324-328) and delete .pv-bc.

**D-044** | `/blog post` | Meta
- What: Post date renders as 'Oct 17, 2026, 12:00:00 PM'; no related posts after the CTA band.
- Evidence: Screenshot p_post_s0.
- Fix: themes/vaf/modules/vaf-blog-post.module/module.html: `{{ content.publish_date|format_date('long') }}` (no time) and add a 3-card related-posts row using vaf-related.

**D-045** | `all pages` | Footer link columns
- What: The Solutions column is split into two CSS columns where the second list has no heading, so 'Managed print' starts about 35px below 'Managed IT services' and the two lists do not share a baseline; line height collapses where labels wrap ('Backup and recovery' / 'Business phone systems' touch with no gap) while other rows have 6px gaps; Support column rows are unevenly spaced.
- Evidence: Screenshots home1440_20, p_about_s6: first list items y 387/434/468/494/533/573, second list 394/421/468/494/533/580.
- Fix: themes/vaf/css/vaf.css lines 337-338: `.q-footer-links a{min-height:0;padding:7px 0;line-height:1.35}` and replace the two-column flow with a real second heading ('Print and process') in vaf-footer.module so each column is a separate `<div>`; add `column-gap:28px;orphans:2` and `.q-footer-links.pv-two{columns:1}` at 1440.

**D-046** | `/contact` | Resource cards
- What: 'Where to go next' cards repeat an eyebrow chip 'SOLUTIONS' on every card and two cards have no description, making rows uneven.
- Evidence: Screenshot p_contact_s2.
- Fix: vaf-resources.module: hide the chip when all cards share a kind (`{% if not all_same %}`), require `desc`.

**D-047** | `/` | Mega menu
- What: Panel width 1180 left=130 does not line up with the 1240px content column (100..1340); feature panel eyebrow wraps to two lines ('NOT SURE WHERE TO START?').
- Evidence: Measured .pv-mega x=130 w=1180.
- Fix: vaf.css line 307: `.pv-mega{width:min(1240px,calc(100vw - 32px))}`; shorten `feat_eyebrow` to 'Start here'.

## Make the home page astonishing (ranked by impact vs effort)

1. **Sticky, condensed header with the assessment CTA.** Low effort, high impact. Fix D-004 and keep a 56px header (logo, nav, 'Schedule a consultation') after 80px of scroll; every long page gains a persistent conversion path.
2. **Own-photography pass.** Medium effort, highest impact. Replace stock/clip-art (case cards, blog thumbs, leadership initials, the grey server illustration) with VAF's building, vans, technicians and Customer Care Center; one crop and gradient treatment. Biggest single jump from 'template' to 'owned'.
3. **One proof section instead of four.** Low effort, high impact. Collapse hero stats + 93.4 numeral + 8-card seal into a single vaf-proof with three count-up numbers (93.4, SOC 2, 1914) triggered on reveal; removes about 1,000px and the repetition.
4. **Hero: make card A a live 3-question starter.** Medium effort. Turn 'The Technology Strength Assessment' glass card into real checkboxes (same component as vf-chk) that route into the assessment with the answers pre-filled; the hero becomes interactive proof, not a promo card.
5. **Logo wall rebuilt as a two-row static grid.** Low-medium effort. 12 curated vendors, uniform optical box, 2x SVG, colour on hover, no marquee needed (keeps reduced-motion free); see D-012 for assets.
6. **Real map.** Medium effort. Accurate Indiana outline, service-radius shading that animates in on reveal, pins linked to the office rows, a branch photo in each row.
7. **Closing conversion band.** Low effort. Replace the plain AI-playbook CTA with a navy split band (playbook cover mock + 2-field form) and reuse it as the last block before the footer on every page.
8. **Contact page: form above the fold.** Medium effort. Split hero with form on the right, offices/hours/phone on the left with an 'Open now' status chip computed from local time; delete the site-index sections.

## Layout variety: runs of similar sections (home)
- vaf-proof, vaf-ba, vaf-flow, vaf-hot, vaf-seal: five in a row with centred eyebrow + centred H2 + full-width figure (D-015).
- vaf-seal (8 cards) then vaf-related (3 cards): two card grids adjacent.
- /contact: vaf-resources (12 cards) then vaf-resources (8 cards).
- /services/managed-it: vaf-proof and vaf-ba both pale blue, adjacent.
