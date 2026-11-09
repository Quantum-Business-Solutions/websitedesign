"""Motion and 3D section types for scripts/preview.py: finder, showcase3d, portal, network, stats3d.

Pure CSS, inline SVG and vanilla JS. Every colour comes from the theme variables the re-skin writes
(--card, --border, --fg, --fg-muted, --bg-alt, --q-gold, --accent-ink, --cta-fg, --chrome-*), so the
three directions pick them up. Server HTML is complete without JS (finder shows every product, the 3D
carousel is a scroll-snap list, the portal shows its sign-in state, the network shows a list, the
stats show their final values). MOTION_JS upgrades them. prefers-reduced-motion: no tilt, no float,
no dash flow, no count-up, no scroll progress animation; state changes happen instantly.

Registered in preview.py as RENDER_EXTRA3, EXTRA_CSS3 and MOTION_JS. Each renderer takes (section, ctx).
Rules: no em or en dashes (E() rewrites any that slip in), nothing under 13px, 44px tap targets.
"""
from __future__ import annotations

import json
import math
import re


def _head(s, ctx, center=True):
    E = ctx["E"]
    eb = f'<div class="q-eyebrow">{E(s["eyebrow"])}</div>' if s.get("eyebrow") else ""
    intro = f'<p class="q-lead" style="max-width:660px;margin:16px auto 0">{E(s["intro"])}</p>' if s.get("intro") else ""
    h = f'<h2 class="q-h2" style="margin-top:22px;max-width:760px">{E(s["heading"])}</h2>' if s.get("heading") else ""
    return f'<div class="pv-center mo-head">{eb}{h}{intro}</div>'


def _chip_link(name, L, E):
    """A product chip links to the matching product or system page when one exists; otherwise plain text."""
    import preview_polish
    h = preview_polish.product_href(name)
    return f'<a class="pv-chip-a" href="{E(L(h))}">{E(name)}</a>' if h else E(name)


def _slug(x):
    return re.sub(r"[^a-z0-9]+", "-", str(x).lower()).strip("-")


# ----------------------------------------------------------------------------- 1. finder

