"""Move identical inline <style> and <script> blocks out of every built page into shared files, per direction.

usage: dedupe_assets.py OUT_DIR

A block that appears on at least MIN_PAGES pages of a direction (byte-identical) becomes <direction>/_shared/<hash>.css or .js,
and the page gets <link rel=stylesheet href=...> or <script src=...> in the same position, so order and behaviour are unchanged.
Pages must be opened over http or file:// from the same folder tree (relative paths). JSON-LD and small blocks stay inline.

Performance post-processing on the same pass (all skipped when the inputs are missing, so other clients are unaffected):
  * Self-hosted fonts: when OUT/assets/fonts/inter-latin-var.woff2 and opensans-latin-var.woff2 exist, the Google Fonts @import
    (a render-blocking CSS -> CSS -> font chain) is replaced by local @font-face rules with font-display:swap, plus metric-matched
    "Inter Fallback" / "Open Sans Fallback" faces (size-adjust, ascent/descent overrides on Arial) so the swap does not move text.
  * Head hints: preload for the main shared stylesheet and the two font files (crossorigin), and the now useless preconnects to
    fonts.googleapis.com / fonts.gstatic.com are dropped.
  * Shared scripts that sit after the last inline script get defer (execution order among them is unchanged), so they download
    in parallel with the parser instead of blocking it."""
import hashlib, os, re, sys

PRELOAD_FONTS = True   # measured on a throttled HTTP/1.1 test server the two font preloads cost ~250 ms of first paint (they share the line with the CSS); on HTTP/2 hosts CSS has priority. Set False to drop them.
MIN_PAGES = 12
MIN_BYTES = 1500
STYLE = re.compile(r"<style(?P<attrs>[^>]*)>(?P<body>.*?)</style>", re.S | re.I)
SCRIPT = re.compile(r"<script(?P<attrs>(?:(?!src=)[^>])*)>(?P<body>.*?)</script>", re.S | re.I)


UNI = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
FONTS = (("Inter", "inter-latin-var.woff2", "400 800"), ("Open Sans", "opensans-latin-var.woff2", "400 800"))
# Metrics measured against Arial (Liberation Sans) with the real files: [size-adjust, ascent, descent] for weights 400-500 and 600-800.
FALLBACK = {"Inter": ((106, 91.4, 22.7), (102.5, 94.5, 23.5)), "Open Sans": ((103.5, 103.3, 28.3), (105, 101.8, 27.9))}
FONT_IMPORT = re.compile(r"@import\s+url\(\s*['\"]?https://fonts\.googleapis\.com[^)]*\)\s*;?")
HEAD_PRECONNECT = re.compile(r'<link rel="preconnect" href="https://fonts\.(?:googleapis|gstatic)\.com"(?: crossorigin)?>\s*')


def local_fonts(out):
    return all(os.path.exists(os.path.join(out, "assets", "fonts", f)) for _, f, _ in FONTS)


def font_css(rel):
    """@font-face rules; rel is the path from the stylesheet (or page, if inline) to the assets folder."""
    r = []
    for fam, f, w in FONTS:
        r.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;src:url({rel}/fonts/{f}) format('woff2');unicode-range:{UNI}}}")
        (sa, asc, desc), (sb, ascb, descb) = FALLBACK[fam]
        r.append(f"@font-face{{font-family:'{fam} Fallback';font-weight:400 500;src:local('Arial'),local('ArialMT');size-adjust:{sa}%;ascent-override:{asc}%;descent-override:{desc}%;line-gap-override:0%}}")
        r.append(f"@font-face{{font-family:'{fam} Fallback';font-weight:600 800;src:local('Arial Bold'),local('Arial-BoldMT');size-adjust:{sb}%;ascent-override:{ascb}%;descent-override:{descb}%;line-gap-override:0%}}")
    return "\n".join(r) + "\n"


def selfhost_fonts(css, rel):
    """Swap the Google Fonts @import for local faces, and put the metric-matched fallbacks after each local family name."""
    if not FONT_IMPORT.search(css):
        return css
    css = FONT_IMPORT.sub(lambda m: font_css(rel), css, count=1)
    for fam, _, _ in FONTS:
        css = re.sub(r"(?<=[:,\s])'" + re.escape(fam) + r"'(?=\s*,)", f"'{fam}','{fam} Fallback'", css)
    return css


GUARD = re.compile(r"\s*\(function\(\)\{\s*var \w+=document\.getElementById\(\"([^\"]+)\"\);if\(!\w+\)return;")
SCRIPT_TAG = re.compile(r"<script(?P<attrs>[^>]*)>(?P<body>.*?)</script>", re.S | re.I)


