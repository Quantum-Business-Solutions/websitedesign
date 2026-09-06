# Structured data: SEO and AEO

Yes — and it's the part of the build that most needs systematising, because right now it's one
module doing it well and fifty-six doing nothing.

Schema markup is sold: "Schema and AEO stack" is a line item on **Growth** and **Transform**, and
the website-services page promises "technical SEO, on-page optimization, schema markup, Core Web
Vitals tuning, and pillar page strategy — built in from day one, not bolted on after." This file is
how that gets delivered the same way every time.

---

## ⚠️ Fix this first: every theme ships QBS's identity

`templates/layouts/base.html` in **all nine themes** hardcodes this into `<head>`:

```json
{"@context":"https://schema.org","@type":"Organization",
 "name":"Quantum Business Solutions",
 "url":"https://www.thequantumleap.business",
 "description":"Revenue operations infrastructure for growth-minded companies. HubSpot Diamond and ZoomInfo Solutions Partner.",
 "sameAs":[]}
```

Verified on Flagship, Void, Signal, Converter, Clean, Press, Paper, Journal and Showcase — all nine,
identical.

Eight of the nine are byte-identical. **Void's is different and worse** — a richer block carrying
`@id`, `logo`, a `founder` Person with a real name and LinkedIn URL, and a `contactPoint` with a
real email address. A client site cloned from Void publishes those as its own. Void also emits
`WebSite` + `SearchAction` and a `BreadcrumbList` that the other eight lack, so two rows of the
"missing" table below don't apply to it.

**So every client site built on a Quantum theme declares itself, on every page, to be Quantum
Business Solutions.** Wrong entity name, wrong canonical URL, wrong description, and QBS's partner
credentials asserted on a stranger's domain.

**This is worse than having no schema at all** — but be precise about why, because the obvious
reason is wrong. Google does **not** apply a ranking penalty for bad structured data: unsupported or
misleading markup is usually just ignored, and at worst earns a page-level manual action that costs
rich-result eligibility while leaving rank untouched. The real argument is threefold, and it holds:

1. It is a documented guidelines violation — "don't use structured data to deceive or mislead users.
   Don't impersonate any person or organization, or misrepresent your ownership, affiliation, or
   primary purpose."
2. It forfeits the client's own `Organization` and knowledge-panel eligibility.
3. It actively corrupts entity disambiguation, which is the one thing `Organization` markup exists
   to do.

No markup, by contrast, is explicitly safe: "structured data that's not being used does not cause
problems for Search."

**And it is only a bug on a client's domain.** On QBS's own site the block is *accurate*, which is
why the Semrush audit reports it as 9 valid and markups 100/100. Same code, opposite verdicts
depending on whose domain it's on — so don't escalate it as a QBS-site emergency.

Three reasons it has survived:

1. **Schema is not in the re-skin surface.** `fields.json` has exactly two groups — `appearance.mode`
   and `colors` (five hexes) — and the colour fields are wired to nothing. So the re-skin in
   `process/reskin.md` *cannot* fix it, and there's no field in the UI to make anyone notice.
2. **It's in the layout, not a module.** It never appears in a `dnd_area`, so it's invisible to
   anyone editing the page in HubSpot — client or QBS.
3. **It affects every tier.** Schema is sold from Growth up, but this ships on Launch too. The
   cheapest package currently gets QBS's identity rather than nothing.

Confirm before assuming a live client site is affected — check the rendered `<head>` of any
delivered site. The fix is proposed at the end of this file and needs approval before it touches the
portal.

---

## What exists today

One module of fifty-seven emits structured data, and it does it correctly.

`quantum-faq.module` builds `FAQPage` from its own fields:

```jinja
<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage",
"mainEntity":[{% for it in module.items %}{"@type":"Question","name":"{{ it.q|escapejson }}",
"acceptedAnswer":{"@type":"Answer","text":"{{ it.a|escapejson }}"}}{% if not loop.last %},{% endif %}{% endfor %}]}</script>
```

**This is the house pattern.** Three things make it right, and every new schema block should copy
all three:

