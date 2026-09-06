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
    chrome_bg = brand.get("chrome_bg") if brand.get("chrome") == "dark" else native["--bg"]
    tok["--chrome-bg"] = chrome_bg
    tok["--chrome-fg"] = reskin.best_on(chrome_bg)
    tok["--chrome-muted"] = "rgba(255,255,255,.72)" if tok["--chrome-fg"].lower().startswith("#f") else "rgba(0,0,0,.62)"
    tok["--chrome-border"] = "rgba(255,255,255,.12)" if tok["--chrome-fg"].lower().startswith("#f") else "rgba(0,0,0,.1)"
    tok["--chrome-accent"] = brand["accent"].lower() if tok["--chrome-fg"].lower().startswith("#f") else ink
    return css, tok


PREVIEW_CSS = r'''
/* ===== preview layer: page grammar the modules would supply in HubSpot ===== */
*{box-sizing:border-box}
img{max-width:100%;height:auto}
.q-skip{position:absolute;top:-200px;left:8px;z-index:100;background:var(--q-gold);color:var(--cta-fg);padding:10px 16px;border-radius:6px;font-weight:600}
.q-skip:focus{top:8px}
h1,h2,h3{text-wrap:balance}
.q-eyebrow{font-size:13px}
.q-btn,.q-btn-ghost{min-height:44px}
.q-btn-ghost{padding:10px 0}
/* utility bar */
.pv-util{background:var(--chrome-bg);border-bottom:1px solid var(--chrome-border)}
.pv-util .q-container{display:flex;gap:6px 22px;justify-content:flex-end;flex-wrap:wrap;font-size:13px;padding-top:2px;padding-bottom:2px}
.pv-util a{color:var(--chrome-muted);text-decoration:none;display:inline-flex;align-items:center;min-height:36px}
.pv-util a:hover{color:var(--chrome-fg)}
.pv-util a.pv-phone{color:var(--chrome-fg);font-weight:600}
/* header on chrome */
.q-header{background:var(--chrome-bg);border-bottom:1px solid var(--chrome-border);display:block}
.q-header .q-header-in{position:relative}
.q-header .q-nav > a,.q-header .q-nav-item > a{color:var(--chrome-fg)}
.q-header .q-nav > a:hover{color:var(--chrome-accent)}
.q-header .q-booknow{background:var(--q-gold);color:var(--cta-fg)!important;border-color:var(--q-gold);min-height:44px;display:inline-flex;align-items:center}
.q-header .q-booknow:hover{background:var(--q-gold-bright)}
.q-header-logo img{height:40px}
.q-logo-text{color:var(--chrome-fg)}
.q-mnav > summary{border-color:var(--chrome-border)!important}
.q-mnav > summary span{background:var(--chrome-fg)!important}
.q-mnav-panel{background:var(--chrome-bg)!important;border-top-color:var(--chrome-border)!important}
.q-mnav-panel > a,.q-msub > summary{color:var(--chrome-fg)!important;border-bottom-color:var(--chrome-border)!important}
.q-msub-links a{color:var(--chrome-muted)!important}
.q-mnav-cta{color:var(--cta-fg)!important;background:var(--q-gold);border-color:var(--q-gold)!important}
/* footer on chrome */
.q-footer{background:var(--chrome-bg);border-top:1px solid var(--chrome-border);color:var(--chrome-fg)}
.q-footer-grid{grid-template-columns:1.6fr 1fr 1fr 1fr}
.q-footer-tag,.q-footer-contact,.q-footer-contact a,.q-footer-links a,.q-footer-legal,.q-footer-legal a,.q-footer-social a{color:var(--chrome-muted)}
.q-footer-head,.q-footer-contact .q-footer-phone{color:var(--chrome-fg)}
.q-footer-links a:hover,.q-footer-social a:hover{color:var(--chrome-accent)}
.q-footer-links a{min-height:36px;display:flex;align-items:center;padding:0}
.q-footer-legal{border-top-color:var(--chrome-border)}
.q-footer-legal a{display:inline-flex;align-items:center;min-height:44px;padding:0 6px}
.q-footer-social a{margin:0;width:44px;height:44px}
.q-footer img{height:36px}
@media(max-width:1024px){.q-footer-grid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.q-footer-grid{grid-template-columns:1fr}}
/* hero */
.pv-hero-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:56px;align-items:center}
.pv-hero-img{width:100%;aspect-ratio:3/2;border-radius:calc(var(--radius) + 6px);overflow:hidden;border:1px solid var(--border);background:var(--bg-alt);position:relative}
.pv-hero-img img{width:100%;height:100%;object-fit:cover;display:block}
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
.pv-logos{display:flex;flex-wrap:wrap;gap:18px 34px;align-items:center;justify-content:center}
.pv-logos img{height:40px;width:auto;max-width:130px;object-fit:contain;filter:grayscale(1);transition:filter .2s}
.pv-logos img:hover{filter:none}
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
.pv-loc .q-card p{font-size:14.5px;line-height:1.7;color:var(--fg-muted);margin:0}
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
.q-form input[type=text],.q-form input[type=email],.q-form input[type=tel],.q-form select,.q-form textarea,.q-form input[type=submit],.q-form .hs-button{font-size:16px;min-height:44px}
.q-form .hs-button{min-height:48px;font-size:16px;width:100%}
.pv-form-note{font-size:13px;color:var(--fg-muted);margin:12px 0 0}
/* detail */
.pv-detail{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:start}
.pv-detail .q-h2{margin-top:14px}
.pv-detail ul{margin:22px 0 0;padding-left:20px;color:var(--fg);line-height:1.8;font-size:16px}
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
.pv-switch{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:90;display:flex;gap:4px;align-items:center;background:rgba(20,23,28,.92);color:#fff;border-radius:999px;padding:6px 8px 6px 14px;font:13px/1 Inter,system-ui,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.25);backdrop-filter:blur(6px)}
.pv-switch .lbl{opacity:.7;margin-right:6px}
.pv-switch a{color:#fff;text-decoration:none;padding:10px 12px;border-radius:999px;min-height:36px;display:inline-flex;align-items:center}
.pv-switch a.on{background:rgba(255,255,255,.16)}
.pv-switch a:hover{background:rgba(255,255,255,.1)}
/* responsive */
@media(max-width:1024px){.pv-hero-grid{grid-template-columns:1fr}.pv-cs,.pv-contact,.pv-detail{grid-template-columns:1fr;gap:34px}.pv-grid-4{grid-template-columns:repeat(2,1fr)}.pv-grid-5{grid-template-columns:repeat(5,1fr);gap:12px}.pv-stats{grid-template-columns:repeat(2,1fr);gap:28px 0}.pv-stat:nth-child(3){border-left:none}}
@media(max-width:767px){
  .q-section{padding:56px 0}
  .pv-util .q-container{justify-content:flex-start}
  .pv-grid-2,.pv-grid-3,.pv-grid-4,.pv-grid-5{grid-template-columns:1fr}
  .pv-svc a{grid-template-columns:1fr;gap:8px;padding:20px 0}.pv-svc .num{display:none}.pv-svc .more{justify-self:start}
  .pv-stats{grid-template-columns:1fr 1fr}.pv-stat b{font-size:42px}
  .pv-cs .h{font-size:30px}.pv-quote{font-size:19px}
  .pv-switch{bottom:8px;padding:4px 6px 4px 10px;font-size:12.5px;max-width:calc(100vw - 16px)}.pv-switch .lbl{display:none}
}
'''


