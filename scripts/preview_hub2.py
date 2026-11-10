"""The chooser hub, second version: a dark header that shows the three directions as pictures before anything else,
then the same evidence sections as before (preview_hub.py), restyled and kept short.

preview_hub.hub() hands over to hub() here (set HUB_V1=1 to get the old page). Nothing in this file is client specific:
the client name, logo, accent, domain, roles and pitch copy all come from the content and brand data.

What is new compared with preview_hub.py
  * Direction cards carry a screenshot of each direction's home page, taken at build time by scripts/hub_shots.py into
    <out>/assets/hub/ (a committed copy in brands/<slug>.assets/hub/ is the fallback). On hover or keyboard focus a tall
    screenshot scrolls inside the frame (CSS only; not on touch devices, not with reduced motion).
  * No Google Fonts when the build ships assets/fonts/inter-latin-var.woff2 and opensans-latin-var.woff2.
  * The per-URL audit (preview_seo) is folded into one compact row per page, 25 at a time, with the rest in the HTML
    behind a <details> for readers without JavaScript; "Open the rebuilt page" links are plain hrefs.
  * The long lists (to confirm, every page) show their first items and fold the rest.
"""
from __future__ import annotations

import html
import json
import os
import re

import reskin

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DARK = "#0a0b0d"
WORDS = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
AUDIT_PAGE = 25
PIXEL = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="

# same faces and fallback metrics as scripts/dedupe_assets.py (measured against Arial)
UNI = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
FONTS = (("Inter", "inter-latin-var.woff2", "400 800"), ("Open Sans", "opensans-latin-var.woff2", "400 800"))
FALLBACK = {"Inter": ((106, 91.4, 22.7), (102.5, 94.5, 23.5)), "Open Sans": ((103.5, 103.3, 28.3), (105, 101.8, 27.9))}


def _e(s) -> str:
    s = "" if s is None else str(s)
    s = re.sub(r"\s*[—–]\s*", ", ", s)
    return html.escape(s, quote=True)


def _slug(theme: str) -> str:
    return theme.replace("Quantum ", "").lower()


def _short(theme: str) -> str:
    return theme.replace("Quantum ", "")


def _sentence(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return ""
    s = s[0].upper() + s[1:]
    return s if s[-1] in ".!?" else s + "."


def local_fonts(out_dir) -> bool:
    return bool(out_dir) and all(os.path.exists(os.path.join(out_dir, "assets", "fonts", f)) for _, f, _ in FONTS)


def font_css(rel="assets") -> str:
    r = []
    for fam, f, w in FONTS:
        r.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;src:url({rel}/fonts/{f}) format('woff2');unicode-range:{UNI}}}")
        (sa, asc, desc), (sb, ascb, descb) = FALLBACK[fam]
        r.append(f"@font-face{{font-family:'{fam} Fallback';font-weight:400 500;src:local('Arial'),local('ArialMT');size-adjust:{sa}%;ascent-override:{asc}%;descent-override:{desc}%;line-gap-override:0%}}")
        r.append(f"@font-face{{font-family:'{fam} Fallback';font-weight:600 800;src:local('Arial Bold'),local('Arial-BoldMT');size-adjust:{sb}%;ascent-override:{ascb}%;descent-override:{descb}%;line-gap-override:0%}}")
    return "\n".join(r) + "\n"


def _on_dark(accent: str) -> str:
    """The accent, lightened until it reads on the dark ground."""
    c = accent
    for _ in range(40):
        if reskin.contrast_ratio(c, DARK) >= 5:
            break
        c = reskin.lighten(c, 0.06)
    return c


def load_roles(content, themes, roles):
    """Roles as given on the command line; when none were passed, the brand's build.json, read now so the copy is never stale."""
    if roles:
        return roles
    p = os.path.join(ROOT, "brands", f"{content.get('slug', '')}.build.json")
    try:
        cfg = json.load(open(p, encoding="utf-8")).get("roles") or {}
    except Exception:  # noqa: BLE001
        return {}
    return {t: cfg[_short(t)] for t in themes if _short(t) in cfg}


def _role(roles, t) -> str:
    return re.sub(r"^[A-Za-z ]+:\s*", "", roles.get(t, "") or "")


def _ground_word(look) -> str:
    hero = reskin.relative_luminance(look.get("hero_ground") or "#ffffff")
    page = reskin.relative_luminance(look.get("page_ground") or "#ffffff")
    if hero < 0.18:
        return "Dark ground" if page < 0.18 else "Dark hero, light pages"
    return "White ground" if hero > 0.93 else "Warm paper ground"


def facts(content, theme, nat, ground, look=None) -> dict:
    """Mood, headline type and ground for one direction. The type and ground are measured on the built home page by
    hub_shots.py when it has run (look), otherwise read from the direction's tokens; the mood word comes from
    data/hub_directions.json, which can also override all three per client."""
    try:
        data = json.load(open(os.path.join(ROOT, "data", "hub_directions.json"), encoding="utf-8"))
    except Exception:  # noqa: BLE001
        data = {}
    s = _slug(theme)
    d = dict((data.get("default") or {}).get(s) or {})
    d.update(((data.get("clients") or {}).get(content.get("slug", "")) or {}).get(s) or {})
    face = (look or {}).get("heading_face") or (nat.get("--q-serif") or nat.get("--q-sans") or "").split(",")[0].strip("'\" ")
    return {"mood": d.get("mood") or "",
            "type": d.get("type") or (f"{face} headlines" if face else ""),
            "ground": d.get("ground") or (_ground_word(look) if look else f"{ground} ground")}


# ---------------------------------------------------------------- screenshots

