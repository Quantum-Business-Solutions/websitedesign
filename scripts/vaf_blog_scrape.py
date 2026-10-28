#!/usr/bin/env python3
"""Scrape every vanausdall.com blog post into brands/vanausdall.blog.json (normalised: clean semantic HTML).

Reads the live listing (https://www.vanausdall.com/blog, which lists every post with date, teaser, thumbnail and
categories), then each post page. Raw pages are cached in $VAF_BLOG_RAW (default: a temp dir).

    python3 scripts/vaf_blog_scrape.py
"""
import html, json, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.vanausdall.com"
RAW = os.environ.get("VAF_BLOG_RAW") or os.path.join(tempfile.gettempdir(), "vaf-blog-raw")
OUT = os.path.join(ROOT, "brands/vanausdall.blog.json")
CATS = {"ai-consulting": "AI Consulting", "business-phone-systems": "Business Phone Systems",
        "business-process-solutions": "Business Process Solutions", "cloud-solutions": "Cloud Solutions",
        "cybersecurity": "Cybersecurity", "document-conversion": "Document Conversion",
        "document-management": "Document Management", "managed-it": "Managed IT Services",
        "managed-print-services": "Managed Print Services", "news": "News & Press", "physical-security": "Physical Security"}


def get(url, dest=None):
    for _ in range(3):
        r = subprocess.run(["curl", "-s", "-m", "40", "-A", "Mozilla/5.0", "-w", "\n%{http_code}", url], capture_output=True)
        body, _, code = r.stdout.rpartition(b"\n")
        if code == b"200":
            return body.decode("utf-8", "replace")
    return None


def tidy(body, featured):
    b = body.replace("<h2p>", "<h2>").replace("</h2p>", "</h2>")
    if featured:   # the featured image is rendered by the post template, do not repeat it at the top of the body
        b = re.sub(r'^\s*<img [^>]*src="%s"[^>]*>\s*' % re.escape(featured), "", b, count=1)
    b = re.sub(r"<(h[1-6]|p|li|blockquote|cite|q)(\s[^>]*)?>\s+", r"<\1\2>", b)
    b = re.sub(r"\s+</(h[1-6]|p|li|blockquote|cite|q)>", r"</\1>", b)
    b = re.sub(r'rel="\s*noopener"', 'rel="noopener"', b)
    # internal absolute links -> site-relative; category archives -> tag archives
    b = re.sub(r'(href=")https?://(?:www\.)?vanausdall\.com(/blog/)', r"\1\2", b)
    b = re.sub(r'href="/blog/(' + "|".join(CATS) + r')/?"', r'href="/blog/tag/\1"', b)
    # a bare link that is a button (press release PDFs) becomes a paragraph holding a themed button
    b = re.sub(r'(?<!>)\s*<a ([^>]*)class="btn"([^>]*)>(.*?)</a>', r'<p><a \1class="q-btn"\2>\3</a></p>', b, flags=re.S)
    b = b.replace('class="btn"', 'class="q-btn"')
    b = re.sub(r'href="(www\.[^"]+)"', r'href="https://\1"', b)   # scheme-less external links would resolve as relative paths
    b = re.sub(r'src="images/', 'src="/images/', b)
    b = re.sub(r"\n{3,}", "\n\n", b)
    return b.strip()


def main():
    os.makedirs(RAW, exist_ok=True)
    lst = get(SITE + "/blog")
    items = []
    for m in re.finditer(r'<div class="post" data-date="([^"]+)">(.*?)\n</div>', lst, re.S):
        d, b = m.groups()
        sl = re.search(r'<h2><a href="/blog/([^"]+)">', b).group(1)
        im = re.search(r'<div class="postThumbnail"><img [^>]*?src="([^"]+)" alt="([^"]*)"', b)
        tz = re.search(r'<p class="post-teaser">(.*?)</p>', b, re.S)
        items.append({"slug": sl, "date": d, "thumb": ("/" + im.group(1).lstrip("/")) if im else "", "alt": html.unescape(im.group(2)) if im else "",
                      "teaser": html.unescape(tz.group(1)).strip() if tz else ""})

    def fetch(it):
        p = os.path.join(RAW, it["slug"] + ".html")
        if not (os.path.exists(p) and os.path.getsize(p) > 2000):
            t = get(f"{SITE}/blog/{it['slug']}")
            if t:
                open(p, "w", encoding="utf-8").write(t)
        return it["slug"] if not os.path.exists(p) else None
    with ThreadPoolExecutor(6) as ex:
        missing = [x for x in ex.map(fetch, items) if x]

    posts = []
    for it in items:
        p = os.path.join(RAW, it["slug"] + ".html")
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        main_ = re.search(r"<main>\s*<div class=\"wrap\">\s*(.*?)</main>", s, re.S).group(1)
        title = html.unescape(re.search(r"<h1>(.*?)</h1>", main_, re.S).group(1)).strip()
        meta = lambda n: (re.search(r'<meta name="%s" content="([^"]*)"' % n, s) or [None, ""])[1]
        cats = [c for c in re.findall(r'href="/blog/([^/"]+)/"', main_.split('<p class="postcats">')[-1])]
        tags = []
        for t in html.unescape(meta("tags")).split(","):
            t = t.strip()
            if t and t.lower() not in [x.lower() for x in tags]:
                tags.append(t)
        body = re.search(r"</h1>\s*<p>[^<]*</p>(.*?)(?:<p class=\"posttags\">|<p class=\"postcats\">)", main_, re.S).group(1)
        body = tidy(body, it["thumb"])
        posts.append({
            "slug": it["slug"], "url": f"{SITE}/blog/{it['slug']}", "title": title,
            "htmlTitle": html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1)).strip(),
            "date": it["date"], "author": "Van Ausdall & Farrar",
            "categories": [{"slug": c, "name": CATS.get(c, c)} for c in cats], "tags": tags,
            "featuredImage": it["thumb"], "featuredImageAlt": it["alt"],
            "teaser": it["teaser"], "metaDescription": html.unescape(meta("description")), "bodyHtml": body,
        })
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    json.dump(posts, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(posts)} posts of {len(items)} listed; unretrievable: {missing}")


if __name__ == "__main__":
    main()
