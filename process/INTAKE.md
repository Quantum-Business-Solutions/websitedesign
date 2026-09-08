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

`nav`: five to seven top items. Each is `[label, file]` for a plain link, or a dict with
`children: [[label, file], ...]` for a dropdown, or `groups: [{title, items}]` plus an optional
`featured` card for a mega menu. The mobile menu becomes accordions automatically, and the current
section is marked on every page.

`crumbs`: on any page, `[[label, file], ...]` renders a breadcrumb with BreadcrumbList schema.

**Three compositions from one content file.** A page may carry `compose: {clean: [ids], showcase:
[ids], press: [ids]}` to order and select its sections per direction, and any section may carry
`variants: {press: {...}}` to override fields in one direction. Give every home section an `id`.
This is how the three directions stop being three skins.

**Products.** When the client sells things, every product gets a page under `products/` and a
`products.html` catalogue, and the mega menu lists all of them in groups. The Kelly script's
`PRODUCTS` list is the shape: slug, group, title, image, one-liner, body, benefits, bullets, FAQ,
brands. Only what the client's own site or a signed brief states.

`pages`: one entry per page with `file` (nested paths allowed: `services/managed-print.html`,
`blog/<slug>.html`, `locations/<city>.html`), `title` (with the brand after a pipe), `description`
(140 to 160 characters), optional per-page `schema` (a list of JSON-LD objects, for LocalBusiness on
location pages and BlogPosting on posts) and `sections`.

Section types, all in `scripts/preview.py` and `scripts/preview_sections.py`:

| Family | Types |
|---|---|
| Openers | `hero` (split or centered, image, badge, note, `stats` proof strip, `ribbon` band), `hero-video`, `partners` (auto-scrolling logo strip; static on Press) |
| Proof | `stats` (count-up on scroll, years and small numbers stay still), `testimonials` (grid, or `layout: feature` for one big quote and a letters column), `proof` (one giant numeral), `casestudy`, `leadership`, `timeline`, `values`, `video` (Vimeo behind a poster and play button, or a self-hosted mp4) |
| Offer | `services` (list), `cards` (3D tilt on hover), `resources`, `tabs` (industries or steps, with image), `process`, `comparison` (table), `checklist` (interactive), `calculator` (three sliders, live result), `detail`, `band` |
| Local | `locations` (phone at the card foot), `map` (state outline with a pin per branch, from lon/lat), `faq` |
| Content | `listing` (blog index), `article` (breadcrumb, table of contents, chapters, pull quote, callout, author), `related` |
| Convert | `contact`, `leadform`, `cta` (suppressed automatically on pages with a form), `sticky` (mobile two-button bar, set once under `brand.sticky`) |

Card counts that balance: 2, 3, 4, 5 (stays five across), 6, 8. Seven goes in a list, not a grid.

**Author the JSON from a script, not by hand.** `brands/kelly-office-solutions.content.py` is the
pattern: the facts live once as Python constants (services, industries, locations, partners,
testimonials, posts), builder functions turn each service, industry, city and post into a page, and
`build()` writes the JSON. Thirty-six pages from about 600 lines, and a new dealer is a new
constants block, not a new file of prose. Blurbs come from `brief()`, which cuts at a sentence or
clause boundary, never mid-sentence.

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

### Signature modules (added 2026-09-08, `scripts/preview_modules.py`)
Every one degrades to plain HTML: a list, a grid or a poster. Motion stops under `prefers-reduced-motion`.
Place them with `compose` per direction; ids are what `compose` references.

| type | Required fields | Optional | Renders |
|---|---|---|---|
| `hero-layered` | `heading`, `subhead`, `primary`, `image` (2100 wide plate), `image_w/h` | `eyebrow`, `secondary`, `stats [[value,label]]`, `card_a {eyebrow,title,body,items,cta}`, `card_b {eyebrow,title,body,links}`, `note` | Dark full-bleed hero, pointer glow, two floating cards with parallax and tilt, stats strip |
| `wheel` | `heading`, `items [[label, blurb, href]]` (5 to 8) | `eyebrow`, `intro`, `panel_eyebrow`, `link_label` | SVG ring, hover or focus swaps the panel, autoplays until touched; ordered list fallback |
| `flow` | `heading`, `steps [{label, when, summary, title, body, receive[]}]` | `eyebrow`, `intro`, `detail_eyebrow`, `receive_label`, `alt` | Numbered nodes on a self-drawing line, click for detail; vertical on phones |
| `fleet` | `heading`, `items [{title, band, brands, image (PNG cutout), bullets[], href}]` | `intro`, `alt` | Scroll-snap rail of tilting device cards |
| `seal` | `heading`, `items [[mark, title, body]]` | `eyebrow`, `intro`, `source` | Conic badge grid; every line must be sourced |
| `beforeafter` | `heading`, `before {title, body, items}`, `after {title, body, items}` | `eyebrow`, `before.eyebrow`, `after.eyebrow`, `hint`, `range_label` | Range-driven reveal; two stacked panels under 768px |
| `hotspots` | `heading`, `image`, `image_w/h`, `alt`, `items [{x, y, k, title, body, href, label}]` (percent coords) | `eyebrow`, `intro` | Numbered points with popovers; numbered list fallback. Shawn: "a great concept on almost any client." Any business with a place works: an office floor for a dealer or MSP, a clinic, a plant floor, a campus, a warehouse, a storefront. Generate the isometric with the client's rooms named in the prompt, then place the points by measuring the render (scripts/_offsets.mjs and a screenshot). |
| `model3d` | `heading`, `poster` | `intro`, `model` (GLB path), `alt`, `cta`, `id` | `<model-viewer>` with the poster shown until the element is defined; plain image when `model` is absent |
| `brand.launcher` | `label`, `links [[label, href]]`, `phone` | | Fixed bottom-left drawer, appears after 560px of scroll |

Directions: pass `--recommend` only when we are recommending; without it the hub shows "Your call" with the three cards and the switcher carries no "(recommended)". Order in `--themes` is the order on the hub and in the switcher.

Content-file helpers for Kelly: `_flow()` and `_ba()` build service-page modules from tuples; `SERVICE_MODULES[slug]` lists what each service page inserts after its benefits cards.
Generated 3D: Higgsfield `generate_image_batch` (product render, plain white ground, no logos) then `remove_background(media_id=job_id)` then `generate_3d(model image_to_3d, should_texture:true)`; the textured GLB lands around 4MB. Label it generated in the intro.
A brand's primary line goes first in every brand list (Kelly: Sharp).
