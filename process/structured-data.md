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

**So every client site built on a Quantum theme declares itself, on every page, to be Quantum
Business Solutions.** Wrong entity name, wrong canonical URL, wrong description, and QBS's partner
credentials asserted on a stranger's domain.

This is worse than having no schema at all. No markup means search engines infer the entity from the
page. Wrong markup means we've told them something false, in the one format they're built to trust.

Three reasons it has survived:

1. **Schema is not in the re-skin surface.** `fields.json` has exactly two groups — `appearance.mode`
   and `colors` (five hexes). Nothing about identity. So the six-value re-skin in
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
   Hand-written JSON-LD in a separate rich-text block drifts the first time someone edits the page —
   and drift between markup and visible content is exactly what Google penalises.
2. **`|escapejson` on every interpolated value.** Without it a client typing an apostrophe or a
   quote in an answer produces invalid JSON-LD, and the whole block is silently discarded.
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
| **FAQPage** | `quantum-faq.module` | ✅ Done | The strongest AEO signal we ship |
| **BlogPosting** | `templates/blog-post.html` | Missing | Author, dates, headline. The most-cited page type |
| **Article** | `templates/case-study.html` | Missing | Case studies are the proof pages; unattributed |
| **Service** | `templates/interior.html` | Missing | What the business actually sells |
| **Offer** / **Product** | `templates/pricing.html`, `quantum-pricing*` | Missing | Prices are already on the page as text |
| **BreadcrumbList** | `layouts/base.html` | Missing | Cheap; disambiguates deep pages |
| **Event** | `templates/event.html`, `quantum-event-hero` | Missing | The one type with strong rich results still intact |
| **Person** | `quantum-team.module` | Missing | Feeds author attribution and entity graphs |
| **WebSite** | `layouts/base.html` | Missing | Low value now — see the honesty note below |

### Be honest about what schema still buys

Overselling this is easy and it damages credibility when a client checks:

- **FAQ rich results are effectively gone.** Google restricted them in August 2023 to authoritative
  government and health sites. We keep `FAQPage` markup anyway — **for AEO, not SEO.** It's clean,
  extractable question-answer structure, which is precisely what an LLM wants when deciding what to
  quote. Say it that way; don't promise FAQ accordions in the SERP.
- **HowTo rich results were retired** for the same reason. Don't add `HowTo` expecting a snippet.
- **`WebSite` + `SearchAction`** was for the sitelinks searchbox, which Google retired in November
  2023. Include `WebSite` for entity clarity if you like, but it earns nothing visible.
- **Review and AggregateRating are restricted.** Self-serving reviews — testimonials collected and
  published on your own site — are **not eligible** for review rich results. Marking up
  `quantum-reviews` with `AggregateRating` risks a manual action. Leave it alone.

What still genuinely earns visible results: **Event**, **Product/Offer**, **Breadcrumb**,
**Article** metadata, and **Organization** knowledge-panel signals.

### What actually moves AEO

AI engines cite what they can attribute and verify. In rough order:

1. **A correct, consistent entity.** One `Organization` per site — right name, right URL, real
   `sameAs` links to LinkedIn and Crunchbase. This is #1 by a distance, and it's the thing currently
   broken.
2. **Attribution.** `BlogPosting` with a real `author` (a `Person`, not "Admin"), `datePublished`
   and `dateModified`. An engine that can't attribute a claim is less likely to repeat it.
3. **Extractable answers.** `FAQPage`, and prose that answers the question in its first sentence.
   The persuasion modules already encourage this shape — `myth-reality` and `is-this-you` are
   question-answer structures whether or not they're marked up.
4. **Agreement between markup and visible text.** Markup that claims more than the page shows is the
   fastest way to get discounted.

The live QBS site already sells an "AEO Health Check" and an AEO score grader. Every client site we
build should be able to pass the check we're selling.

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

**3. Add schema to five templates and three modules**, following the `quantum-faq` pattern —
`BlogPosting` on `blog-post.html`, `Article` on `case-study.html`, `Service` on `interior.html`,
`Offer` on `pricing.html`, `BreadcrumbList` in `base.html`, `Event` on `quantum-event-hero`,
`Person` on `quantum-team`, `Offer` on `quantum-pricing-matrix`.

Change 2 is the one that matters — it stops nine themes asserting a false identity. Changes 1 and 3
are the product improvement, and because they're fixes **at source** rather than per-client forks,
every past and future client benefits from one edit. That's the whole argument for not forking
themes, made concrete.

Sequence it as: nine `fields.json` patches → nine `base.html` patches → validate on one non-production
theme → then the module and template work.
