"""Panel art direction for the DMP preview: THE SITE IS A SECURITY PANEL.

Everything here is gated on the DMP content slug (post() returns the page untouched for any other client), and the section
types it registers (pn-hero, pn-zone, pn-feature) are only ever named by brands/dmp_panel.py.

  RENDER_PANEL      section renderers: the keypad hero, the six zone scenes, the Press feature story
  post(doc, ...)    one pass over a finished page: system colour key, zone bar, heartbeat rail, the panel CSS and JS,
                    the self-hosted display faces, and (Showcase only) the black-and-yellow regrade of the existing modules

Showcase = the Panel (industrial black and DMP yellow, condensed display type, mono micro labels).
Clean    = Swiss spec sheet (hairline grid, tick marks, dimension lines, tabular numerals).
Press    = editorial magazine (serif headlines, photo covers, pull quotes, columns).
"""
from __future__ import annotations

import colorsys
import html as _html
import re

from preview_panel_css import SYS_CSS, SHOWCASE_CSS, CLEAN_CSS, PRESS_CSS, PANEL_JS

SLUG = "digital-monitoring-products"

ZONES = [
    (1, "intrusion", "Intrusion", "#ffd23d", "services/intrusion.html"),
    (2, "access", "Access", "#2fd47a", "services/access-control.html"),
    (3, "fire", "Fire", "#ff5a4d", "services/fire.html"),
    (4, "video", "Video", "#4aa3ff", "services/video.html"),
    (5, "mobile", "Mobile", "#9b87ff", "services/mobile-automation.html"),
    (6, "dealers", "Dealers", "#f3f2ed", "find-a-dealer.html"),
]
ZCOL = {z[0]: z[3] for z in ZONES}

MARK_A, MARK_B = "<!--pn:keep-->", "<!--/pn:keep-->"


def _keep(markup: str) -> str:
    """Panel markup carries its own colours; the Showcase regrade must not touch it."""
    return MARK_A + markup + MARK_B


# ------------------------------------------------------------------------------------------------ hero: the keypad

SHIELD = '''<svg viewBox="0 0 160 170" aria-hidden="true" focusable="false">
<defs><linearGradient id="pnShG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#bfe0ff"/><stop offset=".45" stop-color="#4f9bff"/><stop offset="1" stop-color="#0d3da8"/></linearGradient>
<linearGradient id="pnShF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a7af0"/><stop offset="1" stop-color="#0a2f8c"/></linearGradient></defs>
<circle class="sh-ring-bg" cx="80" cy="85" r="78"/><circle class="sh-ring" cx="80" cy="85" r="78" pathLength="100"/>
<path class="sh-outer" d="M80 22 L128 37 V80 C128 111 108 135 80 147 C52 135 32 111 32 80 V37 Z"/>
<path class="sh-trace" pathLength="100" d="M80 22 L128 37 V80 C128 111 108 135 80 147 C52 135 32 111 32 80 V37 Z"/>
<path class="sh-inner" d="M80 36 L116 47 V80 C116 104 101 122 80 132 C59 122 44 104 44 80 V47 Z"/>
<g class="sh-lock"><path class="sh-shackle" d="M68 80 V70 a12 12 0 0 1 24 0 V80"/><rect class="sh-body" x="62" y="80" width="36" height="28" rx="4"/><circle class="sh-key" cx="80" cy="92" r="3.6"/><rect class="sh-key" x="78.4" y="93" width="3.2" height="8" rx="1.4"/></g>
</svg>'''

SND_SVG = ('<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/>'
           '<path class="on" d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
           '<path class="off" d="M16.5 9.5l5 5m0-5l-5 5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>')


