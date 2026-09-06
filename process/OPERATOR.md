# Operator checklist — building a client site in HubSpot

**Hand this one file to whoever is building. It is self-contained.** Read the rest of the repo only
when a step says to.

Portal `20682069`. Auth via PAT in `$QBS_HUBSPOT_TOKEN` — never write it to a file, never paste it
into a commit.

---

## Read this first: five traps that will bite you

These are verified defects in the theme set, not theory. Each one has shipped or nearly shipped.

1. **Never edit one of the nine themes.** Quantum Flagship, Void, Signal, Converter, Clean, Press,
   Paper, Journal, Showcase are the product line, shared across every client. Editing one changes
   every other client's site. **Always clone first.**
2. **Every theme emits QBS's `Organization` schema.** A clone left alone tells Google the client's
   site *is* Quantum Business Solutions. Void's block is worse — it also carries a real founder name
   and email address.
3. **The header and footer hardcode QBS's logo, nav, social links and copyright.** The re-skin
   script does **not** fix this. A client sees it in five seconds.
4. **`colors.*` in `fields.json` does nothing.** `theme.colors` is referenced in zero files. Colour
   lives in `css/quantum.css`, in the `NATIVE DIRECTION` block. Editing the colour fields in the
   theme editor changes nothing on the page.
5. **Five of nine themes fail WCAG AA on button text.** Clean, Paper, Journal, Showcase at 3.9:1 and
   Press at 3.52:1, against a 4.5:1 minimum. If you clone a light theme and don't re-skin the
   accent, you ship an accessibility failure.

`appearance.mode` is nearly vestigial — it does **not** control colour (the native block overrides
both modes), but it does drive `.only-dark` / `.only-light` logo visibility. Set it to match the
ground or the client's logo shows the wrong variant.

---

## 0 · Orient

- [ ] `python3 scripts/reskin.py audit` — sweeps all nine, shows real grounds, contrast, module and
      template counts, and which themes leak QBS. Run it once so the numbers are in front of you.
- [ ] Confirm the portal is `20682069` before anything else. The script does this and refuses to
      proceed otherwise.
- [ ] Read `brands/<slug>.md`. **If it doesn't exist, stop and run `/mockups <company>` first.**
      Building without a brief is how the model reaches for its defaults.

## 1 · Before you touch HubSpot

- [ ] **Entity facts** in the brief: legal name, canonical URL, logo URL, `sameAs` (LinkedIn,
      Crunchbase). **Without these the clone ships our identity.** Non-negotiable.
- [ ] **Tier purchased** — Launch, Growth or Transform. Decides re-skin depth and page count.
- [ ] **Ground** — light or dark, taken from the brief, not from taste. If the client said light,
      the four dark themes are out. Full stop.
- [ ] **The accent hex**, measured off their live site (`firecrawl_scrape`, `formats:["branding"]`),
      not eyeballed from a logo.
- [ ] **SEO baseline written down** — organic traffic, keywords, traffic value, top pages, Site
      Health. `process/seo-baseline.md` has the four Semrush pulls. **No baseline, no way to prove
      the work worked**, and the optimisation window is what Transform charges for.
- [ ] **URL inventory of every page earning traffic today.** Each one needs a 301 to a new home.
      On QBS's own domain, articles are 82% of organic traffic — losing them in a redesign costs
      more than the build is worth.
- [ ] **Client's HubSpot subscription** confirmed. Blog, forms and meetings all need it. Find out at
      kickoff, not in week ten.
- [ ] **Multi-location?** No location/address/hours module exists and there's no `LocalBusiness`
      schema. **Out of tier** — scope it as custom before promising location pages.

## 2 · Clone and re-skin

Never by hand in Design Manager. Use the script — it does the clone, the colour block,
`appearance.mode` and the client's schema in one pass, so the schema can't be forgotten.

- [ ] Propose (read-only, writes nothing):

```bash
python3 scripts/reskin.py plan \
    --theme "Quantum <Theme>" --client "<Company>" \
    --accent "#RRGGBB" --ground <light|dark> \
    --org-name "<Legal name>" --org-url "https://<domain>" \
    --org-logo "<logo url>" --org-sameas "<linkedin>" "<crunchbase>"
```

- [ ] **Read the whole output.** It prints the exact change table, four contrast ratios, and what it
      will not fix.
- [ ] **Show that table to whoever approves portal writes and wait for an explicit yes.** That table
      *is* the propose-then-confirm proposal. No exceptions.
- [ ] All four contrast gates PASS. If any fails, fix with `--set` before applying — the script
      refuses to apply a failing re-skin, and `--force` needs a stated reason.
- [ ] Apply:

```bash
    … --apply --approved-by "<name>"
```

- [ ] Target name is `<Company> — <Theme>`. The script refuses to write to any of the nine.
- [ ] **Never fix contrast with `opacity`.** Use a real colour.

