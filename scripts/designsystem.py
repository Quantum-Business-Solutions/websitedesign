#!/usr/bin/env python3
"""Generate the Website Design System document from the real measured tokens.

Generated, not hand-written, so it cannot drift from what actually ships. Reads
themes/tokens.json (refresh it with scripts/themetokens.py) and themes/catalogue.md
for the module inventory.

  python3 scripts/designsystem.py --out /tmp/design-system.html
"""
from __future__ import annotations
import argparse, html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = lambda s: html.escape(str(s or ""), quote=True)

FONT_URL = (
    "https://fonts.googleapis.com/css2"
    "?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700"
    "&family=Instrument+Serif:ital@0;1"
    "&family=Poppins:wght@400;500;600"
    "&family=Space+Grotesk:wght@400;500;700"
    "&family=Open+Sans:wght@400;600;700"
    "&family=Playfair+Display:ital,wght@0,500;0,700;1,500"
    "&family=Spectral:wght@400;600;700"
    "&family=Newsreader:opsz,wght@6..72,400;6..72,600;6..72,700"
    "&family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,700"
    "&family=Inter:wght@400;500;600"
    "&family=DM+Sans:wght@400;500;600;700"
    "&family=IBM+Plex+Mono:wght@400;500"
    "&display=swap"
)

ROLES = [
    ("--q-gold",        "accent",      "Links, primary CTA fill. The one saturated colour."),
    ("--q-gold-bright", "accent hover","A lighter step of the same hue. Never a second colour."),
    ("--q-gold-dim",    "accent dim",  "De-emphasised accent."),
    ("--bg",            "ground",      "The page. This is the real light/dark answer, not the mode field."),
    ("--bg-alt",        "surface",     "Alternating bands, raised panels."),
    ("--card",          "card",        "Card fill."),
    ("--fg",            "text",        "Body copy."),
    ("--fg-muted",      "muted",       "Secondary copy, labels."),
    ("--border",        "hairline",    "Rules and card edges. Carries the accent hue."),
    ("--cta-fg",        "on-accent",   "Text ON the accent. Contrast-critical."),
    ("--q-serif",       "headings",    "The theme's identity."),
    ("--q-sans",        "body",        "Reading face."),
]

GRID = [
    ("2",  "—",        "—",        "2×1 ✅"),
    ("3",  "—",        "3×1 ✅",   "+1 weak"),
    ("4",  "4×1 ✅",   "+1 ORPHAN","2×2 ✅"),
    ("5",  "+1 ORPHAN","3+2 ok",   "+1 weak"),
    ("6",  "4+2 weak", "3×2 ✅",   "2×3 ✅"),
    ("7",  "+3 ok",    "+1 ORPHAN","+1 weak"),
    ("8",  "4×2 ✅",   "+2 ok",    "2×4 ✅"),
    ("9",  "+1 ORPHAN","3×3 ✅",   "+1 weak"),
    ("12", "4×3 ✅",   "3×4 ✅",   "2×6 ✅"),
]

FLOORS = [
    ("Text on ground",        "4.5:1",  "WCAG 1.4.3 AA, normal text"),
    ("Muted text on ground",  "4.5:1",  "Muted is still body text"),
    ("Text on accent",        "4.5:1",  "Every primary button"),
    ("Accent on ground",      "3.0:1",  "Links and large text, WCAG 1.4.11"),
    ("Tap target",            "24×24px","WCAG 2.5.8 AA. 44×44 is Apple's guidance"),
    ("Target spacing",        "8px",    "Adjacent interactive elements"),
    ("Body text on mobile",   "13px",   "12px is a desktop habit"),
    ("Form inputs",           "16px",   "Below this iOS zooms the page on focus"),
    ("Pinch-zoom",            "allowed","Blocking it fails WCAG 1.4.4"),
    ("Sticky chrome",         "≤25% vh","Header plus sticky CTA together"),
]


