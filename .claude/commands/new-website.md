---
description: Company name in, three grounded website directions out — the full methodology
argument-hint: "<company name or URL>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__Firecrawl__firecrawl_scrape, mcp__Firecrawl__firecrawl_search, mcp__BrandCommand__list_brands, mcp__BrandCommand__query_table, mcp__BrandCommand__insert_row, mcp__BrandCommand__list_websites, mcp__BrandCommand__get_website, mcp__Higgsfield__generate_image
---

Produce three distinct website directions for `$ARGUMENTS`, using the house methodology rather than
improvising. Follow the steps in order — the ordering is what prevents generic output.

**BrandCommand is the system of record.** Projects, directions, tokens and pages live there
(`brand_profiles`, `website_projects`, `builder_pages`, `builder_sections`). This repo supplies the
methodology and the taste. Do not build a parallel store.

## 1. Resolve the company

- `list_brands` to find an existing `brand_profile_id`. If none matches, say so and ask before
  creating one — a stray brand profile pollutes a live client system.
- `query_table` on `website_projects` filtered to that brand: **if directions already exist, read
  them first.** Extending or replacing existing work beats duplicating it. Report what's there.

## 2. Gather evidence — never design from the company name alone

- Their current site: `firecrawl_scrape` with `formats: ["branding"]` for measured tokens. Record
  the URL as `extracted_from`.
- Two or three category competitors, same way, so you know what the sector looks like — and
  therefore what "not generic here" means.
- `brands/<slug>.md` if it exists. Client-stated constraints outrank everything else you gather.
- If the client supplied a **Figma file**, it is the most precise source available (real fills, type
  styles, spacing, variables) — use it over any scrape of a rendered page.

## 3. Ground in the house taste

Read `design/guardrails.md` and `design/references.md`. Pull token files for the relevant page type
or register. **Where the brand brief and the guardrails conflict, the brief wins** — a house default
never overrides a paying client's stated preference.

## 4. Write the brief before designing

Create or update `brands/<slug>.md` from `brands/_template.md`. State the design read explicitly:
*"Reading this as: <page kind> for <audience>, with a <vibe> language, leaning toward <family>."*

If the read genuinely diverges, ask **one** question. Otherwise proceed.

## 5. Three genuinely distinct directions

Not one design with variations. Each direction needs a different **aesthetic family** — different
type pairing, different ground, different register. Follow the house naming convention already in
use:

```
<Company> — <DirectionName>
"Direction N of 3. <one-line rationale>. <palette and type in a phrase>."
```

Revolution's Signature / Ink / Press is the reference for this. One direction should sit close to
where the brand is today; the others should genuinely stretch, or the choice is theatre.

For each, produce a full token set matching the shape already in `website_projects.colors`
(`primary`, `secondary`, `accent`, `background`, `text`, plus `surface` / `dark` / `muted` where
useful) and `fonts` (`heading`, `body`).

## 6. Write them to BrandCommand

`insert_row` into `website_projects`, one row per direction, with `brand_profile_id`, `name`,
`description`, `colors`, `fonts`, `logo_url`, `extracted_from`, `current_website_url`,
`current_platform`, `status: "draft"`.

These are **live client records** — state exactly what you are about to write and get confirmation
before the first insert.

## 7. Show the options

Build one artifact showing all three side by side: real palette swatches, the type pairing set in
the actual faces, the rationale, and a representative hero block for each. The client picks from
this. Three directions in one view is the entire point — comparison is what makes the choice real.

Hero imagery comes later, only for the chosen direction — see `design/prompts.md`. Don't spend
credits rendering three heroes when two get discarded.

## 8. Run the anti-slop gate before anything ships

`/impeccable critique` and `/impeccable audit`, then re-check against `design/guardrails.md` line by
line. A direction that trips a guardrail doesn't go to the client.

## 9. Feed it back

New reference worth keeping → `design/inbox.md`. A rule that generalises → `design/guardrails.md`.
A prompt that worked → `design/prompts.md` with model and settings.
