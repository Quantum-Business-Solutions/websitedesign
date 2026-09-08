# Hotspot walk ("Walk the building")

An illustration of the buyer's own environment with numbered markers. Each marker opens a finding
card: what we find there, the figure it produced, and a link. A Before / After toggle removes the
things the engagement takes away. First shipped on Revolution Office (Home and Managed Print
Services), 2026-09-08. The reasoning is in `design/patterns.md` → "The hotspot walk"; this folder is
the kit.

## What is here

| File | Use |
|---|---|
| `module/` | The HubSpot module, drop-in (`site-map.module`): meta, fields, HubL, CSS, JS. Rename the folder to match the theme's module naming. Depends on the theme tokens `--accent`, `--accent-fg`, `--accent-text`, `--ink`, `--line`, `--muted`, `--bg`, `--surface-bg`, `--radius`, `--font-heading`, `--font-body`, `--stack-3` and the `.band`, `.band--*`, `.band__eyebrow`, `.band__note`, `.wrap`, `.card` classes every Quantum theme carries. |
| `example-revolution-office.js` | The seven findings plus three "before only" markers, as page data. Copy, then replace every figure with the new client's own. |
| `preview/` | Desktop at rest, desktop with pin 4 open and After toggled, phone stack. |
| Illustration | `library/office-technology/scenes/isometric-admin-building-cutaway-2400.jpg` (generated, no text). Prompt in `design/prompts.md`. |

## How to reuse (30 minutes)

1. **Pick the building.** Use the vertical's isometric scene from `library/*/scenes/`, or generate one with the prompt. The illustration must carry **no text**: every word lives in the HTML cards so search and answer engines read the findings. Ask for "rooms arranged left to right" and name each room the client's process touches.
2. **Write the findings first, then place them.** One row per place: `place`, `title` (the finding, not the service), `copy`, `figure`, `figure_label`, `to`, `link_text`. The figure must come from the client's own record (a case study, the assessment workbook, a published stat). No figure, no marker.
3. **Measure positions as percentages.** Open the illustration at any size, note the pixel of the object, divide by width and height. Percentages survive any responsive width. Six to eight numbered markers; more and the picture turns into a legend.
4. **Add the "before only" markers.** Two or three small red × markers on the things the engagement removes (`state: 'before'`). The toggle is what turns a diagram into an argument.
5. **Place it early.** Right after the page names the problem ("nobody has the number") and before the method. On a service page, straight under the hero.
6. **QA the states, not just the rest position.** Capture desktop at rest, desktop with a marker open and After toggled, phone. The repo's `qa-remote.mjs` pattern: `QA_CLICK='.ro-walk__pin[data-pin="3"];.ro-walk__tb[data-state="after"]' QA_ELEMENTS=.ro-walk`.

## Module behaviour

- Desktop: map left (1.55fr), one finding card right, arrows and counter step through the numbered findings only. Hover on a fine pointer opens the card; tap or click on touch. Arrow keys work.
- Phone (under 1024px): illustration on top, every card stacked beneath it, toggle centred; the After view hides the removed-device cards.
- Reduced motion: the pulse rings stop; nothing else depends on animation.
- Every hotspot is a repeater row in the editor. Swapping the illustration keeps the percentages.

## Verticals

| Vertical | Building | Markers that earned their place |
|---|---|---|
| Office technology / managed print | Administration floor: copier room, open office with desk printers, supply closet, front office, IT closet, business office, second campus through the window | Copier room · a desk printer · supply closet · front office and records · IT closet · business office · the second campus |
| IT / MSP | Office with network closet, conference room, reception, warehouse door (`library/it-msp/scenes/isometric-office-eight-systems-1600.jpg`) | Network closet · conference room · every desk (endpoints) · reception (cameras and access) · the phone system · the cloud (out the window) · backup · the invoice |
| Accounting / advisory | A client's own office: front desk, owner's office, the file room, the bank (out the window) | Where the month-end sits, where the receipts pile up, where the cash actually is |
