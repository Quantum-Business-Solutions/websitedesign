#!/usr/bin/env python3
"""Give every published VAF blog post a clean summary.

    CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_blog_summary_fix.py [--dry]
HubSpot builds a post's summary from its body when none is set. Once the TL;DR box sits at the top of the body, the summary
(and so the blog card excerpts and the standfirst under the H1) starts with the whole TL;DR box. This sets postSummary to the
post's own meta description. Idempotent: posts whose summary already equals the meta description are skipped."""
import json, os, sys, time, urllib.request, urllib.error

TOKEN = os.environ["CLIENT_HUBSPOT_TOKEN"]


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


def main():
    dry = "--dry" in sys.argv
    posts, after = [], None
    while True:
        r = api("GET", "/cms/v3/blogs/posts?limit=100&state=PUBLISHED" + (f"&after={after}" if after else ""))
        posts += r.get("results", [])
        after = (r.get("paging") or {}).get("next", {}).get("after")
        if not after:
            break
    done = skipped = nometa = fail = 0
    for p in posts:
        meta = (p.get("metaDescription") or "").strip()
        if not meta:
            nometa += 1; continue
        if (p.get("postSummary") or "").strip() == meta:
            skipped += 1; continue
        if dry:
            done += 1; continue
        try:
            api("PATCH", f"/cms/v3/blogs/posts/{p['id']}/draft", {"postSummary": meta})
            api("POST", f"/cms/v3/blogs/posts/{p['id']}/draft/push-live")
            done += 1; print("  summary", p["slug"].rsplit("/", 1)[-1], flush=True)
        except Exception as ex:
            fail += 1; print("  FAIL", p["slug"], str(ex)[:200], flush=True)
        time.sleep(0.25)
    print(f"{'would fix' if dry else 'fixed'} {done}, already clean {skipped}, no meta description {nometa}, failed {fail}")


main()
