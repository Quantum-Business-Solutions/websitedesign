# Launch standards: traffic and leads

The baseline every site we build has to meet. Not a wish list — the specific, checkable things that
decide whether a beautiful site actually earns traffic and captures leads, or just sits there.

Everything below was **measured** against the live QBS site (`/website-services`, Quantum Void) and
the theme source, so the gaps named are real rather than generic advice. If our own flagship page
misses something, a client build will too.

---

## What HubSpot already gives you — don't rebuild it

Verified present in the rendered `<head>` without any theme code:

| Signal | Status | Source |
|---|---|---|
| `rel="canonical"` | ✅ Present **by default** | Portal setting — verify it |
| `og:title`, `og:description` | ✅ Present | Page meta |
| `twitter:card` | ✅ Present | `standard_header_includes` |
| `robots.txt` | ✅ Sane defaults — previews and cache-busters disallowed | Portal setting |
| `sitemap.xml` | ✅ Auto-generated, with image entries | Platform |
| SSL, CDN, no plugin surface | ✅ | Platform |

Two caveats on canonicals, both from HubSpot's own docs. It's a **portal setting** (Settings →
Content → Pages → SEO & Crawlers), not unconditional template behaviour — if someone has selected
"don't add canonical URLs," you set them by hand. And **blog listing and paginated pages have no
canonical by default, deliberately**, so search engines can find subsequent pages. That answers the
open question in `process/seo-baseline.md` about nine live pages lacking one: check whether they're
listing pages before raising it. Per-page overrides also beat the portal setting, so a canonical
hand-set by a previous agency can silently win.

That aside, most of "technical SEO" is handled, and it's a genuine reason the HubSpot CMS pitch on
the website-services page holds up. **Time spent re-implementing these is wasted** — spend it on the
gaps below, which the platform does *not* cover.

## What the themes already get right

Worth knowing so nobody "fixes" it:

- **Exactly one `<h1>` per page.** Verified. Heading hierarchy is sound.
- **Alt text on every content image**, and `alt=""` on the decorative background SVG — which is
  correct, not an omission. Decorative images should be invisible to screen readers.
- **`display=swap` on the font request**, so text renders immediately in a fallback rather than
  hanging invisible. **With a caveat:** `swap` is also the main *cause* of font-related CLS — the
  fallback gets replaced once the webfont lands. Keep `swap` for display and heading type; for body
  text either match fallback metrics (`size-adjust`, `ascent-override`) or use
  `font-display: optional`.

---

## Traffic gaps — measured

### 1. Fonts load through a CSS `@import`. This is an LCP problem.

`css/quantum.css` line 2:

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:...&display=swap');
```

An `@import` inside a stylesheet creates a **serial** request chain: HTML -> `quantum.css` -> Google
Fonts CSS -> the font files. The browser can't discover the font request until `quantum.css` has
downloaded and parsed.

Via `<link>` in `base.html` that's three serial steps instead of four - and, more importantly, the
request is **discovered by the preload scanner in the initial HTML parse** rather than after a
stylesheet round trip. web.dev is explicit that the `<link>` element includes a preconnect resource
hint and thus likely results in faster stylesheet delivery than `@import`.

The snippet:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=...&display=swap">
```

Self-hosting the woff2 files removes the third-party hop and is *usually* better on a CDN — but
web.dev cautions that the performance difference "is less clear cut," and the Web Almanac has found
third-party fonts sometimes rendering faster. It's conditional on replicating the subsetting Google
Fonts does automatically. **Measure before committing nine themes.**

This is a **theme-level fix at source** — nine `base.html` and nine `quantum.css` edits, and every
past and future client gets faster.

> **Not the biggest win, though.** An earlier version called this "the single biggest available win,"
> which our own data contradicts: Semrush scores this site's performance **97/100**. Two bigger ones:
> **INP** (below), and the page parked at position 11 in `process/seo-baseline.md`.

### 2. `preconnect` is missing from eight of the nine themes; `preload` from all nine.

**Correction:** an earlier version said "zero, across the theme and rendered page." Void's
`base.html` has **both** preconnects, and the live page loads fonts by `<link>` from its own
`headHtml` — so the fix prescribed above was already in place on the very page it was measured
against. The `@import` is still there in all nine stylesheets, and the other eight themes have no
preconnect at all.

The hero image should be `fetchpriority="high"` and never lazy — it's almost always the LCP element.
Note `loading="lazy"` and `fetchpriority="high"` together is pointless: the image stays deferred.

### 3. Every image loads eagerly. `loading="lazy"` count: 0 of 15.

Fifteen images competing for bandwidth with the LCP element, including theme previews far below the
fold. Rule: **hero eager with `fetchpriority="high"`, everything below the fold `loading="lazy"`.**

**Don't make lazy the unconditional default.** web.dev's data shows pages using lazy loading have
*worse* median p75 LCP (3,546ms vs 2,922ms), because the fold gets misjudged. The above-the-fold
toggle in the theme fix below is what makes a lazy default safe — ship them together or not at all.

