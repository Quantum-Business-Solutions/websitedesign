---
description: Company name in, three gorgeous directions out. No HubSpot writes.
argument-hint: "<company name or URL>"
allowed-tools: AskUserQuestion, Read, Write, Edit, Glob, Grep, Bash, Skill, mcp__Firecrawl__firecrawl_scrape, mcp__Firecrawl__firecrawl_search, mcp__BrandCommand__list_brands, mcp__BrandCommand__query_table, mcp__Semrush__overview_research, mcp__Semrush__organic_research, mcp__Semrush__projects_research, mcp__Semrush__get_report_schema, mcp__Semrush__execute_report
---

Build mockups for `$ARGUMENTS`. **Nothing here touches HubSpot.** That's the point: a mockup should
cost nothing and commit to nothing. The clone happens once, after they choose — `/build`.

## 1 — Gather evidence before asking anything

In parallel:

- `list_brands` → `brand_profile_id`, then `query_table` on `website_projects` — **if directions
  already exist, read them before proposing new ones.**
- `firecrawl_scrape` their site with `formats: ["branding"]` → the accent hex comes from here.
- Two or three category competitors, same way.
- The four Semrush pulls in `process/seo-baseline.md`. Pulls 1–3 work without a project.
- `brands/<slug>.md` if it exists. Client-stated constraints outrank everything.

## 2 — Four questions, one `AskUserQuestion` call

Options drawn from the evidence, never generic. Recommendation first.

1. **Ground** — light or dark. If the brief already says, confirm rather than ask. *This is the
   question that prevents the Revolution "Ink" mistake.*
2. **Register** — which three themes, from your recommended safe / stretch / wildcard.
3. **The promise** — one line: what must a visitor believe? The one thing you cannot infer.
4. **Lane** — full site, or a single scroll page via `scroll-craft`.

## 3 — Write the brief

`brands/<slug>.md` from `brands/_template.md`. Fill the entity facts, the SEO baseline, the
promise verbatim, the competitors, the tier. **Every section in that template is consumed by a
later phase** — a gap now is a blocked step in week six.

Cross-check against existing constraints and **stop if they conflict.** That check is why the
brief exists.

## 4 — Generate

```bash
python3 scripts/mockup.py \
    --client "<Company>" \
    --themes "Quantum <A>,Quantum <B>,Quantum <C>" \
    --accent "#RRGGBB" \
    --brief brands/<slug>.md \
    --roles "The safe one|The stretch|The wildcard" \
    --rationales "<why A>|<why B>|<why C>" \
    --out /tmp/<slug>-directions.html
```

Pipe-separated, so rationales can contain commas. It renders from `themes/tokens.json` — the
themes' real tokens — so the colours and faces are what ships, not an approximation.

**Act on its warnings.** It enforces the selection rules from `themes/catalogue.md`: mixed grounds,
two themes with the same ground and typeface class, Converter's watchlist status, and the
light-theme contrast failure. A warning means the *set* is wrong, not that the tool is fussy.

If `themes/tokens.json` is missing: `QBS_HUBSPOT_TOKEN=... python3 scripts/themetokens.py`.

## 5 — Look at it. Then publish.

Screenshot at 1440 and 390 and **actually look**. This is the step that gets skipped, and this
script's own first run produced three near-identical options — caught only by looking.

Then publish as an artifact and hand over the link.

## 6 — Only after they choose

Hero imagery (`design/prompts.md`), `/impeccable polish`, `design-taste-frontend`. Three
Higgsfield heroes when two get discarded is wasted credit.

Then `/build <company>` clones the chosen one.

## 7 — Feed it back

The choice **and why, in their words** → `brands/<slug>.md`. The rejected two are worth as much as
the winner. A rule that generalises → `design/guardrails.md`.
