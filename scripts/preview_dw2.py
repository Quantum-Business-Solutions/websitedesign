"""Design wave B: pinned product story, world distributor map, closing footer, one icon set.

Registered in preview.py as RENDER_DW2 (section renderers), DW2_CSS, DW2_JS, footer() and wrap(RENDER).
Content is prepared by brands/dmp_dw2.py (apply(data) runs last in finalize()).

Section types
  dw2-story   pinned product story for the four system pages: the product cutout stays sticky on the left while 3 to 4 steps
              scroll past on the right; each step moves the product, the glow ring and the caption chip. Steps are the page's
              own copy. Phones and no-JS: stacked cards with the image on top.
  dw2-map     dot-matrix world map (land mask baked from Natural Earth 110m, public domain, in dw2_landmask.py) with a pulsing
              pin per distributor, arcs from Springfield, and a card on hover, focus or tap. Phones: list view.
Other pieces
  ICONS / icon(key)   twelve line icons on one 24px grid; merged into preview_pop2's registry so every module that asks for
                      "shield", "key", "phone", "camera", "cap", "doc", "keypad" or "signal" now draws this set
  footer(content, ctx) closing footer: "Talk to a person at DMP", the phone number as a large link, Find a dealer, link columns, legal row
  wrap(RENDER)         adds icons to doors and cards when a section carries "icons"

Server HTML is complete without JS (the story is a stacked list, the map pins open on hover and focus). JS only upgrades.
prefers-reduced-motion: no pulsing, no travelling dashes, no gradient drift, no product shift.
Rules: no em or en dashes, nothing under 13px, 44px tap targets, no horizontal overflow at 390/768/1024/1440.
"""
from __future__ import annotations

import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dw2_landmask as LM  # noqa: E402
import preview_pop2  # noqa: E402

# ------------------------------------------------------------------------------------------------ icons
# 24 x 24 grid, 1.7 stroke, round caps and joins, no fills. One idea per icon.
ICONS = {
    "intrusion": '<path d="M12 3l8 3v6c0 4.500-3.200 7.800-8 9-4.800-1.200-8-4.500-8-9V6z"/><path d="M8.500 12l2.500 2.500 4.500-5"/>',
    "access": '<path d="M6 21V4.500A1.500 1.500 0 0 1 7.500 3h9A1.500 1.500 0 0 1 18 4.500V21M3 21h18"/><circle cx="14.500" cy="12" r="1"/><path d="M9.500 8.500h3"/>',
    "fire": '<path d="M12 3c.600 3.200 5.500 5.200 5.500 10.500a5.500 5.500 0 0 1-11 0c0-2.200.900-3.800 2.200-5 .200 1.700 1 2.600 1.900 2.900C10.300 8.700 10.500 5.700 12 3z"/><path d="M12 20.500a2.300 2.300 0 0 1-2.300-2.300c0-1.500 1.300-2.200 2.300-3.600 1 1.400 2.300 2.100 2.300 3.600a2.300 2.300 0 0 1-2.300 2.300z"/>',
    "video": '<rect x="3" y="6.500" width="12.500" height="11" rx="2.500"/><path d="M15.500 10.500l5.500-3.200v9.400l-5.500-3.200"/>',
    "mobile": '<rect x="7" y="2.500" width="10" height="19" rx="2.500"/><path d="M10.500 5.500h3M11 18.500h2"/>',
    "communicator": '<rect x="4.500" y="13" width="15" height="7.500" rx="2"/><path d="M12 13V7"/><circle cx="12" cy="5.500" r="1.500"/><path d="M7.500 3.500a6 6 0 0 0 0 4.500M16.500 3.500a6 6 0 0 1 0 4.500M8 17h.01M12 17h4"/>',
    "keypad": '<rect x="5" y="3" width="14" height="18" rx="2.500"/><path d="M9 8h.01M12 8h.01M15 8h.01M9 12h.01M12 12h.01M15 12h.01M9 16h.01M12 16h.01M15 16h.01"/>',
    "cloud": '<path d="M7.500 18.500a4.500 4.500 0 0 1-.700-8.950 5.800 5.800 0 0 1 11.100 1.600 3.700 3.700 0 0 1-.400 7.350z"/>',
    "docs": '<path d="M9 3h6.500l4 4v11.500H9z"/><path d="M15.500 3v4h4M12 12h5M12 15.500h5M5.500 7.500V21h10"/>',
    "training": '<path d="M2.500 9.500L12 5l9.500 4.500L12 14z"/><path d="M6.500 12v4.200c0 1.400 2.500 2.800 5.500 2.800s5.500-1.400 5.500-2.800V12M21.500 9.500V15"/>',
    "support": '<path d="M4.500 14v-2a7.500 7.500 0 0 1 15 0v2"/><rect x="3" y="13" width="4" height="6.500" rx="1.700"/><rect x="17" y="13" width="4" height="6.500" rx="1.700"/><path d="M19 19.500c0 1.600-2 2.500-5 2.500"/>',
    "partner": '<path d="M10.500 13.500a4 4 0 0 0 5.700 0l3-3a4 4 0 0 0-5.700-5.700l-1 1"/><path d="M13.500 10.500a4 4 0 0 0-5.700 0l-3 3a4 4 0 0 0 5.700 5.700l1-1"/>',
}
# the same set under the keys preview_pop2 already uses, so every module that drew its own icon now draws this one
_ALIAS = {"shield": "intrusion", "key": "access", "door": "access", "phone": "mobile", "camera": "video", "cap": "training", "doc": "docs",
          "signal": "communicator", "flame": "fire", "headset": "support", "link": "partner"}
preview_pop2._IC.update({k: v for k, v in ICONS.items()})
preview_pop2._IC.update({a: ICONS[b] for a, b in _ALIAS.items()})


