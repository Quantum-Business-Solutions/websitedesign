# The agent roster

What each agent is for, what it may touch, and — the part that decides whether this works — **what
it is checked against.**

An agent with no objective gate is a confident guesser. Every producing agent below is paired with
something that can fail it: a script with an exit code, a measured token, or a written constraint.
That pairing is the design; the roster is just the list.

## Why this repo can support agents when most can't

Four things already exist that make agent output *checkable* rather than merely plausible:

- **`scripts/verify.mjs`** — exit code 1 on accessibility, contrast, schema entity, card-grid
  balance, conversion paths, placeholder text
- **`scripts/reskin.py`** — refuses to apply a re-skin failing four contrast ratios
- **`design/guardrails.md`** — written always/never, several earned from real failures
- **`process/seo-baseline.md`** — measured numbers, not impressions

**Build the gate before the agent that feeds it.** An unchecked agent produces work someone has to
review by hand, which is slower than doing it.

---

## Producing agents

### Brand agent
Establishes the visual and verbal identity when a client hasn't got one, or extracts it when they
have.

- **Reads:** their live site (`firecrawl_scrape` `formats:["branding"]`), logo files, any Figma,
  competitor scrapes
- **Writes:** the brand-asset and entity-facts sections of `brands/<slug>.md`,
  `design/tokens/<slug>.json`
- **Gate:** every colour traceable to a measured token or a client-supplied asset. **No invented
  hexes.** `design/SCHEMA.md`'s failure rule applies — leave a gap rather than guess
- **Trap:** extractors mislabel state colours as base colours. Two token files in this repo prove
  it. Sanity-check against the live page every time

### Marketing / copy agent
**The highest-value agent to build, because copy is the last unsolved bottleneck** — 15 of the 43
page hours, and the only remaining "AI slop" tell now that design is systematised.

- **Reads:** the brief, the Semrush striking-distance keywords, competitor scrapes, the client's own
  existing language
- **Writes:** page copy against a chosen section order
- **Gate:** the **three P's** above the fold — what problem, am I the person, what's promised. Plus
  `verify.mjs` on placeholder text and heading structure. Plus one hard rule: **the `<h1>` must
  answer a real keyword from the baseline**, not a slogan
- **Trap:** generic copy is what makes a site read as AI-built. Ground every page in the client's
  own words and a real search term, or it will average out

### FAQ + AEO agent
Answers the "built in, not bolted on" promise on the website-services page.

- **Writes:** FAQ content into `quantum-faq.module` fields — which is the only module in the 57 that
  emits structured data, and it does it correctly
- **Gate:** `verify.mjs` parses every JSON-LD block and asserts the `Organization` names the client
- **Read `process/structured-data.md` first.** The honest limits are non-obvious and an agent will
  otherwise overclaim: **FAQ rich results were fully retired 7 May 2026**, `Service` earns nothing
  visible, `BreadcrumbList` is desktop-only, and Google states plainly that structured data *isn't
  required* for generative AI search. Keep `FAQPage` for clean extractable Q&A; never sell it as a
  rich result
- **What actually moves AEO:** markup that agrees with visible text, genuinely useful non-commodity
  content, off-site brand presence, and real author attribution. In that order

### Website developer agent
Turns an approved section order and approved copy into pages in HubSpot.

- **Reads:** `process/OPERATOR.md` — self-contained, and opens with the five traps
- **Writes:** pages in the **cloned** theme only
- **Gate:** `verify.mjs --expect-org "<Client>"`, exit 0 required
- **Hard limits:** never edit one of the nine · never write to the portal without the
  propose-then-confirm table · `reskin.py plan` before `--apply`

### Layout / section agent
Picks module order from the 57 — this is Phase 03 wireframing, and it's a selection problem, not a
drawing problem.

- **Gate:** card-grid balance (the rule in `design/guardrails.md`, measured by `verify.mjs` at three
  widths), and the persuasion-module mapping — when a hero fails the three-P test the fix is usually
  a missing module, not new adjectives

---

## Checking agents

The producing agents above are individually gated. These review across a build, and their value is
that **they are not the agent that produced the work.**

### Quality agent
Runs `process/checklist.md` end to end plus `verify.mjs`, reads `design/guardrails.md` line by line
against the build, and **looks at the screenshots**.

Its most important instruction: **report what you see, not what was intended.** This repo's own
history is the argument — two hand-coded graphics shipped with a written note admitting they were
flat, because nobody looked. And `verify.mjs` found two accessibility failures on QBS's own site
that four QA agents missed.

### Fact-check agent
Verifies claims against primary sources, with web access. Non-optional for anything client-facing
about search behaviour.

Justified by result: a fact-check pass on this repo found the FAQ deprecation was three years out of
date, the searchbox retirement was off by a year, "302s don't pass authority" was folklore Google
reversed in 2016, the AEO priority list was **inverted** against Google's own guidance, and four
places overstated a Google penalty that doesn't exist.

**Instruction that makes it work:** return UNVERIFIABLE rather than invent a citation.

### Adversarial verifier
Takes each finding from a review and tries to disprove it. Cheap, and it's what stops a review
becoming a list of plausible-sounding non-problems.

---

## The loop that actually works

```
brief → sections → copy → build → verify.mjs → [exit 0? ship : back to the failing station]
                                             ↘ quality agent looks at screenshots
```

Three properties worth preserving:

1. **The loop terminates on an exit code**, not on an opinion. Otherwise it runs forever or stops
   too early.
2. **A failure returns to the station that caused it**, not to the start. A contrast failure is a
   re-skin problem; placeholder text is a copy problem.
3. **A human looks before the client does.** The harness catches what's measurable. It cannot tell
   you the design is wrong.

## Build order

1. **The gates first.** They exist. Don't add agents until each has one.
2. **Copy agent.** Biggest bottleneck, clearest gate.
3. **FAQ + AEO agent.** Small, and it closes a sold promise.
4. **Quality + fact-check agents.** Cheap; they've already proved their worth on this repo.
5. **Website developer agent.** Last, because it's the one that writes to a live portal, and it
   should only run once everything upstream is reliably gated.

## Two things an agent must never be trusted with alone

- **Writes to portal `20682069`.** Propose-then-confirm, with a human yes. No exceptions.
- **A claim about what Google does.** Cite a primary source with a date, or say UNVERIFIABLE.
