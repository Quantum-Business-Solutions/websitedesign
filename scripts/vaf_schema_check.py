#!/usr/bin/env python3
"""Structured-data check on the live rebuild: every JSON-LD block parses, required properties are present, @id references resolve,
and nothing is declared twice. Usage: python3 scripts/vaf_schema_check.py [base-url] [extra-path ...]"""
import concurrent.futures as cf, json, os, re, subprocess, sys, time
from collections import Counter, defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://50498425.hs-sites.com").rstrip("/")
red = json.load(open(os.path.join(ROOT, "brands/vanausdall.redirects.json")))
paths = sorted({r["to"].rstrip("/") or "/" for r in red}) + sys.argv[2:]
REQ = {"LocalBusiness": ["name", "address", "telephone"], "Organization": ["name", "url", "logo"], "WebSite": ["name", "url"], "FAQPage": ["mainEntity"], "Question": ["name", "acceptedAnswer"],
       "Answer": ["text"], "Service": ["name", "provider"], "BlogPosting": ["headline", "datePublished", "author", "image", "publisher"], "Blog": ["name"], "BreadcrumbList": ["itemListElement"],
       "ListItem": ["position", "name"], "Review": ["reviewBody", "author", "itemReviewed"], "Article": ["headline", "datePublished", "author"], "PostalAddress": ["streetAddress", "addressLocality"],
       "OpeningHoursSpecification": ["dayOfWeek", "opens", "closes"]}


def fetch(p):
    return p, subprocess.run(["curl", "-s", "-L", "--max-time", "40", f"{BASE}{p}?cb={int(time.time())}"], capture_output=True).stdout.decode("utf-8", "replace")


def nodes(x, out):
    if isinstance(x, list): [nodes(i, out) for i in x]
    elif isinstance(x, dict):
        out.append(x); [nodes(v, out) for v in x.values() if isinstance(v, (dict, list))]
    return out


def main():
    with cf.ThreadPoolExecutor(8) as ex: pages = dict(ex.map(fetch, paths))
    problems = defaultdict(list); stats = Counter(); n = 0
    for p, h in pages.items():
        if "<title" not in h.lower(): problems["page did not load"].append(p); continue
        n += 1; blocks = re.findall(r'<script[^>]+ld\+json[^>]*>(.*?)</script>', h, re.S | re.I)
        allnodes = []; ids = {}; refs = []
        for b in blocks:
            try: d = json.loads(b)
            except Exception as e: problems["JSON-LD does not parse"].append(p); continue
            for nd in nodes(d, []):
                allnodes.append(nd)
                if "@id" in nd and len(nd) > 1: ids.setdefault(nd["@id"], []).append(nd.get("@type"))
                elif "@id" in nd and len(nd) == 1: refs.append(nd["@id"])
        types = Counter()
        for nd in allnodes:
            t = nd.get("@type"); ts = t if isinstance(t, list) else [t]
            for tt in ts:
                if not tt: continue
                types[tt] += 1
                if tt == "Organization" and "@id" not in nd: continue   # a nested publisher or customer stub, not the site's own organisation
                for need in REQ.get(tt, []):
                    if not nd.get(need): problems[f"{tt} missing {need}"].append(p)
        tops = Counter(nd.get("@type") for nd in allnodes if "@context" in nd)   # top-level blocks only
        for tt in ("Organization", "LocalBusiness", "WebSite", "FAQPage", "BreadcrumbList", "BlogPosting", "Article"):
            if tops[tt] > 1: problems[f"{tt} block repeated {tops[tt]} times"].append(p)
        for i, ts in ids.items():
            if len(ts) > 1: problems[f"@id declared twice: {i}"].append(p)
        for r in refs:
            if r not in ids: problems[f"@id referenced but never defined: {r}"].append(p)
        for tt in types: stats[tt] += 1
    print(f"{n} pages checked; pages carrying each type:", dict(stats.most_common()))
    if not problems: print("no problems")
    for k, v in sorted(problems.items(), key=lambda kv: -len(kv[1])): print(f"  {len(v):4}  {k}   e.g. {', '.join(v[:3])}")


if __name__ == "__main__":
    main()
