"""Write launch-package/robots.txt, llms.txt and sitemap.xml from the built content, for the client's real domain.
usage: launch_package.py CONTENT_JSON OUT_DIR DOMAIN   (DOMAIN like https://www.example.com)"""
import json, os, sys, html

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
    sm += [f"  <url><loc>{html.escape(url(p['file']))}</loc></url>" for p in pages]
    sm.append("</urlset>")
    open(os.path.join(d, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    name = c.get("client", "")
    groups = {}
    for p in pages:
        f = p["file"]; seg = f.split("/")[0] if "/" in f else ("home" if f == "index.html" else "main")
        groups.setdefault(seg, []).append(p)
    lines = [f"# {name}", "", f"> {(c.get('schema', {}).get('org_description') or '').strip()}", ""]
    order = ["home", "main", "services", "products", "industries", "support", "partners", "training", "about", "news"]
    for seg in sorted(groups, key=lambda s: order.index(s) if s in order else 99):
        if seg == "home": continue
        lines.append(f"## {seg.replace('-', ' ').title()}")
        for p in groups[seg]:
            lines.append(f"- [{(p.get('title') or p['file']).split(' | ')[0]}]({url(p['file'])}): {(p.get('description') or '').strip()}")
        lines.append("")
    open(os.path.join(d, "llms.txt"), "w").write("\n".join(lines))
    print(f"launch package: {len(pages)} pages -> {d}")

main()