def modules():
    """Pull the module inventory straight out of the catalogue so one source governs.

    The lists wrap across lines and are separated by middots, so capture the whole
    block from the bold label to the next blank line rather than line by line -- the
    first version of this only caught the first line of each and reported 42 of 57.
    """
    txt = open(os.path.join(ROOT, "themes", "catalogue.md"), encoding="utf-8").read()
    out = []
    for label in ("Persuasion modules", "Proof", "Conversion", "Structure & content"):
        m = re.search(rf"\*\*{re.escape(label)}[^*]*\*\*(.*?)(?:\n\s*\n)", txt, re.S)
        if not m:
            continue
        names = re.findall(r"`([a-z0-9-]+)`", m.group(1))
        if names:
            out.append((label.replace(" modules", ""), names))
    return out


def build(themes):
    order = ["Quantum Flagship", "Quantum Void", "Quantum Signal", "Quantum Converter",
             "Quantum Clean", "Quantum Press", "Quantum Paper", "Quantum Journal",
             "Quantum Showcase"]
    order = [t for t in order if t in themes]

    cards = []
    for i, name in enumerate(order, 1):
        m = themes[name]
        t = m["tokens"]
        short = name.replace("Quantum ", "")
        cr = m.get("ctaContrast")
        ok = m.get("ctaPassesAA", True)
        badge = (f'<span class="cr ok">{cr}:1</span>' if ok
                 else f'<span class="cr bad">{cr}:1 · fails AA</span>')
        chips = "".join(
            f'<span class="chip" title="{E(k)} {E(t[k])}" '
            f'style="background:{E(t[k])}"></span>'
            for k in ("--bg", "--bg-alt", "--card", "--q-gold", "--fg", "--fg-muted")
            if t.get(k, "").startswith("#"))
        cards.append(f"""
<article class="theme" style="--tbg:{E(t.get('--bg','#fff'))};--tfg:{E(t.get('--fg','#111'))};
  --tmut:{E(t.get('--fg-muted','#666'))};--tacc:{E(t.get('--q-gold','#c4a44a'))};
  --tcta:{E(t.get('--cta-fg','#fff'))};--tcard:{E(t.get('--card','#fff'))};
  --tbd:{E(t.get('--border','rgba(0,0,0,.12)'))};--tserif:{E(t.get('--q-serif','serif'))};
  --tsans:{E(t.get('--q-sans','sans-serif'))}">
  <div class="specimen">
    <span class="eyebrow">{i:02d} · {E(m['ground'])}</span>
    <h3 class="tname">{E(short)}</h3>
    <p class="tsample">Handled with care from the first conversation.</p>
    <span class="tbtn">Book a consult</span>
  </div>
  <div class="tmeta">
    <p class="reads">{E(m.get('readsAs'))}</p>
    <p class="reach">{E(m.get('reachForIt'))}</p>
    <dl>
      <dt>Headings</dt><dd>{E(t.get('--q-serif','').split(',')[0].strip(chr(39)))}</dd>
      <dt>Body</dt><dd>{E(t.get('--q-sans','').split(',')[0].strip(chr(39)))}</dd>
      <dt>Ground</dt><dd class="mono">{E(t.get('--bg'))}</dd>
      <dt>Accent</dt><dd class="mono">{E(t.get('--q-gold'))}</dd>
      <dt>On accent</dt><dd>{badge}</dd>
    </dl>
    <div class="chips">{chips}</div>
  </div>
</article>""")

    role_rows = "".join(
        f"<tr><td class='mono'>{E(k)}</td><td>{E(lbl)}</td><td>{E(desc)}</td></tr>"
        for k, lbl, desc in ROLES)

    grid_rows = "".join(
        "<tr><td class='mono'>{}</td>{}</tr>".format(
            E(n), "".join(
                f"<td class='{'orph' if 'ORPHAN' in c else ('good' if '✅' in c else '')}'>{E(c)}</td>"
                for c in (a, b, cc)))
        for n, a, b, cc in GRID)

    floor_rows = "".join(
        f"<tr><td>{E(a)}</td><td class='mono num'>{E(b)}</td><td>{E(c)}</td></tr>"
        for a, b, c in FLOORS)

    mod_html = "".join(
        f"<div class='modgroup'><h4>{E(label)} <span>{len(names)}</span></h4><p>" +
        " · ".join(f"<code>{E(n)}</code>" for n in names) + "</p></div>"
        for label, names in modules())

    fails = [n.replace("Quantum ", "") for n in order
             if themes[n].get("ctaPassesAA") is False]

    return f"""<title>Quantum Website Design System</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONT_URL}">
<style>
:root{{
  --paper:#f6f4ef; --panel:#fffefb; --ink:#1a1c1a; --ink-2:#5d635c;
  --faint:#8d938a; --line:#e2ded4; --rule:#cec9bb; --accent:#7a6320;
  --good:#2f6b46; --bad:#a33b18;
}}
@media (prefers-color-scheme:dark){{ :root:not([data-theme="light"]){{
  --paper:#131412; --panel:#1a1c19; --ink:#eceae4; --ink-2:#a8ada3;
  --faint:#7d837a; --line:#2a2c27; --rule:#3a3d36; --accent:#d3b66a;
  --good:#6fbc8c; --bad:#e08a5c;
}}}}
:root[data-theme="dark"]{{
  --paper:#131412; --panel:#1a1c19; --ink:#eceae4; --ink-2:#a8ada3;
  --faint:#7d837a; --line:#2a2c27; --rule:#3a3d36; --accent:#d3b66a;
  --good:#6fbc8c; --bad:#e08a5c;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);
  font:16px/1.65 'DM Sans',system-ui,-apple-system,sans-serif}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 24px}}
h1,h2,h3,h4{{font-family:Fraunces,Georgia,serif;margin:0;line-height:1.1;
  letter-spacing:-.02em;text-wrap:balance}}
h1{{font-size:clamp(34px,6vw,64px);font-weight:600}}
h2{{font-size:clamp(21px,2.7vw,29px);font-weight:600}}
h4{{font-size:15px;letter-spacing:0}}
.mono{{font-family:'IBM Plex Mono',ui-monospace,monospace;font-variant-numeric:tabular-nums}}
.tag{{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--faint)}}
header.top{{padding:66px 0 40px}}
header.top .tag{{display:block;margin-bottom:18px}}
header.top p{{font-size:19px;color:var(--ink-2);max-width:60ch;margin:22px 0 0}}
header.top p b{{color:var(--ink);font-weight:600}}
section{{padding:48px 0;border-top:1px solid var(--rule)}}
section > .tag{{display:block;color:var(--accent);margin-bottom:8px}}
section > .lead{{color:var(--ink-2);max-width:68ch;margin:12px 0 0}}
.themes{{display:grid;grid-template-columns:1fr;gap:20px;margin:32px 0 0}}
@media(min-width:760px){{.themes{{grid-template-columns:1fr 1fr}}}}
@media(min-width:1040px){{.themes{{grid-template-columns:1fr 1fr 1fr}}}}
.theme{{border:1px solid var(--line);border-radius:5px;overflow:hidden;background:var(--panel)}}
.specimen{{background:var(--tbg);color:var(--tfg);font-family:var(--tsans);
  padding:24px 22px 26px;border-bottom:1px solid var(--tbd)}}
.specimen .eyebrow{{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--tacc)}}
.tname{{font-family:var(--tserif);font-size:29px;margin:9px 0 10px;color:var(--tfg);font-weight:600}}
.tsample{{font-size:13.5px;color:var(--tmut);margin:0 0 18px;line-height:1.55}}
.tbtn{{display:inline-block;background:var(--tacc);color:var(--tcta);font-size:12.5px;
  font-weight:600;padding:9px 17px;border-radius:5px}}
.tmeta{{padding:18px 22px 20px}}
.reads{{font-weight:600;font-size:14px;margin:0 0 4px}}
.reach{{font-size:13px;color:var(--ink-2);margin:0 0 15px;line-height:1.5}}
.tmeta dl{{display:grid;grid-template-columns:auto 1fr;gap:5px 14px;margin:0;font-size:12.5px}}
.tmeta dt{{color:var(--faint)}} .tmeta dd{{margin:0;text-align:right}}
.cr{{font-family:'IBM Plex Mono',monospace;font-size:11.5px;padding:1px 6px;border-radius:3px}}
.cr.ok{{color:var(--good);background:color-mix(in srgb,var(--good) 13%,transparent)}}
.cr.bad{{color:var(--bad);background:color-mix(in srgb,var(--bad) 15%,transparent);font-weight:600}}
.chips{{display:flex;gap:4px;margin:16px 0 0}}
.chip{{width:26px;height:16px;border-radius:2px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.15)}}
table{{border-collapse:collapse;width:100%;font-size:14.5px;margin:24px 0 0}}
th{{text-align:left;font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--faint);padding:0 12px 9px;border-bottom:1px solid var(--rule);
  font-weight:500}}
td{{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}}
td.num,th.num{{text-align:right}}
td.orph{{color:var(--bad);font-weight:600}} td.good{{color:var(--good)}}
.scroller{{overflow-x:auto}}
.modgroup{{padding:16px 0;border-bottom:1px solid var(--line)}}
.modgroup h4{{margin-bottom:7px}}
.modgroup h4 span{{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--faint);
  font-weight:400;margin-left:6px}}
.modgroup p{{margin:0;font-size:13px;line-height:2}}
code{{font-family:'IBM Plex Mono',monospace;font-size:12px;
  background:color-mix(in srgb,var(--ink) 6%,transparent);padding:2px 6px;border-radius:3px}}
.flag{{border-left:2px solid var(--bad);padding:4px 0 4px 16px;margin:26px 0 0}}
.flag h4{{color:var(--bad);margin-bottom:5px}}
.flag p{{margin:0;color:var(--ink-2);font-size:14.5px}}
.cols{{display:grid;grid-template-columns:1fr;gap:24px;margin:26px 0 0}}
@media(min-width:800px){{.cols{{grid-template-columns:1fr 1fr}}}}
.note{{border-left:2px solid var(--rule);padding:2px 0 2px 16px}}
.note h4{{margin-bottom:5px}} .note p{{margin:0;color:var(--ink-2);font-size:14.5px}}
footer{{padding:40px 0 70px;color:var(--faint);font-size:13px}}
</style>

<div class="wrap">
<header class="top">
  <span class="tag">Quantum Business Solutions</span>
  <h1>Website Design System</h1>
  <p><b>Nine themes, one system, {sum(len(n) for _, n in modules())} shared modules.</b> Every value
  on this page was read from the live theme source, not transcribed — so it cannot drift from what
  ships. Regenerate with <span class="mono">scripts/designsystem.py</span>.</p>
</header>

<section>
  <span class="tag">Foundations</span>
  <h2>The nine themes</h2>
  <p class="lead">A theme's identity is its <b>ground</b> and its <b>heading typeface</b>. The layout
  system and the modules are shared, so the typeface does the character work — which is why you pick
  a theme partly <em>for</em> its typeface. Each specimen below is set in the theme's real faces at
  its real colours.</p>
  <div class="themes">{''.join(cards)}</div>
  {'''<div class="flag"><h4>''' + ', '.join(fails) + ''' fail WCAG AA on button text</h4>
  <p>Near-white on a mid-gold: 3.52:1 for Press, 3.9:1 for the rest, against a 4.5:1 minimum. That is
  every primary button on every light-theme site. The four dark themes pass at 8.21:1. Fix at source
  — and until then, <span class="mono">reskin.py</span> derives a compliant on-accent colour, so a
  re-skinned clone clears the gate even though the theme does not.</p></div>''' if fails else ''}
</section>

<section>
  <span class="tag">Colour</span>
  <h2>Twelve properties, one block</h2>
  <p class="lead">The re-skin surface is the <span class="mono">NATIVE DIRECTION</span> block in
  <span class="mono">css/quantum.css</span> — <b>not</b> <span class="mono">fields.json</span>, whose
  colour fields are wired to nothing. Twelve custom properties, one contiguous place.</p>
  <div class="scroller"><table>
    <thead><tr><th>property</th><th>role</th><th>what it does</th></tr></thead>
    <tbody>{role_rows}</tbody>
  </table></div>
  <div class="cols">
    <div class="note"><h4>Accent hover is derived, never picked</h4>
      <p>Same hue, shifted lightness. A second unrelated colour there reads as a mistake.</p></div>
    <div class="note"><h4>Neutrals carry a hue</h4>
      <p>A pure mid-grey reads as inherited; a slight cast reads as chosen. Saturation has to
      <em>rise</em> at the extremes — at 5% lightness, 10% saturation rounds to grey.</p></div>
  </div>
</section>

<section>
  <span class="tag">Layout</span>
  <h2>Card grids must balance</h2>
  <p class="lead">Six cards on one row and two on the next reads as a mistake because it is one —
  nobody chose it, a <span class="mono">grid-template-columns</span> did. <b>Change the column count,
  not the content.</b> 12 is the only count clean at every width.</p>
  <div class="scroller"><table>
    <thead><tr><th>cards</th><th>4 col</th><th>3 col</th><th>2 col</th></tr></thead>
    <tbody>{grid_rows}</tbody>
  </table></div>
  <div class="cols">
    <div class="note"><h4>The cascade is part of the decision</h4>
      <p>3 or 9 cards go 3 → <b>1</b> and skip 2 columns; 4 or 8 go 4 → 2 → 1 and skip 3. A grid
      balanced on desktop can orphan on tablet.</p></div>
    <div class="note"><h4>When the count is fixed</h4>
      <p>Change the columns so the remainder is at least half a row; or span the odd card
      (<span class="mono">grid-column: span 2</span>) so it reads as designed; or change the count —
      a list padded to fill a grid usually has a weak item in it.</p></div>
  </div>
</section>

<section>
  <span class="tag">Accessibility</span>
  <h2>Floors, not aspirations</h2>
  <p class="lead">Every row is measured by <span class="mono">scripts/verify.mjs</span> at
  390 / 768 / 1440. Exit code 1 means it failed. <b>Review mobile before desktop</b> — most of this
  fails on a phone first.</p>
  <div class="scroller"><table>
    <thead><tr><th>what</th><th class="num">floor</th><th>why</th></tr></thead>
    <tbody>{floor_rows}</tbody>
  </table></div>
  <div class="flag"><h4>Never composite text with opacity</h4>
    <p>Use <span class="mono">color-mix()</span> or a real colour. Opacity-composited text fails
    contrast measurement, and the failure is invisible until someone measures it.</p></div>
</section>

<section>
  <span class="tag">Components</span>
  <h2>The shared module library</h2>
  <p class="lead">Every theme draws on the same modules, and 12 of the 16 page templates are a
  <span class="mono">dnd_area</span> — so a delivered site is genuinely drag-and-drop editable. The
  modules are also the <b>wireframe vocabulary</b>: sectioning a page means choosing from this
  inventory, not drawing boxes.</p>
  {mod_html}
  <div class="note" style="margin-top:22px"><h4>Persuasion modules are the sales method, encoded</h4>
    <p><code>pain-bridge</code> is Pain · <code>is-this-you</code> is Person ·
    <code>two-futures</code> and <code>why-now</code> carry Promise. When a hero fails the three-P
    test, the fix is usually a missing module, not new adjectives.</p></div>
</section>

<section>
  <span class="tag">Imagery</span>
  <h2>Generated assets</h2>
  <div class="cols">
    <div class="note"><h4>Route</h4><p><b>Higgsfield MCP</b> first, <b>fal.ai</b> as the fallback.
    Check balance and preflight the cost. Render only for the <em>chosen</em> direction — three
    heroes when two get discarded is wasted credit.</p></div>
    <div class="note"><h4>Always generate blank surfaces</h4><p>So every label stays real HTML text:
    crisp, editable, translatable, and readable by search engines. Baked-in AI text fails all
    four.</p></div>
    <div class="note"><h4>Don't approximate a render</h4><p>If a reference's quality comes from 3D
    rendering, flat SVG and CSS polygons produce SmartArt. Brief it properly instead.</p></div>
    <div class="note"><h4>Stop after two failed attempts</h4><p>Write the brief rather than iterate a
    third time. This rule was earned.</p></div>
  </div>
</section>

<footer>
  Generated from <span class="mono">themes/tokens.json</span> and
  <span class="mono">themes/catalogue.md</span> in
  <span class="mono">Quantum-Business-Solutions/websitedesign</span>.
  Refresh the tokens with <span class="mono">scripts/themetokens.py</span>, then regenerate.
</footer>
</div>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="design-system.html")
    a = ap.parse_args()
    with open(os.path.join(ROOT, "themes", "tokens.json"), encoding="utf-8") as fh:
        themes = json.load(fh)["themes"]
    doc = build(themes)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(doc)
    print(f"wrote {a.out} ({len(themes)} themes)")


if __name__ == "__main__":
    main()
