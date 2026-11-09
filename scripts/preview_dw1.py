"""Design wow pass 1: section types, mega menus, and global polish (CSS and JS).

New section types (read the theme variables, so Showcase, Clean and Press all pick them up):
  dwbuilding  an interactive cutaway of a building in flat brand colors on a dark stage. Eight glowing hotspots; hover,
              focus or tap one and the products that belong there appear, each with its cutout and a link. A guided tour
              steps through the stops. Phones: the hotspots drop away and a vertical accordion sits under the drawing.
  dwanatomy   a product cutout large on a dark stage with numbered callouts around it and leader lines to the frame
              edge. The callouts list the features named on the product page. They never point at a component, because
              the page text does not say where anything sits.

Global pieces in this file:
  mega_panel / mega_mobile  rich mega menu panels (products, industries, support) and their phone accordions, called from
                            header() in preview.py when a nav item carries dw_mega.
  DW1_CSS / DW1_JS          mega menu behaviour, header that condenses without moving the page, cursor spotlight, grain and
                            a slow gradient mesh on dark stages, View Transitions between pages, focus rings and pressed states.

Server HTML is complete without JS (the building lists every stop with its products, the anatomy is a plain list, the
mega menus open on hover and focus-within). prefers-reduced-motion: no pulse, no mesh drift, no spotlight, no transitions.
No em or en dashes. Rules: nothing under 13px, 44px tap targets.
"""
from __future__ import annotations

import html
import os
import re

_ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "brands", "digital-monitoring-products.assets")


def E(s) -> str:
    s = "" if s is None else str(s)
    s = re.sub(r"\s*[—–]\s*", ", ", s)
    return html.escape(s, quote=True)


def _small(path: str) -> str:
    """Prefer the 600px variant when the build has it (mega menu images are small)."""
    if "-1200-cut." in path:
        cand = path.replace("-1200-cut.", "-1200-cut-600.")
    elif "-1200." in path:
        cand = path.replace("-1200.", "-600.")
    else:
        return path
    return cand if os.path.exists(os.path.join(_ASSETS, os.path.basename(cand))) else path


# ============================================================================================ building

_SVG = """<svg class="dw-svg" viewBox="0 0 1000 560" role="img" aria-label="A cutaway drawing of a commercial building with a roof communicator, windows, a main door, a panel room, a stairwell, a teller and vault area and a parking gate, plus an owner's phone">
<defs>
<linearGradient id="dwg-glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4a8bc9"/><stop offset="1" stop-color="#1f4470"/></linearGradient>
<linearGradient id="dwg-ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a2744"/><stop offset="1" stop-color="#0b1220"/></linearGradient>
<linearGradient id="dwg-wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b2a4a"/><stop offset="1" stop-color="#15213b"/></linearGradient>
<pattern id="dwg-stripe" width="20" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#ffd23d"/><rect x="10" width="10" height="10" fill="#111827"/></pattern>
<radialGradient id="dwg-sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd23d" stop-opacity=".28"/><stop offset="1" stop-color="#ffd23d" stop-opacity="0"/></radialGradient>
</defs>
<circle cx="880" cy="140" r="180" fill="url(#dwg-sun)"/>
<circle cx="331" cy="70" r="120" fill="url(#dwg-sun)" opacity=".7"/>
<g class="dw-ground"><rect x="0" y="470" width="1000" height="90" fill="url(#dwg-ground)"/><rect x="720" y="470" width="280" height="14" fill="#223255"/>
<path d="M740 477H990" stroke="#3a4f7e" stroke-width="2" stroke-dasharray="14 12"/><path d="M0 470.5H1000" stroke="#33477a" stroke-width="2"/></g>
<g class="dw-shell">
<rect x="110" y="140" width="620" height="330" rx="3" fill="#121c33" stroke="#33477a" stroke-width="3"/>
<rect x="118" y="148" width="512" height="98" fill="url(#dwg-wall)"/>
<rect x="118" y="258" width="184" height="98" fill="#0f182c"/><rect x="308" y="258" width="322" height="98" fill="url(#dwg-wall)"/>
<rect x="118" y="368" width="300" height="100" fill="url(#dwg-wall)"/><rect x="424" y="368" width="206" height="100" fill="#1c2c4e"/>
<rect x="636" y="148" width="86" height="320" fill="#0f182c"/>
<rect x="110" y="246" width="620" height="12" fill="#2c3f69"/><rect x="110" y="356" width="620" height="12" fill="#2c3f69"/><rect x="630" y="140" width="6" height="328" fill="#2c3f69"/>
<rect x="96" y="124" width="648" height="18" rx="3" fill="#2c3f69"/><rect x="96" y="124" width="648" height="3" fill="#ffd23d" opacity=".85"/>
</g>
<g class="dw-win" fill="url(#dwg-glass)" stroke="#7fa6d6" stroke-width="2" stroke-opacity=".7">
<rect x="136" y="170" width="46" height="54" rx="3"/><rect x="202" y="170" width="46" height="54" rx="3"/><rect x="268" y="170" width="46" height="54" rx="3"/><rect x="334" y="170" width="46" height="54" rx="3"/><rect x="400" y="170" width="46" height="54" rx="3"/><rect x="466" y="170" width="46" height="54" rx="3"/><rect x="532" y="170" width="46" height="54" rx="3"/>
<rect x="326" y="280" width="46" height="54" rx="3"/><rect x="392" y="280" width="46" height="54" rx="3"/><rect x="458" y="280" width="46" height="54" rx="3"/><rect x="524" y="280" width="46" height="54" rx="3"/>
<rect x="262" y="394" width="56" height="48" rx="3"/><rect x="336" y="394" width="56" height="48" rx="3"/>
</g>
<g stroke="#7fa6d6" stroke-opacity=".5" stroke-width="2"><path d="M159 170V224M225 170V224M291 170V224M357 170V224M423 170V224M489 170V224M555 170V224M349 280V334M415 280V334M481 280V334M547 280V334M290 394V442M364 394V442"/></g>
<g fill="#2c3f69"><rect x="150" y="232" width="110" height="7" rx="2"/><rect x="290" y="232" width="110" height="7" rx="2"/><rect x="430" y="232" width="110" height="7" rx="2"/><rect x="340" y="340" width="110" height="7" rx="2"/><rect x="470" y="340" width="110" height="7" rx="2"/></g>
<g class="dw-panelroom"><g fill="#0a1222" stroke="#3a4f7e" stroke-width="2"><rect x="134" y="272" width="34" height="78" rx="2"/><rect x="176" y="272" width="34" height="78" rx="2"/><rect x="218" y="272" width="34" height="78" rx="2"/></g>
<g fill="#ffd23d"><circle cx="151" cy="286" r="2.6"/><circle cx="151" cy="298" r="2.6" opacity=".5"/><circle cx="151" cy="310" r="2.6"/><circle cx="193" cy="286" r="2.6" opacity=".5"/><circle cx="193" cy="298" r="2.6"/><circle cx="193" cy="310" r="2.6" opacity=".5"/><circle cx="235" cy="286" r="2.6"/><circle cx="235" cy="298" r="2.6"/><circle cx="235" cy="310" r="2.6" opacity=".5"/></g>
<g stroke="#3a4f7e" stroke-width="2"><path d="M138 322H164M138 332H164M180 322H206M180 332H206M222 322H248M222 332H248"/></g>
<rect x="266" y="284" width="30" height="44" rx="3" fill="#22345a" stroke="#ffd23d" stroke-opacity=".7" stroke-width="2"/><rect x="271" y="290" width="20" height="14" rx="2" fill="#0a1222"/><circle cx="281" cy="316" r="3" fill="#ffd23d"/></g>
<g class="dw-stairs" fill="none" stroke-linecap="round"><g stroke="#3a4f7e"><path d="M646 244L712 192" stroke-width="9" stroke-dasharray="3 7"/><path d="M712 354L646 302" stroke-width="9" stroke-dasharray="3 7"/><path d="M646 464L712 412" stroke-width="9" stroke-dasharray="3 7"/></g>
<g stroke="#8ea4cc" stroke-width="2"><path d="M646 232L712 180M712 342L646 290M646 452L712 400"/></g></g>
<g class="dw-smoke"><circle cx="680" cy="268" r="7" fill="#e9eef8"/><circle cx="680" cy="268" r="3" fill="#0f182c"/><circle cx="680" cy="268" r="11" fill="none" stroke="#e9eef8" stroke-opacity=".35" stroke-width="2"/></g>
<g class="dw-door"><rect x="124" y="384" width="104" height="9" rx="2" fill="#2c3f69"/><rect x="140" y="394" width="72" height="74" fill="#0a1222" stroke="#ffd23d" stroke-width="3"/><path d="M176 394V468" stroke="#ffd23d" stroke-opacity=".6" stroke-width="2"/><rect x="146" y="402" width="24" height="56" fill="url(#dwg-glass)" opacity=".55"/><rect x="182" y="402" width="24" height="56" fill="url(#dwg-glass)" opacity=".55"/>
<rect x="218" y="420" width="10" height="24" rx="2" fill="#ffd23d"/><circle cx="223" cy="432" r="2" fill="#111827"/></g>
<g class="dw-teller"><rect x="440" y="426" width="84" height="42" fill="#2c3f69"/><rect x="440" y="394" width="84" height="32" fill="url(#dwg-glass)" opacity=".5" stroke="#7fa6d6" stroke-opacity=".6" stroke-width="2"/>
<rect x="530" y="410" width="28" height="58" rx="3" fill="#0a1222" stroke="#ffd23d" stroke-opacity=".7" stroke-width="2"/><rect x="535" y="416" width="18" height="14" rx="2" fill="#22345a"/><rect x="535" y="436" width="18" height="4" rx="1" fill="#3a4f7e"/>
<circle cx="596" cy="418" r="34" fill="#0f182c" stroke="#3a4f7e" stroke-width="4"/><circle cx="596" cy="418" r="23" fill="none" stroke="#ffd23d" stroke-opacity=".75" stroke-width="2"/><path d="M596 395V441M573 418H619M580 402L612 434M612 402L580 434" stroke="#3a4f7e" stroke-width="2.5"/><circle cx="596" cy="418" r="6" fill="#ffd23d"/></g>
<g class="dw-roof"><rect x="294" y="106" width="74" height="20" rx="3" fill="#2c3f69"/><rect x="304" y="112" width="16" height="8" rx="1" fill="#0a1222"/><path d="M331 106V62" stroke="#c9d4ea" stroke-width="4" stroke-linecap="round"/><path d="M318 78H344M322 90H340" stroke="#c9d4ea" stroke-width="3" stroke-linecap="round"/><circle cx="331" cy="60" r="5" fill="#ffd23d"/>
<g class="dw-wave" fill="none" stroke="#ffd23d" stroke-width="3" stroke-linecap="round"><path d="M313 46a26 26 0 0 1 36 0"/><path d="M303 34a40 40 0 0 1 56 0" opacity=".6"/></g></g>
<path class="dw-link" d="M338 56C470 -4 720 6 846 118" fill="none" stroke="#ffd23d" stroke-opacity=".7" stroke-width="2.5" stroke-dasharray="3 9" stroke-linecap="round"/>
<g class="dw-phone"><rect x="842" y="84" width="64" height="112" rx="13" fill="#0f182c" stroke="#ffd23d" stroke-width="3"/><rect x="849" y="98" width="50" height="84" rx="4" fill="#1d2b4a"/><rect x="862" y="89" width="24" height="4" rx="2" fill="#3a4f7e"/>
<path d="M874 110l17 6v13c0 10-7 16-17 20c-10-4-17-10-17-20v-13z" fill="#ffd23d"/><path d="M866 130l6 6 11-12" fill="none" stroke="#111827" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></g>
<g class="dw-gate"><polygon points="928,320 770,468 934,468" fill="#ffd23d" opacity=".09"/><rect x="738" y="432" width="18" height="38" rx="2" fill="#22345a"/><rect x="742" y="438" width="10" height="14" rx="2" fill="#ffd23d"/>
<rect x="780" y="406" width="20" height="64" rx="2" fill="#2c3f69"/><rect x="780" y="406" width="20" height="6" fill="#ffd23d"/><rect x="800" y="414" width="146" height="9" rx="2" fill="url(#dwg-stripe)"/>
<rect x="826" y="448" width="102" height="22" rx="8" fill="#22345a"/><rect x="846" y="432" width="58" height="20" rx="7" fill="#2c3f69"/><circle cx="850" cy="470" r="8" fill="#0a1222" stroke="#3a4f7e" stroke-width="2"/><circle cx="906" cy="470" r="8" fill="#0a1222" stroke="#3a4f7e" stroke-width="2"/>
<rect x="962" y="318" width="8" height="152" fill="#2c3f69"/><rect x="928" y="308" width="42" height="18" rx="4" fill="#c9d4ea"/><circle cx="928" cy="318" r="6" fill="#0a1222" stroke="#ffd23d" stroke-width="2"/></g>
<g class="dw-zones" fill="#ffd23d" fill-opacity=".09" stroke="#ffd23d" stroke-width="2.5" stroke-dasharray="7 6">
<rect data-z="roof" x="282" y="36" width="98" height="96" rx="10"/><rect data-z="windows" x="126" y="160" width="462" height="74" rx="8"/><rect data-z="door" x="126" y="378" width="112" height="92" rx="8"/><rect data-z="gate" x="726" y="298" width="254" height="174" rx="10"/>
<rect data-z="panel" x="120" y="260" width="180" height="94" rx="8"/><rect data-z="stair" x="638" y="150" width="82" height="316" rx="8"/><rect data-z="teller" x="428" y="372" width="198" height="94" rx="8"/><rect data-z="phone" x="824" y="68" width="104" height="142" rx="12"/></g>
</svg>"""