import preview_motion  # noqa: E402
# the home journey draws the same set: detect, decide, report, respond, control
preview_motion._JY_ICONS[:] = [ICONS["video"], ICONS["keypad"], ICONS["communicator"], ICONS["support"], ICONS["mobile"]]


def icon(key, size=24, sw=1.7):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS.get(key, ICONS["intrusion"])}</svg>')


# ------------------------------------------------------------------------------------------------ story
def _story(s, ctx):
    E, L = ctx["E"], ctx["L"]
    steps = s["steps"]
    n = len(steps)
    chips = "".join(f'<span class="dw2-chip{" on" if i == 0 else ""}" data-i="{i}" aria-hidden="true"><small>Step {i + 1} of {n}</small><b>{E(st["title"])}</b></span>'
                    for i, st in enumerate(steps))
    ticks = "".join(f'<i class="{"on" if i == 0 else ""}"></i>' for i in range(n))
    items = []
    for i, st in enumerate(steps):
        links = ""
        if st.get("links"):
            links = '<ul class="dw2-st-links">' + "".join(f'<li><a href="{E(L(h))}">{E(t)}</a></li>' for t, h in st["links"]) + "</ul>"
        cta = ""
        if st.get("cta"):
            cta = f'<a class="dw2-st-cta" href="{E(L(st["cta"][1]))}">{E(st["cta"][0])}<span aria-hidden="true">&rarr;</span></a>'
        items.append(f'<li class="dw2-st-step{" on" if i == 0 else ""}" data-i="{i}"><span class="dw2-st-n" aria-hidden="true">{i + 1:02d}</span>'
                     f'<div class="dw2-st-b"><h3>{E(st["title"])}</h3><p>{E(st["text"])}</p>{links}{cta}</div></li>')
    img = (f'<img src="{E(ctx["rel"](s["image"]))}"{ctx["srcset"](s["image"])} alt="{E(s.get("alt", ""))}" width="900" height="900" '
           f'decoding="async" loading="lazy">')
    head = (f'<div class="dw2-st-hd">{f"<div class=q-eyebrow>{E(s.get(chr(101) + chr(121) + chr(101) + chr(98) + chr(114) + chr(111) + chr(119)))}</div>" if s.get("eyebrow") else ""}'
            f'<h2 class="q-h2">{E(s["heading"])}</h2></div>')
    return (f'{ctx["sec_open"](s, "dw2-story")}<div class="q-container">{head}<div class="dw2-st-grid">'
            f'<div class="dw2-st-col"><div class="dw2-st-pin"><div class="dw2-st-stage" data-step="0">'
            f'<span class="dw2-glow" aria-hidden="true"></span><span class="dw2-ring r1" aria-hidden="true"></span><span class="dw2-ring r2" aria-hidden="true"></span>'
            f'<span class="dw2-st-prog" aria-hidden="true">{ticks}</span><div class="dw2-st-img">{img}</div><div class="dw2-chips">{chips}</div></div></div></div>'
            f'<ol class="dw2-st-steps">{"".join(items)}</ol></div></div></section>')


# ------------------------------------------------------------------------------------------------ map
MW, MH = 1440, 560            # 4 units per degree: x = (lon + 180) * 4, y = (82 - lat) * 4


def _xy(lat, lon):
    return (lon + 180) * 4, (82 - lat) * 4


def _land_path():
    out = []
    for j, row in enumerate(LM.ROWS):
        y = round((j + .5) * LM.STEP * 4, 1)
        for i, c in enumerate(row):
            if c == "1":
                out.append(f"M{round((i + .5) * LM.STEP * 4, 1)} {y}h0")
    return "".join(out)


_LAND = None


def _map(s, ctx):
    global _LAND
    E = ctx["E"]
    if _LAND is None:
        _LAND = _land_path()
    hx, hy = _xy(*s["hq"])
    arcs, pins, lst = [], [], []
    for i, it in enumerate(s["items"]):
        x, y = _xy(it["lat"], it["lon"])
        mx, my = (x + hx) / 2, (y + hy) / 2
        dist = ((x - hx) ** 2 + (y - hy) ** 2) ** .5
        cy = my - max(30, dist * .28)
        arcs.append(f'<path class="dw2-arc" style="--d:{i * .35:.2f}s" d="M{hx:.1f} {hy:.1f}Q{mx:.1f} {cy:.1f} {x:.1f} {y:.1f}"/>')
        left, top = x / MW * 100, y / MH * 100
        pos = ("l" if left > 58 else "r") + ("u" if top > 58 else "d")
        dom = re.sub(r"^https?://(www\.)?", "", it["url"]).rstrip("/")
        contact = f'<p class="dw2-pc-c">DMP contact: <b>{E(it["contact"])}</b></p>' if it.get("contact") else ""
        card = (f'<span class="dw2-pc-r">{E(it["region"])}</span><span class="dw2-pc-n">{E(it["company"])}</span>{contact}'
                f'<a class="dw2-pc-a" href="{E(it["url"])}" target="_blank" rel="noopener">{E(it["label"])}<small>{E(dom)}</small><span class="dw2-sr"> (opens in a new tab)</span></a>')
        pins.append(f'<div class="dw2-pin pos-{pos}" style="left:{left:.2f}%;top:{top:.2f}%;--d:{i * .4:.1f}s">'
                    f'<button type="button" class="dw2-pb" aria-expanded="false" aria-controls="dw2-pc{i}" aria-label="{E(it["region"])}: {E(it["company"])}"><i></i><i></i><b></b></button>'
                    f'<div class="dw2-pc" id="dw2-pc{i}" role="group" aria-label="{E(it["company"])}">{card}</div></div>')
        lst.append(f'<li class="dw2-ml-i"><span class="dw2-pc-r">{E(it["region"])}</span><span class="dw2-pc-n">{E(it["company"])}</span>{contact}'
                   f'<a class="dw2-pc-a" href="{E(it["url"])}" target="_blank" rel="noopener">{E(it["label"])}<small>{E(dom)}</small><span class="dw2-sr"> (opens in a new tab)</span></a></li>')
    hl = (f'<span class="dw2-hq" style="left:{hx / MW * 100:.2f}%;top:{hy / MH * 100:.2f}%"><i></i><span>{E(s["hq_label"])}</span></span>')
    head = (f'<div class="dw2-mp-hd"><div class="q-eyebrow">{E(s["eyebrow"])}</div><h2 class="q-h2">{E(s["heading"])}</h2>'
            f'<p class="q-lead">{E(s["intro"])}<span class="dw2-hint"> {E(s.get("hint", ""))}</span></p></div>')
    return (f'{ctx["sec_open"](s, "dw2-mapsec")}<div class="q-container">{head}'
            f'<div class="dw2-map" role="group" aria-label="{E(s.get("aria", "World map of authorized distributors"))}">'
            f'<svg class="dw2-svg" viewBox="0 0 {MW} {MH}" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">'
            f'<path class="dw2-land" d="{_LAND}"/>{"".join(arcs)}</svg>{hl}{"".join(pins)}</div>'
            f'<ul class="dw2-mlist">{"".join(lst)}</ul></div></section>')


