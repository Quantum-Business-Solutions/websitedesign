#!/usr/bin/env python3
"""Generate the launch-time SEO/AEO artefacts from the content file (nothing is published here):
   brands/vanausdall.llms.txt        what an AI crawler should know about VAF and where the key pages are
   brands/vanausdall.redirects.json  old vanausdall.com path -> new path (the 301 map), ready for scripts/vaf_redirects.py at go-live
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from vaf_common import ROOT, slug_of
C = json.load(open(os.path.join(ROOT, "brands/vanausdall.content.json"), encoding="utf-8"))
extra = os.path.join(ROOT, "brands/vanausdall.extra-pages.json")
pages = C["pages"] + (json.load(open(extra, encoding="utf-8")) if os.path.exists(extra) else [])
S = "https://www.vanausdall.com"
by = {p["file"]: p for p in pages}


def line(f):
    p = by.get(f)
    return f"- [{p['title'].split('|')[0].strip()}]({S}/{slug_of(f)}): {p.get('description', '')}" if p else ""


groups = [("Start here", ["index.html", "company-facts.html", "technology-strength-assessment.html", "contact.html"]),
          ("Solutions", [f for f in by if f.startswith("solutions")] + [f"services/{x}.html" for x in ("managed-it", "cybersecurity", "cloud", "business-phone-systems", "copiers", "managed-print", "copier-service", "production-print", "document-management", "document-conversion", "ai-consulting", "business-continuity", "it-support")]),
          ("Industries", sorted(f for f in by if f.startswith("industries"))),
          ("Proof", ["case-studies.html"] + sorted(f for f in by if f.startswith("case-studies/"))),
          ("Locations", ["locations.html", "locations/indianapolis.html", "locations/fort-wayne.html", "locations/evansville.html"])]
txt = ["# Van Ausdall & Farrar, Inc.", "",
       "> " + C["schema"]["org_description"], "",
       "Facts: founded 1914 (Thomas Edison Company distributor); privately owned and operated in Indianapolis; headquarters 6430 E 75th Street, Indianapolis, IN 46250; offices in Fort Wayne and Evansville; SOC 2 certified; Net Promoter Score 92.8 audited by CEO Juice; Mitel Gold partner; Customer Care Center Monday to Friday 7:00am to 5:00pm, (317) 634-2913.", ""]
for h, fs in groups:
    ls = [line(f) for f in fs if line(f)]
    if ls:
        txt += [f"## {h}", *ls, ""]
open(os.path.join(ROOT, "brands/vanausdall.llms.txt"), "w", encoding="utf-8").write("\n".join(txt))
m = (C.get("pitch", {}).get("migration", {}) or {}).get("map") or {}
red = [{"from": k if k.startswith("/") else "/" + k, "to": "/" + slug_of(v) if v else "/"} for k, v in m.items()]
json.dump(red, open(os.path.join(ROOT, "brands/vanausdall.redirects.json"), "w"), indent=1)
print(len(txt), "llms.txt lines;", len(red), "redirects")
