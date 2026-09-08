"""Design system page, generated per client from the content file and the direction tokens.

Written to <out>/design-system.html by preview.py before the hub, so the hub can link it.
Colour and type come from client_tokens (the same derivation the pages use), the module inventory from the
section types the content actually uses, the voice rules from the pitch, and the logo section from the brand
plus an optional assets/logo-concepts/concepts.json.
"""
from __future__ import annotations

import html
import json
import os

import reskin  # noqa: E402

E = html.escape

MODULES = {
    "hero-layered": ("Layered hero", "Full-bleed plate, pointer glow, network canvas, 3D hero object on a turntable, floating card, stats strip, load choreography", "Static plate, stacked card, no motion under reduced motion"),
    "wheel": ("Services wheel", "Segments lift toward the pointer; hover or focus swaps the panel; autoplays with a progress bar until touched", "Ordered list of the lines"),
    "flow": ("Process chart", "Numbered nodes on a self-drawing line; click for what happens and what you receive", "Vertical list on phones; no animation under reduced motion"),
    "beforeafter": ("Before and after", "Drag handle or arrow keys reveal the client's side over the status quo", "Two stacked panels on phones"),
    "fleet": ("Fleet rail", "Scroll-snap rail of product cutouts floating over floor shadows, with tilt", "Plain grid"),
    "story3d": ("3D story", "The device holds still in a sticky stage and turns to a new camera orbit for each step you scroll", "Poster image; steps still read"),
    "model3d": ("3D device", "Rotatable model in a stage", "Poster image"),
    "hotspots": ("Floor plan hotspots", "Numbered points on an isometric building, each opening a popover and a link", "Numbered list of the same links"),
    "seal": ("Seal of commitments", "Sourced commitments as badges with a source line", "Text list"),
    "map": ("Service map", "State outline with pins and travel rings", "Address list"),
    "timeline": ("History rail", "A line that draws across the years, big numerals, optional images, arrows; vertical on phones", "Plain list"),
    "proof": ("Proof number", "One large audited number on a stage with a perspective floor and spotlight", "Number and caption"),
    "checklist": ("Is this you", "Checkboxes that change the message as you tick them", "Static list"),
    "partners": ("Partner marquee", "Logos in a slow marquee with edge masks; pauses on hover", "Wrapped grid"),
    "video": ("Film", "Poster facade that loads the embed on click", "Link to the film"),
    "testimonials": ("Voices", "Feature layout with a lead quote", "Stacked quotes"),
    "calculator": ("Calculator", "Estimator with draft ranges, labelled as such", "Static table"),
    "comparison": ("Comparison", "Lease, rent, buy side by side with a recommended column", "Plain table"),
    "tabs": ("Tabs", "Keyboard-operable tabs with Home and End", "Stacked panels"),
    "cards": ("Cards", "Specular tilt and lift in Showcase", "Plain cards"),
    "stats": ("Stats", "Count up once on scroll, static ones marked", "Numbers"),
}
FACE_LINKS = "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Inter:wght@400;500;600;700&family=Open+Sans:wght@600;700;800&family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600;700&family=Instrument+Serif&display=swap"


def _face(stack: str) -> str:
    return (stack or "").split(",")[0].strip().strip("'\"") or "system-ui"


def _sw(label, value, note):
    try:
        fg = reskin.best_on(value)
    except Exception:
        fg = "#ffffff"
    return f'<div class="sw"><div class="chip" style="background:{E(value)};color:{E(fg)};text-shadow:none;border-bottom:1px solid var(--border)">{E(label)}</div><div class="meta"><code>{E(value)}</code>{E(note)}</div></div>'


