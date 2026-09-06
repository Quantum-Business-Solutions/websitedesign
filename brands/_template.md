# <Company>

- **slug:** <slug>
- **brand_profile_id:** <uuid from list_brands — create the profile first if the client is new>
- **package purchased:** Launch / Growth / Transform / custom — **decides re-skin depth**
- **current site:** <url> (<platform>)
- **tokens:** `design/tokens/<slug>.json` if ingested
- **HubSpot subscription (client's):** <tier — required for blog, forms, meetings>
- **Client portal id:** <id — the site lives here, NOT in QBS 20682069>
- **Pages allowed by their subscription:** <n — free tier caps site pages at 30>
- **Pages planned:** <n — if this exceeds the line above, stop>

## The promise

The client's answer to interview question 4, **verbatim**. What does this site have to make a
visitor believe? Everything downstream hangs off this, and it is the one thing you cannot infer.

> "<their words>"

## The design read

Reading this as: **<page kind>** for **<audience>**, with a **<vibe>** language.

## Client-stated constraints — these outrank house defaults

Verbatim where possible, with who said it and when. This section is the most valuable part of the
file: it is the difference between designing for this client and designing for the category.

- <constraint> — <who, when>

## Entity facts — for structured data

Consumed by `process/structured-data.md` and by `scripts/reskin.py --org-*`. Get these in Phase 01;
they are the difference between a client site that owns its identity and one that ships ours.

- **Legal name:** <exact>
- **Canonical URL:** <https://…>
- **Logo URL:** <absolute>
- **`sameAs`** — company profiles the client controls, absolute `https://`, name/address/phone
  matching the site. In priority order (`process/structured-data.md` → *sameAs*):
  - LinkedIn **company** page: <https://www.linkedin.com/company/…>  ← the one that matters most
  - Google Business Profile (Maps share URL): <…>
  - Manufacturer authorized-dealer listing (office tech): <…>
  - Crunchbase / Clutch / G2 / BBB, whichever the category uses: <…>
  - YouTube / Facebook, only if active: <…>
  - ⛔ Never a QBS profile. `reskin.py` blocks it; `verify.mjs` fails it.
- **Locations:** <count, and addresses if local>
  - ⚠️ **More than one location?** No location/address/hours module exists in the 57 and there is no
    `LocalBusiness` schema. Multi-location is **out of tier** — scope it as custom. See
    `process/structured-data.md`.

## SEO baseline — before we touch anything

From `process/seo-baseline.md`. **This is the number the engagement gets measured against.** No
baseline, no way to prove the optimisation window worked.

- **Organic traffic:** <n>/mo · **keywords:** <n> · **traffic value:** $<n>/mo
- **Semrush project id:** <id — create it on day one; the crawl takes hours>
- **Top five pages by traffic**, and whether they're articles or service pages:
  | Page | Traffic | Share |
  |---|---|---|
- **Striking distance** (position 11–20, volume > 100, difficulty < 30):
  | Keyword | Pos | Volume | KD |
  |---|---|---|---|
- **Site Health:** <n> · **specific errors:** <list>

## Conversion paths

Two per page, minimum — `process/launch-standards.md`.

- **Hard offer:** <book a call / demo>
- **Soft offer:** <gated asset / calculator / grader>
  - ⚠️ **If the client has no gateable asset, that's a scope item.** Surface it now, not in week ten.

## URL migration map

Every page earning traffic today gets a **301** — not a 302. A redesign that changes URLs without
them destroys the only traffic the client has.

| Old URL | Traffic | New URL | 301 in place |
|---|---|---|---|

## Their process — ask for the deck

The single highest-return question in discovery. Their real internal process, staged, is the
differentiator; the generic industry version is what every competitor publishes. See
`design/patterns.md`.

- **Deck received:** <y/n, date>
- **Stages:** <name each, and what each one PRODUCES — the artifact, not the activity>
- **Outcomes they attach to it:** <the "and then what">
- **Does it loop?** <if it returns to stage one, that is the retainer argument>

## Brand assets

- Logo: <url>
- Palette: <hex values, and whether measured or supplied>
- Type: <faces, and whether licensed>
- Photography: <what exists, what has to be sourced — one set per location if multi-site>
- Figma: <link if the client supplied one — most precise source available>

## Audience

Who decides, what they need to see to act, and what makes them distrust a site.

## Competitors ingested

Named on the pitch main page, so these have to be real. `firecrawl_scrape` with
`formats: ["branding"]`.

| Competitor | Ingested | What the category looks like |
|---|---|---|

## Directions produced

| Name | Theme | Rationale | Status |
|---|---|---|---|
| <Company> — <ThemeName> | <one of the nine> | Direction 1 of 3. <one line> | draft / shown / chosen |

Use the real theme name — the clone is `<Company> — <ThemeName>`, and labelling it after a theme it
isn't will confuse everyone later.

## Chosen direction, and why — in their words

The rejected two are worth as much as the winner.

- **Chosen:** <name> — "<why, their words>"
- **Rejected:** <name> — <reason> · <name> — <reason>

## Regulated-industry review

Delete if not applicable. Health, finance, legal and anything YMYL: who reviews clinical or
compliance claims **client-side**, the testimonial policy, and whether authorship needs a named
credentialed person (it does, for medical content — that's a content requirement, not a markup one).

## Guardrails specific to this client

Things true here that should NOT be promoted to `design/guardrails.md`.

- <rule>
