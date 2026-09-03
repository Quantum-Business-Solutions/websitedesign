---
description: Interview, then build — company name in, three gorgeous options out
argument-hint: "<company name or URL>"
allowed-tools: AskUserQuestion, Read, Write, Edit, Glob, Grep, Bash, Skill, mcp__Firecrawl__firecrawl_scrape, mcp__Firecrawl__firecrawl_search, mcp__BrandCommand__list_brands, mcp__BrandCommand__query_table, mcp__BrandCommand__insert_row, mcp__BrandCommand__list_websites, mcp__BrandCommand__get_website, mcp__Higgsfield__generate_image, mcp__Higgsfield__balance, mcp__Higgsfield__job_display, mcp__Higgsfield__upscale_image
---

Build website options for `$ARGUMENTS`. **Interview first, then build in one pass.** The interview
is four questions — do not skip it and do not expand it. Guessing the answers is what produces slop;
asking twelve questions is what makes people stop using the tool.

This command is Phases 01–03 of the process QBS actually sells — six phases, 90 days, three fixed
packages. Read `process/website-design-process.md` once so you know which phase you're in and what
tier was bought; the tier decides re-skin depth (Launch = theme as-is, Growth = clone and re-skin,
Transform = clone, re-skin and extend at source).

## Step 1 — Gather evidence BEFORE asking anything

Ask nothing you could have found out yourself. Run these first, in parallel:

- `list_brands` → the `brand_profile_id`. Then `query_table` on `website_projects` for that brand —
  **if directions already exist, read them before proposing new ones.**
- `firecrawl_scrape` their current site with `formats: ["branding"]` → measured tokens.
- `firecrawl_scrape` two or three category competitors the same way.
- `brands/<slug>.md` if it exists — client-stated constraints outrank everything.
- `themes/catalogue.md` and `design/guardrails.md`.

Then state a one-line **design read**: *"Reading this as: <page kind> for <audience>, with a <vibe>
language."*

## Step 2 — The interview: exactly four questions

One `AskUserQuestion` call, four questions, each with concrete options drawn from the evidence you
just gathered — never generic. Offer your recommendation as the first option.

1. **Lane.** Full multi-page site (three of the nine themes, re-skinned → HubSpot) or a single
   signature scroll page (`scroll-craft`)? Recommend by what they asked for; full site is the
   default for a client website.
2. **Ground.** Light or dark? Pull the answer from the brief if it's already stated — if it is, say
   so and confirm rather than asking blind. **This is the question that prevents the Revolution
   "Ink" mistake.**
3. **Register.** Which three themes, from your recommended set of three (safe / stretch / wildcard,
   per the selection rules)? Show the typeface and what each reads as.
4. **The promise.** In one line, what does this site have to make a visitor believe? Pain, person,
   promise. Everything downstream — hero copy, section order, imagery — hangs off this, and it is
   the one thing you genuinely cannot infer.

## Step 3 — Write the brief

Create or update `brands/<slug>.md` from the template with the answers, the measured tokens, the
competitor reads, and the chosen themes. **This is the artifact that makes the next build faster.**

Cross-check the answers against the brief's existing constraints and **stop if they conflict** —
that check is the whole reason the brief exists.

## Step 4 — Build

### Lane A: full site (three of nine, re-skinned)

Follow `process/reskin.md`. Per theme: map the client's measured tokens onto the six-value surface
(`appearance.mode` — **always set explicitly**, the defaults are wrong — plus `gold`, `gold_bright`,
`void`, `navy`, `paper`). Record each as a `website_projects` row using the house naming
convention:

```
<Company> — <ThemeName>
"Direction N of 3. <one-line rationale>. <palette and type in a phrase>."
```

### Lane B: signature scroll page

Invoke the `scroll-craft` skill. It runs its own deeper interview, picks a page grammar and a
signature move, and verifies by screenshotting its own scroll. Don't duplicate its questions —
hand it the brief and let it work.

## Step 5 — Make it gorgeous, not just correct

This is the step that separates a re-skin from something worth showing.

- **Hero imagery — Higgsfield.** `design/prompts.md` has a proven render prompt and the four things
  that make it work. Check `balance` first, preflight with `get_cost: true`, and **generate with
  blank surfaces** so labels stay real HTML text — crisp, editable, translatable, and readable by
  search engines. Baked-in AI text fails all four.
  Only render for the **chosen** direction. Three heroes when two get discarded is wasted credit.
- **Craft pass — Impeccable.** `/impeccable polish` on the chosen build, and `/impeccable bolder`
  where a direction is landing safe.
- **Anti-default pass — `design-taste-frontend`.** It states a design read and steers off LLM
  defaults. Cheap, and it catches the generic reflexes.
- **Motion and components.** See the sourcing routes in `design/references.md` — 21st.dev for
  component prompts, motion-primitives for animated backgrounds, godly.design and Awwwards for
  niche references. **Take the technique, not the frame** (see the sourcing rules in
  `design/guardrails.md`).

## Step 6 — The gate. Nothing ships without it

Run `process/checklist.md` end to end. Then:

- `/impeccable critique` — UX and hierarchy
- `/impeccable audit` — accessibility, responsive, performance
- Re-read `design/guardrails.md` and check line by line

**Verification loop:** screenshot the build and actually look at it — including at mobile width.
Iterate on what you see, not on what you intended. A build nobody looked at is a build nobody
checked.

A direction that trips a guardrail does not go to the client.

**And check it's findable, not just handsome.** `process/launch-standards.md` and
`process/structured-data.md` — schema names the *client* not QBS, `og:image` set, images lazy below
the fold, two conversion paths per page. A beautiful site nobody finds and nobody converts on is a
failed build.

## Step 7 — Show one main page, then three options

Follow `process/pitch-presentation.md`. Four pages, not one: a **main page** carrying the design
read, the measured tokens, the competitors, the client's promise in their own words, and the
constraints being honoured — then **three option pages**, one per direction.

Each option: real palette swatches at the re-skinned values, the type pairing **set in the actual
faces**, a representative hero block, one line of rationale. Label them by character, not by number
— *"Signature — the safe one"*, not *"Option 1"*.

The main page is what makes a prospect believe effort was already invested, because it shows the
evidence rather than asserting it. Comparison is what makes their choice real.

## Step 8 — Feed it back

Record the client's choice in `brands/<slug>.md` — **and why, in their words.** The rejected
directions and the reason are worth as much as the winner.

New reference → `design/inbox.md`, then `/design-ingest`. A rule that generalises →
`design/guardrails.md`. A prompt that worked → `design/prompts.md` with model and settings. A theme
tweak worth keeping → `themes/catalogue.md`.
