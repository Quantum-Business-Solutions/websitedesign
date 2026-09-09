#!/usr/bin/env python3
"""Analysis only: the search and AI-answer report for a prospect who has no build yet.

    python3 scripts/analyze.py <slug> [--fetch] [--audit]

Reads brands/<slug>.analysis.json:
    {"client": "GoodSuite", "domain": "goodsuite.com",
     "accent": "#97d700", "chrome": "#004b87",              # brand colours from the live site
     "cities": ["Chatsworth", "Los Angeles", "Fresno"],     # the places the site itself names, headquarters first
     "sitemaps": ["https://goodsuite.com/page-sitemap.xml", "https://goodsuite.com/post-sitemap.xml"],
     "skip": "feed|attachment|\\\\.(jpg|png|pdf)$",
     "out": "analyses/goodsuite"}                           # relative to websitedesign/; analyses/ is one Vercel project for every prospect

Needs brands/<slug>.seo.json (authored from the Semrush and Firecrawl pulls) and brands/<slug>.audit.json.
--fetch pulls every sitemap URL to disk; --audit runs seo_audit.py live over them into brands/<slug>.audit.json
(using brands/<slug>.types.json when present). Then the report, every-page cards, CSV and workbook are written to
<out>. The same renderer serves the full build, so the day a build exists the same seo.json carries over and the
report gains its build column.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
SCRATCH = os.environ.get("QBS_SCRATCH", os.path.join(ROOT, ".scratch"))


def sitemap_urls(url, seen=None):
    seen = seen if seen is not None else set()
    if url in seen:
        return []
    seen.add(url)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; QBS audit)"})
    try:
        body = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    except Exception as e:  # noqa: BLE001
        print("  sitemap failed", url, e)
        return []
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)
    if "<sitemapindex" in body:
        out = []
        for l in locs:
            out += sitemap_urls(l, seen)
        return out
    return locs


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("slug")
    p.add_argument("--fetch", action="store_true", help="download every sitemap URL to the scratch folder")
    p.add_argument("--audit", action="store_true", help="run the live audit into brands/<slug>.audit.json")
    p.add_argument("--date", default=None, help="measured date for the audit, e.g. '9 September 2026'")
    a = p.parse_args(argv)

    cfg_path = os.path.join(ROOT, "brands", f"{a.slug}.analysis.json")
    if not os.path.exists(cfg_path):
        sys.exit(f"no {cfg_path}. Copy brands/_starter.analysis.json and fill it.")
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    out = os.path.normpath(os.path.join(ROOT, cfg.get("out", f"../{a.slug}-analysis")))
    html_dir = os.path.join(SCRATCH, "seo", "html", a.slug)
    urls_file = os.path.join(SCRATCH, "seo", f"{a.slug}-urls.txt")
    audit_path = os.path.join(ROOT, "brands", f"{a.slug}.audit.json")
    types_path = os.path.join(ROOT, "brands", f"{a.slug}.types.json")

    if a.fetch:
        os.makedirs(os.path.dirname(urls_file), exist_ok=True)
        urls = []
        for sm in cfg.get("sitemaps") or [f"https://{cfg['domain']}/sitemap.xml"]:
            urls += sitemap_urls(sm)
        urls = sorted(set(urls))
        open(urls_file, "w", encoding="utf-8").write("\n".join(urls) + "\n")
        print(f"  {len(urls)} URLs from the sitemaps")
        subprocess.run([sys.executable, os.path.join(HERE, "seo_audit.py"), "fetch", "--urls", urls_file, "--html", html_dir], check=True)
    if a.audit:
        if not os.path.exists(urls_file):
            sys.exit("run with --fetch first")
        cmd = [sys.executable, os.path.join(HERE, "seo_audit.py"), "live", "--urls", urls_file, "--html", html_dir, "--domain", cfg["domain"],
               "--cities", ",".join(cfg.get("cities", [])), "--out", audit_path]
        if os.path.exists(types_path):
            cmd += ["--types", types_path]
        if cfg.get("skip"):
            cmd += ["--skip", cfg["skip"]]
        if a.date:
            cmd += ["--date", a.date]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        summ = json.load(open(audit_path, encoding="utf-8"))["summary"]
        print(f"  audit: {summ['count']} pages, average {summ['avg_score']}, {summ['grade_d_f']} D or F")

    import preview_seo
    preview_seo.write_analysis(a.slug, cfg, out)
    print(f"report: {os.path.join(out, 'seo-report.html')}")


if __name__ == "__main__":
    main()