### 4. No `width`/`height` on images — CLS risk.

Images are sized in CSS (`style="width:100%;height:100%;object-fit:cover"`) with no intrinsic
dimensions, so the browser can't reserve space before the image arrives. Content shifts as each one
loads, and CLS is a ranking signal.

**The obvious fix doesn't work here.** Browsers reserve space by deriving an `aspect-ratio` from the
`width`/`height` attributes — and an explicit CSS `height:100%` overrides that, so adding the
attributes while keeping the inline height reserves nothing. The fix is the attributes **plus**
`height:auto`, or an `aspect-ratio` on the container.

Measured caveat: 14 of 14 *content* images lack both attributes. The one image that has them is a
ZoomInfo tracking pixel, not theme output.

### 5. INP is unmeasured, and it's the likely real weak spot.

Core Web Vitals are **LCP, INP and CLS** — INP replaced FID as stable in 2024, threshold 200ms. This
file covered only LCP and CLS.

On HubSpot, `{{ standard_header_includes }}` injects **jQuery**, layout CSS, analytics and tracking
code. jQuery in the head is a classic INP and render-blocking problem — and it can be disabled or
moved to the footer in **Settings → Content → Pages → Templates**. That's a **portal setting, not a
theme fork**, which makes it cheaper than all nine CSS edits and possibly worth more.

Measure it before assuming. Then measure again after.

### 6. `og:image` is missing — social shares render blank.

**And it's 31 pages, not one.** From the pages API, 31 of 41 site pages have an empty
`featuredImage` — including `/about-us`, `/contact-us`, `/pricing`, `/technology` and every playbook
page.

`og:title` and `twitter:card` are injected, but `og:image` count is **0**. The page's
`featuredImage` field is empty. Every LinkedIn or Slack share of that URL shows a bare text link.
Also absent site-wide: `og:type`, `twitter:image`.

This is a **per-page content requirement**, not a theme bug: set a featured image on every published
page. Cheapest traffic fix on this list, and it belongs in the Phase 06 checklist.

---

## Lead gaps — measured

### The money page has no on-page conversion path.

On `/website-services`: `hs-form` count **0**, `<form>` count **0**, meetings embed count **0**.
There are **10** links to `meetings.hubspot.com` across four CTAs — "Book Now", "Request a Demo",
"Book a call", "talk to a human" — but they are **off-page links, not embeds.** So there is a hard
conversion path; there is no *on-page* capture of any kind.

That's a defensible design for a high-intent buyer. But it means:

- A visitor who is interested but **not ready to book a call** has no way to convert. No email
  capture, no gated asset, no soft offer. They leave and are never identifiable again.
- Every conversion pays a click-through tax, and each hop loses visitors.

And the modules to fix it **already exist and are unused here** — `quantum-leadgen`,
`quantum-multistep-form`, `quantum-gated-download`, `quantum-meetings`, `quantum-sticky-cta`,
`quantum-roi-calculator`, `quantum-roi-estimator`.

### The standard: two conversion paths per page, minimum

1. **A hard offer** — book a call, request a demo. For the ready buyer.
2. **A soft offer** — gated asset, ROI calculator, grader, newsletter. For the 95% who aren't ready
   today but will be. This is what builds a remarketable list instead of a bounce.

Plus:

- **`quantum-sticky-cta` on every long page.** A CTA the visitor scrolled past is a CTA that no
  longer exists.
- **`quantum-meetings` embedded inline**, not linked. Every click between intent and calendar loses
  people.
- **Shortest form that qualifies.** Email plus one qualifying field beats seven fields.
  `quantum-multistep-form` when more is genuinely needed — progressive disclosure converts better
  than a long single page.
- **A real thank-you page**, not an inline confirmation. `templates/thank-you.html` exists in every
  theme kit. It's the conversion event, the place to deliver the asset, and the place to make the
  next offer.

### Interest that never becomes a lead

`quantum-roi-calculator` and `quantum-roi-estimator` are the highest-intent modules in the library —
someone entering their own numbers is qualifying themselves. Gate the *result*, not the tool: let
them use it, capture the email to send the breakdown.

---

## The baseline, by tier

Maps onto the packages in `process/website-design-process.md`. Nothing here is optional at any tier —
the tier changes depth, not whether it's done.

| | Launch $4,950 | Growth $9,950 | Transform $14,950 |
|---|---|---|---|
| Canonical, OG, sitemap, robots | Platform ✅ | ✅ | ✅ |
| One `<h1>`, alt text, heading order | ✅ | ✅ | ✅ |
| `og:image` (featured image) on every page | ✅ | ✅ | ✅ |
| Lazy below fold, `fetchpriority` on hero | ✅ | ✅ | ✅ |
| `width`/`height` on every image | ✅ | ✅ | ✅ |
| Correct `Organization` schema | ✅ | ✅ | ✅ |
| Two conversion paths per page | ✅ | ✅ | ✅ |
| Thank-you page + tracked conversion event | ✅ | ✅ | ✅ |
| Full schema set (Article, Service, Offer, Breadcrumb) — **blocked, see note** | — | ✅ | ✅ |
| Blog set up with `BlogPosting` schema | — | ✅ | ✅ |
| Gated asset / calculator as the soft offer | — | ✅ | ✅ |
| Conversion architecture — offers mapped to funnel stage | — | — | ✅ |
| Analytics + grader baseline captured at launch | — | — | ✅ |
| Post-launch optimisation window | — | — | ✅ |