RENDER_DW2 = {"dw2-story": _story, "dw2-map": _map}


# ------------------------------------------------------------------------------------------------ icons in existing modules
def wrap(RENDER):
    """Wrap the doors and cards renderers: a section with "icons": [key, ...] gets that icon on each item."""
    _doors, _cards = RENDER["doors"], RENDER["cards"]

    def doors(s, ctx):
        out = _doors(s, ctx)
        for it in s.get("items", []):
            if it.get("icon"):
                k = f'<span class="pp-door-k">{ctx["E"](it["kicker"])}</span>'
                out = out.replace(k, f'<span class="pp-door-k"><span class="dw2-di">{icon(it["icon"], 18, 2)}</span>{ctx["E"](it["kicker"])}</span>', 1)
        return out

    def cards(s, ctx):
        out = _cards(s, ctx)
        ics = s.get("icons")
        if ics:
            it = iter(ics)
            out = re.sub(r'<div class="q-card"><h3>', lambda m: f'<div class="q-card"><span class="dw2-ci">{icon(next(it, "intrusion"), 26)}</span><h3>', out)
        return out
    RENDER["doors"], RENDER["cards"] = doors, cards

    def anchored(name, key, center):
        orig = RENDER[name]

        def f(s, ctx):
            out = orig(s, ctx)
            return out.replace('<h2 class="q-h2"', f'<div class="dw2-hbw{" c" if center else ""}"><span class="dw2-ci" aria-hidden="true">{icon(key, 26)}</span></div><h2 class="q-h2"', 1)
        RENDER[name] = f
    _stats = RENDER["stats3d"]

    def stats(s, ctx):          # the stat band built its own class list and ignored the section flags
        out = _stats(s, ctx)
        return out.replace('class="q-section mo-stats"', 'class="q-section mo-stats q-bg-alt"', 1) if s.get("alt") else out
    RENDER["stats3d"] = stats
    # headings that had no visual anchor get an icon badge
    anchored("faq", "support", True)
    anchored("contact", "support", False)
    anchored("leadform", "docs", False)


# ------------------------------------------------------------------------------------------------ footer
def footer(content, ctx):
    E, L = ctx["E"], ctx["L"]
    b = content["brand"]
    lw, lh = b.get("logo_w", 300), b.get("logo_h", 100)
    logo = (f'<img class="dw2-flogo" src="{E(ctx["rel"](b["logo"]))}" alt="{E(b.get("logo_alt", content["client"]))}" width="{round(36 * lw / lh)}" height="36" loading="lazy">'
            if b.get("logo") else f'<span class="q-logo-text">{E(content["client"])}</span>')
    fic = {"Products": "keypad", "Industries": "access", "Support and training": "support", "Company": "docs"}
    cols = "".join(
        f'<div class="dw2-fc"><div class="q-footer-head"><span aria-hidden="true">{icon(fic.get(c["title"], "partner"), 20, 1.8)}</span>{E(c["title"])}</div>'
        f'<nav class="q-footer-links" aria-label="{E(c["title"])}">' + "".join(f'<a href="{E(L(h))}">{E(l)}</a>' for l, h in c["links"]) + "</nav></div>"
        for c in b.get("footer_columns", []))
    soc = b.get("social", {})
    _names = {"linkedin": "LinkedIn", "facebook": "Facebook", "x": "X", "instagram": "Instagram", "youtube": "YouTube"}
    social = "".join(f'<a href="{E(u)}" aria-label="{E(_names.get(k, k.title()))}">{E(_names.get(k, k.title()))}</a>' for k, u in soc.items() if u)
    social = f'<div class="q-footer-social">{social}</div>' if social else ""
    phone, phone_href = b.get("phone", ""), b.get("phone_href", "")
    email = b.get("email", "")
    legal = "".join(f'<a href="{E(L(h))}">{E(l)}</a>' for l, h in b.get("legal", []))
    arrow = '<svg viewBox="0 0 24 24" width="0.6em" height="0.6em" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
    call = ""
    if phone:
        mail = f' Or write to <a href="mailto:{E(email)}">{E(email)}</a>.' if email else ""
        call = (f'<a class="dw2-fphone q-footer-phone" href="{E(phone_href)}"><span>{E(phone)}</span>{arrow}</a>'
                f'<div class="dw2-frow"><p class="dw2-fnote">Inside Sales, 8 a.m. to 5 p.m. Central.{mail}</p>@@BTNS@@</div>')
    btns = (f'<div class="dw2-fcta-b"><a class="dw2-fbtn" href="{E(L("find-a-dealer.html"))}">Find a dealer<span aria-hidden="true">&rarr;</span></a>'
            f'<a class="dw2-fbtn ghost" href="{E(L("contact.html"))}">Contact DMP</a></div>')
    return f'''</div>
<footer class="q-footer dw2-foot"><span class="dw2-fedge" aria-hidden="true"></span><span class="dw2-fglow" aria-hidden="true"></span>
<div class="q-container dw2-fcta"><h2 class="dw2-fh">Talk to a person at DMP</h2>{call.replace("@@BTNS@@", btns)}</div>
<div class="q-container dw2-fgrid pv-fcols-{len(b.get("footer_columns", []))}"><div class="dw2-fbrand">{logo}<p class="q-footer-tag">{E(b.get("tagline"))}</p>{social}</div>{cols}</div>
<div class="q-container q-footer-legal dw2-flegal"><span class="pv-legal-item">Copyright &copy; {ctx["year"]} {E(content["client"])}</span><span class="dw2-fl">{legal}</span></div></footer>'''


