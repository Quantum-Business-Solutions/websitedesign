"""Write launch-package/robots.txt, llms.txt and sitemap.xml from the built content, for the client's real domain.
usage: launch_package.py CONTENT_JSON OUT_DIR DOMAIN   (DOMAIN like https://www.example.com)"""
import json, os, re, sys, html

def main():
    content_json, out, domain = sys.argv[1], sys.argv[2], sys.argv[3].rstrip("/")
    c = json.load(open(content_json))
    pages = c["pages"]
    d = os.path.join(out, "launch-package"); os.makedirs(d, exist_ok=True)
    url = lambda f: domain + "/" + ("" if f == "index.html" else f[:-5] if f.endswith(".html") else f)
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "PerplexityBot", "Google-Extended", "Applebot-Extended"]
    robots = "# Open to search and AI answer engines. Review the list with the client before launch.\nUser-agent: *\nAllow: /\n\n" + \
        "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {domain}/sitemap.xml\n"
    open(os.path.join(d, "robots.txt"), "w").write(robots)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sch = c.get("schema", {})
    skip = set(sch.get("sitemap_exclude", []))                      # pages that stay live but are not for search (a dealer login, for example)
    lastmod = sch.get("updated") or __import__("datetime").date.today().isoformat()
    pages_idx = [p for p in pages if p["file"] not in skip]
    sm += [f"  <url><loc>{html.escape(url(p['file']))}</loc><lastmod>{lastmod}</lastmod></url>" for p in pages_idx]
    sm.append("</urlset>")
    open(os.path.join(d, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    name = c.get("client", "")
    groups = {}
    for p in pages_idx:
        f = p["file"]; seg = f.split("/")[0] if "/" in f else ("home" if f == "index.html" else "main")
        groups.setdefault(seg, []).append(p)
    lines = [f"# {name}", "", f"> {(c.get('schema', {}).get('org_description') or '').strip()}", ""]
    order = ["home", "main", "services", "products", "industries", "support", "partners", "training", "about", "news"]
    for seg in sorted(groups, key=lambda s: order.index(s) if s in order else 99):
        if seg == "home": continue
        lines.append(f"## {seg.replace('-', ' ').title()}")
        for p in groups[seg]:
            lines.append(re.sub(r"\.{2,}$", ".", f"- [{(p.get('title') or p['file']).split(' | ')[0]}]({url(p['file'])}): {(p.get('description') or '').strip()}"))
        lines.append("")
    open(os.path.join(d, "llms.txt"), "w").write("\n".join(lines))
    readme = f"""LAUNCH PACKAGE: what to do at launch
=====================================

These files are for the live domain ({domain}). The preview build under /clean, /showcase and /press is a staging copy and is
deliberately not ready to be indexed:

  1. Every page carries <meta name="robots" content="noindex, nofollow">. Remove it on launch.
  2. <link rel="canonical">, og:url and og:image point at the staging host. At launch they must be rewritten to {domain}.
  3. The preview direction switcher (the "Direction" bar) must be removed.

scripts/launch_rewrite.py does all three for one direction folder:

  python3 scripts/launch_rewrite.py <built-direction-folder> {domain} <output-folder>

It writes a launch-ready copy and leaves the preview untouched. Then:

  - robots.txt, sitemap.xml ({len(pages_idx)} URLs, lastmod {lastmod}) and llms.txt in this folder go in the site root.
  - Apply the 301 map in redirects.csv (old URL to new path; rows marked 410 return Gone).
  - Submit sitemap.xml in Google Search Console and Bing Webmaster Tools.
  - Article markup carries no datePublished, dateModified or author until DMP supplies them (see the TO_CONFIRM list).
"""
    open(os.path.join(d, "README.txt"), "w").write(readme)
    print(f"launch package: {len(pages_idx)} pages -> {d}")

main()