1. **Derived from the module's own fields**, so the markup can never contradict the visible copy.
   Hand-written JSON-LD in a separate rich-text block drifts the first time someone edits the page,
   and Google lists "the structured data is not representative of the main content of the page, or
   is potentially misleading" as a common reason a rich result simply doesn't show.
   QBS's own `/website-services` page does exactly the wrong thing: its `FAQPage` and `Service`
   blocks are hand-pasted into per-page `headHtml` rather than coming from `quantum-faq`, so no
   client build inherits them and they drift on the first edit.
2. **`|escapejson` on every interpolated value.** Without it a client typing a double quote,
   backslash or raw newline produces invalid JSON-LD and the whole block is silently discarded.
   (An apostrophe alone won't break JSON — but escape everything anyway.)
3. **It lives in the module that renders the content**, so it appears if and only if that section is
   on the page. A client who deletes the FAQ section deletes its markup too. That's correct
   behaviour and you get it for free.

---

## What's missing

Verified by grepping all 57 modules and every template in the Press kit for `ld+json` and
`schema.org`. Ordered by value.

| Type | Where it belongs | Status | Why it matters |
|---|---|---|---|
| **Organization** | `layouts/base.html` | **Wrong** — hardcoded to QBS | The entity anchor. Everything else hangs off it |
| **FAQPage** | `quantum-faq.module` | ✅ Done | Retired May 2026. Keep for clean Q&A; never sell it |
| **BlogPosting** | `templates/blog-post.html` | Missing | Author, dates, headline. The most-cited page type |
| **Article** | `templates/case-study.html` | Missing | Case studies are the proof pages; unattributed |
| **Service** | `templates/interior.html` | Missing | What the business actually sells |
| **Offer** / **Product** | `templates/pricing.html`, `quantum-pricing*` | Missing | Prices are already on the page as text |
| **BreadcrumbList** | `layouts/base.html` | Missing | Cheap; disambiguates deep pages |
| **LocalBusiness** | *no module exists* | **Blocked** | Multi-location clients — see below |
| **Event** | `templates/event.html`, `quantum-event-hero` | Missing | The one type with strong rich results still intact |
| **Person** | `quantum-team.module` | Missing | Feeds author attribution and entity graphs |
| **WebSite** | `layouts/base.html` | Missing | Low value now — see the honesty note below |

### Be honest about what schema still buys

Overselling this is easy and it damages credibility when a client checks:

- **FAQ rich results are fully retired, not merely restricted.** Restricted August 2023 to
  government and health sites, then **deprecated entirely on 7 May 2026** — documentation removed
  from the search gallery, no longer testable in the Rich Results Test. Keeping `FAQPage` markup is
  harmless; **selling** it is not, and calling it "our strongest AEO signal" is unsupported (see the
  AEO section).
  **Do not migrate to `QAPage`.** Google lists "an FAQ page written by the site itself with no way
  for users to submit alternative answers" as an *invalid use case*. `QAPage` needs
  user-submittable answers.
- **HowTo rich results were retired** in two stages — mobile in August 2023, desktop 13 September
  2023. Don't add `HowTo` expecting a snippet.
- **`WebSite` still earns something.** The sitelinks searchbox retired **21 November 2024** (not
  2023), but Google's own announcement notes that `WebSite` structured data also drives **site
  names** in results, which is a live visible feature on mobile and desktop. Include it — **on the
  home page only.** Google: "the `WebSite` structured data must be on the home page of the site."
- **Self-serving reviews are ineligible.** Testimonials about you, published on your own site under
  `Organization` or `LocalBusiness`, are not eligible for review rich results. Leave
  `quantum-reviews` unmarked. The realistic downside is a page-level structured-data manual action,
  which costs rich-result eligibility and **does not affect ranking** — still a reason not to do it.
  **Scope matters:** first-party *customer reviews of a specific product* on a `Product` page are
  explicitly supported. Don't forbid legitimate markup on an e-commerce client.

What genuinely earns a **visible rich result**: **Event** only, unreservedly. The rest are weaker
than they sound:

- **`BreadcrumbList` is desktop-only** since January 2025 — worth adding, but don't call it a rich
  result without saying "on desktop," especially when our own gate reads mobile scores.
- **`Product`/`Offer` needs a single-product page.** Google: "product rich results only support
  pages that focus on a single product." A three-tier services pricing page is a category page and
  earns nothing.
- **`Article` is an enhancement**, not a distinct rich result — better title, image and date
  handling. It has **no required properties**.
- **`Service` is not in the search gallery at all.** Useful as entity description; earns nothing
  visible.
- **`Organization`** drives logo and knowledge-panel signals.

**So "Full schema set (Article, Service, Offer, Breadcrumb)" is close to unsellable as a
visible-outcome promise.** Sell it as a machine-readable entity and content graph — which is real
and worth having — never as rich results.

### Multi-location is a product gap, not a documentation gap

There is **no location, address, hours, map or branch module** in the 57, and no `locations.html`
template. For a multi-location client — a practice group, a dealer network, a franchise — local pack
visibility *is* the traffic, and we currently cannot emit `LocalBusiness`, `openingHours`,
`areaServed` or per-branch `geo` at all. The proposed `seo` field group below is single-entity only.

**Treat multi-location as out of tier until a `quantum-location` module exists.** Scope it as a
custom build, or build the module: one page per location, `LocalBusiness` (or the specific subtype)
derived from the module's own fields per the `quantum-faq` pattern, plus NAP consistency and Google
Business Profile in the Phase 01 checklist. Selling location pages we cannot mark up is selling
local SEO we cannot deliver.

### What actually moves AEO — corrected against Google's own guidance

Google published *Optimizing your website for generative AI features on Google Search* in May 2026,
including a section titled **"Mythbusting generative AI search: what you don't need to do."** An
earlier version of this file ranked four factors, and three of them appear in that section on the
wrong side. The corrected picture:

1. **Markup that agrees with the visible text.** This is the **only** structured-data item Google
   names as helping: "making sure your structured data matches the visible text on the page." It was
   ranked fourth here; it should be first.
2. **Content people find unique and genuinely useful.** Google: this "will likely influence your
   website's presence in generative AI search in the long run **more than any of the other
   suggestions in this guide**." Its example of what *not* to write is a commodity listicle.
3. **Off-site brand presence.** The strongest *measured* correlate, and the thing this repo was not
   looking at. Ahrefs, 75,000 brands: YouTube mentions ~0.74, branded web mentions 0.66–0.71 —
   against backlinks at only 0.28–0.34. Correlation isn't causation, and Google explicitly names
   "seeking inauthentic mentions" as a myth, so this means real digital PR, podcasts, third-party
   coverage, video and community presence.
4. **Attribution.** `BlogPosting` with a real `author` (a `Person`, not "Admin"), `datePublished`
   and `dateModified`. Defensible on E-E-A-T grounds, but no primary source ties author markup to AI
   citation — so don't oversell it.

**What Google says you do *not* need:** structured data ("isn't required for generative AI search,
and there's no special schema.org markup you need to add"), "chunking" content into small pieces,
rewriting content specifically for AI, or `llms.txt` and similar files ("Google Search itself doesn't
use them" — and server logs show AI systems don't even request them). Name `llms.txt` as a non-task
so nobody sells it.

**Don't cite the Semrush schema-prevalence study as support.** It reports that 25% of ChatGPT-cited
pages carry `Organization` schema with no uncited control group — which means most AI-cited pages
carry none at all. It undercuts the claim it looks like it supports.

**Terminology:** Google's position is that optimising for generative AI search *is* SEO, and it
points its "evaluating third-party SEO advice" page directly at AEO/GEO vendors. We sell an AEO
Health Check and a score grader; the same guide warns to "be wary of third-party tools that promise
ranking success or claim to use 'internal' Google metrics. No third-party tool has access to our
internal ranking or AI systems." Our own rule — never quote a score without reading what's underneath
it — applies to the score we *sell*, not just the ones we buy.

### Missing from the process entirely, and all of it cheap

- **Google Search Console.** The largest single omission. The **Generative AI performance report**
  (global rollout August 2026) is the only first-party AI-visibility data that exists. Also the
  Search-generative-AI inclusion control — default is included, so this is verify-don't-break.
- **`nosnippet` / `max-snippet` auditing.** `nosnippet` "will also prevent the content from being
  used as a direct input for AI Overviews and AI Mode." One stray directive zeroes AI visibility.
  Belongs in the launch gate.
- **AI crawler user agents — and we would have got these wrong.** The *retrieval* bots are
  `OAI-SearchBot` (`GPTBot` is training-only), `Claude-SearchBot` and `Claude-User` (`ClaudeBot` is
  training), and `PerplexityBot`. `Google-Extended` governs Gemini training, **not** AI Overviews —
  Googlebot's robots.txt controls those.
- **`LocalBusiness` + Google Business Profile** for local clients, named in Google's AI docs as a
  lever. Blocked here — see the multi-location note below.
- **Content refresh cadence.** We mark up `dateModified` and have no refresh process, while our own
  Semrush data says the highest-ROI work available is improving one existing page.

---

## Where this lands in the process

Structured data is **Phase 05 Design & Build**, not a phase-06 afterthought — which is exactly what
"built in from day one, not bolted on after" commits us to.

| Step | Action |
|---|---|
| Phase 01 Information Gathering | Capture the client's real entity facts into `brands/<slug>.md`: legal name, canonical URL, logo URL, LinkedIn, Crunchbase, and location if they serve locally |
| Phase 02 Planning | Decide which page types are in scope. Page types decide schema types |
| Phase 05 Design & Build | Set the Organization values on the clone. Verify every schema-bearing module on every template |
| Phase 06 Test, Review & Launch | **Validate.** No build ships unvalidated — see below |
| Post-launch | Re-validate after content edits. A client editing an FAQ regenerates its markup; a client pasting hand-written JSON-LD breaks it |

### The validation gate

Add to `process/checklist.md` item 7. Two checks, both free, neither optional:

1. **Google Rich Results Test** on the home page, one blog post, one case study, one interior page,
   and the pricing page — [search.google.com/test/rich-results](https://search.google.com/test/rich-results)
2. **Schema.org validator** for spec correctness Google's tool doesn't flag —
   [validator.schema.org](https://validator.schema.org)

Then read the rendered `<head>` and confirm the `Organization` block names **the client**. Until the
theme fix below ships, this check catches the bug on its own.

---

## Proposed fix — needs approval before it touches the portal

Writes to portal `20682069` follow propose-then-confirm per the `qbs-hubspot-private-app` skill.
Nothing here has been executed. Three changes, smallest first:

**1. Add an `seo` field group to `fields.json` on all nine themes.**

| Field | Type | Default |
|---|---|---|
| `seo.org_name` | text | *(empty — falls back to `site_settings.company_name`)* |
| `seo.org_url` | text | *(empty — falls back to `request.domain`)* |
| `seo.org_description` | text | *(empty)* |
| `seo.org_logo` | image | *(empty)* |
| `seo.org_sameas` | repeated text | *(empty)* |

**2. Make `base.html` render `Organization` from those fields, and omit the block entirely when
`org_name` is empty.** Absent markup is safe; wrong markup is not. This turns the bug into a
fail-safe.

Then narrow it: Google recommends `Organization` **on the home page or a single about page** — "you
don't need to include it on every page of your site." Site-wide is why the audit counts nine valid
blocks. `WebSite` is home-page-only by requirement. `BreadcrumbList` stays site-wide.

**3. Add schema to five templates and three modules**, following the `quantum-faq` pattern —
`BlogPosting` on `blog-post.html`, `Article` on `case-study.html`, `Service` on `interior.html`,
`Offer` on `pricing.html`, `BreadcrumbList` in `base.html`, `Event` on `quantum-event-hero`,
`Person` on `quantum-team`, `Offer` on `quantum-pricing` and `quantum-pricing-toggle`.

Note the last one: `quantum-pricing-matrix` is one of Void's four QBS-only extras and never ships to
a client, so marking it up buys clients nothing. The shared conversion modules are `pricing` and
`pricing-toggle`.

Change 2 is the one that matters — it stops nine themes asserting a false identity. Changes 1 and 3
are the product improvement, and because they're fixes **at source** rather than per-client forks,
every past and future client benefits from one edit. That's the whole argument for not forking
themes, made concrete.

Sequence it as: nine `fields.json` patches → nine `base.html` patches → validate on one non-production
theme → then the module and template work.
