# Van Ausdall & Farrar

- **slug:** vanausdall
- **brand_profile_id:** none yet in BrandCommand; create at step 9
- **package purchased:** not yet. This is the pitch. Recommend **Growth** (48 pages per direction; 12 solutions, 8 industries, 3 offices, case studies, blog)
- **current site:** https://www.vanausdall.com (custom CMS by Atomic8Ball / "Design by A8B"; Helium AI chat widget; ADP careers; forms embedded from a third party)
- **client repo:** `Quantum-Business-Solutions/vanausdall`, connected to Vercel project `quantum-business-solutions1/van-ausdall`. Every push to `main` deploys.
- **Preview:** https://van-ausdall.vercel.app (hub; each direction opens in its own tab, every page built)
- **tokens:** measured 2026-09-08 via Firecrawl branding: accent `#2A71AF` (buttons, links), theme-color `#006fbf`, body `#403D39` on white, Poppins throughout, 5px radius
- **HubSpot subscription (client's):** VAF runs AgentDealer on Salesforce and e-automate today (Hindsight, July 2026). A HubSpot demo and configurator project were in progress in July and August 2026 with Patrick Dodge. Portal id and tier: **to confirm**
- **QBS contact on the account:** Shawn Peterson. **Client contacts seen in meetings:** Patrick Dodge, Brian Courtney, Nolan Flike, Hanna Bowden (Hindsight, June to August 2026). Who approves the website: **to confirm**
- **Revenue, for scoping:** about $26M (Hindsight, July 2026). Indiana's largest full-service office technology provider, privately owned.

## The promise

⚠️ **Not yet from an interview.** These are VAF's own published lines, verbatim, used until someone at VAF answers question 4 directly.

> "Business Technology Simplified" (under the logo)
> "Everything your business needs, under one roof since 1914" (home hero)
> "Indianapolis' Trusted Managed Technology Partner" (home H1)

## The design read

Reading this as: **a regional managed-technology provider site** for **CIOs, IT directors, office managers and owners at Indiana SMBs, schools, hospitals and municipalities**, with a **plain, established, competent** register: 1914 as proof of staying power, the Technology Strength Assessment as the method, audited service scores instead of adjectives.

## Client-stated constraints — these outrank house defaults

None recorded yet from a design conversation. What the live site asserts:

- Blue `#2A71AF` is the brand; the logo is a charcoal wordmark with a blue striped V, built for a **light** ground. Chrome stays light in every direction.
- Four pillars organize everything: **Information, Communication, Print, Process** (partners page, city pages). The nav uses them.
- The **Technology Strength Assessment™** is the signature process: four assessments in two parts each, 10 to 15 minutes, "eliminate, optimize, leverage". It is the primary CTA.
- Existing customers use the **Client Service Center**: support, supplies, IT support emails and the Customer Care Center number. One click from the header.
- Copier brands: Canon, Ricoh, Kyocera, HP (home, copier pages). Partners page adds Brother and Zebra.
- Tone: proof over hype, Indianapolis and Indiana named, dry humor allowed ("two world wars, two pandemics and a few bad Colts teams").

## Entity facts — for structured data

- **Legal name:** Van Ausdall & Farrar, Inc. (footer copyright, CEO Juice report)
- **Canonical URL:** https://www.vanausdall.com (with www)
- **Logo URL:** https://www.vanausdall.com/images/logo.png (981×196 PNG; ask for a vector and a reversed variant)
- **`sameAs`**
  - LinkedIn company: https://www.linkedin.com/company/van-ausdall-&-farrar ✅ footer
  - Facebook: https://www.facebook.com/Vanausdallinc/ ✅ footer
  - Instagram: https://www.instagram.com/vanausdallinc/ ✅ footer
  - Google Business Profile: https://goo.gl/maps/ekbY63gHTu56ifBd8 ✅ footer
  - YouTube channel UC7KLcaxIeSjWl_67SK5An_A (careers video) — confirm it is theirs before adding
- **Locations:** 3. Indianapolis HQ (6430 E 75th Street, 46250, (317) 634-2913, M–F 7:00am–5:00pm, 57,000 sq ft, built 2006), Fort Wayne (1241 N Wells Street, 46808, (260) 432-1547), Evansville ((812) 424-5736, **no street address published**). Toll-free (800) 467-7474. Fax (317) 638-1843.
  - Service area pages exist for Indianapolis, Bloomington, Columbus, Evansville, Fort Wayne, Muncie, South Bend, Fishers, Carmel, Noblesville, Greenwood with near-identical copy. Only the three real offices get pages; the rest is a service-area list.
  - ⚠️ Multi-location is the known gap in the nine themes (no location module, no `LocalBusiness`). The preview carries `LocalBusiness` on the three office pages; the HubSpot build needs a `quantum-location` module or a custom section.
- **Emails:** support@, supplies@, itsupport@, clientsuccess@, careers@ (all vanausdall.com)

## SEO baseline — before we touch anything

Semrush US database, 2026-09-08. **This is the number the engagement gets measured against.**

- **Organic traffic:** 1,081/mo · **keywords:** 365 · **traffic value:** $1,015/mo · **paid:** none · Semrush rank 1,060,314
- **Semrush project id:** none yet. Create on day one.
- **About 80% of traffic is branded:** the five brand variants (van ausdall & farrar inc, van ausdall and farrar, van ausdall & farrar, van ausdall, vanausdall) are 79.9% of visits between them. **The home page earns 85% of all organic traffic.** 25 URLs earn anything.
- **Top pages by traffic**
  | Page | What it ranks for | Kind |
  |---|---|---|
  | `/` | branded terms | home |
  | `/blog?p=what-are-the-benefits-of-a-physical-intrusion-detection-system-240503` | physical intrusion detection #6 | **blog post, the second-highest traffic URL** |
  | `/contact/` | branded and phone-number terms | contact |
  | `/fort-wayne/managed-it-solutions-fort-wayne-in` | managed it services fort wayne #6, 49 keywords, business phone systems #25 (9,900/mo) | **best non-brand page** |
  | `/fort-wayne/cloud-solutions-fort-wayne-in` | cloud services management fort wayne indiana #2 | city page |
  | `/evansville/managed-it-solutions-evansville-in` | managed it evansville #2, managed it services evansville #2 | city page |
  | `/blog?p=document-conversion-the-key-to...` | document conversion companies #2, digital document conversion #5 | blog post |
  | `/communication/business-phone-systems` | voip phone systems indianapolis #5 | service |
  | `/knowbe4/free-phish-alert-button` | phish alert button #15 (390/mo) | partner page, keep |
- **Striking distance:** "business phone systems" 9,900/mo at #25 via the Fort Wayne page; "cloud services brownsburg" #14; "managed it service munster" #18.
- **What this means for the build:** (1) Indianapolis, the HQ market, does not appear in the top 50 for managed IT: the Indianapolis pages are the largest untapped local opportunity; (2) the Fort Wayne and Evansville pages are the non-brand earners and get 301s to the office pages; (3) blog posts live on `blog?p=` query-string URLs and need real URLs with per-post titles, images and `BlogPosting`; (4) the phone systems page and guide are aimed at the 9,900/mo term.
- **Site defects seen on the live site (2026-09-08):** the contact form renders the placeholder string `as5d4f65s4f564we654fw` on the home, contact, support and print assessment pages; home `og:image` is a stock AI-hand image; the customer comments meta description says "since 1974" against 1914 everywhere else; "112 years" is hardcoded on the history and why pages.

## Conversion paths

- **Hard offer:** Schedule Your Free Consultation (`/get-started`) · (317) 634-2913 · Speak with a Solutions Expert form (currently broken, see above)
- **Soft offers, already theirs:** Technology Strength Assessment (10 to 15 minutes, saves for later), Free Print Assessment, 2026 CIO AI Playbook (gated download), KnowBe4 free Phish Alert Button. The preview adds a print cost calculator.

## URL migration map

Every page earning traffic today gets a **301**. Fill the right-hand columns at step 14.

| Old URL | Traffic | New URL | 301 in place |
|---|---|---|---|
| `/` | ~80% branded | `/` | n/a |
| `/fort-wayne/managed-it-solutions-fort-wayne-in` | best non-brand | `/locations/fort-wayne` | ☐ |
| `/evansville/managed-it-solutions-evansville-in` | managed it evansville #2 | `/locations/evansville` | ☐ |
| `/fort-wayne/business-phone-systems-in-fort-wayne-in` | business phone systems #25 | `/services/business-phone-systems` | ☐ |
| `/fort-wayne/cloud-solutions-fort-wayne-in` | cloud fort wayne #2 | `/services/cloud` | ☐ |
| `/blog?p=what-are-the-benefits-of-a-physical-intrusion-detection-system-240503` | 4% of traffic | `/blog/physical-intrusion-detection-systems` | ☐ |
| `/blog?p=document-conversion-the-key-to-unlocking-efficiency-and-accessibility-241101` | doc conversion #2 | `/blog/document-conversion-services-what-to-expect` | ☐ |
| `/communication/business-phone-systems` | voip indianapolis #5 | `/services/business-phone-systems` | ☐ |
| `/knowbe4/free-phish-alert-button` | 390/mo | keep | ☐ |
| `/case-studies/*` (18) | low | `/case-studies/*` same slugs | ☐ |
| `/industries/*-technology-solutions` (8) | low | `/industries/<short>` | ☐ |
| other city directories (9) | near zero | `/locations` | ☐ |

⚠️ Query-string blog URLs (`blog?p=`) need redirect rules that match on the query, which HubSpot's URL mappings do not do natively. Plan for a small redirect script or keep the old `blog` path serving a 301 index.

## Their process — ask for the deck

**Technology Strength Assessment™** → **eliminate, optimize, leverage** roadmap → **We Implement** → **We Monitor 24/7** (print page). The assessment has four parts (Information, Print, Process, Communication) in two sections each, about 80 yes/no questions, with a Technology Summary Scorecard. Ask how the score is calculated and what the client receives after.

- **Deck received:** no
- **Stages:** Assess · Roadmap · Implement · Monitor (drafted from the site; theirs to replace)

## Brand assets

- Logo: URL above (raster). Ask for SVG and a reversed variant.
- Palette, **measured** 2026-09-08: blue `#2A71AF` (accent, buttons), `#006fbf` (theme-color), link `#0066CC`, body `#403D39`, white ground. `#2A71AF` on white is about 5.6:1, so it passes as button fill with white text and as link text; `reskin.py` derives the rest.
- Type: **Poppins** for everything, 32/24/20px. One family at one weight is the boilerplate signature; every direction pairs a display face against a body face.
- Photography: hero and section images on vanausdall.com are stock-style (data center, hands with AI letters, healthcare). One real photo of the HQ entrance and one of the president. The 75th Street building, the Document Conversion Center, technicians and the service fleet are the shoot.
- Video: careers film on YouTube (`i-q4U5SnvaM`). Used on About and Careers.
- Partner logos on hand (from `/images/partners/`): 8x8, Arctic Wolf, Brother, Canon, Datto, Elevate, Fortinet, Fujitsu, HP, Juniper, KnowBe4, Kyocera, Microsoft, Mitel, N-able, OnBase, OPEX, Ricoh, RingCentral, Sophos, Square 9, Tenable, VMware, Zebra.

## Proof points — the `stat-band`

All on the record:

- **Since 1914**, chosen as a Thomas Edison Company distributor (say "since 1914", not a year count)
- **NPS 93.4**, audited by CEO Juice, World Class (above 70) every year 2019 to 2025; average US company 10
- **SOC 2** certified (home page badge)
- **Mitel Gold** seven consecutive years, top 7% of 1,400 partners; **in telecom since 1983, 4,000+ systems**
- **Fortinet** Engaged Advanced Partner, NSE-7 engineers, first SD-WAN Specialization in the Great Lakes region
- **250+ years** of combined IT experience on the Vsecure team, CISSP on staff; sales tenure 15 years average
- **25-point inspection** on every service call; Customer Care Center responds within **24 hours**, M–F 7 to 5
- **57,000 sq ft** HQ (2006) with the secure Document Conversion Center
- Case studies with numbers: Tippecanoe $1M and 1,200→300 devices; STAR Financial 70%; Johnson Memorial 1.5M files in 90 days; City of Anderson $40,000/yr
- Ten real customer comments from after-service surveys (first names and dates)

## Audience

CIOs and IT directors at 50 to 500-person Indiana organizations; office and facilities managers who own the copier and the phones; owners of SMBs and non-profits; administrators in schools, hospitals, cities and utilities. Cost-conscious, insurance-driven on security, burned by vendors who do not answer. They decide on **one accountable partner, local response, and proof someone else audited.**

## Competitors ingested

Not yet. Day-one task: measure two Indianapolis MSPs and one copier dealer with Firecrawl `branding`. The office-technology vertical read (`verticals/office-technology.md`) applies: light ground, saturated mid-tone accent, phone-number-forward.

## Directions produced

| Name | Theme | Rationale | Status |
|---|---|---|---|
| Van Ausdall & Farrar — Clean | Quantum Clean | **The clear one, and our recommendation.** Light, humanist sans, maximum clarity: the design that says Business Technology Simplified without saying it. Credible to a CIO and an office manager alike | full preview site, 48 pages |
| Van Ausdall & Farrar — Showcase | Quantum Showcase | **The technology-partner one.** Same light ground, a display grotesque and bigger rhythm; the four pillars as a wheel, the seven-vendor comparison, the process front and center | full preview site, 48 pages |
| Van Ausdall & Farrar — Press | Quantum Press | **The established one.** Editorial serif on warm paper. 1914, Edison, four generations of leadership and an audited service score land harder in a serif. Nobody in the category looks like an institution | full preview site, 48 pages |

All three light, per `verticals/office-technology.md` and the logo. Signal considered as a dark IT-forward wildcard and dropped: the wordmark is charcoal with no reversed variant, and "simplified" is not a dark register. It stays in reserve if the first call reveals appetite.

**Preview:** https://van-ausdall.vercel.app. Content source of truth: `brands/vanausdall.content.py`, which writes `brands/vanausdall.content.json`. Forty-eight pages per direction: home, solutions plus 12 solution pages, industries plus 8 industry pages, case studies plus 4 full case studies, Technology Strength Assessment, free print assessment, cost calculator, CIO AI Playbook, about, partners, careers, Client Service Center, locations plus 3 office pages with `LocalBusiness` schema, blog plus 6 posts with `BlogPosting` schema, contact. Gate run on five pages 2026-09-08: A grades (94 to 96), all failures were LCP under a single-threaded local server; re-run against the Vercel URL.

## Chosen direction, and why — in their words

- **Chosen:** —
- **Rejected:** —

## Guardrails specific to this client

- The Technology Strength Assessment is the primary CTA on every page. "Schedule a consultation" is secondary. Do not invert them.
- The Client Service Center links (support, supplies, IT support) never move below the fold on mobile.
- Never print "112 years" or any year count. Say "since 1914".
- Do not collapse the four pillars into "IT" and "print". Communication and Process are revenue lines with their own certifications and case studies.
- Print the service commitments exactly as VAF states them (24-hour response, same-day for most metro calls). Do not tighten or round them.
- Steven Sigmon's quote is from the managed IT page; confirm before it ships.

## 2026-09-08: preview built and deployed

Three directions generated in one pass from the live site, the CEO Juice report and Semrush; no interview yet. Client repo created and pushed; Vercel project `van-ausdall` auto-deploys from `main`. Everything unverified is on the hub's "To confirm" list (13 items), starting with the Evansville address, office hours and who approves.
