# Re-skinning a theme

How a client's brand gets onto one of the nine. This is the mechanical core of Lane A, and it is
much smaller than it sounds: **six values per theme.**

## The surface

Identical across all nine themes — verified against every `fields.json`. Typefaces are baked into
the theme and are not re-skinnable; changing type means changing theme, which is why nine themes is
the type system.

| Field | QBS default | Set it to |
|---|---|---|
| `appearance.mode` | `dark` | `light` or `dark` — **always explicit** |
| `colors.gold` | `#c4a44a` | Client's accent — links and primary CTA |
| `colors.gold_bright` | `#d4ba6a` | Accent hover/active — a lighter step of the same hue |
| `colors.void` | `#080b12` | Darkest ground |
| `colors.navy` | `#101725` | Mid surface — cards, raised panels |
| `colors.paper` | `#fbfaf6` | Lightest ground |

> **The trap:** every theme defaults to `mode: dark`, including the five light ones. Clean, Press,
> Paper, Journal and Showcase all render dark out of the box, contradicting their own descriptions.
> Never rely on the default.

> **The bigger trap: six values is not the whole re-skin.** `fields.json` has only `appearance` and
> `colors` — there is no field for identity. So `templates/layouts/base.html` keeps emitting *QBS's*
> `Organization` JSON-LD on every page of every client site, and no amount of re-skinning changes
> it. Until that's fixed at source, **hand-edit `base.html` on the clone** so the schema names the
> client. See `process/structured-data.md`.

## Mapping measured tokens onto the surface

Firecrawl's `branding` extractor gives roled colours — see `design/SCHEMA.md`. The mapping:

| Measured | → | Theme field |
|---|---|---|
| `colors.accent` (or `link`) | → | `gold` |
| a lighter step of that hue | → | `gold_bright` |
| `colors.background` if dark, else darkest neutral | → | `void` |
| a mid surface between ground and accent | → | `navy` |
| `colors.background` if light, else lightest neutral | → | `paper` |

Three rules that decide whether it looks designed or generated:

1. **Sanity-check every extracted colour against the live site.** Extractors mislabel state colours
   as base colours — GOV.UK's "link" is its focus-highlight yellow; Vercel's doesn't match anything
   visible. See "Reading measured tokens" in `design/guardrails.md`.
2. **`gold_bright` is derived, not extracted.** Same hue, lifted lightness. A second unrelated
   colour here reads as a mistake.
3. **Bias the neutrals toward the accent hue.** A pure mid-grey reads as inherited; a neutral with a
   slight hue cast reads as chosen. This is a house guardrail and it survives re-skinning.

## The operation

Themes live in HubSpot Design Manager on portal `20682069`. Auth via PAT — see the
`qbs-hubspot-private-app` skill; the OAuth MCP returns `REQUIRES_REAUTHORIZATION` for CMS.

Read the current surface:

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.hubapi.com/cms/v3/source-code/published/content/Quantum%20Clean/fields.json"
```

**Do not edit the nine in place.** They are the product line, shared across every client. Clone to a
client-specific child, then re-skin the clone:

```
Quantum Press            ← never touched
Revolution — Press       ← the clone that gets the client's six values
```

Writes to a live portal follow the propose-then-confirm protocol in the
`qbs-hubspot-private-app` skill: state the exact change as a table, wait for explicit approval, then
execute. No exceptions.

## Recording it

One `website_projects` row per direction, house naming convention:

```
<Company> — <ThemeName>
"Direction N of 3. <one-line rationale>. <palette and type in a phrase>."
```

Populate `colors` and `fonts` with the re-skinned values — `fonts` from the theme's baked typeface,
so the record is self-describing without opening HubSpot. Set `extracted_from` to the URL the tokens
came from and `current_website_url` to the site being replaced.

## What re-skinning does not fix

Colour and ground only — and that's narrower than it sounds. **Identity is not colour.** The
`Organization` schema in `base.html` and anything else naming QBS survives a perfect re-skin
untouched, because it isn't a field. Check the clone's `<head>` by hand every time.

Beyond that: If a direction is wrong because the **typeface** is wrong, the answer is a
different theme, not a different palette — and if it's wrong because the **structure** is wrong,
that's a theme fix at source, benefiting every future client. Resist per-client structural forks;
that's how nine maintainable themes become forty unmaintainable ones.
