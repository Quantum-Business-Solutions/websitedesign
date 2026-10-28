#!/usr/bin/env python3
"""Copy the blog's images (featured + body images hosted on vanausdall.com) into HubSpot Files (/vaf/blog) in portal
50498425 and rewrite the URLs in brands/vanausdall.blog.json. Resumable: the source->HubSpot map is brands/vanausdall.blog-images.json.

    CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_blog_images.py
"""
import json, os, re, subprocess, sys, tempfile, time, urllib.parse
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = os.environ["CLIENT_HUBSPOT_TOKEN"]
SITE = "https://www.vanausdall.com"
DATA = os.path.join(ROOT, "brands/vanausdall.blog.json")
MAP = os.path.join(ROOT, "brands/vanausdall.blog-images.json")


def upload(local, name):
    for attempt in range(5):
        out = subprocess.run(["curl", "-s", "-X", "POST", "-H", "@-", "-F", f"file=@{local};filename={name}",
                              "-F", 'options={"access":"PUBLIC_NOT_INDEXABLE","overwrite":true}', "-F", "folderPath=/vaf/blog",
                              "https://api.hubapi.com/files/v3/files"], input=f"Authorization: Bearer {TOKEN}\n".encode(),
                             capture_output=True).stdout
        try:
            d = json.loads(out)
        except ValueError:
            d = {}
        if "defaultHostingUrl" in d:
            return d["defaultHostingUrl"]
        time.sleep(2 + attempt * 3)
    raise RuntimeError(f"upload failed for {name}: {out[:200]!r}")


def main():
    posts = json.load(open(DATA, encoding="utf-8"))
    srcs = set()
    for p in posts:
        if p["featuredImage"].startswith("/"):
            srcs.add(p["featuredImage"])
        srcs.update(s for s in re.findall(r'<img[^>]*?src="([^"]+)"', p["bodyHtml"]) if s.startswith("/"))
    amap = json.load(open(MAP)) if os.path.exists(MAP) else {}
    names = {}
    for s in sorted(srcs):
        names.setdefault(os.path.basename(s), []).append(s)
    clash = {k: v for k, v in names.items() if len(v) > 1}
    if clash:
        raise SystemExit(f"basename collisions: {clash}")
    tmp = tempfile.mkdtemp()
    failed = []

    def one(s):
        if s in amap:
            return
        local = os.path.join(tmp, os.path.basename(s))
        r = subprocess.run(["curl", "-s", "-f", "-m", "60", "-A", "Mozilla/5.0", "-o", local, SITE + urllib.parse.quote(s)])
        if r.returncode or os.path.getsize(local) < 200:
            failed.append(s)
            return
        try:
            amap[s] = upload(local, os.path.basename(s))
        except RuntimeError as e:
            failed.append(s)
            print("  FAIL", e)
            return
        os.unlink(local)
        print("  ok", s)

    with ThreadPoolExecutor(4) as ex:
        list(ex.map(one, sorted(srcs)))
    json.dump(amap, open(MAP, "w"), indent=1, sort_keys=True)
    print(f"{len(amap)} of {len(srcs)} images in HubSpot Files; failed: {failed}")
    # rewrite URLs (idempotent: only /images/... sources are replaced)
    def fix(html_):
        return re.sub(r'(<img[^>]*?src=")(/[^"]+)(")', lambda m: m.group(1) + amap.get(m.group(2), m.group(2)) + m.group(3), html_)
    for p in posts:
        if p["featuredImage"].startswith("/"):
            p["featuredImageSource"] = p["featuredImage"]
            p["featuredImage"] = amap.get(p["featuredImage"], p["featuredImage"])
        p["bodyHtml"] = fix(p["bodyHtml"])
    json.dump(posts, open(DATA, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
