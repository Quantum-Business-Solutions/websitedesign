# What the nine themes should become

The Revolution Office build solved, independently and in production, five problems the nine themes
still have. It is on a **client portal (`47019673`)**, not ours, and it is the better architecture.

Evidence: `Quantum-Business-Solutions/revolution`, `hubspot-theme/revolution-office/`. Its
`fields.json`:

```
direction [choice]  default=signature      ← one theme, three directions, a FIELD
brand
  accent      [color]                      ← the fill
  accent_ink  [color]                      ← accent TEXT on light grounds
type
  heading_font [font]                      ← typefaces ARE fields
  body_font    [font]
layout
  maxw [number]                            ← geometry is a field
```

And critically, **those fields are wired** — `theme.direction` (×3),
`theme.brand.accent.color` (×2), `theme.brand.accent_ink.color` (×2), `theme.layout.maxw` (×2),
`theme.type.heading_font.font`, `theme.type.body_font.font` all appear in the source. Compare the
nine, where `theme.colors` appears **zero** times.

---

## 1. Split the accent in two. This is the WCAG fix.

Revolution's own comment, in `lib/themes.js`:

> *"`--accent` is the fill: buttons, chips, rules, icons, and any accent text sitting on a dark
> ground. `--accent-ink` is accent TEXT on light grounds, darkened until it clears WCAG AA — the
> bright amber that makes a button work is **1.86:1 on white**, which fails badly on exactly the
> numbers we most want read."*

That is the same defect as the five light Quantum themes failing at 3.5–3.9:1 — and the right fix
is not "darken the accent," which kills the button. It is **two tokens with two jobs**:

| Token | Job | Constraint |
|---|---|---|
| `--accent` | Fill — buttons, chips, rules, icons | Its *text* must clear 4.5:1 |
| `--accent-ink` | Accent text on light grounds | Darkened until it clears 4.5:1 |
| `--accent-lift` | Accent text on dark bands | Signature's amber works; Press's bronze doesn't — hence a token |

Revolution needed a *third* because a single accent cannot serve a light band and a dark band. The
nine have one accent doing all three jobs, which is why the buttons fail.

## 2. A direction is not a palette

> *"Each one owns its own geometry — band rhythm, measure, display scale, grid density, card padding
> and alignment — so the three read as genuinely different systems rather than one layout
> recoloured. **Color tokens alone produced three pages with identical band heights, which is the
> thing a buyer notices immediately.**"*

`scripts/mockup.py` hit exactly this on its first run — three near-identical options differing only
in typeface. Revolution's answer is better than the one applied there: **geometry tokens**.

```
--hero-size · --display-1 · --display-2 · --display-3
--maxw · --sec-y · --radius · --heading-tracking · --heading-weight
```

The nine themes have **none** of these, which is why a re-skin of the nine can only ever change
colour. Adding them is what would make the nine feel like nine systems rather than nine palettes.

Revolution goes further still: `heroMode` per direction, so the three **don't share a first
screen** — and the chooser card reads it from the same source, "so the spec table cannot drift from
what the page actually renders."

## 3. One theme with a `direction` field beats N clones

Revolution ships **one** theme with `direction: choice`. The nine's model is nine themes plus a
clone per client. One field is cheaper to maintain, cheaper to switch, and it means a client can be
moved between directions after launch without a rebuild.

## 4. Global header and footer as MODULES, not hardcoded partials

Revolution: **31 modules = 29 content + global header/footer**, with their defaults regenerated
from `lib/site.js` by `gen-chrome.mjs`.

The nine hardcode QBS's logo, nav, social links and copyright into `partials/header.html` and
`footer.html` — which is the leak `scripts/reskin.py` explicitly cannot fix, and the one a client
notices in five seconds. **Revolution already shows the fix: make them field-driven modules.**

## 5. Generate the tokens, don't hand-maintain them

