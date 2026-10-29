#!/usr/bin/env python3
"""Apply TL;DR and FAQ (brands/vanausdall.blog-enrich.json) to the published VAF blog posts.

    CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_blog_enrich_apply.py [--limit N] [--slug SLUG]
Idempotent: a post that already carries the <!--vaf-enrich--> marker is skipped. Posts marked skip:true are left alone."""
import html, json, os, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = os.environ["CLIENT_HUBSPOT_TOKEN"]
import re
ENRICH = {re.sub(r"-+", "-", k): v for k, v in json.load(open(os.path.join(ROOT, "brands/vanausdall.blog-enrich.json"), encoding="utf-8")).items()}   # the importer collapses double hyphens in slugs
MARK = "<!--vaf-enrich-->"


def api(method, path, body=None, tries=5):
    for i in range(tries):
        req = urllib.request.Request("https://api.hubapi.com" + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                     headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                t = r.read()
                return json.loads(t) if t else {}
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                time.sleep(2 ** (i + 1)); continue
            raise RuntimeError(f"{method} {path} -> {e.code} {e.read()[:300]!r}")


def tldr_html(items):
    lis = "".join(f'<li style="margin:0 0 8px">{html.escape(t)}</li>' for t in items)
    return (f'{MARK}<aside class="vaf-tldr" style="background:#f3f7fb;border-left:5px solid #2a71af;border-radius:12px;padding:20px 24px;margin:0 0 28px">'
            f'<p style="margin:0 0 10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:13px;color:#2a71af">TL;DR</p>'
            f'<ul style="margin:0;padding-left:20px">{lis}</ul></aside>')


def faq_html(faqs):
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faqs]}
    body = "".join(f'<h3>{html.escape(f["q"])}</h3><p>{html.escape(f["a"])}</p>' for f in faqs)
    js = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")
    return (f'<section class="vaf-faq-post"><h2>Frequently asked questions</h2>{body}</section>'
            f'<script type="application/ld+json">{js}</script>')


def all_posts():
    out, after = [], None
    while True:
        r = api("GET", "/cms/v3/blogs/posts?limit=100&state=PUBLISHED" + (f"&after={after}" if after else ""))
        out += r.get("results", [])
        after = (r.get("paging") or {}).get("next", {}).get("after")
        if not after:
            return out


def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 10 ** 9
    only = sys.argv[sys.argv.index("--slug") + 1] if "--slug" in sys.argv else None
    done = skipped = missing = fail = 0
    seen = set()
    for p in all_posts():
        slug = re.sub(r"-+", "-", p["slug"].split("/", 1)[-1])
        e = ENRICH.get(slug)
        if not e or e.get("skip") or (only and slug != only):
            continue
        seen.add(slug)
        if MARK in p["postBody"]:
            skipped += 1; continue
        if done >= limit:
            break
        try:
            body = tldr_html(e["tldr"]) + p["postBody"] + faq_html(e["faq"])
            api("PATCH", f"/cms/v3/blogs/posts/{p['id']}/draft", {"postBody": body})
            api("POST", f"/cms/v3/blogs/posts/{p['id']}/draft/push-live")
            done += 1; print("  enriched", slug, flush=True)
        except Exception as ex:
            fail += 1; print("  FAIL", slug, str(ex)[:200], flush=True)
        time.sleep(0.25)
    todo = [s for s, v in ENRICH.items() if not v.get("skip")]
    print(f"done {done}, already {skipped}, failed {fail}; enrichable {len(todo)}, not found as published: {len([s for s in todo if s not in seen])}")


main()
