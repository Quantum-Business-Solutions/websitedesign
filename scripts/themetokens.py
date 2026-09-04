#!/usr/bin/env python3
"""Cache the nine themes' TRUE design tokens to themes/tokens.json.

Read-only. Run once, then mockups work with no portal access at all.

Why not read the [data-qdir] presets, which are all in every theme's stylesheet?
Because they're degraded: all nine presets carry only two heading faces (Plus Jakarta
Sans and Instrument Serif) instead of the nine the catalogue promises. Only each
theme's own NATIVE DIRECTION block has the real face -- Press's native block is
Playfair Display, its data-qdir preset says Instrument Serif. So we read the native
block from each theme, nine fetches, and cache the result.
"""
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reskin import (NINE, LIGHT_THEMES, SURFACE, read_source, parse_native,
                    verify_portal, contrast_ratio, HubSpotError)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "themes", "tokens.json")

# From themes/catalogue.md -- what each theme is for. Kept here so a mockup can
# print the rationale without reading markdown.
READS_AS = {
    "Quantum Flagship":  ("Established, expensive, confident",
                          "Top-end professional services; look like the incumbent"),
    "Quantum Void":      ("Sophisticated, restrained, brand-forward",
                          "Design-conscious buyers; elegance over energy"),
    "Quantum Signal":    ("Tech-forward but approachable",
                          "SaaS, product, AI -- friendly rather than austere"),
    "Quantum Converter": ("Technical, developer-credible",
                          "Platforms, data, infrastructure. Space Grotesk is on the watchlist"),
    "Quantum Clean":     ("Maximum clarity, zero personality",
                          "Broad or non-technical audiences; accessibility-first"),
    "Quantum Press":     ("Editorial, traditional-premium",
                          "Consultancies, law, finance, heritage brands"),
    "Quantum Paper":     ("Long-form, considered, literary",
                          "Content-heavy sites; thought leadership"),
    "Quantum Journal":   ("Journalistic, credible, text-forward",
                          "Research, reports, media, anything evidence-led"),
    "Quantum Showcase":  ("Contemporary creative, design-aware",
                          "Agencies, portfolios, creative services"),
}


def main():
    token = os.environ.get("QBS_HUBSPOT_TOKEN")
    if not token:
        raise SystemExit("Set $QBS_HUBSPOT_TOKEN")
    verify_portal(token)

    out = {"themes": {}}
    for t in NINE:
        try:
            css = read_source(f"{t}/css/quantum.css", token)
            nat = parse_native(css)
        except HubSpotError as e:
            print(f"  {t}: FAILED {e}", file=sys.stderr)
            continue
        reads, use = READS_AS.get(t, ("", ""))
        cta, acc = nat.get("--cta-fg", ""), nat.get("--q-gold", "")
        entry = {
            "ground": "light" if t in LIGHT_THEMES else "dark",
            "readsAs": reads,
            "reachForIt": use,
            "tokens": {k: nat.get(k) for k, _ in SURFACE if nat.get(k)},
        }
        if cta.startswith("#") and acc.startswith("#"):
            entry["ctaContrast"] = round(contrast_ratio(acc, cta), 2)
            entry["ctaPassesAA"] = entry["ctaContrast"] >= 4.5
        out["themes"][t] = entry
        flag = "" if entry.get("ctaPassesAA", True) else "  <-- FAILS WCAG AA"
        print(f"  {t:20} {entry['ground']:5} cta {entry.get('ctaContrast','?')}{flag}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"\nwrote {OUT} ({len(out['themes'])} themes)")


if __name__ == "__main__":
    main()