`gen-tokens.mjs` regenerates `css/tokens.css` from `lib/themes.js` "so the theme cannot drift from
the review previews." Same principle as `scripts/designsystem.py` here. One source, generated
downstream.

## Also better, and cheap to copy

- **Skip link and semantic main** — `<a class="skip" href="#main">` and `<main id="main">`.
  The nine have neither.
- **No hardcoded identity in `base.html`.** Revolution's is clean because it was built *for the
  client*. The nine's carries QBS's `Organization` block.
- **A `sections/` layer** — 7 drag-and-drop sections (`assessment`, `close`, `faq`, `outcome`,
  `partners`, `proof`, `solutions`) sitting between modules and templates. A page grammar the nine
  don't have: a section is a *pre-composed* group of modules, so building a page is choosing seven
  sections rather than twenty modules.

---

## Production constraints found the hard way

Straight from the Revolution build. These are not opinions.

1. **`layoutSections` populated via the API does not render.** The fix was to *bake page content
   into per-page templates* (commit `611e068`). This directly qualifies the approach in the
   `qbs-atlas-page-builder` skill — verify before relying on programmatic `layoutSections` for a
   new build. Note the theme's own README still describes the `layoutSections` approach, so **the
   README is stale relative to the commit**; trust the commit.
2. **Draft pages cannot be rendered anonymously** — preview links redirect to a HubSpot login. So
   `verify.mjs` cannot gate a draft. Visual QA needs a logged-in browser or a **temporary publish to
   the `<portal>.hs-sites.com` staging subdomain.** Plan for the staging publish; it is not
   optional.
3. **HubSpot free tier caps website pages at 30** (`contents limit 30 (cms-site-pages)`). CMS Hub
   Starter lifts it. A 50-page Transform build on a free portal is impossible — **check the client's
   tier at kickoff**, which is why it's step 4 of the runbook.
4. **Client portals use `CLIENT_HUBSPOT_TOKEN`**, never the QBS token, and never the OAuth MCP —
   which is bound to portal `20682069` and would silently corrupt the analysis.

## Status, 2026-09-06

**Patched at source, locally, not yet uploaded.** `scripts/themefix.py --all` applies items 1, 2, 4
and 5 to all nine and item 3 to the eight client-facing themes; the result is committed under
`themes/source/` (so `reskin.py drift` will report the portal as *behind* until the upload lands).
Two things the QA pass changed before anything shipped:

- **HubSpot theme `fields.json` does not accept text, image or menu fields** — only boolean, choice,
  color, font, number, spacing. So the brand and schema fields are **modules**
  (`quantum-site-header`, `quantum-site-footer`, `quantum-org-schema`) included from the global
  partials — which is Revolution's pattern anyway. The first draft put them in theme fields and
  would have failed validation on all nine.
- **Quantum Void is QBS's live theme** (41 published pages, a header full of QBS-specific menu logic).
  It gets the safe subset only: accent-ink (identity on dark, so nothing moves), geometry tokens at
  today's values, skip link and the content landmark. Its header, footer and schema are untouched.
  Clients clone from the other eight.

The upload itself (`reskin.py upload --fix-at-source --approved-by … --reason …`) was approved in
chat and is blocked only by the session's write permission to the portal. It validates every file
with the HubL validator before writing, foundation files first.

## The recommendation

Do not fork the nine toward this piecemeal. **Take the Revolution theme as the reference
implementation and bring the nine to it in one pass**, because four of the five changes touch the
same files:

1. `accent` → `accent` + `accent_ink` + `accent_lift`, and **wire them**
2. Geometry tokens per direction
3. Header/footer from hardcoded partials to field-driven modules
4. `seo` field group with the fail-safe `Organization` block (`process/structured-data.md`)
5. Skip link and semantic `<main>`

That single change fixes the contrast failure, the identity leak, the dead-fields problem and the
"nine palettes not nine systems" problem together — and every past and future client inherits it.
Still a write to portal `20682069`, so still propose-then-confirm.