# hotspot centers inside the 1000 x 560 drawing
_POS = {"roof": (331, 92), "windows": (300, 197), "door": (176, 430), "gate": (850, 440), "panel": (210, 312), "stair": (680, 330), "teller": (528, 392), "phone": (874, 140)}


def _open(s, cls):
    c = "q-section" + (" lf-dark" if s.get("dark") else "") + " " + cls
    return f'<section class="{c}" id="{E(s["id"])}">'


def _chev():
    return '<svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true" focusable="false"><path d="M5 7.5l5 5 5-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def _pcard(p, ctx):
    soon = '<span class="dw-soon">Coming soon</span>' if p.get("soon") else ""
    return (f'<a class="dw-pc" href="{E(ctx["L"](p["href"]))}"><span class="dw-pc-i"><img src="{E(ctx["rel"](_small(p["image"])))}" alt="" width="120" height="90" loading="lazy" decoding="async"></span>'
            f'<span class="dw-pc-t"><b>{E(p["name"])}</b><i>{E(p["kicker"])}</i>{soon}<span>{E(p["fact"])}</span></span>'
            f'<span class="dw-pc-go" aria-hidden="true"><svg viewBox="0 0 20 20" width="18" height="18"><path d="M4 10h11M11 5l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span></a>')


def _building(s, ctx):
    spots = s["spots"]
    n = len(spots)
    hot, lis = [], []
    for i, sp in enumerate(spots):
        x, y = _POS[sp["id"]]
        names = ", ".join(p["name"] for p in sp["products"])
        hot.append(f'<button type="button" class="dw-hs" data-i="{i}" style="left:{x / 10:.2f}%;top:{y / 5.6:.2f}%" aria-pressed="false" aria-label="{E(sp["label"])}: {E(names)}"><i>{i + 1}</i><b>{E(sp["label"])}</b></button>')
        more = f'<a class="dw-more" href="{E(ctx["L"](sp["more"]["href"]))}">{E(sp["more"]["label"])}</a>' if sp.get("more") else ""
        lis.append(f'''<li class="dw-li{" on" if i == 0 else ""}" data-z="{E(sp["id"])}"><button type="button" class="dw-lb" id="dw-b{i}" aria-expanded="{"true" if i == 0 else "false"}" aria-controls="dw-d{i}"><span class="n">{i + 1}</span><span class="t">{E(sp["label"])}</span><span class="c">{_chev()}</span></button>
<div class="dw-det" id="dw-d{i}" role="region" aria-labelledby="dw-b{i}"><h3>{E(sp["title"])}</h3><p class="dw-lede">{E(sp["lede"])}</p><div class="dw-pcs">{"".join(_pcard(p, ctx) for p in sp["products"])}</div>{more}</div></li>''')
    return f'''{_open(s, "dw")} <div class="q-container" data-dw="bld" data-n="{n}">
<div class="dw-hd"><div class="q-eyebrow">{E(s.get("eyebrow"))}</div><h2 class="q-h2">{E(s["heading"])}</h2><p class="q-lead">{E(s.get("intro"))}</p></div>
<div class="dw-grid"><div class="dw-left"><div class="dw-stage">{_SVG}<div class="dw-hsl">{"".join(hot)}</div></div>
<div class="dw-tour"><button type="button" class="dw-tbtn pp-btn gold" aria-pressed="false"><svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M6 4l10 6-10 6z" fill="currentColor"/></svg><span>Take the guided tour</span></button>
<p class="dw-tstat" aria-live="polite"><span class="dw-tn">Stop 1 of {n}</span> <span class="dw-tl">{E(spots[0]["label"])}</span></p><span class="dw-prog" aria-hidden="true"><i></i></span></div></div>
<ol class="dw-list" aria-label="Places in the building">{"".join(lis)}</ol></div>
<p class="dw-note">{E(s.get("note", ""))}</p></div></section>'''


