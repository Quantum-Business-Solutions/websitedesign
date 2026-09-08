#!/usr/bin/env python3
"""Score every page of a site for search and AI-answer readiness.

Two modes:
  --fetch-log LOG --pages DIR   pages fetched with curl (log lines: "<status> <hash> <url>")
  --dir DIR --base URL          a generated build on disk (every *.html under DIR)

Output: JSON with summary, site and rows; optional CSV. Same seventeen checks and weights
as the hub and the SEO report, so a client site and its rebuild are scored identically.
"""
import argparse, csv, glob, html, json, os, re, sys

CITY_WORDS = ("indianapolis", "indiana", "fort wayne", "evansville", "bloomington", "carmel", "fishers", "noblesville", "greenwood", "muncie", "columbus", "south bend")
WEIGHTS = dict(title=6, city=6, meta=5, h1=5, h2=5, qh=8, words=10, depth=4, faq=14, stype=10, local=4, review=6, alt=4, links=3, canon=3, og=3, cta=4)


def txt(x):
    return html.unescape(re.sub(r"<[^>]+>", "", x)).strip()


def classify(path):
    p = path.lower()
    if p.startswith("/policies") or "thank" in p or p in ("/sitemap", "/standard.html", "/index.html") and False:
        return "policy"
    if p.startswith("/case-studies/") and p not in ("/case-studies/", "/case-studies.html"):
        return "case study"
    if p.startswith("/blog/") or p.startswith("/blog?p=") or "/posts/" in p:
        return "post"
    if p.startswith("/locations/") or any(p.startswith("/" + c.replace(" ", "-")) for c in CITY_WORDS):
        return "city"
    if p.startswith("/services/") or p.startswith("/industries/") or any(k in p for k in ("/information", "/communication", "/print", "/process", "/copier", "/document-", "/managed-", "/ai", "/knowbe4")):
        return "service"
    return "company"


