#!/usr/bin/env python3
"""Scaffold a new client in one go.

    python3 scripts/newclient.py --slug acme-office --client "Acme Office Solutions" --short Acme \
        --domain acmeoffice.com --repo ../acme-office [--city-tag NC --cities "Raleigh,Durham,NC"] [--no-fetch]

Creates
  brands/<slug>.content.py    from brands/_starter.content.py with the constants filled
  brands/<slug>.seo.json      from brands/_starter.seo.json with the domain and client filled
  brands/<slug>.build.json    themes, roles placeholders, base_url https://<repo-name>.vercel.app, out
  brands/<slug>.types.json    URL-type rules to edit after the first audit
  <repo>/                     git init, vercel.json (noindex on every path), README with the build command
and, unless --no-fetch, pulls the sitemap index, fetches every URL to /tmp/<slug>-html and writes
brands/<slug>.audit.json with seo_audit.py, so the every-page audit is ready before a word is written.

What still needs a person: the facts in the content file, the Semrush and live-result pulls into seo.json,
the Vercel project (import the repo in the dashboard; the API cannot link a repository), and the confirm list.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
B = os.path.join(ROOT, "brands")


def fetch_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; QBS-audit)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")


def sitemap_urls(domain):
    urls = []
    for cand in (f"https://{domain}/sitemap_index.xml", f"https://www.{domain}/sitemap_index.xml", f"https://{domain}/sitemap.xml", f"https://www.{domain}/sitemap.xml"):
        try:
            x = fetch_text(cand)
        except Exception:  # noqa: BLE001
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)", x)
        if not locs:
            continue
        if "<sitemapindex" in x:
            for sm in locs:
                try:
                    urls += re.findall(r"<loc>\s*([^<\s]+)", fetch_text(sm))
                except Exception:  # noqa: BLE001
                    pass
        else:
            urls = locs
        if urls:
            break
    return sorted(set(u for u in urls if not re.search(r"\.(jpe?g|png|gif|webp|svg|pdf|mp4)$", u, re.I)))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--slug", required=True)
    p.add_argument("--client", required=True)
    p.add_argument("--short", help="one word, default first word of the client name")
    p.add_argument("--domain", required=True, help="bare domain, no scheme")
    p.add_argument("--repo", required=True, help="client repo folder, relative to websitedesign/")
    p.add_argument("--base-url", help="default https://<repo folder name>.vercel.app")
    p.add_argument("--city-tag", default="", help="what goes in titles, e.g. NC or Raleigh-Durham")
    p.add_argument("--cities", default="", help="comma list for the city-in-title check")
    p.add_argument("--no-fetch", action="store_true")
    a = p.parse_args(argv)
    short = a.short or a.client.split(" ")[0]
    repo = os.path.normpath(os.path.join(ROOT, a.repo))
    base = a.base_url or f"https://{os.path.basename(repo)}.vercel.app"

    # content.py from the starter
    dst = os.path.join(B, f"{a.slug}.content.py")
    if not os.path.exists(dst):
        s = open(os.path.join(B, "_starter.content.py"), encoding="utf-8").read()
        s = s.replace('"SLUG.content.json"', f'"{a.slug}.content.json"').replace('"CLIENT_REPO_FOLDER"', f'"{os.path.basename(repo)}"')
        s = s.replace('CLIENT = "CLIENT NAME"', f'CLIENT = "{a.client}"').replace('SHORT = "CLIENT"', f'SHORT = "{short}"')
        s = s.replace("<slug>", a.slug).replace("<client-repo>", os.path.basename(repo))
        open(dst, "w", encoding="utf-8").write(s)
        print("wrote", dst)
    # seo.json from the starter
    dst = os.path.join(B, f"{a.slug}.seo.json")
    if not os.path.exists(dst):
        s = open(os.path.join(B, "_starter.seo.json"), encoding="utf-8").read().replace("<domain>", a.domain).replace("<Client>", a.client)
        open(dst, "w", encoding="utf-8").write(s)
        print("wrote", dst)
    # build.json
    dst = os.path.join(B, f"{a.slug}.build.json")
    if not os.path.exists(dst):
        json.dump({"content": f"brands/{a.slug}.content.py", "themes": ["Quantum Showcase", "Quantum Clean", "Quantum Press"], "recommend": None,
                   "roles": {"Showcase": "the whole business made visible, image-led, layered, the most sales-forward of the three",
                             "Clean": "the disciplined, fast, easy-to-read site that lets the proof do the talking",
                             "Press": "editorial, serif, the one that reads like an established company"},
                   "base_url": base, "out": os.path.relpath(repo, ROOT)}, open(dst, "w", encoding="utf-8"), indent=1)
        print("wrote", dst)
    # types.json
    dst = os.path.join(B, f"{a.slug}.types.json")
    if not os.path.exists(dst):
        json.dump([["^/(tag|category|author)/", "archive"], ["^/(services?|solutions?|products?)/", "service"], ["^/(industries|markets|key-markets)/.", "industry"],
                   ["^/(locations?|contact-us)/.", "city"], ["^/(blog|news|resources)/.", "post"], ["-form/?$", "form"], ["^/(privacy|terms|thank-you)", "policy"]],
                  open(dst, "w", encoding="utf-8"), indent=1)
        print("wrote", dst)
    # client repo
    os.makedirs(repo, exist_ok=True)
    if not os.path.exists(os.path.join(repo, ".git")):
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo)
    vj = os.path.join(repo, "vercel.json")
    if not os.path.exists(vj):
        json.dump({"headers": [{"source": "/(.*)", "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}]}]}, open(vj, "w"), indent=2)
    rd = os.path.join(repo, "README.md")
    if not os.path.exists(rd):
        open(rd, "w", encoding="utf-8").write(f"""# {a.client}: website preview