# ============================================================================================ anatomy

def _anatomy(s, ctx):
    items = s["items"]
    half = (len(items) + 1) // 2
    def co(it):
        return (f'<li class="dw-co" data-k="{it["n"] - 1}"><span class="dw-cn">{it["n"]}</span><div><h3>{E(it["title"])}</h3><p>{E(it["text"])}</p></div></li>')
    left = "".join(co(it) for it in items[:half])
    right = "".join(co(it) for it in items[half:])
    img = s["image"]
    return f'''{_open(s, "dw-an")} <div class="q-container"><div class="dw-hd"><div class="q-eyebrow">{E(s.get("eyebrow", "Anatomy"))}</div><h2 class="q-h2">{E(s["heading"])}</h2></div>
<div class="dw-an-fig" data-dw="an"><div class="dw-an-c"><div class="dw-an-frame"><img src="{E(ctx["rel"](img))}"{ctx["srcset"](img)} alt="{E(s.get("image_alt", ""))}" width="{s.get("image_w", 1200)}" height="{s.get("image_h", 800)}" loading="lazy" decoding="async"><i class="k a"></i><i class="k b"></i><i class="k c"></i><i class="k d"></i></div></div>
<ol class="dw-an-l" start="1">{left}</ol><ol class="dw-an-r" start="{half + 1}">{right}</ol><svg class="dw-an-ln" aria-hidden="true" focusable="false"></svg></div>
<p class="dw-note">{E(s.get("note", ""))}</p></div></section>'''


RENDER_DW1 = {"dwbuilding": _building, "dwanatomy": _anatomy}


# ============================================================================================ mega menus

def _tel(n: str) -> str:
    return "tel:+1" + re.sub(r"\D", "", n)


def mega_panel(it, ctx):
    """Return (panel_html, mobile_links_html, panel_id) for a nav item that carries dw_mega, else None."""
    m = it.get("dw_mega")
    if not m:
        return None
    L, rel = ctx["L"], ctx["rel"]
    kind = m["kind"]
    pid = f"dw-m-{kind}"
    foot = "".join(f'<a href="{E(L(h))}">{E(l)}<svg viewBox="0 0 20 20" width="16" height="16" aria-hidden="true"><path d="M4 10h11M11 5l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>' for l, h in m.get("foot", []))
    if kind == "products":
        tiles = "".join(f'<li><a class="dw-mt" href="{E(L(h))}"><span class="dw-mt-i"><img src="{E(rel(_small(img)))}" alt="" width="120" height="90" loading="lazy" decoding="async"></span><span class="dw-mt-t"><b>{E(l)}</b><span>{E(p)}</span></span></a></li>' for l, p, h, img in m["tiles"])
        f = m["featured"]
        inner = (f'<div class="dw-m-main"><p class="dw-m-k">Eight systems, one manufacturer</p><ul class="dw-m-tiles">{tiles}</ul></div>'
                 f'<a class="dw-m-feat" href="{E(L(f["href"]))}"><span class="dw-m-fi"><img src="{E(rel(_small(f["image"])))}" alt="" width="360" height="260" loading="lazy" decoding="async"></span><span class="dw-m-fk">{E(f["eyebrow"])}</span><b>{E(f["name"])}</b><span class="dw-m-fb">{E(f["body"])}</span><span class="dw-m-fl">{E(f["label"])}</span></a>')
        mob = "".join(f'<a class="dw-ma" href="{E(L(h))}"><img class="dw-mth" src="{E(rel(_small(img)))}" alt="" width="44" height="44" loading="lazy"><span>{E(l)}</span></a>' for l, p, h, img in m["tiles"])
    elif kind == "industries":
        chips = "".join(f'<li><a class="dw-ic" href="{E(L(h))}"><img src="{E(rel(_small(img)))}" alt="" width="260" height="160" loading="lazy" decoding="async"><b>{E(l)}</b></a></li>' for l, h, img in m["chips"])
        inner = (f'<div class="dw-m-main dw-m-wide"><p class="dw-m-k">Eleven kinds of building</p><ul class="dw-m-chips">{chips}<li><a class="dw-ic dw-ic-all" href="{E(L(it["href"]))}"><b>See all industries</b><svg viewBox="0 0 20 20" width="22" height="22" aria-hidden="true"><path d="M4 10h11M11 5l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></a></li></ul></div>')
        mob = "".join(f'<a class="dw-ma" href="{E(L(h))}"><img class="dw-mth" src="{E(rel(_small(img)))}" alt="" width="44" height="44" loading="lazy"><span>{E(l)}</span></a>' for l, h, img in m["chips"])
    else:
        cols = "".join(f'<li class="dw-sl"><span class="dw-sl-k">{E(x["label"])}</span><a class="dw-sl-n" href="{E(_tel(x["number"]))}">{E(x["number"])}</a><span class="dw-sl-h">{E(x["hours"])}</span><span class="dw-sl-t">{E(x["text"])}</span></li>' for x in m["lines"])
        links = "".join(f'<a href="{E(L(h))}">{E(l)}</a>' for l, h in m["links"])
        inner = f'<div class="dw-m-main dw-m-wide"><p class="dw-m-k">Four lines, one phone call away</p><ul class="dw-m-lines">{cols}</ul><div class="dw-m-links" aria-label="Support pages">{links}</div></div>'
        mob = ("".join(f'<a class="dw-ma dw-ma-tel" href="{E(_tel(x["number"]))}"><b>{E(x["number"])}</b><span>{E(x["label"])}, {E(x["hours"])}</span></a>' for x in m["lines"])
               + "".join(f'<a href="{E(L(h))}">{E(l)}</a>' for l, h in m["links"]))
    panel = f'<div class="dw-mega dw-m-{kind}" id="{pid}" aria-label="{E(it["label"])} menu"><div class="dw-m-in">{inner}</div><div class="dw-m-foot">{foot}</div></div>'
    return panel, mob, pid


# ============================================================================================ CSS

