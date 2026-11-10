---
description: Headless. From a Client Command brief to three complete directions. Runs inside the Website directions workflow; nobody is watching.
argument-hint: "<slug>"
allowed-tools: Read, Write, Edit, MultiEdit, Glob, Grep, Bash, WebFetch
---

Build the three directions for `$ARGUMENTS` from the brief Client Command sent. **Nobody is watching.**
There is no one to ask, so decide by the written rules, and put every fact you could not source under
`pitch["confirm"]` instead of guessing. **Nothing here touches HubSpot, Vercel, BrandCommand or Client
Command directly**; the workflow around you does the upload and the commit.

This is `/preview` with the interview replaced by a form. Same output, same rules, and now the same gate:
`process/directions-standard.md` says what the result must be, and `scripts/directions_qa.py` fails the build when it is not.
The quality bar is the Kelly, Revolution and Van Ausdall & Farrar builds. A thin, brochure-like home page, a colour that
is not theirs, a display face they do not use, or white type on a pale photograph is a failed build, not a style choice.

## 0 — What is already on disk

| Path | What it is |
|---|---|
| `brands/<slug>.brief.json` | The form a teammate filled in Client Command: `client`, `short`, `domain`, `cities`, `city_tag`, `vertical`, `ground` (light, dark or none), `accent`, `promise` (the one line a visitor must believe, verbatim), `service_lines`, `likes`, `dislikes`, `notes`, `portal` (what Client Command knows about the client), `qbs_contact` (who started it), `base_url` (where the site will be served), `seo` when Client Command has run its SEO/AEO analysis on this domain, and **`branding`** when Client Command could measure the live site: `colors` (primary, secondary, accent, background, textPrimary), `fonts` (family and role), `radius` (cards, inputs), `button_radius`, `buttons`, `logo`, `colorScheme`. |
| `brands/<slug>.audit.json`, `brands/<slug>.urls.txt`, `/tmp/<slug>-html/` | Every sitemap URL fetched and scored by `newclient.py`. Empty when the site has no sitemap: then fetch the home page and every page its navigation links to with `curl -sL -A "Mozilla/5.0"` into `/tmp/<slug>-html/` yourself before writing a word. |
| `brands/<slug>.content.py`, `.seo.json`, `.build.json`, `.types.json` | Scaffolded from the starters by `newclient.py`. If this client was built before, these are the real files: update them, do not start over. |
| `../out-<slug>/` | The output folder, with `assets/` inside. |

Report where you are with `python3 scripts/cc.py progress $CC_BUILD_ID <step> "<one line>"` at the start of
each numbered section below; the steps are `read`, `brief`, `themes`, `content`, `render`, `gate`. The
teammate sees that line in Client Command.

## 1 — Read, in this order

1. `process/directions-standard.md` (what done means: read all of it), `process/INTAKE.md` (what the content file needs, section by
   section), `design/guardrails.md` (always and never, the card-grid rule), `themes/catalogue.md` (the selection rules).
2. `verticals/<vertical>.md` when `brief.vertical` names one that exists (`office-technology` does). It knows
   the category's page set, module kit and colour problem.
3. `brands/_template.md` (the brief), then **the two rich examples**: `brands/nexus-network-technologies.content.py` and
   `brands/image-2000.content.py` (28 and 34 module types, a `compose` list per direction, builders for `flow`, `beforeafter`,
   `seal`, `proof`, `map`, `timeline`); `brands/kelly-office-solutions.content.py` (facts as constants, a builder per page type,
   `build()` writes the JSON); `library/README.md` (stand-in imagery you may use, and how to label it).
4. Then the client: the brief, the audit, the fetched HTML of the home, about, services, locations and contact pages, and
   their live CSS (`curl -sL` the stylesheet the home page links).

## 2 — The brand, measured

Before the record, before the themes, **measure the client's brand** (`process/directions-standard.md`, section 1). In this order:
`brief.branding` (Client Command measured it with a real browser); then the live CSS (the primary button's background and radius,
the heading and body `font-family`, the header background); then the logo file itself. Write what you found into
`brands/<slug>.md` under "Brand", and into the content file's `brand` block as `accent`, `bg_alt`, `navy`, `chrome`/`chrome_bg`,
`fonts` (`{"heading": ..., "body": ...}`), `radius` (cards and inputs), `button_radius` (buttons) and `logo`.

