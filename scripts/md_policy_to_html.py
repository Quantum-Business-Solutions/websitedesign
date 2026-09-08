#!/usr/bin/env python3
"""Convert a policy scraped as markdown (Firecrawl) into simple HTML for extract_pages.py --policies.
Usage: python3 scripts/md_policy_to_html.py in.md out.html [--drop-before 'Heading text']"""
import html, re, sys

def main():
    src, dst = sys.argv[1], sys.argv[2]
    lines = open(src, encoding="utf-8").read().splitlines()
    out, in_list = [], False
    started = False
    for ln in lines:
        t = ln.rstrip()
        if not started:
            if t.startswith("# "):
                started = True
            else:
                continue  # skip the page chrome above the H1
        if t.startswith("AI Chat") or t.startswith("**Disclaimer:** AI responses"):
            break
        t = re.sub(r"^\d{1,2}\.\s+", "- ", t)  # numbered lists become bullets
        if t.startswith("- "):
            if not in_list: out.append("<ul>"); in_list = True
            li = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t[2:]).strip()
            out.append(f"<li>{html.escape(li)}</li>"); continue
        if in_list: out.append("</ul>"); in_list = False
        m = re.match(r"^(#{1,4})\s+(.*)", t)
        if m:
            lvl = min(len(m.group(1)) + 1, 3) if len(m.group(1)) > 1 else 2
            out.append(f"<h{lvl}>{html.escape(m.group(2).strip())}</h{lvl}>"); continue
        if t.strip():
            txt = re.sub(r"\*\*(.*?)\*\*", r"\1", t); txt = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", txt)
            out.append(f"<p>{html.escape(txt.strip())}</p>")
    if in_list: out.append("</ul>")
    open(dst, "w", encoding="utf-8").write("\n".join(out))
    print(dst, len(out), "elements")

if __name__ == "__main__":
    main()