DW1_CSS = r"""
/* ===== dw1 (preview_dw1.py): building cutaway, anatomy, mega menus, global polish ===== */
.dw-hd{text-align:center;max-width:820px;margin:0 auto clamp(30px,4vw,54px)}
.dw-hd .q-h2{margin:20px 0 0;color:#fff}.dw-hd .q-lead{margin:16px auto 0;max-width:640px;color:var(--fg-muted)}
.dw{padding:clamp(64px,8vw,112px) 0}
.dw-grid{display:grid;grid-template-columns:minmax(0,1.42fr) minmax(0,1fr);gap:clamp(22px,3vw,48px);align-items:start}
.dw-stage{position:relative;border-radius:calc(var(--radius,14px) + 12px);overflow:hidden;border:1px solid rgba(255,255,255,.16);background:radial-gradient(120% 90% at 78% 8%,#1b2c52 0,#0f1a31 55%,#0a1222 100%);box-shadow:0 50px 90px -50px rgba(0,0,0,.95),inset 0 1px 0 rgba(255,255,255,.08)}
.dw-svg{display:block;width:100%;height:auto}
.dw-zones rect{opacity:0;transition:opacity .35s}
.dw[data-act=roof] [data-z=roof],.dw[data-act=windows] [data-z=windows],.dw[data-act=door] [data-z=door],.dw[data-act=gate] [data-z=gate],.dw[data-act=panel] [data-z=panel],.dw[data-act=stair] [data-z=stair],.dw[data-act=teller] [data-z=teller],.dw[data-act=phone] [data-z=phone]{opacity:1;animation:dw-dash 1.4s linear infinite}
@keyframes dw-dash{to{stroke-dashoffset:-26}}
.dw-wave path{animation:dw-wave 2.4s ease-in-out infinite}.dw-wave path+path{animation-delay:.5s}
@keyframes dw-wave{0%,100%{opacity:.25}50%{opacity:1}}
.dw-link{animation:dw-dash 2.2s linear infinite}
.dw-smoke circle:last-child{animation:dw-wave 2s ease-in-out infinite}
.dw-hsl{position:absolute;inset:0}
.dw-hs{position:absolute;width:48px;height:48px;margin:-24px 0 0 -24px;padding:0;border:0;background:none;border-radius:50%;cursor:pointer;z-index:2;font-family:inherit}
.dw-hs i{position:absolute;left:50%;top:50%;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;background:var(--q-gold);color:#111;font:800 14px/30px var(--q-sans,system-ui);font-style:normal;text-align:center;box-shadow:0 0 0 4px rgba(255,210,61,.28),0 0 26px rgba(255,210,61,.75);transition:transform .25s cubic-bezier(.2,.7,.2,1),background .25s}
.dw-hs::before{content:"";position:absolute;inset:3px;border-radius:50%;border:2px solid var(--q-gold);opacity:0;animation:dw-ping 2.6s ease-out infinite}
@keyframes dw-ping{0%{transform:scale(.55);opacity:.9}100%{transform:scale(1.35);opacity:0}}
.dw-hs:hover i,.dw-hs.on i{transform:scale(1.18)}
.dw-hs.on i{background:#fff;box-shadow:0 0 0 4px rgba(255,210,61,.9),0 0 34px rgba(255,210,61,.9)}
.dw-hs b{position:absolute;left:50%;bottom:calc(100% - 2px);transform:translate(-50%,4px);white-space:nowrap;padding:7px 13px;border-radius:999px;background:#fff;color:#111;font:700 13px/1 var(--q-sans,system-ui);letter-spacing:.01em;box-shadow:0 10px 24px -8px rgba(0,0,0,.6);opacity:0;pointer-events:none;transition:opacity .2s,transform .2s}
.dw-hs:hover b,.dw-hs:focus-visible b,.dw-hs.on b{opacity:1;transform:translate(-50%,0)}
.dw-hs:focus-visible{outline:3px solid #fff;outline-offset:0;box-shadow:none}
.dw-tour{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-top:20px;position:relative}
.dw-tstat{margin:0;font-size:15px;color:var(--fg-muted)}.dw-tn{font-weight:700;color:#fff;letter-spacing:.02em}
.dw-prog{position:absolute;left:0;right:0;bottom:-12px;height:2px;border-radius:2px;background:rgba(255,255,255,.12);overflow:hidden;opacity:0;transition:opacity .3s}
.dw-prog i{display:block;height:100%;width:100%;background:var(--q-gold);transform:scaleX(0);transform-origin:left}
.dw.touring .dw-prog{opacity:1}.dw.touring .dw-prog i{animation:dw-prog var(--dw-step,5.5s) linear forwards}
@keyframes dw-prog{to{transform:scaleX(1)}}
.dw-list{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.dw-li{display:contents}
.dw-lb{display:flex;align-items:center;gap:12px;min-height:48px;padding:6px 14px 6px 8px;border-radius:14px;border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.04);color:#fff;font:600 15px/1.2 var(--q-sans,system-ui);cursor:pointer;text-align:left;transition:background .25s,border-color .25s,transform .2s}
.dw-lb .n{flex:none;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;background:rgba(255,210,61,.16);color:var(--q-gold);font-weight:800;font-size:14px;transition:background .25s,color .25s}
.dw-lb .t{flex:1;min-width:0}.dw-lb .c{display:none}
.dw-lb:hover{border-color:rgba(255,210,61,.6);background:rgba(255,255,255,.08)}
.dw-lb:active{transform:scale(.98)}
.dw-li.on .dw-lb{border-color:var(--q-gold);background:rgba(255,210,61,.12)}.dw-li.on .dw-lb .n{background:var(--q-gold);color:#111}
.dw-det{grid-column:1/-1;grid-row:5;margin-top:6px;padding:22px 22px 20px;border-radius:calc(var(--radius,14px) + 8px);background:linear-gradient(180deg,rgba(255,255,255,.09),rgba(255,255,255,.03));border:1px solid rgba(255,255,255,.16);position:relative;overflow:hidden}
.dw-det::before{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,var(--q-gold),transparent)}
.dw-det h3{margin:0;font-size:clamp(20px,1.8vw,24px);letter-spacing:-.02em;color:#fff}
.dw-lede{margin:8px 0 16px;color:var(--fg-muted);font-size:15.5px;line-height:1.5}
.dw-pcs{display:grid;gap:10px}
.dw-pc{display:grid;grid-template-columns:76px minmax(0,1fr) auto;gap:14px;align-items:center;padding:10px 14px 10px 10px;border-radius:16px;background:rgba(7,12,24,.55);border:1px solid rgba(255,255,255,.12);text-decoration:none;color:#fff;transition:transform .3s cubic-bezier(.2,.7,.2,1),border-color .3s,background .3s}
.dw-pc:hover{transform:translateX(4px);border-color:rgba(255,210,61,.7);background:rgba(7,12,24,.8)}
.dw-pc:active{transform:translateX(2px) scale(.99)}
.dw-pc-i{width:76px;height:64px;border-radius:12px;display:grid;place-items:center;background:radial-gradient(circle at 50% 40%,rgba(255,255,255,.2),rgba(255,255,255,.04) 75%)}
.dw-pc-i{position:relative}.dw-pc-i img{position:absolute;inset:0;margin:auto;max-width:88%;max-height:88%;width:auto;height:auto;object-fit:contain;filter:drop-shadow(0 8px 8px rgba(0,0,0,.45))}
.dw-pc-t{display:flex;flex-direction:column;gap:2px;min-width:0}.dw-pc-t b{font-size:16.5px;line-height:1.2}
.dw-pc-t i{font-style:normal;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--q-gold);font-weight:700}
.dw-pc-t span:last-child{font-size:14px;line-height:1.4;color:var(--fg-muted)}
.dw-soon{align-self:flex-start;font-size:13px;font-weight:700;color:#111;background:var(--q-gold);border-radius:999px;padding:2px 9px}
.dw-pc-go{color:var(--q-gold);transition:transform .3s}.dw-pc:hover .dw-pc-go{transform:translateX(3px)}
.dw-more{display:inline-flex;align-items:center;min-height:44px;margin-top:10px;color:var(--q-gold);font-weight:700;font-size:15px}
.dw-note{text-align:center;margin:28px 0 0;font-size:14px;color:var(--fg-muted)}
.dw.dw-on .dw-det{opacity:0;visibility:hidden;pointer-events:none;transition:opacity .3s,visibility 0s .3s}
.dw.dw-on .dw-li.on .dw-det{opacity:1;visibility:visible;pointer-events:auto;transition:opacity .35s .05s}
@media(max-width:1024px){.dw-grid{grid-template-columns:minmax(0,1fr)}.dw-list{grid-template-columns:repeat(4,minmax(0,1fr))}.dw-lb .t{font-size:14px}}
@media(max-width:767px){
  .dw-hsl{display:none}
  .dw-list{display:block}.dw-li{display:block;margin-bottom:8px}
  .dw-lb{width:100%}.dw-lb .c{display:block;transition:transform .3s}.dw-li.on .dw-lb .c{transform:rotate(180deg)}
  .dw-det{margin-top:6px}.dw.dw-on .dw-det{display:none;opacity:1;visibility:visible;pointer-events:auto}.dw.dw-on .dw-li.on .dw-det{display:block}
  .dw-pc{grid-template-columns:64px minmax(0,1fr) auto}.dw-pc-i{width:64px;height:56px}
  .dw-stage{border-radius:18px}.dw-tour{margin:16px 0}
}
@media(max-width:480px){.dw-pc-go{display:none}.dw-pc{grid-template-columns:64px minmax(0,1fr)}}
@media(prefers-reduced-motion:reduce){.dw-wave path,.dw-link,.dw-smoke circle:last-child,.dw-hs::before,.dw-zones rect,.dw-prog i{animation:none!important}.dw-hs::before{opacity:.5}.dw-det,.dw-hs i,.dw-hs b{transition:none!important}}

/* anatomy */
.dw-an{padding:clamp(64px,8vw,112px) 0}
.dw-an-fig{position:relative;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr) minmax(0,1fr);grid-template-areas:"l c r";gap:clamp(24px,5vw,84px);align-items:center}
.dw-an-c{grid-area:c}.dw-an-l{grid-area:l}.dw-an-r{grid-area:r}
.dw-an-l,.dw-an-r{list-style:none;margin:0;padding:0;display:grid;gap:clamp(14px,2vw,28px);position:relative;z-index:1}
.dw-an-frame{position:relative;aspect-ratio:4/3;display:grid;place-items:center;border-radius:calc(var(--radius,14px) + 10px);background:radial-gradient(70% 65% at 50% 46%,rgba(255,210,61,.22),rgba(255,255,255,.03) 70%);border:1px solid rgba(255,255,255,.14);box-shadow:inset 0 0 0 1px rgba(255,255,255,.04),0 40px 80px -50px rgba(0,0,0,.9)}
.dw-an-frame img{grid-area:1/1;max-width:84%;max-height:82%;width:auto;height:auto;object-fit:contain;filter:drop-shadow(0 30px 28px rgba(0,0,0,.55));transition:transform .8s cubic-bezier(.2,.7,.2,1)}
.dw-an-fig:hover .dw-an-frame img{transform:scale(1.03)}
.dw-an-frame .k{position:absolute;width:26px;height:26px;border:3px solid var(--q-gold);pointer-events:none}
.dw-an-frame .a{left:-1px;top:-1px;border-right:0;border-bottom:0;border-top-left-radius:inherit}.dw-an-frame .b{right:-1px;top:-1px;border-left:0;border-bottom:0;border-top-right-radius:inherit}
.dw-an-frame .c{left:-1px;bottom:-1px;border-right:0;border-top:0;border-bottom-left-radius:inherit}.dw-an-frame .d{right:-1px;bottom:-1px;border-left:0;border-top:0;border-bottom-right-radius:inherit}
.dw-co{display:grid;grid-template-columns:34px minmax(0,1fr);gap:14px;padding:16px 18px;border-radius:16px;background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.03));border:1px solid rgba(255,255,255,.14);transition:border-color .3s,transform .3s,background .3s}
.dw-co.hot{border-color:var(--q-gold);transform:translateY(-3px);background:rgba(255,210,61,.1)}
.dw-cn{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:var(--q-gold);color:#111;font:800 15px var(--q-sans,system-ui)}
.dw-co h3{margin:2px 0 4px;font-size:17px;line-height:1.25;color:#fff;letter-spacing:-.01em}.dw-co p{margin:0;font-size:14.5px;line-height:1.5;color:var(--fg-muted)}
.dw-an-ln{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible;z-index:0}
.dw-an-ln path{fill:none;stroke:rgba(255,210,61,.5);stroke-width:1.5;transition:stroke .3s,stroke-width .3s}
.dw-an-ln .hot{stroke:var(--q-gold);stroke-width:2.5}
.dw-an-ln circle{fill:var(--q-gold)}.dw-an-ln text{fill:#111;font:800 13px var(--q-sans,system-ui);text-anchor:middle;dominant-baseline:central}
@media(max-width:1000px){.dw-an-fig{grid-template-columns:minmax(0,1fr) minmax(0,1fr);grid-template-areas:"c c" "l r"}.dw-an-ln{display:none}.dw-an-frame{max-width:560px;margin:0 auto;width:100%}}
@media(max-width:640px){.dw-an-fig{grid-template-columns:minmax(0,1fr);grid-template-areas:"c" "l" "r";gap:14px}}

/* mega menus (desktop only; the phone menu is the accordion below) */
@media(min-width:1025px){
.q-header .q-nav-item[data-dwm]{position:static}
.q-header .dw-mega{position:absolute;left:50%;top:100%;width:min(1180px,calc(100vw - 32px));max-height:calc(100vh - 120px);overflow:auto;transform:translate(-50%,10px);opacity:0;visibility:hidden;pointer-events:none;border-radius:0 0 26px 26px;border:1px solid rgba(255,255,255,.14);border-top:3px solid var(--q-gold);color:#fff;
  background:radial-gradient(700px 320px at 92% -10%,rgba(255,210,61,.15),transparent 62%),radial-gradient(600px 300px at 0% 110%,rgba(80,120,255,.16),transparent 60%),linear-gradient(170deg,#142040,#0a1222 70%);box-shadow:0 50px 90px -30px rgba(0,0,0,.7);transition:opacity .22s ease,transform .26s cubic-bezier(.2,.7,.2,1),visibility 0s .26s;z-index:90;--fg:#f4f6fb;--fg-muted:#b7c0d3}
.q-header .q-nav-item.dw-open>.dw-mega,html:not(.dw-js) .q-header .q-nav-item[data-dwm]:hover>.dw-mega,html:not(.dw-js) .q-header .q-nav-item[data-dwm]:focus-within>.dw-mega{opacity:1;visibility:visible;pointer-events:auto;transform:translate(-50%,0);transition:opacity .22s ease,transform .26s cubic-bezier(.2,.7,.2,1),visibility 0s}
.q-header .q-nav-item[data-dwm]>a .q-caret{transition:transform .25s}.q-header .q-nav-item.dw-open>a .q-caret{transform:rotate(225deg) translate(-2px,-1px)}
.dw-m-in{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:0}
.dw-m-main{padding:26px 28px 22px}.dw-m-main.dw-m-wide{grid-column:1/-1;padding:26px 32px 22px}
.dw-m-industries .dw-m-in,.dw-m-support .dw-m-in{grid-template-columns:minmax(0,1fr)}
.dw-m-k{margin:0 0 16px;font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--q-gold)}
.dw-m-tiles{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.dw-mt{display:flex;flex-direction:column;gap:10px;height:100%;padding:12px;border-radius:16px;border:1px solid transparent;background:rgba(255,255,255,.04);text-decoration:none;color:#fff;transition:background .25s,border-color .25s,transform .3s cubic-bezier(.2,.7,.2,1)}
.q-header .q-nav a.dw-mt,.q-header .q-nav a.dw-ic,.q-header .q-nav a.dw-m-feat{padding:12px;color:#fff;display:flex}
.dw-mt:hover,.dw-mt:focus-visible{background:rgba(255,255,255,.1);border-color:rgba(255,210,61,.6);transform:translateY(-3px)}
.dw-mt-i{display:grid;place-items:center;height:78px;border-radius:12px;background:radial-gradient(circle at 50% 40%,rgba(255,255,255,.18),rgba(255,255,255,.03) 75%)}
.dw-mt-i{position:relative}.dw-mt-i img{position:absolute;inset:0;margin:auto;max-width:80%;max-height:84%;width:auto;height:auto;object-fit:contain;filter:drop-shadow(0 8px 8px rgba(0,0,0,.45));transition:transform .5s cubic-bezier(.2,.7,.2,1)}.dw-mt:hover .dw-mt-i img{transform:scale(1.1)}
.dw-mt-t{display:flex;flex-direction:column;gap:4px}.dw-mt-t b{font-size:16px;line-height:1.2;letter-spacing:-.01em;white-space:normal}
.dw-mt-t span{font-size:13px;line-height:1.4;color:var(--fg-muted);white-space:normal;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.q-header .q-nav a.dw-m-feat{flex-direction:column;gap:6px;border-left:1px solid rgba(255,255,255,.12);padding:26px 26px 22px;white-space:normal;background:linear-gradient(180deg,rgba(255,210,61,.1),rgba(255,210,61,.02));text-decoration:none;transition:background .3s}
.dw-m-feat:hover,.dw-m-feat:focus-visible{background:linear-gradient(180deg,rgba(255,210,61,.18),rgba(255,210,61,.05))}
.dw-m-fi{display:grid;place-items:center;height:150px;margin:0 -6px 6px;background:radial-gradient(circle at 50% 45%,rgba(255,210,61,.28),transparent 68%)}
.dw-m-fi{position:relative}.dw-m-fi img{position:absolute;inset:0;margin:auto;max-width:84%;max-height:100%;width:auto;height:auto;object-fit:contain;filter:drop-shadow(0 18px 18px rgba(0,0,0,.5));transition:transform .6s cubic-bezier(.2,.7,.2,1)}.dw-m-feat:hover .dw-m-fi img{transform:scale(1.07) rotate(-1.5deg)}
.dw-m-fk{font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--q-gold)}.dw-m-feat b{font-size:22px;line-height:1.15;letter-spacing:-.02em}
.dw-m-fb{font-size:14.5px;line-height:1.5;color:var(--fg-muted)}.dw-m-fl{margin-top:auto;font-weight:700;color:var(--q-gold);font-size:15px;padding-top:8px}
.dw-m-chips{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.dw-ic{position:relative;display:block;aspect-ratio:16/7;border-radius:16px;overflow:hidden;background:#0a1222;border:1px solid rgba(255,255,255,.14);text-decoration:none;color:#fff;transition:transform .35s cubic-bezier(.2,.7,.2,1),border-color .3s,box-shadow .3s}
.q-header .q-nav a.dw-ic{padding:0;display:block}
.dw-ic img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .7s cubic-bezier(.2,.7,.2,1)}
.dw-ic::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,13,26,0) 30%,rgba(8,13,26,.9))}
.dw-ic b{position:absolute;left:14px;right:14px;bottom:11px;z-index:1;font-size:15.5px;line-height:1.2;letter-spacing:-.01em;white-space:normal;text-shadow:0 2px 12px rgba(0,0,0,.6)}
.dw-ic:hover,.dw-ic:focus-visible{transform:translateY(-4px);border-color:var(--q-gold);box-shadow:0 22px 34px -22px rgba(0,0,0,.9),0 0 0 1px rgba(255,210,61,.4)}.dw-ic:hover img{transform:scale(1.08)}
.dw-ic-all{display:flex!important;align-items:center;justify-content:center;gap:10px;background:var(--q-gold);color:#111;border-color:var(--q-gold)}.dw-ic-all::after{display:none}
.dw-ic-all b{position:static;text-shadow:none;font-size:16px;color:#111;flex:none}
.q-header .q-nav a.dw-ic-all{color:#111}
.dw-m-lines{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.dw-sl{display:flex;flex-direction:column;gap:6px;padding:20px 20px 18px;border-radius:18px;background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.02));border:1px solid rgba(255,255,255,.14)}
.dw-sl-k{font-size:13px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--q-gold);line-height:1.35}
.q-header .q-nav a.dw-sl-n{display:inline-block;padding:2px 0;font-size:25px;font-weight:800;letter-spacing:-.02em;color:#fff;line-height:1.2;white-space:nowrap;min-height:44px}.dw-sl-n:hover{color:var(--q-gold)}
.dw-sl-h{font-size:14px;font-weight:600;color:#fff}.dw-sl-t{font-size:14px;line-height:1.5;color:var(--fg-muted)}
.dw-m-links{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.q-header .q-nav .dw-m-links a{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border-radius:999px;border:1px solid rgba(255,255,255,.22);color:#fff;font-size:15px;white-space:nowrap;transition:background .25s,border-color .25s}
.q-header .q-nav .dw-m-links a:hover,.q-header .q-nav .dw-m-links a:focus-visible{background:rgba(255,210,61,.14);border-color:var(--q-gold);color:#fff}
.dw-m-foot{display:flex;gap:26px;flex-wrap:wrap;padding:6px 32px;border-top:1px solid rgba(255,255,255,.12);background:rgba(0,0,0,.22)}
.q-header .q-nav .dw-m-foot a{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0;color:var(--q-gold);font-weight:700;font-size:15px;white-space:nowrap}.q-header .q-nav .dw-m-foot a:hover{color:#fff}
.q-header .q-nav .dw-m-foot svg{transition:transform .3s}.q-header .q-nav .dw-m-foot a:hover svg{transform:translateX(4px)}
.dw-scrim{position:fixed;left:0;right:0;bottom:0;top:var(--dw-scrim,90px);z-index:55;background:rgba(5,8,15,.5);opacity:0;visibility:hidden;transition:opacity .25s,visibility 0s .25s;-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px)}
.dw-scrim.on{opacity:1;visibility:visible;transition:opacity .25s}
.q-header .q-nav .dw-mega a:focus-visible{outline:3px solid var(--q-gold);outline-offset:-3px;box-shadow:none}
}
@media(max-width:1100px) and (min-width:1025px){.dw-m-in{grid-template-columns:minmax(0,1fr) 240px}.dw-m-tiles{grid-template-columns:repeat(4,minmax(0,1fr))}.dw-mt-t span{-webkit-line-clamp:2}.dw-sl-n{font-size:21px!important}}
@media(max-width:1024px){.dw-mega,.dw-scrim{display:none!important}}
/* phone accordion with thumbnails */
.dw-ma{display:flex!important;align-items:center;gap:14px;min-height:56px}
.dw-mth{flex:none;width:44px;height:44px;border-radius:10px;object-fit:cover;background:rgba(127,127,127,.14)}
.dw-ma-tel{flex-direction:column;align-items:flex-start!important;justify-content:center;gap:2px}.dw-ma-tel b{font-size:19px;letter-spacing:-.01em}.dw-ma-tel span{font-size:13.5px;opacity:.8;line-height:1.35}
.q-msub-links .dw-ma img[src*="-cut"]{object-fit:contain;padding:3px;background:rgba(127,127,127,.14)}

/* header that condenses without moving the page: the box keeps its height, only the painted bar and its contents shrink */
.q-header.dw-fix{position:sticky;top:0;background:transparent!important;border-bottom:0!important;box-shadow:none!important;pointer-events:none;height:var(--dw-h0);z-index:70;-webkit-backdrop-filter:none!important;backdrop-filter:none!important}
.q-header.dw-fix::before{content:"";position:absolute;left:0;right:0;top:0;height:var(--dw-h0);background:var(--chrome-bg);border-bottom:1px solid var(--chrome-border);transition:height .32s cubic-bezier(.2,.7,.2,1),background-color .32s,box-shadow .32s;z-index:0;pointer-events:none}
.q-header.dw-fix .pv-util,.q-header.dw-fix .q-header-in{pointer-events:auto}
.q-header.dw-fix .pv-util{position:relative;z-index:1;height:var(--dw-u);overflow:hidden;transition:height .32s cubic-bezier(.2,.7,.2,1),opacity .2s}
.q-header.dw-fix .q-header-in{z-index:1;transition:height .32s cubic-bezier(.2,.7,.2,1)}
.q-header.dw-fix .q-header-logo img{transition:height .32s cubic-bezier(.2,.7,.2,1),width .32s}
.q-header.dw-fix .q-nav>a,.q-header.dw-fix .q-nav-item>a{transition:padding .32s cubic-bezier(.2,.7,.2,1)}
.q-header.dw-cond::before{height:var(--dw-h1);background:color-mix(in srgb,var(--chrome-bg) 84%,transparent);-webkit-backdrop-filter:blur(16px) saturate(1.5);backdrop-filter:blur(16px) saturate(1.5);box-shadow:0 12px 34px -20px rgba(0,0,0,.5)}
.q-header.dw-cond .pv-util{height:0;opacity:0}
.q-header.dw-cond .q-header-in{height:var(--dw-hin1)}
.q-header.dw-cond .q-header-logo img{height:30px;width:auto}
.q-header.dw-cond .q-nav>a,.q-header.dw-cond .q-nav-item>a{padding-top:20px;padding-bottom:20px}
.q-header.dw-cond .q-nav>a[aria-current]::after,.q-header.dw-cond .q-nav-item>a[aria-current]::after{bottom:14px}
.q-header.dw-fix .q-mnav-panel{max-height:calc(100vh - var(--dw-h1,64px))}

/* dark stage texture: grain and a slow mesh, plus the cursor spotlight (all injected as one aria-hidden element) */
.pv-dark,.dw-stagefx{position:relative;isolation:isolate}
.dw-fx{position:absolute;inset:0;z-index:-1;overflow:hidden;pointer-events:none}
.dw-fx-mesh{position:absolute;inset:-18%;background:radial-gradient(38% 46% at 18% 28%,rgba(255,210,61,.11),transparent 70%),radial-gradient(42% 52% at 82% 18%,rgba(74,118,255,.15),transparent 70%),radial-gradient(46% 56% at 62% 92%,rgba(255,210,61,.08),transparent 70%);animation:dw-mesh 26s ease-in-out infinite alternate;animation-play-state:paused;will-change:transform}
.dw-fx.vis .dw-fx-mesh{animation-play-state:running}
@keyframes dw-mesh{0%{transform:translate3d(-2%,1%,0) rotate(0deg) scale(1)}100%{transform:translate3d(3%,-3%,0) rotate(5deg) scale(1.1)}}
.dw-fx-grain{position:absolute;inset:0;opacity:.07;mix-blend-mode:overlay;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .6 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");background-size:160px 160px}
.dw-fx-spot{position:absolute;inset:0;opacity:0;transition:opacity .45s;background:radial-gradient(420px circle at var(--dw-x,50%) var(--dw-y,50%),rgba(255,226,122,.16),rgba(255,210,61,.05) 40%,transparent 70%)}
.dw-fx.hov .dw-fx-spot{opacity:1}
@media(prefers-reduced-motion:reduce){.dw-fx-mesh{animation:none}.dw-fx-spot{display:none}}

/* page-to-page View Transitions, same-origin only; the header, switcher and sticky bars hold still */
@media(prefers-reduced-motion:no-preference){
@view-transition{navigation:auto}
::view-transition-old(root){animation:dw-vo .16s ease-out both}
::view-transition-new(root){animation:dw-vn .3s cubic-bezier(.2,.7,.2,1) both}
.q-header{view-transition-name:dw-hd}.pv-switch{view-transition-name:dw-sw}.pv-sticky{view-transition-name:dw-st}
::view-transition-group(dw-hd){animation-duration:.3s}
@keyframes dw-vo{to{opacity:0}}@keyframes dw-vn{from{opacity:0;transform:translateY(8px)}}
}

/* micro-interactions: a two-tone focus ring in the brand yellow, pressed states, steady transitions */
:where(a,button,summary,input,select,textarea,[tabindex]):focus-visible{outline:3px solid var(--q-gold,#ffd23d);outline-offset:3px;box-shadow:0 0 0 3px #111}
.lf-dark :where(a,button,summary,input,select,textarea,[tabindex]):focus-visible,.pv-dark :where(a,button,summary,input,select,textarea,[tabindex]):focus-visible{box-shadow:0 0 0 3px rgba(0,0,0,.55)}
.q-btn,.q-btn-ghost,.pp-btn,.hs-button,.q-booknow,.q-mnav-cta,.pv-sbtn{transition:transform .25s cubic-bezier(.2,.7,.2,1),box-shadow .25s,background-color .25s,color .25s,border-color .25s,filter .25s}
.q-btn:hover,.hs-button:hover,.q-booknow:hover{transform:translateY(-2px)}
.q-btn:active,.q-btn-ghost:active,.pp-btn:active,.hs-button:active,.q-booknow:active,.q-mnav-cta:active,.pv-sbtn:active,.mo-chip:active,.pp-chip:active{transform:translateY(1px) scale(.97)!important;transition-duration:.08s;filter:brightness(.95)}
a.q-card:active,.pv-post:active,.pv-res a:active,.lf-spec-c:active{transform:translateY(-1px) scale(.992)!important;transition-duration:.08s}
@media(prefers-reduced-motion:reduce){.q-btn,.pp-btn,.hs-button,.q-booknow{transition:none}.q-btn:hover,.hs-button:hover,.q-booknow:hover{transform:none}.q-btn:active,.pp-btn:active,.hs-button:active{transform:none!important}}
"""