- Download **their** logo into `../out-<slug>/assets/` (`curl -sL -A "Mozilla/5.0"`; static asset URLs usually work even when the pages sit
  behind a bot challenge). Look at it: white type means `chrome = "dark"` with a `chrome_bg`. Never type a wordmark in CSS while a real file exists.
- If the site is behind a bot challenge, **do not try to get past it.** Use the sitemap, `robots.txt`, static assets, `brief.branding` and
  `brief.seo`, and write "not read" for the rest. Never invent a placeholder colour: a red or gold accent that is nobody's brand ships as
  the client's brand.
- A typeface we cannot ship (a licensed face) is mapped to its closest free neighbour by the preview code; say so in `pitch["confirm"]`.

## 3 — The record, then three themes

Write `brands/<slug>.md` from `brands/_template.md`. The promise verbatim from `brief.promise`; if empty, the
home page's own headline, marked unconfirmed. Client-stated constraints from `ground`, `likes`, `dislikes` and
`notes`; these outrank house defaults. Entity facts from their site (legal name from the footer or the
privacy page, canonical URL, logo, phone, every address, the social profiles their footer links). SEO
baseline from `brief.seo` when present, otherwise the words "not pulled". Directions produced after this step.
Leave "Chosen direction" empty; the client has not chosen. Only what the site, the brief or `brief.seo`
states. Nothing invented.

Apply the selection rules in `themes/catalogue.md`. The house set for a light-ground category (office
technology, most B2B services) is Showcase (safe), Clean (stretch), Press (wildcard), Showcase first. When
`brief.ground` is `dark`, the light five are out: pick from Flagship, Void, Signal, Converter, never two with
the same ground and typeface class, and Converter only with a written reason. When the brief names sites they
like or hate, let that move the stretch and the wildcard. **Type:** unless `brand.fonts` is set, Showcase and Clean use Open Sans and
Press uses Playfair Display (the house type; Bricolage Grotesque is not used in client builds). Write into `brands/<slug>.build.json`:

- `themes`: three, safe first.
- `roles`: one line each, written for this client, not the starter's generic text.
- `recommend`: our pick. A pitch that refuses to have an opinion reads as hedging (`process/decisions.md`),
  so recommend unless `brief.notes` says not to, and give the reasons in `pitch["pick_reasons"]` tied to
  what they said.