Three complete, clickable website directions for {a.client}, prepared by Quantum Business Solutions. Served at {base} (noindex on every path).

Generated by `scripts/build.py {a.slug}` in `Quantum-Business-Solutions/websitedesign` from `brands/{a.slug}.content.py`,
with `brands/{a.slug}.seo.json` and `.audit.json` for the search and AI-answer package. Rebuild and deploy with:

```bash
cd websitedesign && python3 scripts/build.py {a.slug} --push
```

- `index.html`: the hub. The three directions, side by side, search and AI answers, every page of {a.domain} scored against its rebuilt page, what we heard, to confirm, every page, the plan.
- `showcase/`, `clean/`, `press/`: one folder per direction, every page, with a direction switcher on each.
- `seo-report.html`, `seo-audit-pages.csv`, `redirects.csv`: the search analysis, the audit sheet, the 301 map.
- `design-system.html`, `standard.html`: the design system and the Quantum Website Standard.

Nothing here is live or indexed. No form submits anywhere. No analytics.
""")
    os.makedirs(os.path.join(repo, "assets"), exist_ok=True)
    print("repo ready", repo)

    if not a.no_fetch:
        urls = sitemap_urls(a.domain)
        print(f"sitemap: {len(urls)} URLs")
        if urls:
            uf = os.path.join(B, f"{a.slug}.urls.txt")
            open(uf, "w").write("\n".join(urls) + "\n")
            html_dir = f"/tmp/{a.slug}-html"
            subprocess.run([sys.executable, os.path.join(HERE, "seo_audit.py"), "fetch", "--urls", uf, "--html", html_dir], cwd=ROOT)
            subprocess.run([sys.executable, os.path.join(HERE, "seo_audit.py"), "live", "--urls", uf, "--html", html_dir, "--domain", a.domain,
                            "--cities", a.cities or a.city_tag, "--types", os.path.join(B, f"{a.slug}.types.json"),
                            "--out", os.path.join(B, f"{a.slug}.audit.json")], cwd=ROOT)
    print(f"""
next
  1 fill brands/{a.slug}.content.py (the facts) and set schema short_name/title_city/cities/local
  2 Semrush and live-result pulls into brands/{a.slug}.seo.json (INTAKE.md, the search baseline)
  3 python3 scripts/build.py {a.slug} --shots            # look at it
  4 create the GitHub repo, add it as origin, then: python3 scripts/build.py {a.slug} --push
  5 import the repo as a Vercel project named {os.path.basename(repo)}; the hub is live at {base}
""")


if __name__ == "__main__":
    main()
