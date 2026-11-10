#!/usr/bin/env python3
"""Turn a built preview direction folder into a launch-ready copy for the real domain.

usage: launch_rewrite.py BUILT_DIRECTION_DIR DOMAIN OUT_DIR   (DOMAIN like https://www.example.com)

For every .html file:
  - canonical, og:url and og:image / twitter:image are rewritten from the staging host to DOMAIN (the direction prefix is dropped:
    https://staging/clean/services/x.html -> DOMAIN/services/x ; the home page -> DOMAIN/)
  - the robots meta (noindex, nofollow) is removed
  - the preview direction switcher (nav.pv-switch, details.pv-switch-m and its embed script) is removed
Everything else is copied as is. The site assets folder next to the direction folder (../assets) is copied into OUT_DIR/assets,
and page links of the form ../assets/ are rewritten to assets/ so the folder stands on its own."""
import os, re, shutil, sys


def rewrite(html, domain, rel):
    path = "" if rel == "index.html" else rel[:-5] if rel.endswith(".html") else rel
    page_url = f"{domain}/{path}"
    html = re.sub(r'<meta name="robots" content="[^"]*">\n?', "", html)
    html = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + page_url + m.group(2), html)
    html = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + page_url + m.group(2), html)

    def img(m):
        v = m.group(2)
        v = re.sub(r"^https?://[^/]+/(?:s/[0-9a-f]{16,}/)?(?:(?:clean|showcase|press)/)?", "", v)
        return m.group(1) + f"{domain}/{v}" + m.group(3)
    html = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")([^"]*)(")', img, html)
    html = re.sub(r'<nav class="pv-switch".*?</nav>', "", html, flags=re.S)
    html = re.sub(r'<details class="pv-switch-m".*?</details>', "", html, flags=re.S)
    html = html.replace('<script>if(top!==self){document.documentElement.classList.add("embedded")}</script>', "")
    # the design-preview bar script that runs first in <body> (preview_notice.NOTICE_BAR_JS) has no job on the live domain
    html = re.sub(r"(<body>\n)<script>[^<]*?pv-notice[^<]*?</script>\n", r"\1", html, count=1, flags=re.S)
    return html


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    src, domain, out = sys.argv[1].rstrip("/"), sys.argv[2].rstrip("/"), sys.argv[3].rstrip("/")
    n = 0
    for root, _, files in os.walk(src):
        for fn in files:
            f = os.path.join(root, fn)
            rel = os.path.relpath(f, src).replace(os.sep, "/")
            dst = os.path.join(out, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if fn.endswith(".html"):
                depth = rel.count("/")
                h = rewrite(open(f, encoding="utf-8").read(), domain, rel)
                up = "../" * (depth + 1)
                h = h.replace(f'"{up}assets/', f'"{"../" * depth}assets/').replace(f"'{up}assets/", f"'{'../' * depth}assets/").replace(f", {up}assets/", f", {'../' * depth}assets/")
                open(dst, "w", encoding="utf-8").write(h)
                n += 1
            elif fn.endswith(".css") and "assets/" in open(f, encoding="utf-8", errors="ignore").read():
                # shared stylesheets (_shared/*.css) point at the site assets folder with url(../../assets/...); the launch copy keeps
                # the assets one level above the stylesheet's folder, so each url() loses one "../"
                depth = rel.count("/")
                css = open(f, encoding="utf-8").read()
                css = css.replace(f"url({'../' * (depth + 1)}assets/", f"url({'../' * depth}assets/")
                open(dst, "w", encoding="utf-8").write(css)
            else:
                shutil.copy2(f, dst)
    assets = os.path.join(os.path.dirname(src), "assets")
    if os.path.isdir(assets):
        shutil.copytree(assets, os.path.join(out, "assets"), dirs_exist_ok=True)
    print(f"launch-ready copy: {n} pages -> {out} for {domain}")


if __name__ == "__main__":
    main()
