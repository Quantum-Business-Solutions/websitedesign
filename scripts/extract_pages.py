#!/usr/bin/env python3
"""Extract structured copy from a crawled site for page-for-page migration.

  python3 scripts/extract_pages.py --fetch-log LOG --pages DIR --out brands/<slug>.pages.json \
      [--policies DIR]  # rendered policy HTML named <slug>.html, keyed by the last URL segment

fetch.log lines: "<status> <hash> <url>", pages/<hash>.html as saved by curl. For each page:
title, meta, H1, ordered blocks of heading, paragraphs, bullets, og:image and a word count. Pages
whose copy lives in <div>s fall back to a flat split. Policy pages served by an embed (Termageddon,
Termly) have no text in the crawl; pass --policies with the rendered HTML fetched from the
provider's render endpoint and it replaces the placeholder blocks.
"""
import argparse, glob, html, json, os, re


def txt(x):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))).strip()


def blocks_from(body):
    blocks, cur = [], {"heading": "", "paras": [], "bullets": []}
    for tag, inner in re.findall(r"<(h2|h3|p|li)[^>]*>(.*?)</\1>", body, re.S | re.I):
        t = txt(inner)
        if not t or len(t) < 3:
            continue
        if tag.lower() in ("h2", "h3"):
            if cur["paras"] or cur["bullets"] or cur["heading"]:
                blocks.append(cur)
            cur = {"heading": t, "paras": [], "bullets": []}
        elif tag.lower() == "p":
            if len(t) > 40 and t not in cur["paras"]:
                cur["paras"].append(t)
        else:
            if 3 < len(t) < 220 and t not in cur["bullets"]:
                cur["bullets"].append(t)
    if cur["paras"] or cur["bullets"] or cur["heading"]:
        blocks.append(cur)
    return blocks


def flat_blocks(body):
    flat = re.sub(r"<(br|/p|/div|/li|/h\d|/tr)[^>]*>", "\n", body, flags=re.I)
    flat = html.unescape(re.sub(r"<[^>]+>", " ", flat))
    paras = [re.sub(r"\s+", " ", x).strip() for x in flat.split("\n")]
    seen, out = set(), []
    for p in paras:
        if len(p) > 60 and p not in seen:
            seen.add(p); out.append(p)
    return [{"heading": "", "paras": out[:40], "bullets": []}] if out else []


BAD_HEADINGS = ("cookie", "privacy policy", "all rights reserved", "schedule a consultation", "speak with a solutions expert", "read full story", "recent posts", "categories")
PLACEHOLDERS = ("Please wait while the policy is loaded", "There was an error loading this policy")


def words_of(blocks):
    return sum(len(p.split()) for b in blocks for p in b["paras"]) + sum(len(x.split()) for b in blocks for x in b["bullets"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch-log", required=True); ap.add_argument("--pages", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--policies", help="directory of rendered policy HTML, <last-url-segment>.html")
    a = ap.parse_args()
    out = []
    for line in open(a.fetch_log):
        code, f, u = line.split(" ", 2); u = u.strip()
        h = open(os.path.join(a.pages, f + ".html"), encoding="utf-8", errors="ignore").read()
        path = re.sub(r"^https?://[^/]+", "", u) or "/"
        title = txt((re.search(r"<title[^>]*>(.*?)</title>", h, re.S | re.I) or [None, ""])[1]) if re.search(r"<title", h, re.I) else ""
        meta = html.unescape((re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', h, re.I) or [None, ""])[1]) if re.search(r'name=["\']description', h, re.I) else ""
        h1 = txt((re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S | re.I) or [""])[0])
        body = re.sub(r"<(script|style|nav|footer|header|form|noscript|select)[^>]*>.*?</\1>", "", h, flags=re.S | re.I)
        m = re.search(r"<main[^>]*>(.*?)</main>", body, re.S | re.I); body = m.group(1) if m else body
        blocks = blocks_from(body)
        if words_of(blocks) < 60:
            blocks = flat_blocks(body) or blocks
        blocks = [b for b in blocks if b["heading"].lower() not in BAD_HEADINGS]
        embedded = False
        if a.policies and any(ph in p for b in blocks for p in b["paras"] for ph in PLACEHOLDERS):
            pf = os.path.join(a.policies, path.rstrip("/").split("/")[-1] + ".html")
            if os.path.exists(pf):
                ph = open(pf, encoding="utf-8", errors="ignore").read()
                pb = blocks_from(ph)
                if words_of(pb) < 60:
                    pb = flat_blocks(ph)
                if pb:
                    blocks = pb; embedded = True
        og = (re.search(r'property=["\']og:image["\'][^>]+content=["\']([^"\']*)', h, re.I) or [None, ""])[1] if re.search(r'og:image', h) else ""
        out.append(dict(url=path, title=title, meta=meta, h1=h1, blocks=blocks, og=og, words=words_of(blocks), embedded_policy=embedded))
    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
    thin = [o["url"] for o in out if o["words"] < 80]
    print(f"{len(out)} pages; {len(thin)} under 80 words: {thin[:12]}")
    print(f"embedded policies replaced: {sum(1 for o in out if o['embedded_policy'])}")


if __name__ == "__main__":
    main()