def _hero(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    hid = s.get("id", "hero")
    logo = rel("assets/dmp-logo-light.svg")
    eb = s.get("eyebrow") or []
    eyebrow = ('<p class="pn-eyebrow"><i aria-hidden="true"></i>' + ' <span aria-hidden="true">/</span> '.join(E(x) for x in eb) + "</p>") if eb else ""
    lines = "".join(f'<span class="pn-h1-l">{E(x)}</span>' for x in s.get("lines", []))
    btns = ""
    if s.get("primary"):
        btns += f'<a class="pn-btn pn-btn-y" href="{E(L(s["primary"]["href"]))}">{E(s["primary"]["label"])}</a>'
    if s.get("secondary"):
        btns += f'<a class="pn-btn pn-btn-o" href="{E(L(s["secondary"]["href"]))}">{E(s["secondary"]["label"])}</a>'
    lane = "".join(f'<a href="{E(L(h))}">{E(t)}{" <span aria-hidden=true>&darr;</span>" if h.startswith("#") else ""}</a>' for t, h in s.get("lane", []))
    lane = f'<p class="pn-lane">{lane}</p>' if lane else ""
    menu = "".join(f'<a href="#z{n}" style="--zc:{c}"><i aria-hidden="true"></i>{E(label)}</a>' for n, _k, label, c, _h in ZONES)
    spec = "".join(f'<div><dt>{E(k)}</dt><dd>{E(v)}</dd><dd class="d">{E(d)}</dd></div>' for k, v, d in s.get("spec", []))
    out = f'''<section class="pn-hero" id="{E(hid)}" aria-labelledby="pn-h1">
<script>document.documentElement.classList.add("pn-js")</script>
<div class="pn-hero-grid" aria-hidden="true"></div><span class="pn-mark pn-mark-tl" aria-hidden="true"></span><span class="pn-mark pn-mark-br" aria-hidden="true"></span>
<div class="pn-hero-in">
<div class="pn-hero-copy">{eyebrow}
<h1 id="pn-h1" class="pn-h1">{lines}<span class="pn-h1-l pn-h1-state"><span class="pn-h1-word" data-pn-headline>Armed.</span></span></h1>
<div class="pn-hero-more"><p class="pn-lede">{E(s.get("subhead", ""))} <strong class="pn-js-only" data-pn-invite>Disarm it, then arm it again.</strong></p>
<div class="pn-hero-cta">{btns}</div>{lane}</div>
</div>
<div class="pn-hero-kp">
<div class="pn-kp" id="pn-kp">
<div class="pn-kp-case"><i class="pn-kp-led" aria-hidden="true"></i><i class="pn-kp-mic" aria-hidden="true"></i>
<div class="pn-kp-glass"><div class="pn-kp-screen">
<svg class="pn-kp-arcs" viewBox="0 0 700 440" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="M452 -20 C404 120 404 320 452 460" fill="none" stroke="rgba(160,205,255,.35)" stroke-width="1.5"/><path d="M452 -20 C404 120 404 320 452 460 L720 460 L720 -20 Z" fill="rgba(2,10,40,.38)"/><path d="M-20 318 C120 290 260 300 420 352" fill="none" stroke="rgba(160,205,255,.14)" stroke-width="1"/></svg>
<div class="pn-kp-bar"><img class="pn-kp-logo" src="{E(logo)}" alt="" width="100" height="37"><span class="pn-kp-clock" aria-hidden="true"><span data-pn-day>TUE</span> <span data-pn-time>5:35 PM</span><svg viewBox="0 0 20 14" aria-hidden="true" focusable="false"><path d="M1 5a13 13 0 0 1 18 0M4 8a9 9 0 0 1 12 0M7 11a4.5 4.5 0 0 1 6 0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></span></div>
<div class="pn-kp-info" aria-hidden="true"><span class="pn-kp-big">06</span><span class="pn-kp-cap">Zones</span><dl><div><dt>Status</dt><dd data-pn-status>Secure</dd></div><div><dt>Check-in</dt><dd>OK</dd></div></dl></div>
<div class="pn-kp-core">
<button class="pn-kp-shield" type="button" data-pn-toggle aria-pressed="true" aria-label="Site armed. Press to disarm">{SHIELD}</button>
<p class="pn-kp-state" data-pn-label aria-hidden="true">ARMED</p>
<button class="pn-kp-arm" type="button" data-pn-toggle data-pn-armtxt tabindex="-1" aria-hidden="true">Disarm</button>
</div>
<nav class="pn-kp-menu" aria-label="Keypad menu, jump to a zone">{menu}</nav>
<p class="pn-kp-log" aria-hidden="true"><span>Event</span> <b data-pn-logline>All zones armed. Supervised.</b></p>
<div class="pn-kp-events" id="pn-events" hidden><div class="pn-kp-events-h"><b>Events</b><button type="button" data-pn-events-close>Close</button></div><ol data-pn-events-list><li><b>00:00:00</b><span>System armed</span></li></ol></div>
<i class="pn-kp-sheen" aria-hidden="true"></i>
</div></div></div>
<i class="pn-kp-floor" aria-hidden="true"></i>
</div>
<div class="pn-ctl pn-js-only" role="group" aria-label="Keypad controls">
<button type="button" class="pn-key pn-key-arm" data-pn-toggle data-pn-armtxt>Disarm</button>
<button type="button" class="pn-key" data-pn-events-open aria-expanded="false" aria-controls="pn-events">Events</button>
<button type="button" class="pn-key pn-snd" data-pn-sound aria-pressed="false">{SND_SVG}<span data-pn-sndtxt>Sound off</span></button>
</div>
<p class="pn-kp-hint" role="status" aria-live="polite" data-pn-hint>Site armed. Six zones supervised.</p>
<p class="pn-kp-demo">Demo keypad. No signal is sent.</p>
</div>
</div>
<dl class="pn-hero-spec">{spec}</dl>
</section>'''
    return _keep(out)


# ------------------------------------------------------------------------------------------------ zone scenes

def _zhead(s, E):
    n = s["z"]
    meta = f'<span class="pn-zmeta">{E(s["meta"])}</span>' if s.get("meta") else ""
    return (f'<header class="pn-zhead"><span class="pn-ztag"><i class="pn-led" aria-hidden="true"></i>Zone {n:02d}</span>'
            f'<span class="pn-zname">{E(s["name"])}</span><span class="pn-zrule" aria-hidden="true"></span>{meta}</header>')


def _more(s, ctx):
    if not s.get("more"):
        return ""
    t, h = s["more"]
    return f'<p class="pn-more"><a class="pn-btn pn-btn-o" href="{ctx["E"](ctx["L"](h))}">{ctx["E"](t)} <span aria-hidden="true">&rarr;</span></a></p>'


def _z1(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    u = s.get("unit") or ["", "", ""]
    sl = s["slab"]
    rows = "".join(f"<div><dt>{E(k)}</dt><dd>{E(_short(v))}</dd></div>" for k, v in sl["items"])
    notes = ""
    for n in s.get("notes", []):
        soon = " pn-soon" if n.get("soon") else ""
        notes += (f'<li class="pn-rv{soon}"><span class="pn-nk">{"<i aria-hidden=true></i>" if n.get("soon") else ""}{E(n["k"])}</span>'
                  f'<h3><a href="{E(L(n["href"]))}">{E(n["title"])}</a></h3><p>{E(n["text"])}</p></li>')
    return f'''<div class="pn-z1-grid">
<div class="pn-z1-num"><p class="pn-num" aria-hidden="true"><span class="pn-num-o">{E(s["num"])}</span><span class="pn-num-f">{E(s["num"])}</span></p>
<p class="pn-num-unit"><span>{E(u[0])}</span><span class="pn-num-plus" aria-hidden="true">+</span><span><b>{E(u[1])}</b> {E(u[2])}</span></p></div>
<div class="pn-z1-copy pn-rv"><h2 id="{E(s["id"])}h" class="pn-h2">{ctx["RAW"](s["heading"])}</h2><p>{E(s.get("body", ""))}</p>{_more(s, ctx)}</div>
<div class="pn-slab pn-rv"><p class="pn-slab-h"><span>{E(sl["title"])}</span><span>{E(sl["name"])}</span></p><dl>{rows}</dl>
<a class="pn-slab-go" href="{E(L(sl["href"]))}">{E(sl["label"])} <span aria-hidden="true">&rarr;</span></a>
<img class="pn-slab-img" src="{E(rel(sl["image"]))}" alt="{E(sl["alt"])}" width="1200" height="818" loading="lazy" decoding="async"></div>
</div>
<ul class="pn-notes">{notes}</ul>'''


def _short(v):
    """Spec values on the slab: '32 out of the box, 96 maximum' -> '32 / 96 max'."""
    m = re.match(r"^(\d+) out of the box, (\d+) maximum$", str(v))
    return f"{m.group(1)} / {m.group(2)} max" if m else v


def _z2(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    ro = s.get("readout")
    readout = f'<p class="pn-readout"><span>{E(ro[0])}</span><b>{E(ro[1])}</b></p>' if ro else ""
    calls = "".join(f'<li class="pn-rv"><span class="pn-cn" aria-hidden="true">{i + 1:02d}</span><div><h3><a href="{E(L(c["href"]))}">{E(c["title"])}</a></h3><p>{E(c["text"])}</p></div></li>'
                    for i, c in enumerate(s.get("calls", [])))
    return f'''<div class="pn-z2-grid">
<div class="pn-z2-copy pn-rv"><h2 id="{E(s["id"])}h" class="pn-h2">{ctx["RAW"](s["heading"])}</h2><p>{E(s.get("body", ""))}</p>{readout}{_more(s, ctx)}</div>
<div class="pn-z2-stage"><i class="pn-ring r1" aria-hidden="true"></i><i class="pn-ring r2" aria-hidden="true"></i><i class="pn-ring r3" aria-hidden="true"></i>
<img src="{E(rel(s["image"]))}" alt="{E(s.get("alt", ""))}" width="347" height="924" loading="lazy" decoding="async"></div>
<ol class="pn-calls">{calls}</ol>
</div>'''


def _z3(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    big = s.get("big") or ["", ""]
    lcd = s.get("lcd") or []
    lines = "".join(f'<p>{"" if i == 0 else "&gt; "}{E(x)}{"<i aria-hidden=true></i>" if i == len(lcd) - 1 else ""}</p>' for i, x in enumerate(lcd))
    stats = "".join(f'<div class="pn-rv"><dd>{E(v)}</dd><dt>{E(k)}</dt></div>' for v, k in s.get("stats", []))
    bg = (f'<div class="pn-z3-bg" aria-hidden="true"><img src="{E(rel(s["bg"]))}" alt="" width="1280" height="724" loading="lazy" decoding="async"></div>'
          f'<p class="pv-envcap">Illustrative scene</p>') if s.get("bg") else ""
    return f'''{bg}<div class="pn-z3-grid">
<div class="pn-z3-copy"><p class="pn-volt" aria-hidden="true">{E(big[0])}<span>{E(big[1])}</span></p>
<h2 id="{E(s["id"])}h" class="pn-h2 pn-rv">{ctx["RAW"](s["heading"])}</h2>
<div class="pn-lcd pn-rv" role="img" aria-label="{E(s.get("lcd_label", ""))}">{lines}</div>{_more(s, ctx)}</div>
<figure class="pn-z3-prod pn-rv"><a href="{E(L(s["href"]))}" aria-label="{E(s.get("label", ""))}"><img src="{E(rel(s["image"]))}" alt="{E(s.get("alt", ""))}" width="1016" height="920" loading="lazy" decoding="async"></a></figure>
</div>
<dl class="pn-z3-stats">{stats}</dl>'''


VMS_SVG = ('<svg viewBox="0 0 64 64" aria-hidden="true" focusable="false"><rect x="8" y="12" width="48" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="2.5"/>'
           '<path d="M8 22h48M24 12v32M40 12v32M22 52h20M32 44v8" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>')


def _z4(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    cap = s.get("cap") or ["", ""]
    steps = ""
    for i, p in enumerate(s.get("path", [])):
        media = (f'<div class="pn-pimg pn-palarm">{VMS_SVG}</div>' if p.get("icon") else
                 f'<div class="pn-pimg"><img src="{E(rel(p["image"]))}" alt="" width="600" height="342" loading="lazy" decoding="async"></div>')
        steps += f'<li><span class="pn-pn" aria-hidden="true">{i + 1:02d}</span>{media}<h3><a href="{E(L(p["href"]))}">{E(p["title"])}</a></h3><p>{E(p["text"])}</p></li>'
    return f'''<div class="pn-z4-top">
<div class="pn-z4-copy pn-rv"><h2 id="{E(s["id"])}h" class="pn-h2">{ctx["RAW"](s["heading"])}</h2><p>{E(s.get("body", ""))}</p>{_more(s, ctx)}</div>
<figure class="pn-finder pn-rv"><img src="{E(rel(s["image"]))}" alt="{E(s.get("alt", ""))}" width="1200" height="800" loading="lazy" decoding="async">
<i class="pn-fc tl" aria-hidden="true"></i><i class="pn-fc tr" aria-hidden="true"></i><i class="pn-fc bl" aria-hidden="true"></i><i class="pn-fc br" aria-hidden="true"></i>
<figcaption><span><i class="pn-rec" aria-hidden="true"></i>{E(cap[0])}</span><span>{E(cap[1])}</span></figcaption></figure>
</div>
<div class="pn-path" role="group" aria-label="How a video alarm travels"><p class="pn-path-h">{E(s.get("path_label", "Signal path"))}</p>
<div class="pn-path-line" aria-hidden="true"><i></i></div><ol>{steps}</ol></div>'''


def _z5(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    pl = s["plate"]
    rows = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in pl["rows"])
    links = "".join(f'<a href="{E(L(h))}">{E(t)}</a>' for t, h in s.get("links", []))
    return f'''<div class="pn-z5-grid">
<div class="pn-z5-stage pn-rv"><img src="{E(rel(s["image"]))}" alt="{E(s.get("alt", ""))}" width="1200" height="682" loading="lazy" decoding="async"></div>
<div class="pn-z5-copy pn-rv"><h2 id="{E(s["id"])}h" class="pn-h2">{ctx["RAW"](s["heading"])}</h2><p>{E(s.get("body", ""))}</p>
<p class="pn-chips">{links}</p>{_more(s, ctx)}</div>
<div class="pn-plate pn-rv"><i class="pn-rivet a" aria-hidden="true"></i><i class="pn-rivet b" aria-hidden="true"></i><i class="pn-rivet c" aria-hidden="true"></i><i class="pn-rivet d" aria-hidden="true"></i>
<p class="pn-plate-k">{E(pl["k"])}</p><p class="pn-plate-big"><span>{E(pl["big"][0])}</span><span>{E(pl["big"][1])}</span></p><dl>{rows}</dl>
<a class="pn-plate-go" href="{E(L(pl["href"]))}">{E(pl["label"])} <span aria-hidden="true">&rarr;</span></a></div>
</div>'''


def _z6(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    ctas = "".join(f'<a class="pn-btn {"pn-btn-k" if i == 0 else "pn-btn-ko"}" href="{E(L(h))}">{E(t)}</a>' for i, (t, h) in enumerate(s.get("ctas", [])))
    v = s.get("video") or {}
    cap = v.get("cap") or ["", ""]
    feed = ""
    if v:
        feed = (f'<figure class="pn-feed pn-rv"><div class="pn-feed-v" data-pn-video data-mp4="{E(rel(v["mp4"]))}" data-webm="{E(rel(v.get("webm", "")))}">'
                f'<img src="{E(rel(v["poster"]))}" alt="{E(v.get("label", ""))}" width="1600" height="900" loading="lazy" decoding="async"></div>'
                f'<i class="pn-fc tl" aria-hidden="true"></i><i class="pn-fc tr" aria-hidden="true"></i><i class="pn-fc bl" aria-hidden="true"></i><i class="pn-fc br" aria-hidden="true"></i>'
                f'<figcaption><span>{E(cap[0])}</span><span>{E(cap[1])}</span></figcaption></figure>')
    row = "".join(f'<div><dt>{E(k)}</dt><dd>{f"<a href={chr(34)}{E(L(h))}{chr(34)}>{E(val)}</a>" if h else E(val)}</dd></div>' for k, val, h in s.get("row", []))
    return f'''<div class="pn-z6-grid">
<div class="pn-z6-copy"><p class="pn-year" aria-hidden="true">{E(s.get("year", ""))}</p>
<h2 id="{E(s["id"])}h" class="pn-h2 pn-rv">{ctx["RAW"](s["heading"])}</h2><p class="pn-rv">{E(s.get("body", ""))}</p>
<div class="pn-z6-cta pn-rv">{ctas}</div></div>{feed}
</div>
<dl class="pn-z6-row">{row}</dl>'''


_Z = {1: _z1, 2: _z2, 3: _z3, 4: _z4, 5: _z5, 6: _z6}


def _zone(s, ctx):
    E = ctx["E"]
    n = int(s["z"])
    zc = ZCOL[n]
    body = _Z[n](s, ctx)
    return _keep(f'<section class="pn-zone pn-z{n}" id="{E(s["id"])}" data-zone="{n}" style="--zc:{zc}" aria-labelledby="{E(s["id"])}h">'
                 f'<div class="pn-zin">{_zhead(s, E)}{body}</div></section>')


# ------------------------------------------------------------------------------------------------ Press feature story

def _feature(s, ctx):
    """Press: the history timeline as a magazine feature. A full-bleed cover with a pull quote, then the milestones in columns."""
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    items = s.get("items", [])
    cols = "".join(f'<li><span class="y">{E(it[0])}</span><h3>{E(it[1])}</h3><p>{E(it[2])}</p></li>' for it in items)
    more = f'<p class="pnf-more"><a href="{E(L(s["more"][1]))}">{E(s["more"][0])}</a></p>' if s.get("more") else ""
    cover = ""
    if s.get("cover"):
        base = s["cover"].replace("-1280.jpg", "")
        cover = (f'<div class="pnf-cover"><img src="{E(rel(s["cover"]))}" srcset="{E(rel(base + "-800.jpg"))} 800w, {E(rel(s["cover"]))} 1280w, {E(rel(base + "-1920.jpg"))} 1920w" sizes="100vw" alt="" width="1920" height="1086" loading="lazy" decoding="async">'
                 f'<div class="pnf-over"><div class="q-container"><p class="pnf-k">{E(s.get("kicker", "Feature"))} <span>{E(s.get("eyebrow", ""))}</span></p>'
                 f'<h2 class="q-h2 pnf-h">{E(s["heading"])}</h2>'
                 f'<blockquote class="pnf-q"><p>{E(s.get("quote", ""))}</p><footer>{E(s.get("quote_by", ""))}</footer></blockquote></div></div>'
                 f'<p class="pv-envcap">{E(s.get("cover_caption", "Illustrative scene"))}</p></div>')
    return (f'<section class="q-section pnf" id="{E(s.get("id", "story"))}">{cover}'
            f'<div class="q-container"><p class="pnf-intro">{E(s.get("intro", ""))}</p><ol class="pnf-cols">{cols}</ol>{more}</div></section>')


def _brief(s, ctx):
    """Showcase home: news and guides as one panel readout. Two columns of dated lines, every one a link."""
    E, L = ctx["E"], ctx["L"]
    hid = s.get("id", "brief")
    cols = ""
    for ci, c in enumerate(s.get("cols", [])):
        rows = ""
        for i, (tag, title, text, href) in enumerate(c["items"]):
            rows += (f'<li class="pn-rv"><span class="pn-bn" aria-hidden="true">{i + 1:02d}</span><div><p class="pn-bt">{E(tag)}</p>'
                     f'<h4><a href="{E(L(href))}">{E(title)} <span aria-hidden="true">&rarr;</span></a></h4><p>{E(text)}</p></div></li>')
        cols += (f'<div class="pn-bcol"><p class="pn-bk"><i class="pn-led" aria-hidden="true"></i>{E(c["k"])}</p>'
                 f'<h3 id="{E(hid)}-c{ci}">{E(c["title"])}</h3><ol aria-labelledby="{E(hid)}-c{ci}">{rows}</ol></div>')
    return _keep(f'<section class="pn-brief" id="{E(hid)}" aria-labelledby="{E(hid)}-h"><div class="pn-bin">'
                 f'{_shead(s.get("eyebrow", "Briefing"), "News / Guides")}<header class="pn-bhead"><h2 id="{E(hid)}-h" class="pn-h2">{E(s["heading"])}</h2></header>'
                 f'<div class="pn-bgrid">{cols}</div></div></section>')


def _none(s, ctx):
    """A section that exists in one direction only: the base type renders nothing, a variant supplies the real section."""
    return ""


RENDER_PANEL = {"pn-hero": _hero, "pn-zone": _zone, "pn-feature": _feature, "pn-brief": _brief, "pn-none": _none}


# ------------------------------------------------------------------------------------------------ Showcase regrade

_HEX = re.compile(r"(?<![&%\w])#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
_RGB = re.compile(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})")


# where navy goes in each direction: (hue, saturation of the dark tones, darkening of the deepest tones, hue and saturation of light tints)
TONE = {"showcase": (0.62, 0.035, 0.62, 0.13, 0.10),      # neutral black
        "clean": (0.60, 0.10, 0.92, 0.60, 0.10),          # cool graphite
        "press": (0.10, 0.13, 0.80, 0.11, 0.22)}          # warm ink


def _neutral(r, g, b, tone):
    """Navy and blue-grey become the direction's own dark; everything else is returned unchanged (None)."""
    th, ts, dk, lh, ls = tone
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    hue = h * 360
    if not (200 <= hue <= 250):
        return None
    if l < 0.42 and s > 0.16:
        l2 = l * (dk if l < 0.2 else (dk + 1) / 2)
        r2, g2, b2 = colorsys.hls_to_rgb(th, l2, ts)
    elif l >= 0.6 and 0.12 < s < 0.62:
        r2, g2, b2 = colorsys.hls_to_rgb(lh, l, ls)
    elif 0.42 <= l < 0.6 and 0.12 < s < 0.45:
        r2, g2, b2 = colorsys.hls_to_rgb(th, l, ts)
    elif 0.45 <= l < 0.8 and s >= 0.45 and 214 <= hue <= 240:
        r2, g2, b2 = colorsys.hls_to_rgb(lh, 0.62, 0.06)          # blue corner glows become a neutral haze
    else:
        return None
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)


def _regrade_text(t: str, tone) -> str:
    def hx(m):
        v = m.group(1)
        if len(v) == 3:
            v = "".join(c * 2 for c in v)
        n = _neutral(int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16), tone)
        return m.group(0) if n is None else "#%02x%02x%02x" % n

    def rg(m):
        n = _neutral(int(m.group(1)), int(m.group(2)), int(m.group(3)), tone)
        return m.group(0) if n is None else m.group(0)[:m.group(0).index("(") + 1] + "%d,%d,%d" % n
    return _RGB.sub(rg, _HEX.sub(hx, t))


_RADIUS = re.compile(r"border-radius:([^;}]+)")


def _square(css: str) -> str:
    """Industrial corners: every pixel radius (cards, pills, chips) becomes 2px; circles written as 50% stay round."""
    def sub(m):
        v = m.group(1)
        if "%" in v or "inherit" in v or v.strip() in ("0", "0px", "1px", "2px"):
            return m.group(0)
        imp = "!important" if "!important" in v else ""
        return "border-radius:2px" + imp
    return _RADIUS.sub(sub, css)


def regrade(doc: str, dslug: str) -> str:
    """Navy leaves the page (each direction has its own dark), skipping panel markup (the keypad is blue on purpose) and ld+json."""
    tone = TONE[dslug]
    out, pos = [], 0
    for m in re.finditer(re.escape(MARK_A) + r".*?" + re.escape(MARK_B) + r"|<script type=\"application/ld\+json\">.*?</script>", doc, re.S):
        out.append(_regrade_text(doc[pos:m.start()], tone))
        out.append(m.group(0))
        pos = m.end()
    out.append(_regrade_text(doc[pos:], tone))
    return "".join(out)


# ------------------------------------------------------------------------------------------------ chrome: zone bar, rail

def _zonebar(page, root):
    E = _html.escape
    home = page["file"] == "index.html"
    cur = page.get("sys")
    items = []
    for n, key, label, c, href in ZONES:
        if home:
            a = f'<a href="#z{n}" style="--zc:{c}" data-z="{n}"><i class="pn-led" aria-hidden="true"></i><b>Z{n}</b><span>{E(label)}</span><em aria-hidden="true" data-pn-zst>Secure</em></a>'
        else:
            on = ' class="is-on" aria-current="true"' if key == cur else ""
            a = f'<a href="{E(root + href)}" style="--zc:{c}"{on}><i class="pn-led" aria-hidden="true"></i><b>Z{n}</b><span>{E(label)}</span></a>'
        items.append(f"<li>{a}</li>")
    right = ('<div class="pn-zb-r"><span class="pn-st" aria-hidden="true"><i></i><span data-pn-label>ARMED</span></span></div>' if home else "")
    return (f'<nav class="pn-zb{" pn-zb-home" if home else ""}" aria-label="{"Zones on this page" if home else "DMP systems"}">'
            f'<ol>{"".join(items)}</ol>{right}</nav>')


# chapter rail (Showcase home, wide screens): section id, label. Only chapters whose section is on the page are listed.
CHAPTERS = [("hero-layered", "Panel"), ("z1", "Zones"), ("night", "Night shift"), ("scenes", "Scenes"), ("z6", "Dealers"),
            ("proof", "Proof"), ("who", "Start here"), ("brief", "News"), ("contact", "Contact")]


def _chapters(doc):
    E = _html.escape
    have = [(i, t) for i, t in CHAPTERS if f' id="{i}"' in doc]
    if len(have) < 3:
        return ""
    ON = ' class="is-on" aria-current="true"'
    li = "".join(f'<li><a href="#{E(i)}" data-ch="{E(i)}" data-t="{E(t)}" aria-label="Chapter {n + 1}, {E(t)}"{ON if n == 0 else ""}><i class="pn-led" aria-hidden="true"></i><span aria-hidden="true"><b>{n + 1:02d}</b> {E(t)}</span></a></li>'
                 for n, (i, t) in enumerate(have))
    return (f'<nav class="pn-ch" aria-label="Chapters on this page"><ol>{li}</ol>'
            f'<span class="pn-ch-tag" aria-hidden="true"><b data-pn-chn>01</b> / {len(have):02d} <em data-pn-cht>{E(have[0][1])}</em></span></nav>')


# Showcase home: the modules after the zones get the same head row the zones have (tag, rule, meta), so the page reads as
# one panel from top to bottom. Decorative (aria-hidden): each section keeps its own eyebrow and heading.
SECTION_HEADS = {"proof": ("Proof", "Since 1975"), "story": ("History", "1975 to 2025"),
                 "who": ("Start here", "Dealers / Specifiers / Building owners"),
                 "faq": ("Questions", "Dealers / Specifiers"), "contact": ("Contact", "Inside Sales")}


def _shead(label, meta):
    E = _html.escape
    return (f'<div class="pn-sh" aria-hidden="true"><span class="pn-sh-t"><i class="pn-led"></i>{E(label)}</span>'
            f'<span class="pn-sh-r"></span><span class="pn-sh-m">{E(meta)}</span></div>')


def _section_heads(doc):
    for sid, (label, meta) in SECTION_HEADS.items():
        doc = re.sub(r'(<section class="q-section[^"]*" id="%s"[^>]*>)' % re.escape(sid), lambda m: m.group(1) + _shead(label, meta), doc, count=1)
    return doc


RAIL = ('<div class="pn-beat" aria-hidden="true"><i class="pn-beat-base"></i><i class="pn-beat-live"></i>'
        '<span class="pn-beat-tag"><b>SUPERVISED</b> <em data-pn-beat>CHECK-IN 0001</em></span></div>')


def _fonts(dslug, up):
    """Per-page inline faces (the url depends on the page depth, so this block stays inline and small)."""
    f = up + "assets/fonts/"
    uni = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
    if dslug == "showcase":
        return ("<style>"
                f"@font-face{{font-family:'Barlow Condensed';font-weight:800;font-display:swap;src:url({f}barlow-condensed-800-latin.woff2) format('woff2');unicode-range:{uni}}}"
                f"@font-face{{font-family:'Barlow Condensed';font-weight:700;font-display:swap;src:url({f}barlow-condensed-700-latin.woff2) format('woff2');unicode-range:{uni}}}"
                "@font-face{font-family:'Barlow Condensed Fallback';font-weight:700 800;src:local('Arial Bold'),local('Arial-BoldMT');size-adjust:70%;ascent-override:118%;descent-override:26%;line-gap-override:0%}"
                f"@font-face{{font-family:'JetBrains Mono';font-weight:400 700;font-display:swap;src:url({f}jetbrains-mono-latin-var.woff2) format('woff2');unicode-range:{uni}}}"
                "</style>"
                f'<meta name="pv-preload-font" content="{f}barlow-condensed-800-latin.woff2">')
    if dslug == "clean":
        return ("<style>"
                f"@font-face{{font-family:'JetBrains Mono';font-weight:400 700;font-display:swap;src:url({f}jetbrains-mono-latin-var.woff2) format('woff2');unicode-range:{uni}}}"
                "</style>")
    if dslug == "press":
        return ("<style>"
                f"@font-face{{font-family:'Playfair Display';font-style:normal;font-weight:400 900;font-display:swap;src:url({f}playfair-display-latin-var.woff2) format('woff2');unicode-range:{uni}}}"
                f"@font-face{{font-family:'Playfair Display';font-style:italic;font-weight:400 900;font-display:swap;src:url({f}playfair-display-italic-latin-var.woff2) format('woff2');unicode-range:{uni}}}"
                "@font-face{font-family:'Playfair Fallback';src:local('Georgia');size-adjust:103%}"
                "</style>"
                f'<meta name="pv-preload-font" content="{f}playfair-display-latin-var.woff2">')
    return ""


_SECTION = re.compile(r'<section class="(q-section[^"]*)"')
_LIGHT_OK = ("pv-lh", "lf-dark", "pv-dark", "pp-closer", "pv-tl-stage", "pn-")


def _all_dark(doc):
    """Showcase: every band takes the dark component variants the modules already ship (lf-dark)."""
    def sub(m):
        cls = m.group(1)
        if any(k in cls for k in _LIGHT_OK):
            return m.group(0)
        return f'<section class="{cls} lf-dark pn-dk"'
    return _SECTION.sub(sub, doc)


def post(doc: str, content: dict, page: dict, dslug: str) -> str:
    if content.get("slug") != SLUG:
        return doc
    depth = page["file"].count("/")
    up, root = "../" * (depth + 1), "../" * depth
    home = page["file"] == "index.html"
    sysk = page.get("sys") or ""
    zb = dslug == "showcase" and (home or bool(sysk))

    if dslug in TONE:
        doc = regrade(doc, dslug)
    if dslug == "showcase":
        doc = _all_dark(doc)
        # DMP yellow becomes a variable in the stylesheet, so the DISARMED state can turn the whole page amber
        i = doc.find("</style>")
        head = doc[:i]
        head = re.sub(r"rgba\(255,\s*210,\s*61,\s*(0?\.\d+|1|0)\)", lambda m: "color-mix(in srgb,var(--pn-y) %g%%,transparent)" % (float(m.group(1)) * 100), head)
        head = re.sub(r"(?<![&%\w])#ffd23d\b", "var(--pn-y)", head, flags=re.I)
        head = _square(head)
        doc = head + doc[i:]
        # light logo on the black header
        h0, h1 = doc.find('<header class="q-header">'), doc.find("</header>")
        if h0 >= 0 and h1 > h0:
            doc = doc[:h0] + doc[h0:h1].replace("assets/dmp-logo.svg", "assets/dmp-logo-light.svg") + doc[h1:]
    doc = doc.replace(MARK_A, "").replace(MARK_B, "")

    attrs = f' data-pn="armed"' if dslug == "showcase" else ""
    if sysk:
        attrs += f' data-sys="{sysk}"'
    cls = "pn" + (" pn-zbar" if zb else "") + (" pn-home" if home else "")
    doc = doc.replace(f'<html lang="en" data-dir="{dslug}">', f'<html lang="en" data-dir="{dslug}" class="{cls}"{attrs}>', 1)

    css = SYS_CSS + {"showcase": SHOWCASE_CSS, "clean": CLEAN_CSS, "press": PRESS_CSS}.get(dslug, "")
    i = doc.find("</style>")
    doc = doc[:i] + "\n/* ===== panel pass (scripts/preview_panel.py) ===== */\n" + css + doc[i:]
    doc = doc.replace("</head>", _fonts(dslug, up) + "\n</head>", 1)

    if dslug == "showcase":
        if home:
            doc = _section_heads(doc)
        if zb:
            doc = doc.replace("</div></header>", "</div>" + _zonebar(page, root) + "</header>", 1)
        doc = doc.replace("</body>", (_chapters(doc) if home else "") + RAIL + "\n<script>" + PANEL_JS + "</script>\n</body>", 1)
    return doc
