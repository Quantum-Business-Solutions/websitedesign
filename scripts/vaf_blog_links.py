#!/usr/bin/env python3
"""Add contextual internal links from published VAF blog posts to the matching service pages.

    CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_blog_links.py [--dry] [--limit N]
First mention only, at most four links per post, never inside headings, existing links, the TL;DR box or the FAQ. Idempotent (marker)."""
import json, os, re, sys, time, urllib.request, urllib.error

TOKEN = os.environ["CLIENT_HUBSPOT_TOKEN"]
MARK = "<!--vaf-links-->"
PHRASES = [
    (r"Technology Strength Assessment", "/technology-strength-assessment"),
    (r"managed IT services?", "/services/managed-it"),
    (r"managed print(?: services?)?", "/services/managed-print"),
    (r"business phone systems?", "/services/business-phone-systems"),
    (r"unified communications", "/services/unified-communications"),
    (r"cyber ?security", "/services/cybersecurity"),
    (r"document management", "/services/document-management"),
    (r"document conversion", "/services/document-conversion"),
    (r"AI consulting", "/services/ai-consulting"),
    (r"disaster recovery|data backup", "/services/cloud"),
    (r"contact center", "/services/call-center-services"),
    (r"production print", "/services/production-print"),
    (r"copiers?", "/services/copiers"),
    (r"physical security|video surveillance", "/services/physical-security"),
    (r"network security", "/services/network-security"),
]
SKIP = {"a", "h1", "h2", "h3", "h4", "h5", "h6", "script", "style", "aside", "button", "figcaption"}


def api(method, path, body=None, tries=5):
    for i in range(tries):
        req = urllib.request.Request("https://api.hubapi.com" + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                     headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                t = r.read(); return json.loads(t) if t else {}
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                time.sleep(2 ** (i + 1)); continue
            raise RuntimeError(f"{method} {path} -> {e.code} {e.read()[:200]!r}")


def link_body(html):
    parts = re.split(r"(<[^>]+>)", html)
    stack, used, added, in_faq = [], set(), 0, False
    out = []
    for tok in parts:
        if tok.startswith("<"):
            m = re.match(r"<(/?)([a-zA-Z0-9]+)", tok)
            if m:
                closing, name = m.group(1) == "/", m.group(2).lower()
                if name == "section" and "vaf-faq-post" in tok and not closing: in_faq = True
                if name == "section" and closing and in_faq: in_faq = False
                if name in SKIP and not tok.endswith("/>"):
                    if closing:
                        if name in stack: stack.remove(name)
                    else: stack.append(name)
            out.append(tok); continue
        if stack or in_faq or added >= 4 or not tok.strip():
            out.append(tok); continue
        for rx, href in PHRASES:
            if added >= 4 or href in used: continue
            m = re.search(r"\b(" + rx + r")\b", tok, re.I)
            if m:
                tok = tok[:m.start()] + f'<a href="{href}">{m.group(1)}</a>' + tok[m.end():]
                used.add(href); added += 1
        out.append(tok)
    return "".join(out), added


def main():
    dry = "--dry" in sys.argv
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 10 ** 9
    after, posts = None, []
    while True:
        r = api("GET", "/cms/v3/blogs/posts?limit=100&state=PUBLISHED" + (f"&after={after}" if after else ""))
        posts += r.get("results", []); after = (r.get("paging") or {}).get("next", {}).get("after")
        if not after: break
    done = skipped = nolink = fail = 0
    for p in posts:
        body = p["postBody"]
        if MARK in body: skipped += 1; continue
        if done >= limit: break
        new, n = link_body(body)
        if n == 0: nolink += 1; continue
        if dry: print(f"  would link {n}: {p['slug']}"); done += 1; continue
        try:
            api("PATCH", f"/cms/v3/blogs/posts/{p['id']}/draft", {"postBody": MARK + new})
            api("POST", f"/cms/v3/blogs/posts/{p['id']}/draft/push-live")
            done += 1; print("  linked", n, p["slug"], flush=True)
        except Exception as ex:
            fail += 1; print("  FAIL", p["slug"], str(ex)[:160], flush=True)
        time.sleep(0.25)
    print(f"done {done}, already {skipped}, no link targets {nolink}, failed {fail}, of {len(posts)}")


main()
