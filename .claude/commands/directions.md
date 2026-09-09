---
description: Headless. From a Client Command brief to three complete directions. Runs inside the Website directions workflow; nobody is watching.
argument-hint: "<slug>"
allowed-tools: Read, Write, Edit, MultiEdit, Glob, Grep, Bash, WebFetch
---

Build the three directions for `$ARGUMENTS` from the brief Client Command sent. **Nobody is watching.**
There is no one to ask, so decide by the written rules, and put every fact you could not source under
`pitch["confirm"]` instead of guessing. **Nothing here touches HubSpot, Vercel, BrandCommand or Client
Command directly**; the workflow around you does the upload and the commit.

This is `/preview` with the interview replaced by a form. Same output, same rules, same gate.

## 0 — What is already on disk

| Path | What it is |
|---|---|
| `brands/<slug>.brief.json` | The form a teammate filled in Client Command: `client`, `short`, `domain`, `cities`, `city_tag`, `vertical`, `ground` (light, dark or none), `accent`, `promise` (the one line a visitor must believe, verbatim), `service_lines`, `likes`, `dislikes`, `notes`, `portal` (what Client Command knows about the client), `qbs_contact` (who started it), `base_url` (where the site will be served), and `seo` when Client Command has run its SEO/AEO analysis on this domain (the same shape as `brands/<slug>.seo.json` needs, more or less). |
| `brands/<slug>.audit.json`, `brands/<slug>.urls.txt`, `/tmp/<slug>-html/` | Every sitemap URL fetched and scored by `newclient.py`. Empty when the site has no sitemap: then fetch the home page and every page its navigation links to with `curl -sL` into `/tmp/<slug>-html/` yourself before writing a word. |
| `brands/<slug>.content.py`, `.seo.json`, `.build.json`, `.types.json` | Scaffolded from the starters by `newclient.py`. If this client was built before, these are the real files: update them, do not start over. |
| `../out-<slug>/` | The output folder, with `assets/` inside. |

Report where you are with `python3 scripts/cc.py progress $CC_BUILD_ID <step> "<one line>"` at the start of
each numbered section below; the steps are `read`, `brief`, `themes`, `content`, `render`, `gate`. The
teammate sees that line in Client Command.

## 1 — Read, in this order

1. `process/INTAKE.md` (what the content file needs, section by section), `design/guardrails.md` (always and
   never, the card-grid rule), `themes/catalogue.md` (the selection rules).
2. `verticals/<vertical>.md` when `brief.vertical` names one that exists (`office-technology` does). It knows
   the category's page set, module kit and colour problem.
3. `brands/_template.md` (the brief), `brands/kelly-office-solutions.content.py` (the pattern: facts as
   constants, a builder per page type, `build()` writes the JSON), `brands/image-2000.content.py` (a shorter
   second example), `library/README.md` (stand-in imagery you may use, and how to label it).
4. Then the client: the brief, the audit, the fetched HTML of the home, about, services, locations and contact
   pages, and their live CSS for the accent when the brief gives none (`curl -sL` the stylesheet the home page
   links; the accent is the colour on the primary button).

## 2 — The brief, the record

Write `brands/<slug>.md` from `brands/_template.md`. The promise verbatim from `brief.promise`; if empty, the
home page's own headline, marked unconfirmed. Client-stated constraints from `ground`, `likes`, `dislikes` and
`notes`; these outrank house defaults. Entity facts from their site (legal name from the footer or the
privacy page, canonical URL, logo, phone, every address, the social profiles their footer links). SEO
baseline from `brief.seo` when present, otherwise the words "not pulled". Directions produced after step 3.
Leave "Chosen direction" empty; the client has not chosen. Only what the site, the brief or `brief.seo`
states. Nothing invented.

## 3 — Three themes

Apply the selection rules in `themes/catalogue.md`. The house set for a light-ground category (office
technology, most B2B services) is Showcase (safe), Clean (stretch), Press (wildcard), Showcase first. When
`brief.ground` is `dark`, the light five are out: pick from Flagship, Void, Signal, Converter, never two with
the same ground and typeface class, and Converter only with a written reason. When the brief names sites they
like or hate, let that move the stretch and the wildcard. Write into `brands/<slug>.build.json`:

- `themes`: three, safe first.
- `roles`: one line each, written for this client, not the starter's generic text.
- `recommend`: our pick. A pitch that refuses to have an opinion reads as hedging (`process/decisions.md`),
  so recommend unless `brief.notes` says not to, and give the reasons in `pitch["pick_reasons"]` tied to
  what they said.
- `base_url` stays what `cc.py scaffold` set (Client Command's address), `out` stays `../out-<slug>`.

## 4 — The content file

Fill `brands/<slug>.content.py`. The CAPITALISED constants are the facts; the builders below them already
turn each service, industry, city and post into a page. Rules, all of them from `process/INTAKE.md`:

- **Every fact sourced**: their site, the brief, `brief.seo`. Service lines in their words and their order
  (`brief.service_lines` first, then their navigation). Locations with the address and phone on their site,
  with lon and lat for the map (`REGION` per `preview_sections.REGIONS`; add one there if the state is
  missing). Partners from the logos they show. Testimonials only the ones they publish. Team only the people
  they name. Years, counts and ratings only where the site or the brief states them.
- **Never**: em dashes, exclamation marks, response-time or pricing promises they have not published,
  adjectives stacked three deep, copy that could belong to any company in the category.
- Blurbs through `brief()`, descriptions through `desc()`; every page a `title` with the brand after a pipe
  and a `description` of 140 to 160 characters; `schema.short_name`, `title_city`, `cities`, `area_served`,
  `meta_tail`, `local` set.
- **Images.** Download the client's own images (logo, hero, team, premises, products) from their site into
  `../out-<slug>/assets/` with `curl -sL`, keeping sensible names, and reference them as `assets/<name>`. Look
  at the logo: white type means `chrome = "dark"` with a `chrome_bg`. Where they have no usable image, copy a
  stand-in from `library/<vertical>/scenes` or `devices` into `assets/` and say "generated" in its alt text,
  per `library/README.md`. Write `assets/hero-og.jpg` at 1200 wide (a copy of the hero is fine). No
  Higgsfield here; nothing is generated in this run.
- **The pitch block**: `heard` from the brief (promise, likes, dislikes, notes, in their words), `found` from
  the audit and `brief.seo.findings`, `pick_reasons` tied to what they said, `pick_change` (the one thing we
  would change), `alternatives` (the other two, one line each), `plan` (the six phases, 90 days), `confirm`
  (everything you could not source: this list is where honesty lives), `qbs_contact` from
  `brief.qbs_contact`, `prepared_for` the client.
- **Search package.** When `brief.seo` is present, write `brands/<slug>.seo.json` from it in the shape of
  `brands/_starter.seo.json` (measured, hero tiles, findings with severity, compare, moves, blog, entity,
  today, competitors, local, plan, measure), numbers only from `brief.seo`, "not pulled" where it has none.
  When `brief.seo` is absent, `rm brands/<slug>.seo.json`: the hub renders without the search sections, and
  a starter full of angle-bracket placeholders must never reach a client.

Run `python3 brands/<slug>.content.py` and fix until it writes the JSON without a traceback.

## 5 — Render, then look

`python3 scripts/build.py <slug> --shots`. It writes every page in the three directions, the hub, the design
system, removes stale pages, scores the first direction and screenshots the hub. Then **look**: Read
`../out-<slug>/screenshots/hub-1280.jpg` and `hub-390.jpg` (the Read tool shows images). Check, and fix the
content rather than the output:

- No starter text survives: `CLIENT NAME`, `START HEADING`, `BODY`, `SUBMIT LABEL`, `000-000-0000`, `YEAR`,
  `"..."`. `grep -rn` the output folder for each.
- No em dashes (build.py prints every hit), no exclamation marks.
- The logo shows in the header; the navigation names their services; card grids balance (2, 3, 4, 5, 6, 8).
- Every direction has an `index.html` and every page the content names.
- The first-direction score `build.py` prints is 80 or more. Under 80: titles carry the city, descriptions
  are 140 to 160 characters, one h1 per page, the description is not the title. Fix, rerun.

Two honest passes and it is still wrong: stop, leave it as it is, and write what is wrong into
`pitch["confirm"]` so a person sees it on the hub. Do not spend the run polishing one page.

## 6 — Hand back

Do not `git commit`, `git push`, or touch anything outside `brands/<slug>.*` and `../out-<slug>/`. The
workflow uploads the output into Client Command and commits the brand files. Finish with a short summary on
stdout: the three themes and the recommendation, the page count, the score, and the `confirm` list.
