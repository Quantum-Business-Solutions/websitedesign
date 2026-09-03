# Re-skinning a theme

How a client's brand gets onto one of the nine. This is the mechanical core of Lane A.

> **Rewritten 2026-09-03.** The previous version described a six-value `fields.json` re-skin. That
> mechanism does not exist: `theme.colors` is referenced in **zero** files across all nine themes, so
> the five colour fields were dead and setting them changed nothing on the rendered page. See
> `process/qa-findings.md`. What follows is the surface that actually renders.

## The real surface: `css/quantum.css`

Every theme's stylesheet has the same architecture:

```
:root                                        base --q-* tokens (identical in all nine)
[data-theme="dark"] / [data-theme="light"]   the mode palettes
[data-qdir="clean"] … [data-qdir="void"]     ALL NINE directions, in EVERY theme's CSS
/* ===== NATIVE DIRECTION: <Theme> ===== */
  :root, [data-theme="dark"], [data-theme="light"] { … }   ← pins this theme's direction
```

**The nine themes are one stylesheet with nine presets.** The native-direction block selects which,
and because it sits last at equal specificity it overrides both mode palettes — which is why
`appearance.mode` has no effect on colour.

Re-skinning means rewriting that one block. Twelve custom properties:

| Property | Role |
|---|---|
| `--q-gold` | Primary accent — links, primary CTA |
| `--q-gold-bright` | Accent hover/active |
| `--q-gold-dim` | Accent, de-emphasised |
| `--q-serif` | Heading face — **the theme's identity** |
| `--q-sans` | Body face |
| `--bg` | Page ground. **This is the real light/dark answer** |
| `--bg-alt` | Alternating band / raised surface |
| `--fg` | Body text |
| `--fg-muted` | Secondary text |
| `--border` | Hairlines |
| `--card` | Card surface |
| `--cta-fg` | Text **on** the accent — contrast-critical, see below |

**Typefaces are re-skinnable.** `--q-serif` and `--q-sans` are in the block. The old claim that
changing type means changing theme was true of `fields.json` and false of the product. Changing
theme is still usually the *right* call — nine typefaces is a curated system and a client-specific
face is a fork — but it is a judgement now, not a constraint.

### `fields.json` — one live field

`appearance.mode` still drives the `.only-dark` / `.only-light` logo visibility rules, so set it to
match the ground or the client's logo shows the wrong variant. `colors.*` is dead; leave it alone.

## Run it

```bash
export QBS_HUBSPOT_TOKEN=...          # never written to disk

python3 scripts/reskin.py audit       # sweep all nine for known defects
python3 scripts/reskin.py inspect --theme "Quantum Press"

python3 scripts/reskin.py plan \
    --theme "Quantum Press" --client "Meridian Dental" \
    --accent "#1E6B8C" --ground light \
    --org-name "Meridian Dental Group" --org-url "https://meridiandental.com"
```

`plan` is **read-only** and prints the exact change table. That table *is* the propose-then-confirm
proposal required by the `qbs-hubspot-private-app` skill. To execute:

```bash
    … --apply --approved-by "<name>"
```

The script refuses to write to any of the nine, verifies the portal is `20682069` first, and does
the clone, the native-direction block, `appearance.mode` and the client's `Organization` schema in
one pass — so the schema cannot be forgotten.

## The contrast gate

`plan` measures four ratios and **refuses to apply** if any fails:

| Pair | Needs |
|---|---|
| `--cta-fg` on `--q-gold` | 4.5:1 |
| `--fg` on `--bg` | 4.5:1 |
| `--fg-muted` on `--bg` | 4.5:1 |
| `--q-gold` on `--bg` | 3.0:1 |

This is not theoretical. **All five light themes currently fail the first one** — 3.9:1 for Clean,
Paper, Journal and Showcase, **3.5:1 for Press** — near-white text on a mid-gold. That is every
primary button on every light-theme site. The four dark themes pass at 8.2:1.

Never fix contrast with `opacity`. Use a real colour — `guardrails.md`.

## Deriving the values

Give the script an accent and it derives the rest. Three rules survive from the old version:

1. **Sanity-check every extracted colour against the live site.** Extractors mislabel state colours
   as base colours — GOV.UK's "link" is its focus-highlight yellow. Two token files in this repo
   prove it; see `design/guardrails.md`.
2. **`--q-gold-bright` is derived, not extracted.** Same hue, shifted lightness. A second unrelated
   colour reads as a mistake.
3. **Bias the neutrals toward a hue.** A pure mid-grey reads as inherited; a slight cast reads as
   chosen. Saturation has to *rise* at the extremes — at lightness 0.05 a saturation of 0.10 rounds
   to pure grey and silently fails the guardrail it was written to satisfy.

`--neutral-hue` defaults to the accent. Pass a hex for a complementary scheme — which is what the
QBS originals actually do: gold accent against blue-cast neutrals. The guardrail as written doesn't
describe the house themes; both are legitimate, so make the choice explicitly.

## What the script does NOT fix

**The header and footer still say Quantum Business Solutions.** `templates/partials/header.html` and
`footer.html` hardcode QBS's logo images, LinkedIn/Facebook/Instagram URLs, QBS nav links, a Quantum
Academy enrolment link, and the copyright line. A crawler has to be told about bad schema; a client
notices our logo on their site in five seconds.

Both are `templateType: global_partial` — **portal-scoped singletons**, so this is not a
clone-and-edit. Resolve it before anything goes in front of a client: either convert the partials to
field-driven modules at source (the right fix, benefits everyone) or build client-specific partials
and repoint the clone's `base.html` blocks at them.

`reskin.py plan` reports the leak on every run so it can't be forgotten.

## Recording it

One `website_projects` row per direction:

```
<Company> — <ThemeName>
"Direction N of 3. <one-line rationale>. <palette and type in a phrase>."
```

Populate `colors` and `fonts` from the native-direction values. Note the schema is a five-key jsonb
(`text`, `accent`, `primary`, `secondary`, `background`) with **no slot for the ground or the clone
path** — put the theme name and preview URL in `name`/`description` by convention until a column
exists.

## What re-skinning does not fix

Colour, type and ground. If a direction is wrong because the **structure** is wrong, that's a theme
fix at source, benefiting every future client. Resist per-client structural forks; that's how nine
maintainable themes become forty unmaintainable ones.

And a caution worth knowing: **eight of the nine themes have never rendered a live page.** Every
live QBS page uses Void. A client build on Press or Journal is that theme's first real test — which
is exactly how the contrast failure above would have reached production. Gate it with
`node scripts/verify.mjs`.
