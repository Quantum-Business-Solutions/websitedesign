# Intake: what to feed the machine

The list of inputs that make a new client build smooth, in the order they are needed, with who
supplies each and what happens if it is missing. Hand this to whoever is talking to the client.
Everything downstream (`/mockups`, `/preview`, `/build`) reads from these files and nothing else.

Version 1.0, 2026-09-06.

---

## The two files everything reads from

| File | What it is | Who fills it |
|---|---|---|
| `brands/<slug>.md` | The brief: promise, constraints, entity facts, SEO baseline, proof points, competitors, directions, decision | QBS, from discovery + research. Template: `brands/_template.md` |
| `brands/<slug>.content.json` | The site: brand tokens, nav, footer, schema, every page as a list of sections, plus the pitch block | QBS, from the brief and the client's current site. Reference: `brands/kelly-office-solutions.content.json` |

The brief is the record. The content file is the build. A change to copy goes in the content file;
a change to what we know about the client goes in the brief.

## Day one: from the client (ten minutes on a call)

Ask for all of it at once. Every item here has a default that ships if it does not arrive by the
date you give (`process/SCHEDULE.md`).

| Ask | Why | Default if missing |
|---|---|---|
| **Legal name** of the company | Organization schema, footer, copyright | Trading name from the site, flagged |
| **The logo, as a vector** (SVG or AI), plus any light-ground / dark-ground variants | Header, footer, `og:image`, schema | The PNG from their site. Note whether it needs a dark ground (Kelly's does) |
| **Primary accent and secondary colour** (hex) | The re-skin | Measured from their site with Firecrawl `branding` |
| **The one line a visitor must believe** (interview question 4, verbatim) | The hero, the promise | Their current homepage tagline, flagged as unconfirmed |
| **Ground preference**: light, dark, or no opinion | Filters the nine themes (rule 1) | No opinion; the vertical decides |
| **Two or three sites they like, two they hate** | Direction selection, category read | Competitors from Semrush |
| **Service lines**, in their words, in their order | Nav, services list, footer | Their current nav |
| **Locations**: address, phone, hours for each | Location pages, LocalBusiness later | Their contact page, flagged |
| **Proof points**: years, headcount, customers, response time, ratings, awards, authorizations | The stat band, the case-study metrics | Only what the site or public sources state; nothing invented |
| **Their process as a deck**, stage by stage | The framework section, the retainer argument | The stages on their current site, flagged |
| **Testimonials and case studies** we may use, with permission | Social proof | The ones already public on their site |
| **Photography**: what exists, who owns it | Hero and every image | One generated stand-in, labelled; a shoot proposed |
| **Partner and manufacturer logos** we are authorized to show | Logo strip, sameAs | The ones on their current site |
| **Social profiles**: LinkedIn company page, Facebook, X, YouTube, Google Business | `sameAs`, footer | Only the ones linked from their site |
| **Named recipient for form submissions** | Conversion path, form test record | Blocked at step 29 until named |
| **HubSpot portal id and tier**, and a private app token in `CLIENT_HUBSPOT_TOKEN` | The build | Blocked at Phase 4 |
| **Who approves**: one name for direction, one for copy, one for go-live | Approvals at 13, 17, 20, 35 | The person who signed the SOW |

## Day one: from QBS (before the client call)

- Semrush baseline: domain overview, organic keywords, top pages, striking distance. `process/seo-baseline.md`.
- Two or three competitors measured with Firecrawl `branding`: colours, type, ground, CMS.
- BrandCommand: `list_brands` for the brand profile id; `website_projects` and `builder_pages` for anything already built.
- Hindsight recall on the company: meetings, contacts, constraints already stated.
- Vertical layer, if one exists (`verticals/<vertical>.md`): page set, module kit, keyword profile.

## What the content file needs, section by section

`brand`: accent, ink_secondary, chrome (dark or light, decided by the logo), logo path, phone and
`tel:` href, email, utility links (what existing customers do on the site), CTA, social, tagline,
footer columns, legal links.

`schema`: org_name, org_url, org_logo, org_description, sameAs, telephone.

`nav`: label and file, five to seven items.

`pages`: one entry per page with `file`, `title` (with the brand after a pipe), `description` (140
to 160 characters) and `sections`. Section types available in `scripts/preview.py`: hero (split or
centered), partners, stats, services, process, casestudy, cards, band, locations, faq, contact,
detail, listing, team, cta. Card counts that balance: 2, 3, 4, 5 (stays five across), 6, 8. Seven
goes in a list, not a grid.

`pitch`: what we heard, what we found, the reasons for our pick tied to what they said, the one
thing we would change, the alternatives, the plan, and who at QBS answers.

Rules for every string: no em dashes; no claim without a source in the brief; no adjective
stacks; write for their visitor, not for us.

## What comes out, and in what order

1. `/mockups <client>`: the brief filled, three directions chosen, the pitch page rendered.
2. `/preview <client>`: three complete clickable sites plus the hub, generated into the client repo,
   auto-deployed by Vercel at `https://<slug>.vercel.app`.
3. The gate on every generated page, and the QA agents on the hub and the home page. Nothing goes to
   the client under 80.
4. The client picks. The choice and their words go in the brief.
5. `/build <client>`: clone, re-skin, blog templates, pages, in their HubSpot.

## The three things that slow every build

1. **The promise arrives late.** Everything hangs off it. Ask for it on day one and ship the default.
2. **The logo is a small PNG.** Ask for the vector on day one. Check whether it needs a dark ground.
3. **Nobody owns the form.** Name the recipient before the build starts, not at launch.