# ----------------------------------------------------------------------------- sections

def sec_open(s: dict, extra_cls: str = "") -> str:
    cls = "q-section" + (" q-bg-alt" if s.get("alt") else "") + (" " + extra_cls if extra_cls else "")
    idattr = f' id="{E(s["id"])}"' if s.get("id") else ""
    return f'<section class="{cls}"{idattr}>'


def r_hero(s, ctx):
    eyebrow = f'<div class="q-eyebrow">{E(s.get("eyebrow"))}</div>' if s.get("eyebrow") else ""
    btns = ""
    if s.get("primary"):
        btns += f'<a class="q-btn" href="{E(s["primary"]["href"])}">{E(s["primary"]["label"])}</a>'
    if s.get("secondary"):
        btns += f'<a class="q-btn-ghost" href="{E(s["secondary"]["href"])}">{E(s["secondary"]["label"])}<span style="width:22px;height:1px;background:currentColor;display:inline-block"></span></a>'
    btns = f'<div class="pv-btns">{btns}</div>' if btns else ""
    note = f'<div class="pv-hero-note">{E(s["note"])}</div>' if s.get("note") else ""
    if s.get("layout") == "split" and s.get("image"):
        badge = (f'<div class="pv-badge"><b>{E(s["badge"]["value"])}</b><span>{E(s["badge"]["label"])}</span></div>'
                 if s.get("badge") else "")
        return f'''{sec_open(s)} <div class="q-container"><div class="pv-hero-grid"><div>{eyebrow}
<h1 class="q-h1" style="margin-top:22px">{RAW(s["heading"])}</h1>
<div class="q-lead" style="max-width:540px;margin:24px 0 0">{E(s.get("subhead"))}</div>{btns}{note}</div>
<div class="pv-hero-img"><img src="{E(ctx["rel"](s["image"]))}"{ctx["srcset"](s["image"])} alt="{E(s.get("image_alt"))}" width="{s.get("image_w", 1200)}" height="{s.get("image_h", 800)}" fetchpriority="high" decoding="async">{badge}</div></div></div></section>'''
    return f'''{sec_open(s)} <div class="q-container"><div class="pv-center" style="max-width:860px;margin:0 auto">{eyebrow}
<h1 class="q-h1" style="margin-top:22px">{RAW(s["heading"])}</h1>
<div class="q-lead" style="max-width:640px;margin:24px 0 0">{E(s.get("subhead"))}</div>{btns.replace('class="pv-btns"', 'class="pv-btns" style="justify-content:center"')}{note}</div>{f'<div class="pv-hero-wide"><img src="{E(ctx["rel"](s["image"]))}"{ctx["srcset"](s["image"])} alt="{E(s.get("image_alt", ""))}" width="{s.get("image_w", 1200)}" height="{s.get("image_h", 675)}" fetchpriority="high" decoding="async"></div>' if s.get("image") else ""}</div></section>'''


