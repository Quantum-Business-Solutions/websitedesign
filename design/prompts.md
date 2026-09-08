# Working generation prompts

Prompts that produced usable assets, kept verbatim so they're re-runnable and tunable rather than
re-derived from scratch. Record the model and the settings — a prompt without them isn't reusable.

---

## Isometric modular ring — dark + gold render

- **model:** `nano_banana_pro` (Higgsfield; resolves to `nano_banana_2`)
- **settings:** `aspect_ratio: "16:9"`, `resolution: "1k"`, `count: 4`
- **cost:** 2 credits per image at 1k (video on `seedance_2_0` is 22.5 — preflight with `get_cost: true`)
- **reference:** the technique entry in `references.md`
- **outcome:** 4/4 usable on the first run. Cleared the bar that two hand-coded attempts (flat SVG,
  then a raymarched SDF) both missed — see the medium guardrail in `guardrails.md`.

```
Premium 3D product render, elevated three-quarter near-isometric view. Six chunky modular blocks
with softly rounded bevelled edges arranged in a closed hexagonal ring, interlocking so their sides
touch, surrounding one single taller block at the exact centre. The six ring blocks are matte dark
navy-black anodised metal, colour #101725, very low reflectivity, subtle fine micro-texture. The
centre block is polished brushed gold, colour #C4A44A, clearly taller than the ring blocks, catching
a warm specular highlight along its top bevel edge. Deep near-black background colour #080B12 with
soft radial falloff, no horizon line, no floor pattern. Lighting: large soft softbox key from upper
left, cool subtle rim light from behind, gentle realistic contact shadows and ambient occlusion in
the narrow gaps where the blocks meet. Redshift / Octane render quality, crisp bevel highlights,
physically accurate materials, studio product photography, extremely clean and premium, 8k detail.
IMPORTANT: every surface is completely blank and empty — absolutely no text, no letters, no numbers,
no words, no logos, no labels, no icons, no symbols, no engravings on any face.
```

### What makes it work

- **Name the material, not the look.** "Matte dark navy-black anodised metal, very low reflectivity"
  beats "premium dark blocks." Same for "polished brushed gold" — that's what produced real
  anisotropic streaking instead of flat yellow.
- **Specify the light rig explicitly.** Softbox key direction, rim light, contact shadows, ambient
  occlusion. This is the single biggest lever; without it you get flat studio nothing.
- **Name a renderer.** "Redshift / Octane render quality" reliably shifts output toward physically
  plausible materials.
- **Demand blank faces, emphatically and last.** Text is where image models fail hardest, and this
  concept depends on legible service names. Generating blank and compositing labels afterward in
  Figma or Canva keeps type crisp, editable, translatable, and readable by search engines. The long
  "no text, no letters, no numbers…" clause is doing real work — shorten it and lettering creeps back.
- **Hex codes land approximately.** Treat them as direction, not spec. Grade to exact brand values in
  post if the asset has to match a live page.

### Known deviations

The model produced 8 ring blocks rather than the 6 requested, and read "hexagonal ring" loosely.
Composition is good regardless, but exact counts and arrangements aren't reliable — art-direct by
choosing among generations rather than by tightening the count in the prompt.

---

## Isometric administration-building cutaway — hotspot walk plate

- **model:** `nano_banana_pro` (Higgsfield; resolves to `nano_banana_2`)
- **settings:** `aspect_ratio: "16:9"`, `count: 2`; then `upscale_image` (bytedance, 4k) → 4096×2294, saved at 2400 wide
- **outcome:** 2/2 usable on the first run. Variant A (flat vector, polished) shipped; variant B (thin-line illustration) is a valid alternative for a warmer, editorial theme.
- **used on:** Revolution Office, Home and Managed Print Services (`library/patterns/hotspot-walk/`)
- **file:** `library/office-technology/scenes/isometric-admin-building-cutaway-2400.jpg`

```
Isometric cutaway illustration of one floor of a modern school administration building, seen from
above at a 45 degree angle with the roof removed. Flat vector illustration style, clean geometry,
soft matte shading, no outlines, no gradients banding. Palette: warm cream floors and walls
(#F6F1E8), light oak desks, muted sage green and slate blue accents, warm amber (#E3A32B) used
sparingly on a few objects like chairs and a rug. Rooms arranged left to right: a copier room with
one large office multifunction printer; an open-plan office with eight desks where two desks each
have a small desktop printer; a supply closet with shelves stacked with small toner boxes; a front
office reception counter with a tray of papers; a small IT closet with a server rack and blinking
lights; a business office with a desk, a monitor and filing cabinets; and along the far side a
window wall looking out at a second smaller building across a courtyard with trees. Four simple
stylized people with no facial detail. Absolutely no text, no letters, no labels, no numbers, no
logos, no signage anywhere in the image. Even soft daylight with subtle long shadows. Wide
composition centered on a plain cream background with generous empty margins around the building.
```

### What makes it work

- **Rooms named in reading order** ("arranged left to right") so the markers have somewhere to land and the eye follows the sequence.
- **The client's palette by hex**, which keeps the plate inside the theme without a re-colour pass.
- **"No text" stated three ways.** The model still wanted signage on the copier room door in one early variant of a similar prompt.
- **A window onto a second building** gives the "every location" marker a place to sit without a second illustration.