# ------------------------------------------------------------------------------------------------ CSS
DW2_CSS = r"""
/* ===== dw2: shared ===== */
.dw2-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.dw2-ci{display:grid;place-items:center;width:54px;height:54px;border-radius:16px;background:var(--q-gold);color:#111;margin-bottom:18px;box-shadow:0 14px 26px -14px rgba(255,210,61,.9)}
.dw2-hbw{margin:0 0 4px}.dw2-hbw.c{text-align:center}.dw2-hbw .dw2-ci{margin-bottom:12px}
.dw2-di{display:inline-grid;place-items:center;vertical-align:-4px;margin-right:7px}
.pp-door-k{display:inline-flex;align-items:center}

/* ===== dw2: rhythm: text-only detail blocks, stat bands and form sections ===== */
.pv-detail:has(>div:last-child>ul:only-child){align-items:center}
.pv-detail>div:last-child>ul:only-child{list-style:none;margin:0;padding:0;display:grid;gap:12px}
.pv-detail>div:last-child>ul:only-child li{position:relative;margin:0;padding:20px 22px 20px 66px;border-radius:18px;background:var(--card);border:1px solid var(--border);box-shadow:0 1px 2px rgba(17,24,39,.05),0 18px 34px -26px rgba(17,24,39,.3);line-height:1.5;font-size:17px}
.pv-detail>div:last-child>ul:only-child li::before{content:"";position:absolute;left:22px;top:21px;width:28px;height:28px;border-radius:50%;background:var(--q-gold)}
.pv-detail>div:last-child>ul:only-child li::after{content:"";position:absolute;left:32px;top:27px;width:7px;height:12px;border:solid #111;border-width:0 2.5px 2.5px 0;transform:rotate(40deg)}
/* the stat band follows the section flags (it set its own background before) */
.q-section.mo-stats.q-bg-alt:not(.lf-dark){background:linear-gradient(180deg,var(--bg-alt),color-mix(in srgb,var(--bg-alt) 62%,var(--bg)))}
@media(min-width:1025px){
 .q-section.mo-stats{padding-top:84px;padding-bottom:84px}
 .q-section:has(>.pv-contact){padding-top:96px;padding-bottom:96px}
}

/* ===== dw2: pinned story ===== */
.dw2-story{padding:clamp(56px,7vw,104px) 0 clamp(48px,6vw,88px);overflow:clip}
.dw2-st-hd{text-align:center;max-width:820px;margin:0 auto clamp(32px,4vw,56px)}
.dw2-st-hd .q-h2{margin:20px 0 0}
.dw2-st-grid{display:grid;grid-template-columns:minmax(0,1.04fr) minmax(0,1fr);gap:clamp(32px,5vw,96px);align-items:start}
.dw2-st-col{align-self:stretch;min-width:0}
.dw2-st-stage{position:relative;isolation:isolate;overflow:hidden;border-radius:30px;aspect-ratio:1/1;max-height:calc(100vh - 210px);min-height:340px;margin:0 auto;width:100%;
  background:radial-gradient(120% 90% at 50% 0%,#1b2b4a 0%,#0b1220 62%);color:#fff;box-shadow:0 50px 90px -48px rgba(11,18,32,.9),0 0 0 1px rgba(255,255,255,.08) inset;
  --tx:0%;--ty:0%;--rot:-4deg;--sc:1;--gx:50%;--gy:52%;--rx:0%;--ry:0%;--rs:1}
.dw2-st-stage::before{content:"";position:absolute;inset:0;z-index:-1;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:44px 44px;mask-image:radial-gradient(ellipse at 50% 50%,#000 25%,transparent 75%);-webkit-mask-image:radial-gradient(ellipse at 50% 50%,#000 25%,transparent 75%)}
.dw2-glow{position:absolute;inset:0;z-index:0;background:radial-gradient(circle at var(--gx) var(--gy),rgba(255,210,61,.42),rgba(255,210,61,.08) 34%,transparent 58%);transition:background-position .9s}
.dw2-ring{position:absolute;left:50%;top:50%;border-radius:50%;border:2px solid rgba(255,210,61,.7);z-index:1;pointer-events:none;
  transform:translate(calc(-50% + var(--rx)),calc(-50% + var(--ry))) scale(var(--rs));transition:transform 1s cubic-bezier(.2,.7,.2,1)}
.dw2-ring.r1{width:62%;aspect-ratio:1/1}
.dw2-ring.r2{width:84%;aspect-ratio:1/1;border:1px dashed rgba(255,255,255,.4);transition-duration:1.3s}
.dw2-ring.r1::after{content:"";position:absolute;right:6%;top:14%;width:14px;height:14px;border-radius:50%;background:#ffd23d;box-shadow:0 0 0 6px rgba(255,210,61,.28),0 0 24px 4px #ffd23d}
.dw2-st-img{position:absolute;inset:0;z-index:2;display:grid;place-items:center}
.dw2-st-img{padding-bottom:12%}
.dw2-st-img img{width:70%;height:64%;object-fit:contain;filter:drop-shadow(0 34px 34px rgba(0,0,0,.55));
  transform:translate(var(--tx),var(--ty)) rotate(var(--rot)) scale(var(--sc));transition:transform 1s cubic-bezier(.2,.7,.2,1)}
.dw2-st-prog{position:absolute;left:24px;right:24px;top:22px;z-index:4;display:flex;gap:8px}
.dw2-st-prog i{flex:1;height:4px;border-radius:2px;background:rgba(255,255,255,.22);transition:background .5s}
.dw2-st-prog i.on{background:#ffd23d}
.dw2-chips{position:absolute;left:22px;right:22px;bottom:22px;z-index:4;min-height:84px}
.dw2-chip{position:absolute;left:0;bottom:0;max-width:min(100%,430px);display:flex;flex-direction:column;gap:3px;padding:13px 20px 14px;border-radius:18px;background:#ffd23d;color:#111;box-shadow:0 20px 36px -18px rgba(0,0,0,.85);visibility:hidden;opacity:0;transform:translateY(14px);transition:transform .5s cubic-bezier(.2,.7,.2,1),opacity .3s,visibility 0s .3s}
.dw2-chip.on{visibility:visible;opacity:1;transform:none;transition:transform .6s cubic-bezier(.2,.7,.2,1) .15s,opacity .4s .15s,visibility 0s}
.dw2-chip small{font-size:13px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#4a3b00}
.dw2-chip b{font-size:clamp(16px,1.4vw,19px);line-height:1.25;font-weight:800}
/* per step: where the product, the glow and the rings sit */
.dw2-st-stage[data-step="0"]{--rot:-4deg;--sc:1;--tx:0%;--ty:-2%;--gx:50%;--gy:48%;--rx:0%;--ry:-2%;--rs:1}
.dw2-st-stage[data-step="1"]{--rot:5deg;--sc:1.1;--tx:-5%;--ty:2%;--gx:34%;--gy:60%;--rx:-9%;--ry:3%;--rs:1.08}
.dw2-st-stage[data-step="2"]{--rot:-9deg;--sc:.92;--tx:5%;--ty:-4%;--gx:68%;--gy:36%;--rx:8%;--ry:-6%;--rs:.94}
.dw2-st-stage[data-step="3"]{--rot:2deg;--sc:1.04;--tx:0%;--ty:3%;--gx:50%;--gy:66%;--rx:0%;--ry:5%;--rs:1.14}
/* steps */
.dw2-st-steps{list-style:none;margin:0;padding:0;display:grid;gap:18px;counter-reset:none}
.dw2-st-step{position:relative;display:grid;grid-template-columns:auto 1fr;gap:20px;padding:30px 30px 32px;border-radius:24px;background:var(--card);border:1px solid var(--border);box-shadow:0 1px 2px rgba(17,24,39,.05),0 24px 44px -30px rgba(17,24,39,.35)}
.dw2-st-n{font-family:var(--q-display,var(--q-sans));font-weight:800;font-size:clamp(46px,5vw,76px);line-height:.9;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:2px var(--accent-ink);min-width:1.55em}
.dw2-st-b h3{margin:0 0 12px;font-size:clamp(23px,2.2vw,34px);line-height:1.12;letter-spacing:-.02em}
.dw2-st-b p{margin:0;font-size:clamp(17px,1.2vw,19px);line-height:1.6;color:var(--fg-muted)}
.dw2-st-links{list-style:none;margin:20px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.dw2-st-links a{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border-radius:999px;border:1px solid var(--border);background:var(--bg);color:var(--fg);font-weight:700;font-size:15px;text-decoration:none;transition:background .25s,border-color .25s,transform .25s}
.dw2-st-links a:hover{background:var(--q-gold);border-color:var(--q-gold);color:#111;transform:translateY(-2px)}
.dw2-st-cta{display:inline-flex;align-items:center;gap:10px;margin-top:20px;min-height:48px;padding:0 24px;border-radius:999px;background:var(--q-gold);color:#111;font-weight:800;font-size:15.5px;text-decoration:none;box-shadow:0 14px 30px -14px rgba(255,210,61,.9);transition:transform .3s}
.dw2-st-cta:hover{transform:translateY(-2px)}
.dw2-st-cta+.dw2-st-links,.dw2-st-links+.dw2-st-cta{margin-top:14px}
.dw2-st-links a:focus-visible,.dw2-st-cta:focus-visible{outline:3px solid var(--q-gold);outline-offset:3px}
/* desktop with JS: the stage pins, the steps scroll past */
@media(min-width:1025px){
 html.pv-js .dw2-st-pin{position:sticky;top:164px}
 html.pv-js .dw2-st-steps{gap:0;padding:6vh 0 14vh}
 html.pv-js .dw2-st-step{min-height:58vh;align-content:center;background:transparent;border-color:transparent;box-shadow:none;padding:30px 0 30px 34px;border-radius:0;border-left:3px solid var(--border);transition:border-color .6s}
 html.pv-js .dw2-st-step .dw2-st-b h3,html.pv-js .dw2-st-step .dw2-st-b p{transition:color .6s}
 html.pv-js .dw2-st-step:not(.on) .dw2-st-b h3{color:var(--fg-muted)}
 html.pv-js .dw2-st-step:not(.on) .dw2-st-n{-webkit-text-stroke-color:var(--fg-muted)}
 html.pv-js .dw2-st-step.on{border-left-color:var(--q-gold)}
}
@media(max-width:1024px){
 .dw2-st-grid{grid-template-columns:minmax(0,1fr);gap:26px}
 .dw2-st-stage{aspect-ratio:16/10;max-height:none;min-height:0;max-width:640px}
 .dw2-st-img img{width:62%;height:78%}
 .dw2-st-prog,.dw2-chips{display:none}
 .dw2-st-steps{max-width:640px;margin:0 auto;width:100%}
}
@media(max-width:560px){.dw2-st-step{grid-template-columns:minmax(0,1fr);gap:8px;padding:24px 22px 26px}.dw2-st-n{font-size:48px}.dw2-st-stage{border-radius:22px;aspect-ratio:4/3}}
@media(prefers-reduced-motion:reduce){.dw2-st-img img,.dw2-ring,.dw2-glow,.dw2-chip,.dw2-st-prog i{transition:none!important}}

/* ===== dw2: world map ===== */
.dw2-mapsec{padding:clamp(64px,8vw,112px) 0 clamp(56px,7vw,96px)}
.dw2-mp-hd{text-align:center;max-width:780px;margin:0 auto clamp(30px,4vw,48px)}
.dw2-mp-hd .q-h2{margin:20px 0 0;color:#fff}
.dw2-mp-hd .q-lead{margin:16px auto 0;max-width:620px}
.dw2-map{position:relative;width:100%;max-width:1240px;margin:0 auto;aspect-ratio:1440/560;border-radius:28px;background:radial-gradient(100% 90% at 50% 0%,rgba(255,210,61,.07),transparent 60%),rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.12)}
.dw2-svg{position:absolute;inset:0;width:100%;height:100%;overflow:hidden;border-radius:28px}
.dw2-land{fill:none;stroke:rgba(205,216,240,.5);stroke-width:5.4;stroke-linecap:round}
.dw2-arc{fill:none;stroke:#ffd23d;stroke-width:1.6;stroke-linecap:round;stroke-dasharray:3 9;opacity:.8;animation:dw2-dash 2.4s linear infinite;animation-delay:var(--d)}
@keyframes dw2-dash{to{stroke-dashoffset:-48}}
.dw2-hq{position:absolute;transform:translate(-50%,-50%);z-index:2;display:flex;align-items:center;pointer-events:none}
.dw2-hq i{width:16px;height:16px;border-radius:50%;background:#fff;box-shadow:0 0 0 5px rgba(255,255,255,.25),0 0 22px 4px rgba(255,255,255,.5);flex:0 0 auto}
.dw2-hq span{position:absolute;left:-4px;top:20px;white-space:nowrap;font-size:13px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#fff;padding:4px 10px;border-radius:999px;background:rgba(11,18,32,.82)}
.dw2-pin{position:absolute;width:0;height:0;z-index:3}
.dw2-pin:hover,.dw2-pin:focus-within,.dw2-pin.open{z-index:9}
.dw2-pb{position:absolute;left:-22px;top:-22px;width:44px;height:44px;padding:0;border:0;border-radius:50%;background:transparent;cursor:pointer;display:grid;place-items:center}
.dw2-pb b{position:absolute;width:15px;height:15px;border-radius:50%;background:#ffd23d;box-shadow:0 0 0 3px #0b1220,0 0 18px 2px rgba(255,210,61,.8);transition:transform .25s}
.dw2-pb i{position:absolute;width:15px;height:15px;border-radius:50%;border:2px solid #ffd23d;animation:dw2-pulse 2.6s ease-out infinite;animation-delay:var(--d);pointer-events:none}
.dw2-pb i+i{animation-delay:calc(var(--d) + 1.3s)}
@keyframes dw2-pulse{0%{transform:scale(1);opacity:.9}100%{transform:scale(3.3);opacity:0}}
.dw2-pb:hover b,.dw2-pb:focus-visible b,.dw2-pin.open .dw2-pb b{transform:scale(1.3)}
.dw2-pb:focus-visible{outline:3px solid #fff;outline-offset:1px}
.dw2-pc{position:absolute;z-index:2;width:268px;padding:16px 18px 18px;border-radius:18px;background:#fff;color:#111827;box-shadow:0 30px 60px -20px rgba(0,0,0,.7),0 0 0 2px #ffd23d;display:flex;flex-direction:column;gap:5px;visibility:hidden;opacity:0;transform:translateY(6px);transition:opacity .2s,transform .2s,visibility 0s .2s;text-align:left}
.dw2-pin.pos-rd .dw2-pc{left:20px;top:14px}.dw2-pin.pos-ld .dw2-pc{right:20px;top:14px}
.dw2-pin.pos-ru .dw2-pc{left:20px;bottom:14px}.dw2-pin.pos-lu .dw2-pc{right:20px;bottom:14px}
.dw2-pin:hover .dw2-pc,.dw2-pin:focus-within .dw2-pc,.dw2-pin.open .dw2-pc{visibility:visible;opacity:1;transform:none;transition:opacity .2s,transform .2s,visibility 0s}
.dw2-pin.off .dw2-pc{visibility:hidden!important;opacity:0!important}
.dw2-pc-r{font-size:13px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#6b5200;line-height:1.3}
.dw2-pc-n{font-family:var(--q-display,var(--q-sans));font-size:23px;font-weight:800;line-height:1.1;letter-spacing:-.02em;color:#111827}
.dw2-pc-c{margin:2px 0 0;font-size:15px;line-height:1.4;color:#374151}.dw2-pc-c b{color:#111827}
.dw2-pc-a{display:flex;flex-direction:column;justify-content:center;margin-top:8px;min-height:44px;padding:6px 16px;border-radius:12px;background:#ffd23d;color:#111;font-weight:800;font-size:15px;text-decoration:none;line-height:1.25}
.dw2-pc-a small{font-size:13px;font-weight:600;color:#3b3200}
.dw2-pc-a:hover{background:#ffe27a}.dw2-pc-a:focus-visible{outline:3px solid #111;outline-offset:2px}
.dw2-mlist{display:none}
@media(max-width:700px){.dw2-hint{display:none}}
@media(max-width:1024px){.dw2-pc{width:236px}.dw2-hq span{font-size:13px}}
@media(max-width:700px){
 .dw2-map{display:none}
 .dw2-mlist{display:grid;gap:12px;list-style:none;margin:0;padding:0}
 .dw2-ml-i{display:flex;flex-direction:column;gap:5px;padding:18px 20px 20px;border-radius:18px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.16)}
 .dw2-ml-i .dw2-pc-r{color:#ffd23d}.dw2-ml-i .dw2-pc-n{color:#fff}.dw2-ml-i .dw2-pc-c{color:var(--fg-muted)}.dw2-ml-i .dw2-pc-c b{color:#fff}
}
@media(prefers-reduced-motion:reduce){.dw2-arc,.dw2-pb i{animation:none}.dw2-pb i{display:none}.dw2-pc{transition:none}}

/* ===== dw2: closing footer ===== */
.q-footer.dw2-foot{position:relative;isolation:isolate;overflow:hidden;background:#0b1220;border-top:0;color:#f4f6fb;padding:0;
  --chrome-fg:#f4f6fb;--chrome-muted:#c0c9dc;--chrome-border:rgba(255,255,255,.14);--chrome-accent:#ffd23d}
.dw2-fedge{position:absolute;left:0;right:0;top:0;height:5px;z-index:2;background:linear-gradient(90deg,#ffd23d,#ff9a3d,#ff5a5a,#7a8cff,#35d0ba,#ffd23d);background-size:240% 100%;animation:dw2-edge 14s linear infinite}
@keyframes dw2-edge{to{background-position:240% 0}}
.dw2-fglow{position:absolute;left:-10%;right:-10%;top:-30%;height:80%;z-index:-1;pointer-events:none;background:radial-gradient(40% 60% at 22% 30%,rgba(255,210,61,.22),transparent 70%),radial-gradient(34% 55% at 80% 20%,rgba(122,140,255,.2),transparent 70%);animation:dw2-drift 18s ease-in-out infinite alternate}
@keyframes dw2-drift{to{transform:translate3d(4%,6%,0) scale(1.08)}}
.q-footer.dw2-foot::after{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:56px 56px;mask-image:radial-gradient(ellipse at 30% 10%,#000 10%,transparent 70%);-webkit-mask-image:radial-gradient(ellipse at 30% 10%,#000 10%,transparent 70%)}
.dw2-fcta{padding-top:clamp(64px,8vw,116px);padding-bottom:clamp(48px,6vw,84px)}
.dw2-fh{margin:0;font-family:var(--q-display,var(--q-sans));font-weight:800;font-size:clamp(34px,5.4vw,84px);line-height:1;letter-spacing:-.04em;color:#fff}
.dw2-fphone{display:inline-flex;align-items:center;gap:.28em;margin-top:clamp(14px,2vw,26px);min-height:44px;white-space:nowrap;max-width:100%;font-family:var(--q-display,var(--q-sans));font-weight:800;font-size:clamp(38px,10.4vw,148px);line-height:1;letter-spacing:-.05em;text-decoration:none;color:#ffd23d;transition:color .3s}
.q-footer.dw2-foot .q-footer-phone{color:#ffd23d}
.dw2-fphone span{background:linear-gradient(100deg,#ffd23d 20%,#fff0a8 50%,#ffd23d 80%);background-size:220% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;transition:background-position .6s}
.dw2-fphone:hover span{background-position:100% 0}
.dw2-fphone svg{transition:transform .35s;color:#ffd23d}.dw2-fphone:hover svg{transform:translateX(.12em)}
.dw2-fphone:focus-visible{outline:3px solid #ffd23d;outline-offset:6px;border-radius:12px}
.dw2-frow{display:flex;align-items:center;justify-content:space-between;gap:20px 40px;flex-wrap:wrap;margin-top:clamp(18px,2.4vw,30px)}
.dw2-fnote{margin:0;flex:1 1 320px;font-size:17px;line-height:1.5;color:#c0c9dc}
.dw2-fnote a{color:#fff;text-decoration:underline;text-underline-offset:3px}
.dw2-fcta-b{display:flex;gap:12px;flex-wrap:wrap}
.dw2-fbtn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:56px;padding:0 30px;border-radius:999px;background:#ffd23d;color:#111;font-weight:800;font-size:17px;text-decoration:none;border:2px solid #ffd23d;box-shadow:0 18px 38px -16px rgba(255,210,61,.85);transition:transform .3s,background .3s,box-shadow .3s}
.dw2-fbtn:hover{transform:translateY(-3px);background:#ffe27a;border-color:#ffe27a}
.dw2-fbtn.ghost{background:transparent;color:#fff;border-color:rgba(255,255,255,.55);box-shadow:none}.dw2-fbtn.ghost:hover{background:rgba(255,255,255,.1);border-color:#fff}
.dw2-fbtn:focus-visible{outline:3px solid #fff;outline-offset:3px}
.dw2-fgrid{display:grid;grid-template-columns:1.3fr repeat(4,1fr);gap:clamp(28px,3vw,56px);padding-top:clamp(40px,5vw,64px);padding-bottom:clamp(36px,4vw,52px);border-top:1px solid rgba(255,255,255,.14);align-items:start}
.dw2-fgrid.pv-fcols-3{grid-template-columns:1.3fr repeat(3,1fr)}
.dw2-flogo{height:36px;width:auto;filter:brightness(0) invert(1)}
.q-footer.dw2-foot .q-footer-tag{margin:20px 0 18px;max-width:300px;font-size:16px;line-height:1.55;color:#c0c9dc}
.q-footer.dw2-foot .q-footer-head{display:flex;align-items:center;gap:10px;margin:0 0 12px;font-size:13px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#fff}
.q-footer.dw2-foot .q-footer-head span{display:grid;place-items:center;width:34px;height:34px;border-radius:10px;background:rgba(255,210,61,.14);color:#ffd23d}
.q-footer.dw2-foot .q-footer-links a{color:#c0c9dc;font-size:15.5px;min-height:44px;transition:color .2s,transform .2s}
.q-footer.dw2-foot .q-footer-links a:hover{color:#ffd23d;transform:translateX(4px)}
.q-footer.dw2-foot a:focus-visible{outline:3px solid #ffd23d;outline-offset:2px;border-radius:4px}
.q-footer.dw2-foot .q-footer-social a{color:#c0c9dc}
.q-footer.dw2-foot .q-footer-legal.dw2-flegal{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:4px 24px;margin:0 auto;padding-top:14px;padding-bottom:calc(14px + env(safe-area-inset-bottom,0px));border-top:1px solid rgba(255,255,255,.14);text-align:left;font-size:14px;color:#c0c9dc}
.dw2-fl{display:flex;flex-wrap:wrap;gap:0 8px}.dw2-fl a{display:inline-flex;align-items:center;min-height:44px;padding:0 10px}
.q-footer.dw2-foot .q-footer-legal a{color:#c0c9dc;text-decoration:none}.q-footer.dw2-foot .q-footer-legal a:hover{color:#ffd23d;text-decoration:underline}
@media(min-width:768px) and (max-width:1100px){.dw2-fgrid,.dw2-fgrid.pv-fcols-3{grid-template-columns:repeat(2,1fr)}.dw2-fbrand{grid-column:1/-1}}
@media(max-width:767px){.dw2-fgrid,.dw2-fgrid.pv-fcols-3{grid-template-columns:repeat(2,minmax(0,1fr));gap:30px 20px}.dw2-fbrand{grid-column:1/-1}.dw2-fcta-b{width:100%}.dw2-fbtn{flex:1 1 200px}}
@media(max-width:480px){.dw2-fgrid,.dw2-fgrid.pv-fcols-3{grid-template-columns:minmax(0,1fr)}.q-footer.dw2-foot .q-footer-legal.dw2-flegal{flex-direction:column;align-items:flex-start}}
@media(prefers-reduced-motion:reduce){.dw2-fedge,.dw2-fglow{animation:none}.q-footer.dw2-foot .q-footer-links a,.dw2-fbtn{transition:none}}
/* final fixes (lead): proof band caption centered; dealer portal sign-in frame not oversized before sign-in */
.pp-proof .pp-pr-foot{width:100%;max-width:820px;margin:clamp(40px,5vw,72px) auto 0;padding:0}
.mo-screen:not(.is-in){height:510px;min-height:0;overflow:hidden}
@media(max-width:767px){.mo-screen:not(.is-in){height:470px}}
"""