def write(content, themes, roles, client_tokens, out_dir):
    b = content["brand"]
    client = content["client"]
    short = client.split(" ")[0]
    dirs = []
    for t in themes:
        css, tok = client_tokens(t, b)
        native = reskin.parse_native(css)
        dirs.append({"theme": t, "name": t.replace("Quantum ", ""), "tok": tok, "native": native, "role": roles.get(t, "")})
    d0 = dirs[0]
    tok0 = d0["tok"]
    accent, ink, cta_fg, chrome = tok0["--q-gold"], tok0["--accent-ink"], tok0["--cta-fg"], tok0["--chrome-bg"]
    bright, dim = tok0.get("--q-gold-bright", accent), tok0.get("--q-gold-dim", accent)

    # ---- module inventory from the content
    used = {}
    for p in content["pages"]:
        for s in p["sections"]:
            used.setdefault(s["type"], set()).add(p["file"])
    rows = []
    for k, (name, what, fb) in MODULES.items():
        if k in used:
            where = sorted(used[k])
            where_txt = "Every service page" if sum(1 for w in where if w.startswith("services/")) >= 4 and len(where) > 4 else ", ".join(w.replace(".html", "").replace("index", "home") for w in where[:4]) + (" and more" if len(where) > 4 else "")
            rows.append(f"<tr><td>{E(name)}</td><td>{E(what)}</td><td>{E(where_txt)}</td><td>{E(fb)}</td></tr>")

    # ---- palette swatches
    sw = [_sw("Accent", accent, " Buttons, dots, rings, highlights. Never body text."), _sw("Chrome", chrome, " Header, footer, dark bands, text on accent buttons." if b.get("chrome") == "dark" else " Header and footer ground."),
          _sw("Accent text", ink, " Eyebrows, links, big numbers on light grounds. Passes 4.5 to 1."), _sw("Hover", bright, " Button hover and pressed states.")]
    for d in dirs:
        n = d["native"]
        sw.append(_sw(f"{d['name']} ground", n.get("--bg", "#ffffff"), f" Page ground in {d['name']}."))
        sw.append(_sw(f"{d['name']} band", n.get("--bg-alt", "#f6f6f6"), f" Alternate section ground in {d['name']}."))
    sw.append(_sw("Text", d0["native"].get("--fg", "#111111"), " Body text."))
    sw.append(_sw("Muted", d0["native"].get("--fg-muted", "#555555"), " Secondary text, captions, sources."))

    # ---- type per direction
    type_rows = []
    for d in dirs:
        serif, sans = d["tok"].get("--q-serif", d["native"].get("--q-serif", "")), d["tok"].get("--q-sans", d["native"].get("--q-sans", ""))
        borrowed = (b.get("type_from") or {}).get(d["theme"])
        type_rows.append(f'<div class="dir"><div class="head" style="background:{E(d["native"].get("--bg-alt", "#f6f6f6"))}"><div class="k">{E(d["name"])}{" (type borrowed from " + E(borrowed.replace("Quantum ", "")) + ")" if borrowed else ""}</div>'
                         f'<div class="h" style="font-family:{E(serif)}">Serviced by people who <span style="color:{E(ink)}">answer the phone</span>.</div>'
                         f'<p style="font-family:{E(sans)};margin:8px 0 0">Body, navigation, labels and forms in {E(_face(sans))}. Headings in {E(_face(serif))}.</p>'
                         f'<div class="tok"><span>{E(_face(serif))}</span><span>{E(_face(sans))}</span><span>radius {E(d["native"].get("--radius", "8px"))}</span><span>{E(d["role"])}</span></div></div></div>')

    # ---- voice from the pitch
    heard = (content.get("pitch") or {}).get("heard", [])[:4]
    voice = "".join(f'<div class="rule"><div class="do">Do</div><div>{E(h)}</div></div>' for h in heard)
    voice += ('<div class="rule"><div class="do">Do</div><div><b>Say the number and where it came from.</b> Every figure on the site carries its source.</div></div>'
              '<div class="rule"><div class="do">Do</div><div><b>Name what the customer receives.</b> Every process step ends with what lands in their hands.</div></div>'
              '<div class="rule"><div class="dont">Avoid</div><div><b>Unsourced promises.</b> No response-time or pricing claims the client has not published or put in an agreement.</div></div>'
              '<div class="rule"><div class="dont">Avoid</div><div><b>Em dashes, exclamation marks, and Learn more.</b> Buttons and links say what happens.</div></div>')

    # ---- logo and optional concepts
    logo = b.get("logo", "")
    logo_html = f'<div class="logo"><div class="art{" dark" if b.get("chrome") == "dark" else ""}"><img src="{E(logo)}" alt="{E(b.get("logo_alt", client))}" width="{b.get("logo_w", 300)}" height="{b.get("logo_h", 100)}"></div><div class="meta"><span class="tag">Today</span><b>Current logo</b>{E(b.get("logo_note", ""))}</div></div>'
    concepts_intro, concepts_note = "", ""
    cj = os.path.join(out_dir, "assets", "logo-concepts", "concepts.json")
    if os.path.exists(cj):
        c = json.load(open(cj, encoding="utf-8"))
        concepts_intro = f'<p class="intro">{E(c.get("intro", ""))}</p>'
        for it in c.get("items", []):
            logo_html += (f'<div class="logo"><div class="art"><img src="assets/logo-concepts/{E(it["file"])}" alt="{E(it.get("title", ""))}" width="900" height="900"></div>'
                          f'<div class="meta"><span class="tag{" rec" if "ecommend" in it.get("tag", "") else ""}">{E(it.get("tag", "Concept"))}</span><b>{E(it.get("title", ""))}</b>{E(it.get("body", ""))}</div></div>')
        concepts_note = f'<p class="note">{E(c.get("note", ""))}</p>' if c.get("note") else ""
    else:
        concepts_intro = '<p class="intro">The site is designed so the current logo works on day one. Logo exploration is available on request and is separate from the website scope.</p>'

    dir_cards = "".join(f'<div class="dcard"><div class="k">{E(d["name"])}</div><p>{E(d["role"])}</p><a href="{E(d["theme"].lower().replace("quantum ", ""))}/index.html">Open {E(d["name"])}</a></div>' for d in dirs)
    h_face = _face(d0["tok"].get("--q-serif", ""))
    s_face = _face(d0["tok"].get("--q-sans", "Inter"))

    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(client)} Design System</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="{FACE_LINKS}">