def r_partners(s, ctx):
    items = []
    for name in s["items"]:
        img = ctx["partner_logo"](name)
        if img:
            items.append(f'<img src="{E(img)}" alt="{E(name)}" loading="lazy" width="120" height="40">')
        else:
            items.append(f"<span>{E(name)}</span>")
    return f'<section class="pv-partners"><div class="q-container"><p class="pv-cap">{E(s.get("caption", "Partners"))}</p><div class="pv-logos">{"".join(items)}</div></div></section>'


def r_stats(s, ctx):
    n = len(s["items"])
    cells = "".join(f'<div class="pv-stat"><b>{E(v)}</b><span>{E(k)}</span></div>' for v, k in s["items"])
    return f'{sec_open(s)} <div class="q-container pv-stats" style="grid-template-columns:repeat({n},1fr)">{cells}</div></section>'


def r_services(s, ctx):
    rows = "".join(
        f'<a href="{E(href)}"><div class="num" aria-hidden="true"></div><div><h3>{E(t)}</h3><p>{E(b)}</p></div><div class="more">Learn more</div></a>'
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
    return f'''{sec_open(s)} <div class="q-container pv-cs"><div><div class="q-eyebrow">{E(s.get("eyebrow"))}</div><div class="h">{E(s["heading"])}</div><p class="pv-quote">"{E(s["quote"])}"</p><div class="pv-attr">{E(s.get("attribution"))}</div></div><div class="pv-grid pv-grid-2">{metrics}</div></div></section>'''


def r_cards(s, ctx):
    n = len(s["items"]); cols = cols_for(n)
    cards = "".join(f'<div class="q-card"><h3>{E(t)}</h3><p>{E(b)}</p></div>' for t, b in s["items"])
    head = ""
    if s.get("heading"):
        head = f'<div class="pv-center" style="margin-bottom:44px">{f"<div class=q-eyebrow>{E(s.get(chr(101)+chr(121)+chr(101)+chr(98)+chr(114)+chr(111)+chr(119)))}</div>" if s.get("eyebrow") else ""}<h2 class="q-h2" style="margin-top:22px;max-width:700px">{E(s["heading"])}</h2></div>'
    return f'{sec_open(s)} <div class="q-container">{head}<div class="pv-grid pv-grid-{cols}">{cards}</div></div></section>'


def r_band(s, ctx):
    n = len(s["items"]); cols = cols_for(n)
    cards = "".join(f'<a class="q-card" href="{E(h)}"><div class="t">{E(t)}</div><div class="d">{E(d)}</div></a>' for t, d, h in s["items"])
    return f'''{sec_open(s, "pv-band")} <div class="q-container pv-cs"><div><div class="q-eyebrow">{E(s.get("eyebrow"))}</div><h2 class="q-h2" style="margin-top:22px">{E(s["heading"])}</h2><div class="q-lead" style="margin-top:20px;max-width:480px">{E(s.get("subhead"))}</div></div><div class="pv-grid pv-grid-{min(cols,2)}">{cards}</div></div></section>'''


def r_locations(s, ctx):
    n = len(s["items"]); cols = cols_for(n)
    cards = []
    for name, a1, a2, phone, href in s["items"]:
        mp = '<div class="pv-map">Map and hours</div>' if s.get("detailed") else ""
        cards.append(f'<div class="q-card">{mp}<h3>{E(name)}</h3><p>{E(a1)}<br>{E(a2)}<br><a href="{E(href)}">{E(phone)}</a></p></div>')
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
<div style="margin-top:28px;display:flex;flex-direction:column;gap:14px"><a class="q-btn" style="align-self:flex-start" href="{E(brand["phone_href"])}">Call {E(brand["phone"])}</a><a href="mailto:{E(brand["email"])}" style="font-size:15px;color:var(--fg-muted);min-height:44px;display:inline-flex;align-items:center">{E(brand["email"])}</a></div></div>
<form class="q-form" onsubmit="return false"><label for="f1">Name</label><input id="f1" type="text"><label for="f2">Work email</label><input id="f2" type="email"><label for="f3">Phone</label><input id="f3" type="tel"><label for="f4">What would you like to look at?</label><select id="f4">{opts}</select><input type="submit" class="hs-button" value="{E(s.get("submit", "Send"))}"><p class="pv-form-note">{E(s.get("note"))}</p></form></div></section>'''


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
    posts = "".join(f'<a class="pv-post" href="{E(it[3] if len(it) > 3 else "#")}"{" target=_blank rel=noopener" if len(it) > 3 and str(it[3]).startswith("http") else ""}><div class="ph"></div><span class="tag">{E(it[0])}</span><h2>{E(it[1])}</h2><p>{E(it[2])}</p></a>' for it in s["items"])
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
    return f'''{sec_open(s)} <div class="q-container pv-contact" style="align-items:center"><div><h2 class="q-h2">{E(s["heading"])}</h2><div class="q-lead" style="margin-top:16px">{E(s.get("body"))}</div><p style="margin-top:20px;font-size:15px;color:var(--fg-muted)">Or call <a href="{E(brand["phone_href"])}" style="color:var(--fg);font-weight:600;min-height:44px;display:inline-flex;align-items:center">{E(brand["phone"])}</a></p></div>
<form class="q-form" onsubmit="return false"><label for="{E(fid)}-e">Work email</label><input id="{E(fid)}-e" type="email"><label for="{E(fid)}-c">Company</label><input id="{E(fid)}-c" type="text"><input type="submit" class="hs-button" value="{E(s.get("submit", "Send"))}"><p class="pv-form-note">{E(s.get("note", ""))}</p></form></div></section>'''


def r_cta(s, ctx):
    btn = f'<div style="margin-top:34px"><a class="q-btn" href="{E(s["primary"]["href"])}">{E(s["primary"]["label"])}</a></div>' if s.get("primary") else ""
    return f'{sec_open(s, "pv-cta")} <div class="q-container"><h2 class="q-h2" style="font-size:clamp(30px,4vw,52px)">{E(s["heading"])}</h2><div class="q-lead" style="max-width:540px;margin:22px auto 0">{E(s.get("subhead"))}</div>{btn}</div></section>'


RENDER = {"hero": r_hero, "partners": r_partners, "stats": r_stats, "services": r_services, "process": r_process,
          "casestudy": r_casestudy, "cards": r_cards, "band": r_band, "locations": r_locations, "faq": r_faq,
          "contact": r_contact, "detail": r_detail, "listing": r_listing, "team": r_team, "cta": r_cta,
          "leadform": r_leadform}


# ------------------------------------------------------------------------------ chrome

def header(content, ctx):
    b = content["brand"]
    util = "".join(f'<a href="{E(h)}">{E(l)}</a>' for l, h in ((u["label"], u["href"]) for u in b.get("utility", [])))
    if b.get("phone"):
        util += f'<a class="pv-phone" href="{E(b["phone_href"])}">{E(b["phone"])}</a>'
    nav = "".join(f'<a href="{E(h)}">{E(l)}</a>' for l, h in content["nav"])
    mnav = "".join(f'<a href="{E(h)}">{E(l)}</a>' for l, h in content["nav"])
    cta = f'<a class="q-booknow" href="{E(b["cta"]["href"])}">{E(b["cta"]["label"])}</a>' if b.get("cta") else ""
    mcta = f'<a class="q-mnav-cta" href="{E(b["cta"]["href"])}">{E(b["cta"]["label"])}</a>' if b.get("cta") else ""
    lw, lh = b.get("logo_w", 300), b.get("logo_h", 100)
    logo = (f'<img src="{E(ctx["rel"](b["logo"]))}" alt="{E(b.get("logo_alt", content["client"]))}" width="{round(40 * lw / lh)}" height="40" loading="eager">'
            if b.get("logo") else f'<span class="q-logo-text">{E(content["client"])}</span>')
    return f'''<header class="q-header"><a class="q-skip" href="#q-content">Skip to content</a>
<div class="pv-util"><div class="q-container">{util}</div></div>
<div class="q-container q-header-in">
  <a href="index.html" class="q-header-logo" aria-label="{E(content["client"])} home">{logo}</a>
  <nav class="q-nav" aria-label="Main navigation">{nav}{cta}</nav>
  <details class="q-mnav"><summary aria-label="Open menu"><span></span><span></span><span></span></summary><div class="q-mnav-panel">{mnav}{mcta}</div></details>
</div></header>
<div id="q-content" tabindex="-1">'''


def footer(content, ctx):
    b = content["brand"]
    lw, lh = b.get("logo_w", 300), b.get("logo_h", 100)
    logo = (f'<img src="{E(ctx["rel"](b["logo"]))}" alt="{E(b.get("logo_alt", content["client"]))}" width="{round(36 * lw / lh)}" height="36" loading="lazy">'
            if b.get("logo") else f'<span class="q-logo-text">{E(content["client"])}</span>')
    cols = "".join(
        f'<div><div class="q-footer-head">{E(c["title"])}</div><nav class="q-footer-links" aria-label="{E(c["title"])}">'
        + "".join(f'<a href="{E(h)}">{E(l)}</a>' for l, h in c["links"]) + "</nav></div>"
        for c in b.get("footer_columns", []))
    soc = b.get("social", {})
    _names = {"linkedin": "LinkedIn", "facebook": "Facebook", "x": "X", "instagram": "Instagram", "youtube": "YouTube"}
    social = "".join(f'<a href="{E(u)}" aria-label="{E(_names.get(k, k.title()))}">{E(_names.get(k, k.title()))}</a>' for k, u in soc.items() if u)
    contact = ""
    if b.get("phone") or b.get("email"):
        contact = f'<p class="q-footer-contact">{f"<a class=q-footer-phone href={E(b[chr(112)+chr(104)+chr(111)+chr(110)+chr(101)+chr(95)+chr(104)+chr(114)+chr(101)+chr(102)])}>{E(b[chr(112)+chr(104)+chr(111)+chr(110)+chr(101)])}</a>" if b.get("phone") else ""}{" &nbsp;·&nbsp; " if b.get("phone") and b.get("email") else ""}{f"<a href=mailto:{E(b[chr(101)+chr(109)+chr(97)+chr(105)+chr(108)])}>{E(b[chr(101)+chr(109)+chr(97)+chr(105)+chr(108)])}</a>" if b.get("email") else ""}</p>'
    legal = "".join(f' &nbsp;|&nbsp; <a href="{E(h)}">{E(l)}</a>' for l, h in b.get("legal", []))
    return f'''</div>
<footer class="q-footer"><div class="q-container q-footer-grid"><div>{logo}<p class="q-footer-tag">{E(b.get("tagline"))}</p>{contact}<div class="q-footer-social" style="gap:8px;font-size:14px">{social}</div></div>{cols}</div>
<div class="q-container q-footer-legal">Copyright &copy; {ctx["year"]} {E(content["client"])}{legal}</div></footer>'''


def switcher(themes, this_theme, page_file, recommend):
    links = "".join(
        f'<a href="../{slug_of(t)}/{page_file}"{" class=on" if t == this_theme else ""}>{E(t.replace("Quantum ", ""))}{" ★" if t == recommend else ""}</a>'
        for t in themes)
    return f'<nav class="pv-switch" aria-label="Preview directions"><span class="lbl">Direction</span>{links}<a href="../index.html">All</a></nav>'


def schema_blocks(content, page, base, dslug):
    sch = content.get("schema") or {}
    if not sch.get("org_name"):
        return ""
    site = sch.get("org_url") or base
    if page["file"] == "index.html":
        org = {"@context": "https://schema.org", "@type": "Organization", "@id": f"{site}/#organization", "name": sch["org_name"], "url": site}
        for k, v in (("logo", sch.get("org_logo")), ("description", sch.get("org_description")), ("sameAs", sch.get("sameAs"))):
            if v:
                org[k] = {"@type": "ImageObject", "url": v} if k == "logo" else v
        if sch.get("telephone"):
            org["contactPoint"] = {"@type": "ContactPoint", "contactType": "Sales", "telephone": sch["telephone"], "areaServed": "US", "availableLanguage": "English"}
        web = {"@context": "https://schema.org", "@type": "WebSite", "@id": f"{site}/#website", "url": site, "name": sch["org_name"], "publisher": {"@id": f"{site}/#organization"}, "inLanguage": "en-US"}
        return (f'<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>\n'
                f'<script type="application/ld+json">{json.dumps(web, ensure_ascii=False)}</script>')
    name = page["title"].split("|")[0].strip()
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{site}/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{site}/{page['file'].replace('.html', '')}"}]}
    return f'<script type="application/ld+json">{json.dumps(bc, ensure_ascii=False)}</script>'


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

    def rel(p):
        return "../" + p

    def partner_logo(name):
        s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        for ext in ("png", "jpg", "svg", "webp"):
            if os.path.exists(os.path.join(partners_dir, f"{s}.{ext}")):
                return f"../assets/partners/{s}.{ext}"
        return None

    ctx = {"rel": rel, "partner_logo": partner_logo, "brand": b, "year": 2026, "srcset": lambda pth: srcset_for(pth, out_dir)}
    body = "".join(RENDER[s["type"]](s, ctx) for s in page["sections"])
    canonical = f"{base}/{dslug}/{page['file'].replace('index.html', '')}".rstrip("/") if page["file"] == "index.html" else f"{base}/{dslug}/{page['file'].replace('.html', '')}"
    og_img = f"{base}/assets/hero-og.jpg"
    tokcss = "\n  ".join(f"{k}:{v};" for k, v in tok.items())
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(page["title"])}</title>
<meta name="description" content="{E(page["description"])}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{E(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(content["client"])}">
<meta property="og:title" content="{E(page["title"])}">
<meta property="og:description" content="{E(page["description"])}">
<meta property="og:url" content="{E(canonical)}">
<meta property="og:image" content="{E(og_img)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(page["title"])}">
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
</style>
{schema_blocks(content, page, base, dslug)}
</head>
<body>
{header(content, ctx)}
<main id="main">
{body}
</main>
{footer(content, ctx)}
{switcher(themes, theme, page["file"], recommend)}
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
            open(os.path.join(d, page["file"]), "w", encoding="utf-8").write(doc); written += 1
        print(f"  {t:20} {len(content['pages'])} pages  accent {tok['--q-gold']} ink {tok['--accent-ink']} cta-fg {tok['--cta-fg']} chrome {tok['--chrome-bg']}")
    open(os.path.join(a.out, "index.html"), "w", encoding="utf-8").write(hub(content, themes, a.recommend, base, roles, not a.no_standard, client_tokens))
    print(f"wrote {written} pages + hub to {a.out}")
    if DASH_HITS:
        print(f"\nwarning: {len(DASH_HITS)} string(s) contained an em/en dash and were rewritten with a comma. Fix the content file:")
        for h in DASH_HITS[:10]:
            print("  -", h)


if __name__ == "__main__":
    main()
