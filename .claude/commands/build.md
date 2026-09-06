---
description: Build the chosen direction in HubSpot. Clone, re-skin, gate.
argument-hint: "<company name>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, mcp__BrandCommand__list_brands, mcp__BrandCommand__query_table, mcp__BrandCommand__insert_row, mcp__BrandCommand__create_website_project
---

Build the chosen direction for `$ARGUMENTS` in HubSpot. Run `/mockups` first — this command assumes
a brief exists and a direction has been picked.

## 1 — Confirm what was chosen

Read `brands/<slug>.md`. You need the theme name, the accent, the ground, and the entity facts
(legal name, canonical URL, logo, `sameAs`). **If the entity facts are missing, stop and get them** —
without them the clone ships QBS's identity, and that is the most damaging defect in the set.

## 2 — Propose

```bash
python3 scripts/reskin.py plan \
    --theme "Quantum <Theme>" --client "<Company>" \
    --accent "#RRGGBB" --ground <light|dark> \
    --org-name "<Legal name>" --org-url "https://<domain>" \
    --org-logo "<url>" --org-sameas "<linkedin>" "<crunchbase>"
```

Read-only. It prints the exact change table, the four contrast ratios, and what it will **not**
fix. **That table is the propose-then-confirm proposal** required by the
`qbs-hubspot-private-app` skill. Show it and wait.

## 3 — Apply

```bash
    … --apply --approved-by "<name>"
```

It refuses to write to any of the nine, verifies the portal is `20682069` first, and refuses to
apply a re-skin that fails the contrast gate. Clone, native-direction block, `appearance.mode` and
the client's `Organization` schema in one pass.

## 4 — Fix what the script can't

**The header and footer still say Quantum Business Solutions** — logo, nav, social links,
copyright. They're `global_partial`s, so this needs deliberate handling. `process/reskin.md` has
the two options. **Nothing goes in front of a client until this is done.**

## 5 — Pages and content

Create pages from the clone's templates. 12 of the 16 are a `dnd_area`, so the client can reorder
sections after launch — which is a real deliverable, so make it true: put the *right* sections in,
per the module inventory in `themes/catalogue.md`. The persuasion modules map onto the three P's.

## 6 — The gate

```bash
node scripts/verify.mjs <staging-url> --env staging --expect-org "<Legal name>"
```

Exit 1 means it failed. Then `process/checklist.md` end to end, `/impeccable audit`, and
**open the screenshots in `verify-out/` and look**, at phone width too.

Every changed URL needs a **301** — the URL map in the brief. On QBS's own domain, articles are 82%
of organic traffic; losing them in a redesign costs more than the build is worth.

## 7 — Record it

A `website_projects` row per direction, house naming. Then the baseline: the pre-launch numbers from
`process/seo-baseline.md` are what the optimisation window gets measured against. **No baseline, no
proof the work worked.**
