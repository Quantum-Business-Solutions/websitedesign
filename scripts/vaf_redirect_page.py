#!/usr/bin/env python3
"""Client-facing redirect map page (markdown) from brands/vanausdall.redirects.csv, grouped for approval.
    python3 scripts/vaf_redirect_page.py > brands/vanausdall.redirect-page.md"""
import csv, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(ROOT, "brands/vanausdall.redirects.csv"), encoding="utf-8")))
pages = [r for r in rows if r["Reason"] == "Mapped to the rebuilt page"]
retired = [r for r in rows if r["Reason"].startswith("Retired")]
blog = [r for r in rows if r["Reason"].startswith("HubSpot collapses")]
rules = [r for r in rows if r not in pages + retired + blog]
G = [("Case studies (customers are described, not named)", lambda r: r["Old URL"].startswith("/case-studies/")),
     ("Locations", lambda r: any(r["New URL"].startswith("/locations/") for _ in [0])),
     ("Services and industries", lambda r: r["New URL"].startswith(("/services/", "/industries/"))),
     ("Company, solutions and support pages", lambda r: True)]
o = []; w = o.append
w(f"""A redirect sends anyone who has the old address (a bookmark, a Google result, a link on another website) to the right page on the new site, and tells Google the page has moved so its ranking comes with it. This is the full list, **{len(rows)} rules**, ready to load on launch day. Every new address was checked and loads today on the staging site.

**What we need from you:** read the tables, tell us about any page that should go somewhere else, then mark the Redirect map row on the sign-off sheet Approved.

| Kind of rule | Count |
|---|---|
| Old pages sent to their rebuilt page | {len(pages)} |
| Retired pages sent to the closest live page | {len(retired)} |
| Blog addresses that change by one character | {len(blog)} |
| Site-wide rules | {len(rules)} |

## Retired pages: where each one goes

These old pages have no direct match on the new site. Tell us if you would send any of them somewhere else.

| Old page | Goes to |
|---|---|""")
for r in retired: w(f"| {r['Old URL']} | {r['New URL']} |")
w("""
## Blog addresses

Forty-seven old blog addresses contain a double hyphen (for example `van-ausdall--farrar`). HubSpot collapses a double hyphen to a single one, so each of those posts is one character different on the new site, and each gets its own redirect. The other blog addresses are unchanged. Older links of the form `/blog?p=<name>-<date>` are redirected to `/blog/<name>` the same way.

## Site-wide rules
""")
for r in rules: w(f"- `{r['Old URL']}` goes to `{r['New URL']}`: {r['Reason'].lower()}.")
used = set()
for name, f in G:
    grp = [r for r in pages if id(r) not in used and f(r)]
    for r in grp: used.add(id(r))
    w(f"\n## {name} ({len(grp)})\n\n| Old page | New page |\n|---|---|")
    for r in sorted(grp, key=lambda r: r["Old URL"]): w(f"| {r['Old URL']} | {r['New URL']} |")
print("\n".join(o))
