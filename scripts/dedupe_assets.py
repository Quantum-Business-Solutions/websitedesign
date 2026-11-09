"""Move identical inline <style> and <script> blocks out of every built page into shared files, per direction.

usage: dedupe_assets.py OUT_DIR

A block that appears on at least MIN_PAGES pages of a direction (byte-identical) becomes <direction>/_shared/<hash>.css or .js,
and the page gets <link rel=stylesheet href=...> or <script src=...> in the same position, so order and behaviour are unchanged.
Pages must be opened over http or file:// from the same folder tree (relative paths). JSON-LD and small blocks stay inline."""
import hashlib, os, re, sys

MIN_PAGES = 12
MIN_BYTES = 1500
STYLE = re.compile(r"<style(?P<attrs>[^>]*)>(?P<body>.*?)</style>", re.S | re.I)
SCRIPT = re.compile(r"<script(?P<attrs>(?:(?!src=)[^>])*)>(?P<body>.*?)</script>", re.S | re.I)


def pages(root):
    for dp, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(".html"):
                yield os.path.join(dp, f)


def main():
    out = sys.argv[1]
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
                    if name not in written:
                        open(os.path.join(sdir, name), "w", encoding="utf-8").write(body)
                        written.add(name)
                    if kind == "css":
                        media = re.search(r'media="[^"]*"', attrs)
                        return f'<link rel="stylesheet" href="{rel}/{name}"' + (f" {media.group(0)}" if media else "") + ">"
                    return f'<script src="{rel}/{name}"{attrs}></script>'
                return repl

            html = STYLE.sub(sub("css", STYLE), html)
            html = SCRIPT.sub(sub("js", SCRIPT), html)
            open(fp, "w", encoding="utf-8").write(html)
            saved += before - len(html.encode())
        print(f"  {direction}: {len(shared)} shared blocks, {len(files)} pages")
    print(f"dedupe: saved {saved / 1e6:.1f} MB of inline code")


main()