The first eight rows are the **launch gate**. A site that misses any of them isn't finished, whatever
was paid — they're cheap, and each one is a hole traffic or leads fall through.

> **The Growth schema row cannot currently be delivered.** `BlogPosting`, `Article`, `Service`,
> `Offer`, `BreadcrumbList`, `Event` and `Person` are all absent from the themes, the source fix is
> unapproved, and hand-writing JSON-LD is banned by `design/guardrails.md`. Either approve the fix
> before the next Growth sale, or say the line item is blocked. And when it does ship, sell it as a
> machine-readable entity graph — of those four types, `Service` earns nothing visible, `Offer` needs
> a single-product page, `BreadcrumbList` is desktop-only and `Article` is an enhancement. See
> `process/structured-data.md`.

---

## Where this lands in the process

| Phase | What happens |
|---|---|
| 01 Information Gathering | Capture entity facts (`process/structured-data.md`) and what the soft offer will be. If the client has no gateable asset, that's a scope item — surface it now, not in week ten |
| 02 Planning | Page types decide schema types. Decide the two conversion paths per template |
| 04 Content Writing | One `<h1>` per page answering the search intent. First sentence answers the question — that's what AEO extracts |
| 05 Design & Build | Lazy-loading, image dimensions, `fetchpriority`, featured images, forms wired, thank-you pages live |
| 06 Test, Review & Launch | The gate below. Capture the analytics baseline **before** launch — no baseline, no way to prove the optimisation window worked |
| Post-launch | Growth-driven design. Monthly review against the launch baseline |

### The launch gate

Add to `process/checklist.md`:

- **PageSpeed Insights** on home, one interior, one blog post — mobile scores, not desktop. Desktop
  scores hide exactly the problems above.
- **Rich Results Test** + `validator.schema.org`, and confirm the `Organization` block names the
  **client** — see `process/structured-data.md`.
- **Submit one form and book one meeting yourself.** End to end: submission lands in the CRM, the
  thank-you page fires, the asset actually arrives. A form nobody tested is a form that doesn't work.
- **Share one URL into Slack or LinkedIn** and look at the preview card. That's the `og:image` check,
  and it takes ten seconds.
- **Everything at phone width.** Most of this list fails on mobile first.

Run the harness first; it does all of the above except the human look:

```bash
node scripts/verify.mjs <url> --expect-org "<Client legal name>"
```

Exit code 1 means the gate failed. On QBS's own `/website-services` it currently returns
**9 FAIL / 4 WARN / 14 PASS** — including two accessibility failures nobody had spotted: the Ask
Quantum chat dialog has no accessible name, and body-copy links are distinguishable by colour alone
(WCAG 1.4.1). CLS, though, measures **0.016** — comfortably inside budget, so the missing image
dimensions haven't cost anything on that page yet. Fix the a11y failures before the CSS work.

**A caveat on running it here:** where the sandbox blocks the browser's own egress, the harness
routes requests through curl. Screenshots and axe-core stay fully valid; network *timing* does not,
so LCP reports as unavailable rather than as a fabricated number. Use PageSpeed Insights for real
timing.

---

## The theme-level fixes worth making at source

Per-client patching of any of these is waste. Fixing them once in the nine themes fixes every past
and future build — the same argument as `process/structured-data.md`, and worth batching with it into
one approved change:

1. **Fix the light-theme contrast failure first.** All five light themes ship `--cta-fg` on
   `--q-gold` at 3.5–3.9:1 against a 4.5:1 requirement — every primary button on every light-theme
   site. Found by `scripts/reskin.py audit`. An accessibility defect, not a preference.
2. **Try the jQuery portal setting before any CSS work.** Settings → Content → Pages → Templates.
   Free, and it targets INP.
3. **Field-drive the header and footer partials**, or provide client-specific ones. They hardcode
   QBS's logo, nav, social links and copyright — visible to the client immediately, and worse than
   the schema leak. They're `global_partial`s, so this needs care.
4. **Fonts via `<link>` + `preconnect` in `base.html`.** Remove the CSS `@import`. Consider
   self-hosting, but measure first.
2. **`loading="lazy"` by default on image modules**, with an "above the fold" toggle that switches to
   eager + `fetchpriority="high"`.
3. **`width`/`height` passed through** on every image module.
4. **The `seo` field group and fail-safe `Organization` block** from `process/structured-data.md`.

All four are writes to portal `20682069` and need approval first, per the
`qbs-hubspot-private-app` propose-then-confirm protocol. Nothing has been executed.
