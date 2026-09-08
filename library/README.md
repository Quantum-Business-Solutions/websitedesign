# Generated asset library

Renders, plates, cutouts and 3D models generated for client previews, kept here so the next client in the same vertical starts with a full set.
All of it is generated (Higgsfield, nano_banana_2 image model, image_to_3d with texture) and must be labelled as generated wherever it appears; nothing here is a photograph of a client's people or premises. Cutouts are transparent PNGs, 900px on the long side, trimmed. Plates are 2100 wide JPEG at 80. Scenes are 1200 wide JPEG. Models are textured GLB, about 4 to 6 MB.

Prompts follow one recipe: "Studio product photograph of [device], [materials], three-quarter front view from slightly above, soft even lighting, plain pure white background, no logos, no brand text, photorealistic", then remove_background, then _fitpng.mjs.

| Folder | What is in it | First used |
|---|---|---|
| office-technology/devices | Sharp-style A3 and A4 multifunction devices, desktop printer, wide format, production press, postage meter, water and coffee | Kelly Office Solutions, 2026-09 |
| office-technology/scenes | Office at dusk with copier room (hero plate), isometric office with seven lines, isometric administration-building cutaway for the hotspot walk (Revolution Office), technician, mailroom, break room, document management, IT and forensics scenes | Kelly Office Solutions |
| it-msp/devices | Switch stack with firewall, ceiling access point, conference video bar with display and controller, dome camera with access reader, portrait signage display, desktop firewall | Nexus Network Technologies, 2026-09 |
| it-msp/scenes | Office at dusk with glass conference room and network closet (hero plate), isometric office with eight systems, patch cables in a rack, empty conference room with NC pines, life sciences bench, warehouse floor | Nexus Network Technologies |
| logo-concepts/kelly | Six generated logo exploration concepts for Kelly (for discussion, not artwork) | Kelly Office Solutions |
| 3d | sharp-style-a3-mfp.glb, network-switch-stack.glb | Kelly, Nexus |

To add: copy the file in, name it by what it shows (not by client), add a row. Reuse across clients in the same vertical is expected; do not reuse a plate that shows a recognisable client-specific detail.

## Patterns as kits

`patterns/` holds shipped interactive sections as drop-in kits (module source, example data, previews) where the pattern needs more than a layout to reproduce. First entry: `patterns/hotspot-walk/` (the numbered-marker building map with a Before / After toggle, Revolution Office). The reasoning lives in `design/patterns.md`; the kit is what you copy.
