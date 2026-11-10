# The /directions standard

What a headless three-directions build must be before a person sends the link. Written 9 Nov 2026 after the first two
automated builds (IMS Technology Services, Digital Monitoring Products) looked off and weak next to Kelly, Revolution
and Van Ausdall & Farrar. Everything here is either a defect a person fixed by hand on those three sites
(`process/qa-findings.md`, the three sign-off sheets, the plan trackers) or a defect the first two automated builds
shipped. The command that applies it is `.claude/commands/directions.md`; the gate that enforces it is
`scripts/directions_qa.py`.

**Done means** `python3 scripts/directions_qa.py <slug>` exits 0: no FAIL. A WARN is read by a person before the link goes.

---

## 1. Brand fidelity: measure, never guess

The preview has to look like the client's company before anything else about it can be judged.

| Token | Where it comes from | In the content file |
|---|---|---|
| Accent | `brief.branding.colors.primary` (Client Command measures it at dispatch from the live site's primary button). Else the colour on their primary button in the live CSS. Never the logo's brightest pixel, never a made-up placeholder | `brand.accent` |
| Secondary | `brief.branding.colors.secondary` | `brand.bg_alt` (a 6 to 10 percent tint of it) and `brand.navy` if it is dark |
| Ground | the live site's page background and header. White type in the logo means a dark header | `brand.chrome = "dark"`, `brand.chrome_bg` |
| Type | `brief.branding.fonts`. See rule 2 | `brand.fonts = {"heading": ..., "body": ...}` |
| Corners | `brief.branding.radius` for cards and inputs, `brief.branding.button_radius` for buttons (they differ: DMP's buttons are pills, its cards square) | `brand.radius` and `brand.button_radius` (px). Square stays square, a pill stays a pill |
| Logo | their own file, downloaded from their site: the SVG if there is one, else the largest PNG. A wordmark typed in CSS is the last resort | `brand.logo` |

If the site cannot be read (a JavaScript bot challenge, as on dmp.com): do not circumvent it. Take the values from
`brief.branding` (Client Command reads them with its own browser service), from the sitemap, from `robots.txt`, from static
assets (a logo SVG under `/static/` is usually fetchable with a normal user agent), and put every value you could not
measure under `pitch["confirm"]`. A red or gold placeholder accent that is nobody's brand is worse than a gap on the list.

## 2. Type

- **House type: Open Sans headings and Inter body on Showcase and Clean; Playfair Display on Press.** Kelly and Van Ausdall
  both shipped this (Van Ausdall set `type_from: {"showcase": "clean"}`; Kelly's Showcase renders Open Sans 800). Showcase's own
  face, Bricolage Grotesque at weight 800 with negative tracking, reads as whimsical on a B2B site and is no longer
  used in a client build. `scripts/preview.py` applies the house type whenever the brand sets no type of its own.
- **No route back to a rejected face.** `REJECTED_FACES` in `scripts/preview.py` lists the theme display faces
  (Bricolage Grotesque, Fraunces, Instrument Serif) and the script and rounded display faces a brief could name. The
  house mapping is the base even when a brand sets `type_from` or `fonts`; a rejected face named by a theme, a borrowed
  direction or `brand.fonts` is replaced by the house face; its Google import and every mention of it are taken out of
  the page. The hub card and the design-system page name and load the face the pages render.
- When the client's own site uses a face on Google Fonts (Oswald, Poppins, Jost, Roboto, Montserrat, Lato, Open Sans...)
  set `brand.fonts` and Showcase and Clean use it. A licensed face we cannot ship (Gotham, Proxima Nova, Helvetica Neue)
  is swapped for its closest free neighbour by `FONT_NEIGHBOURS` in `scripts/preview.py`, and the swap goes in `pitch["confirm"]`.
- The gate reads the computed font of the first headline in a real browser, then every face the browser actually drew in the
  headings, buttons, numerals and body of each home page. A theme default leaking through is a FAIL.

## 3. The hero is readable, on any photograph

White type needs a dark ground. The layered hero's scrim is `--hero-bg`: the dark header colour when there is one,
otherwise a deep tint of the accent, otherwise near-black. It used to be built from the page's white, so a light-header
brand put a white headline over a white scrim on a bright photo (IMS). The gate samples the pixels behind the headline
and the lead line with the text hidden and fails under 3:1 and 4.5:1.

Use the client's own photograph for the hero whenever their site has one (IMS publishes a team photo and an award badge;
the build used a generated stage). Stand-in imagery from `library/` is labelled "generated" in its alt text and is never
used for people or premises.

## 4. The home page kit: build it like Van Ausdall, not like a brochure

The Van Ausdall home runs 24 sections over 20 module types; Kelly's 25 over 22. The first DMP home had 6 sections over 6.
The difference is most of what reads as weak.

- **Home: at least 10 sections over at least 8 module types**, with a `compose` list per direction (see
  `brands/nexus-network-technologies.content.py` and `brands/image-2000.content.py`, which use 28 and 34 types, and
  copy their builders `_flow`, `_ba`, `_seal`, `_proof`, ...). A compose id that matches no section stops the build.
- **Always available (text and sourced facts only):** `hero`, `partners`, `wheel` (the service lines), `flow` (the client's
  process, from their site or the vertical's), `seal` (certifications and awards they publish), `beforeafter`, `proof` (one
  sourced number), `stats`, `cards`, `casestudy`, `tabs`, `map` (offices with lon and lat), `timeline` (dates they publish),
  `checklist`, `services`, `testimonials` (only ones they publish), `faq`, `contact`.
- **Only when the assets exist:** `model3d`, `fleet`, `hotspots`, `video`, `story3d`, `hero-layered` with a photo that
  carries the story. Do not render an empty slot.
- **Every service page** carries a process chart (`flow`), a before and after, an FAQ and related pages.
- A module with no sourced data behind it is left out. Thin is better than invented.

## 5. Claims: nothing is stronger than the client's own page

The same six corrections came back on Revolution, Kelly and Van Ausdall, roughly 45 times, and all three made a claims
register a launch blocker.

- No absolutes ("every", "always", "never", "guarantee", "unconditional", "world-class"), no response-time or
  availability promises ("same day", "within one business day", "24/7"), no savings percentages, unless the client's own
  page says it. Say "average", never "guarantee". The gate FAILs a sentence that carries one and is not listed in
  `content["claims_ok"] = [{"text": "...", "source": "https://..."}]`.
- Every figure, year and count lands in `claims-register.csv` (the gate writes it) for the client to confirm.
- One proof client or one stat band per page, rotated. The same logo, quote or number does not repeat across pages.
- Partner and certification wording only as the partner states it. No revenue share, no commercial terms, no internal deal
  values on a public page. Customer names only where they are published.
- A customer's quote is theirs: the gate does not scan testimonial sections.

## 6. Page set

- Mirror the client's service lines, industries and offices, in their words and their order, but **merge near-duplicates**
  (the gate warns above 50 percent overlap and fails above 80). Sixty-three mirrored service pages on Van Ausdall overlapped
  by 92 percent and had to be collapsed by hand.
- Every item in the navigation has a page. No tile without a destination. No placeholder blog.
- Service and about pages are at least 200 words; the SEO score also expects 300.
- Page withdrawals the client names go in `pitch["confirm"]`: ask what to retire.

## 7. Forms, legal and launch (carried forward, never invented)

`/directions` builds a static preview and touches nothing else. These are the items that cost the most on the three
shipped sites, so each belongs on `pitch["confirm"]` when the brief does not answer it: the lead product line; the existing
forms to reuse (one per intent, and the contact form is not the assessment form); who receives each form; privacy, terms and
cookie text for counsel; logo, manufacturer-image and customer-name permissions; the glossary (the standard call to action
label); DNS, registrar and Search Console access and the prior agency; the HubSpot tier and page cap.

## 8. The beauty bar: what good looks like, and what the gate measures

The first three options a prospect sees have to look designed for them without anyone touching them by hand. The house
finish (`scripts/preview_polish.py`) puts every module on one scale; the gate takes pictures and measures what can be
measured. A person still looks, at `qa/index.html` in the build output.

| | What good looks like | What fails the build |
|---|---|---|
| **Type** | House type only (rule 2). One scale: h1 40 to 66px sized by how long the headline is, h2 30 to 44px, h3 20 to 22px, lead 18 to 20px, body 16px, card copy 15.5px, labels 13px uppercase. Headings carry weight (700 on Clean, 800 on Showcase, 500 serif on Press), so a section heading never reads lighter than its own body. Numerals are lining and tabular | A rejected display, script or rounded face drawn anywhere or named in the page (`face-leak`). Text under 12px at 1280 or 390 (`type-floor`); under 13px is a WARN. More than one h1, or a heading level skipped (`heading-order`) |
| **Spacing** | One section rhythm (72 to 112px, 64px on a phone). One heading stack: label, 16px, heading, 16px, lead, 48px, content. Cards and form panels 28 to 32px inside, 24px apart. Grids balance, with no orphan card and no orphan word in a heading | Sideways scroll at 390 (`overflow`) |
| **Hero** | The first screen says what the company does, in its own words, over its own photograph where it has one. White type sits on the brand's deep ground (rule 3). A long headline steps down a size instead of running to five lines | Headline under 3:1 or lead under 4.5:1 against the pixels behind it (`legible`) |
| **Density** | One idea per section, one proof per page. Ten or more sections on the home page, none of them empty. A module with no data is left out; a module with thin data takes its thin form (names with no logo files sit in a still row, a brand with no phone gets no Call button) | Under 10 sections or 8 module types on the home page (`home-richness`) |
| **Colour** | The client's accent, its deep colour and neutrals. The alternate band is a tint of their deep colour, never a stock cream; cards on it are white; hairlines and shadows carry the same deep colour | More than three saturated colour families used as paint (`accent-count`); three is a WARN. Any text under 4.5:1, or 3:1 when large (`contrast-floor`). Any other axe violation on the home page (`axe`) |
| **Imagery** | The client's own photographs first, one subject per image, no picture on more than six pages. Stand-ins are labelled generated and never show people or premises. Photographs sit in a frame with the direction's corner, never stretched | Missing logo (`logo`). Reuse and all-stand-in builds are WARNs (`image-reuse`, `own-imagery`) |
| **Motion** | One thing moves at a time. Reveals travel 12px over half a second, once. Cards lift 3px on hover; nothing tilts, pulses, orbits or floats for decoration. The partner marquee takes 80 seconds a lap and stops on hover. Everything is still under reduced motion | Not measured: look at the page |
| **States** | Every link, button, tab, field and card shows a hover and a keyboard focus ring that reads on its ground, light or dark. Form fields have a visible edge (3:1) and a labelled focus | Covered by `axe` and `contrast-floor` where it can be |

**The pictures.** `scripts/directions_qa.py` writes `qa/contact-sheet.jpg` (the home page of each direction, whole, at 1280
and 390, on one sheet), the six pictures on their own, and `qa/index.html`, which sets the pictures beside every PASS,
WARN and FAIL. They upload with the site, so the person who opens the build in Client Command sees them at
`<site address>/qa/`. The pictures are taken with motion reduced, so every scroll reveal is in.

## 9. Open decision

`schema_blocks()` in `scripts/preview.py` emits Organization and the headquarters LocalBusiness on every page, while
`design/guardrails.md` says Organization belongs on the home page or one about page. The entity-graph score (11 Sep 2026)
rewards connected references, so changing the code changes the score. Decide which rule wins before changing either.