<style>
:root{{--accent:{accent};--ink:{ink};--chrome:{chrome};--cta:{cta_fg};--bright:{bright};--bg:#ffffff;--bg-alt:{d0["native"].get("--bg-alt", "#f6f6f6")};--fg:{d0["native"].get("--fg", "#1a1a1a")};--muted:{d0["native"].get("--fg-muted", "#555")};--border:{tok0.get("--border", "#e4e4e4")};--sans:'{s_face}',system-ui,sans-serif;--show:'{h_face}',system-ui,sans-serif}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:17px/1.55 var(--sans);-webkit-font-smoothing:antialiased}}a{{color:var(--ink)}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 24px}}
header.top{{background:var(--chrome);color:#fff;padding:18px 0;position:sticky;top:0;z-index:5}}header.top .wrap{{display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap}}
header.top img{{height:40px;width:auto;{"background:#fff;padding:6px 10px;border-radius:6px;" if b.get("logo_plate") else ""}}}header.top nav{{display:flex;gap:16px;flex-wrap:wrap}}header.top nav a{{color:rgba(255,255,255,.85);text-decoration:none;font-size:14px;font-weight:600}}header.top nav a:hover{{color:var(--accent)}}
.hero{{padding:88px 0 56px;border-bottom:1px solid var(--border)}}
.eyebrow{{font-size:13px;letter-spacing:.22em;text-transform:uppercase;font-weight:600;color:var(--ink);display:inline-flex;align-items:center;gap:10px}}.eyebrow::before{{content:"";width:8px;height:8px;border-radius:50%;background:var(--accent)}}
h1{{font:800 clamp(40px,5vw,68px)/1.02 var(--show);letter-spacing:-.03em;margin:18px 0 20px;max-width:16ch;text-wrap:balance}}h1 em{{font-style:normal;color:var(--ink)}}
.lead{{font-size:20px;line-height:1.5;color:var(--muted);max-width:62ch;margin:0}}
section{{padding:72px 0;border-bottom:1px solid var(--border)}}section.alt{{background:var(--bg-alt)}}
h2{{font:700 clamp(28px,3vw,40px)/1.1 var(--show);letter-spacing:-.02em;margin:14px 0 12px;text-wrap:balance}}h3{{font:700 19px/1.3 var(--sans);margin:0 0 6px}}p{{margin:0 0 12px}}
.intro{{color:var(--muted);max-width:66ch;margin-bottom:34px}}
.grid{{display:grid;gap:18px}}.g3{{grid-template-columns:repeat(3,minmax(0,1fr))}}.g4{{grid-template-columns:repeat(4,minmax(0,1fr))}}.g2{{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:900px){{.g3,.g4{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}@media(max-width:600px){{.g3,.g4,.g2{{grid-template-columns:1fr}}}}
.sw{{border:1px solid var(--border);border-radius:10px;overflow:hidden;background:#fff}}.sw .chip{{height:96px;display:flex;align-items:flex-end;padding:12px 14px;font:600 13px/1 var(--sans);letter-spacing:.04em;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.5)}}.sw .meta{{padding:12px 14px;font-size:13.5px;color:var(--muted)}}.sw code{{display:block;font:13px/1 ui-monospace,Menlo,monospace;color:var(--fg);margin-bottom:6px}}
.dir{{border:1px solid var(--border);border-radius:14px;overflow:hidden;margin-bottom:16px}}.dir .head{{padding:26px}}.dir .k{{font-size:12.5px;letter-spacing:.18em;text-transform:uppercase;font-weight:600;color:var(--muted)}}.dir .h{{margin:10px 0 8px;font-size:30px;line-height:1.05;letter-spacing:-.02em;font-weight:700}}
.tok{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}.tok span{{font:12.5px/1.3 ui-monospace,Menlo,monospace;background:rgba(0,0,0,.05);border:1px solid var(--border);padding:7px 9px;border-radius:6px}}
.dcard{{border:1px solid var(--border);border-radius:14px;padding:22px;background:#fff}}.dcard .k{{font-size:12.5px;letter-spacing:.18em;text-transform:uppercase;font-weight:700;color:var(--ink)}}.dcard p{{color:var(--muted);font-size:15px}}.dcard a{{font-weight:700;text-decoration:none}}
.btn{{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 24px;border-radius:999px;background:var(--accent);color:var(--cta);font:600 16px/1 var(--sans);text-decoration:none;border:2px solid var(--accent)}}.btn.ghost{{background:transparent;color:var(--fg);border-color:var(--border)}}.btn.sq{{border-radius:6px}}
.demo{{border:1px solid var(--border);border-radius:14px;padding:28px;background:#fff}}.demo.dark{{background:var(--chrome);color:#fff;border-color:transparent}}.demo .lab{{font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);font-weight:600;margin-bottom:16px}}.demo.dark .lab{{color:rgba(255,255,255,.7)}}
.row{{display:flex;gap:14px;flex-wrap:wrap;align-items:center}}.stat b{{display:block;font:800 44px/1 var(--show);letter-spacing:-.03em;color:var(--ink)}}.stat span{{display:block;font-size:14px;color:var(--muted);margin-top:6px}}.demo.dark .stat b{{color:#fff}}.demo.dark .stat span{{color:rgba(255,255,255,.7)}}
.seal{{display:flex;gap:14px;align-items:flex-start}}.seal .badge{{width:64px;height:64px;border-radius:50%;flex:none;display:grid;place-items:center;background:conic-gradient(var(--accent) 0 75%,var(--border) 75% 100%)}}.seal .badge b{{width:52px;height:52px;border-radius:50%;background:#fff;display:grid;place-items:center;font:800 14px/1 var(--show);color:var(--chrome)}}
.node{{display:flex;gap:14px;align-items:flex-start}}.node .dot{{width:46px;height:46px;border-radius:50%;background:var(--accent);color:var(--cta);display:grid;place-items:center;font:800 16px/1 var(--show);flex:none}}
.rule{{display:grid;grid-template-columns:110px minmax(0,1fr);gap:18px;padding:16px 0;border-top:1px solid var(--border);font-size:15.5px}}.rule:last-child{{border-bottom:1px solid var(--border)}}.rule .do{{color:var(--ink);font-weight:700;font-size:13px;letter-spacing:.12em;text-transform:uppercase;padding-top:3px}}.rule .dont{{color:#9a3b2f;font-weight:700;font-size:13px;letter-spacing:.12em;text-transform:uppercase;padding-top:3px}}
.logo{{border:1px solid var(--border);border-radius:14px;overflow:hidden;background:#fff}}.logo .art{{aspect-ratio:4/3;position:relative;background:#fff}}.logo .art.dark{{background:var(--chrome)}}.logo .art img{{position:absolute;inset:28px;width:calc(100% - 56px);height:calc(100% - 56px);object-fit:contain}}.logo .meta{{padding:16px 18px 20px;font-size:14.5px;color:var(--muted);border-top:1px solid var(--border)}}.logo .meta b{{display:block;color:var(--fg);font-size:16px;margin:6px 0}}.logo .tag{{display:inline-block;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--ink)}}.logo .tag.rec{{background:var(--accent);color:var(--cta);padding:4px 8px;border-radius:4px}}
.note{{font-size:14px;color:var(--muted);border-left:3px solid var(--accent);padding:8px 14px;margin-top:22px;max-width:70ch}}
table{{width:100%;border-collapse:collapse;font-size:15px}}th,td{{text-align:left;padding:12px 10px;border-bottom:1px solid var(--border);vertical-align:top}}th{{font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600}}.tblwrap{{overflow-x:auto}}
footer{{padding:40px 0 60px;font-size:14px;color:var(--muted)}}:focus-visible{{outline:3px solid var(--chrome);outline-offset:3px}}
</style>
</head>
<body>
<header class="top"><div class="wrap"><img src="{E(logo)}" alt="{E(b.get("logo_alt", client))}" width="{b.get("logo_w", 300)}" height="{b.get("logo_h", 100)}"><nav aria-label="Sections"><a href="#color">Color</a><a href="#type">Type</a><a href="#directions">Directions</a><a href="#components">Components</a><a href="#imagery">Imagery</a><a href="#voice">Voice</a><a href="#logo">Logo</a><a href="index.html">Back to the preview</a></nav></div></header>
<div class="hero"><div class="wrap"><div class="eyebrow">Design system, generated {E(str(__import__("datetime").date.today()))}</div><h1>One brand, {["one","two","three","four","five"][len(dirs)-1] if len(dirs) <= 5 else len(dirs)} directions, <em>every decision written down</em>.</h1>
<p class="lead">The colours, type, spacing, components, imagery rules and voice behind the {E(client)} preview. Every page in every direction derives from these tokens, so whichever direction is chosen, the build in HubSpot starts from a documented system rather than from taste.</p></div></div>
<section id="color"><div class="wrap"><div class="eyebrow">Color</div><h2>One accent does the work. The chrome holds the frame. Everything else stays quiet.</h2>
<p class="intro">The accent comes from the logo. It is the only accent on the site: buttons, the eyebrow dot, progress lines, the badge ring. Where it is too light to carry text, a darker ink derived from it is used for accent text and passes 4.5 to 1 on every ground.</p>
<div class="grid g4">{"".join(sw)}</div></div></section>
<section class="alt" id="type"><div class="wrap"><div class="eyebrow">Typography</div><h2>One body face for reading. One display face per direction for character.</h2>
<p class="intro">Body copy, navigation, labels and forms use the same face in every direction, so the reading experience is identical whichever is chosen. Headings carry the personality. Headings balance across lines, uppercase labels get letter-spacing, running text stays near 65 characters wide.</p>{"".join(type_rows)}</div></section>
<section id="directions"><div class="wrap"><div class="eyebrow">The {len(dirs)} directions</div><h2>Same words, same accent, {len(dirs)} compositions.</h2><p class="intro">Each direction owns its geometry and its heading face. The copy, the proof and the page set are identical, so the choice is about how {E(short)} wants to be read, not what it says.</p><div class="grid g3">{dir_cards}</div></div></section>
<section class="alt" id="components"><div class="wrap"><div class="eyebrow">Components</div><h2>The parts, and the rules each one follows.</h2>
<div class="grid g2">
<div class="demo"><div class="lab">Buttons</div><div class="row"><a class="btn" href="#">{E(b.get("cta", {}).get("label", "Start"))}</a><a class="btn ghost" href="#">Secondary</a><a class="btn sq" href="#">Clean</a></div><p style="font-size:14px;color:var(--muted);margin:16px 0 0">Accent fill, 48px tall, one primary per view. Labels say what happens, never Learn more.</p></div>
<div class="demo dark"><div class="lab">Stats on chrome</div><div class="row" style="gap:36px"><div class="stat"><b>1</b><span>Partner</span></div><div class="stat"><b>24x7</b><span>Monitoring</span></div></div><p style="font-size:14px;color:rgba(255,255,255,.7);margin:16px 0 0">Numbers count up once on scroll, then hold. Every figure has a source on the page.</p></div>
<div class="demo"><div class="lab">Seal of commitments</div><div class="seal"><div class="badge"><b>2016</b></div><div><h3>A commitment someone else verifies</h3><p style="font-size:14.5px;color:var(--muted);margin:0">Only sourced lines go in a badge.</p></div></div></div>
<div class="demo"><div class="lab">Process chart node</div><div class="node"><div class="dot">1</div><div><h3>Assess</h3><p style="font-size:14.5px;color:var(--muted);margin:6px 0 0">Nodes on a self-drawing line; click for what happens and what you receive.</p></div></div></div>
</div>
<div class="tblwrap" style="margin-top:34px"><table><thead><tr><th>Signature module</th><th>What it does</th><th>Where it lives</th><th>Falls back to</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<p class="note">Every module degrades to plain HTML and stops moving under prefers-reduced-motion. The depth layer (scroll reveals, specular tilt, perspective floor, glass header, hero choreography) runs on every page and needs no content.</p></div></section>
<section id="imagery"><div class="wrap"><div class="eyebrow">Imagery</div><h2>Real devices, real people, real places. Labelled stand-ins until then.</h2>
<p class="intro">Every photograph and render on the preview is generated and says so in a caption. None of it is passed off as {E(short)}'s people or premises. The build swaps them for the client's own imagery and manufacturer product photography before launch.</p>
<div class="rule"><div class="do">Do</div><div><b>Lead with the primary line.</b> The main manufacturer or service appears first in every list and in the hero object.</div></div>
<div class="rule"><div class="do">Do</div><div><b>Cut out products.</b> Devices on transparent backgrounds with a soft floor shadow, three-quarter view, no logos on generated units.</div></div>
<div class="rule"><div class="do">Do</div><div><b>Show the work.</b> Hands and machines over handshakes.</div></div>
<div class="rule"><div class="dont">Avoid</div><div><b>Stock office people.</b> If it is not the client's team, it is a device, a place or an illustration.</div></div>
<div class="rule"><div class="dont">Avoid</div><div><b>Heavy pages.</b> Hero plates at 2,100px, everything else at 1,200 and 600, lazy below the fold.</div></div></div></section>
<section class="alt" id="voice"><div class="wrap"><div class="eyebrow">Voice</div><h2>Plain, specific, and sourced. The proof does the selling.</h2>{voice}</div></section>
<section id="logo"><div class="wrap"><div class="eyebrow">Logo</div><h2>The current mark{", and directions for a fresher one" if concepts_note else ""}.</h2>{concepts_intro}<div class="grid g3">{logo_html}</div>{concepts_note}</div></section>
<footer><div class="wrap">{E(client)} design system, generated by Quantum Business Solutions from the preview's own tokens. Preview imagery is generated and labelled.</div></footer>
</body>
</html>
'''
    with open(os.path.join(out_dir, "design-system.html"), "w", encoding="utf-8") as f:
        f.write(doc)