def _manifest(out_dir) -> dict:
    try:
        return json.load(open(os.path.join(out_dir, "assets", "hub", "shots.json"), encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}


def frame_inner(slug, name, out_dir, first=False) -> str:
    """The picture inside a card's frame: the hero crop, plus the tall crop that scrolls on hover. Empty frame when no image exists."""
    m = (_manifest(out_dir) if out_dir else {}).get(slug) or {}
    base = os.path.join(out_dir or "", "assets", "hub")

    def have(kind, w):
        return f"{kind}-{w}" in m and os.path.exists(os.path.join(base, f"{slug}-{kind}-{w}.jpg"))

    hero = [w for w in (640, 960) if have("hero", w)]
    if not hero:
        return f'<span class="dnone" aria-hidden="true">{_e(name)}</span>'
    w0 = hero[-1]
    hw, hh = m[f"hero-{w0}"]
    sizes = "(max-width:900px) calc(100vw - 50px), (max-width:1400px) 30vw, 420px"
    srcset = ", ".join(f"assets/hub/{slug}-hero-{w}.jpg {w}w" for w in hero)
    out = (f'<img class="dshot" src="assets/hub/{slug}-hero-{hero[0]}.jpg" srcset="{srcset}" sizes="{sizes}" width="{hw}" height="{hh}" '
           f'alt="{_e(name)}: the top of the home page"{" fetchpriority=high" if first else ""} decoding="async">')
    tall = [w for w in (640, 960) if have("tall", w)]
    if tall:
        tw, th = m[f"tall-{tall[-1]}"]
        tset = ", ".join(f"assets/hub/{slug}-tall-{w}.jpg {w}w" for w in tall)
        # only a pointer device on a wide screen ever shows it, so only there is it downloaded: everyone else gets a 43 byte pixel
        out += (f'<picture><source media="(min-width:901px) and (hover:hover) and (prefers-reduced-motion:no-preference)" srcset="{tset}" sizes="{sizes}">'
                f'<img class="dtall" src="{PIXEL}" width="{tw}" height="{th}" '
                f'alt="" loading="lazy" decoding="async" style="--dur:{max(4, round(th / tw * 3.2, 1))}s"></picture>')
    return out


SHOT_RX = re.compile(r"<!--shot:([a-z0-9-]+)\|([^|>]*)\|([01])-->.*?<!--/shot-->", re.S)


def apply_shots(doc: str, out_dir: str) -> str:
    """Refill every card frame from the images now in <out>/assets/hub (called by hub_shots.py after it writes them)."""
    return SHOT_RX.sub(lambda m: f"<!--shot:{m.group(1)}|{m.group(2)}|{m.group(3)}-->{frame_inner(m.group(1), html.unescape(m.group(2)), out_dir, m.group(3) == '1')}<!--/shot-->", doc)


# ---------------------------------------------------------------- the per-URL audit, folded

ART_RX = re.compile(r'<article class="pg[^"]*"(?P<attrs>[^>]*)>.*?</article>', re.S)
SCORE_RX = re.compile(r'<b style="--g:(#[0-9a-fA-F]{3,8})">([^<]*)<i>([^<]*)</i></b>')


def compact_audit(audit_html: str, first_dir: str) -> str:
    """Turn preview_seo's one-card-per-URL list into one <details> row per URL, paged, with static links.
    Returns the input untouched when the markup is not what this expects, so a change over there cannot break the hub."""
    start_tag = '<div class="pglist" id="alist">'
    a = audit_html.find(start_tag)
    s0 = audit_html.find("<script>", a) if a >= 0 else -1
    s1 = audit_html.find("</script>", s0) if s0 >= 0 else -1
    if min(a, s0, s1) < 0:
        return audit_html
    body = audit_html[a + len(start_tag):s0]
    arts = list(ART_RX.finditer(body))
    if not arts:
        return audit_html
    rows = []
    for m in arts:
        art = m.group(0)
        attrs = m.group("attrs")
        g = lambda k: (re.search(k + r'="([^"]*)"', attrs) or [None, ""])[1]  # noqa: E731
        url = g("data-url")
        title = (re.search(r"<small>(.*?)</small>", art, re.S) or [None, ""])[1]
        build_part = art.split('class="pg-score build"', 1)
        today = SCORE_RX.search(build_part[0])
        built = SCORE_RX.search(build_part[1].split("</div>", 1)[0]) if len(build_part) > 1 else None
        fixed = re.search(r"<span>(\d+) checks fixed</span>", art)
        chip = lambda mm: f'<b class="sc" style="--g:{mm.group(1)}">{mm.group(2)}<i>{mm.group(3)}</i></b>'  # noqa: E731
        sc = (chip(today) if today else "") + (('<em class="to" aria-hidden="true"></em><span class="sr"> today, </span>' + chip(built) + '<span class="sr"> in the build</span>') if built else "")
        # the link is known at build time: no script needed to open the rebuilt page
        art = re.sub(r' data-q="[^"]*"', "", art, count=1).replace("&ndash;", "none")  # the row carries the filter text; no dashes on the hub
        art = re.sub(r'<a href="" data-rel=""[^>]*>.*?</a>', "", art)  # a page that is not rebuilt has nothing to open
        art = re.sub(r'href="([^"]*)" data-rel="[^"]*"', lambda mm: f'href="{first_dir}/{mm.group(1)}"' if first_dir else mm.group(0), art)
        rows.append(
            f'<details class="pgd"{attrs}><summary><span class="pu"><b>{url if url != "/" else "/ (home page)"}</b><small>{title}</small></span>'
            f'<span class="pt">{g("data-type")}</span><span class="ps">{sc}</span>'
            f'<span class="pf">{(fixed.group(1) + " fixed") if fixed else ("" if built else "not rebuilt")}</span></summary>{art}</details>')
    n = len(rows)
    head, rest = rows[:AUDIT_PAGE], rows[AUDIT_PAGE:]
    more = (f'<details class="pgmore"><summary>Show the other {len(rest)} pages</summary><div class="pglist">{"".join(rest)}</div></details>' if rest else "")
    tail = body[arts[-1].end():]  # the closing tags that followed the last card
    pager = (f'<div class="apager" id="apager"><button type="button" class="btn small" id="amore">Show {AUDIT_PAGE} more</button>'
             f'<button type="button" class="btn small ghost" id="aall">Show all {n}</button></div>')
    lst = f'{start_tag}{"".join(head)}{more}' + (tail.replace("</div>", "</div>" + pager, 1) if "</div>" in tail else tail + pager)
    out = audit_html[:a] + lst + audit_html[s1 + len("</script>"):]
    # one line above the filters says how the list works
    out = out.replace('<div class="afilter">', f'<p class="fine ahow">One row per page, lowest score first. Open a row for its sixteen checks and what changed. The first {AUDIT_PAGE} are shown; the spreadsheet has all {n}.</p><div class="afilter">', 1)
    return out


AUDIT_JS = r"""
(function(){var w=document.getElementById('alist');if(!w||!w.querySelector('.pgd'))return;
var more=w.querySelector('.pgmore');if(more){[].slice.call(more.querySelectorAll('.pgd')).forEach(function(r){w.insertBefore(r,more)});more.parentNode.removeChild(more)}
var $=function(i){return document.getElementById(i)},rows=[].slice.call(w.querySelectorAll('.pgd')),q=$('aq'),pb=$('aprob'),ty=$('atype'),so=$('asort'),c=$('acount'),bm=$('amore'),ba=$('aall'),STEP=__STEP__,lim=STEP;
function n(r,k){return +r.getAttribute(k)}
function f(){var s=q?q.value.trim().toLowerCase():'',p=pb&&pb.checked,tv=ty?ty.value:'',m=0,shown=0;
rows.forEach(function(r){var ok=(!s||r.getAttribute('data-q').indexOf(s)>-1)&&(!p||n(r,'data-issues')>=5)&&(!tv||r.getAttribute('data-type')===tv);if(ok)m++;var vis=ok&&m<=lim;r.hidden=!vis;if(vis)shown++});
if(c)c.textContent=m===rows.length?(shown<m?shown+' shown of '+m+' pages':m+' pages'):(shown<m?shown+' shown of ':'')+m+' matching, of '+rows.length+' pages';
if(bm){bm.hidden=shown>=m;bm.textContent='Show '+Math.min(STEP,m-shown)+' more'}if(ba){ba.hidden=shown>=m;ba.textContent='Show all '+m}}
function srt(){var v=so?so.value:'score-asc';rows.sort(function(a,b){if(v==='score-asc')return n(a,'data-score')-n(b,'data-score');if(v==='score-desc')return n(b,'data-score')-n(a,'data-score');if(v==='words')return n(a,'data-words')-n(b,'data-words');return a.getAttribute('data-url').localeCompare(b.getAttribute('data-url'))});rows.forEach(function(r){w.appendChild(r)});f()}
function reset(){lim=STEP;f()}
if(q)q.addEventListener('input',reset);if(pb)pb.addEventListener('change',reset);if(ty)ty.addEventListener('change',reset);if(so)so.addEventListener('change',function(){lim=STEP;srt()});
if(bm)bm.addEventListener('click',function(){var k=lim;lim+=STEP;f();var v=rows.filter(function(r){return !r.hidden})[k];if(v)v.querySelector('summary').focus()});
if(ba)ba.addEventListener('click',function(){lim=1e9;f()});
f()})();
"""

HUB_JS = r"""
(function(){var d=document;
/* side by side: pictures first, the live pages only when asked for */
var fr=[].slice.call(d.querySelectorAll('.frames .scale')),sel=d.getElementById('cmp'),go=d.getElementById('cmpgo'),live=false;
function fit(){fr.forEach(function(s){var f=s.querySelector('iframe');if(f)f.style.transform='scale('+(s.clientWidth/1440)+')'})}
function load(){var pg=sel?sel.value:'index.html';fr.forEach(function(s){var f=s.querySelector('iframe');if(!f){f=d.createElement('iframe');f.width=1440;f.height=900;f.title=s.getAttribute('data-name')+' preview';f.setAttribute('tabindex','-1');s.appendChild(f)}f.src=s.getAttribute('data-dir')+'/'+pg;s.classList.add('live')});
[].slice.call(d.querySelectorAll('.frames .open')).forEach(function(a){a.href=a.getAttribute('data-dir')+'/'+pg});live=true;fit();if(go)go.hidden=true}
if(fr.length){window.addEventListener('resize',fit);if(go)go.addEventListener('click',load);if(sel)sel.addEventListener('change',load);if(!go)load()}
/* every page: a text filter */
var eq=d.getElementById('eq'),ev=d.getElementById('everylist');
if(eq&&ev){var er=[].slice.call(ev.querySelectorAll('.row')),em=ev.querySelector('details'),ec=d.getElementById('ecount');eq.addEventListener('input',function(){var s=eq.value.trim().toLowerCase(),k=0;if(s&&em)em.open=true;er.forEach(function(r){var ok=!s||r.textContent.toLowerCase().indexOf(s)>-1;r.hidden=!ok;if(ok)k++});if(ec)ec.textContent=s?k+' of '+er.length+' pages':''})}
})();
"""

CSS = r"""
:root{--bg:#ffffff;--bg-alt:#f4f5f3;--fg:#14171a;--muted:#525a61;--border:#e1e4e2;--accent:__ACCENT__;--ink:__INK__;--chrome:__DARK__;--on-accent:__BTNFG__;--gold:__ONDARK__;
--head:__HEAD__;--body:__BODY__;--r:16px}
*{box-sizing:border-box}html{scroll-padding-top:84px;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--chrome);color:var(--fg);font:16px/1.62 var(--body);-webkit-font-smoothing:antialiased}
a{color:var(--ink)}img{max-width:100%}
:focus-visible{outline:3px solid var(--ink);outline-offset:3px;border-radius:6px}
.dk :focus-visible,.top :focus-visible,footer :focus-visible{outline-color:var(--gold)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.skip{position:absolute;top:-200px;left:8px;background:var(--accent);color:var(--on-accent);padding:10px 16px;border-radius:8px;z-index:50;font-weight:700}.skip:focus{top:8px}
.wrap{max-width:1128px;margin:0 auto;padding:0 24px}.wrap.wide,.hero .wrap{max-width:1368px}
/* nav */
.top{background:rgba(10,11,13,.86);-webkit-backdrop-filter:saturate(1.4) blur(14px);backdrop-filter:saturate(1.4) blur(14px);position:sticky;top:0;z-index:30;border-bottom:1px solid rgba(255,255,255,.08)}
.top .wrap{max-width:1368px;display:flex;align-items:center;justify-content:space-between;gap:20px;min-height:64px}
.top .logo{display:flex;align-items:center;flex-shrink:0}.top .logo img{height:32px;width:auto;display:block}
.top nav{display:flex;gap:2px;min-width:0;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}.top nav::-webkit-scrollbar{display:none}
.top nav a{color:rgba(255,255,255,.78);text-decoration:none;font:500 13.5px/1 var(--head);padding:0 11px;border-radius:999px;min-height:44px;display:inline-flex;align-items:center;white-space:nowrap}
.top nav a:hover{color:#fff;background:rgba(255,255,255,.09)}
@media(max-width:1180px){.top .wrap{flex-direction:column;align-items:stretch;gap:0;padding-top:12px}.top nav{margin:0 -24px;padding:0 14px;-webkit-mask-image:linear-gradient(90deg,transparent,#000 14px,#000 calc(100% - 28px),transparent);mask-image:linear-gradient(90deg,transparent,#000 14px,#000 calc(100% - 28px),transparent)}html{scroll-padding-top:112px}}
@media(max-width:900px){.top{position:static}html{scroll-padding-top:12px}}
/* type */
section{padding:88px 0;background:var(--bg);color:var(--fg)}
section.tint{background:var(--bg-alt)}
.dk{--bg:__DARK__;--bg-alt:#131519;--fg:#f3f4f2;--muted:#aab0b6;--border:rgba(255,255,255,.13);--ink:var(--gold);background:var(--bg);color:var(--fg)}
.eyebrow{font:700 12.5px/1.3 var(--head);letter-spacing:.16em;text-transform:uppercase;color:var(--ink);margin:0 0 16px;display:flex;align-items:center;gap:10px}
.eyebrow::before{content:"";width:22px;height:2px;background:var(--accent);flex-shrink:0}
h1,h2,h3,h4{font-family:var(--head);color:var(--fg)}
h1{font-size:clamp(34px,4.4vw,58px);line-height:1;letter-spacing:-.035em;font-weight:800;margin:0;text-wrap:balance}
h2{font-size:clamp(27px,3.2vw,40px);line-height:1.08;letter-spacing:-.028em;font-weight:800;margin:0 0 14px;text-wrap:balance;max-width:24ch}
h3,.h3{font-size:21px;line-height:1.25;margin:0 0 8px;letter-spacing:-.015em;font-weight:700}h4,.h4{font-size:16px;line-height:1.3;margin:0 0 6px;font-weight:700}
.lead{color:var(--muted);max-width:64ch;margin:0 0 32px;font-size:17.5px;line-height:1.6}
.fine{font-size:14px;color:var(--muted)}
ul{margin:0;padding-left:18px}li{margin:8px 0}li::marker{color:var(--ink)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:48px;padding:11px 20px;background:var(--accent);color:var(--on-accent);border-radius:10px;text-decoration:none;font:700 15px/1.2 var(--head);border:0;cursor:pointer}
.btn:hover{filter:brightness(.94)}.btn.small{min-height:44px;padding:9px 14px;font-size:14px}.btn.ghost{background:transparent;border:1px solid var(--border);color:var(--fg)}.btn.ghost:hover{border-color:var(--ink);filter:none}
/* hero */
.hero{position:relative;padding:40px 0 0;overflow:hidden;isolation:isolate}
.hero::before{content:"";position:absolute;inset:0;z-index:-1;background:
 radial-gradient(900px 520px at 86% -8%,color-mix(in srgb,var(--accent) 20%,transparent),transparent 62%),
 radial-gradient(700px 480px at -6% 46%,rgba(255,255,255,.055),transparent 60%),
 linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px) 0 0/100% 72px,
 linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px) 0 0/72px 100%;
 -webkit-mask-image:linear-gradient(#000 55%,transparent);mask-image:linear-gradient(#000 55%,transparent)}
.hero-h{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:28px 64px;align-items:end;margin-bottom:28px}
.hero-h .eyebrow{grid-column:1/-1;margin:0}
.hero h1 em{font-style:normal;color:var(--gold)}
.hero .sub{margin:0;color:#c5cacf;font-size:16.5px;line-height:1.55;max-width:56ch;padding-bottom:4px}
.dcards{display:grid;grid-template-columns:repeat(__N__,minmax(0,1fr));gap:22px}
.dcard{position:relative;display:flex;flex-direction:column;background:linear-gradient(180deg,rgba(255,255,255,.065),rgba(255,255,255,.025));border:1px solid rgba(255,255,255,.12);border-radius:20px;padding:12px 12px 0;transition:transform .35s cubic-bezier(.2,.7,.2,1),border-color .25s,box-shadow .35s}
.dframe{border-radius:11px;overflow:hidden;background:#1b1e23;box-shadow:0 0 0 1px rgba(255,255,255,.1)}
.dbar{display:flex;align-items:center;gap:6px;height:26px;padding:0 10px;background:#1b1e23}.dbar i{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,.2)}
.dbar span{margin-left:8px;font:500 11px/1 var(--head);color:rgba(255,255,255,.62);letter-spacing:.02em;background:rgba(255,255,255,.07);border-radius:999px;padding:4px 10px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.dview{position:relative;aspect-ratio:16/10;overflow:hidden;background:#111317;container-type:size}
.dview img{position:absolute;left:0;top:0;width:100%;height:auto;display:block}
.dtall{display:none}
.dnone{position:absolute;inset:0;display:grid;place-items:center;font:800 clamp(28px,4vw,44px)/1 var(--head);letter-spacing:-.03em;color:rgba(255,255,255,.2);background:linear-gradient(135deg,rgba(255,255,255,.07),transparent 60%)}
.dbody{display:flex;flex-direction:column;flex:1;padding:20px 12px 22px}
.dname{font-size:27px;line-height:1.1;letter-spacing:-.03em;margin:0;max-width:none;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.rec{font:700 11.5px/1 var(--head);letter-spacing:.08em;text-transform:uppercase;color:var(--gold);border:1px solid var(--gold);border-radius:999px;padding:5px 10px}
.drole{margin:8px 0 0;color:#c5cacf;font-size:15px;line-height:1.5}
.chips{list-style:none;display:flex;flex-wrap:wrap;gap:6px;padding:0;margin:14px 0 18px}.dk .chips li{margin:0;font:600 12px/1 var(--head);letter-spacing:.03em;color:#d7dbdf;border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:7px 11px}.dtop{display:flex;align-items:center;justify-content:space-between;gap:12px}.mood{font:800 11.5px/1 var(--head);letter-spacing:.1em;text-transform:uppercase;background:var(--gold);color:#0a0b0d;border-radius:999px;padding:7px 11px;white-space:nowrap}.drole strong{color:#fff;font-weight:700}
.dopen{margin-top:auto;display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:52px;padding:12px 18px;background:var(--accent);color:var(--on-accent);border-radius:12px;text-decoration:none;font:800 16px/1.2 var(--head);letter-spacing:-.01em}
.dopen::after{content:"";position:absolute;inset:0;border-radius:20px}
.dopen svg{flex-shrink:0;transition:transform .3s cubic-bezier(.2,.7,.2,1)}
.dopen:focus-visible{outline:0}.dcard:has(.dopen:focus-visible){outline:3px solid var(--gold);outline-offset:4px}
@media(hover:hover){.dcard:hover{transform:translateY(-6px);border-color:color-mix(in srgb,var(--gold) 70%,transparent);box-shadow:0 30px 70px -30px rgba(0,0,0,.9),0 0 0 1px color-mix(in srgb,var(--gold) 35%,transparent)}.dcard:hover .dopen svg{transform:translateX(4px)}}
@media(hover:hover) and (min-width:901px) and (prefers-reduced-motion:no-preference){
 .dtall{display:block;transition:transform 1s cubic-bezier(.3,0,.2,1)}
 .dcard:hover .dtall,.dcard:focus-within .dtall{transform:translateY(calc(-100% + 100cqh));transition:transform var(--dur,9s) cubic-bezier(.35,0,.3,1) .35s}}
@media(prefers-reduced-motion:reduce){.dcard,.dopen svg{transition:none}.dcard:hover{transform:none}}
.same{margin-top:44px;padding:30px 0 34px;border-top:1px solid rgba(255,255,255,.12);display:grid;grid-template-columns:minmax(0,1fr) auto;gap:20px 56px;align-items:center}
.same h2{font-size:clamp(21px,2vw,26px);letter-spacing:-.02em;margin:0 0 6px;max-width:none}.same p{margin:0;color:#b9bfc5;font-size:15.5px;max-width:68ch}
.pill{display:flex;align-items:center;gap:3px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);border-radius:999px;padding:6px 8px 6px 16px;font:500 13px/1 var(--head);color:#fff;white-space:nowrap}
.pill small{font-size:13px;color:rgba(255,255,255,.66);margin-right:8px}.pill span{padding:9px 12px;border-radius:999px}.pill span.on{background:rgba(255,255,255,.18);box-shadow:inset 0 0 0 1px rgba(255,255,255,.3)}
/* how to choose, recommendation */
.whys{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0 36px}.why{padding:20px 0 4px;border-top:2px solid var(--fg)}.why p{margin:6px 0 0;color:var(--muted);font-size:15.5px}
.pickbox .change{margin-top:26px}
.change{background:var(--bg-alt);border:1px solid var(--border);border-radius:var(--r);padding:20px 24px;margin-top:24px;font-size:15.5px}section.tint .change{background:var(--bg)}
.alts{display:grid;grid-template-columns:1fr 1fr;gap:16px}.alt{display:block;border:1px solid var(--border);border-radius:var(--r);padding:22px 24px;text-decoration:none;color:inherit;background:var(--bg-alt);transition:border-color .2s}.alt:hover{border-color:var(--ink)}.alt p{color:var(--muted);font-size:15px;margin:0 0 12px}.alt span{font:700 14px/1 var(--head);color:var(--ink)}
.looks{display:grid;grid-template-columns:repeat(__N__,minmax(0,1fr));gap:22px}
.look{background:var(--bg);border:1px solid var(--border);border-radius:20px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 1px 2px rgba(10,11,13,.04),0 18px 40px -28px rgba(10,11,13,.35)}
section.tint .look{background:#fff}
.look-type{height:210px;display:flex;align-items:center;padding:18px 22px;border-bottom:1px solid var(--border);overflow:hidden}
.look-type img{max-width:100%;max-height:100%;width:auto;height:auto;display:block}.look-type span{font:800 44px/1 var(--head);letter-spacing:-.03em}
.look-b{padding:24px 26px 26px;display:flex;flex-direction:column;flex:1}
.look h3{font-size:24px;letter-spacing:-.025em;margin:0 0 18px;display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}.look h3 small{font:600 14px/1.3 var(--head);letter-spacing:0;color:var(--muted)}
.sw{list-style:none;padding:0;margin:0 0 20px;display:flex;gap:8px}.sw li{margin:0;flex:1;min-width:0}.sw i{display:block;height:46px;border-radius:10px;box-shadow:inset 0 0 0 1px rgba(10,11,13,.14)}
.sw span{display:block;margin-top:7px;font:600 11px/1.3 var(--head);color:var(--muted);letter-spacing:.02em}.sw b{display:block;font-weight:600;color:var(--fg);font-size:10.5px;letter-spacing:.03em}
.diff{margin:0 0 18px;border-top:1px solid var(--border)}.diff div{display:grid;grid-template-columns:96px 1fr;gap:12px;padding:10px 0;border-bottom:1px solid var(--border);align-items:baseline}.diff dt{font:700 11.5px/1.3 var(--head);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}.diff dd{margin:0;font:700 15px/1.35 var(--head);color:var(--fg)}
.look p{margin:0 0 20px;color:var(--muted);font-size:15px;line-height:1.55}
.look-open{margin-top:auto;display:inline-flex;align-items:center;gap:8px;min-height:44px;font:800 15px/1 var(--head);color:var(--fg);text-decoration:none;align-self:flex-start;border-bottom:3px solid var(--accent)}.look-open svg{transition:transform .3s}.look-open:hover svg{transform:translateX(4px)}
/* side by side */
.cmp-bar{display:none;gap:12px;align-items:center;margin:0 0 22px;flex-wrap:wrap}.js .cmp-bar{display:flex}
.cmp-bar label{font:600 14px/1 var(--head)}
select,input[type=search]{font:inherit;font-size:16px;padding:10px 12px;border:1px solid var(--border);border-radius:10px;background:var(--bg);color:var(--fg);min-height:44px;max-width:100%}
.frames{display:grid;grid-template-columns:repeat(__N__,minmax(0,1fr));gap:18px}.frames figure{margin:0}.frames figcaption{font:700 14px/1 var(--head);margin:0 0 10px}
.frames .scale{width:100%;aspect-ratio:16/10;overflow:hidden;border:1px solid var(--border);border-radius:12px;background:#fff;position:relative}
.frames .scale img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:top;display:block}.frames .scale.live img{display:none}
.frames iframe{width:1440px;height:900px;border:0;transform-origin:0 0;position:absolute;left:0;top:0;pointer-events:none}
.frames .open{display:inline-flex;align-items:center;min-height:44px;font:700 14px/1 var(--head);text-decoration:none;color:var(--ink)}
.cmp-note{display:none;color:var(--muted);font-size:15px}
/* search */
.two{display:grid;grid-template-columns:1fr 1fr;gap:48px}
.stiles{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:26px}.stile{border:1px solid var(--border);border-radius:var(--r);padding:20px 22px;background:var(--bg-alt)}section.tint .stile,section.tint .step,section.tint .alt,section.tint .fnd{background:var(--bg)}.stile b{display:block;font:800 36px/1 var(--head);letter-spacing:-.03em;color:var(--fg)}.stile span{display:block;margin-top:10px;font-size:13.5px;line-height:1.45;color:var(--muted)}
.asof{font-size:13px;color:var(--muted);font-weight:400;margin-left:8px;letter-spacing:0}
.tblwrap{overflow-x:auto;margin-top:14px}table.seo{width:100%;border-collapse:collapse;font-size:14.5px}table.seo th,table.seo td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--border);vertical-align:top}table.seo th{font:700 12.5px/1.3 var(--head);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}table.seo code{font-size:13px;background:var(--bg-alt);padding:2px 6px;border-radius:6px}
/* lists that fold */
.fold>summary,.pgmore>summary{cursor:pointer;display:inline-flex;align-items:center;gap:10px;min-height:48px;padding:0 18px;margin-top:18px;border:1px solid var(--border);border-radius:10px;font:700 14.5px/1 var(--head);color:var(--fg);list-style:none;background:var(--bg)}
.fold>summary::-webkit-details-marker,.pgmore>summary::-webkit-details-marker,.pgd>summary::-webkit-details-marker{display:none}
.fold>summary::before,.pgmore>summary::before{content:"+";font-size:18px;color:var(--ink);font-weight:800}.fold[open]>summary::before,.pgmore[open]>summary::before{content:"\2212"}
.fold>summary:hover,.pgmore>summary:hover{border-color:var(--ink)}
.confirm{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:12px 16px;counter-reset:cf __CF0__}.confirm li{counter-increment:cf;margin:0;padding:18px 20px 18px 58px;position:relative;border:1px solid var(--border);border-radius:var(--r);background:var(--bg);font-size:15px;line-height:1.55}
.confirm li::before{content:counter(cf);position:absolute;left:18px;top:17px;font:800 15px/1.6 var(--head);color:var(--ink);min-width:26px}
.fold .confirm{margin-top:12px}
.efilter{display:none;gap:12px;align-items:center;margin:0 0 18px;flex-wrap:wrap}.js .efilter{display:flex}.efilter input{flex:1;min-width:220px;max-width:420px}.efilter span{font-size:14px;color:var(--muted)}
.every{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0 40px}.every .row{min-width:0;display:flex;align-items:center;justify-content:space-between;gap:14px;min-height:46px;border-top:1px solid var(--border);font-size:15px}.every .row[hidden]{display:none}.every .pn{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.every .links{display:flex;gap:2px;flex-shrink:0}.every .links a{display:inline-flex;align-items:center;min-height:40px;padding:0 10px;border-radius:8px;text-decoration:none;color:var(--ink);font:700 13px/1 var(--head)}.every .links a:hover{background:var(--bg-alt)}
.fold .every{margin-top:12px}
/* heard */
.dk .two h2{font-size:clamp(24px,2.4vw,31px)}.dk li{color:#dfe2e4;font-size:15.5px}.dk .lead{color:var(--muted)}
/* plan */
.plan{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;counter-reset:st}.step{counter-increment:st;position:relative;background:var(--bg-alt);border:1px solid var(--border);border-radius:var(--r);padding:24px 22px 26px}.step::before{content:counter(st,decimal-leading-zero);display:block;font:800 13px/1 var(--head);letter-spacing:.08em;color:var(--muted);margin-bottom:16px}
.when{display:inline-block;font:800 19px/1.2 var(--head);letter-spacing:-.015em;color:var(--fg);border-bottom:3px solid var(--accent);padding-bottom:4px}.step p{margin:14px 0 0;font-size:15.5px;line-height:1.55;color:var(--fg)}
/* your turn */
#turn{padding:96px 0 72px;position:relative;overflow:hidden;isolation:isolate}#turn::before{content:"";position:absolute;inset:0;z-index:-1;background:radial-gradient(800px 420px at 12% 110%,color-mix(in srgb,var(--accent) 18%,transparent),transparent 62%)}
#turn h2{font-size:clamp(32px,4.4vw,56px);letter-spacing:-.035em;max-width:18ch}.turn .btns{display:flex;gap:12px;flex-wrap:wrap}.turn .btn{min-height:54px;padding:14px 26px;font-size:16px}.turn .btn.ghost{color:#fff;border-color:rgba(255,255,255,.3)}
footer{background:var(--chrome);color:#aab0b6;font-size:13.5px;padding:0 0 64px}footer .wrap{border-top:1px solid rgba(255,255,255,.12);padding-top:26px}footer p{margin:0;max-width:80ch}
@media(max-width:1100px){.hero-h{grid-template-columns:1fr;gap:18px}.hero .sub{max-width:60ch}.same{grid-template-columns:1fr}.pill{justify-self:start}}
@media(max-width:900px){section{padding:60px 0}.hero{padding-top:36px}.looks{grid-template-columns:minmax(0,1fr)}.look-type{height:auto;min-height:150px}.dcards,.plan,.whys,.alts,.two,.confirm,.every{grid-template-columns:minmax(0,1fr)}.dcards{gap:18px}.two{gap:40px}.why{padding-bottom:16px}.frames,.cmp-bar,.js .cmp-bar{display:none}.cmp-note{display:block}.hero-h{margin-bottom:28px}.same{margin-top:32px}}
@media(max-width:900px){.dcards{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -24px;padding:4px 24px 14px;scroll-padding:0 24px;scrollbar-width:none;-webkit-overflow-scrolling:touch}.dcards::-webkit-scrollbar{display:none}.dcard{flex:0 0 min(82%,360px);scroll-snap-align:start}.dname{font-size:24px}.same{margin-top:18px}}
@media(max-width:767px){.stiles,.stiles.eight{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.stile{padding:16px;min-width:0}.stile span{overflow-wrap:anywhere;hyphens:auto}.stile b{font-size:clamp(22px,7.4vw,30px);overflow-wrap:anywhere}}
@media(max-width:420px){.wrap{padding:0 18px}.dcards{margin:0 -18px;padding:4px 18px 14px;scroll-padding:0 18px}.top nav{margin:0 -18px}.pill{font-size:12px;padding-left:12px}.pill span{padding:8px 9px}.pill small{margin-right:4px}}
"""

# after preview_seo's own CSS: the folded audit list and small corrections so its blocks sit in this page's type
CSS_AFTER = r"""
.fnd{border-left-width:4px;border-radius:var(--r);min-width:0}.fnd>*{min-width:0;overflow-wrap:anywhere}.fnds{grid-template-columns:minmax(0,1fr)}@media(max-width:420px){.fnd{grid-template-columns:30px minmax(0,1fr);padding:16px 14px}.fnd .rank{font-size:24px}}.fnd .rank{font-family:var(--head);color:var(--fg)}
.cmpbox{background:__DARK__;border-radius:20px;padding:30px 32px}.cmp-row .build{font-family:var(--head)}
.sitechk li{border-radius:10px}
.ahow{margin:28px 0 -14px;max-width:80ch}
html:not(.js) .afilter>input,html:not(.js) .afilter>select,html:not(.js) .afilter>label,html:not(.js) #acount,html:not(.js) .apager{display:none}
.pglist{gap:8px}
.pgd{border:1px solid var(--border);border-radius:12px;background:var(--bg)}.pgd[hidden]{display:none}
.pgd>summary{display:grid;grid-template-columns:minmax(0,1fr) 110px 132px 76px 16px;gap:16px;align-items:center;padding:8px 16px;min-height:54px;cursor:pointer;list-style:none;border-radius:12px}
.pgd>summary::after{content:"";width:8px;height:8px;border-right:2px solid var(--muted);border-bottom:2px solid var(--muted);transform:rotate(45deg);justify-self:center;margin-top:-4px}.pgd[open]>summary::after{transform:rotate(-135deg);margin-top:4px}
.pgd>summary:hover{background:var(--bg-alt)}.pgd[open]{border-color:var(--fg)}
.pu{min-width:0}.pu b{display:block;font:700 14.5px/1.35 var(--head);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.pu small{display:block;font-size:13px;line-height:1.35;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pt{font:700 12px/1.2 var(--head);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.ps{display:flex;align-items:center;gap:8px;white-space:nowrap}.sc{font:800 19px/1 var(--head);letter-spacing:-.02em;color:var(--g)}.sc i{font-style:normal;font-size:12px;margin-left:4px;color:#fff;background:var(--g);border-radius:5px;padding:2px 5px;vertical-align:2px;letter-spacing:0}
.ps .to{width:14px;height:2px;background:var(--muted);position:relative;flex-shrink:0}.ps .to::after{content:"";position:absolute;right:-2px;top:-3px;border:4px solid transparent;border-left-color:var(--muted)}
.pf{font-size:13px;color:var(--muted);white-space:nowrap}
.pgd .pg{border:0;border-top:1px solid var(--border);border-radius:0 0 12px 12px;background:var(--bg-alt)}
.pgmore>.pglist{margin-top:10px}
.apager{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px;padding:0}.apager [hidden]{display:none}
.afilter{margin:26px 0 16px}
@media(max-width:760px){.pgd>summary{grid-template-columns:minmax(0,1fr) auto 16px;gap:4px 12px;padding:10px 14px}.pgd>summary .pu{grid-column:1/3}.pgd>summary .pt{grid-column:1;grid-row:2}.pgd>summary .ps{grid-column:2;grid-row:2}.pgd>summary .pf{display:none}.pgd>summary::after{grid-column:3;grid-row:1/3}.afilter #acount{margin-left:0;width:100%}}
"""

ARROW = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 10h11M10.5 5l5 5-5 5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def hub(content, themes, recommend, base, roles, standard, client_tokens, out_dir=None, seo=None):
    b = content["brand"]
    pitch = content.get("pitch", {})
    client = content["client"]
    n = len(themes)
    roles = load_roles(content, themes, roles)
    accent = b["accent"]
    btn_fg = "#ffffff" if reskin.relative_luminance(accent) < 0.3 else "#0a0b0d"
    ink = reskin.darken_until(accent, "#f4f5f3")
    domain = content.get("domain_hint") or ""
    pages = content["pages"]
    fonts = local_fonts(out_dir)
    head = "'Inter','Inter Fallback',system-ui,-apple-system,'Segoe UI',sans-serif" if fonts else "Inter,system-ui,-apple-system,'Segoe UI',sans-serif"
    body = "'Open Sans','Open Sans Fallback',system-ui,-apple-system,'Segoe UI',sans-serif" if fonts else head
    ds_link = '<a href="design-system.html">Design system</a>' if out_dir and os.path.exists(os.path.join(out_dir, "design-system.html")) else ""

    def pname(pg):
        return "Home" if pg["file"] == "index.html" else pg["title"].split("|")[0].strip()

    # ---- the cards
    man = _manifest(out_dir) if out_dir else {}
    cards, looks = [], []
    for i, t in enumerate(themes):
        css, _tok = client_tokens(t, b)
        nat = reskin.parse_native(css)
        lum = reskin.relative_luminance(nat.get("--bg", "#ffffff"))
        ground = "Dark" if lum < 0.18 else ("Warm paper" if lum < 0.93 else "White")
        short, slug = _short(t), _slug(t)
        rec = '<span class="rec">Our recommendation</span>' if t == recommend else ""
        look = (man.get(slug) or {}).get("look")
        fx = facts(content, t, nat, ground, look)
        looks.append((t, fx, look, (man.get(slug) or {}).get("type")))
        tags = "".join(f"<li>{_e(fx[k])}</li>" for k in ("type", "ground") if fx[k])
        mood = f'<span class="mood">{_e(fx["mood"])}</span>' if fx["mood"] else ""
        # "the Panel: cinematic, industrial black. The home page is ..." reads as a name for the idea, then one line about it
        role = _role(roles, t)
        tag, _, rest = role.partition(": ")
        if rest and len(tag) <= 36:
            lead = f'<strong>{_e(_sentence(tag)[:-1])}.</strong> '
            role = rest
        else:
            lead = ""
        first = re.split(r"(?<=[.!?])\s+", role.strip(), maxsplit=1)[0]
        cards.append(
            f'<article class="dcard"><div class="dframe"><div class="dbar" aria-hidden="true"><i></i><i></i><i></i><span>{_e(domain or client)}</span></div>'
            f'<div class="dview"><!--shot:{slug}|{_e(short)}|{1 if i == 0 else 0}-->{frame_inner(slug, short, out_dir, i == 0)}<!--/shot--></div></div>'
            f'<div class="dbody"><div class="dtop"><h2 class="dname">{_e(short)}{rec}</h2>{mood}</div><p class="drole">{lead}{_e(_sentence(first))}</p>'
            f'{f"<ul class=chips aria-label=Character>{tags}</ul>" if tags else ""}'
            f'<a class="dopen" href="{slug}/index.html" target="_blank" rel="noopener"><span>Open {_e(short)}<span class="sr">, the whole site, in a new tab</span></span>{ARROW}</a></div></article>')

    count = WORDS.get(n, str(n))
    headline = pitch.get("hub_headline") or (f"{count} directions for <em>{_e(domain)}</em>." if domain else f"{count} directions for <em>{_e(client)}</em>.")
    if pitch.get("hub_headline"):
        headline = _e(headline)
    default_intro = "The words and the pages are the same in all of them. What differs is the personality. Open each one, and tell us which feels like you."
    sub = pitch.get("hub_sub") or (pitch.get("choice_intro") if recommend else pitch.get("choose_intro")) or default_intro
    names = [_short(t) for t in themes]
    pill = '<div class="pill" aria-hidden="true"><small>Directions</small>' + "".join(f'<span{" class=on" if i == 0 else ""}>{_e(x)}</span>' for i, x in enumerate(names)) + "</div>"
    same = (f'<div class="same"><div><h2>Same pages, same words, {count.lower()} personalities</h2>'
            f'<p>Every one of the {len(pages)} pages is built in all {count.lower()}, with the same copy. Open any direction, then use the Directions tab at the edge of the page to flip between them without losing your place.</p></div>{pill}</div>')

    # ---- how to choose, or the recommendation
    pick = recommend or themes[0]
    pick_short, pick_slug = _short(pick), _slug(pick)
    alts = ""
    if recommend:
        reasons = "".join(f'<div class="why"><h3 class="h4">{_e(h)}</h3><p>{_e(t)}</p></div>' for h, t in pitch.get("pick_reasons", []))
        alts = "".join(f'<a class="alt" href="{_slug(t)}/index.html" target="_blank" rel="noopener"><h3 class="h4">{_e(_short(t))}</h3><p>{_e(why)}</p><span>Open {_e(_short(t))}</span></a>'
                       for t, why in pitch.get("alternatives", []))
        choose = (f'<section id="pick"><div class="wrap pickbox"><p class="eyebrow">Our recommendation</p><h2>We would build {_e(pick_short)}</h2><p class="lead">{_e(_sentence(_role(roles, pick)))}</p>'
                  f'<div class="whys">{reasons}</div>' + (f'<div class="change"><strong>The one thing we would change:</strong> {_e(pitch.get("pick_change", ""))}</div>' if pitch.get("pick_change") else "")
                  + f'<p style="margin:26px 0 0"><a class="btn" href="{pick_slug}/index.html" target="_blank" rel="noopener">Open {_e(pick_short)}</a></p>'
                  + (f'<h3 class="h3" style="margin-top:44px">The alternatives</h3><div class="alts" style="margin-top:14px">{alts}</div>' if alts else "") + '</div></section>')
    else:
        cr = pitch.get("choose_reasons", [])

        def reason(short):
            for h, tx in cr:
                if h.lower().startswith(short.lower()):
                    return re.sub(r"^[\s:,.-]+", "", h[len(short):]).strip(), tx
            return "", ""
        if all(lk for _t, _f, lk, _ty in looks):
            cols = []
            for t, fx, lk, ty in looks:
                short, slug = _short(t), _slug(t)
                sw, seen = [], set()
                for label, key in (("Hero", "hero_ground"), ("Page", "page_ground"), ("Headline", "heading_color"), ("Text", "text_color"), ("Accent", "accent")):
                    v = (lk.get(key) or "").lower()
                    if v and v not in seen:
                        seen.add(v)
                        sw.append(f'<li><i style="background:{_e(v)}"></i><span>{label}<b>{_e(v.upper())}</b></span></li>')
                hg = lk.get("hero_ground") or "#ffffff"
                sample = (f'<img src="assets/hub/{slug}-type.jpg" width="{ty[0]}" height="{ty[1]}" loading="lazy" decoding="async" alt="{_e(short)} headline, set in {_e(lk.get("heading_face") or "its own type")}">'
                          if ty and os.path.exists(os.path.join(out_dir, "assets", "hub", f"{slug}-type.jpg")) else f'<span style="color:{_e(lk.get("heading_color") or "#111")}">{_e(short)}</span>')
                rh, rt = reason(short)
                rows = "".join(f"<div><dt>{k}</dt><dd>{_e(v)}</dd></div>" for k, v in (("Mood", fx["mood"]), ("Headlines", lk.get("heading_face") or fx["type"]), ("Ground", fx["ground"])) if v)
                cols.append(
                    f'<article class="look"><div class="look-type" style="background:{_e(hg)}">{sample}</div><div class="look-b">'
                    f'<h3>{_e(short)}{f"<small>{_e(_sentence(rh)[:-1])}</small>" if rh else ""}</h3>'
                    f'<ul class="sw" aria-label="{_e(short)} colours">{"".join(sw)}</ul><dl class="diff">{rows}</dl>'
                    f'{f"<p>{_e(rt)}</p>" if rt else ""}<a class="look-open" href="{slug}/index.html" target="_blank" rel="noopener">Open {_e(short)}{ARROW}</a></div></article>')
            choose = (f'<section id="choose" class="tint"><div class="wrap wide"><p class="eyebrow">How to choose</p><h2>{_e(pitch.get("choose_heading", "Your call."))}</h2>'
                      f'<p class="lead">The headline, the colours and the ground of each direction, taken from its home page as built.</p><div class="looks">{"".join(cols)}</div></div></section>')
        else:
            creasons = "".join(f'<div class="why"><h3 class="h4">{_e(h)}</h3><p>{_e(t)}</p></div>' for h, t in cr)
            choose = (f'<section id="choose"><div class="wrap"><p class="eyebrow">How to choose</p><h2>{_e(pitch.get("choose_heading", "Your call."))}</h2>'
                      f'<div class="whys" style="margin-top:30px">{creasons}</div></div></section>') if creasons else ""

    # ---- side by side
    posters = all((man.get(_slug(t)) or {}).get("hero-960") or (man.get(_slug(t)) or {}).get("hero-640") for t in themes)
    page_opts = "".join(f'<option value="{_e(pg["file"])}">{_e(pname(pg))}</option>' for pg in pages)
    frames = ""
    for t in themes:
        short, slug = _short(t), _slug(t)
        if posters:
            ws = [w for w in (640, 960) if f"hero-{w}" in man[slug]]
            pw, ph = man[slug][f"hero-{ws[-1]}"]
            # same files and the same srcset as the cards above, so nothing is downloaded twice
            inner = (f'<img src="assets/hub/{slug}-hero-{ws[0]}.jpg" srcset="{", ".join(f"assets/hub/{slug}-hero-{w}.jpg {w}w" for w in ws)}" sizes="(max-width:1400px) 30vw, 420px" '
                     f'alt="{_e(short)} home page" width="{pw}" height="{ph}" loading="lazy" decoding="async">')
        else:
            inner = f'<iframe title="{_e(short)} preview" loading="lazy" src="{slug}/index.html" width="1440" height="900" tabindex="-1"></iframe>'
        frames += (f'<figure><figcaption>{_e(short)}</figcaption><div class="scale" data-dir="{slug}" data-name="{_e(short)}">{inner}</div>'
                   f'<a class="open" href="{slug}/index.html" target="_blank" rel="noopener" data-dir="{slug}">Open {_e(short)} full size</a></figure>')
    go = '<button type="button" class="btn small" id="cmpgo">Load the live pages</button>' if posters else ""
    compare = (f'<section id="compare"><div class="wrap wide"><p class="eyebrow">Side by side</p><h2>The same page, all {count.lower()} at once</h2>'
               f'<div class="cmp-bar"><label for="cmp">Pick a page</label><select id="cmp">{page_opts}</select>{go}</div>'
               f'<p class="cmp-note">Side by side needs a wider screen. On a phone, open each direction from the cards above.</p><div class="frames">{frames}</div></div></section>')

    # ---- search and the per-URL audit
    search_html = ""
    sr = pitch.get("search")
    if seo:
        search_html = seo["search"].replace('<section id="search">', '<section id="search" class="tint">', 1) + "\n" + compact_audit(seo["audit"], seo.get("first_dir", ""))
    elif sr:
        tiles = "".join(f'<div class="stile"><b>{_e(v)}</b><span>{_e(l)}</span></div>' for v, l in sr.get("today_stats", []))
        today = "".join(f"<li>{_e(x)}</li>" for x in sr.get("today", []))
        after = "".join(f"<li>{_e(x)}</li>" for x in sr.get("after", []))
        keep = "".join(f"<tr><td><code>{_e(o)}</code></td><td><code>{_e(nw)}</code></td><td>{_e(w)}</td></tr>" for o, nw, w in sr.get("keep", []))
        keep_tbl = (f'<div class="tblwrap" tabindex="0"><table class="seo"><thead><tr><th scope="col">Today</th><th scope="col">After launch (301)</th><th scope="col">What it ranks for now</th></tr></thead><tbody>{keep}</tbody></table></div>' if keep else "")
        search_html = f'''<section id="search" class="tint"><div class="wrap"><p class="eyebrow">Search and AI answers</p><h2>{_e(sr.get("heading", "Where you stand today, and what changes"))}</h2><p class="lead">{_e(sr.get("intro", ""))}</p>
<div class="stiles">{tiles}</div>
<div class="two" style="margin-top:34px"><div><h3 class="h3">Today <span class="asof">{_e(sr.get("as_of", ""))}</span></h3><ul>{today}</ul></div><div><h3 class="h3">After launch</h3><ul>{after}</ul></div></div>
{('<h3 class="h3" style="margin-top:34px">' + _e(sr.get("keep_heading", "Every page that earns a visitor today keeps earning it")) + '</h3>') if keep else ""}{keep_tbl}
<div class="change" style="margin-top:22px"><strong>What we do not promise:</strong> {_e(sr.get("note", "Rankings or traffic. Those depend on the market and the content you publish after launch. We promise the inputs, and we measure the result against this baseline at 30, 60 and 90 days."))}</div></div></section>'''

    # ---- fixed, found, to confirm
    heard = "".join(f"<li>{_e(x)}</li>" for x in pitch.get("heard", []))
    found = "".join(f"<li>{_e(x)}</li>" for x in pitch.get("found", []))
    heard_intro = pitch.get("heard_intro", "Tell us if any of this is wrong. It outranks our house defaults.")
    conf = pitch.get("confirm", [])
    CF = 6
    c_head = "".join(f"<li>{_e(x)}</li>" for x in conf[:CF])
    c_rest = "".join(f"<li>{_e(x)}</li>" for x in conf[CF:])
    nconf = len(conf)
    cword = WORDS.get(nconf, f"{nconf}") if nconf < 7 else {7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve"}.get(nconf, str(nconf))
    confirm_html = (f'<section id="confirm" class="tint"><div class="wrap"><p class="eyebrow">To confirm with you</p><h2>{cword} thing{"" if nconf == 1 else "s"} we wrote as a draft, not a fact</h2>'
                    f'<p class="lead">Each of these appears on the pages. None is built until you confirm or correct it.</p><ol class="confirm">{c_head}</ol>'
                    + (f'<details class="fold"><summary>Show the other {nconf - CF}</summary><ol class="confirm" style="counter-reset:cf {CF}">{c_rest}</ol></details>' if c_rest else "")
                    + '</div></section>') if conf else '<section id="confirm" hidden></section>'

    # ---- every page
    def erow(pg):
        return (f'<div class="row"><span class="pn">{_e(pname(pg))}</span><span class="links">'
                + "".join(f'<a href="{_slug(t)}/{pg["file"]}" target="_blank" rel="noopener" aria-label="{_e(pname(pg))} in {_e(_short(t))}">{_e(_short(t))}</a>' for t in themes) + "</span></div>")
    EV = 12
    e_head = "".join(erow(pg) for pg in pages[:EV])
    e_rest = "".join(erow(pg) for pg in pages[EV:])
    every_html = (f'<section id="every"><div class="wrap"><p class="eyebrow">Every page</p><h2>{len(pages)} pages, built and live in all {count.lower()}</h2>'
                  f'<p class="lead">One row per page; the links open it in each direction.</p>'
                  f'<div class="efilter"><label class="sr" for="eq">Find a page</label><input type="search" id="eq" placeholder="Find a page by name"><span id="ecount" aria-live="polite"></span></div>'
                  f'<div id="everylist"><div class="every">{e_head}</div>'
                  + (f'<details class="fold"><summary>Show all {len(pages)} pages</summary><div class="every">{e_rest}</div></details>' if e_rest else "") + '</div></div></section>')

    # ---- plan, turn
    plan = "".join(f'<div class="step"><div class="when">{_e(w)}</div><p>{_e(what)}</p></div>' for w, what in pitch.get("plan", []))
    qc = pitch.get("qbs_contact", {})
    std = ('<a class="alt" href="standard.html" target="_blank" rel="noopener"><h3 class="h4">The Quantum Website Standard</h3>'
           '<p>The ten things every site we build is guaranteed to have at launch, and the evidence you receive for each.</p><span>Open</span></a>') if standard else ""
    for t_, d_, h_ in pitch.get("more", []):
        std += f'<a class="alt" href="{_e(h_)}" target="_blank" rel="noopener"><h3 class="h4">{_e(t_)}</h3><p>{_e(d_)}</p><span>Open</span></a>'
    phone_href = re.sub(r"[^0-9+]", "", qc.get("phone", ""))
    call = f'<a class="btn ghost" href="tel:{_e(phone_href)}">Call {_e(qc.get("phone", ""))}</a>' if phone_href else ""
    subj = _e(client).replace(" ", "%20") + "%20website%20direction"
    mail = ""
    if qc.get("email"):
        mail = "".join(f'<a class="btn" href="mailto:{_e(qc["email"])}?subject={subj}:%20{_e(_short(t))}">We choose {_e(_short(t))}</a>' for t in themes)
        mail += f'<a class="btn ghost" href="mailto:{_e(qc["email"])}?subject={subj}">Email {_e(qc.get("name", "us"))} with notes</a>'

    # the bar is always dark here, so use the light logo variant when the build ships one
    hub_logo = b["logo"]
    _lt = re.sub(r"(\.\w+)$", r"-light\1", hub_logo)
    if out_dir and os.path.exists(os.path.join(out_dir, _lt)):
        hub_logo = _lt
    lw, lh = b.get("logo_w") or 99, b.get("logo_h") or 36
    logo_w = round(32 * lw / lh)

    css = CSS
    for k, v in (("__ACCENT__", accent), ("__INK__", ink), ("__DARK__", DARK), ("__BTNFG__", btn_fg), ("__ONDARK__", _on_dark(accent)),
                 ("__HEAD__", head), ("__BODY__", body), ("__N__", str(n)), ("__CF0__", "0")):
        css = css.replace(k, v)
    css_after = CSS_AFTER.replace("__DARK__", DARK)
    if fonts:
        font_head = ('<link rel="preload" href="assets/fonts/inter-latin-var.woff2" as="font" type="font/woff2" crossorigin>'
                     f"\n<style>{font_css('assets')}</style>")
    else:  # a build without the self-hosted files keeps the old behaviour
        font_head = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                     '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">')
    js = HUB_JS + (AUDIT_JS.replace("__STEP__", str(AUDIT_PAGE)) if seo else "")
    title = f"{_e(client)}, {count.lower()} website directions"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{count} complete website directions for {_e(client)}, prepared by Quantum Business Solutions.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{DARK}">
<link rel="canonical" href="{_e(base)}/">
<meta property="og:title" content="{title}">
<meta property="og:image" content="{_e(base)}/assets/hero-og.jpg">
<meta name="twitter:card" content="summary_large_image">
<script>document.documentElement.className='js'</script>
{font_head}
<style>{css}{seo["css"] if seo else ""}{css_after}</style></head><body data-first-dir="{_e(seo["first_dir"]) if seo else ""}">
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap"><a class="logo" href="#main" aria-label="{_e(client)}, back to the top"><img src="{_e(hub_logo)}" alt="{_e(b.get("logo_alt") or client)}" height="32" width="{logo_w}"></a><nav aria-label="Sections"><a href="#three">The {count.lower()}</a>{'<a href="#pick">Our pick</a>' if recommend else ''}<a href="#compare">Compare</a>{'<a href="#search">Search</a>' if search_html else ''}{seo["nav"] if seo else ""}<a href="#heard">Fixed</a>{'<a href="#confirm">To confirm</a>' if conf else ''}<a href="#every">Every page</a><a href="#plan">The plan</a><a href="#turn">Your turn</a>{ds_link}</nav></div></header>
<main id="main" tabindex="-1">
<section class="hero dk"><div class="wrap"><div class="hero-h"><p class="eyebrow">Quantum Business Solutions for {_e(client)}</p><h1>{headline}</h1><p class="sub">{_e(sub)}</p></div>
<div class="dcards" id="three">{"".join(cards)}</div>
{same}</div></section>
{choose}
{compare}
{search_html}
<section id="heard" class="dk"><div class="wrap"><div class="two"><div><p class="eyebrow">What we are treating as fixed</p><h2>What your site and brand profile already say</h2><p class="lead" style="margin-bottom:14px">{_e(heard_intro)}</p><ul>{heard}</ul></div><div><p class="eyebrow">What we found</p><h2>And what we would do about it</h2><ul>{found}</ul></div></div></div></section>
{confirm_html}
{every_html}
<section id="plan" class="tint"><div class="wrap"><p class="eyebrow">The plan</p><h2>From a choice to a live site</h2><div class="plan" style="margin-top:30px">{plan}</div>{('<div class="alts" style="margin-top:28px">' + std + '</div>') if std else ""}</div></section>
<section id="turn" class="dk"><div class="wrap turn"><p class="eyebrow">Your turn</p><h2>Tell us which one, and what you would change</h2><p class="lead">Reply with the direction and anything on any page you would change. Nothing is locked until you say so.</p><div class="btns">{mail}{call}</div></div></section>
</main>
<footer><div class="wrap"><p>{_e(pitch.get("footer", "Prepared for " + pitch.get("prepared_for", client) + ". Nothing here is live or indexed."))}</p></div></footer>
<script>{js}</script>
</body></html>
"""
