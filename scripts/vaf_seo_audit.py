#!/usr/bin/env python3
"""SEO and AEO audit of the built VAF staging pages: metadata, headings, schema, FAQs, alt text, links.

    python3 scripts/vaf_seo_audit.py <base-url> [slug ...]        # default: every page in brands/vanausdall.content.json
Writes brands/vanausdall.seo-audit-build.json and prints a summary. Compared against the September baseline:
FAQPage on 4 of 171 pages, 0 Review, 68 pages under 300 words, titles without the city, stock og:image.
"""
import concurrent.futures as cf, json, os, re, subprocess, sys
from html.parser import HTMLParser
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "https://50498425.hs-sites.com"
C = json.load(open(os.path.join(ROOT, "brands/vanausdall.content.json"), encoding="utf-8"))


def slug(file):
    s = re.sub(r"\.html$", "", file)
    return "" if s == "index" else s


class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.d = dict(title="", desc="", canon="", robots="", og={}, h1=0, h2=0, imgs=0, noalt=0, links=0, ld=[], text=[]); self._t = None; self._ld = False; self._skip = 0
    def handle_starttag(self, t, a):
        a = dict(a)
        if t == "title": self._t = ""
        if t == "meta":
            n, p, c = (a.get("name") or "").lower(), (a.get("property") or "").lower(), a.get("content") or ""
            if n == "description": self.d["desc"] = c
            if n == "robots": self.d["robots"] = c
            if p.startswith("og:") or n.startswith("twitter:"): self.d["og"][p or n] = c
        if t == "link" and a.get("rel") == "canonical": self.d["canon"] = a.get("href", "")
        if t == "h1": self.d["h1"] += 1
        if t == "h2": self.d["h2"] += 1
        if t == "img":
            self.d["imgs"] += 1
            if not (a.get("alt") or "").strip() and a.get("role") != "presentation" and a.get("aria-hidden") != "true": self.d["noalt"] += 1
        if t == "a" and (a.get("href") or "").startswith("/"): self.d["links"] += 1
        if t == "script" and a.get("type") == "application/ld+json": self._ld = True; self._buf = ""
        elif t in ("script", "style", "noscript"): self._skip += 1
    def handle_endtag(self, t):
        if t == "title": self.d["title"] = (self._t or "").strip(); self._t = None
        if t == "script" and self._ld:
            self._ld = False
            try: self.d["ld"].append(json.loads(self._buf))
            except Exception: self.d["ld"].append({"@type": "INVALID_JSON"})
        elif t in ("script", "style", "noscript") and self._skip: self._skip -= 1
    def handle_data(self, x):
        if self._t is not None: self._t += x
        if self._ld: self._buf += x
        elif not self._skip: self.d["text"].append(x)


def types(ld):
    out = []
    def walk(x):
        if isinstance(x, list): [walk(i) for i in x]
        elif isinstance(x, dict):
            t = x.get("@type")
            if t: out.extend(t if isinstance(t, list) else [t])
            [walk(v) for v in x.values() if isinstance(v, (dict, list))]
    walk(ld); return out


def audit(sl):
    html = subprocess.run(["curl", "-s", "-L", "--max-time", "40", f"{BASE}/{sl}"], capture_output=True).stdout.decode("utf-8", "replace")
    p = P(); p.feed(html); d = p.d
    t = types(d["ld"]); words = len(re.findall(r"\w+", " ".join(d["text"])))
    faq_q = sum(1 for b in d["ld"] for x in (b.get("@graph", [b]) if isinstance(b, dict) else []) if isinstance(x, dict) and x.get("@type") == "FAQPage" for _ in x.get("mainEntity", []))
    return {"slug": sl, "ok": bool(html) and "Error 404" not in html[:2000], "title": d["title"], "title_len": len(d["title"]), "desc_len": len(d["desc"]),
            "h1": d["h1"], "h2": d["h2"], "canonical": bool(d["canon"]), "og_image": bool(d["og"].get("og:image")), "og_title": bool(d["og"].get("og:title")),
            "twitter": bool(d["og"].get("twitter:card")), "robots": d["robots"], "schema": sorted(set(t)), "faq_questions": faq_q, "imgs": d["imgs"],
            "imgs_no_alt": d["noalt"], "words": words, "internal_links": d["links"], "has_city": "indianapolis" in d["title"].lower() or "indiana" in d["title"].lower()}


if __name__ == "__main__":
    sl = [a for a in sys.argv[2:]] or [slug(p["file"]) for p in C["pages"] if not slug(p["file"]).startswith("blog")]
    with cf.ThreadPoolExecutor(8) as ex: rows = list(ex.map(audit, sl))
    json.dump(rows, open(os.path.join(ROOT, "brands/vanausdall.seo-audit-build.json"), "w"), indent=1)
    ok = [r for r in rows if r["ok"]]; n = len(ok)
    def c(f): return sum(1 for r in ok if f(r))
    print(f"{n} of {len(rows)} pages live")
    for lab, f in (("title 30-60 chars", lambda r: 30 <= r["title_len"] <= 60), ("meta description 110-160", lambda r: 110 <= r["desc_len"] <= 160), ("exactly one H1", lambda r: r["h1"] == 1),
                   ("canonical", lambda r: r["canonical"]), ("og:image", lambda r: r["og_image"]), ("og:title", lambda r: r["og_title"]), ("twitter card", lambda r: r["twitter"]),
                   ("Organization schema", lambda r: "Organization" in r["schema"]), ("LocalBusiness schema", lambda r: "LocalBusiness" in r["schema"]), ("BreadcrumbList", lambda r: "BreadcrumbList" in r["schema"]),
                   ("FAQPage", lambda r: "FAQPage" in r["schema"]), ("Service schema", lambda r: "Service" in r["schema"]), ("Article/BlogPosting", lambda r: bool({"Article", "BlogPosting"} & set(r["schema"]))),
                   ("all images have alt", lambda r: r["imgs_no_alt"] == 0), ("300+ words", lambda r: r["words"] >= 300), ("city/state in title", lambda r: r["has_city"])):
        print(f"  {lab:28s} {c(f):4d} / {n}")