## 3 · The four things the script does not fix

**Nothing goes in front of a client until these are done.**

- [ ] **`templates/partials/header.html`** — QBS logo, nav links, Quantum Academy link. These are
      `global_partial`s (portal-scoped singletons), so this is not a clone-and-edit. Either
      field-drive them at source or build client-specific partials and repoint the clone's
      `base.html` blocks. `process/reskin.md` has both options.
- [ ] **`templates/partials/footer.html`** — same, plus the copyright line and social URLs.
- [ ] **Fonts** load via a CSS `@import` in `css/quantum.css` — one extra serial hop, invisible to
      the preload scanner. Move to `<link>` + `preconnect` in `base.html`.
- [ ] **Check `<head>` for anything else naming QBS.** Read it, don't assume.

## 4 · Pages and content

- [ ] Create pages from the clone's templates. **19 files, 16 page templates** — not 21.
- [ ] 12 of the 16 are a `dnd_area`. `blog-listing`, `password-prompt`, `system-404` and
      `system-search` are not, which is correct for system pages.
- [ ] Section order per page from the module inventory in `themes/catalogue.md`. **The 57 modules
      are the wireframe vocabulary** — pick from the inventory rather than inventing layouts.
- [ ] Every page passes the **three P's** above the fold: what problem is this for, am I the person,
      what's being promised? If the hero could belong to any company in the category, it isn't
      done — and the fix is usually a **missing persuasion module** (`pain-bridge`, `is-this-you`,
      `cost-of-inaction`, `two-futures`, `why-now`), not better adjectives.
- [ ] **Card grids balance — no orphan rows.** Six cards on one row and two on the next reads as a
      mistake, because it is one: nobody chose it, a `grid-template-columns` did. **Change the column
      count, not the client's content.** 12 is clean at every width; 2·4·8 are clean at 4/2/1;
      3·6·9 are clean at 3. Never 4 cards at 3 columns, or 5/9 at 4 columns.
      **And check every breakpoint** — 3 or 9 cards must go 3 → 1 and skip 2 columns; 4 or 8 must go
      4 → 2 → 1 and skip 3. Full table in `design/guardrails.md`; the gate measures rendered rows and
      fails on an orphan.
- [ ] **Real content. No Lorem, no `example.com`, no "Your Company".** The gate checks for these.
- [ ] Exactly one `<h1>` per page, answering the search intent from the baseline.
- [ ] **Featured image set on every page** — otherwise `og:image` is absent and every LinkedIn or
      Slack share renders a bare text link. On QBS's own site this is missing on 31 of 41 pages.
- [ ] Alt text on every content image; `alt=""` on purely decorative art.
- [ ] Images: `loading="lazy"` below the fold, hero eager with `fetchpriority="high"`. Never both on
      one image.
- [ ] `width`/`height` on every image **plus `height:auto`** — an inline CSS `height:100%` overrides
      the attribute-derived aspect ratio and reserves nothing.

## 5 · Structured data

- [ ] `Organization` names **the client**. Read the rendered `<head>` and confirm by eye.
- [ ] Derive any new JSON-LD **from the module's own fields**, with `|escapejson` on every value.
      Copy the `quantum-faq.module` pattern. **Never hand-write JSON-LD into a rich-text block** —
      it drifts on the first client edit.
- [ ] Don't mark up self-published testimonials with `AggregateRating` or `Review`. Ineligible, and
      risks a manual action.
- [ ] Growth tier sold a "full schema set"? **`BlogPosting`, `Article`, `Service`, `Offer`,
      `BreadcrumbList`, `Event` and `Person` are all absent from the themes.** The source fix is
      unapproved. Flag it rather than hand-writing it.
- [ ] Don't promise rich results that don't exist: FAQ retired May 2026, HowTo 2023. Of what's left,
      only `Event` unreservedly earns one; `BreadcrumbList` is desktop-only, `Offer` needs a
      single-product page, `Article` is an enhancement, `Service` earns nothing visible.

## 6 · Conversion paths

- [ ] **Two per page, minimum.** A hard offer (book a call, demo) *and* a soft offer (gated asset,
      calculator, grader, newsletter). Without the soft one, everybody not ready to buy today leaves
      unidentifiable — which is most visitors.
- [ ] `quantum-sticky-cta` on every long page. A CTA the visitor scrolled past no longer exists.
- [ ] `quantum-meetings` **embedded inline**, not linked. Every click between intent and calendar
      loses people.
- [ ] Shortest form that qualifies. `quantum-multistep-form` when more is genuinely needed.
- [ ] A real **thank-you page** (`templates/thank-you.html`) — the conversion event, the asset
      delivery, and the next offer.
- [ ] Gate the *result* of a calculator, not the tool.

## 6b · Mobile — review it before desktop

