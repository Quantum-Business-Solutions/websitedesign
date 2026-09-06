# Layer 2 — Office technology and managed print

The house system (`themes/`, `design/`, `process/`) is layer one: it works for anybody. This is
layer two: everything that is true of **copier dealers, managed print providers and office
technology companies** and would otherwise be rediscovered on every build.

**This vertical is already the majority of the book.** Six of the ten `website_projects` in
BrandCommand are office technology:

| Client | Site | Accent measured | Type | Platform |
|---|---|---|---|---|
| Revolution Office | revolutionoffice.com | `#F5A622` amber on white | Poppins | WordPress / Elementor |
| Kelly Office Solutions | kellyofficesolutions.com | `#65BC7B` green + `#000545` navy | Jost / Roboto | WordPress |
| Imagine Technology Group | itgarizona.com | `#c41e2a` red + `#4a9b8e` teal | Inter | — |
| Managed IT / MSP | — | `#3dae1e` green | Inter | — |
| CCG / corpcomm | corpcomm.com | `#B22A2E` red + `#3D72E7` blue | Montserrat / Open Sans | WordPress |
| Pacific Office Automation | pacificoffice.com | — | — | — |

Plus Semrush projects for Aztec Office, OEM Connect and CCI Voice, and live QBS assets already
aimed here: *Q2: The Revenue Machine for Copier Dealers*, the *Office Technology Prospecting
Playbook*, and the *Copier Dealer AEO Guide*.

---

## What the category actually looks like

Measured, not assumed.

**Light ground, saturated mid-tone accent.** Amber, green, red — never a dark-premium palette. So
the relevant Quantum themes are **Clean, Press, Paper, Journal, Showcase**, and the four dark ones
are usually wrong for the category.

> ⚠️ **This collides with a known defect.** Those five are exactly the themes that fail WCAG AA on
> button contrast (3.52–3.9:1). A saturated amber or green accent makes it *worse*: Revolution's own
> amber is **1.86:1 on white**. Every build in this vertical needs the two-token accent fix in
> `themes/architecture.md` — `accent` for fills, `accent_ink` for accent text. This is not optional
> here; it is the category's defining colour problem.

**Sans-serif, mostly.** Poppins, Jost, Inter, Montserrat. A serif reads as law-firm, not
technology. Of the light five, **Clean** and **Showcase** match the category; **Press**, **Paper**
and **Journal** are the deliberate differentiators — which can work, since the whole category looks
the same, but it's a stretch call not a safe one.

## The traffic reality, and it's uncomfortable

Pacific Office Automation, one of the largest independents in the country. Their top 20 organic
keywords:

- **Branded:** "pacific office automation" (9,900), "pacific automation" (3,600), plus a dozen
  location and spelling variants — all position 1
- **Jobs:** "pacific office automation careers" (110), "…jobs" (110), "…job" (40) — a real share of
  their organic traffic is people looking for work, not buyers
- **Non-brand commercial, the entire list:** "printer lease" (1,900, pos 4), "lease copiers" (390,
  pos 1), "office automation" (480, pos 1)

**Dealers rank for their own name and for job seekers. They do not rank for what they sell.**

Three consequences:

1. **The non-brand commercial head terms are lease/rental terms** — "printer lease", "copier lease",
   "managed print services", "cost per page". Short, transactional, and winnable because the
   category invests almost nothing in content.
2. **Local intent is the real volume.** "copier lease `<city>`", "managed print `<state>`". Which
   means location pages matter — and see the multi-location gap below.
3. **The blog is the whole growth story here, and it is the weakest thing we produce.** Live critic
   scores put `blog` at 67.4 against 85.1 for every other asset type. In a category that invests
   nothing in content, a genuinely good blog is the entire competitive opening — and right now it
   is our lowest-scoring output. Fix that before selling content-led growth to a dealer.
4. **A Launch-tier build in this vertical is selling a conversion surface to someone whose traffic
   is their own brand name.** Say so. The content engine is where the growth is, and it starts at
   Growth.

## Positioning: lead with the assessment, not the lease

From Tom Menton's brief for Revolution, and it generalises:

> *"Revolution Office as a national managed print and office technology company, with the
> **assessment process at the center of the story** — not a copier dealer leading on lease
> savings."*

Every dealer in the category leads on price and equipment. The differentiator is the **process**:
a fleet assessment, a documented finding, a projected saving, a guarantee. That is what
`process-steps`, `workbook-extract`, `deliverable` and `guarantee` exist for.

## The vertical module kit — already built

Revolution's HubSpot theme carries **29 content modules**. Seventeen of them have no equivalent in the nine, and they are the layer-two kit. Two apparent
matches are **not** gaps — `before-after` and `stats-band` already exist in the 57, so don't port
those:

| Module | What it does | Why the category needs it |
|---|---|---|
| `cost-calculator` | Devices × pages × cost-per-page → spend | **The highest-intent module in the category.** Fields: `devices`, `pages`, `cpp`, `cta` |
| `savings-ledger` | Line-item current vs proposed | Fields: `headers`, `lines`, `footer`. The assessment made visible |
| `fleet-diagram` | The device fleet as a picture | Nobody else shows the buyer their own estate |
| `workbook-extract` | A page of the actual assessment deliverable | Proof the process is real, not a sales step |
| `deliverable` | What they physically receive | Turns a service into an object |
| `guarantee` | The service-level promise | Response time and uptime are the category's real currency |
| `process-steps` | The assessment, step by step | Lead with this, not the lease |
| `association-strip` | Association and partner logos | Dealer credibility runs through associations |
| `award` | Manufacturer and industry awards | Every dealer has them and most bury them |
| `logo-wall` | Manufacturer authorisations | Ricoh, Canon, Kyocera, Sharp, HP, Xerox |
| `before-after` | The fleet before and after | The clearest single proof in the category |
| `contrast-pair` | Us vs manufacturer-direct | The actual competitive question a buyer is asking |
| `reframe-band` | Reframes the buying question | Moves off price |
| `stat-band` | Years, technicians, response time | The four numbers every dealer has and rarely leads with |
| `spotlight` · `narrative` · `checklist` | Editorial support | — |

Plus **seven drag-and-drop sections** — `assessment`, `close`, `faq`, `outcome`, `partners`,
`proof`, `solutions` — a pre-composed page grammar. Building a dealer page becomes *choosing seven
sections*, not twenty modules.

**Port these to the nine as a vertical module set**, don't rebuild them per client. That is the
single highest-value thing in this file.

## The standard dealer page set

Known in advance, which is what makes the vertical repeatable:

1. **Home** — lead with the assessment
2. **The assessment / how it works** — the differentiator, its own page
3. **Managed print services**
4. **Copiers & multifunction devices**
5. **Managed IT** (most dealers now sell it)
6. **VoIP / unified communications** (many do)
7. **Production print** (some do)
8. **Service & support** — response times, technician count, coverage
9. **About / heritage** — Kelly's 78 years is a real asset
10. **Locations** — ⚠️ see below
11. **Contact / request an assessment**
12. **Cost calculator** — its own page, its own template
13. **Case studies** — by vertical: healthcare, legal, education, government
14. **Blog** — the traffic engine, and the thing the category neglects

## Kelly Office Solutions — the page set, already built

The BrandCommand builder already holds a full eight-page Kelly build with real meta titles and
descriptions, which is the best evidence of the real dealer page set:

**Home · What We Do · About · Service & Support · Industries · FAQ · Contact · Blog**

Details worth reusing across the category:

- **Heritage is an asset.** *"Office Technology Done Right Since 1947"* — 78 years, family-built.
  Most dealers have decades and bury it.
- **Service lines are enumerable.** Kelly's six: office products, managed print, document
  management, production print, IT services, and a water/coffee line. Ask for the list; it drives
  the page set.
- **Industries is its own page**, not a paragraph: healthcare, legal, education, manufacturing,
  financial services, government. Each one is also a case-study bucket.
- **Service & Support is a selling page**, not a support page — same-day service, automated
  supplies, online training, customer portal.
- **Locations are named in the meta description** — Winston-Salem, Greensboro, Hickory, Charlotte.
  Four locations, which is the multi-location gap below, on a client we already have.

