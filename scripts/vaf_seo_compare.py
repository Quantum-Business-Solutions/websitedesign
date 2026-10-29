#!/usr/bin/env python3
"""Before and after SEO/AEO scorecard: the old site's September crawl against the live rebuild, same 17 checks.

    python3 scripts/vaf_seo_compare.py [base-url]
Reads brands/vanausdall.seo-full.json (before) and brands/vanausdall.redirects.json (old URL to new URL),
fetches each new page, scores it with scripts/site_audit.parse, and writes brands/vanausdall.seo-compare.json
and brands/vanausdall.seo-compare.md.
"""
import concurrent.futures as cf, json, os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_audit as SA

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://50498425.hs-sites.com").rstrip("/")
before = json.load(open(os.path.join(ROOT, "brands/vanausdall.seo-full.json"), encoding="utf-8"))["rows"]
redirects = {r["from"].rstrip("/") or "/": (r["to"].rstrip("/") or "/") for r in json.load(open(os.path.join(ROOT, "brands/vanausdall.redirects.json"), encoding="utf-8"))}


def fetch(path):
    url = f"{BASE}{path}" + ("?" if "?" not in path else "&") + f"cb={int(time.time())}"
    h = subprocess.run(["curl", "-s", "-L", "--max-time", "40", url], capture_output=True).stdout.decode("utf-8", "replace")
    return path, h


def main():
    olds = {}
    for r in before:
        olds[r["url"].rstrip("/") or "/"] = r
    news = sorted({redirects.get(u, u) for u in olds})
    with cf.ThreadPoolExecutor(8) as ex: pages = dict(ex.map(fetch, news))
    after = {}
    for p, h in pages.items():
        if not h or "Error 404" in h[:3000] or "<title" not in h.lower(): continue
        after[p] = SA.parse(h, BASE + p, p)
    pairs = []
    for u, o in olds.items():
        n = after.get(redirects.get(u, u))
        pairs.append(dict(old_url=u, new_url=redirects.get(u, u), before=o["score"], after=(n or {}).get("score"), old=o, new=n))
    live = [p for p in pairs if p["new"]]
    uniq = {}
    for p in live: uniq[p["new_url"]] = p["new"]
    rows = list(uniq.values())
    out = dict(base=BASE, old_summary=SA.summarise(before), new_summary=SA.summarise(rows), pairs=pairs, missing=[p["new_url"] for p in pairs if not p["new"]])
    json.dump(out, open(os.path.join(ROOT, "brands/vanausdall.seo-compare.json"), "w"), indent=1)

    o, n = out["old_summary"], out["new_summary"]
    L = [f"# Van Ausdall & Farrar: SEO and AEO before and after", "",
         f"Before: the old site crawled 8 September 2026 ({o['pages']} pages). After: the rebuild at {BASE} ({n['pages']} pages). Same seventeen checks and weights for both.", "",
         "| Measure | Before | After |", "|---|---|---|",
         f"| Average page score | {o['avg_score']} | {n['avg_score']} |"]
    for k, lab in (("faq", "Pages with FAQPage schema"), ("service", "Pages with Service schema"), ("local", "Pages with LocalBusiness schema"), ("review", "Pages with Review or AggregateRating schema"),
                   ("article", "Pages with Article or BlogPosting schema"), ("breadcrumb", "Pages with BreadcrumbList"), ("city_in_title", "Titles naming the city"), ("thin", "Pages under 300 words"),
                   ("question_headings", "Pages with a question heading"), ("images_no_alt", "Images missing alt text"), ("stock_og", "Pages with a stock or missing share image")):
        L.append(f"| {lab} | {o[k]} | {n[k]} |")
    L.append(f"| Grades A / B / C / D / F | {' / '.join(str(o['grades'][g]) for g in 'ABCDF')} | {' / '.join(str(n['grades'][g]) for g in 'ABCDF')} |")
    L += ["", "## By page type", "", "| Type | Before (pages, avg) | After (pages, avg) |", "|---|---|---|"]
    for t in sorted(set(o["by_type"]) | set(n["by_type"])):
        a, b = o["by_type"].get(t), n["by_type"].get(t)
        L.append(f"| {t} | {a['pages'] if a else 0}, {a['avg'] if a else '-'} | {b['pages'] if b else 0}, {b['avg'] if b else '-'} |")
    from collections import Counter
    fails = Counter(f for r in rows for f in r["recommendations"])
    L += ["", "## What still costs points on the rebuild", "", "| Pages | Fix |", "|---|---|"] + [f"| {c} | {f} |" for f, c in fails.most_common(12)]
    L += ["", "## Lowest scoring pages after", "", "| Score | Page | Fixes |", "|---|---|---|"]
    for r in sorted(rows, key=lambda r: r["score"])[:25]: L.append(f"| {r['score']} | {r['url']} | {'; '.join(r['recommendations'][:3])} |")
    if out["missing"]: L += ["", "## Not found on the rebuild", ""] + [f"- {m}" for m in out["missing"]]
    L += ["", "## Every page", "", "| Old URL | New URL | Before | After |", "|---|---|---|---|"]
    for p in sorted(pairs, key=lambda p: p["old_url"]): L.append(f"| {p['old_url']} | {p['new_url']} | {p['before']} | {p['after'] if p['after'] is not None else 'missing'} |")
    open(os.path.join(ROOT, "brands/vanausdall.seo-compare.md"), "w").write("\n".join(L) + "\n")
    print(f"before avg {o['avg_score']} ({o['pages']} pages) -> after avg {n['avg_score']} ({n['pages']} pages); missing {len(out['missing'])}")
    print("grades", o["grades"], "->", n["grades"])
    print("most common remaining fixes:"); [print(f"  {c:3}  {f}") for f, c in fails.most_common(10)]


if __name__ == "__main__":
    main()
