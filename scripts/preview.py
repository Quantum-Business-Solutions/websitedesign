#!/usr/bin/env python3
"""Render a client's site as three complete, clickable preview sites, one per direction.

    python3 scripts/preview.py --content brands/<slug>.content.json \
        --themes "Quantum Clean,Quantum Showcase,Quantum Press" --recommend "Quantum Clean" \
        --base-url https://<slug>.vercel.app --out /path/to/<client-repo>

For each theme this writes <out>/<direction>/<page>.html for every page in the content file,
plus <out>/index.html, a hub that opens each direction in its own tab. Every page carries the
theme's real css/quantum.css (from themes/source/, as patched by themefix.py) with the client's
accent derived onto it, the theme's own header and footer CSS, working navigation between
pages, a small direction switcher, noindex, canonical, Open Graph, and the fail-safe
Organization schema on the home page only.

Why this exists: a hero panel is a mood board. A buyer decides on a site they can click through
on their phone, in the direction's own typography and rhythm, with their logo in the header and
their locations on the locations page. Revolution's preview worked because every direction was
a usable site in its own tab. This is that, generated from one content file, for any client.

Rules it enforces (design/guardrails.md, process/quality-standard.md): no em dashes in output,
no text under 13px, tap targets 44px, no opacity-composited text, balanced card grids, one h1,
the client's Organization schema and nothing of ours.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reskin  # noqa: E402
import themefix  # noqa: E402
from preview_hub import hub  # noqa: E402
import preview_sections  # noqa: E402
import preview_modules  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASH_HITS: list[str] = []


def E(s) -> str:
    s = "" if s is None else str(s)
    if "—" in s or "–" in s:
        DASH_HITS.append(s[:70])
        s = re.sub(r"\s*[—–]\s*", ", ", s)
    return html.escape(s, quote=True)


def RAW(s) -> str:
    """Trusted inline markup from the content file (an <em> in a heading). Still no dashes."""
    s = "" if s is None else str(s)
    if "—" in s or "–" in s:
        DASH_HITS.append(s[:70])
        s = re.sub(r"\s*[—–]\s*", ", ", s)
    return s


def slug_of(theme: str) -> str:
    return theme.replace("Quantum ", "").lower()


def cols_for(n: int) -> int:
    """Column count that never leaves an orphan (design/guardrails.md)."""
    if n <= 1:
        return 1
    if n in (2, 4):
        return 2 if n == 2 else 4
    if n % 3 == 0:
        return 3
    if n == 5:
        return 5
    if n % 4 == 0:
        return 4
    if n % 2 == 0:
        return 2
    return 3  # 7, 11: caller should prefer a list


# ------------------------------------------------------------------------------ tokens

def client_tokens(theme: str, brand: dict) -> tuple[str, dict]:
    css_path = os.path.join(reskin.SOURCE_DIR, theme, "css", "quantum.css")
    css = open(css_path, encoding="utf-8").read().replace("\u2014", "-")
    native = reskin.parse_native(css)
    ground = "dark" if reskin.relative_luminance(native["--bg"]) < 0.18 else "light"
    d = reskin.derive_native(brand["accent"], ground)
    # Accent text must clear 4.5 on the section ground AND the alternate band; derive against the darker.
    _alt = native.get("--bg-alt", native["--bg"])
    _darker = _alt if reskin.relative_luminance(_alt) < reskin.relative_luminance(native["--bg"]) else native["--bg"]
    ink = reskin.darken_until(brand["accent"], _darker)
    lift = brand["accent"] if ground == "dark" else reskin.darken_until(brand["accent"], native.get("--bg-alt", native["--bg"]))
    sec = brand.get("ink_secondary")
    cta_fg = sec if sec and reskin.contrast_ratio(sec, brand["accent"]) >= 4.5 else reskin.best_on(brand["accent"])
    tok = {
        "--q-gold": brand["accent"].lower(), "--q-gold-bright": d["--q-gold-bright"], "--q-gold-dim": d["--q-gold-dim"],
        "--accent": "var(--q-gold)", "--accent-ink": ink, "--accent-lift": lift, "--cta-fg": cta_fg,
        "--border": d["--border"] if ground == "light" else native.get("--border", d["--border"]),
    }
    # Typefaces: a brand may borrow another direction's type ("type_from": {"Quantum Showcase": "Quantum Clean"}),
    # keeping this direction's geometry and motion but setting headings and body in the other direction's faces.
    type_src = native
    borrowed = (brand.get("type_from") or {}).get(theme)
    if borrowed:
        b_css = open(os.path.join(reskin.SOURCE_DIR, borrowed, "css", "quantum.css"), encoding="utf-8").read().replace("\u2014", "-")
        type_src = reskin.parse_native(b_css)
        imports = re.findall(r"@import url\([^)]*\);?", b_css)
        css = "".join(i if i.endswith(";") else i + ";" for i in imports) + "\n" + css
    for key in ("--q-serif", "--q-sans"):
        face = (type_src.get(key) or "").split(",")[0].strip().strip("'\"").lower()
        if face in FALLBACKS:
            tok[key] = FALLBACKS[face]
        elif borrowed and type_src.get(key):
            tok[key] = type_src[key]
    chrome_bg = brand.get("chrome_bg") if brand.get("chrome") == "dark" else native["--bg"]
    tok["--chrome-bg"] = chrome_bg
    tok["--chrome-fg"] = reskin.best_on(chrome_bg)
    tok["--chrome-muted"] = "rgba(255,255,255,.72)" if tok["--chrome-fg"].lower().startswith("#f") else "rgba(0,0,0,.62)"
    tok["--chrome-border"] = "rgba(255,255,255,.12)" if tok["--chrome-fg"].lower().startswith("#f") else "rgba(0,0,0,.1)"
    tok["--chrome-accent"] = brand["accent"].lower() if tok["--chrome-fg"].lower().startswith("#f") else ink
    return css, tok


# Each direction owns its geometry AND its components, or three directions are one page recoloured
# (themes/architecture.md item 2; the first Kelly QA pass said exactly that about Showcase).
DIRECTION_CSS = {
    "clean": r'''
/* Clean: the control. Humanist sans, bordered cards, 6px buttons, image right. */
.q-h1{font-weight:700;font-size:clamp(40px,4.5vw,66px)}
''',
    "showcase": r'''
/* Showcase: display grotesque at weight 800, pill buttons, floating cards, image LEFT, bigger stats. */
.q-h1,.q-h2,.pv-svc h3,.pv-cs .h,.pv-grid .q-card h3,.pv-loc .q-card h3,.pv-post h2,.pv-stage h3{font-weight:800;letter-spacing:-.03em}
.q-h1{font-size:clamp(40px,4.6vw,68px);line-height:.98}
.q-btn,.q-form .hs-button,.q-header .q-booknow,.q-mnav-cta{border-radius:999px}
.q-card{border:0;box-shadow:0 14px 36px rgba(0,5,69,.08);border-radius:var(--radius)}
.pv-band .q-card{border:1px solid var(--chrome-border);box-shadow:none}
.pv-hero-grid > div:first-child{order:2}
.pv-hero-img{border-radius:28px;border:0;box-shadow:0 30px 70px rgba(0,5,69,.14)}
.pv-badge{border-radius:999px;padding:14px 22px;border:0;box-shadow:0 10px 30px rgba(0,0,0,.12)}
.pv-stat b{font-size:76px;font-weight:800;letter-spacing:-.03em}
.pv-stats{gap:12px}.pv-stat{background:var(--card);border-radius:var(--radius);padding:28px 20px;box-shadow:0 10px 30px rgba(0,5,69,.06)}.pv-stat + .pv-stat{border-left:0}
.q-eyebrow{letter-spacing:.2em;font-weight:700}
.q-eyebrow::before{width:10px;height:10px;border-radius:50%}
.pv-svc a{border-top:0;background:var(--card);border-radius:var(--radius);margin-bottom:12px;padding:26px 24px;box-shadow:0 8px 24px rgba(0,5,69,.05)}
.pv-svc a:last-child{border-bottom:0}
.pv-svc .num{display:none}.pv-svc a{grid-template-columns:1fr 130px}
.q-stagenum{width:56px;height:56px;border:0;background:var(--q-gold);color:var(--cta-fg);font-family:var(--q-sans);font-weight:800}
.pv-quote{border-left:0;padding-left:0;font-size:28px;font-weight:600}
.pv-detail-img{border:0;box-shadow:0 20px 50px rgba(0,5,69,.12);border-radius:24px}
@media(max-width:767px){.pv-hero-grid > div:first-child{order:0}.q-h1{font-size:40px}.pv-stat b{font-size:48px}}
''',
    "press": r'''
.pv-logos{flex-wrap:wrap;justify-content:center;mask-image:none;-webkit-mask-image:none;gap:28px 48px}.pv-logos-track{animation:none;flex-wrap:wrap;justify-content:center;gap:28px 48px}.pv-logos-track[aria-hidden]{display:none}
/* Press: editorial. Serif reaches past the headline; hairline rules; plates around photographs; 2px corners; folios. */
.q-lead,.pv-quote,.pv-cs .h,.pv-stat b,.pv-badge b,.pv-metric .v,.pv-svc h3,.pv-post h2,.pv-grid .q-card h3,.pv-loc .q-card h3,.pv-stage h3,.pv-faq summary{font-family:var(--q-serif)}
.q-lead{font-size:21px;line-height:1.55}
.q-h1{font-weight:500;letter-spacing:-.015em}
.q-h2{font-weight:500}
.q-btn,.q-btn-ghost,.q-form input,.q-form select,.q-form textarea,.q-form .hs-button,.q-card,.pv-detail-img,.pv-hero-img,.pv-hero-wide{border-radius:2px}
.q-header .q-booknow,.q-mnav-cta{border-radius:2px}
.q-eyebrow{font-family:var(--q-sans);font-size:13px;letter-spacing:.22em;font-weight:600}
.q-eyebrow::before{width:40px;background:var(--fg)}
.pv-hero-img,.pv-detail-img,.pv-hero-wide{border:1px solid var(--fg);padding:10px;background:var(--card);box-sizing:border-box}
.pv-hero-img img,.pv-detail-img img,.pv-hero-wide img{border-radius:0}
.pv-badge{border-radius:0;border:1px solid var(--fg);box-shadow:none;left:auto;right:-14px;bottom:-14px}
.q-section{border-bottom:1px solid var(--border)}
.pv-svc a{grid-template-columns:64px 1fr 130px;padding:22px 0}
.pv-svc .num{width:auto;height:auto;border-radius:0;background:none;margin:0;font-family:var(--q-serif);font-size:22px;color:var(--fg-muted);font-style:italic}
.pv-svc .num::after{content:attr(data-folio)}
.pv-svc .more{font-family:var(--q-sans);letter-spacing:.14em}
.q-card{background:transparent;border:1px solid var(--border);border-top:2px solid var(--fg)}
.pv-band .q-card{background:rgba(255,255,255,.06);border-top:2px solid var(--chrome-accent)}
.q-stagenum{border-radius:0;border:1px solid var(--fg);font-style:italic}
.pv-stat b{font-weight:500}
.pv-quote{font-style:italic;border-left:0;padding-left:0;font-size:26px}
.pv-quote::before{content:"\201C";display:block;font-size:64px;line-height:.6;color:var(--accent-ink);margin-bottom:10px}
@media(max-width:767px){.pv-badge{right:10px;bottom:10px}}
''',
}

FALLBACKS = {"open sans": "'Open Sans',Arial,'Helvetica Neue',sans-serif",
             "bricolage grotesque": "'Bricolage Grotesque','Arial Black','Helvetica Neue',Arial,sans-serif",
             "playfair display": "'Playfair Display',Georgia,'Times New Roman',serif",
             "inter": "'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif"}

PREVIEW_CSS = r'''
/* ===== preview layer: page grammar the modules would supply in HubSpot ===== */
*{box-sizing:border-box}
html{scroll-padding-top:130px}
@media(max-width:767px){html{scroll-padding-top:92px}}
img{max-width:100%;height:auto}
.embedded .pv-switch,.embedded .pv-util{display:none}
.q-skip{position:absolute;top:-200px;left:8px;z-index:100;background:var(--q-gold);color:var(--cta-fg);padding:10px 16px;border-radius:6px;font-weight:600}
.q-skip:focus{top:8px}
h1,h2,h3{text-wrap:balance}
.q-eyebrow{font-size:13px}
.q-btn,.q-btn-ghost{min-height:44px}
.q-btn-ghost{padding:10px 0}
/* utility bar */
.pv-util{background:var(--chrome-bg);border-bottom:1px solid var(--chrome-border)}
.pv-util .q-container{display:flex;gap:6px 22px;justify-content:flex-end;flex-wrap:wrap;font-size:13px;padding-top:2px;padding-bottom:2px}
.pv-util a{color:var(--chrome-muted);text-decoration:none;display:inline-flex;align-items:center;min-height:44px;padding:0 2px}
.pv-util a:hover{color:var(--chrome-fg)}
.pv-util a.pv-phone{color:var(--chrome-fg);font-weight:600}
/* header on chrome */
.q-header{background:var(--chrome-bg);border-bottom:1px solid var(--chrome-border);display:block}
.q-header .q-header-in{position:relative}
.q-header .q-nav > a,.q-header .q-nav-item > a{color:var(--chrome-fg)}
.q-header .q-nav > a:hover{color:var(--chrome-accent)}
.q-header .q-booknow{background:var(--q-gold);color:var(--cta-fg)!important;border-color:var(--q-gold);min-height:44px;display:inline-flex;align-items:center}
.q-header .q-booknow:hover{background:var(--q-gold-bright)}
.q-header-logo img{height:48px;width:auto}
@media(max-width:767px){.q-header{position:sticky;top:0;z-index:60}.pv-util{display:none}.q-header-logo img{height:40px}}
.q-logo-text{color:var(--chrome-fg)}
.q-mnav > summary{border-color:var(--chrome-border)!important}
.q-mnav > summary span{background:var(--chrome-fg)!important}
.q-mnav-panel{background:var(--chrome-bg)!important;border-top-color:var(--chrome-border)!important}
.q-mnav-panel > a,.q-msub > summary{color:var(--chrome-fg)!important;border-bottom-color:var(--chrome-border)!important}
.q-msub-links a{color:var(--chrome-muted)!important}
.q-mnav-cta{color:var(--cta-fg)!important;background:var(--q-gold);border-color:var(--q-gold)!important}
/* hero proof strip and ribbon */
.pv-hero-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:0;margin-top:56px;border-top:1px solid var(--border)}
.pv-hero-stats > div{padding:22px 24px 0 0;border-left:1px solid var(--border);padding-left:24px}.pv-hero-stats > div:first-child{border-left:0;padding-left:0}
.pv-hero-stats b{display:block;font-family:var(--q-serif);font-size:40px;line-height:1;font-weight:800;letter-spacing:-.03em;color:var(--accent-ink)}
.pv-hero-stats span{display:block;margin-top:8px;font-size:13px;line-height:1.45;color:var(--fg-muted)}
.pv-ribbon{background:var(--chrome-bg);color:var(--chrome-fg)}
.pv-ribbon .q-container{display:flex;flex-wrap:wrap;gap:10px 36px;align-items:center;min-height:56px;padding-top:12px;padding-bottom:12px;font-size:14px}
.pv-ribbon span{display:inline-flex;align-items:center;gap:10px}.pv-ribbon span::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--q-gold)}
/* proof numeral */
.pv-proof{text-align:center}.pv-proof b{display:block;font-family:var(--q-serif);font-size:clamp(96px,14vw,200px);line-height:.95;font-weight:800;letter-spacing:-.04em;color:var(--accent-ink)}
.pv-proof .q-lead{max-width:640px;margin:22px auto 0}.pv-proof .src{margin-top:14px;font-size:13.5px;color:var(--fg-muted)}
/* service-area map */
.pv-map-wrap{display:grid;grid-template-columns:1.2fr 1fr;gap:48px;align-items:center}
.pv-map-svg{width:100%;height:auto;display:block}
.pv-map-svg .land{fill:var(--bg-alt);stroke:var(--fg);stroke-width:1.2;stroke-linejoin:round}
.pv-map-svg .ring{fill:var(--q-gold);fill-opacity:.12;stroke:var(--accent-ink);stroke-dasharray:3 3;stroke-width:.8}
.pv-map-svg .pin{fill:var(--accent-ink);stroke:#fff;stroke-width:1.5}.pv-map-svg .pin.hq{fill:var(--chrome-bg)}
.pv-map-svg text{font:600 11px/1 var(--q-sans);fill:var(--fg)}
.pv-map-list{list-style:none;margin:0;padding:0;display:grid;gap:0}
.pv-map-list li{display:grid;grid-template-columns:1fr auto;gap:8px 18px;padding:14px 0;border-top:1px solid var(--border);align-items:baseline}
.pv-map-list li:last-child{border-bottom:1px solid var(--border)}
.pv-map-list b{font-weight:600;color:var(--fg)}.pv-map-list small{display:block;color:var(--fg-muted);font-size:13.5px;margin-top:2px}
.pv-map-list a{white-space:nowrap;font-weight:600;color:var(--accent-ink)}
@media(max-width:1024px){.pv-map-wrap{grid-template-columns:1fr;gap:28px}}
/* header collapse */
.q-header .pv-util{transition:max-height .25s ease,opacity .2s ease;max-height:60px;overflow:hidden}
.q-header.is-scrolled .pv-util{max-height:0;opacity:0}
.pv-grid-5 .q-card h3{min-height:2.6em}
/* dropdowns, mega menu, breadcrumbs */
@media(min-width:1025px){.q-footer-grid.pv-fcols-4{grid-template-columns:1.4fr repeat(4,1fr)}.q-footer-grid.pv-fcols-5{grid-template-columns:1.3fr repeat(5,1fr)}}
@media(min-width:768px) and (max-width:1024px){.q-footer-grid.pv-fcols-4,.q-footer-grid.pv-fcols-5{grid-template-columns:repeat(4,1fr)}.q-footer-grid.pv-fcols-4 > div:first-child,.q-footer-grid.pv-fcols-5 > div:first-child{grid-column:1/-1}}
.q-mnav:not([open]) .q-mnav-panel{display:none}
.pv-sticky.pv-sticky-off{opacity:0;pointer-events:none;transform:translateY(12px)}.pv-sticky{transition:opacity .2s,transform .2s}
html{scroll-padding-bottom:72px}
.pv-logos{position:relative}
.pv-cmp{position:relative;mask-image:linear-gradient(90deg,#000 88%,transparent);-webkit-mask-image:linear-gradient(90deg,#000 88%,transparent)}
.pv-cmp table td:first-child,.pv-cmp table th:first-child{position:sticky;left:0;background:var(--bg);z-index:1}
.pv-cmp-hint{display:none;font-size:13.5px;color:var(--fg-muted);margin:8px 0 0}
@media(max-width:767px){.pv-cmp-hint{display:block}}
@media(min-width:1200px){.pv-res.pv-res-5{grid-template-columns:repeat(5,1fr)!important}}
@media(max-width:480px){.pv-grid-4{grid-template-columns:1fr!important}}
.q-msub > summary{white-space:normal}
.q-header .q-nav > a[aria-current],.q-header .q-nav-item > a[aria-current]{color:var(--q-gold)}
.q-header .q-nav > a,.q-header .q-nav-item > a{position:relative}
.q-header .q-nav > a[aria-current]::after,.q-header .q-nav-item > a[aria-current]::after{content:"";position:absolute;left:0;right:0;bottom:22px;height:2px;background:var(--q-gold);border-radius:2px}
.q-subnav{padding:10px 0;border-radius:12px;box-shadow:0 24px 60px rgba(0,0,0,.22);z-index:80}
.q-subnav a{padding:10px 22px;font-size:15px}
.q-nav-item.pv-has-mega{position:static}
.pv-mega{left:50%;transform:translate(-50%,6px);width:min(1180px,calc(100vw - 32px));padding:0;overflow:hidden}
.q-nav-item:hover .pv-mega,.q-nav-item:focus-within .pv-mega{transform:translate(-50%,0)}
.pv-mega-in{display:grid;grid-template-columns:repeat(4,minmax(0,1fr)) minmax(0,1.2fr);gap:0}
.pv-mega .col{padding:26px 22px 22px;border-right:1px solid var(--border)}
.pv-mega .gt{font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--accent-ink);margin:0 0 10px;line-height:1.3}
.pv-mega .feat .q-eyebrow{white-space:normal;line-height:1.3}
.menu-open .pv-sticky,.menu-open .pv-switch-m{display:none!important}
.pv-mega .col a{display:block;padding:8px 0;font-size:15px;white-space:normal;color:var(--fg);border-radius:0}
.pv-mega .col a:hover{background:none;color:var(--accent-ink);text-decoration:underline;text-underline-offset:3px}
.pv-mega .feat{display:flex;flex-direction:column;gap:8px;min-width:0;padding:26px 26px 22px;background:var(--bg-alt);color:var(--fg);white-space:normal}
.pv-mega .feat b{font-size:20px;line-height:1.2;font-weight:700;letter-spacing:-.01em}
.pv-mega .feat p{margin:0;color:var(--fg-muted);font-size:14.5px;line-height:1.55}
.pv-mega .feat .more{color:var(--accent-ink);font-weight:600;font-size:14px;margin-top:auto}
.pv-mega .feat:hover{background:var(--bg-alt)}.pv-mega .feat:hover b{color:var(--accent-ink)}
.pv-mega-foot{border-top:1px solid var(--border);padding:12px 26px;background:var(--bg)}
.pv-mega-foot a{display:inline;padding:0;font-weight:600;color:var(--accent-ink);font-size:14px}
.pv-mgt{font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--chrome-muted);padding:14px 14px 4px}
.pv-mall{font-weight:600}
.pv-crumbs{border-bottom:1px solid var(--border);background:var(--bg)}
.pv-crumbs ol{list-style:none;margin:0;padding:12px 0;display:flex;flex-wrap:wrap;gap:6px 10px;font-size:14px;color:var(--fg-muted)}
.pv-crumbs li + li::before{content:"/";margin-right:10px;color:var(--border)}
.pv-crumbs a{color:var(--fg-muted);text-decoration:none;min-height:24px;display:inline-flex;align-items:center}.pv-crumbs a:hover{color:var(--accent-ink);text-decoration:underline}
.pv-crumbs [aria-current]{color:var(--fg)}
.q-msub-links a,.q-mnav-panel > a{color:var(--chrome-fg)!important}
.q-msub > summary .q-caret{border-color:var(--q-gold)!important}
/* footer on chrome */
.q-footer{background:var(--chrome-bg);border-top:1px solid var(--chrome-border);color:var(--chrome-fg)}
.q-footer-grid{grid-template-columns:1.6fr 1fr 1fr 1fr}
.q-footer-tag,.q-footer-contact,.q-footer-contact a,.q-footer-links a,.q-footer-legal,.q-footer-legal a,.q-footer-social a{color:var(--chrome-muted)}
.q-footer-head,.q-footer-contact .q-footer-phone{color:var(--chrome-fg)}
.q-footer-links a:hover,.q-footer-social a:hover{color:var(--chrome-accent)}
.q-footer-links a{min-height:44px;display:flex;align-items:center;padding:0}
.q-footer-links{gap:0}
.pv-legal-item{display:inline-flex;align-items:center;white-space:nowrap}.pv-legal-item + .pv-legal-item::before{content:"|";margin:0 10px;color:var(--chrome-muted)}
.q-header-logo{min-height:44px;display:inline-flex;align-items:center}
.q-footer-legal{border-top-color:var(--chrome-border)}
.q-footer-legal a{display:inline-flex;align-items:center;min-height:44px;padding:0 6px}
.q-footer-social a{margin:0;width:auto;min-width:44px;height:44px;padding:0 10px}
.q-footer-contact a{display:inline-flex;align-items:center;min-height:44px}.q-footer-contact br{display:block;content:""}
.q-footer img{height:36px}
@media(max-width:1024px){.q-footer-grid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.q-footer-grid{grid-template-columns:1fr}}
/* hero */
.pv-hero-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:56px;align-items:center}
.pv-hero-img{width:100%;aspect-ratio:3/2;border-radius:calc(var(--radius) + 6px);overflow:hidden;border:1px solid var(--border);background:var(--bg-alt);position:relative}
.pv-hero-img img{width:100%;height:100%;object-fit:cover;object-position:22% 50%;display:block}
.q-h1{max-width:16ch}
.pv-badge{position:absolute;left:20px;bottom:20px;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:14px 18px;box-shadow:0 10px 30px rgba(0,0,0,.08)}
.pv-badge b{display:block;font-family:var(--q-serif);font-size:30px;line-height:1;color:var(--accent-ink)}
.pv-badge span{font-size:13px;color:var(--fg-muted)}
.pv-hero-note{margin-top:28px;font-size:13.5px;color:var(--fg-muted)}
.pv-hero-wide{margin:48px auto 0;max-width:1000px;aspect-ratio:16/9;border-radius:calc(var(--radius) + 6px);overflow:hidden;border:1px solid var(--border);background:var(--bg-alt)}
.pv-hero-wide img{width:100%;height:100%;object-fit:cover;display:block}
.pv-btns{display:flex;gap:16px;margin-top:36px;flex-wrap:wrap;align-items:center}
.q-h1 em{font-style:normal;color:var(--accent-ink)}
/* partners */
.pv-partners{padding:8px 0 70px}
.pv-partners .q-container{padding-top:36px;border-top:1px solid var(--border)}
.pv-cap{font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--fg-muted);text-align:center;margin:0 0 22px}
.pv-logos{display:flex;overflow:hidden;gap:64px;mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.pv-logos-track{display:flex;align-items:center;gap:64px;flex:none;animation:pv-marquee 46s linear infinite}.pv-logos:hover .pv-logos-track{animation-play-state:paused}
@keyframes pv-marquee{to{transform:translateX(calc(-100% - 64px))}}
@media(prefers-reduced-motion:reduce){.pv-logos{flex-wrap:wrap;justify-content:center;mask-image:none;-webkit-mask-image:none}.pv-logos-track{animation:none;flex-wrap:wrap;justify-content:center}.pv-logos-track[aria-hidden]{display:none}}
.pv-logos img{width:auto;max-width:170px;height:56px;object-fit:contain;mix-blend-mode:multiply;filter:grayscale(1) opacity(.82);transition:filter .2s}
.pv-logos img:hover{filter:none}
@media(max-width:767px){.pv-logos,.pv-logos-track{gap:40px}.pv-logos img{height:44px;max-width:130px}@keyframes pv-marquee{to{transform:translateX(calc(-100% - 40px))}}}
.pv-logos span{font-family:var(--q-serif);font-size:20px;color:var(--fg-muted)}
/* stats */
.pv-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:0}
.pv-stat{padding:0 28px;text-align:center}
.pv-stat b{display:block;font-family:var(--q-serif);font-size:60px;line-height:1;color:var(--accent-ink)}
.pv-stat span{display:block;font-size:14px;color:var(--fg-muted);margin-top:12px}
.pv-stat + .pv-stat{border-left:1px solid var(--border)}
/* services list */
.pv-split{display:flex;justify-content:space-between;align-items:flex-end;gap:40px;flex-wrap:wrap;margin-bottom:40px}
.pv-split .q-h2{max-width:560px}
.pv-split p{font-size:16px;line-height:1.65;color:var(--fg-muted);max-width:360px;margin:0}
.pv-svc a{display:grid;grid-template-columns:28px 1fr 130px;gap:32px;align-items:center;padding:26px 8px;border-top:1px solid var(--border);color:inherit;text-decoration:none;min-height:44px}
.pv-svc a:last-child{border-bottom:1px solid var(--border)}
.pv-svc a:hover h3{color:var(--accent-ink)}
.pv-svc .num{width:10px;height:10px;border-radius:50%;background:var(--q-gold);margin-top:8px}
.pv-svc h3{font-family:var(--q-serif);font-size:22px;font-weight:600;color:var(--fg);margin:0 0 6px}
.pv-svc p{font-size:15px;color:var(--fg-muted);margin:0;line-height:1.6}
.pv-svc .more{justify-self:end;font-size:13px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--accent-ink)}
/* process */
.pv-center{text-align:center;display:flex;flex-direction:column;align-items:center}
.pv-stage h3{font-family:var(--q-serif);font-size:17px;font-weight:600;color:var(--fg);margin:20px 0 8px}
.pv-stage p{font-size:14px;line-height:1.6;color:var(--fg-muted);margin:0;max-width:200px}
/* case study */
.pv-cs{display:grid;grid-template-columns:.9fr 1.1fr;gap:64px;align-items:center}
.pv-cs .h{font-family:var(--q-serif);font-size:40px;line-height:1.1;color:var(--fg);margin:18px 0 0}
.pv-quote{border-left:3px solid var(--q-gold);padding-left:22px;font-family:var(--q-serif);font-size:23px;line-height:1.45;color:var(--fg);margin:24px 0 0}
.pv-attr{font-size:14px;color:var(--fg-muted);margin-top:18px}
.pv-metric .k{font-size:13px;text-transform:uppercase;letter-spacing:.12em;color:var(--fg-muted)}
.pv-metric .v{font-family:var(--q-serif);font-size:34px;color:var(--accent-ink);margin-top:8px}
.pv-metric .d{font-size:14px;color:var(--fg-muted);margin-top:6px}
/* cards */
.pv-grid{display:grid;gap:20px}
.pv-grid-2{grid-template-columns:repeat(2,1fr)}.pv-grid-3{grid-template-columns:repeat(3,1fr)}.pv-grid-4{grid-template-columns:repeat(4,1fr)}.pv-grid-5{grid-template-columns:repeat(5,1fr)}
.pv-grid .q-card h3{font-family:var(--q-serif);font-size:22px;margin:0 0 10px;font-weight:600;color:var(--fg)}
.pv-grid .q-card p{font-size:15px;line-height:1.7;color:var(--fg-muted);margin:0}
.pv-grid .q-card a{color:var(--fg);font-weight:600;text-decoration:none;display:inline-flex;align-items:center;min-height:44px}
/* band */
.pv-band{background:var(--chrome-bg);color:var(--chrome-fg)}
.pv-band .q-h2{color:var(--chrome-fg)}
.pv-band .q-lead{color:var(--chrome-muted)}
.pv-band .q-eyebrow{color:var(--chrome-accent)}
.pv-band .q-eyebrow::before{background:var(--chrome-accent)}
.pv-band .q-card{background:rgba(255,255,255,.06);border-color:var(--chrome-border);color:var(--chrome-fg);text-decoration:none;display:block}
.pv-band .q-card:hover{border-color:var(--chrome-accent)}
.pv-band .q-card .t{font-family:var(--q-serif);font-size:20px;font-weight:600}
.pv-band .q-card .d{font-size:14px;color:var(--chrome-muted);margin-top:6px}
/* locations */
.pv-loc .q-card h3{font-family:var(--q-serif);font-size:20px;margin:0 0 8px;font-weight:600}
.pv-loc .q-card p{font-size:14.5px;line-height:1.7;color:var(--fg-muted);margin:0}.pv-loc .q-card{display:flex;flex-direction:column}.pv-loc .q-card p{display:flex;flex-direction:column;flex:1}.pv-loc .q-card p a{margin-top:auto;padding-top:8px;font-weight:600;color:var(--fg)}.pv-loc .q-card p br{display:none}
.pv-map{aspect-ratio:16/9;border-radius:var(--radius);background:linear-gradient(135deg,var(--bg-alt),var(--card));border:1px solid var(--border);display:flex;align-items:center;justify-content:center;color:var(--fg-muted);font-size:13px;margin-bottom:14px}
/* faq */
.pv-faq details{border-top:1px solid var(--border);padding:18px 0}
.pv-faq details:last-child{border-bottom:1px solid var(--border)}
.pv-faq summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:16px;font-family:var(--q-serif);font-size:20px;color:var(--fg);font-weight:500;min-height:44px}
.pv-faq summary::-webkit-details-marker{display:none}
.pv-faq summary span{color:var(--accent-ink);font-size:24px;transition:transform .2s}
.pv-faq details[open] summary span{transform:rotate(45deg)}
.pv-faq p{font-size:15px;line-height:1.7;color:var(--fg-muted);margin:14px 0 0;max-width:720px}
/* contact + forms */
.pv-contact{display:grid;grid-template-columns:.9fr 1.1fr;gap:64px;align-items:start}
.q-form{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:32px}
.q-form label{display:block;font-size:13px;color:var(--fg-muted);margin:0 0 6px}
.q-form input[type=text],.q-form input[type=email],.q-form input[type=tel],.q-form input[type=url],.q-form select,.q-form textarea,.q-form input[type=submit],.q-form .hs-button{font-size:16px;min-height:44px}
.q-form .hs-button{min-height:48px;font-size:16px;width:100%}
.pv-form-note{font-size:13px;color:var(--fg-muted);margin:12px 0 0}
/* detail */
.pv-detail{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:start}
.pv-detail .q-h2{margin-top:14px}
.pv-detail ul{margin:22px 0 0;padding-left:20px;color:var(--fg);line-height:1.8;font-size:16px}
.pv-detail > div:last-child > ul:first-child{margin-top:38px}
.pv-detail ul li::marker{color:var(--accent-ink)}
.pv-detail .q-lead{margin-top:18px}
.pv-detail-img{aspect-ratio:3/2;border-radius:var(--radius);overflow:hidden;border:1px solid var(--border);background:var(--bg-alt);margin-bottom:18px}
.pv-detail-img img{width:100%;height:100%;object-fit:cover;display:block}
.pv-flip > div:first-child{order:2}
/* listing */
.pv-post{display:flex;flex-direction:column;gap:10px;text-decoration:none;color:inherit}
.pv-post .tag{font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--accent-ink)}
.pv-post h2{font-family:var(--q-serif);font-size:22px;margin:0;font-weight:600;color:var(--fg);line-height:1.25}
.pv-post p{font-size:15px;line-height:1.65;color:var(--fg-muted);margin:0}
.pv-post .rt{font-size:13px;color:var(--fg-muted)}
.pv-post .ph{aspect-ratio:16/9;border-radius:var(--radius);background:linear-gradient(135deg,var(--bg-alt),var(--card));border:1px solid var(--border)}
/* team */
.pv-team .q-card .av{aspect-ratio:1;border-radius:50%;width:96px;background:linear-gradient(135deg,var(--bg-alt),var(--border));margin:0 0 16px}
/* cta */
.pv-cta{text-align:center}
.pv-cta .q-container{max-width:820px}
/* direction switcher */
.pv-switch{position:fixed;right:14px;bottom:14px;z-index:90;display:flex;gap:4px;align-items:center;background:rgba(20,23,28,.94);color:#fff;border-radius:999px;padding:6px 8px 6px 14px;font:13px/1 Inter,system-ui,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.25);backdrop-filter:blur(6px);white-space:nowrap}
.pv-switch .lbl{opacity:.7;margin-right:6px}
.pv-switch a{color:#fff;text-decoration:none;padding:10px 12px;border-radius:999px;min-height:36px;display:inline-flex;align-items:center;white-space:nowrap}
.pv-switch a[aria-current]{background:rgba(255,255,255,.18);box-shadow:inset 0 0 0 1px rgba(255,255,255,.35)}
.pv-switch a:hover{background:rgba(255,255,255,.1)}
.pv-switch-m{display:none}
@media(max-width:767px){
  .pv-switch{display:none}
  .pv-switch-m{display:block;position:fixed;right:10px;bottom:70px;z-index:90;font:13px/1 Inter,system-ui,sans-serif}
  .pv-switch-m summary{list-style:none;cursor:pointer;background:rgba(20,23,28,.94);color:#fff;border-radius:999px;padding:12px 16px;min-height:44px;display:inline-flex;align-items:center;gap:8px;box-shadow:0 10px 30px rgba(0,0,0,.25)}
  .pv-switch-m summary::-webkit-details-marker{display:none}
  .pv-switch-m[open] summary{border-radius:14px 14px 0 0}
  .pv-switch-m .menu{position:absolute;right:0;bottom:100%;margin-bottom:6px;background:rgba(20,23,28,.96);border-radius:14px;padding:6px;display:flex;flex-direction:column;min-width:236px;white-space:nowrap;box-shadow:0 10px 30px rgba(0,0,0,.3)}
  .pv-switch-m .menu a{color:#fff;text-decoration:none;padding:12px 14px;border-radius:10px;min-height:44px;display:flex;align-items:center}
  .pv-switch-m .menu a[aria-current]{background:rgba(255,255,255,.18)}
}
/* responsive */
@media(max-width:1024px){.pv-hero-grid{grid-template-columns:1fr}.pv-cs,.pv-contact,.pv-detail{grid-template-columns:1fr;gap:34px}.pv-grid-4{grid-template-columns:repeat(2,1fr)}.pv-grid-5{grid-template-columns:repeat(5,1fr);gap:12px}.pv-stats{grid-template-columns:repeat(2,1fr);gap:28px 0}.pv-stat:nth-child(3){border-left:none}}
@media(max-width:767px){
  .q-section{padding:56px 0}
  .q-h1{max-width:none}
  .pv-util .q-container{justify-content:flex-start}
  .pv-grid-2,.pv-grid-3,.pv-grid-4,.pv-grid-5{grid-template-columns:1fr}
  .pv-svc a{grid-template-columns:1fr;gap:8px;padding:20px 0}.pv-svc .num{display:none}.pv-svc .more{justify-self:start}
  .pv-stats{grid-template-columns:1fr 1fr}.pv-stat b{font-size:42px}
  .pv-cs .h{font-size:30px}.pv-quote{font-size:19px}
  .pv-switch{bottom:8px;padding:4px 6px 4px 10px;font-size:12.5px;max-width:calc(100vw - 16px)}.pv-switch .lbl{display:none}
}
'''


PREVIEW_JS = r"""
(function(){
var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
/* count-up on stat numbers */
var stats=[].filter.call(document.querySelectorAll('.pv-stat b,.pv-hero-stats b,.pv-proof b'),function(b){if(b.hasAttribute('data-static'))return false;var t=b.textContent.trim().replace(/,/g,''),n=parseFloat(t);return !isNaN(n)&&n>=100&&!(t.length===4&&n>1800&&n<2100)});
if(!rm&&'IntersectionObserver' in window&&stats.length){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;io.unobserve(e.target);var el=e.target,txt=el.textContent.trim(),m=txt.match(/^([^0-9]*)([0-9][0-9,]*)(\.[0-9]+)?(.*)$/);if(!m)return;var pre=m[1],intp=m[2].replace(/,/g,''),dec=m[3]||'',suf=m[4],target=parseFloat(intp+dec),places=dec?dec.length-1:0,comma=m[2].indexOf(',')>-1,t0=null;function fmt(v){var f=v.toFixed(places);if(comma){var parts=f.split('.');parts[0]=parts[0].replace(/\B(?=(\d{3})+(?!\d))/g,',');f=parts.join('.')}return pre+f+suf}function step(ts){if(t0===null)t0=ts;var k=Math.min(1,(ts-t0)/1400);k=1-Math.pow(1-k,3);el.textContent=fmt(target*k);if(k<1)requestAnimationFrame(step);else el.textContent=txt}el.textContent=fmt(0);requestAnimationFrame(step)})},{threshold:.4});
  stats.forEach(function(b){io.observe(b)});
}
/* hero image: slow parallax against the scroll */
var hero=document.querySelector('.pv-hero-img img');
if(hero&&!rm&&matchMedia('(min-width:1025px)').matches){
  var raf=0;function move(){raf=0;var r=hero.getBoundingClientRect(),c=(r.top+r.height/2-innerHeight/2)/innerHeight;hero.style.transform='translateY('+(-c*14).toFixed(1)+'px)'}
  hero.style.willChange='transform';addEventListener('scroll',function(){if(!raf)raf=requestAnimationFrame(move)},{passive:true});move();
}
/* cards: light 3D tilt toward the pointer */
if(!rm&&matchMedia('(pointer:fine) and (min-width:1025px)').matches){
  document.querySelectorAll('.pv-tilt').forEach(function(c){
    c.style.transformStyle='preserve-3d';c.style.transition='transform .25s ease, box-shadow .25s ease';
    c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform='perspective(900px) rotateX('+(-y*6).toFixed(2)+'deg) rotateY('+(x*6).toFixed(2)+'deg) translateY(-3px)'});
    c.addEventListener('pointerleave',function(){c.style.transform=''});
  });
}
/* bottom bar: stay out of the way while the hero's own buttons are on screen */
var stk=document.querySelector('.pv-sticky'),hb=document.querySelector('main .pv-btns');
if(stk&&hb&&'IntersectionObserver' in window){new IntersectionObserver(function(es){es.forEach(function(e){stk.classList.toggle('pv-sticky-off',e.isIntersecting)})},{threshold:.2}).observe(hb)}
/* header: fold the utility bar away after the first scroll */
var hd=document.querySelector('.q-header');if(hd){var sc=function(){hd.classList.toggle('is-scrolled',scrollY>80)};addEventListener('scroll',sc,{passive:true});sc()}
/* mobile menu open: hide the bottom bars so the panel is not covered */
var mn=document.querySelector('.q-mnav');if(mn){mn.addEventListener('toggle',function(){document.documentElement.classList.toggle('menu-open',mn.open)})}
/* video facade: poster + play, iframe only on click */
document.querySelectorAll('.pv-video[data-embed]').forEach(function(v){
  var b=v.querySelector('button');if(!b)return;
  b.addEventListener('click',function(){var f=document.createElement('iframe');f.src=v.getAttribute('data-embed');f.title=b.getAttribute('aria-label')||'Video';f.allow='autoplay; fullscreen; picture-in-picture';f.allowFullscreen=true;v.innerHTML='';v.appendChild(f)});
});
})();
"""

MOBILE_LAST_CSS = r"""
.q-header .q-nav a,.q-header .q-booknow{white-space:nowrap}
[data-dir="press"] .q-header .q-nav{gap:20px}[data-dir="press"] .q-header .q-nav > a{font-size:15px}
.pv-hero-c .q-h1{max-width:22ch;margin-left:auto;margin-right:auto}
[data-dir="press"] .pv-loc.pv-grid-4{grid-template-columns:repeat(2,1fr)}
@media(max-width:767px){
  .pv-svc a{grid-template-columns:1fr!important;padding:20px 0!important}.pv-svc .num{display:none!important}
  .pv-quote{font-size:20px!important;font-weight:500!important}
  .q-section .pv-stats[style]{grid-template-columns:1fr 1fr!important;gap:28px 0!important}.pv-stat:nth-child(3){border-left:none}
  .q-h1{font-size:42px;line-height:1.05}.q-h2{font-size:31px;line-height:1.12}
  .pv-loc .q-card p a{padding-top:4px}
}
"""

# ----------------------------------------------------------------------------- sections

def sec_open(s: dict, extra_cls: str = "") -> str:
    cls = "q-section" + (" q-bg-alt" if s.get("alt") else "") + (" " + extra_cls if extra_cls else "")
    idattr = f' id="{E(s["id"])}"' if s.get("id") else ""
    return f'<section class="{cls}"{idattr}>'


def r_hero(s, ctx):
    eyebrow = f'<div class="q-eyebrow">{E(s.get("eyebrow"))}</div>' if s.get("eyebrow") else ""
    btns = ""
    if s.get("primary"):
        btns += f'<a class="q-btn" href="{E(ctx["L"](s["primary"]["href"]))}">{E(s["primary"]["label"])}</a>'
    if s.get("secondary"):
        btns += f'<a class="q-btn-ghost" href="{E(ctx["L"](s["secondary"]["href"]))}">{E(s["secondary"]["label"])}<span style="width:22px;height:1px;background:currentColor;display:inline-block"></span></a>'
    btns = f'<div class="pv-btns">{btns}</div>' if btns else ""
    note = f'<div class="pv-hero-note">{E(s["note"])}</div>' if s.get("note") else ""
    if s.get("layout") == "split" and s.get("image"):
        badge = (f'<div class="pv-badge"><b>{E(s["badge"]["value"])}</b><span>{E(s["badge"]["label"])}</span></div>'
                 if s.get("badge") else "")
        stats = ""
        if s.get("stats"):
            cells = "".join(f'<div><b{" data-static" if not str(v).replace(",", "").replace(".", "").isdigit() or len(str(v)) == 4 or float(str(v).replace(",", "")) < 100 else ""}>{E(v)}</b><span>{E(l)}</span></div>' for v, l in s["stats"])
            stats = f'<div class="pv-hero-stats">{cells}</div>'
        ribbon = ""
        if s.get("ribbon"):
            ribbon = '<div class="pv-ribbon"><div class="q-container">' + "".join(f'<span>{E(x)}</span>' for x in s["ribbon"]) + "</div></div>"
        return f'''{sec_open(s)} <div class="q-container"><div class="pv-hero-grid"><div>{eyebrow}
<h1 class="q-h1" style="margin-top:22px">{RAW(s["heading"])}</h1>
<div class="q-lead" style="max-width:540px;margin:24px 0 0">{E(s.get("subhead"))}</div>{btns}{note}</div>
<div class="pv-hero-img"><img src="{E(ctx["rel"](s["image"]))}"{ctx["srcset"](s["image"])} alt="{E(s.get("image_alt"))}" width="{s.get("image_w", 1200)}" height="{s.get("image_h", 800)}" fetchpriority="high" decoding="async">{badge}</div></div>{stats}</div></section>{ribbon}'''
    return f'''{sec_open(s)} <div class="q-container"><div class="pv-center pv-hero-c" style="max-width:860px;margin:0 auto">{eyebrow}
<h1 class="q-h1" style="margin-top:22px">{RAW(s["heading"])}</h1>
<div class="q-lead" style="max-width:640px;margin:24px 0 0">{E(s.get("subhead"))}</div>{btns.replace('class="pv-btns"', 'class="pv-btns" style="justify-content:center"')}{note}</div>{f'<div class="pv-hero-wide"><img src="{E(ctx["rel"](s["image"]))}"{ctx["srcset"](s["image"])} alt="{E(s.get("image_alt", ""))}" width="{s.get("image_w", 1200)}" height="{s.get("image_h", 675)}" fetchpriority="high" decoding="async"></div>' if s.get("image") else ""}</div></section>'''


def r_partners(s, ctx):
    items = []
    for name in s["items"]:
        img = ctx["partner_logo"](name)
        if img:
            items.append(f'<img src="{E(img)}" alt="{E(name)}" loading="eager" width="144" height="48">')
        else:
            items.append(f"<span>{E(name)}</span>")
    track = "".join(items)
    return f'<section class="pv-partners"><div class="q-container"><p class="pv-cap">{E(s.get("caption", "Partners"))}</p></div><div class="pv-logos" role="region" aria-label="Technology partners"><div class="pv-logos-track">{track}</div><div class="pv-logos-track" aria-hidden="true">{track}</div></div></section>'


def r_stats(s, ctx):
    n = len(s["items"])
    cells = "".join(f'<div class="pv-stat"><b>{E(v)}</b><span>{E(k)}</span></div>' for v, k in s["items"])
    return f'{sec_open(s)} <div class="q-container pv-stats" style="grid-template-columns:repeat({n},1fr)">{cells}</div></section>'


def r_services(s, ctx):
    rows = "".join(
        f'<a href="{E(ctx["L"](href))}"><div class="num" aria-hidden="true" data-folio="{i:02d}"></div><div><h3>{E(t)}</h3><p>{E(b)}</p></div><div class="more">Learn more</div></a>'
        for i, (t, b, href) in enumerate(s["items"], 1))
    return f'{sec_open(s)} <div class="q-container"><div class="pv-split"><h2 class="q-h2">{E(s["heading"])}</h2><p>{E(s.get("intro"))}</p></div><div class="pv-svc">{rows}</div></div></section>'


def r_process(s, ctx):
    n = len(s["stages"])
    stages = "".join(
        f'<div class="pv-center pv-stage"><div class="q-stagenum">{i}</div><h3>{E(t)}</h3><p>{E(b)}</p></div>'
        for i, (t, b) in enumerate(s["stages"], 1))
    grid = "q-grid-5" if n == 5 else f"pv-grid pv-grid-{cols_for(n)}"
    return f'{sec_open(s)} <div class="q-container"><div class="pv-center"><div class="q-eyebrow">{E(s.get("eyebrow"))}</div><h2 class="q-h2" style="margin-top:22px;max-width:760px">{E(s["heading"])}</h2></div><div class="{grid}" style="margin-top:60px">{stages}</div></div></section>'


def r_casestudy(s, ctx):
    metrics = "".join(f'<div class="q-card pv-metric"><div class="k">{E(k)}</div><div class="v">{E(v)}</div><div class="d">{E(d)}</div></div>' for k, v, d in s["metrics"])
    return f'''{sec_open(s)} <div class="q-container pv-cs"><div><div class="q-eyebrow">{E(s.get("eyebrow"))}</div><div class="h">{E(s["heading"])}</div><p class="pv-quote">{E(s["quote"].strip().strip('"'))}</p><div class="pv-attr">{E(s.get("attribution"))}</div></div><div class="pv-grid pv-grid-2">{metrics}</div></div></section>'''


def r_cards(s, ctx):
    n = len(s["items"]); cols = cols_for(n)
    cards = "".join(f'<div class="q-card"><h3>{E(t)}</h3><p>{E(b)}</p></div>' for t, b in s["items"])
    head = ""
    if s.get("heading"):
        head = f'<div class="pv-center" style="margin-bottom:44px">{f"<div class=q-eyebrow>{E(s.get(chr(101)+chr(121)+chr(101)+chr(98)+chr(114)+chr(111)+chr(119)))}</div>" if s.get("eyebrow") else ""}<h2 class="q-h2" style="margin-top:22px;max-width:700px">{E(s["heading"])}</h2></div>'
    return f'{sec_open(s)} <div class="q-container">{head}<div class="pv-grid pv-grid-{cols}">{cards}</div></div></section>'


def r_band(s, ctx):
    n = len(s["items"]); cols = cols_for(n)
    cards = "".join(f'<a class="q-card" href="{E(ctx["L"](h))}"><div class="t">{E(t)}</div><div class="d">{E(d)}</div></a>' for t, d, h in s["items"])
    return f'''{sec_open(s, "pv-band")} <div class="q-container pv-cs"><div><div class="q-eyebrow">{E(s.get("eyebrow"))}</div><h2 class="q-h2" style="margin-top:22px">{E(s["heading"])}</h2><div class="q-lead" style="margin-top:20px;max-width:480px">{E(s.get("subhead"))}</div></div><div class="pv-grid pv-grid-{min(cols,2)}">{cards}</div></div></section>'''


def r_locations(s, ctx):
    n = len(s["items"]); cols = cols_for(n)
    cards = []
    for name, a1, a2, phone, href in s["items"]:
        mp = ""
        cards.append(f'<div class="q-card">{mp}<h3>{E(name)}</h3><p><span>{E(a1)}</span><span>{E(a2)}</span><a href="{E(ctx["L"](href))}">{E(phone)}</a></p></div>')
    return f'{sec_open(s)} <div class="q-container"><div class="pv-split"><h2 class="q-h2">{E(s["heading"])}</h2><p>{E(s.get("intro"))}</p></div><div class="pv-grid pv-grid-{cols} pv-loc">{"".join(cards)}</div></div></section>'


def r_faq(s, ctx):
    items = "".join(f'<details{" open" if i == 0 else ""}><summary>{E(q)}<span>+</span></summary><p>{E(a)}</p></details>' for i, (q, a) in enumerate(s["items"]))
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["items"]]}, ensure_ascii=False)
    return f'{sec_open(s)} <div class="q-container pv-faq" style="max-width:860px"><h2 class="q-h2" style="text-align:center;margin-bottom:36px">{E(s["heading"])}</h2>{items}</div><script type="application/ld+json">{ld}</script></section>'


def r_contact(s, ctx):
    opts = "".join(f"<option>{E(o)}</option>" for o in s.get("options", []))
    brand = ctx["brand"]
    return f'''{sec_open(s)} <div class="q-container pv-contact"><div><h2 class="q-h2">{E(s["heading"])}</h2><div class="q-lead" style="margin-top:20px">{E(s.get("body"))}</div>
<div style="margin-top:28px;display:flex;flex-direction:column;gap:14px"><a class="q-btn" style="align-self:flex-start" href="{E(ctx["L"](brand["phone_href"]))}">Call {E(brand["phone"])}</a><a href="mailto:{E(brand["email"])}" style="font-size:15px;color:var(--fg-muted);min-height:44px;display:inline-flex;align-items:center">{E(brand["email"])}</a></div></div>
<form class="q-form" onsubmit="return false"><label for="f1">Name</label><input id="f1" type="text" autocomplete="name"><label for="f2">Work email</label><input id="f2" type="email" autocomplete="email"><label for="f3">Phone</label><input id="f3" type="tel" autocomplete="tel"><label for="f4">What would you like to look at?</label><select id="f4">{opts}</select><input type="submit" class="hs-button" value="{E(s.get("submit", "Send"))}"><p class="pv-form-note">{E(s.get("note"))}</p></form></div></section>'''


def r_detail(s, ctx):
    bullets = "".join(f"<li>{E(b)}</li>" for b in s.get("bullets", []))
    right = ""
    if s.get("image"):
        right = (f'<div class="pv-detail-img"><img src="{E(ctx["rel"](s["image"]))}"{ctx["srcset"](s["image"])} alt="{E(s.get("image_alt", ""))}" width="{s.get("image_w", 1200)}" height="{s.get("image_h", 800)}" loading="lazy" decoding="async"></div>'
                 + (f'<ul>{bullets}</ul>' if bullets else ""))
        bullets = ""
    elif s.get("form"):
        fields = "".join(f'<label for="{E(s["id"])}-{i}">{E(f)}</label><input id="{E(s["id"])}-{i}" type="text">' for i, f in enumerate(s["form"]["fields"]))
        right = f'<form class="q-form" onsubmit="return false">{fields}<input type="submit" class="hs-button" value="{E(s["form"]["submit"])}"></form>'
    else:
        right = f'<ul>{bullets}</ul>'
        bullets = ""
    return f'''{sec_open(s)} <div class="q-container pv-detail{" pv-flip" if s.get("flip") else ""}"><div><div class="q-eyebrow">{E(s.get("eyebrow"))}</div><h2 class="q-h2">{E(s["heading"])}</h2><div class="q-lead">{E(s.get("body"))}</div>{f"<ul>{bullets}</ul>" if bullets else ""}</div><div>{right}</div></div></section>'''


def r_listing(s, ctx):
    n = len(s["items"]); cols = cols_for(n)
    posts = "".join(f'<a class="pv-post" href="{E(ctx["L"](it[3] if len(it) > 3 else "#"))}"{" target=_blank rel=noopener" if len(it) > 3 and str(it[3]).startswith("http") else ""}><div class="ph"></div><span class="tag">{E(it[0])}</span><h2>{E(it[1])}</h2><p>{E(it[2])}</p></a>' for it in s["items"])
    return f'{sec_open(s)} <div class="q-container"><div class="pv-grid pv-grid-{cols}">{posts}</div></div></section>'


def r_team(s, ctx):
    n = len(s["items"]); cols = cols_for(n)
    cards = "".join(f'<div class="q-card"><div class="av"></div><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t, d in s["items"])
    return f'{sec_open(s)} <div class="q-container"><div class="pv-center" style="margin-bottom:40px"><div class="q-eyebrow">{E(s.get("eyebrow"))}</div><h2 class="q-h2" style="margin-top:22px">{E(s["heading"])}</h2><p style="color:var(--fg-muted);max-width:60ch;margin:14px 0 0">{E(s.get("intro"))}</p></div><div class="pv-grid pv-grid-{cols} pv-team">{cards}</div></div></section>'


def r_leadform(s, ctx):
    """The soft conversion path on pages that have no form: one line, one field, one button,
    plus the phone for the visitor who would rather talk. process/quality-standard.md item 6."""
    brand = ctx["brand"]
    fid = s.get("id", "lead")
    spec = s.get("fields") or [["Name", "text", "name"], ["Work email", "email", "email"], ["Phone", "tel", "tel"], ["Company", "text", "organization"]]
    fields = "".join(f'<label for="{E(fid)}-{i}">{E(l)}</label><input id="{E(fid)}-{i}" type="{E(t)}" autocomplete="{E(a)}">' for i, (l, t, a) in enumerate(spec))
    return f'''{sec_open(s)} <div class="q-container pv-contact" style="align-items:center"><div><h2 class="q-h2">{E(s["heading"])}</h2><div class="q-lead" style="margin-top:16px">{E(s.get("body"))}</div><p style="margin-top:20px;font-size:15px;color:var(--fg-muted)">Or call <a href="{E(ctx["L"](brand["phone_href"]))}" style="color:var(--fg);font-weight:600;min-height:44px;display:inline-flex;align-items:center">{E(brand["phone"])}</a></p></div>
<form class="q-form" onsubmit="return false">{fields}<input type="submit" class="hs-button" value="{E(s.get("submit", "Send"))}"><p class="pv-form-note">{E(s.get("note", ""))}</p></form></div></section>'''


def r_cta(s, ctx):
    btn = f'<div style="margin-top:34px"><a class="q-btn" href="{E(ctx["L"](s["primary"]["href"]))}">{E(s["primary"]["label"])}</a></div>' if s.get("primary") else ""
    return f'{sec_open(s, "pv-cta")} <div class="q-container"><h2 class="q-h2" style="font-size:clamp(30px,4vw,52px)">{E(s["heading"])}</h2><div class="q-lead" style="max-width:540px;margin:22px auto 0">{E(s.get("subhead"))}</div>{btn}</div></section>'


RENDER = {"hero": r_hero, "partners": r_partners, "stats": r_stats, "services": r_services, "process": r_process,
          "casestudy": r_casestudy, "cards": r_cards, "band": r_band, "locations": r_locations, "faq": r_faq,
          "contact": r_contact, "detail": r_detail, "listing": r_listing, "team": r_team, "cta": r_cta,
          "leadform": r_leadform}
RENDER.update(preview_sections.RENDER_EXTRA)
RENDER.update(preview_modules.RENDER_EXTRA2)


# ------------------------------------------------------------------------------ chrome

def _nav_items(content):
    """Normalise nav entries: [label, href] or {label, href, children|groups, featured, mega}."""
    out = []
    for it in content["nav"]:
        if isinstance(it, dict):
            out.append(it)
        else:
            out.append({"label": it[0], "href": it[1]})
    return out


def _active(item, file):
    """True when the current page is this item or sits beneath it."""
    hrefs = [item.get("href", "")]
    hrefs += [c[1] for c in item.get("children", [])]
    for g in item.get("groups", []):
        hrefs += [c[1] for c in g["items"]]
    hrefs = [h.split("#")[0] for h in hrefs if h]
    if file in hrefs:
        return True
    top = item.get("href", "").split("#")[0].rsplit(".", 1)[0]
    return bool(top) and file.startswith(top + "/")


def header(content, ctx):
    b = content["brand"]
    L, file = ctx["L"], ctx.get("file", "")
    util = "".join(f'<a href="{E(L(h))}"{" class=pv-keep" if i == 0 else ""}>{E(l)}</a>' for i, (l, h) in enumerate((u["label"], u["href"]) for u in b.get("utility", [])))
    if b.get("phone"):
        util += f'<a class="pv-phone" href="{E(b["phone_href"])}">{E(b["phone"])}</a>'
    nav, mnav = [], []
    for it in _nav_items(content):
        cur = ' aria-current="true"' if _active(it, file) else ""
        label = E(it["label"])
        if it.get("groups") or it.get("children"):
            if it.get("groups"):
                cols = "".join(f'<div class="col"><div class="gt">{E(g["title"])}</div>' + "".join(f'<a href="{E(L(h))}">{E(l)}</a>' for l, h in g["items"]) + "</div>" for g in it["groups"])
                f = it.get("featured")
                feat = (f'<a class="feat" href="{E(L(f["href"]))}"><span class="q-eyebrow">{E(f.get("eyebrow", ""))}</span><b>{E(f["title"])}</b><p>{E(f.get("body", ""))}</p><span class="more">{E(f.get("label", "Learn more"))}</span></a>' if f else "")
                panel = f'<div class="q-subnav pv-mega"><div class="pv-mega-in">{cols}{feat}</div><div class="pv-mega-foot"><a href="{E(L(it["href"]))}">All {E(it["label"].lower())}</a></div></div>'
            else:
                panel = '<div class="q-subnav">' + "".join(f'<a href="{E(L(h))}">{E(l)}</a>' for l, h in it["children"]) + "</div>"
            nav.append(f'<div class="q-nav-item{" pv-has-mega" if it.get("groups") else ""}"><a href="{E(L(it["href"]))}" aria-haspopup="true"{cur}>{label}<span class="q-caret" aria-hidden="true"></span></a>{panel}</div>')
            # mobile accordion
            links = ""
            if it.get("groups"):
                for g in it["groups"]:
                    links += f'<div class="pv-mgt">{E(g["title"])}</div>' + "".join(f'<a href="{E(L(h))}">{E(l)}</a>' for l, h in g["items"])
                links += f'<a href="{E(L(it["href"]))}" class="pv-mall">All {E(it["label"].lower())}</a>'
            else:
                links = "".join(f'<a href="{E(L(h))}">{E(l)}</a>' for l, h in it["children"])
            mnav.append(f'<details class="q-msub"{" open" if cur else ""}><summary>{label}<span class="q-caret" aria-hidden="true"></span></summary><div class="q-msub-links">{links}</div></details>')
        else:
            nav.append(f'<a href="{E(L(it["href"]))}"{cur}>{label}</a>')
            mnav.append(f'<a href="{E(L(it["href"]))}"{cur}>{label}</a>')
    mnav_s = "".join(mnav) + "".join(f'<a href="{E(L(u["href"]))}">{E(u["label"])}</a>' for u in b.get("utility", []))
    if b.get("phone"):
        mnav_s += f'<a href="{E(b["phone_href"])}">Call {E(b["phone"])}</a>'
    cta = f'<a class="q-booknow" href="{E(L(b["cta"]["href"]))}">{E(b["cta"]["label"])}</a>' if b.get("cta") else ""
    mcta = f'<a class="q-mnav-cta" href="{E(L(b["cta"]["href"]))}">{E(b["cta"]["label"])}</a>' if b.get("cta") else ""
    lw, lh = b.get("logo_w", 300), b.get("logo_h", 100)
    logo = (f'<img src="{E(ctx["rel"](b["logo"]))}" alt="{E(b.get("logo_alt", content["client"]))}" width="{round(40 * lw / lh)}" height="40" loading="eager">'
            if b.get("logo") else f'<span class="q-logo-text">{E(content["client"])}</span>')
    return f'''<header class="q-header"><a class="q-skip" href="#q-content">Skip to content</a>
<div class="pv-util"><div class="q-container">{util}</div></div>
<div class="q-container q-header-in">
  <a href="{E(L("index.html"))}" class="q-header-logo" aria-label="{E(content["client"])} home">{logo}</a>
  <nav class="q-nav" aria-label="Main navigation">{"".join(nav)}{cta}</nav>
  <details class="q-mnav"><summary aria-label="Open menu"><span></span><span></span><span></span></summary><div class="q-mnav-panel">{mnav_s}{mcta}</div></details>
</div></header>
<div id="q-content" tabindex="-1">'''


def crumbs(page, ctx):
    c = page.get("crumbs")
    if not c:
        return ""
    items = []
    for i, (l, h) in enumerate(c):
        last = i == len(c) - 1
        items.append(f'<li>{"<span aria-current=page>" + E(l) + "</span>" if last else f"<a href={chr(34)}{E(ctx[chr(76)](h))}{chr(34)}>{E(l)}</a>"}</li>')
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": l} for i, (l, h) in enumerate(c)]}
    return f'<nav class="pv-crumbs" aria-label="Breadcrumb"><div class="q-container"><ol>{"".join(items)}</ol></div></nav><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'


def footer(content, ctx):
    b = content["brand"]
    lw, lh = b.get("logo_w", 300), b.get("logo_h", 100)
    logo = (f'<img src="{E(ctx["rel"](b["logo"]))}" alt="{E(b.get("logo_alt", content["client"]))}" width="{round(36 * lw / lh)}" height="36" loading="lazy">'
            if b.get("logo") else f'<span class="q-logo-text">{E(content["client"])}</span>')
    cols = "".join(
        f'<div><div class="q-footer-head">{E(c["title"])}</div><nav class="q-footer-links" aria-label="{E(c["title"])}">'
        + "".join(f'<a href="{E(ctx["L"](h))}">{E(l)}</a>' for l, h in c["links"]) + "</nav></div>"
        for c in b.get("footer_columns", []))
    soc = b.get("social", {})
    _names = {"linkedin": "LinkedIn", "facebook": "Facebook", "x": "X", "instagram": "Instagram", "youtube": "YouTube"}
    social = "".join(f'<a href="{E(u)}" aria-label="{E(_names.get(k, k.title()))}">{E(_names.get(k, k.title()))}</a>' for k, u in soc.items() if u)
    contact = ""
    if b.get("phone") or b.get("email"):
        contact = f'<p class="q-footer-contact">{f"<a class=q-footer-phone href={E(b[chr(112)+chr(104)+chr(111)+chr(110)+chr(101)+chr(95)+chr(104)+chr(114)+chr(101)+chr(102)])}>{E(b[chr(112)+chr(104)+chr(111)+chr(110)+chr(101)])}</a>" if b.get("phone") else ""}{"<br>" if b.get("phone") and b.get("email") else ""}{f"<a href=mailto:{E(b[chr(101)+chr(109)+chr(97)+chr(105)+chr(108)])}>{E(b[chr(101)+chr(109)+chr(97)+chr(105)+chr(108)])}</a>" if b.get("email") else ""}</p>'
    legal = "".join(f'<span class="pv-legal-item"><a href="{E(ctx["L"](h))}">{E(l)}</a></span>' for l, h in b.get("legal", []))
    return f'''</div>
<footer class="q-footer"><div class="q-container q-footer-grid pv-fcols-{len(b.get("footer_columns", []))}"><div>{logo}<p class="q-footer-tag">{E(b.get("tagline"))}</p>{contact}<div class="q-footer-social" style="gap:8px;font-size:14px">{social}</div></div>{cols}</div>
<div class="q-container q-footer-legal"><span class="pv-legal-item">Copyright &copy; {ctx["year"]} {E(content["client"])}</span>{legal}</div></footer>'''


def switcher(themes, this_theme, page_file, recommend):
    up = "../" * (page_file.count("/") + 1)
    def link(t):
        cur = ' aria-current="page"' if t == this_theme else ""
        label = t.replace("Quantum ", "") + (" (recommended)" if t == recommend else "")
        return f'<a href="{up}{slug_of(t)}/{page_file}"{cur}>{E(label)}</a>'
    links = "".join(link(t) for t in themes)
    cur_name = this_theme.replace("Quantum ", "")
    return (f'<nav class="pv-switch" aria-label="Preview directions"><span class="lbl">Direction</span>{links}<a href="{up}index.html">All three</a></nav>'
            f'<details class="pv-switch-m"><summary aria-label="Change direction">Direction: {E(cur_name)} &#9662;</summary><nav class="menu" aria-label="Preview directions">{links}<a href="{up}index.html">All three</a></nav></details>'
            '<script>if(top!==self){document.documentElement.classList.add("embedded")}</script>')


def _head_tail(title, client, short):
    head, sep, tail = title.partition(" | ")
    if not sep:
        return title, ""
    if head.strip() in (client, short):          # "Client | what the page is" -> swap
        head, tail = tail, head
    tl = tail.strip().lower()
    if tl.startswith((client.lower(), short.lower())):
        return head.strip(), ""                   # brand suffix, rebuilt below
    return f"{head.strip()}: {tail.strip()}", ""  # a real subtitle: keep it in the head


def normalize_meta(page, content):
    """Titles 30 to 60 characters with the brand and, where the schema block asks for it,
    the service area; meta descriptions 70 to 160 characters cut at a sentence end.
    Returns (title, description, notes)."""
    sch = content.get("schema") or {}
    client = content["client"]
    short = sch.get("short_name") or client.split(" ")[0]
    cities = [c.lower() for c in sch.get("cities", [])]
    city_tag = sch.get("title_city")
    notes = []
    title = page["title"].strip()
    head, _ = _head_tail(title, client, short)

    def has_city(t):
        tl = t.lower()
        return any(re.search(r"(?<![a-z])" + re.escape(c) + r"(?![a-z])", tl) for c in cities)

    def options(h, city_only=False):
        need = bool(city_tag) and not has_city(h)
        if need:
            opts = [f"{h} | {client}, {city_tag}", f"{h} | {short}, {city_tag}", f"{h}, {city_tag} | {short}"]
            if city_only:
                return opts
            return opts + [f"{h} | {client}", f"{h} | {short}"]
        return [f"{h} | {client}", f"{h} | {short}"]

    def fit(h, city_only=False):
        for o in options(h, city_only):
            if len(o) <= 60:
                return o
        return None

    def shorten(h, city_only):
        out = fit(h, city_only)
        if out:
            return out
        for sep_ in (": ", ", ", " and ", " for "):
            if sep_ in h and len(h.split(sep_)[0]) >= 18:
                out = fit(h.split(sep_)[0], city_only)
                if out:
                    return out
        words = h.split()
        while len(words) > 3:
            words.pop()
            while words and words[-1].lower() in ("and", "of", "the", "a", "an", "in", "for", "to", "with", "or", "vs.", "vs"):
                words.pop()
            out = fit(" ".join(words).rstrip(",:;"), city_only)
            if out:
                return out
        return None

    # the service area in the title outranks the full brand name: try city-bearing forms first
    out = shorten(head, city_only=True) if city_tag else None
    if not out:
        out = shorten(head, city_only=False)
    if not out:
        out = title[:60]
    if out != title:
        notes.append("title")
    if city_tag and not has_city(title) and has_city(out):
        notes.append("city")

    desc = re.sub(r"\s+", " ", page.get("description", "")).strip()
    if len(desc) > 160:
        cut = desc[:158]
        i = max(cut.rfind(". "), cut.rfind("? "), cut.rfind("! "))
        if i >= 70:
            desc2 = cut[: i + 1]
        else:
            j = max(cut.rfind(", "), cut.rfind(" "))
            desc2 = cut[:j].rstrip(",;: ") + "."
        desc, notes = desc2, notes + ["meta"]
    elif len(desc) < 70 and sch.get("meta_tail"):
        tail = sch["meta_tail"].strip()
        cand = f"{desc} {tail}" if desc else tail
        desc, notes = cand[:160].rstrip(), notes + ["meta"]
    return out, desc, notes


def schema_blocks(content, page, base, dslug, title=None, description=None):
    """Organization and the headquarters LocalBusiness on every page; WebSite on the home page;
    BreadcrumbList elsewhere; Service on service, industry and product pages; BlogPosting on posts.
    Pages that carry their own LocalBusiness, Service or BlogPosting block are not duplicated."""
    import fnmatch
    sch = content.get("schema") or {}
    if not sch.get("org_name"):
        return ""
    site = sch.get("org_url") or base
    title = title or page["title"]
    description = description or page.get("description", "")
    own = set()
    for blk in page.get("schema", []):
        t = blk.get("@type")
        own.update([t] if isinstance(t, str) else (t or []))
    blocks = []
    org = {"@context": "https://schema.org", "@type": "Organization", "@id": f"{site}/#organization", "name": sch["org_name"], "url": site}
    if sch.get("legal_name"):
        org["legalName"] = sch["legal_name"]
    for k, v in (("logo", sch.get("org_logo")), ("description", sch.get("org_description")), ("sameAs", sch.get("sameAs")), ("foundingDate", sch.get("founded")),
                 ("numberOfEmployees", sch.get("employees")), ("areaServed", sch.get("area_served")), ("slogan", sch.get("slogan"))):
        if v:
            org[k] = {"@type": "ImageObject", "url": v} if k == "logo" else ({"@type": "QuantitativeValue", "value": v} if k == "numberOfEmployees" else v)
    if sch.get("telephone"):
        org["telephone"] = sch["telephone"]
        org["contactPoint"] = {"@type": "ContactPoint", "contactType": "Sales", "telephone": sch["telephone"], "areaServed": "US", "availableLanguage": "English"}
    local = sch.get("local") or []
    if local:
        hq = local[0]
        org["address"] = {"@type": "PostalAddress", "streetAddress": hq.get("street"), "addressLocality": hq.get("city"), "addressRegion": hq.get("region"), "postalCode": hq.get("postal"), "addressCountry": hq.get("country", "US")}
        if len(local) > 1:
            org["subOrganization"] = [{"@id": f"{site}/#local-{l['slug']}"} for l in local[1:]]
    blocks.append(org)
    if page["file"] == "index.html":
        blocks.append({"@context": "https://schema.org", "@type": "WebSite", "@id": f"{site}/#website", "url": site, "name": sch["org_name"], "publisher": {"@id": f"{site}/#organization"}, "inLanguage": "en-US"})
    if local and "LocalBusiness" not in own:
        hq = local[0]
        lb = {"@context": "https://schema.org", "@type": sch.get("local_type", "LocalBusiness"), "@id": f"{site}/#local-{hq['slug']}", "name": hq.get("name") or sch["org_name"], "url": site,
              "parentOrganization": {"@id": f"{site}/#organization"},
              "address": {"@type": "PostalAddress", "streetAddress": hq.get("street"), "addressLocality": hq.get("city"), "addressRegion": hq.get("region"), "postalCode": hq.get("postal"), "addressCountry": hq.get("country", "US")}}
        for k in ("telephone", "priceRange", "openingHours"):
            if hq.get(k):
                lb[k] = hq[k]
        if hq.get("lat") and hq.get("lon"):
            lb["geo"] = {"@type": "GeoCoordinates", "latitude": hq["lat"], "longitude": hq["lon"]}
        if sch.get("area_served"):
            lb["areaServed"] = sch["area_served"]
        if sch.get("org_logo"):
            lb["image"] = sch["org_logo"]
        blocks.append(lb)
    if page["file"] != "index.html":
        name = title.split("|")[0].strip()
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{site}/"}]
        parts = page["file"].split("/")
        if len(parts) > 1:
            items.append({"@type": "ListItem", "position": 2, "name": parts[0].replace("-", " ").title(), "item": f"{site}/{parts[0]}"})
        items.append({"@type": "ListItem", "position": len(items) + 1, "name": name, "item": f"{site}/{page['file'].replace('.html', '')}"})
        blocks.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
        page_url = f"{site}/{page['file'].replace('.html', '')}"
        svc_globs = sch.get("service_globs", ["services/*", "industries/*", "products/*", "brands/*"])
        post_globs = sch.get("post_globs", ["blog/*", "guides/*", "resources/*"])
        if any(fnmatch.fnmatch(page["file"], g) for g in svc_globs) and not (own & {"Service", "ProfessionalService", "Product"}):
            svc = {"@context": "https://schema.org", "@type": "Service", "@id": f"{page_url}#service", "name": name, "serviceType": name, "description": description,
                   "provider": {"@id": f"{site}/#organization"}, "url": page_url}
            if sch.get("area_served"):
                svc["areaServed"] = sch["area_served"]
            blocks.append(svc)
        elif any(fnmatch.fnmatch(page["file"], g) for g in post_globs) and not (own & {"BlogPosting", "Article", "NewsArticle"}):
            post = {"@context": "https://schema.org", "@type": "BlogPosting", "@id": f"{page_url}#article", "headline": name, "description": description, "url": page_url,
                    "mainEntityOfPage": page_url, "author": {"@id": f"{site}/#organization"}, "publisher": {"@id": f"{site}/#organization"}, "inLanguage": "en-US"}
            for k, v in (("datePublished", page.get("date")), ("dateModified", page.get("modified") or page.get("date")), ("articleSection", page.get("section"))):
                if v:
                    post[k] = v
            blocks.append(post)
    return "\n".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in blocks)


def srcset_for(path: str, out_dir: str) -> str:
    """srcset/sizes when a 600px sibling exists (assets/x-1200.jpg -> assets/x-600.jpg)."""
    m = re.match(r"(.*)-(1200|1024)\.(jpe?g|png)$", path)
    if not m:
        return ""
    small = f"{m.group(1)}-600.{m.group(3)}"
    if not os.path.exists(os.path.join(out_dir, small)):
        return ""
    return f' srcset="../{small} 600w, ../{path} {m.group(2)}w" sizes="(max-width: 1024px) 100vw, 50vw"'


def render_page(content, page, theme, css, tok, themes, recommend, base, out_dir, dslug):
    b = content["brand"]
    partners_dir = os.path.join(out_dir, "assets", "partners")
    depth = page["file"].count("/")           # blog/post.html -> 1
    up = "../" * (depth + 1)                   # to the repo root (assets/, other directions)
    root = "../" * depth                       # to this direction's root (index.html, contact.html)

    def rel(p):
        return up + p

    def L(href):
        """Internal links are written root-relative in the content file (contact.html,
        blog/x.html, what-we-do.html#it). Prefix them for the page's depth."""
        if not href or href.startswith(("#", "http", "mailto:", "tel:", "/")):
            return href
        return root + href

    def partner_logo(name):
        s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        for ext in ("png", "jpg", "svg", "webp"):
            if os.path.exists(os.path.join(partners_dir, f"{s}.{ext}")):
                return f"{up}assets/partners/{s}.{ext}"
        return None

    def srcset(pth):
        ss = srcset_for(pth, out_dir)
        return ss.replace('"../', '"' + up).replace(', ../', ', ' + up)

    ctx = {"rel": rel, "L": L, "partner_logo": partner_logo, "brand": b, "year": 2026, "srcset": srcset, "file": page["file"],
           "E": E, "RAW": RAW, "sec_open": sec_open, "depth": depth, "client": content.get("client", ""), "client_short": content.get("client", "").split(" ")[0]}
    secs = []
    for sec in page["sections"]:
        sec = dict(sec)
        v = (sec.pop("variants", None) or {}).get(dslug)
        if v:
            sec.update(v)
        secs.append(sec)
    comp = (page.get("compose") or {}).get(dslug)
    if comp:
        by_id = {x.get("id"): x for x in secs if x.get("id")}
        missing = [i for i in comp if i not in by_id]
        if missing:
            raise SystemExit(f"{page['file']} [{dslug}]: compose names sections that do not exist: {', '.join(missing)}")
        secs = [by_id[i] for i in comp]
    if any(x["type"] in ("leadform", "contact") for x in secs) and secs and secs[-1]["type"] == "cta":
        secs = secs[:-1]   # two "start with the assessment" blocks in a row read as a template bug
    body = "".join(RENDER[s["type"]](s, ctx) for s in secs)
    canonical = f"{base}/{dslug}/" if page["file"] == "index.html" else f"{base}/{dslug}/{page['file']}"
    og_img = f"{base}/assets/hero-og.jpg"
    p_title, p_desc, _notes = normalize_meta(page, content)
    tokcss = "\n  ".join(f"{k}:{v};" for k, v in tok.items())
    return f'''<!doctype html>
<html lang="en" data-dir="{E(dslug)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(p_title)}</title>
<meta name="description" content="{E(p_desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{E(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(content["client"])}">
<meta property="og:title" content="{E(p_title)}">
<meta property="og:description" content="{E(p_desc)}">
<meta property="og:url" content="{E(canonical)}">
<meta property="og:image" content="{E(og_img)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(p_title)}">
<meta name="twitter:image" content="{E(og_img)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<style>
/* ===== {E(theme)}: css/quantum.css from themes/source, as patched by themefix.py ===== */
{css}
/* ===== theme header + footer module CSS ===== */
{themefix.HEADER_CSS}
{themefix.FOOTER_CSS}
/* ===== {E(content["client"])} re-skin: the surface reskin.py writes ===== */
:root, [data-theme="dark"], [data-theme="light"] {{
  {tokcss}
}}
{PREVIEW_CSS}
{preview_sections.EXTRA_CSS}
{preview_modules.EXTRA_CSS2}
/* ===== direction system: {E(dslug)} ===== */
{DIRECTION_CSS.get(dslug, "")}
/* ===== mobile, after the direction system so it wins ===== */
{MOBILE_LAST_CSS}
</style>
{schema_blocks(content, page, base, dslug, p_title, p_desc)}
{"".join(f'<script type="application/ld+json">{json.dumps(blk, ensure_ascii=False)}</script>' for blk in page.get("schema", []))}
</head>
<body>
{header(content, ctx)}
{crumbs(page, ctx)}<main id="main">
{body}
</main>
{footer(content, ctx)}
{preview_sections.RENDER_EXTRA["sticky"](b.get("sticky", {}), ctx) if b.get("sticky") else ""}
{preview_modules._launcher(b["launcher"], ctx) if b.get("launcher") else ""}
{switcher(themes, theme, page["file"], recommend)}
<script>{PREVIEW_JS}</script>
<script>{preview_modules.DEPTH_JS}</script>
</body>
</html>
'''


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--content", required=True)
    p.add_argument("--themes", required=True)
    p.add_argument("--recommend")
    p.add_argument("--roles", default="", help="pipe-separated, one per theme, for the hub")
    p.add_argument("--base-url", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--no-standard", action="store_true")
    a = p.parse_args(argv)

    content = json.load(open(a.content, encoding="utf-8"))
    themes = [t.strip() for t in a.themes.split(",") if t.strip()]
    roles = dict(zip(themes, [r.strip() for r in a.roles.split("|")])) if a.roles else {}
    base = a.base_url.rstrip("/")
    written = 0
    for t in themes:
        css, tok = client_tokens(t, content["brand"])
        d = os.path.join(a.out, slug_of(t)); os.makedirs(d, exist_ok=True)
        for page in content["pages"]:
            doc = render_page(content, page, t, css, tok, themes, a.recommend, base, a.out, slug_of(t))
            dest = os.path.join(d, page["file"]); os.makedirs(os.path.dirname(dest), exist_ok=True)
            open(dest, "w", encoding="utf-8").write(doc); written += 1
        print(f"  {t:20} {len(content['pages'])} pages  accent {tok['--q-gold']} ink {tok['--accent-ink']} cta-fg {tok['--cta-fg']} chrome {tok['--chrome-bg']}")
    import preview_design  # noqa: E402
    import preview_seo  # noqa: E402
    preview_design.write(content, themes, roles, client_tokens, a.out)
    seo = preview_seo.write(content, a.content, themes, roles, base, a.out, slug_of)
    open(os.path.join(a.out, "index.html"), "w", encoding="utf-8").write(hub(content, themes, a.recommend, base, roles, not a.no_standard, client_tokens, a.out, seo))
    print(f"wrote {written} pages + hub to {a.out}")
    if DASH_HITS:
        print(f"\nwarning: {len(DASH_HITS)} string(s) contained an em/en dash and were rewritten with a comma. Fix the content file:")
        for h in DASH_HITS[:10]:
            print("  -", h)


if __name__ == "__main__":
    main()