Most traffic is a phone, and most of what fails on a phone survives a desktop review untouched. The
gate measures all of this at 390px; these are floors, not aspirations.

- [ ] **Tap targets ≥ 24×24 CSS px** (WCAG 2.5.8 AA). Social icons are the usual offender — on QBS's
      own site they are 20×25 and fail. Aim for 44×44, which is Apple's guidance.
- [ ] **≥ 8px between adjacent targets.**
- [ ] **Body text ≥ 13px.** 12px is a desktop habit that shipped to a phone.
- [ ] **Form inputs ≥ 16px.** Below that **iOS zooms the page on focus** and yanks the layout out
      from under whoever is filling the form. The most common mobile form defect there is.
- [ ] **Pinch-zoom not blocked.** No `user-scalable=no`, no `maximum-scale=1` — a WCAG 1.4.4
      failure, and the one mobile mistake a user cannot work around.
- [ ] **Sticky chrome ≤ 25% of the viewport.** A sticky header plus the sticky CTA this checklist
      asks for can eat a third of a phone screen. Reconcile them per build.
- [ ] **Nav works on touch.** A hover-only mega-menu does not exist on a phone.
- [ ] **`srcset` or `<picture>` on every content image.** A 2400px hero on a 390px screen wastes the
      visitor's bandwidth and our LCP.
- [ ] **No horizontal scroll** at 390px. The gate names the element causing it.
- [ ] **Then load it on an actual phone and scroll the whole thing.** The harness measures; it
      cannot tell you it feels wrong in the hand.

## 7 · The gate — nothing ships without it

- [ ] ```bash
      node scripts/verify.mjs <preview-url> --expect-org "<Client legal name>"
      ```
      **Exit code 1 means it failed.** It checks a11y (axe-core) at 390/768/1440, CLS, canonical,
      `og:image`, headings, lazy-loading, image dimensions, JSON-LD validity *and whose name is in
      it*, **card-grid balance at every width**, **the mobile floors above**, placeholder text,
      conversion paths and broken links.
- [ ] **Open the screenshots in `verify-out/` and actually look**, including at phone width. The
      harness catches what's measurable; it cannot tell you the design is wrong. This is the
      most-skipped step in the whole process and the highest-value one.
- [ ] `/impeccable critique` and `/impeccable audit`.
- [ ] Re-read `design/guardrails.md` against the build, line by line.
- [ ] **PageSpeed Insights on mobile**, not desktop. Desktop hides exactly these problems.
- [ ] **Submit a form and book a meeting yourself, end to end.** Submission lands in the CRM, the
      thank-you page fires, the asset actually arrives. A form nobody tested is a form that loses
      every lead silently.
- [ ] **Share one URL into Slack or LinkedIn** and look at the preview card. Ten seconds; catches
      `og:image`.
- [ ] Every changed URL has a **301, not a 302.** A 302 tells Google to keep the old URL canonical,
      so the new one may never replace it.

## 8 · Launch

- [ ] Baseline captured **before** the switch.
- [ ] 301s live and tested on the top-traffic pages individually.
- [ ] Google Analytics connected, and connected to the Semrush project.
- [ ] Check for a stray `noindex` or `nosnippet` — `nosnippet` also blocks AI Overviews entirely.
- [ ] Canonicals present. Note HubSpot deliberately omits them on blog listing and paginated pages —
      that's correct, not a bug.
- [ ] Verify the site in **Google Search Console**. The Generative AI performance report is the only
      first-party AI-visibility data that exists.

## 9 · Record it, and hand over

- [ ] One `website_projects` row per direction, named `<Company> — <Theme>`, with the re-skinned
      values in `colors`/`fonts` and the preview URL in the description.
- [ ] Choice and **why, in the client's words**, into `brands/<slug>.md`. The rejected directions are
      worth as much as the winner.
- [ ] **Show the client how to edit their own `dnd_area`s.** "Editable by your team" is a real
      deliverable — make it true and it cuts your support load.
- [ ] Anything that generalises past this client → `design/guardrails.md`. A prompt that worked →
      `design/prompts.md`. A theme defect → fix it **at source** so all nine benefit.

---

## Never do these

- Edit one of the nine themes in place.
- Write to the portal without showing the change table and getting an explicit yes.
- Ship a clone whose `<head>`, header or footer still says Quantum Business Solutions.
- Hand-write JSON-LD into a rich-text block.
- Fix a contrast failure with `opacity`.
- Leave one card alone on a row beneath three or more.
- Change a URL that has traffic without a 301.
- Fork a theme's *structure* for one client. If the structure is wrong, fix it at source.
- Ship anything nobody has looked at, at phone width.

## If you only have an hour

The four that cause real damage: **entity facts in the schema**, **the header/footer leak**,
**301s on trafficked URLs**, and **`verify.mjs` passing**. Everything else is quality; those four
are correctness.