# ------------------------------------------------------------------------------------------------ JS
DW2_JS = r"""
(function(){
var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
/* pinned story: the step in the middle band of the viewport owns the stage */
document.querySelectorAll('.dw2-story').forEach(function(sec){
  var stage=sec.querySelector('.dw2-st-stage'),steps=[].slice.call(sec.querySelectorAll('.dw2-st-step')),
      chips=[].slice.call(sec.querySelectorAll('.dw2-chip')),ticks=[].slice.call(sec.querySelectorAll('.dw2-st-prog i'));
  if(!stage||!steps.length)return;
  function set(i){stage.setAttribute('data-step',i);
    steps.forEach(function(s,k){s.classList.toggle('on',k===i)});
    chips.forEach(function(c,k){c.classList.toggle('on',k===i)});
    ticks.forEach(function(t,k){t.classList.toggle('on',k<=i)});}
  if(!('IntersectionObserver' in window))return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)set(+e.target.getAttribute('data-i'))})},{rootMargin:'-44% 0px -44% 0px'});
  steps.forEach(function(s){io.observe(s)});
});
/* distributor map: hover and focus work in CSS; click toggles for touch, Escape closes */
document.querySelectorAll('.dw2-map').forEach(function(map){
  var pins=[].slice.call(map.querySelectorAll('.dw2-pin'));
  function closeAll(except){pins.forEach(function(p){if(p!==except){p.classList.remove('open');p.querySelector('.dw2-pb').setAttribute('aria-expanded','false')}})}
  pins.forEach(function(p){
    var b=p.querySelector('.dw2-pb');
    b.addEventListener('click',function(e){var o=!p.classList.contains('open');p.classList.remove('off');closeAll(p);p.classList.toggle('open',o);b.setAttribute('aria-expanded',o?'true':'false');e.stopPropagation()});
    p.addEventListener('mouseenter',function(){closeAll(p)});p.addEventListener('focusin',function(){closeAll(p)});
    p.addEventListener('mouseleave',function(){p.classList.remove('off')});
    p.addEventListener('focusout',function(){setTimeout(function(){if(!p.contains(document.activeElement)){p.classList.remove('off')}},0)});
  });
  document.addEventListener('click',function(e){if(!map.contains(e.target))closeAll()});
  map.addEventListener('keydown',function(e){
    if(e.key==='Escape'){var p=e.target.closest&&e.target.closest('.dw2-pin');closeAll();if(p){p.classList.add('off');p.classList.remove('open');p.querySelector('.dw2-pb').focus()}}
    if(e.key==='ArrowRight'||e.key==='ArrowDown'||e.key==='ArrowLeft'||e.key==='ArrowUp'){
      var cur=pins.indexOf(e.target.closest('.dw2-pin'));if(cur<0)return;
      var d=(e.key==='ArrowRight'||e.key==='ArrowDown')?1:-1,n=pins[(cur+d+pins.length)%pins.length];n.querySelector('.dw2-pb').focus();e.preventDefault()}
  });
});
})();
"""