def parse(h, url, path, city_words=CITY_WORDS):
    g = lambda rx: (re.search(rx, h, re.I | re.S).group(1) if re.search(rx, h, re.I | re.S) else "")
    title = txt(g(r"<title[^>]*>(.*?)</title>"))
    meta = html.unescape(g(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)'))
    h1s = [txt(x) for x in re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S | re.I)]
    h2s = [txt(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", h, re.S | re.I)]
    h3s = [txt(x) for x in re.findall(r"<h3[^>]*>(.*?)</h3>", h, re.S | re.I)]
    qh = sum(1 for x in h2s + h3s if x.rstrip().endswith("?"))
    types = set()
    for blk in re.findall(r'<script[^>]+ld\+json[^>]*>(.*?)</script>', h, re.S | re.I):
        types.update(re.findall(r'"@type"\s*:\s*"([^"]+)"', blk))
    body = re.sub(r"<(script|style|nav|footer|header)[^>]*>.*?</\1>", "", h, flags=re.S | re.I)
    m = re.search(r"<main[^>]*>(.*?)</main>", body, re.S | re.I)
    body = m.group(1) if m else body
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    imgs = re.findall(r"<img\b[^>]*>", h, re.I)
    noalt = sum(1 for i in imgs if not re.search(r'alt=["\'][^"\']+["\']', i, re.I) and not re.search(r'alt=["\']["\']', i, re.I) and not re.search(r'role=["\']presentation', i, re.I))
    links = re.findall(r'<a\b[^>]*href=["\']([^"\'#]+)', h, re.I)
    host = re.sub(r"^https?://", "", url).split("/")[0]
    internal = sum(1 for l in links if not l.startswith(("http", "mailto:", "tel:")) or host in l)
    external = sum(1 for l in links if l.startswith("http") and host not in l)
    og = g(r'property=["\']og:image["\'][^>]+content=["\']([^"\']*)')
    canon = g(r'rel=["\']canonical["\'][^>]+href=["\']([^"\']*)')
    form = bool(re.search(r"<form\b", h, re.I)); tel = bool(re.search(r'href=["\']tel:', h, re.I))
    tl = title.lower()
    city = any(c in tl for c in city_words)
    ptype = classify(path)
    r = dict(url=path, type=ptype, title=title, title_len=len(title), city=city, meta=meta, meta_len=len(meta), h1=h1s[0] if h1s else "", h1_count=len(h1s), h2_count=len(h2s), h3_count=len(h3s), question_headings=qh,
             words=words, images=len(imgs), images_no_alt=noalt, internal_links=internal, external_links=external, canonical=bool(canon), og_image=bool(og), stock_og=(og == "" or og.endswith("artificial-intelligence.jpg")),
             faq="FAQPage" in types, service=bool({"Service", "ITService", "ProfessionalService"} & types), local="LocalBusiness" in types, review=bool({"Review", "AggregateRating"} & types), article=bool({"Article", "BlogPosting", "NewsArticle"} & types), breadcrumb="BreadcrumbList" in types,
             schema=", ".join(sorted(types)), has_form=form, tel_link=tel)
    pts = 0; rec = []
    def chk(ok, key, fix):
        nonlocal pts
        if ok: pts += WEIGHTS[key]
        else: rec.append((WEIGHTS[key], fix))
    chk(30 <= r["title_len"] <= 60, "title", "Retitle to 30 to 60 characters")
    chk(city, "city", "Add Indianapolis or the service city to the title")
    chk(70 <= r["meta_len"] <= 160, "meta", "Write a 70 to 160 character meta description that answers the query")
    chk(r["h1_count"] == 1, "h1", "Use exactly one H1 that names the service and the city")
    chk(r["h2_count"] >= 2, "h2", "Structure the page with at least two H2 sections")
    chk(qh >= 1, "qh", "Add question-form H2s that an assistant can quote (what, how much, is it)")
    chk(words >= 300, "words", "Write at least 300 words of body copy; 600 to 900 for a service page")
    chk(words >= 600 or ptype in ("policy", "case study"), "depth", "Deepen to 600 words or more")
    chk(r["faq"] or ptype == "policy", "faq", "Add a five-question FAQ marked up as FAQPage")
    stype_ok = r["service"] if ptype in ("service", "city") else (r["article"] if ptype in ("case study", "post") else True)
    chk(stype_ok, "stype", "Add Service schema (or Article on case studies and posts) declaring what the page offers")
    chk(r["local"], "local", "Add LocalBusiness schema")
    chk(r["review"] or ptype in ("policy", "case study", "post"), "review", "Add Review or AggregateRating schema from real Google reviews")
    chk(noalt == 0, "alt", "Give every image descriptive alt text")
    chk(internal >= 10, "links", "Link to at least ten related pages")
    chk(bool(canon), "canon", "Set a self-referencing canonical")
    chk(not r["stock_og"], "og", "Replace the stock share image with a branded one")
    chk(form or tel or ptype == "policy", "cta", "Put a form or a click-to-call number on the page")
    mx = sum(WEIGHTS.values())
    r["score"] = round(100 * pts / mx)
    r["grade"] = "A" if r["score"] >= 85 else "B" if r["score"] >= 70 else "C" if r["score"] >= 55 else "D" if r["score"] >= 40 else "F"
    rec.sort(key=lambda x: -x[0]); r["recommendations"] = [f for _, f in rec[:4]]; r["issues"] = len(rec)
    return r


def summarise(rows):
    n = len(rows); c = lambda k: sum(1 for r in rows if r[k])
    types = sorted({r["type"] for r in rows})
    return dict(pages=n, avg_score=round(sum(r["score"] for r in rows) / max(1, n)), faq=c("faq"), service=c("service"), local=c("local"), review=c("review"), article=c("article"), breadcrumb=c("breadcrumb"), city_in_title=c("city"),
                thin=sum(1 for r in rows if r["words"] < 300), no_h1=sum(1 for r in rows if r["h1_count"] == 0), question_headings=sum(1 for r in rows if r["question_headings"] > 0),
                images_no_alt=sum(r["images_no_alt"] for r in rows), no_canonical=sum(1 for r in rows if not r["canonical"]), stock_og=c("stock_og"), has_form=c("has_form"),
                grades={g: sum(1 for r in rows if r["grade"] == g) for g in "ABCDF"},
                by_type={t: dict(pages=sum(1 for r in rows if r["type"] == t), avg=round(sum(r["score"] for r in rows if r["type"] == t) / max(1, sum(1 for r in rows if r["type"] == t)))) for t in types})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch-log"); ap.add_argument("--pages"); ap.add_argument("--dir"); ap.add_argument("--base", default="https://example.com")
    ap.add_argument("--out", required=True); ap.add_argument("--csv"); ap.add_argument("--exclude", default="")
    a = ap.parse_args()
    rows = []
    if a.fetch_log:
        for line in open(a.fetch_log):
            code, f, u = line.split(" ", 2); u = u.strip()
            h = open(os.path.join(a.pages, f + ".html"), encoding="utf-8", errors="ignore").read()
            path = re.sub(r"^https?://[^/]+", "", u) or "/"
            rows.append(parse(h, u, path))
    else:
        ex = [x for x in a.exclude.split(",") if x]
        for fp in sorted(glob.glob(os.path.join(a.dir, "**", "*.html"), recursive=True)):
            rel = "/" + os.path.relpath(fp, a.dir).replace(os.sep, "/")
            if any(e in rel for e in ex): continue
            h = open(fp, encoding="utf-8", errors="ignore").read()
            rows.append(parse(h, a.base.rstrip("/") + rel, rel))
    out = dict(summary=summarise(rows), rows=rows)
    json.dump(out, open(a.out, "w"), indent=1)
    if a.csv:
        with open(a.csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader()
            for r in rows: w.writerow({k: (" | ".join(v) if isinstance(v, list) else v) for k, v in r.items()})
    s = out["summary"]; print(f"{s['pages']} pages, average {s['avg_score']}, grades {s['grades']}")
    worst = sorted(rows, key=lambda r: r["score"])[:8]
    for r in worst: print(f"  {r['score']:3} {r['grade']} {r['url']}  {r['recommendations'][:3]}")
    from collections import Counter
    fails = Counter(f for r in rows for f in r["recommendations"])
    print("most common fixes:"); [print(f"  {c:3}  {f}") for f, c in fails.most_common(10)]


if __name__ == "__main__":
    main()
