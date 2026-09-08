#!/usr/bin/env python3
"""Quality gate for a preview build: verify that what the hub and report claim is actually in the files.

Runs the on-page claims against every HTML page in each option folder, checks the redirect map
against the built files, and checks the hub's card count and links. Exit code 1 when any claim
fails, so it can sit in front of a push.

  python3 scripts/quality_check.py --out /path/to/client-repo --options clean,showcase,press \
      --domain www.vanausdall.com [--policy-prefix policies/]
"""
import argparse, csv, glob, html, json, os, re, sys

CITY_WORDS = ("indianapolis", "indiana", "fort wayne", "evansville", "bloomington", "carmel", "fishers", "noblesville", "greenwood", "muncie", "columbus", "south bend")


def types_in(h):
    types, bad = set(), 0
    for blk in re.findall(r'<script[^>]+ld\+json[^>]*>(.*?)</script>', h, re.S | re.I):
        try:
            d = json.loads(blk)
        except Exception:
            bad += 1; continue
        stack = [d]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                t = x.get("@type")
                if isinstance(t, str): types.add(t)
                elif isinstance(t, list): types.update(t)
                stack.extend(x.values())
            elif isinstance(x, list):
                stack.extend(x)
    return types, bad


def visible_text(h):
    b = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", h, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", b)


def check_page(path, rel, city_words, policy_prefix):
    h = open(path, encoding="utf-8", errors="ignore").read()
    fails = []
    title = html.unescape(re.sub(r"<[^>]+>", "", (re.search(r"<title[^>]*>(.*?)</title>", h, re.S | re.I) or [None, ""])[1]).strip()) if re.search(r"<title", h, re.I) else ""
    if not (30 <= len(title) <= 60): fails.append(f"title {len(title)} chars")
    if not any(c in title.lower() for c in city_words): fails.append("title has no city")
    meta = html.unescape((re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', h, re.I) or [None, ""])[1]) if re.search(r'name=["\']description', h, re.I) else ""
    if not (70 <= len(meta) <= 160): fails.append(f"meta {len(meta)} chars")
    h1n = len(re.findall(r"<h1\b", h, re.I))
    if h1n != 1: fails.append(f"h1 count {h1n}")
    if len(re.findall(r"<h2\b", h, re.I)) < 2: fails.append("fewer than two H2s")
    heads = [re.sub(r"<[^>]+>", "", x).strip() for x in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", h, re.S | re.I)]
    if not any(x.endswith("?") for x in heads): fails.append("no question heading")
    if not re.search(r'rel=["\']canonical["\']', h, re.I): fails.append("no canonical")
    if not re.search(r'property=["\']og:image["\']', h, re.I): fails.append("no og:image")
    types, bad = types_in(h)
    if bad: fails.append(f"{bad} JSON-LD block(s) do not parse")
    for need in ("Organization", "LocalBusiness"):
        if need not in types: fails.append(f"no {need} schema")
    is_policy = rel.startswith(policy_prefix)
    if not is_policy and "FAQPage" not in types: fails.append("no FAQPage schema")
    if rel.startswith(("services/", "industries/", "locations/")) and not ({"Service", "ITService", "ProfessionalService"} & types): fails.append("no Service schema")
    if rel.startswith(("case-studies/", "blog/")) and not ({"Article", "BlogPosting", "NewsArticle"} & types): fails.append("no Article schema")
    if not is_policy and not (re.search(r"<form\b", h, re.I) or re.search(r'href=["\']tel:', h, re.I)): fails.append("no form or tel link")
    links = re.findall(r'<a\b[^>]*href=["\']([^"\'#]+)', h, re.I)
    if sum(1 for l in links if not l.startswith(("http", "mailto:", "tel:"))) < 10: fails.append("fewer than 10 internal links")
    vt = visible_text(h)
    if "—" in vt or "–" in vt: fails.append("em or en dash in visible text")
    if "u2019" in vt: fails.append("literal u2019 escape")
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True); ap.add_argument("--options", default="clean,showcase,press")
    ap.add_argument("--domain", required=True); ap.add_argument("--policy-prefix", default="policies/")
    ap.add_argument("--redirects", default="redirects.csv"); ap.add_argument("--exclude", default="standard.html")
    a = ap.parse_args()
    opts = a.options.split(","); ex = a.exclude.split(",")
    total_fail = 0
    for o in opts:
        root = os.path.join(a.out, o); n = 0; bad = {}
        for fp in sorted(glob.glob(os.path.join(root, "**", "*.html"), recursive=True)):
            rel = os.path.relpath(fp, root).replace(os.sep, "/")
            if any(e in rel for e in ex): continue
            n += 1
            f = check_page(fp, rel, CITY_WORDS, a.policy_prefix)
            if f: bad[rel] = f
        print(f"{o}: {n} pages, {len(bad)} with failures")
        for rel, f in list(bad.items())[:20]:
            print(f"   {rel}: {'; '.join(f)}")
        total_fail += len(bad)
    # redirects
    rp = os.path.join(a.out, a.redirects)
    if os.path.exists(rp):
        missing = []
        for row in csv.DictReader(open(rp)):
            if row.get("status", "").startswith("301") and "retired" not in row.get("status", ""):
                new = row["new_path_in_build"].lstrip("/")
                for o in opts:
                    if not os.path.exists(os.path.join(a.out, o, new)): missing.append(f"{o}/{new}")
        print(f"redirects: {len(missing)} target(s) missing" + (": " + ", ".join(missing[:10]) if missing else ""))
        total_fail += len(missing)
    # hub
    hub = open(os.path.join(a.out, "index.html"), encoding="utf-8").read()
    cards = len(re.findall(r'<article class="pg ', hub))
    live = len(re.findall(rf'href="https://{re.escape(a.domain)}', hub))
    hrefs = set(re.findall(r'href="((?:clean|showcase|press)/[^"#]+)"', hub))
    missing_h = [h for h in hrefs if not os.path.exists(os.path.join(a.out, h))]
    print(f"hub: {cards} page cards, {live} live-page links, {len(hrefs)} distinct new-page links, {len(missing_h)} missing targets")
    total_fail += len(missing_h)
    print("RESULT:", "PASS" if total_fail == 0 else f"FAIL ({total_fail})")
    sys.exit(0 if total_fail == 0 else 1)


if __name__ == "__main__":
    main()