def _finder(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    fid = s.get("id", "finder")
    bl = s.get("buildings", [])
    nd = s.get("needs", [])

    def chips(kind, items, label):
        btns = [f'<button type="button" class="mo-chip" data-k="all" aria-pressed="true">All</button>']
        btns += [f'<button type="button" class="mo-chip" data-k="{E(i["key"])}" aria-pressed="false">{E(i["label"])}</button>' for i in items]
        return (f'<div class="mo-fnd-row" data-kind="{kind}" role="group" aria-label="{E(label)}"><span class="mo-fnd-lab">{E(label)}</span>'
                f'<div class="mo-chips">{"".join(btns)}</div></div>')

    cards = []
    for p in s.get("products", []):
        b = " ".join(p.get("buildings", []))
        n = " ".join(p.get("needs", []))
        img = (f'<div class="mo-fc-img"><img src="{E(rel(p["img"]))}" alt="" width="600" height="450" loading="lazy" decoding="async"></div>'
               if p.get("img") else "")
        cards.append(f'<li class="mo-fc" data-b="{E(b)}" data-n="{E(n)}"><a href="{E(L(p.get("href", "#")))}">{img}'
                     f'<div class="mo-fc-t"><h3>{E(p["name"])}</h3><p>{E(p.get("blurb", ""))}</p><span class="mo-go">View product</span></div></a></li>')
    total = len(cards)
    contact = E(L(s.get("contact_href", "contact.html")))
    empty = (f'<div class="mo-fnd-empty" hidden><h3>No product matches that pair yet</h3><p>Tell us the building and the problem and we will point you to the right system.</p>'
             f'<div class="mo-fnd-empty-btns"><a class="q-btn" href="{contact}">Talk to a specialist</a><button type="button" class="mo-reset">Reset filters</button></div></div>')
    return (f'{ctx["sec_open"](s)} <div class="q-container mo-fnd" id="{E(fid)}-w" data-mo="finder">{_head(s, ctx)}'
            f'<div class="mo-fnd-filters">{chips("b", bl, s.get("building_label", "Building type"))}{chips("n", nd, s.get("need_label", "What you need"))}'
            f'<p class="mo-count" role="status" aria-live="polite"><b data-count>{total}</b> <span data-unit>{"product" if total == 1 else "products"}</span></p></div>'
            f'<ul class="mo-fnd-grid">{"".join(cards)}</ul>{empty}</div></section>')


# ----------------------------------------------------------------------------- 2. showcase3d

def _showcase3d(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    items = s["items"][:9]
    cards = []
    dots = []
    for i, it in enumerate(items):
        name, img, href, blurb = (list(it) + ["", "", "#", ""])[:4]
        cards.append(f'<li class="mo-c3-card" data-i="{i}"><a href="{E(L(href))}" data-blurb="{E(blurb)}"><span class="mo-c3-in">'
                     f'<span class="mo-c3-img"><img src="{E(rel(img))}" alt="" width="600" height="600" loading="lazy" decoding="async" draggable="false"></span>'
                     f'<span class="mo-c3-n">{E(name)}</span></span></a></li>')
        dots.append(f'<button type="button" class="mo-c3-dot" aria-label="Show {E(name)}" data-i="{i}"></button>')
    first = items[0]
    cap = (f'<div class="mo-c3-cap" aria-live="polite"><h3 data-n>{E(first[0])}</h3><p data-b>{E(first[3] if len(first) > 3 else "")}</p>'
           f'<a class="q-btn" data-go href="{E(L(first[2]))}">{E(s.get("link_label", "View product"))}</a></div>')
    return (f'{ctx["sec_open"](s)} <div class="q-container mo-c3" data-mo="c3" id="{E(s.get("id", "showcase3d"))}-w">{_head(s, ctx)}'
            f'<div class="mo-c3-stage" tabindex="0" role="region" aria-roledescription="carousel" aria-label="{E(s.get("heading", "Products"))}">'
            f'<ul class="mo-c3-ring">{"".join(cards)}</ul><div class="mo-c3-floor" aria-hidden="true"></div></div>'
            f'<div class="mo-c3-ctl"><button type="button" class="mo-c3-btn" data-d="-1" aria-label="Previous product">&#8592;</button>'
            f'<div class="mo-c3-dots">{"".join(dots)}</div><button type="button" class="mo-c3-btn" data-d="1" aria-label="Next product">&#8594;</button></div>'
            f'{cap}<p class="mo-c3-hint">Drag, swipe or use the arrow keys</p></div></section>')


# ----------------------------------------------------------------------------- 3. portal

ICONS = {
    "docs": '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>',
    "cart": '<path d="M3 4h2l2.4 11h10.2L20 8H6.2"/><circle cx="9" cy="19.5" r="1.4"/><circle cx="17" cy="19.5" r="1.4"/>',
    "megaphone": '<path d="M4 10v4h3l7 4V6L7 10z"/><path d="M17.5 9.5a4 4 0 0 1 0 5M19.5 7a7.5 7.5 0 0 1 0 10"/>',
    "training": '<path d="M2.5 9 12 4.5 21.5 9 12 13.5z"/><path d="M6 11.5V16c0 1.4 2.7 3 6 3s6-1.600 6-3v-4.500M21.500 9v5.500"/>',
    "support": '<path d="M4 13v-1a8 8 0 0 1 16 0v1"/><rect x="3" y="13" width="4" height="6" rx="1.500"/><rect x="17" y="13" width="4" height="6" rx="1.500"/><path d="M19 19c0 1.500-2 2.500-5 2.500"/>',
    "quote": '<path d="M5 3h14v18l-3-2-2 2-2-2-2 2-2-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
}
PORTAL_LINKS = {"docs": "support/documentation.html", "cart": "support/become-a-dealer.html", "megaphone": "support/marketing.html",
                "training": "training.html", "support": "support.html", "quote": "support/get-a-quote.html"}
ICON_DEFAULT = '<circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/>'


def _icon(key):
    return f'<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS.get(key, ICON_DEFAULT)}</svg>'


def _portal(s, ctx):
    E, L = ctx["E"], ctx["L"]
    pid = s.get("id", "portal")
    buy = s.get("cta_href", "") if str(s.get("cta_href", "")).startswith("https://buy.dmp.com") else ""
    hmap = dict(PORTAL_LINKS)
    hmap["cart"] = buy or "support/become-a-dealer.html"

    def _tile(t):
        key = t[2] if len(t) > 2 else ""
        href = t[3] if len(t) > 3 and t[3] else hmap.get(key, "support/documentation.html")
        ext = ' rel="noopener"' if str(href).startswith("http") else ""
        return (f'<a class="mo-pt" href="{E(L(href))}"{ext}><span class="mo-pt-i">{_icon(key)}</span><h3>{E(t[0])}</h3><p>{E(t[1])}</p>'
                f'<span class="mo-pt-open" aria-hidden="true">Open</span></a>')
    tiles = "".join(_tile(t) for t in s.get("tiles", []))
    nav = "".join(f'<i style="width:{w}%"></i>' for w in (70, 55, 64, 48, 58))
    who = E(ctx.get("client_short", "Dealer"))
    lock = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>'
    cta = (f'<div class="mo-portal-cta"><a class="q-btn" href="{E(L(s["cta_href"]))}">{E(s["cta_label"])}</a></div>' if s.get("cta_href") and s.get("cta_label") else "")
    return (f'{ctx["sec_open"](s)} <div class="q-container mo-portal" data-mo="portal" id="{E(pid)}-w">{_head(s, ctx)}'
            f'<div class="mo-pwrap"><div class="mo-win" role="group" aria-label="Dealer portal preview">'
            f'<div class="mo-bar"><span class="mo-dots" aria-hidden="true"><i></i><i></i><i></i></span>'
            f'<span class="mo-url">{lock}<span>dealer sign-in</span></span><span class="mo-bar-r" aria-hidden="true"></span></div>'
            f'<div class="mo-screen"><div class="mo-login" data-login><div class="mo-login-card">'
            f'<span class="mo-tag">Preview</span><span class="mo-logo" aria-hidden="true">{who[:1]}</span><h3>{E(s.get("login_title", "Dealer sign-in"))}</h3>'
            f'<div class="mo-fld" aria-hidden="true"><span class="mo-fl">Dealer ID</span><span class="mo-fake"></span></div>'
            f'<div class="mo-fld" aria-hidden="true"><span class="mo-fl">Password</span><span class="mo-fake"></span></div>'
            f'<button type="button" class="q-btn mo-signin" data-signin aria-describedby="{E(pid)}-pn">{E(s.get("signin_label", "Sign in"))}</button>'
            f'<p class="mo-pnote" id="{E(pid)}-pn">Preview only. This shows an example dashboard; nothing is sent and no account is needed.</p></div></div>'
            f'<div class="mo-dash" data-dash aria-hidden="true"><div class="mo-side">{nav}</div>'
            f'<div class="mo-main"><div class="mo-dash-top"><div><b>{E(s.get("welcome", "Welcome back"))}</b><span>{E(s.get("welcome_sub", "Everything for your next install, in one place"))}</span></div>'
            f'<button type="button" class="mo-out" data-out tabindex="-1">{E(s.get("signout_label", "Sign out"))}</button></div>'
            f'<div class="mo-tiles">{tiles}</div></div></div></div></div></div>{cta}</div></section>')


# ----------------------------------------------------------------------------- 4. network

def _network(s, ctx):
    E = ctx["E"]
    nid = s.get("id", "network")
    nodes = s["nodes"][:8]
    n = len(nodes)
    rx, ry = 37.0, 36.0          # ring radii in percent of the stage box
    lines, pills, rows = [], [], []
    for i, nd in enumerate(nodes):
        a = -math.pi / 2 + i * 2 * math.pi / n
        x, y = 50 + rx * math.cos(a), 50 + ry * math.sin(a)
        side = "l" if x < 34 else ("r" if x > 66 else "c")
        vert = "u" if y > 55 else "d"
        lines.append(f'<line class="mo-ln" data-i="{i}" x1="50" y1="50" x2="{x:.2f}" y2="{y:.2f}" style="--d:{i * 0.35:.2f}s"/>')
        desc = nd[1] if len(nd) > 1 else ""
        pills.append(f'<div class="mo-nd" data-i="{i}" data-s="{side}{vert}" style="left:{x:.2f}%;top:{y:.2f}%"><button type="button" class="mo-nb" aria-expanded="false" aria-controls="{E(nid)}-d{i}">'
                     f'<span class="mo-nn" aria-hidden="true">{i + 1:02d}</span><span>{E(nd[0])}</span></button>'
                     f'<div class="mo-pop" id="{E(nid)}-d{i}" role="region" aria-label="{E(nd[0])}"><b>{E(nd[0])}</b><p>{E(desc)}</p></div></div>')
    return (f'{ctx["sec_open"](s)} <div class="q-container mo-net" data-mo="network" id="{E(nid)}-w">{_head(s, ctx)}'
            f'<div class="mo-stage"><svg class="mo-lines" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            f'<ellipse class="mo-orbit" cx="50" cy="50" rx="{rx}" ry="{ry}"/>{"".join(lines)}</svg>'
            f'<div class="mo-hub"><span class="mo-hub-r" aria-hidden="true"></span><b>{E(s.get("hub", ""))}</b></div>{"".join(pills)}</div></div></section>')


# ----------------------------------------------------------------------------- 5. stats3d

def _stats3d(s, ctx):
    E = ctx["E"]
    items = s["items"][:4]
    cells = []
    for i, (v, k) in enumerate(items):
        txt = str(v)
        _tcls = "" if re.match(r"^[^A-Za-z]*\d[\d,.]*\s*[%+kKmMbB]?\+?$", txt.strip()) else ' class="mo-sc-t"'
        cells.append(f'<div class="mo-sc" style="--z:{[1, 2, 3, 2][i % 4]}"><div class="mo-sc-in"><b data-num{_tcls}>{E(txt)}</b><span>{E(k)}</span></div></div>')
    return (f'<section class="q-section mo-stats"{(" id=" + chr(34) + E(s["id"]) + chr(34)) if s.get("id") else ""} data-mo="stats3d">'
            f'<div class="q-container"><div class="mo-sgrid" data-n="{len(items)}">{"".join(cells)}</div></div></section>')


RENDER_EXTRA3 = {"finder": _finder, "showcase3d": _showcase3d, "portal": _portal, "network": _network, "stats3d": _stats3d}


EXTRA_CSS3 = r"""
/* ===== motion layer: global polish ===== */
.mo-progress{position:fixed;left:0;top:0;height:3px;width:100%;transform:scaleX(0);transform-origin:0 50%;background:var(--q-gold);z-index:300;pointer-events:none}
@media print{.mo-progress{display:none}}
.mo-head{margin-bottom:44px}
.mo-go{display:inline-block;margin-top:14px;font-size:14px;font-weight:700;letter-spacing:.02em;color:var(--accent-ink)}
.mo-go::after{content:"\2192";margin-left:8px;display:inline-block;transition:transform .25s}
a:hover > .mo-go::after,a:hover .mo-go::after{transform:translateX(5px)}

/* ===== finder ===== */
.mo-fnd-filters{display:none;margin-bottom:30px}
html.pv-js .mo-fnd-filters{display:block}
.mo-fnd-row{display:flex;gap:14px 18px;align-items:flex-start;padding:14px 0;border-top:1px solid var(--border)}
.mo-fnd-row:nth-child(2){border-bottom:1px solid var(--border)}
.mo-fnd-lab{flex:0 0 150px;font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--fg-muted);padding-top:13px}
.mo-chips{display:flex;flex-wrap:wrap;gap:8px}
.mo-chip{min-height:44px;padding:0 18px;border-radius:999px;border:1px solid var(--border);background:var(--card);color:var(--fg);font:600 15px/1 var(--q-sans);cursor:pointer;transition:background .2s,color .2s,border-color .2s,transform .2s}
.mo-chip:hover{border-color:var(--q-gold);transform:translateY(-1px)}
.mo-chip[aria-pressed=true]{background:var(--q-gold);border-color:var(--q-gold);color:var(--cta-fg)}
.mo-chip:focus-visible,.mo-reset:focus-visible,.mo-c3-btn:focus-visible,.mo-c3-dot:focus-visible,.mo-nb:focus-visible,.mo-signin:focus-visible,.mo-out:focus-visible{outline:3px solid var(--accent-ink);outline-offset:3px}
[data-dir="press"] .mo-chip{border-radius:2px}
.mo-count{margin:16px 0 0;font-size:15px;color:var(--fg-muted)}.mo-count b{font-family:var(--q-serif);font-size:30px;color:var(--accent-ink);font-variant-numeric:tabular-nums;margin-right:4px}
.mo-fnd-grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.mo-fc{transition:opacity .28s ease,transform .28s ease}
.mo-fc[hidden]{display:none}
.mo-fc.mo-out{opacity:0;transform:translateY(10px) scale(.97)}
.mo-fc.mo-pre{opacity:0;transform:translateY(14px) scale(.97)}
.mo-fc a{display:flex;flex-direction:column;height:100%;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;text-decoration:none;color:inherit;transition:box-shadow .3s,transform .3s,border-color .3s}
.mo-fc a:hover{box-shadow:0 22px 44px rgba(0,5,69,.14);transform:translateY(-4px);border-color:var(--q-gold)}
.mo-fc a:focus-visible{outline:3px solid var(--accent-ink);outline-offset:3px}
.mo-fc-img{aspect-ratio:4/3;background:var(--bg-alt);display:grid;place-items:center;overflow:hidden}
.mo-fc-img img{width:100%;height:100%;object-fit:contain;padding:14px;transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.mo-fc a:hover img{transform:scale(1.06)}
.mo-fc-t{padding:20px 22px 24px;display:flex;flex-direction:column;flex:1}
.mo-fc-t h3{margin:0 0 8px;font-size:19px;line-height:1.25;color:var(--fg)}
.mo-fc-t p{margin:0;font-size:15px;line-height:1.55;color:var(--fg-muted);flex:1}
.mo-fnd-empty{text-align:center;padding:56px 24px;border:1px dashed var(--border);border-radius:var(--radius);background:var(--card)}
.mo-fnd-empty[hidden]{display:none}
.mo-fnd-empty h3{margin:0 0 10px;font-size:22px;color:var(--fg)}.mo-fnd-empty p{margin:0 auto 22px;max-width:46ch;color:var(--fg-muted)}
.mo-fnd-empty-btns{display:flex;gap:18px;justify-content:center;align-items:center;flex-wrap:wrap}
.mo-reset{min-height:44px;background:none;border:0;color:var(--accent-ink);font:600 15px var(--q-sans);text-decoration:underline;text-underline-offset:4px;cursor:pointer}
@media(max-width:1024px){.mo-fnd-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:767px){.mo-fnd-grid{grid-template-columns:1fr}.mo-fnd-row{flex-direction:column;gap:4px}.mo-fnd-lab{flex:none;padding-top:0}
  .mo-chips{flex-wrap:nowrap;overflow-x:auto;max-width:100%;padding-bottom:6px;scrollbar-width:thin;scroll-snap-type:x proximity}.mo-chip{flex:none;scroll-snap-align:start}}

/* ===== 3D coverflow ===== */
.mo-c3-stage{position:relative;outline:none;border-radius:var(--radius)}
.mo-c3-stage:focus-visible{outline:3px solid var(--accent-ink);outline-offset:6px}
.mo-c3-ring{list-style:none;margin:0;padding:6px 4px 16px;display:flex;gap:20px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:thin}
.mo-c3-card{flex:0 0 min(260px,72vw);scroll-snap-align:center}
.mo-c3-card a{display:block;text-decoration:none;color:inherit}
.mo-c3-in{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--border);border-radius:calc(var(--radius) + 4px);overflow:hidden;box-shadow:0 16px 38px rgba(0,5,69,.12)}
.mo-c3-img{display:block;aspect-ratio:1/1;background:var(--bg-alt)}.mo-c3-img img{width:100%;height:100%;object-fit:contain;padding:18px;display:block}
.mo-c3-n{display:block;padding:16px 18px 18px;font:700 17px/1.25 var(--q-sans);color:var(--fg);text-align:center}
.mo-c3-floor,.mo-c3-hint{display:none}
.mo-c3-ctl,.mo-c3-cap{display:none}
html.pv-js .mo-c3-ctl{display:flex}html.pv-js .mo-c3-cap{display:block}
html.pv-js .mo-c3-hint{display:block}
/* upgraded: absolute ring with perspective */
.mo-c3.is-3d .mo-c3-stage{height:clamp(360px,44vw,500px);perspective:1400px;perspective-origin:50% 42%;overflow:hidden;touch-action:pan-y;cursor:grab;user-select:none;-webkit-user-select:none}
.mo-c3.is-3d .mo-c3-stage.is-drag{cursor:grabbing}
.mo-c3.is-3d .mo-c3-ring{position:absolute;inset:0;display:block;padding:0;overflow:visible;transform-style:preserve-3d}
.mo-c3.is-3d .mo-c3-card{position:absolute;left:50%;top:50%;width:clamp(200px,24vw,290px);margin:0;transform-style:preserve-3d;transition:transform .7s cubic-bezier(.2,.7,.2,1),opacity .5s;will-change:transform}
.mo-c3.is-3d .mo-c3-card a{-webkit-user-drag:none}
.mo-c3.is-3d .mo-c3-in{transform-style:preserve-3d;transition:transform .25s ease-out,box-shadow .4s,filter .5s}
.mo-c3-card.is-act .mo-c3-in{box-shadow:0 36px 70px rgba(0,5,69,.28);border-color:var(--q-gold)}
.mo-c3-card:not(.is-act) .mo-c3-in{filter:brightness(.9) saturate(.9)}
.mo-c3.is-3d .mo-c3-floor{display:block;position:absolute;left:12%;right:12%;bottom:8px;height:34px;background:radial-gradient(ellipse at center,rgba(0,5,69,.28),transparent 70%);filter:blur(6px);pointer-events:none}
.mo-c3-ctl{align-items:center;justify-content:center;gap:16px;margin-top:22px}
.mo-c3-btn{width:48px;height:48px;border-radius:50%;border:1px solid var(--border);background:var(--card);color:var(--fg);font-size:20px;cursor:pointer;transition:background .2s,color .2s,border-color .2s}
.mo-c3-btn:hover{background:var(--q-gold);color:var(--cta-fg);border-color:var(--q-gold)}
.mo-c3-dots{display:flex;gap:2px;align-items:center}
.mo-c3-dot{width:28px;height:44px;border:0;background:none;cursor:pointer;position:relative;padding:0}
.mo-c3-dot::after{content:"";position:absolute;left:50%;top:50%;width:10px;height:10px;border-radius:50%;transform:translate(-50%,-50%);background:var(--border);transition:background .25s,width .25s,border-radius .25s}
.mo-c3-dot[aria-current=true]::after{background:var(--q-gold);width:26px;border-radius:6px}
.mo-c3-cap{text-align:center;max-width:560px;margin:14px auto 0}
.mo-c3-cap h3{margin:0 0 8px;font-size:24px;color:var(--fg)}.mo-c3-cap p{margin:0 0 16px;color:var(--fg-muted);line-height:1.6;min-height:3.2em}
.mo-c3-hint{text-align:center;margin:18px 0 0;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--fg-muted)}
@media(max-width:767px){.mo-c3.is-3d .mo-c3-stage{height:340px}.mo-c3.is-3d .mo-c3-card{width:210px}}

/* ===== dealer portal mock ===== */
.mo-pwrap{perspective:1600px;max-width:1020px;margin:0 auto;padding:0 2px}
.mo-win{border-radius:calc(var(--radius) + 8px);background:var(--card);border:1px solid var(--border);overflow:hidden;box-shadow:0 40px 90px rgba(0,5,69,.22),0 8px 24px rgba(0,5,69,.1);transform:rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg)) translateY(var(--ty,0px));transform-style:preserve-3d;will-change:transform}
html.pv-js .mo-win{animation:mo-float 8s ease-in-out infinite}
@keyframes mo-float{0%,100%{translate:0 0}50%{translate:0 -8px}}
.mo-bar{display:flex;align-items:center;gap:14px;padding:12px 16px;background:var(--bg-alt);border-bottom:1px solid var(--border)}
.mo-dots{display:flex;gap:7px}.mo-dots i{width:11px;height:11px;border-radius:50%;background:var(--border)}.mo-dots i:first-child{background:#e5675e}.mo-dots i:nth-child(2){background:#e8b94a}.mo-dots i:nth-child(3){background:#58b35e}
.mo-url{flex:1;max-width:420px;margin:0 auto;display:flex;align-items:center;gap:8px;justify-content:center;padding:8px 16px;border-radius:999px;background:var(--card);border:1px solid var(--border);font-size:14px;color:var(--fg-muted)}
.mo-url svg{color:var(--accent-ink);flex:none}
.mo-bar-r{width:57px}
.mo-screen{position:relative;min-height:430px;background:var(--bg)}
.mo-login{position:absolute;inset:0;display:grid;place-items:center;padding:24px;background:radial-gradient(ellipse at 50% 0%,color-mix(in srgb,var(--q-gold) 14%,transparent),transparent 60%),var(--bg);transition:opacity .45s ease,transform .45s ease}
.mo-login-card{width:min(340px,100%);padding:34px 30px;border-radius:var(--radius);background:var(--card);border:1px solid var(--border);box-shadow:0 20px 44px rgba(0,5,69,.1);display:grid;gap:14px;text-align:center;justify-items:stretch}
.mo-logo{justify-self:center;width:52px;height:52px;border-radius:14px;background:var(--q-gold);color:var(--cta-fg);display:grid;place-items:center;font:800 24px var(--q-sans)}
.mo-login-card h3{margin:2px 0 6px;font-size:21px;color:var(--fg)}
.mo-fake{height:44px;border-radius:calc(var(--radius) - 2px);border:1px solid var(--border);background:var(--bg-alt);position:relative}
.mo-fake::after{content:"";position:absolute;left:14px;top:50%;width:46%;height:8px;margin-top:-4px;border-radius:4px;background:var(--border)}
.mo-fake + .mo-fake::after{width:30%;letter-spacing:4px}
.mo-signin{width:100%;justify-content:center;margin-top:4px;cursor:pointer}
.mo-dash{position:relative;display:grid;grid-template-columns:150px 1fr;min-height:430px;visibility:hidden;opacity:0}
.mo-screen.is-in .mo-login{opacity:0;transform:scale(.96);pointer-events:none;visibility:hidden;transition:opacity .4s,transform .4s,visibility 0s .4s}
.mo-screen.is-in .mo-dash{visibility:visible;opacity:1;transition:opacity .4s .15s}
.mo-side{background:var(--chrome-bg);padding:22px 18px;display:flex;flex-direction:column;gap:14px}
.mo-side i{display:block;height:10px;border-radius:5px;background:var(--chrome-border)}.mo-side i:first-child{background:var(--q-gold)}
.mo-main{padding:22px 26px 28px;min-width:0}
.mo-dash-top{display:flex;justify-content:space-between;align-items:center;gap:14px;margin-bottom:20px;flex-wrap:wrap}
.mo-dash-top b{display:block;font:800 22px/1.2 var(--q-sans);color:var(--fg)}.mo-dash-top span{font-size:14px;color:var(--fg-muted)}
.mo-out{min-height:44px;padding:0 16px;border-radius:999px;border:1px solid var(--border);background:var(--card);color:var(--fg);font:600 14px var(--q-sans);cursor:pointer}
.mo-out:hover{border-color:var(--q-gold)}
[data-dir="press"] .mo-out{border-radius:2px}
.mo-tiles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.mo-pt{position:relative;padding:18px 18px 20px;border-radius:var(--radius);background:var(--card);border:1px solid var(--border);box-shadow:0 8px 20px rgba(0,5,69,.06);opacity:0;transform:translateY(18px) scale(.94);transition:border-color .25s,box-shadow .25s}
.mo-screen.is-in .mo-pt{animation:mo-pop .55s cubic-bezier(.2,.8,.2,1) forwards;animation-delay:calc(.25s + var(--i,0)*.08s)}
@keyframes mo-pop{to{opacity:1;transform:none}}
.mo-pt:hover{border-color:var(--q-gold);box-shadow:0 16px 32px rgba(0,5,69,.12)}
.mo-pt-i{display:grid;place-items:center;width:46px;height:46px;border-radius:12px;background:color-mix(in srgb,var(--q-gold) 16%,var(--card));color:var(--accent-ink);margin-bottom:12px}
.mo-pt h3{margin:0 0 6px;font-size:16.5px;color:var(--fg)}.mo-pt p{margin:0;font-size:14px;line-height:1.5;color:var(--fg-muted)}
.mo-pt-open{display:inline-block;margin-top:12px;font-size:13px;font-weight:700;color:var(--accent-ink)}
.mo-portal-cta{text-align:center;margin-top:36px}
@media(max-width:1024px){.mo-tiles{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:767px){.mo-dash{grid-template-columns:1fr}.mo-side{display:none}.mo-tiles{grid-template-columns:1fr}.mo-main{padding:18px}.mo-url{font-size:13px}.mo-bar-r{display:none}.mo-screen{min-height:380px}}
@media(prefers-reduced-motion:reduce){html.pv-js .mo-win{animation:none}.mo-login,.mo-screen.is-in .mo-login,.mo-screen.is-in .mo-dash{transition:none}.mo-pt,.mo-screen.is-in .mo-pt{animation:none;opacity:1;transform:none}}

/* ===== network diagram ===== */
.mo-stage{position:relative;max-width:980px;margin:0 auto;aspect-ratio:16/10}
.mo-lines{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.mo-orbit{fill:none;stroke:var(--border);stroke-width:1;vector-effect:non-scaling-stroke;stroke-dasharray:2 6}
.mo-ln{stroke:var(--q-gold);stroke-width:2;vector-effect:non-scaling-stroke;stroke-linecap:round;stroke-dasharray:6 9;animation:mo-flow 1.6s linear infinite;animation-delay:var(--d,0s);opacity:.55;transition:opacity .25s,stroke-width .25s}
.mo-ln.on{opacity:1;stroke-width:3.5}
@keyframes mo-flow{to{stroke-dashoffset:-30}}
.mo-hub{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:clamp(120px,17vw,170px);aspect-ratio:1;border-radius:50%;display:grid;place-items:center;text-align:center;padding:14px;background:var(--chrome-bg);color:var(--chrome-fg);z-index:2;border:1px solid var(--chrome-border);box-shadow:0 20px 50px rgba(0,5,69,.22)}
.mo-hub b{font:800 clamp(15px,1.6vw,19px)/1.2 var(--q-sans);position:relative;z-index:1}
.mo-hub-r{position:absolute;inset:-12px;border-radius:50%;border:2px solid var(--q-gold);opacity:.5;animation:mo-pulse 3.2s ease-out infinite}
@keyframes mo-pulse{0%{transform:scale(.92);opacity:.7}100%{transform:scale(1.28);opacity:0}}
.mo-nd{position:absolute;transform:translate(-50%,-50%);z-index:3}
.mo-nd:hover,.mo-nd.on{z-index:6}
.mo-nb{display:flex;align-items:center;gap:10px;min-height:48px;max-width:190px;padding:8px 16px 8px 10px;border-radius:999px;border:1px solid var(--border);background:var(--card);color:var(--fg);font:700 14px/1.2 var(--q-sans);text-align:left;cursor:pointer;box-shadow:0 10px 24px rgba(0,5,69,.12);transition:border-color .25s,background .25s,transform .25s}
[data-dir="press"] .mo-nb{border-radius:4px}
.mo-nn{flex:none;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;background:var(--q-gold);color:var(--cta-fg);font-size:13px;font-weight:800}
.mo-nd.on .mo-nb{border-color:var(--q-gold);transform:scale(1.05)}
.mo-pop{position:absolute;width:250px;padding:16px 18px;border-radius:var(--radius);background:var(--card);border:1px solid var(--q-gold);box-shadow:0 24px 50px rgba(0,5,69,.22);opacity:0;visibility:hidden;transform:translateY(6px);transition:opacity .2s,transform .2s,visibility 0s .2s;pointer-events:none}
.mo-pop b{display:block;margin-bottom:6px;font-size:15px;color:var(--fg)}.mo-pop p{margin:0;font-size:14px;line-height:1.55;color:var(--fg-muted)}
.mo-nd.on .mo-pop{opacity:1;visibility:visible;transform:none;transition:opacity .2s,transform .2s}
.mo-nd[data-s$="d"] .mo-pop{top:calc(100% + 10px)}.mo-nd[data-s$="u"] .mo-pop{bottom:calc(100% + 10px)}
.mo-nd[data-s^="c"] .mo-pop{left:50%;margin-left:-125px}.mo-nd[data-s^="l"] .mo-pop{left:0}.mo-nd[data-s^="r"] .mo-pop{right:0}
@media(max-width:1024px){.mo-stage{aspect-ratio:4/3}.mo-nb{font-size:13px;max-width:150px}.mo-pop{width:220px}.mo-nd[data-s^="c"] .mo-pop{margin-left:-110px}}
@media(max-width:767px){
  .mo-stage{aspect-ratio:auto;display:flex;flex-direction:column;align-items:stretch;gap:0;padding-left:30px}
  .mo-lines{display:none}
  .mo-hub{position:relative;left:auto;top:auto;transform:none;width:auto;aspect-ratio:auto;border-radius:var(--radius);padding:18px;margin:0 0 26px -30px}
  .mo-hub-r{display:none}
  .mo-stage::before{content:"";position:absolute;left:14px;top:60px;bottom:30px;width:2px;background:repeating-linear-gradient(180deg,var(--q-gold) 0 6px,transparent 6px 12px);animation:mo-vflow 1s linear infinite}
  @keyframes mo-vflow{to{background-position:0 12px}}
  .mo-nd{position:relative;left:auto!important;top:auto!important;transform:none;margin-bottom:14px}
  .mo-nd::before{content:"";position:absolute;left:-23px;top:24px;width:16px;height:2px;background:var(--q-gold)}
  .mo-nb{max-width:none;width:100%;box-shadow:none;cursor:default}
  .mo-pop b{display:none}
  .mo-pop{position:static!important;margin:8px 0 0!important;width:auto;opacity:1;visibility:visible;transform:none;pointer-events:auto;box-shadow:none;border-color:var(--border);background:var(--bg-alt)}
}
@media(prefers-reduced-motion:reduce){.mo-ln,.mo-hub-r,.mo-stage::before{animation:none}.mo-ln{stroke-dasharray:none}.mo-hub-r{display:none}}

/* ===== stats3d ===== */
.mo-stats{background:var(--chrome-bg);color:var(--chrome-fg);overflow:hidden}
.mo-sgrid{display:grid;grid-template-columns:repeat(var(--n,4),minmax(0,1fr));gap:22px;perspective:1200px}
.mo-sgrid[data-n="3"]{--n:3}.mo-sgrid[data-n="4"]{--n:4}.mo-sgrid[data-n="2"]{--n:2}
.mo-sc{transform:translateY(var(--py,0px));transform-style:preserve-3d;will-change:transform}
.mo-sc-in{position:relative;padding:36px 22px 30px;border-radius:var(--radius);text-align:center;background:linear-gradient(160deg,color-mix(in srgb,var(--chrome-fg) 12%,var(--chrome-bg)),color-mix(in srgb,var(--chrome-fg) 4%,var(--chrome-bg)));border:1px solid var(--chrome-border);box-shadow:0 calc(8px*var(--z,1)) calc(18px*var(--z,1)) rgba(0,5,69,.16);transform:rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg)) translateZ(calc(var(--z,1)*6px));transition:transform .2s ease-out;overflow:hidden}
.mo-sc-in::before{content:"";position:absolute;inset:0;background:radial-gradient(260px circle at var(--px,50%) var(--py2,0%),color-mix(in srgb,var(--q-gold) 26%,transparent),transparent 60%);pointer-events:none}
.mo-sc-in::after{content:"";position:absolute;left:22%;right:22%;bottom:0;height:3px;background:var(--q-gold);border-radius:3px 3px 0 0}
.mo-sc b{display:block;position:relative;font:800 clamp(40px,5.2vw,72px)/1 var(--q-serif);letter-spacing:-.03em;color:var(--chrome-fg);font-variant-numeric:tabular-nums}
.mo-sc span{display:block;position:relative;margin-top:12px;font-size:15px;line-height:1.4;color:var(--chrome-muted)}
@media(max-width:1024px){.mo-sgrid{grid-template-columns:repeat(2,minmax(0,1fr))}.mo-sgrid[data-n="3"] .mo-sc:last-child{grid-column:1/-1}}
@media(max-width:480px){.mo-sgrid{gap:14px}.mo-sc-in{padding:28px 12px 24px}.mo-sc b{font-size:38px}}
@media(prefers-reduced-motion:reduce){.mo-sc{transform:none}.mo-sc-in{transform:none;transition:none}}
"""


MOTION_JS = r"""(function(){
var rm=matchMedia('(prefers-reduced-motion: reduce)').matches,fine=matchMedia('(pointer:fine)').matches,desk=function(){return matchMedia('(min-width:768px)').matches};
function $(r,s){return r.querySelector(s)}function $$(r,s){return [].slice.call(r.querySelectorAll(s))}
/* scroll progress bar */
if(!rm&&!document.querySelector('.mo-progress')){var pb=document.createElement('div');pb.className='mo-progress';pb.setAttribute('aria-hidden','true');document.body.appendChild(pb);var pr=0;
function pu(){pr=0;var h=document.documentElement.scrollHeight-innerHeight;pb.style.transform='scaleX('+(h>0?Math.min(1,scrollY/h):0).toFixed(4)+')'}
addEventListener('scroll',function(){if(!pr)pr=requestAnimationFrame(pu)},{passive:true});addEventListener('resize',pu);pu()}
/* magnetic primary buttons */
if(!rm&&fine){$$(document,'main .q-btn').forEach(function(b){if(b.classList.contains('mo-signin'))return;b.addEventListener('pointermove',function(e){var r=b.getBoundingClientRect(),x=(e.clientX-r.left-r.width/2)/r.width,y=(e.clientY-r.top-r.height/2)/r.height;b.style.transition='transform .15s ease-out';b.style.transform='translate('+(x*10).toFixed(1)+'px,'+(y*8).toFixed(1)+'px)'});b.addEventListener('pointerleave',function(){b.style.transition='transform .35s cubic-bezier(.2,.7,.2,1)';b.style.transform=''})})}

/* ---- finder ---- */
$$(document,'[data-mo=finder]').forEach(function(root){
var cards=$$(root,'.mo-fc'),cnt=$(root,'[data-count]'),unit=$(root,'[data-unit]'),empty=$(root,'.mo-fnd-empty'),sel={b:'all',n:'all'},first=true;
function has(c,att,k){if(k==='all')return true;var v=(c.getAttribute(att)||'').split(' ').filter(Boolean);return !v.length||v.indexOf(k)>-1}
function apply(){var shown=0;cards.forEach(function(c){var ok=has(c,'data-b',sel.b)&&has(c,'data-n',sel.n);if(ok)shown++;
if(rm||first){c.hidden=!ok;c.classList.remove('mo-out','mo-pre');return}
if(ok&&c.hidden){c.hidden=false;c.classList.remove('mo-out');c.classList.add('mo-pre');void c.offsetWidth;c.classList.remove('mo-pre')}
else if(ok){c.classList.remove('mo-out')}
else if(!c.hidden&&!c.classList.contains('mo-out')){c.classList.add('mo-out');(function(c){setTimeout(function(){if(c.classList.contains('mo-out'))c.hidden=true},280)})(c)}});
cnt.textContent=shown;unit.textContent=shown===1?'product':'products';empty.hidden=shown>0}
$$(root,'.mo-fnd-row').forEach(function(row){var kind=row.getAttribute('data-kind');$$(row,'.mo-chip').forEach(function(ch){ch.addEventListener('click',function(){sel[kind]=ch.getAttribute('data-k');$$(row,'.mo-chip').forEach(function(o){o.setAttribute('aria-pressed',o===ch?'true':'false')});apply()})})});
var rs=$(root,'.mo-reset');if(rs)rs.addEventListener('click',function(){sel={b:'all',n:'all'};$$(root,'.mo-chip').forEach(function(o){o.setAttribute('aria-pressed',o.getAttribute('data-k')==='all'?'true':'false')});apply()});
apply();first=false});

/* ---- 3D coverflow ---- */
$$(document,'[data-mo=c3]').forEach(function(root){
var stage=$(root,'.mo-c3-stage'),cards=$$(root,'.mo-c3-card'),dots=$$(root,'.mo-c3-dot'),n=cards.length,cur=0,nm=$(root,'[data-n]'),bl=$(root,'[data-b]'),go=$(root,'[data-go]');
root.classList.add('is-3d');
function lay(){var w=stage.clientWidth,cw=cards[0].offsetWidth,small=w<640,step=small?cw*.5:Math.min(cw*.72,w/4.2),ang=small?38:44,dz=small?120:170;
cards.forEach(function(c,i){var o=i-cur;if(o>n/2)o-=n;if(o<-n/2)o+=n;var a=Math.abs(o),vis=a<=(small?1:3),x=o*step+(o>0?cw*.1:o<0?-cw*.1:0)*(small?0:1);
c.style.transform='translate(-50%,-50%) translateX('+x.toFixed(1)+'px) translateZ('+(a===0?60:-a*dz*.55).toFixed(0)+'px) rotateY('+(o===0?0:(o>0?-ang:ang))+'deg) scale('+(a===0?1:Math.max(.72,1-a*.08)).toFixed(3)+')';
c.style.zIndex=String(50-a);c.style.opacity=vis?'1':'0';c.style.pointerEvents=vis?'auto':'none';c.classList.toggle('is-act',o===0);
var lk=$(c,'a');lk.tabIndex=o===0?0:-1;lk.setAttribute('aria-hidden',o===0?'false':'true');c.setAttribute('aria-label',(i+1)+' of '+n)});
dots.forEach(function(d,i){if(i===cur)d.setAttribute('aria-current','true');else d.removeAttribute('aria-current')});
var act=$(cards[cur],'a');nm.textContent=$(act,'.mo-c3-n').textContent;bl.textContent=act.getAttribute('data-blurb')||'';go.setAttribute('href',act.getAttribute('href'))}
function to(i){cur=(i%n+n)%n;lay()}
$$(root,'.mo-c3-btn').forEach(function(b){b.addEventListener('click',function(){to(cur+ +b.getAttribute('data-d'))})});
dots.forEach(function(d,i){d.addEventListener('click',function(){to(i)})});
stage.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){e.preventDefault();to(cur+1)}else if(e.key==='ArrowLeft'){e.preventDefault();to(cur-1)}else if(e.key==='Home'){e.preventDefault();to(0)}else if(e.key==='End'){e.preventDefault();to(n-1)}});
var sx=0,sc=0,drag=false,moved=false,id=null;
stage.addEventListener('pointerdown',function(e){if(e.button>0)return;sx=e.clientX;sc=cur;drag=true;moved=false;id=e.pointerId});
stage.addEventListener('pointermove',function(e){if(drag){var dx=e.clientX-sx;if(Math.abs(dx)>6&&!moved){moved=true;stage.classList.add('is-drag');try{stage.setPointerCapture(id)}catch(x){}}
if(moved){var cw=cards[0].offsetWidth*.6;var k=Math.round(-dx/cw);if(sc+k!==cur)to(sc+k)}return}
if(rm||!fine)return;var a=$(cards[cur],'.mo-c3-in'),r=a.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;if(Math.abs(x)<.9&&Math.abs(y)<.9)a.style.transform='rotateX('+(-y*12).toFixed(1)+'deg) rotateY('+(x*14).toFixed(1)+'deg)'});
function end(){if(!drag)return;drag=false;stage.classList.remove('is-drag');setTimeout(function(){moved=false},0)}
stage.addEventListener('pointerup',end);stage.addEventListener('pointercancel',end);
stage.addEventListener('pointerleave',function(){cards.forEach(function(c){$(c,'.mo-c3-in').style.transform=''})});
cards.forEach(function(c,i){$(c,'a').addEventListener('click',function(e){if(moved){e.preventDefault();return}if(i!==cur){e.preventDefault();to(i)}})});
addEventListener('resize',lay);lay()});

/* ---- portal ---- */
$$(document,'[data-mo=portal]').forEach(function(root){
var scr=$(root,'.mo-screen'),win=$(root,'.mo-win'),dash=$(root,'[data-dash]'),inb=$(root,'[data-signin]'),out=$(root,'[data-out]');
$$(root,'.mo-pt').forEach(function(t,i){t.style.setProperty('--i',i)});
function setIn(v){scr.classList.toggle('is-in',v);dash.setAttribute('aria-hidden',v?'false':'true');out.tabIndex=v?0:-1;if(v)setTimeout(function(){out.focus({preventScroll:true})},rm?0:450);else inb.focus({preventScroll:true})}
inb.addEventListener('click',function(){setIn(true)});out.addEventListener('click',function(){setIn(false)});
if(!rm&&fine){var raf=0;function tilt(){raf=0;var r=root.getBoundingClientRect(),c=(r.top+r.height/2-innerHeight/2)/innerHeight;c=Math.max(-1,Math.min(1,c));win.style.setProperty('--rx',(c*6).toFixed(2)+'deg');win.style.setProperty('--ry',(c*-3).toFixed(2)+'deg');win.style.setProperty('--ty',(c*14).toFixed(1)+'px')}
addEventListener('scroll',function(){if(!raf)raf=requestAnimationFrame(tilt)},{passive:true});tilt()}});

/* ---- network ---- */
$$(document,'[data-mo=network]').forEach(function(root){
var nds=$$(root,'.mo-nd'),lns=$$(root,'.mo-ln'),pin=-1;
function set(i){nds.forEach(function(d,j){var on=j===i;d.classList.toggle('on',on);$(d,'.mo-nb').setAttribute('aria-expanded',on?'true':'false')});lns.forEach(function(l,j){l.classList.toggle('on',j===i)})}
nds.forEach(function(d,i){var b=$(d,'.mo-nb');
d.addEventListener('pointerenter',function(e){if(e.pointerType==='mouse'&&desk())set(i)});
d.addEventListener('pointerleave',function(e){if(e.pointerType==='mouse'&&desk()&&pin!==i)set(pin)});
b.addEventListener('focus',function(){if(desk())set(i)});
b.addEventListener('blur',function(){if(desk()&&pin!==i)setTimeout(function(){if(!root.contains(document.activeElement)||document.activeElement===document.body)set(pin)},0)});
b.addEventListener('click',function(){if(!desk())return;pin=pin===i?-1:i;set(pin)})});
document.addEventListener('keydown',function(e){if(e.key==='Escape'){pin=-1;set(-1)}});
document.addEventListener('click',function(e){if(!root.contains(e.target)){pin=-1;set(-1)}})});

/* ---- stats3d ---- */
$$(document,'[data-mo=stats3d]').forEach(function(root){
var cs=$$(root,'.mo-sc');
if(!rm&&'IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;io.unobserve(e.target);var el=e.target,txt=el.textContent.trim();if(txt.indexOf('/')>-1)return;var m=txt.match(/^([^0-9]*)([0-9][0-9,]*)(\.[0-9]+)?(.*)$/);if(!m)return;var pre=m[1],dec=m[3]||'',suf=m[4],comma=m[2].indexOf(',')>-1,target=parseFloat(m[2].replace(/,/g,'')+dec),pl=dec?dec.length-1:0,t0=null;
function f(v){var s=v.toFixed(pl);if(comma){var p=s.split('.');p[0]=p[0].replace(/\B(?=(\d{3})+(?!\d))/g,',');s=p.join('.')}return pre+s+suf}
function st(ts){if(t0===null)t0=ts;var k=Math.min(1,(ts-t0)/1500);k=1-Math.pow(1-k,3);el.textContent=f(target*k);if(k<1)requestAnimationFrame(st);else el.textContent=txt}el.textContent=f(0);requestAnimationFrame(st)})},{threshold:.5});
$$(root,'[data-num]').forEach(function(b){io.observe(b)})}
if(!rm&&fine){cs.forEach(function(c){var a=$(c,'.mo-sc-in');c.addEventListener('pointermove',function(e){var r=a.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;a.style.setProperty('--rx',((.5-y)*14).toFixed(1)+'deg');a.style.setProperty('--ry',((x-.5)*16).toFixed(1)+'deg');a.style.setProperty('--px',(x*100).toFixed(0)+'%');a.style.setProperty('--py2',(y*100).toFixed(0)+'%')});c.addEventListener('pointerleave',function(){a.style.setProperty('--rx','0deg');a.style.setProperty('--ry','0deg')})})}
if(!rm&&desk()){var raf=0;function par(){raf=0;var r=root.getBoundingClientRect(),c=(r.top+r.height/2-innerHeight/2)/innerHeight;c=Math.max(-1,Math.min(1,c));cs.forEach(function(el,i){el.style.setProperty('--py',(c*(i%2?-1:1)*(10+i*5)).toFixed(1)+'px')})}
addEventListener('scroll',function(){if(!raf)raf=requestAnimationFrame(par)},{passive:true});par()}});
})();"""


# ----------------------------------------------------------------------------- 6. explorer
# A guided product explorer: vertical rail of systems with auto-advancing progress rings, a dark stage with a
# tilting product plate, "what it includes" chips joined to the product by animated connector lines, a platform
# strip and keyboard roving tabindex. Server HTML shows the first system and the rail as plain links (no JS).

_EX_ICONS = {
    "intrusion": '<path d="M12 3 4.5 6v5.5c0 4.4 3 8.2 7.5 9.5 4.5-1.3 7.5-5.1 7.5-9.500V6z"/><path d="m8.8 12.2 2.4 2.4 4.2-4.6"/>',
    "access": '<circle cx="8" cy="12" r="3.5"/><path d="M11.5 12H21m-3.5 0v3.500M14.5 12v2.5"/>',
    "fire": '<path d="M12 3c.6 3.2-2.8 4.8-2.8 8.200A3.3 3.3 0 0 0 12.5 14.500c0-1.2-.5-1.8-.9-2.5 2.6.8 4.4 3 4.4 5.300A5 5 0 0 1 12 22a6 6 0 0 1-6-6c0-3.2 2.2-5.2 3.8-7.100C10.9 7.6 11.8 5.8 12 3z"/>',
    "video": '<rect x="3" y="6" width="12.5" height="12" rx="2.5"/><path d="m15.5 10.5 5.5-3v9l-5.5-3z"/>',
    "mobile": '<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 18.500h2"/>',
}
_EX_DEFAULT_ICON = '<circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/>'


def _ex_icon(item):
    key = _slug(item.get("icon") or item.get("label", ""))
    for k, v in _EX_ICONS.items():
        if k in key:
            return v
    return _EX_DEFAULT_ICON


def _explorer(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    eid = s.get("id", "explorer")
    items = s["items"]
    n = len(items)
    svg = lambda body, cls="": (f'<svg class="ex-ic {cls}" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" '
                                f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{body}</svg>')
    rail, panels, pills = [], [], []
    for i, t in enumerate(items):
        href = E(L(t["href"])) if t.get("href") else "#"
        ring = ('<svg class="ex-ring" viewBox="0 0 40 40" width="40" height="40" aria-hidden="true" focusable="false">'
                '<circle class="ex-ring-bg" cx="20" cy="20" r="17" pathLength="100"/><circle class="ex-ring-fg" cx="20" cy="20" r="17" pathLength="100"/></svg>')
        rail.append(f'<li><a class="ex-tab" id="{E(eid)}-t{i}" href="{href}" data-i="{i}" aria-controls="{E(eid)}-p{i}"{" aria-current=true" if i == 0 else ""}>'
                    f'<span class="ex-ico">{ring}{svg(_ex_icon(t))}</span><span class="ex-lab">{E(t["label"])}</span><span class="ex-num" aria-hidden="true">{i + 1:02d}</span></a></li>')
        chips = "".join(f'<li class="ex-chip"><span class="ex-dot" aria-hidden="true"></span>{_chip_link(b, L, E)}</li>' for b in t.get("bullets", [])[:4])
        img = (f'<div class="ex-plate"><div class="ex-glow" aria-hidden="true"></div><div class="ex-float"><div class="ex-card">'
               f'<img src="{E(rel(t["image"]))}" alt="{E(t.get("image_alt", ""))}" width="1200" height="900" decoding="async"{"" if i == 0 else " loading=lazy"}>'
               f'<span class="ex-sheen" aria-hidden="true"></span></div></div><div class="ex-shadow" aria-hidden="true"></div></div>') if t.get("image") else ""
        cta = (f'<a class="q-btn ex-cta" href="{href}">Explore {E(t["label"])}</a>') if t.get("href") else ""
        panels.append(f'<div class="ex-panel" role="group" aria-roledescription="slide" id="{E(eid)}-p{i}" aria-labelledby="{E(eid)}-t{i}" data-i="{i}"{"" if i == 0 else " hidden"}>'
                      f'<div class="ex-copy"><p class="ex-kick"><span>{i + 1:02d}</span>{E(t["label"])}</p><h3 class="ex-h">{E(t["title"])}</h3><p class="ex-p">{E(t["body"])}</p>'
                      f'<p class="ex-incl">What it includes</p><ul class="ex-chips">{chips}</ul>{cta}</div>{img}</div>')
        pills.append(f'<li><a class="ex-pill" href="{href}" data-i="{i}">{svg(_ex_icon(t))}<span>{E(t["label"])}</span></a></li>')
    strip_label = E(s.get("strip_label", "The rest of the platform"))
    return (f'{ctx["sec_open"](s)} <div class="q-container mo-ex" id="{E(eid)}-w" data-mo="explorer" data-n="{n}" data-ms="{int(s.get("interval_ms", 7000))}">{_head(s, ctx)}'
            f'<div class="ex-grid"><nav class="ex-rail" aria-label="{E(s.get("heading", "Systems"))}"><ol>{"".join(rail)}</ol></nav>'
            f'<div class="ex-main"><div class="ex-stage" aria-live="off"><div class="ex-bg" aria-hidden="true"></div><div class="ex-panels">{"".join(panels)}</div></div>'
            f'<div class="ex-strip"><span class="ex-strip-l">{strip_label}</span><ul>{"".join(pills)}</ul></div></div></div></div></section>')


RENDER_EXTRA3["explorer"] = _explorer

EX_CSS = r"""
/* ===== explorer ===== */
.mo-ex{--ex-ground:#0b1220;--ex-ground2:#121c30;--ex-fg:#f4f6fb;--ex-mut:#b7c0d3}
.ex-grid{display:grid;grid-template-columns:minmax(250px,310px) minmax(0,1fr);gap:28px;align-items:stretch}
.ex-rail{display:flex}.ex-rail ol{flex:1}.ex-rail li{flex:1;display:flex}.ex-rail li .ex-tab{flex:1}
.ex-rail ol,.ex-strip ul,.ex-chips{list-style:none;margin:0;padding:0}
.ex-rail ol{display:flex;flex-direction:column;gap:10px}
.ex-tab{position:relative;display:grid;grid-template-columns:48px 1fr auto;align-items:center;gap:14px;min-height:76px;padding:12px 18px 12px 14px;border:1px solid var(--border);border-radius:14px;background:var(--card);color:var(--fg);text-decoration:none;font-weight:700;font-size:18px;line-height:1.2;overflow:hidden;transition:background .3s,color .3s,border-color .3s,transform .3s,box-shadow .3s}
.ex-tab:hover{border-color:var(--q-gold);transform:translateX(3px)}
.ex-tab:focus-visible,.ex-pill:focus-visible,.ex-cta:focus-visible{outline:3px solid var(--q-gold);outline-offset:3px}
.ex-tab::before{content:"";position:absolute;left:0;top:14px;bottom:14px;width:4px;border-radius:0 4px 4px 0;background:var(--q-gold);transform:scaleY(0);transition:transform .35s}
.ex-ico{position:relative;display:grid;place-items:center;width:48px;height:48px;border-radius:50%;background:var(--bg-alt);color:var(--accent-ink);transition:background .3s,color .3s}
.ex-ico .ex-ic{width:24px;height:24px}
.ex-ring{position:absolute;inset:0;width:100%;height:100%;transform:rotate(-90deg);opacity:0;transition:opacity .3s}
.ex-ring circle{fill:none;stroke-width:2.5}
.ex-ring-bg{stroke:rgba(255,255,255,.16)}
.ex-ring-fg{stroke:var(--q-gold);stroke-linecap:round;stroke-dasharray:100;stroke-dashoffset:100}
.ex-num{font-size:13px;font-weight:700;letter-spacing:.08em;color:var(--fg-muted);font-variant-numeric:tabular-nums}
.ex-tab[aria-selected=true],.ex-tab[aria-current=true]{background:var(--ex-ground);border-color:var(--ex-ground);color:var(--ex-fg);box-shadow:0 18px 40px -22px rgba(0,0,0,.6)}
.ex-tab[aria-selected=true]::before,.ex-tab[aria-current=true]::before{transform:scaleY(1)}
.ex-tab[aria-selected=true] .ex-ico,.ex-tab[aria-current=true] .ex-ico{background:rgba(255,255,255,.08);color:var(--q-gold)}
.ex-tab[aria-selected=true] .ex-num,.ex-tab[aria-current=true] .ex-num{color:var(--ex-mut)}
.ex-tab[aria-selected=true]:hover{transform:none}
.mo-ex.is-live:not(.is-manual) .ex-tab[aria-selected=true] .ex-ring{opacity:1}
.mo-ex.is-live:not(.is-manual) .ex-tab[aria-selected=true] .ex-ring-fg{animation:exring var(--ex-ms,7000ms) linear forwards}
.mo-ex.is-paused .ex-ring-fg{animation-play-state:paused!important}
@keyframes exring{to{stroke-dashoffset:0}}

.ex-stage{position:relative;overflow:hidden;border-radius:22px;background:linear-gradient(160deg,var(--ex-ground2),var(--ex-ground) 60%);color:var(--ex-fg);min-height:540px;box-shadow:0 40px 80px -40px rgba(0,0,0,.55);isolation:isolate}
.ex-bg{position:absolute;inset:0;z-index:0;pointer-events:none;background:
 radial-gradient(60% 70% at 78% 40%,color-mix(in srgb,var(--q-gold) 34%,transparent),transparent 70%),
 linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px) 0 0/44px 44px,
 linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px) 0 0/44px 44px;
 -webkit-mask-image:radial-gradient(90% 90% at 70% 45%,#000 40%,transparent 100%);mask-image:radial-gradient(90% 90% at 70% 45%,#000 40%,transparent 100%)}
.ex-panels{position:relative;z-index:1;display:grid}
.ex-panel{grid-area:1/1;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:20px;align-items:center;padding:44px 44px 44px 48px;position:relative}
html:not(.js-ex) .ex-panel[hidden]{display:none}
.js-ex .ex-panel{visibility:hidden;opacity:0;pointer-events:none;transform:translateX(calc(var(--exd,1)*46px));transition:opacity .55s ease,transform .7s cubic-bezier(.2,.8,.2,1),visibility 0s .7s}
.js-ex .ex-panel.is-on{visibility:visible;opacity:1;pointer-events:auto;transform:none;transition:opacity .55s ease .08s,transform .7s cubic-bezier(.2,.8,.2,1) .08s,visibility 0s}
.js-ex .ex-panel.is-out{transform:translateX(calc(var(--exd,1)*-46px))}
.ex-copy{position:relative;z-index:2}
.ex-kick{margin:0 0 14px;display:flex;align-items:center;gap:12px;font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--q-gold)}
.ex-kick span{display:inline-block;padding:3px 9px;border:1px solid currentColor;border-radius:99px;letter-spacing:.06em}
.ex-h{margin:0;font-family:var(--q-display,var(--q-sans));font-size:clamp(28px,2.6vw,40px);line-height:1.1;font-weight:700;color:var(--ex-fg);text-wrap:balance}
.ex-p{margin:16px 0 0;font-size:16px;line-height:1.6;color:var(--ex-mut);max-width:46ch}
.ex-incl{margin:26px 0 10px;font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--ex-mut)}
.ex-chips{display:flex;flex-direction:column;align-items:flex-start;gap:8px}
.ex-chip{display:inline-flex;align-items:center;gap:10px;padding:9px 16px 9px 12px;border-radius:99px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.07);backdrop-filter:blur(6px);font-size:14px;font-weight:600;line-height:1.3;color:var(--ex-fg)}
.ex-dot{flex:none;width:8px;height:8px;border-radius:50%;background:var(--q-gold);box-shadow:0 0 0 4px color-mix(in srgb,var(--q-gold) 28%,transparent)}
.ex-cta{margin-top:28px;display:inline-flex;align-items:center;gap:10px}
.ex-cta::after{content:"\2192";transition:transform .25s}
.ex-cta:hover::after{transform:translateX(5px)}
.ex-plate{position:relative;z-index:1;perspective:1100px;padding:10px 0 26px}
.ex-glow{position:absolute;inset:6% 2% 10% 2%;border-radius:50%;background:radial-gradient(closest-side,color-mix(in srgb,var(--q-gold) 46%,transparent),transparent);filter:blur(24px);opacity:.75}
.ex-float{position:relative;animation:exfloat 7s ease-in-out infinite}
.ex-card{position:relative;border-radius:20px;overflow:hidden;transform-style:preserve-3d;transform:rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg)) rotateZ(var(--rz,-1deg));transition:transform .25s ease-out;box-shadow:0 50px 70px -30px rgba(0,0,0,.75),0 0 0 1px rgba(255,255,255,.14);background:#d9d4c8}
.ex-card img{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover}
.ex-card::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(11,18,32,.0) 45%,rgba(11,18,32,.5)),radial-gradient(120% 100% at 50% 40%,transparent 55%,rgba(11,18,32,.55));box-shadow:inset 0 0 0 1px rgba(255,255,255,.12)}
.ex-sheen{position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(115deg,transparent 35%,rgba(255,255,255,.22) 50%,transparent 65%);background-size:250% 100%;background-position:calc(100% - var(--sx,30%)) 0;mix-blend-mode:soft-light}
.ex-shadow{position:absolute;left:12%;right:12%;bottom:0;height:22px;border-radius:50%;background:radial-gradient(closest-side,rgba(0,0,0,.55),transparent);filter:blur(6px);animation:exshadow 7s ease-in-out infinite}
@keyframes exfloat{50%{transform:translateY(-12px)}}
@keyframes exshadow{50%{transform:scale(.86);opacity:.7}}
.ex-conn{position:absolute;left:0;top:0;width:100%;height:100%;z-index:1;pointer-events:none;overflow:visible}
.ex-conn path{fill:none;stroke:var(--q-gold);stroke-width:1.5;stroke-dasharray:5 7;opacity:.75;animation:exflow 1.600s linear infinite}
.ex-conn circle{fill:var(--q-gold);animation:expulse 2.400s ease-in-out infinite}
@keyframes exflow{to{stroke-dashoffset:-24}}
@keyframes expulse{50%{opacity:.35}}
.ex-strip{display:flex;align-items:center;flex-wrap:wrap;gap:12px 18px;margin-top:16px;padding:14px 18px;border:1px solid var(--border);border-radius:14px;background:var(--card)}
.ex-strip-l{font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--fg-muted)}
.ex-strip ul{display:flex;flex-wrap:wrap;gap:8px}
.ex-pill{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px 0 12px;border-radius:99px;border:1px solid var(--border);background:var(--bg-alt);color:var(--fg);font-size:14px;font-weight:600;text-decoration:none;cursor:pointer;font-family:inherit;transition:border-color .25s,transform .25s,background .25s}
.ex-pill .ex-ic{width:18px;height:18px;color:var(--accent-ink)}
.ex-pill:hover{border-color:var(--q-gold);transform:translateY(-2px)}
.ex-pill.is-here{display:none}
@media(max-width:1100px){.ex-panel{padding:34px 28px}.ex-grid{grid-template-columns:minmax(220px,260px) minmax(0,1fr)}.ex-tab{font-size:16px;grid-template-columns:44px 1fr auto}.ex-ico{width:44px;height:44px}}
@media(max-width:767.98px){
.ex-grid{grid-template-columns:minmax(0,1fr);gap:16px}.ex-rail li{flex:none;display:block}.ex-rail li .ex-tab{flex:none}
.ex-rail ol{flex-direction:row;flex-wrap:wrap;gap:8px}
.ex-tab{grid-template-columns:auto auto;min-height:44px;padding:6px 14px 6px 8px;gap:8px;font-size:15px;border-radius:99px}
.ex-tab:hover{transform:none}.ex-tab::before,.ex-num{display:none}
.ex-ico{width:36px;height:36px}.ex-ico .ex-ic{width:19px;height:19px}
.ex-stage{min-height:0;border-radius:18px}
.ex-panel{grid-template-columns:minmax(0,1fr);padding:22px 20px 26px;gap:8px}
.ex-plate{order:-1;padding:6px 0 20px}.ex-card{transform:none!important}
.ex-conn{display:none}
.ex-chips{width:100%}.ex-chip{width:100%;border-radius:14px}
.ex-cta{width:100%;justify-content:center}
}
@media(prefers-reduced-motion:reduce){.ex-float,.ex-shadow,.ex-conn path,.ex-conn circle{animation:none}.js-ex .ex-panel,.js-ex .ex-panel.is-on{transition:none;transform:none}.ex-card{transition:none}}
"""

EX_JS = r"""(function(){
var rm=matchMedia('(prefers-reduced-motion: reduce)').matches,fine=matchMedia('(pointer:fine)').matches,desk=function(){return matchMedia('(min-width:768px)').matches};
[].slice.call(document.querySelectorAll('[data-mo=explorer]')).forEach(function(root){
var tabs=[].slice.call(root.querySelectorAll('.ex-tab')),panels=[].slice.call(root.querySelectorAll('.ex-panel')),pills=[].slice.call(root.querySelectorAll('.ex-pill')),stage=root.querySelector('.ex-stage'),n=tabs.length,cur=0,manual=false,NS='http://www.w3.org/2000/svg';
if(!n)return;
root.classList.add('js-ex');document.documentElement.classList.add('js-ex');
root.style.setProperty('--ex-ms',(+root.getAttribute('data-ms')||7000)+'ms');
root.querySelector('.ex-rail ol').setAttribute('role','tablist');root.querySelector('.ex-rail ol').setAttribute('aria-orientation','vertical');
[].slice.call(root.querySelectorAll('.ex-rail li')).forEach(function(li){li.setAttribute('role','presentation')});
tabs.forEach(function(t,i){t.setAttribute('role','tab');t.removeAttribute('aria-current');t.setAttribute('aria-selected',i===0?'true':'false');t.tabIndex=i===0?0:-1;t.setAttribute('href',t.getAttribute('href'))});
panels.forEach(function(p,i){p.setAttribute('role','tabpanel');p.removeAttribute('aria-roledescription');p.hidden=false;if(i===0)p.classList.add('is-on')});
function drawConn(p){if(!desk()){return}var old=p.querySelector('.ex-conn');if(old)old.remove();var plate=p.querySelector('.ex-plate'),chips=[].slice.call(p.querySelectorAll('.ex-chip'));if(!plate||!chips.length)return;
var pr=p.getBoundingClientRect(),cr=plate.querySelector('.ex-card').getBoundingClientRect(),svg=document.createElementNS(NS,'svg');svg.setAttribute('class','ex-conn');svg.setAttribute('aria-hidden','true');svg.setAttribute('viewBox','0 0 '+pr.width+' '+pr.height);
var tx=cr.left-pr.left+cr.width*.1,ty0=cr.top-pr.top+cr.height*.5,ty1=cr.top-pr.top+cr.height*.85;
chips.forEach(function(c,i){var r=c.getBoundingClientRect(),x=r.right-pr.left,y=r.top-pr.top+r.height/2,ty=ty0+(chips.length>1?(ty1-ty0)*i/(chips.length-1):0),mx=x+(tx-x)*.5;
var d=document.createElementNS(NS,'path');d.setAttribute('d','M'+x+' '+y+' C'+mx+' '+y+' '+mx+' '+ty+' '+tx+' '+ty);svg.appendChild(d);var o=document.createElementNS(NS,'circle');o.setAttribute('cx',tx);o.setAttribute('cy',ty);o.setAttribute('r',4.5);svg.appendChild(o)});
p.insertBefore(svg,p.firstChild)}
function drawAll(){drawConn(panels[cur])}
function restartRing(){var r=tabs[cur].querySelector('.ex-ring-fg');if(!r)return;r.style.animation='none';void r.getBoundingClientRect();r.style.animation=''}
function show(i,user){if(i===cur&&!user)return;var dir=i>cur?1:-1;if(i===0&&cur===n-1&&!user)dir=1;if(i===n-1&&cur===0&&!user)dir=-1;root.style.setProperty('--exd',dir);
var old=panels[cur];old.classList.remove('is-on');old.classList.add('is-out');setTimeout(function(){old.classList.remove('is-out')},760);
tabs.forEach(function(t,j){t.setAttribute('aria-selected',j===i?'true':'false');t.tabIndex=j===i?0:-1});
cur=i;panels[i].classList.add('is-on');pills.forEach(function(p){p.classList.toggle('is-here',+p.getAttribute('data-i')===i)});
requestAnimationFrame(function(){drawAll()});restartRing()}
function manualSel(i,focus){if(!manual){manual=true;root.classList.add('is-manual')}show(i,true);if(focus)tabs[i].focus()}
tabs.forEach(function(t,i){t.addEventListener('click',function(e){e.preventDefault();manualSel(i,false)});
t.addEventListener('keydown',function(e){var k=e.key,j=-1;if(k==='ArrowDown'||k==='ArrowRight')j=(i+1)%n;else if(k==='ArrowUp'||k==='ArrowLeft')j=(i-1+n)%n;else if(k==='Home')j=0;else if(k==='End')j=n-1;if(j<0)return;e.preventDefault();manualSel(j,true)})});
pills.forEach(function(p){p.setAttribute('role','button');p.addEventListener('click',function(e){e.preventDefault();manualSel(+p.getAttribute('data-i'),false)})});
pills[0]&&pills[0].classList.add('is-here');
/* tilt + parallax */
if(!rm&&fine){stage.addEventListener('pointermove',function(e){if(!desk())return;var p=panels[cur],card=p.querySelector('.ex-card');if(!card)return;var r=stage.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;card.style.setProperty('--ry',(x*14).toFixed(2)+'deg');card.style.setProperty('--rx',(-y*10).toFixed(2)+'deg');card.style.setProperty('--sx',(50+x*60).toFixed(0)+'%');var g=p.querySelector('.ex-glow');if(g)g.style.transform='translate('+(x*-26).toFixed(1)+'px,'+(y*-18).toFixed(1)+'px)'});
stage.addEventListener('pointerleave',function(){panels.forEach(function(p){var c=p.querySelector('.ex-card');if(c){c.style.setProperty('--rx','0deg');c.style.setProperty('--ry','0deg')}})})}
/* autoplay */
if(!rm){var vis=false;
var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){vis=e.isIntersecting;root.classList.toggle('is-live',vis);if(vis&&!manual)restartRing()})},{threshold:.35}):null;
if(io)io.observe(root);else root.classList.add('is-live');
var holds=0;function hold(a){holds=Math.max(0,holds+(a?1:-1));root.classList.toggle('is-paused',holds>0)}
var hov=false,foc=false;
root.addEventListener('pointerenter',function(e){if(e.pointerType!=='touch'&&!hov){hov=true;hold(true)}});root.addEventListener('pointerleave',function(){if(hov){hov=false;hold(false)}});
root.addEventListener('focusin',function(){if(!foc){foc=true;hold(true)}});root.addEventListener('focusout',function(e){if(foc&&!root.contains(e.relatedTarget)){foc=false;hold(false)}});
root.addEventListener('pointerdown',function(e){if(e.pointerType==='touch'&&!manual){manual=true;root.classList.add('is-manual')}});
root.addEventListener('animationend',function(e){if(e.animationName==='exring'&&!manual)show((cur+1)%n,false)})}
var rt;addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(drawAll,120)});
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(drawAll);
addEventListener('load',drawAll);requestAnimationFrame(drawAll)});
})();
"""
EXTRA_CSS3 = EXTRA_CSS3 + EX_CSS
MOTION_JS = MOTION_JS + "\n" + EX_JS


# ----------------------------------------------------------------------------- 7. journey
# A scroll-driven story: five large icon nodes on a glowing line, a signal pulse that travels with scroll (and
# auto-plays once on first reveal), one big caption panel for the active step. Server HTML is a plain vertical
# list of five cards (no JS, reduced motion). Items use the same data shape as the "flow" section:
# steps: [{label, when, summary, title, body, receive:[...]}]

_JY_ICONS = [
    # detector: body with lens and radiating arcs
    '<rect x="5" y="3.500" width="14" height="10" rx="3.500"/><circle cx="12" cy="8.500" r="2.500"/><path d="M8 17.500c2.500 1.800 5.500 1.800 8 0M5.500 20.500c4 2.800 9 2.800 13 0"/>',
    # control panel: keypad
    '<rect x="5" y="2.500" width="14" height="19" rx="2.500"/><rect x="8" y="5.500" width="8" height="3.500" rx="1"/><path d="M9 13h.01M12 13h.01M15 13h.01M9 16h.01M12 16h.01M15 16h.01M9 19h.01M12 19h.01M15 19h.01" stroke-width="2.400"/>',
    # communicator: antenna with waves
    '<circle cx="12" cy="9.500" r="1.800"/><path d="M12 11.500V21M8.500 21h7M8.300 6.200a5 5 0 0 0 0 6.600M15.700 6.200a5 5 0 0 1 0 6.600M5.500 3.800a9 9 0 0 0 0 11.400M18.500 3.800a9 9 0 0 1 0 11.400"/>',
    # monitoring center: headset
    '<path d="M4.500 14v-2a7.500 7.500 0 0 1 15 0v2"/><rect x="3" y="13" width="4.500" height="6.500" rx="2"/><rect x="16.500" y="13" width="4.500" height="6.500" rx="2"/><path d="M19 19.500c0 1.600-1.800 2.500-4.500 2.500H12.500"/>',
    # phone
    '<rect x="7" y="2.500" width="10" height="19" rx="2.500"/><path d="M11 18.500h2M9.800 7.500l1.600 1.600 2.800-3"/>',
]


def _journey(s, ctx):
    E = ctx["E"]
    jid = s.get("id", "journey")
    steps = s["steps"]
    n = len(steps)
    icon = lambda i: ('<svg class="jy-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
                      f'stroke-linejoin="round" aria-hidden="true" focusable="false">{_JY_ICONS[i % len(_JY_ICONS)]}</svg>')
    lis = []
    for i, t in enumerate(steps):
        chips = "".join(f'<li class="jy-chip"><span class="jy-dot" aria-hidden="true"></span>{_chip_link(b, ctx["L"], E)}</li>' for b in t.get("receive", [])[:3])
        incl = f'<p class="jy-incl">{E(s.get("receive_label", "DMP products at this step"))}</p><ul class="jy-chips">{chips}</ul>' if chips else ""
        lis.append(
            f'<li class="jy-step" data-i="{i}" data-when="{E(t.get("when", ""))}">'
            f'<button type="button" class="jy-node" id="{E(jid)}-n{i}" data-i="{i}" aria-label="Step {i + 1}: {E(t["label"])}" aria-controls="{E(jid)}-panel"><span class="jy-orb"><span class="jy-ring" aria-hidden="true"></span>{icon(i)}</span>'
            f'<span class="jy-num" aria-hidden="true">{i + 1:02d}</span></button>'
            f'<div class="jy-card"><h3 class="jy-lab"><span class="jy-sr">Step {i + 1}: </span>{E(t["label"])}</h3>'
            + (f'<p class="jy-when">{E(t["when"])}</p>' if t.get("when") else "")
            + f'<p class="jy-cap">{E(t.get("summary", ""))}</p>'
            f'<div class="jy-detail"><p class="jy-t">{E(t.get("title", t["label"]))}</p><p class="jy-p">{E(t.get("body", ""))}</p>{incl}</div></div></li>')
    return (f'{ctx["sec_open"](s)} <div class="q-container mo-jy" id="{E(jid)}-w" data-mo="journey" data-n="{n}">{_head(s, ctx)}'
            f'<div class="jy-stage"><div class="jy-bg" aria-hidden="true"></div>'
            f'<div class="jy-path"><div class="jy-line" aria-hidden="true"><i class="jy-fill"></i><b class="jy-pulse"></b></div>'
            f'<ol class="jy-steps">{"".join(lis)}</ol></div></div></div></section>')


RENDER_EXTRA3["journey"] = _journey

JY_CSS = r"""
/* ===== journey ===== */
.mo-jy{--jy-ground:#0b1220;--jy-ground2:#121c30;--jy-fg:#f4f6fb;--jy-mut:#b7c0d3;--p:0}
.jy-stage{position:relative;margin-top:40px;overflow:hidden;border-radius:22px;background:linear-gradient(160deg,var(--jy-ground2),var(--jy-ground) 60%);color:var(--jy-fg);padding:36px 16px 28px;box-shadow:0 40px 80px -40px rgba(0,0,0,.55);isolation:isolate}
.jy-bg{position:absolute;inset:0;z-index:0;pointer-events:none;background:
 radial-gradient(60% 55% at 50% 12%,color-mix(in srgb,var(--q-gold) 26%,transparent),transparent 70%),
 linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px) 0 0/44px 44px,
 linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px) 0 0/44px 44px;
 -webkit-mask-image:radial-gradient(95% 95% at 50% 30%,#000 40%,transparent 100%);mask-image:radial-gradient(95% 95% at 50% 30%,#000 40%,transparent 100%)}
.jy-path{position:relative;z-index:1}
.jy-steps{list-style:none;margin:0;padding:0;position:relative;display:flex;flex-direction:column;gap:18px}
/* vertical line (static list, phones) */
.jy-line{position:absolute;z-index:0;left:31px;top:32px;bottom:32px;width:4px;margin-left:-2px;border-radius:4px;background:rgba(255,255,255,.16)}
.jy-fill{display:block;position:absolute;left:0;top:0;width:100%;height:100%;border-radius:4px;background:linear-gradient(180deg,var(--q-gold),color-mix(in srgb,var(--q-gold) 60%,#fff));box-shadow:0 0 16px color-mix(in srgb,var(--q-gold) 70%,transparent)}
.jy-pulse{display:none}
.jy-step{position:relative;z-index:1;display:grid;grid-template-columns:64px minmax(0,1fr);gap:16px;align-items:start}
.jy-node{position:relative;display:block;width:64px;height:64px;padding:0;border:0;background:none;color:inherit;font:inherit;cursor:pointer;border-radius:50%}
.jy-node:focus-visible{outline:3px solid #fff;outline-offset:4px}
.jy-orb{position:relative;display:grid;place-items:center;width:64px;height:64px;border-radius:50%;background:var(--jy-ground);border:2px solid var(--q-gold);color:var(--q-gold);box-shadow:0 0 0 6px var(--jy-ground),0 0 26px color-mix(in srgb,var(--q-gold) 45%,transparent);transition:transform .5s cubic-bezier(.2,.9,.3,1.3),background .4s,color .4s,border-color .4s,box-shadow .4s}
.jy-ic{width:32px;height:32px}
.jy-ring{position:absolute;inset:-2px;border-radius:50%;border:2px solid var(--q-gold);opacity:0;pointer-events:none}
.jy-num{display:none}
.jy-card{padding:20px 20px 22px;border-radius:16px;border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.06);transition:opacity .5s,transform .5s,border-color .4s,background .4s}
.jy-lab{margin:0;font-family:var(--q-display,var(--q-sans));font-size:26px;line-height:1.15;font-weight:700;color:var(--jy-fg)}
.jy-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.jy-when{margin:6px 0 0;font-size:14px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--q-gold)}
.jy-cap{display:none;margin:10px 0 0;font-size:17px;line-height:1.45;color:var(--jy-mut)}
.jy-detail{margin-top:14px}
.jy-t{margin:0;font-size:19px;line-height:1.3;font-weight:700;color:var(--jy-fg)}
.jy-p{margin:10px 0 0;font-size:17px;line-height:1.6;color:var(--jy-mut)}
.jy-incl{margin:18px 0 10px;font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--jy-mut)}
.jy-chips{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.jy-chip{display:inline-flex;align-items:center;gap:10px;padding:9px 16px 9px 12px;border-radius:99px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.07);font-size:15px;font-weight:600;line-height:1.3;color:var(--jy-fg)}
.jy-dot{flex:none;width:8px;height:8px;border-radius:50%;background:var(--q-gold);box-shadow:0 0 0 4px color-mix(in srgb,var(--q-gold) 28%,transparent)}
.jy-panel,.jy-bar{display:none}

/* JS on: phones keep the vertical timeline and the line draws down with scroll */
.js-jy .jy-fill{height:var(--fy,0px)}
.js-jy .jy-step:not(.is-lit) .jy-orb{background:#18233a;border-color:rgba(255,255,255,.28);color:#aab5cb;box-shadow:0 0 0 6px var(--jy-ground)}
.js-jy .jy-step:not(.is-lit) .jy-card{opacity:.5;transform:translateY(10px);border-color:rgba(255,255,255,.1)}
.js-jy .jy-step.is-cur .jy-orb{background:var(--q-gold);color:var(--cta-fg);transform:scale(1.1)}
.js-jy .jy-step.is-cur .jy-card{border-color:color-mix(in srgb,var(--q-gold) 65%,transparent);background:rgba(255,255,255,.09)}
.js-jy .jy-step.is-cur .jy-ring{animation:jyring 2.2s ease-out infinite}
@keyframes jyring{0%{transform:scale(1);opacity:.85}100%{transform:scale(1.75);opacity:0}}
@keyframes jyflow{to{background-position:0 -64px}}
@keyframes jyflowx{to{background-position:64px 0}}

@media(max-width:479px){.jy-stage{padding:28px 12px 24px}.jy-step{grid-template-columns:48px minmax(0,1fr);gap:12px}.jy-node,.jy-orb{width:48px;height:48px}.jy-ic{width:25px;height:25px}.jy-line{left:24px;top:24px;bottom:24px}.jy-card{padding:16px 16px 18px}.jy-lab{font-size:24px}.jy-orb{box-shadow:0 0 0 4px var(--jy-ground),0 0 20px color-mix(in srgb,var(--q-gold) 45%,transparent)}.js-jy .jy-step:not(.is-lit) .jy-orb{box-shadow:0 0 0 4px var(--jy-ground)}}
/* wide: horizontal path + one big caption panel */
@media(min-width:768px){
.jy-stage{padding:52px 40px 44px}
.js-jy .jy-bar{display:flex;justify-content:flex-end;position:relative;z-index:2;margin:-18px 0 6px}
.jy-replay{display:inline-flex;align-items:center;gap:10px;min-height:44px;padding:0 20px;border-radius:99px;border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.08);color:var(--jy-fg);font:inherit;font-size:16px;font-weight:700;cursor:pointer;transition:background .25s,border-color .25s}
.jy-replay:hover{background:rgba(255,255,255,.16);border-color:var(--q-gold)}
.jy-replay:focus-visible{outline:3px solid #fff;outline-offset:3px}
.jy-replay svg{width:18px;height:18px}
.js-jy .jy-steps{display:grid;grid-template-columns:repeat(var(--n,5),minmax(0,1fr));gap:0;align-items:start}
.js-jy .jy-line{left:10%;right:10%;top:61px;bottom:auto;width:auto;height:4px;margin:0;transform:none}
.js-jy .jy-fill{width:calc(var(--p)*100%);height:100%;background:linear-gradient(90deg,color-mix(in srgb,var(--q-gold) 70%,#000),var(--q-gold))}
.js-jy .jy-fill::after{content:"";position:absolute;inset:0;border-radius:4px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.95) 0 7px,transparent 7px 64px);background-size:64px 100%;animation:jyflowx 1.1s linear infinite;-webkit-mask-image:linear-gradient(90deg,transparent,#000 30%);mask-image:linear-gradient(90deg,transparent,#000 30%);opacity:.9}
.js-jy .jy-line::before{content:"";position:absolute;inset:0;border-radius:4px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.4) 0 6px,transparent 6px 64px);animation:jyflowx 2.4s linear infinite}
.js-jy .jy-pulse{display:block;position:absolute;top:50%;left:calc(var(--p)*100%);width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:50%;background:#fff;box-shadow:0 0 0 6px color-mix(in srgb,var(--q-gold) 55%,transparent),0 0 34px 12px color-mix(in srgb,var(--q-gold) 80%,transparent);z-index:3}
.js-jy .jy-pulse::before{content:"";position:absolute;right:50%;top:50%;width:150px;height:8px;margin-top:-4px;border-radius:8px;background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--q-gold) 90%,transparent));filter:blur(2px)}
.js-jy .jy-step{display:flex;flex-direction:column;align-items:center;text-align:center;gap:0;padding:0 10px}
.js-jy .jy-node{width:122px;height:122px}
.js-jy .jy-orb{width:122px;height:122px;border-width:3px;box-shadow:0 0 0 8px var(--jy-ground),0 0 34px color-mix(in srgb,var(--q-gold) 40%,transparent)}
.js-jy .jy-ic{width:58px;height:58px}
.js-jy .jy-step:not(.is-lit) .jy-orb{box-shadow:0 0 0 8px var(--jy-ground)}
.js-jy .jy-step.is-cur .jy-orb{transform:scale(1.14);box-shadow:0 0 0 8px var(--jy-ground),0 0 56px color-mix(in srgb,var(--q-gold) 75%,transparent)}
.js-jy .jy-num{display:block;position:absolute;right:-2px;top:-2px;min-width:34px;height:34px;padding:0 6px;border-radius:99px;background:var(--jy-ground);border:2px solid currentColor;font-size:14px;font-weight:800;line-height:30px;text-align:center;color:#aab5cb;font-variant-numeric:tabular-nums;z-index:2}
.js-jy .jy-step.is-lit .jy-num{color:var(--q-gold)}
.js-jy .jy-card{margin-top:22px;padding:0;border:0;background:none;transform:none;opacity:1}
.js-jy .jy-step:not(.is-lit) .jy-card{opacity:1;transform:none}
.js-jy .jy-step.is-cur .jy-card{background:none}
.js-jy .jy-lab{font-size:26px;color:#c3cce0;transition:color .4s}
.js-jy .jy-step.is-lit .jy-lab{color:var(--jy-fg)}
.js-jy .jy-when{display:none}
.js-jy .jy-cap{display:block;margin:10px auto 0;max-width:23ch;font-size:17px;opacity:0;transform:translateY(8px);transition:opacity .5s .1s,transform .5s .1s}
.js-jy .jy-step.is-lit .jy-cap{opacity:1;transform:none}
.js-jy .jy-detail{display:none}
.js-jy .jy-panel{display:grid;position:relative;z-index:1;margin-top:40px;border:1px solid rgba(255,255,255,.16);border-radius:20px;background:rgba(255,255,255,.055);overflow:hidden;box-shadow:inset 0 1px 0 rgba(255,255,255,.1)}
.jy-pane{grid-area:1/1;position:relative;display:flex;align-items:center;padding:40px 48px;min-height:260px;visibility:hidden;opacity:0;transform:translateY(16px);transition:opacity .45s ease,transform .6s cubic-bezier(.2,.8,.2,1),visibility 0s .6s}
.jy-pane.is-on{visibility:visible;opacity:1;transform:none;transition:opacity .5s ease .1s,transform .6s cubic-bezier(.2,.8,.2,1) .1s,visibility 0s}
.jy-big{position:absolute;right:36px;top:50%;transform:translateY(-52%);font-family:var(--q-display,var(--q-sans));font-size:clamp(150px,17vw,250px);line-height:1;font-weight:800;letter-spacing:-.04em;color:rgba(255,255,255,.07);pointer-events:none;user-select:none}
.jy-pc{position:relative;z-index:1;max-width:min(760px,100%)}
.jy-k{margin:0 0 14px;display:flex;align-items:center;gap:12px;font-size:14px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--q-gold)}
.jy-k span{display:inline-block;padding:3px 10px;border:1px solid currentColor;border-radius:99px;letter-spacing:.06em}
.jy-pane .jy-t{font-family:var(--q-display,var(--q-sans));font-size:clamp(28px,2.7vw,40px);line-height:1.12;text-wrap:balance}
.jy-pane .jy-p{margin-top:16px;font-size:19px;line-height:1.6;max-width:62ch}
.jy-pane .jy-incl{margin-top:24px}
.jy-pane .jy-chip{font-size:16px}
}
@media(min-width:768px) and (max-width:1023px){
.js-jy .jy-node,.js-jy .jy-orb{width:96px;height:96px}.js-jy .jy-ic{width:46px;height:46px}.js-jy .jy-line{top:47px;left:10%;right:10%}
.js-jy .jy-lab{font-size:22px}.js-jy .jy-cap{font-size:16px}.jy-stage{padding:44px 20px 36px}.jy-pane{padding:32px 28px}.jy-big{font-size:110px;right:16px;top:8px;transform:none}}
@media(prefers-reduced-motion:reduce){.jy-ring,.jy-fill::after,.jy-line::before{animation:none!important}.jy-orb,.jy-card,.jy-pane{transition:none!important}}
"""

JY_JS = r"""(function(){
if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
var desk=function(){return matchMedia('(min-width:768px)').matches};
function clamp(x){return x<0?0:x>1?1:x}
[].slice.call(document.querySelectorAll('[data-mo=journey]')).forEach(function(root){
var steps=[].slice.call(root.querySelectorAll('.jy-step')),n=steps.length;if(n<2)return;
var stage=root.querySelector('.jy-stage'),path=root.querySelector('.jy-path'),list=root.querySelector('.jy-steps'),btns=steps.map(function(s){return s.querySelector('.jy-node')});
root.classList.add('js-jy');root.style.setProperty('--n',n);
/* panel + replay */
var panel=document.createElement('div');panel.className='jy-panel';panel.id=root.id+'-panel';panel.setAttribute('role','region');panel.setAttribute('aria-live','off');panel.setAttribute('aria-label','Selected step');
var panes=steps.map(function(s,i){var pn=document.createElement('div');pn.className='jy-pane';pn.setAttribute('aria-hidden',i?'true':'false');
pn.innerHTML='<span class="jy-big" aria-hidden="true">0'+(i+1)+'</span><div class="jy-pc"><p class="jy-k"><span>0'+(i+1)+'</span>'+(s.getAttribute('data-when')||'')+'</p>'+s.querySelector('.jy-detail').innerHTML+'</div>';panel.appendChild(pn);return pn});
var bar=document.createElement('div');bar.className='jy-bar';
bar.innerHTML='<button type="button" class="jy-replay"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.500 12a8.500 8.500 0 1 0 2.600-6.100M3.500 4v4.500H8"/></svg>Replay</button>';
stage.insertBefore(bar,path);path.appendChild(panel);
var rb=bar.firstChild,P=0,cur=-1,mode='auto',started=false,t0=0,raf=0,tw=null,curSel=0;
function paint(i){if(i===cur)return;cur=i;panes.forEach(function(p,j){p.classList.toggle('is-on',j===i);p.setAttribute('aria-hidden',j===i?'false':'true')});
btns.forEach(function(b,j){if(j===i)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current')})}
function renderDesk(){path.style.setProperty('--p',P.toFixed(4));root.style.setProperty('--p',P.toFixed(4));root.setAttribute('data-p',P.toFixed(3));var c=0;
steps.forEach(function(s,i){var r=P>=i/(n-1)-.025;if(r)c=i;s.classList.toggle('is-lit',r)});if(mode==='manual')c=curSel;steps.forEach(function(s,i){s.classList.toggle('is-cur',i===c)});paint(c)}
function renderMob(){var vy=innerHeight*.62,r=list.getBoundingClientRect(),fy=Math.max(0,Math.min(r.height,vy-r.top)),c=0;
var first=btns[0].getBoundingClientRect(),lastB=btns[n-1].getBoundingClientRect(),lr=path.querySelector('.jy-line').getBoundingClientRect();
path.style.setProperty('--fy',Math.max(0,Math.min(lr.height,vy-lr.top)).toFixed(0)+'px');
steps.forEach(function(s,i){var b=btns[i].getBoundingClientRect(),r2=b.top+b.height/2<=vy;if(r2)c=i;s.classList.toggle('is-lit',r2)});steps.forEach(function(s,i){s.classList.toggle('is-cur',i===c)});paint(c);root.setAttribute('data-p',(lr.height?Math.max(0,Math.min(lr.height,vy-lr.top))/lr.height:0).toFixed(3))}
function scrollP(){var r=stage.getBoundingClientRect();return clamp((innerHeight*.85-r.top)/(innerHeight*.55))}
var SEG=700,DW=800;
function autoP(t){var k=SEG+DW,s=Math.min(n-2,Math.floor(t/k)),u=t-s*k,f=clamp(u/SEG);f=f<.5?2*f*f:1-Math.pow(-2*f+2,2)/2;if(t>=(n-1)*k-DW)return 1;return (s+f)/(n-1)}
function ease(f){return f<.5?2*f*f:1-Math.pow(-2*f+2,2)/2}
function frame(ts){raf=0;var go=false;
if(tw){var f=clamp((ts-tw.t)/tw.d);P=tw.a+(tw.b-tw.a)*ease(f);if(f<1)go=true;else{P=tw.b;tw=null}}
else if(mode==='auto'||mode==='replay'){var a=autoP(ts-t0);P=mode==='auto'?Math.max(P,a,scrollP()):a;if(ts-t0<(n-1)*(SEG+DW)-DW)go=true;else{P=1;mode='done'}}
renderDesk();if(go)raf=requestAnimationFrame(frame)}
function kick(){if(!raf)raf=requestAnimationFrame(frame)}
function select(i,focus){i=Math.max(0,Math.min(n-1,i));if(mode==='manual'&&curSel===i&&(!tw||tw.i===i)){if(focus)btns[i].focus();return}mode='manual';curSel=i;panel.setAttribute('aria-live','polite');
var b=i/(n-1);tw={i:i,a:P,b:b,d:Math.max(450,Math.abs(b-P)*(n-1)*300),t:performance.now()};if(focus)btns[i].focus();kick()}
btns.forEach(function(b,i){b.addEventListener('click',function(){if(desk())select(i,false)});b.addEventListener('focus',function(){if(desk()&&!tw&&(mode!=='manual'||curSel!==i))select(i,false)})});
root.addEventListener('keydown',function(e){if(!desk()||!stage.contains(e.target)||e.target===rb)return;var k=e.key,i=cur<0?0:(mode==='manual'?curSel:cur);
if(k==='ArrowRight'||k==='ArrowDown')i++;else if(k==='ArrowLeft'||k==='ArrowUp')i--;else if(k==='Home')i=0;else if(k==='End')i=n-1;else return;e.preventDefault();select(i,true)});
rb.addEventListener('click',function(){tw=null;mode='replay';P=0;curSel=0;panel.setAttribute('aria-live','off');t0=performance.now();renderDesk();kick()});
function tick(){raf2=0;if(desk()){if(mode==='auto'){var sp=scrollP();if(sp>P){P=sp;renderDesk()}}else if(!raf)renderDesk()}else renderMob()}
var raf2=0;function onScroll(){if(!raf2)raf2=requestAnimationFrame(tick)}
addEventListener('scroll',onScroll,{passive:true});addEventListener('resize',onScroll);
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(onScroll);
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&!started&&desk()){started=true;if(mode==='auto'){t0=performance.now();kick()}}})},{threshold:.3});io.observe(stage)}
else if(desk()){started=true;t0=performance.now();kick()}
(desk()?renderDesk:renderMob)();onScroll();
});
})();"""
EXTRA_CSS3 = EXTRA_CSS3 + JY_CSS
MOTION_JS = MOTION_JS + "\n" + JY_JS