def defer_trailing(html):
    """Add defer to src scripts that come after every inline (non JSON-LD) script, so nothing inline can depend on them."""
    tags = list(SCRIPT_TAG.finditer(html))
    last_inline = -1
    for i, m in enumerate(tags):
        a = m.group("attrs").lower()
        if "src=" not in a and "ld+json" not in a and "type=\"module\"" not in a:
            last_inline = i
    out, pos = [], 0
    for i, m in enumerate(tags):
        a = m.group("attrs")
        if i > last_inline and "src=" in a.lower() and not re.search(r"\b(defer|async)\b|type=[\"']module", a, re.I):
            out.append(html[pos:m.start()])
            out.append(f"<script{a} defer>{m.group('body')}</script>")
            pos = m.end()
    out.append(html[pos:])
    return "".join(out)


def pages(root):
    for dp, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(".html"):
                yield os.path.join(dp, f)


def main():
    out = sys.argv[1]
    local = local_fonts(out)
    saved = 0
    for direction in sorted(os.listdir(out)):
        droot = os.path.join(out, direction)
        if not os.path.isdir(droot) or direction in ("assets", "launch-package"):
            continue
        files = list(pages(droot))
        if len(files) < MIN_PAGES:
            continue
        counts = {}
        for fp in files:
            html = open(fp, encoding="utf-8").read()
            seen = set()
            for rx, kind in ((STYLE, "css"), (SCRIPT, "js")):
                for m in rx.finditer(html):
                    attrs, body = m.group("attrs"), m.group("body")
                    if kind == "js" and "ld+json" in attrs.lower():
                        continue
                    if len(body) < MIN_BYTES:
                        continue
                    key = (kind, hashlib.sha1((attrs + "|" + body).encode()).hexdigest()[:12])
                    if key not in seen:
                        seen.add(key)
                        counts[key] = counts.get(key, 0) + 1
        shared = {k for k, n in counts.items() if n >= MIN_PAGES}
        sdir = os.path.join(droot, "_shared")
        os.makedirs(sdir, exist_ok=True)
        written = set()
        for fp in files:
            html = open(fp, encoding="utf-8").read()
            before = len(html.encode())
            rel = os.path.relpath(sdir, os.path.dirname(fp)).replace(os.sep, "/")

            def sub(kind, rx):
                nonlocal_html = []

                def repl(m):
                    attrs, body = m.group("attrs"), m.group("body")
                    if kind == "js" and "ld+json" in attrs.lower():
                        return m.group(0)
                    key = (kind, hashlib.sha1((attrs + "|" + body).encode()).hexdigest()[:12])
                    if key not in shared:
                        return m.group(0)
                    name = f"{key[1]}.{kind}"
                    if kind == "js":
                        # a script whose first statement is `var h=document.getElementById("ID");if(!h)return;` does nothing on a page without that id
                        g = GUARD.match(body)
                        if g and f'id="{g.group(1)}"' not in page_html:
                            return ""
                    if name not in written:
                        sbody = selfhost_fonts(body, os.path.relpath(os.path.join(out, "assets"), sdir).replace(os.sep, "/")) if local and kind == "css" else body
                        open(os.path.join(sdir, name), "w", encoding="utf-8").write(sbody)
                        written.add(name)
                    if kind == "css":
                        media = re.search(r'media="[^"]*"', attrs)
                        return f'<link rel="stylesheet" href="{rel}/{name}"' + (f" {media.group(0)}" if media else "") + ">"
                    return f'<script src="{rel}/{name}"{attrs}></script>'
                return repl

            html = STYLE.sub(sub("css", STYLE), html)
            page_html = html
            html = SCRIPT.sub(sub("js", SCRIPT), html)
            if local:
                arel = os.path.relpath(os.path.join(out, "assets"), os.path.dirname(fp)).replace(os.sep, "/")
                html = STYLE.sub(lambda m: m.group(0) if "fonts.googleapis.com" not in m.group("body") else f"<style{m.group('attrs')}>{selfhost_fonts(m.group('body'), arel)}</style>", html)
                head_end = html.find("</head>")
                link = re.search(r'<link rel="stylesheet" href="[^"]*_shared/[^"]+\.css"[^>]*>', html[:head_end]) if head_end > 0 else None
                if link and "fonts.googleapis.com/css" not in html[:head_end] and 'rel="preload"' not in html[:head_end]:
                    hints = (f'<link rel="preload" href="{link.group(0).split(chr(34))[3]}" as="style">'
                             + ("".join(f'<link rel="preload" href="{arel}/fonts/{f}" as="font" type="font/woff2" crossorigin>' for f in ("opensans-latin-var.woff2", "inter-latin-var.woff2")) if PRELOAD_FONTS else "") + "\n")
                    html = html[:link.start()] + hints + html[link.start():]
                    html = HEAD_PRECONNECT.sub("", html, count=2)
            html = defer_trailing(html)
            open(fp, "w", encoding="utf-8").write(html)
            saved += before - len(html.encode())
        print(f"  {direction}: {len(shared)} shared blocks, {len(files)} pages")
    print(f"dedupe: saved {saved / 1e6:.1f} MB of inline code")


main()
