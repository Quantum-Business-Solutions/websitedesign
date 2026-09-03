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
| `rel="canonical"` | ✅ Present | `{{ standard_header_includes }}` |
| `og:title`, `og:description` | ✅ Present | Page meta |
| `twitter:card` | ✅ Present | `standard_header_includes` |
| `robots.txt` | ✅ Sane defaults — previews and cache-busters disallowed | Portal setting |
| `sitemap.xml` | ✅ Auto-generated, with image entries | Platform |
| SSL, CDN, no plugin surface | ✅ | Platform |

That's most of "technical SEO" handled, and it's a genuine reason the HubSpot CMS pitch on the
website-services page holds up. **Time spent re-implementing these is wasted** — spend it on the
gaps below, which the platform does *not* cover.

## What the themes already get right

Worth knowing so nobody "fixes" it:

- **Exactly one `<h1>` per page.** Verified. Heading hierarchy is sound.
- **Alt text on every content image**, and `alt=""` on the decorative background SVG — which is
  correct, not an omission. Decorative images should be invisible to screen readers.
- **`display=swap` on the font request**, so text renders immediately in a fallback rather than
  hanging invisible.

---

## Traffic gaps — measured

### 1. Fonts load through a CSS `@import`. This is an LCP problem.

`css/quantum.css` line 2:

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:...&display=swap');
```

An `@import` inside a stylesheet creates a **serial** request chain: HTML → `quantum.css` →
Google Fonts CSS → the font files themselves. The browser can't even discover the font request until
`quantum.css` has downloaded and parsed. Four round trips before the first glyph.

Same fonts via `<link>` in `base.html` cost two, because the browser sees the request in the initial
HTML parse:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=...&display=swap">
```

Self-hosting the woff2 files removes the third-party hop entirely and is the better answer for the
nine themes, since the typeface is the theme's identity and never changes per client.

This is a **theme-level fix at source** — nine `base.html` and nine `quantum.css` edits, and every
past and future client gets faster. Core Web Vitals tuning is sold on the website-services page;
this is the single biggest available win.

### 2. No `preconnect` or `preload` anywhere. Zero, across the theme and rendered page.

Follows from the above. The hero image in particular should be `fetchpriority="high"` and never lazy
— it's almost always the LCP element.

### 3. Every image loads eagerly. `loading="lazy"` count: 0 of 15.

Fifteen images competing for bandwidth with the LCP element, including theme previews far below the
fold. Rule: **hero eager with `fetchpriority="high"`, everything below the fold `loading="lazy"`.**

### 4. No `width`/`height` on images — CLS risk.

Images are sized in CSS (`style="width:100%;height:100%;object-fit:cover"`) with no intrinsic
dimensions, so the browser can't reserve space before the image arrives. Content shifts as each one
loads, and Cumulative Layout Shift is a ranking signal. Add `width` and `height` attributes;
`object-fit` still governs the visual result.

### 5. `og:image` is missing — social shares render blank.

`og:title` and `twitter:card` are injected, but `og:image` count is **0**. The page's
`featuredImage` field is empty. Every LinkedIn or Slack share of that URL shows a bare text link.

This is a **per-page content requirement**, not a theme bug: set a featured image on every published
page. Cheapest traffic fix on this list, and it belongs in the Phase 06 checklist.

---

## Lead gaps — measured

### The money page has no on-page conversion path.

On `/website-services`: `hs-form` count **0**, meetings embed count **0**. Every CTA — "Request a
Demo", "Book a call", "Grade your Website for Free" — is a **link to another page.**

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
| Full schema set (Article, Service, Offer, Breadcrumb) | — | ✅ | ✅ |
| Blog set up with `BlogPosting` schema | — | ✅ | ✅ |
| Gated asset / calculator as the soft offer | — | ✅ | ✅ |
| Conversion architecture — offers mapped to funnel stage | — | — | ✅ |
| Analytics + grader baseline captured at launch | — | — | ✅ |
| Post-launch optimisation window | — | — | ✅ |

The first eight rows are the **launch gate**. A site that misses any of them isn't finished, whatever
was paid — they're cheap, and each one is a hole traffic or leads fall through.

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

---

## The theme-level fixes worth making at source

Per-client patching of any of these is waste. Fixing them once in the nine themes fixes every past
and future build — the same argument as `process/structured-data.md`, and worth batching with it into
one approved change:

1. **Fonts via `<link>` + `preconnect` in `base.html`, or self-hosted woff2.** Remove the CSS
   `@import`. Biggest Core Web Vitals win available.
2. **`loading="lazy"` by default on image modules**, with an "above the fold" toggle that switches to
   eager + `fetchpriority="high"`.
3. **`width`/`height` passed through** on every image module.
4. **The `seo` field group and fail-safe `Organization` block** from `process/structured-data.md`.

All four are writes to portal `20682069` and need approval first, per the
`qbs-hubspot-private-app` propose-then-confirm protocol. Nothing has been executed.
