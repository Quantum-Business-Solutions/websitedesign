#!/usr/bin/env python3
"""Sign-off sheet rows from a before/after SEO comparison: one row per page, with where it stood, where it stands now, and what is left.

    python3 scripts/signoff_rows.py brands/vanausdall.seo-compare.json <page-id-log> <hubspot-portal-id> <out.json>
The page-id log is the output of `vaf_build.py pages all` (lines "  page <id> <path>"). Output is the `rows` array for update_signoff_sheet.
Reusable for any client whose rebuild was scored with scripts/site_audit.py: only the file names and BASE change.
"""
import json, re, sys
cmp_path, idlog, portal, out = sys.argv[1:5]
D = json.load(open(cmp_path))
BASE = D["base"]
ids = {}
for line in open(idlog):
    m = re.match(r"\s+page (\d+) (\S+)", line)
    if m: ids[m.group(2).rstrip("/") or "/"] = m.group(1)
TYPE = {"service": "Service page", "city": "Location page", "company": "Company page", "case study": "Case study", "policy": "Policy", "post": "Blog"}
GRADE = lambda s: "A" if s >= 85 else "B" if s >= 70 else "C" if s >= 55 else "D" if s >= 40 else "F"
by_new = {}
for p in D["pairs"]:
    if p["new"]: by_new.setdefault(p["new_url"], []).append(p)
rows = []
for new_url, ps in sorted(by_new.items()):
    n = ps[0]["new"]; best_old = max(ps, key=lambda p: p["before"]); o = best_old["old"]; b = best_old["before"]
    slug = new_url.strip("/") or "home"
    dropped = [p["old_url"] for p in ps if p is not best_old]
    gain = []
    if n["images_no_alt"] < o["images_no_alt"]: gain.append(f"alt text on every image (was {o['images_no_alt']} missing)")
    if n["faq"] and not o["faq"]: gain.append("FAQ added with FAQPage markup")
    if n["service"] and not o["service"]: gain.append("Service markup")
    if n["breadcrumb"] and not o["breadcrumb"]: gain.append("breadcrumbs with markup")
    if n["review"] and not o["review"]: gain.append("customer comments with Review markup")
    if n["question_headings"] > o["question_headings"]: gain.append("question headings for answer engines")
    if n["words"] > o["words"] + 100: gain.append(f"{o['words']} to {n['words']} words")
    if n["internal_links"] > o["internal_links"] + 5: gain.append(f"{o['internal_links']} to {n['internal_links']} internal links")
    left = [r for r in n["recommendations"]]
    detail = (f"Before: score {b} ({GRADE(b)}), title \"{o['title']}\". Now: score {n['score']} ({n['grade']}), title \"{n['title']}\". "
              + ("Changed: " + "; ".join(gain) + ". " if gain else "")
              + ("Still open: " + "; ".join(left) + "." if left else "Nothing open on the SEO and AEO checks.")
              + (f" Also replaces: {', '.join(dropped)}." if dropped else ""))
    row = {"id": slug, "name": re.sub(r"\s*\|.*$", "", n["title"]) or slug, "group": "p", "type": TYPE.get(n["type"], "Page"), "detail": detail,
           "live_url": BASE + new_url, "old_url": "https://www.vanausdall.com" + best_old["old_url"],
           "labels": [{"severity": "ok" if n["score"] >= 85 else "warn", "short": f"{b} to {n['score']}", "detail": f"SEO and AEO score before and now"}]}
    if left: row["labels"].append({"severity": "mute", "short": f"{len(left)} open"})
    if new_url in ids: row["hubspot_url"] = f"https://app.hubspot.com/pages/{portal}/editor/{ids[new_url]}/content"
    rows.append(row)
json.dump(rows, open(out, "w"), indent=1, ensure_ascii=False)
print(len(rows), "rows,", len(json.dumps(rows)), "bytes")
