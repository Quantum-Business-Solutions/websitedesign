#!/usr/bin/env python3
"""Keep VAF's Net Promoter Score in step with CEO Juice's live widget (the "Last Complete 12 Months" figure).

    python3 scripts/vaf_nps_refresh.py            # show the live score and where the site's copy stands (changes nothing)
    python3 scripts/vaf_nps_refresh.py --apply    # rewrite the figure in the content, overrides and module defaults, then record it

The figure is typed into about 220 places (hero stats, proof strips, schema text). After --apply, rebuild and publish:
    python3 scripts/vaf_upload.py && python3 scripts/vaf_build.py templates all
Source: https://api.ceojuice.com/widgets2/nps?customernumber=215 (public, read-only).
"""
import glob, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "brands/vanausdall.nps.json")
WIDGET = "https://api.ceojuice.com/widgets2/nps?customernumber=215"
FILES = (["brands/vanausdall.content.json"] + sorted(glob.glob(os.path.join(ROOT, "brands/vanausdall.overrides.*.json")))
         + sorted(glob.glob(os.path.join(ROOT, "themes/vaf/modules/*/fields.json"))))


def live():
    html = urllib.request.urlopen(urllib.request.Request(WIDGET, headers={"User-Agent": "qbs-nps-refresh"}), timeout=30).read().decode("utf-8", "ignore")
    m = re.search(r"label:\s*'NPS',\s*formatter:\s*function\s*\(w\)\s*\{\s*return\s*'([-0-9.]+)'", html)
    if not m:
        raise SystemExit("Could not read the score from the widget; its markup may have changed.")
    series = re.search(r"series:\s*\[([-0-9.\s,]+)\]", html)
    return m.group(1), (series.group(1) if series else "")


def main():
    value, series = live()
    cur = json.load(open(STATE))["value"] if os.path.exists(STATE) else None
    print(f"CEO Juice live score (last complete 12 months): {value}   [12 months, this month, last month, total: {series.strip()}]")
    print(f"Site currently uses: {cur}")
    if "--apply" not in sys.argv:
        return
    if cur is None or cur == value:
        print("Nothing to change." if cur == value else "No recorded figure; set brands/vanausdall.nps.json first.")
        return
    n = 0
    for f in FILES:
        p = f if os.path.isabs(f) else os.path.join(ROOT, f)
        s = open(p, encoding="utf-8").read()
        c = s.count(cur)
        if c:
            open(p, "w", encoding="utf-8").write(s.replace(cur, value)); n += c
    json.dump({"value": value, "as_of": __import__("datetime").date.today().isoformat(), "source": WIDGET, "measure": "Last complete 12 months"},
              open(STATE, "w"), indent=1)
    print(f"Replaced {cur} with {value} in {n} places. Now upload the theme and rebuild the templates.")


main()
