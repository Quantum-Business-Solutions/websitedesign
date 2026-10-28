# VAF module port: contract

Goal: the Van Ausdall & Farrar "Showcase" preview (https://van-ausdall.vercel.app/showcase/index.html, built by
`scripts/preview*.py` from `brands/vanausdall.content.json`) rebuilt as HubSpot modules, with **visual and copy parity
with the preview, then better**. World class: this is the site of Indiana's largest office technology provider.

## What exists
- Reference renderers (Python f-strings, one per section `type`): `scripts/preview.py` (core: hero, detail, cards, faq,
  leadform ...), `scripts/preview_sections.py`, `scripts/preview_modules.py`, `scripts/preview_hub.py`. Find yours with
  `grep -n "def _<type>\|\"<type>\"" scripts/preview*.py`.
- Reference CSS: `themes/vaf/reference/showcase.css` (the one shared 84 KB sheet, tokens + every pv-*/q-* class) and
  reference JS: `themes/vaf/reference/showcase-scripts.js`. The theme will load the WHOLE sheet, so your module markup can
  use the same class names and look identical. Put only NEW or overriding rules (mobile fixes, new designs) in `module.css`.
- Built preview pages to look at (a local server is already running on http://localhost:8765/ serving the showcase
  direction, e.g. http://localhost:8765/index.html, /services/managed-it.html). Screenshot with Playwright
  (`require('playwright')`, chromium, no install) at 1360 and 390 wide. Section data: `brands/vanausdall.content.json`
  (`pages[].sections[]`, keyed by `type`).
- Helpers: `scripts/vaf_common.py` (A() asset URL, href(), link(), image(), partner_logo(), esc(), rt()). Images are already
  in HubSpot Files via `brands/vanausdall.asset-map.json`; always map image paths with `A()` / `image()`.
  Partner logo files exist (`partner_logo("Canon")`); use real logos, never plain text where a logo exists.
- Offline checker: `python3 scripts/vaf_check.py themes/vaf/modules/<m>.module` and
  `python3 scripts/vaf_check.py --mapper scripts/vaf_map_<x>.py`. Both must print OK.

## Deliverables per module
`themes/vaf/modules/vaf-<name>.module/` with `fields.json`, `meta.json`, `module.html` (+ `module.css`, `module.js` if needed),
and ONE mapper file `scripts/vaf_map_<x>.py` exporting
`REGISTRY = {"<section type>": ("vaf-<name>", mapper)}` where `mapper(section_dict) -> params dict` (keys = field names;
repeaters = list of dicts keyed by child field names; image fields via `image()`, link fields via `link()`,
rich text via `rt()`). One mapper per section type, covering EVERY key that type uses anywhere in the content file
(check all pages: `python3 -I -c` over content.json; do not design from one example). The builder bakes mapper output into
`dnd_module` defaults, so every page is drag and drop and every visible string/image/link is an editable field.
meta.json: copy `themes/source/Quantum Showcase/modules/quantum-faq.module/meta.json` and change `label`;
keep `host_template_types: ["PAGE"]`.

## HubSpot hard rules (HubSpot rejects or silently breaks otherwise)
- Forbidden field ids: body, label, value, name, type, id, default, content. Use copy, caption, anchor, item_label, etc.
  The content's `id` key becomes field `anchor`; `alt` (alternate background) becomes `alt_bg`.
- Field ids unique across the WHOLE module including nested groups: prefix nested ids (`step_title`, not `title` twice).
- Repeaters: `{"type":"group","occurrence":{"min":N,"max":M,"default":K}, "default":[...]}`; default MUST be an array with at
  least `min` items; occurrence.default >= min.
- Link field value is `{url:{href,type,content_id}, open_in_new_tab, no_follow}` -> `{{ f.url.href }}`; image -> `{{ f.src }}`,
  `{{ f.alt }}`. Rich text fields receive HTML.
- A `form` field ignores `module_attribute`: its default must live in fields.json. Render forms with
  `{% form form_to_use="{{ module.form.form_id }}", no_title=True, response_response_type="inline", response_message="{{ module.form.message }}" %}`.
- Booleans and numbers: pass real JSON types in mapper output.
- HubL: `{% raw %}` for literal braces; `|split('\n')` on richtext only AFTER replace/striptags; no `[a,b]|min`.
- module.js is allowed (host type PAGE only). Scope every selector to the module root (several instances per page);
  respect `prefers-reduced-motion`; no globals; no external libraries.
- No em dashes or en dashes anywhere a visitor reads (copy, aria-labels, alt text, defaults).
- Do not composite text with `opacity`; use colour tokens (`var(--fg-muted)` etc. from the CSS).

## Quality bar
- Mobile first-class: no horizontal scroll at 390px, tap targets 44px, stacked layouts, readable type.
- Accessibility: real headings, buttons for controls, aria for tabs/accordions, visible focus, alt text, contrast.
- Balanced layouts: no orphan card in a last row (choose column count from item count in HubL).
- Interactive pieces (tabs, steppers, sliders, hotspots, maps, wheels) must work with keyboard and without JS must still
  show all the content.
- Do NOT upload to HubSpot, do NOT run git, do NOT edit files outside your own modules/mapper (the orchestrator
  validates, uploads, QAs in a real browser and sends feedback).

## Report back (max 30 lines)
Per module: what you built, the section types and keys it covers, anything the orchestrator must do
(e.g. a new CSS rule needed in the base sheet, an asset to source), and any open doubt.