# ============================================================================================ JS

DW1_JS = r"""
(function(){
var d=document,de=d.documentElement,R=function(q,c){return [].slice.call((c||d).querySelectorAll(q))};
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
de.classList.add('dw-js');

/* ---- building cutaway ---- */
R('[data-dw=bld]').forEach(function(root){
var sec=root.closest('.dw')||root,hs=R('.dw-hs',root),bs=R('.dw-lb',root),lis=R('.dw-li',root),n=lis.length,ids=lis.map(function(l){return l.getAttribute('data-z')}),
tbtn=root.querySelector('.dw-tbtn'),tn=root.querySelector('.dw-tn'),tl=root.querySelector('.dw-tl'),cur=-1,timer=0,hov=0,STEP=5500;
sec.classList.add('dw-on');sec.style.setProperty('--dw-step',STEP+'ms');
function act(i){if(i===cur)return;cur=i;lis.forEach(function(l,k){l.classList.toggle('on',k===i)});
hs.forEach(function(h,k){h.classList.toggle('on',k===i);h.setAttribute('aria-pressed',k===i?'true':'false')});
bs.forEach(function(b,k){b.setAttribute('aria-expanded',k===i?'true':'false')});
sec.setAttribute('data-act',ids[i]);tn.textContent='Stop '+(i+1)+' of '+n;tl.textContent=bs[i].querySelector('.t').textContent;
if(timer){var p=sec.querySelector('.dw-prog i');if(p){p.style.animation='none';void p.offsetWidth;p.style.animation=''}}}
function stop(){if(timer){clearInterval(timer);timer=0}sec.classList.remove('touring');tbtn.setAttribute('aria-pressed','false');tbtn.querySelector('span').textContent='Take the guided tour';tbtn.querySelector('svg').innerHTML='<path d="M6 4l10 6-10 6z" fill="currentColor"/>'}
function step(){act((cur+1)%n)}
function start(){stop();timer=setInterval(step,STEP);sec.classList.add('touring');tbtn.setAttribute('aria-pressed','true');tbtn.querySelector('span').textContent='Pause the tour';tbtn.querySelector('svg').innerHTML='<path d="M5 4h3.5v12H5zM11.5 4H15v12h-3.5z" fill="currentColor"/>';var f=cur<0||cur===n-1?0:cur+1;if(f===cur){}else{act(f)}}
tbtn.addEventListener('click',function(){timer?stop():start()});
hs.forEach(function(h,k){
h.addEventListener('click',function(){stop();act(k)});
h.addEventListener('focus',function(){if(!timer)act(k)});
h.addEventListener('pointerenter',function(e){if(e.pointerType==='touch')return;clearTimeout(hov);hov=setTimeout(function(){stop();act(k)},60)});
h.addEventListener('pointerleave',function(){clearTimeout(hov)});
h.addEventListener('keydown',function(e){var t=null;
if(e.key==='ArrowRight'||e.key==='ArrowDown')t=hs[(k+1)%n];else if(e.key==='ArrowLeft'||e.key==='ArrowUp')t=hs[(k+n-1)%n];else if(e.key==='Home')t=hs[0];else if(e.key==='End')t=hs[n-1];
if(t){e.preventDefault();stop();t.focus();act(+t.getAttribute('data-i'))}})});
bs.forEach(function(b,k){b.addEventListener('click',function(){stop();act(k)});
b.addEventListener('keydown',function(e){var t=null;if(e.key==='ArrowDown')t=bs[(k+1)%n];else if(e.key==='ArrowUp')t=bs[(k+n-1)%n];if(t){e.preventDefault();t.focus()}})});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&timer&&root.contains(d.activeElement))stop()});
if('IntersectionObserver' in window)new IntersectionObserver(function(es){if(!es[0].isIntersecting&&timer)stop()},{threshold:.1}).observe(root);
act(0)});

/* ---- anatomy leader lines ---- */
R('[data-dw=an]').forEach(function(fig){
var svg=fig.querySelector('.dw-an-ln'),fr=fig.querySelector('.dw-an-frame'),cos=R('.dw-co',fig),NS='http://www.w3.org/2000/svg',raf=0;
function draw(){raf=0;svg.innerHTML='';if(innerWidth<=1000)return;var f=fig.getBoundingClientRect(),b=fr.getBoundingClientRect();
var L=cos.filter(function(c){return c.parentNode.classList.contains('dw-an-l')}),Rr=cos.filter(function(c){return c.parentNode.classList.contains('dw-an-r')});
[[L,true],[Rr,false]].forEach(function(g){var arr=g[0],left=g[1],m=arr.length;arr.forEach(function(c,k){
var r=c.getBoundingClientRect(),sx=(left?r.right:r.left)-f.left,sy=r.top+Math.min(r.height/2,32)-f.top,tx=(left?b.left:b.right)-f.left,ty=b.top-f.top+b.height*(k+1)/(m+1),mx=(sx+tx)/2;
var p=d.createElementNS(NS,'path');p.setAttribute('d','M'+sx+' '+sy+'H'+mx+'V'+ty+'H'+tx);p.setAttribute('data-k',c.getAttribute('data-k'));svg.appendChild(p);
var gk=d.createElementNS(NS,'g');gk.setAttribute('data-k',c.getAttribute('data-k'));var ci=d.createElementNS(NS,'circle');ci.setAttribute('cx',tx);ci.setAttribute('cy',ty);ci.setAttribute('r',13);var tx2=d.createElementNS(NS,'text');tx2.setAttribute('x',tx);tx2.setAttribute('y',ty);tx2.textContent=(+c.getAttribute('data-k')+1);gk.appendChild(ci);gk.appendChild(tx2);svg.appendChild(gk)})})}
function q(){if(!raf)raf=requestAnimationFrame(draw)}
cos.forEach(function(c){var k=c.getAttribute('data-k');function on(v){c.classList.toggle('hot',v);R('path[data-k="'+k+'"]',svg).forEach(function(p){p.classList.toggle('hot',v)})}
c.addEventListener('pointerenter',function(){on(true)});c.addEventListener('pointerleave',function(){on(false)})});
addEventListener('resize',q);if('ResizeObserver' in window)new ResizeObserver(q).observe(fig);var im=fr.querySelector('img');if(im&&!im.complete)im.addEventListener('load',q);q();setTimeout(q,400)});

/* ---- mega menus ---- */
var items=R('.q-header .q-nav-item[data-dwm]'),hd=d.querySelector('.q-header'),scrim=null,openIt=null,tIn=0,tOut=0,lastPT='mouse';
if(items.length){scrim=d.createElement('div');scrim.className='dw-scrim';scrim.setAttribute('aria-hidden','true');d.body.appendChild(scrim);scrim.addEventListener('click',function(){close(true)})}
function trig(it){return it.querySelector(':scope>a')}
function pos(){if(!hd||!scrim)return;var hi=hd.querySelector('.q-header-in').getBoundingClientRect();de.style.setProperty('--dw-scrim',Math.round(hi.bottom)+'px')}
function setOpen(it){if(openIt&&openIt!==it){openIt.classList.remove('dw-open');trig(openIt).setAttribute('aria-expanded','false')}
openIt=it;if(it){pos();it.classList.add('dw-open');trig(it).setAttribute('aria-expanded','true');scrim.classList.add('on')}else{scrim.classList.remove('on')}}
function close(focus){var it=openIt;if(!it)return;it.classList.remove('dw-open');trig(it).setAttribute('aria-expanded','false');scrim.classList.remove('on');openIt=null;if(focus)trig(it).focus()}
function foc(p){return R('a[href]',p).filter(function(a){return a.offsetParent!==null||getComputedStyle(a).position==='fixed'})}
items.forEach(function(it,ix){var a=trig(it),p=it.querySelector('.dw-mega');a.setAttribute('aria-expanded','false');if(p)a.setAttribute('aria-controls',p.id);
it.addEventListener('pointerenter',function(e){if(e.pointerType==='touch')return;lastPT='mouse';clearTimeout(tOut);clearTimeout(tIn);if(openIt&&openIt!==it)setOpen(it);else if(!openIt)tIn=setTimeout(function(){setOpen(it)},110)});
it.addEventListener('pointerleave',function(e){if(e.pointerType==='touch')return;clearTimeout(tIn);tOut=setTimeout(function(){if(openIt===it)close(false)},230)});
a.addEventListener('pointerdown',function(e){lastPT=e.pointerType});
a.addEventListener('click',function(e){if(lastPT==='touch'&&innerWidth>1024&&openIt!==it){e.preventDefault();setOpen(it)}});
a.addEventListener('keydown',function(e){var k=e.key,top=R('.q-header .q-nav>a,.q-header .q-nav-item>a');var i=top.indexOf(a);
if(k==='ArrowDown'||k===' '){e.preventDefault();setOpen(it);var f=foc(p);if(f[0])f[0].focus()}
else if(k==='ArrowRight'||k==='ArrowLeft'){e.preventDefault();var t=top[(i+(k==='ArrowRight'?1:top.length-1))%top.length];if(openIt)close(false);t.focus()}
else if(k==='Escape'&&openIt){e.preventDefault();close(true)}});
if(p)p.addEventListener('keydown',function(e){var k=e.key,f=foc(p),i=f.indexOf(d.activeElement);
if(k==='Escape'){e.preventDefault();close(true)}
else if(k==='ArrowDown'||k==='ArrowRight'){e.preventDefault();f[(i+1)%f.length].focus()}
else if(k==='ArrowUp'||k==='ArrowLeft'){e.preventDefault();if(i<=0){a.focus()}else f[i-1].focus()}
else if(k==='Home'){e.preventDefault();f[0].focus()}else if(k==='End'){e.preventDefault();f[f.length-1].focus()}});
it.addEventListener('focusout',function(e){var to=e.relatedTarget;if(openIt===it&&(!to||!it.contains(to)))setTimeout(function(){if(openIt===it&&!it.contains(d.activeElement))close(false)},0)});
a.addEventListener('focus',function(){if(openIt&&openIt!==it)close(false)})});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&openIt)close(true)});
d.addEventListener('pointerdown',function(e){if(openIt&&!openIt.contains(e.target))close(false)});
addEventListener('resize',function(){if(innerWidth<=1024)close(false)});

/* ---- header that condenses (the box keeps its height, so nothing under it moves) ---- */
if(hd){var hi=hd.querySelector('.q-header-in'),ut=hd.querySelector('.pv-util'),cond=false,ticking=false;
function meas(){hd.classList.remove('dw-fix','dw-cond');cond=false;hd.style.removeProperty('--dw-h0');
var uh=ut?ut.offsetHeight:0,h0=hd.offsetHeight,hin=hi.offsetHeight,hin1=Math.round(hin*.78);
hd.style.setProperty('--dw-h0',h0+'px');hd.style.setProperty('--dw-u',uh+'px');hd.style.setProperty('--dw-hin1',hin1+'px');hd.style.setProperty('--dw-h1',hin1+'px');
hd.classList.add('dw-fix');upd(true)}
function pp(v){de.style.setProperty('--pp-hdr',v+'px');de.style.setProperty('--p2-top',v+'px')}
function upd(force){ticking=false;var y=scrollY,c=cond;if(y>80)c=true;else if(y<36)c=false;if(c!==cond||force){cond=c;hd.classList.toggle('dw-cond',c);pp(parseInt(hd.style.getPropertyValue(c?'--dw-h1':'--dw-h0'))||0);pos()}}
meas();addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(function(){upd(false)})}},{passive:true});
var rt=0;addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(meas,150)});
if(d.fonts&&d.fonts.ready)d.fonts.ready.then(function(){meas()})}

/* ---- dark stage texture and cursor spotlight ---- */
var fine=matchMedia('(hover: hover) and (pointer: fine)').matches;
var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){var f=e.target.querySelector(':scope>.dw-fx');if(f)f.classList.toggle('vis',e.isIntersecting)})}):{observe:function(){}};
R('.lf-dark,.pv-dark').forEach(function(s){if(s.querySelector(':scope>.dw-fx'))return;
var fx=d.createElement('i');fx.className='dw-fx';fx.setAttribute('aria-hidden','true');fx.innerHTML='<b class="dw-fx-mesh"></b><b class="dw-fx-grain"></b><b class="dw-fx-spot"></b>';s.insertBefore(fx,s.firstChild);s.classList.add('dw-stagefx');
if(fine&&!reduce){var raf=0,ex=0,ey=0;s.addEventListener('pointermove',function(e){if(e.pointerType==='touch')return;ex=e.clientX;ey=e.clientY;if(!raf)raf=requestAnimationFrame(function(){raf=0;var r=s.getBoundingClientRect();fx.style.setProperty('--dw-x',(ex-r.left)+'px');fx.style.setProperty('--dw-y',(ey-r.top)+'px');fx.classList.add('hov')})},{passive:true});
s.addEventListener('pointerleave',function(){fx.classList.remove('hov')})}
io.observe(s)});
})();
"""