The builder is a real demo-website tool with real content in it. **Check it before starting any
dealer build** — the page set, the meta descriptions and the service-line taxonomy may already
exist.

### The dealer page set as now built for Kelly (the template for the next one)

`brands/kelly-office-solutions.content.py` is the reusable shape. Swap the constants and the assets
and the same script produces the next dealer's site:

| Block | Pages | Notes |
|---|---|---|
| Home | 1 | hero, partner marquee, stats, "is this you" checklist, services list, brand film, process, testimonials, industry tabs, customer fast lane, locations, FAQ, assessment form |
| Services | 7 | one per line: copiers, managed print (four assessment steps, five reports, lease/rent/buy table), document management, production print (film), IT, mailing, water/ice/coffee |
| Industries | 1 + 5 | index plus legal, healthcare, faith-based, architecture, manufacturing |
| Local | 1 + 4 | index plus one page per branch with LocalBusiness schema, hours, named services, branch phone |
| Tools | 2 | cost calculator (sliders), assessment (what you get, what it costs) |
| Company | 3 | about (timeline, owners, values, community), careers, supplies and service |
| Blog | 1 + 9 | listing plus nine posts, each with chapters, FAQ, a form and related reads; the topics are the category's evergreen searches (cost, lease vs buy, water cooler cleaning, same-day service) |
| Contact | 1 | form plus branches |

The next dealer needs: their service-line list in their words, their branches with phones and hours,
their partners (logos), four to six testimonials with names, their process stage names as published,
their films if they have them, and the real photography. Everything else is already written to be
swapped.

## The proof points every dealer has

Ask for these in step 5 of the runbook; they are the `stat-band` and they are always available:

- Years in business · number of technicians · average response time (hours) · first-call fix rate
- Manufacturer authorisations · devices under management · pages managed annually
- Association memberships · uptime or SLA guarantee · service coverage area

## Known gaps that bite in this vertical specifically

1. **⚠️ Multi-location is a hard blocker.** Dealers are regional with 3–20 branches, and location
   pages carry local search. **No location, address, hours or map module exists in the 57, and no
   `LocalBusiness` schema.** Until a `quantum-location` module exists, either scope this as custom
   or say plainly it's out. Do not promise local SEO we cannot mark up.
2. **⚠️ Everyone is on WordPress.** Revolution, Kelly and CCG all are. `process/` has no CMS
   migration procedure — no content inventory, no asset migration, no cutover, no rollback. In this
   vertical that is the *normal* case, not the edge case.
3. **HubSpot free tier caps site pages at 30.** The page set above is already 14 before locations
   or case studies. Check the client's tier at kickoff — `themes/architecture.md`.
4. **Healthcare and legal case studies** need the client's customer's approval, which takes longer
   than anyone plans for.

## Selecting three directions for a dealer

1. **Ground: light.** The category is light. Confirm against the brief, but expect light.
2. **Safe** — **Clean**. Matches the category, maximum clarity for a buyer comparing specs.
3. **Stretch** — **Showcase**. Contemporary, still sans, visibly more modern than their peers.
4. **Wildcard** — **Press** or **Paper**. A serif in this category is a genuine differentiator
   because nobody does it; Revolution's own third direction was Fraunces, and Tom kept it in the set.
5. **Apply the two-token accent fix on all three**, or the buttons fail.
6. **Never** show two of Press / Paper / Journal — all light serifs, one slot wasted.

## What Revolution taught us about their own site

Measured with `firecrawl_scrape` and worth checking on every dealer, because it is probably typical:

- **`h1` renders at 14px while body is 22px** — the page's most important heading is smaller than
  its body text. A one-line fix and a real ranking signal.
- Three conflicting `viewport` meta tags.
- `googlebot: noindex,indexifembedded` on the homepage — verify that is intentional.
- Button radius `0px` while the global radius is `4px`.

Run `node scripts/verify.mjs <their-domain>` on any dealer before the call. In this category it
reliably produces a diagnosis, which is exactly what `process/outbound-mockups.md` needs.
