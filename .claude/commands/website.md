---
description: Interview, then build — company name in, three gorgeous options out
argument-hint: "<company name or URL>"
allowed-tools: AskUserQuestion, Read, Write, Edit, Glob, Grep, Bash, Skill, mcp__Firecrawl__firecrawl_scrape, mcp__Firecrawl__firecrawl_search, mcp__BrandCommand__list_brands, mcp__BrandCommand__query_table, mcp__BrandCommand__insert_row, mcp__BrandCommand__list_websites, mcp__BrandCommand__get_website, mcp__Semrush__overview_research, mcp__Semrush__organic_research, mcp__Semrush__siteaudit_research, mcp__Semrush__projects_research, mcp__Semrush__get_report_schema, mcp__Semrush__execute_report
---

Build website options for `$ARGUMENTS`. **Interview first, then build in one pass.** The interview
is four questions — do not skip it and do not expand it. Guessing the answers is what produces slop;
asking twelve questions is what makes people stop using the tool.

This command spans **Phases 01 through 06** of the process QBS actually sells — six phases, 90 days,
three fixed packages. It does not cover Phase 03 wireframing or Phase 04 content writing, which are
the long poles and are still run by hand. Read `process/website-design-process.md` once so you know
which phase you're in and what tier was bought; the tier decides re-skin depth (Launch = clone with
the theme's own colours, Growth = clone and re-skin, Transform = clone, re-skin and extend at
source). **Every tier clones** — there is no "use the theme as-is" tier.

## Step 1 — Gather evidence BEFORE asking anything

Ask nothing you could have found out yourself. Run these first, in parallel:

- `list_brands` → the `brand_profile_id`. Then `query_table` on `website_projects` for that brand —
  **if directions already exist, read them before proposing new ones.**
- `firecrawl_scrape` their current site with `formats: ["branding"]` → measured tokens.
- `firecrawl_scrape` two or three category competitors the same way.
- **The four Semrush pulls in `process/seo-baseline.md`** — traffic baseline, which pages actually
  earn it, striking-distance keywords, site audit. Write the baseline into the brief; it is the
  number the engagement gets measured against. On a client with no Semrush project, pulls 1-3 still
  work — start the project on day one so the audit is ready for Phase 02.
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

Use `scripts/reskin.py`, which does the clone, the twelve-token native-direction block **and the
client's `Organization` schema** in one pass — see `process/reskin.md` for the reasoning:

```bash
python3 scripts/reskin.py audit                     # sweep the nine for known defects
python3 scripts/reskin.py plan --theme "Quantum Press" --client "<Client>" \
    --accent "#RRGGBB" --ground light \
    --org-name "<Legal name>" --org-url "https://<domain>"
# read the proposal table, then re-run with:  --apply --approved-by "<name>"
```

**Colour is not the whole re-skin.** Identity is not a field: `templates/layouts/base.html`
emits QBS's `Organization` JSON-LD, and a perfect colour re-skin leaves it naming the wrong company.
The script patches it in the same pass so it cannot be forgotten. Never run `--apply` against one of
the nine.

Then record each direction as a `website_projects` row using the house naming convention:

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

**Ordering.** Clone and re-skin all three (Step 4) — that's cheap now. Everything in *this* step is
expensive, so run it on **one** direction only: your recommended one before the pitch, so the set
isn't visibly uneven, then the client's pick after Step 7 if they chose differently. Three
Higgsfield heroes and three polish passes when two get discarded is waste.

- **Hero imagery — Higgsfield.** `design/prompts.md` has a proven render prompt and the four things
  that make it work. Check `balance` first, preflight with `get_cost: true`, and **generate with
  blank surfaces** so labels stay real HTML text — crisp, editable, translatable, and readable by
  search engines. Baked-in AI text fails all four.
  Render for **one** direction only, per the ordering note above.
  Higgsfield is exposed here as skills (`higgsfield-generate`), not as `mcp__Higgsfield__*` tools —
  check which is present before relying on `balance` or `get_cost`.
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

**Verification loop — run the harness, then look at what it produced:**

```bash
node scripts/verify.mjs <staging-url> --env staging --expect-org "<Client legal name>"
```

It screenshots at 390 / 768 / 1440, runs axe-core, measures LCP and CLS on mobile, parses every
JSON-LD block and asserts the `Organization` names **the client**, and checks `og:image`,
lazy-loading, image dimensions, placeholder text, conversion paths and internal links. Exit code 1
means the gate failed.

Then open the screenshots in `verify-out/` and actually look. The harness catches what's measurable;
it cannot tell you the design is wrong. Iterate on what you see, not on what you intended — a build
nobody looked at is a build nobody checked.

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