- `base_url` stays what `cc.py scaffold` set (Client Command's address), `out` stays `../out-<slug>`.

## 4 — The content file

Fill `brands/<slug>.content.py`. The CAPITALISED constants are the facts; the builders below them already
turn each service, industry, city and post into a page. Rules, all of them from `process/INTAKE.md` and `process/directions-standard.md`:

- **Every fact sourced**: their site, the brief, `brief.seo`. Service lines in their words and their order
  (`brief.service_lines` first, then their navigation). Locations with the address and phone on their site,
  with lon and lat for the map (`REGION` per `preview_sections.REGIONS`; add one there if the state is
  missing). Partners from the logos they show. Testimonials only the ones they publish. Team only the people
  they name. Years, counts and ratings only where the site or the brief states them.
- **Claims.** No absolutes, no response-time or availability promises, no savings percentages, unless the client's own page says it; then
  list it in `content["claims_ok"] = [{"text": "<the sentence>", "source": "<their url>"}]`. Say "average", never "guarantee". One proof client or stat
  band per page; do not repeat the same quote or number across pages. Partner wording only as the partner states it.
- **Never**: em dashes, exclamation marks, adjectives stacked three deep, copy that could belong to any company in the category.
- Blurbs through `brief()`, descriptions through `desc()`; every page a `title` with the brand after a pipe
  and a `description` of 120 to 160 characters (never cut mid-word); `schema.short_name`, `title_city`, `cities`, `area_served`,
  `meta_tail`, `local` set.
- **The home page kit.** At least **10 sections over at least 8 module types**, and a `compose` list per direction, copied from the Nexus and Image 2000
  examples: `hero`, `partners`, `wheel`, `flow`, `seal`, `beforeafter`, `proof`, `stats`, `casestudy`, `map`, `timeline`, `checklist`, `services`,
  `testimonials`, `faq`, `contact` are all available from sourced text alone. Use `model3d`, `fleet`, `hotspots`, `video` or `story3d` only when the
  asset exists. Every service page: a `flow` process chart, a `beforeafter`, an FAQ and related pages. Leave a module out rather than invent its data.
- **Page set.** Cover every service line, industry and office their site names, in their order, and merge near-duplicates (the gate compares
  pages). Every navigation item has a page. No placeholder blog.
- **Images.** Download the client's own images (hero, team, premises, products, awards badge) from their site into `../out-<slug>/assets/` with
  `curl -sL -A "Mozilla/5.0"`, keeping sensible names, and reference them as `assets/<name>`. **Use their own photograph as the hero when
  their site has one.** Where they have no usable image, copy a stand-in from `library/<vertical>/scenes` or `devices` into `assets/` and say
  "generated" in its alt text, per `library/README.md`. Write `assets/hero-og.jpg` at 1200 wide. No Higgsfield here; nothing is generated in this run.
- **The pitch block**: `heard` from the brief (promise, likes, dislikes, notes, in their words), `found` from
  the audit and `brief.seo.findings`, `pick_reasons` tied to what they said, `pick_change` (the one thing we
  would change), `alternatives` (the other two, one line each), `plan` (the six phases, 90 days), `confirm`
  (everything you could not source: this list is where honesty lives; also the open items in section 7 of `process/directions-standard.md`),
  `qbs_contact` from `brief.qbs_contact`, `prepared_for` the client.
- **Search package.** When `brief.seo` is present, write `brands/<slug>.seo.json` from it in the shape of
  `brands/_starter.seo.json` (measured, hero tiles, findings with severity, compare, moves, blog, entity,
  today, competitors, local, plan, measure), numbers only from `brief.seo`, "not pulled" where it has none.
  When `brief.seo` is absent, `rm brands/<slug>.seo.json`: the hub renders without the search sections, and
  a starter full of angle-bracket placeholders must never reach a client.

Run `python3 brands/<slug>.content.py` and fix until it writes the JSON without a traceback.

## 5 — Render, gate, look

`python3 scripts/build.py <slug> --shots`. It writes every page in the three directions, the hub, the design
system, removes stale pages, scores the first direction and screenshots the hub. Then **run the gate**:

```
python3 scripts/directions_qa.py <slug>
```

It prints PASS, WARN or FAIL per check and writes `qa.json`, `claims-register.csv` and the pictures (`qa/contact-sheet.jpg`, `qa/index.html`: each
direction's home page at 1280 and 390) into the output folder. **Fix every FAIL in the content
file (not the output) and rerun.** The checks: starter text, em dashes, unsourced claims, near-duplicate pages, the home page kit, brand
accent, logo, the rendered heading face, corner shape, headline and lead contrast against the photograph behind them, sideways scroll on a phone,
and the measurable half of the beauty bar (`process/directions-standard.md`, rule 8): no rejected face, no text under 12px, heading order,
at most three saturated colour families, the contrast floor, no axe violation.
Then **look**: Read `../out-<slug>/qa/contact-sheet.jpg`, then `screenshots/hub-1280.jpg` and `hub-390.jpg` (the Read tool shows images), and check
what a machine cannot, against the beauty bar:

- The colours, face and corners look like the client's own site (open it in your head against the fetched CSS), not like a Quantum template.
- The logo shows, is sharp and is theirs; the navigation names their services; card grids balance (2, 3, 4, 5, 6, 8).
- Section buttons and headings are centred where the section is centred and no heading wraps one word onto a line.
- The first-direction score `build.py` prints is 80 or more. Under 80: titles carry the city, descriptions
  are 120 to 160 characters, one h1 per page, the description is not the title. Fix, rerun.

Two honest passes and a FAIL remains: stop, leave it as it is, and write what is wrong into `pitch["confirm"]` so a person sees it on the hub.
Do not spend the run polishing one page.

## 6 — Hand back

Do not `git commit`, `git push`, or touch anything outside `brands/<slug>.*`, `scripts/preview_sections.py` (only to add a map region) and `../out-<slug>/`. The
workflow uploads the output into Client Command and commits the brand files. Finish with a short summary on
stdout: the three themes and the recommendation, the brand you measured (accent, faces, corners, logo source), the page count, the home's section
count, the score, the gate's PASS/WARN/FAIL counts with every FAIL and WARN named, and the `confirm` list.
