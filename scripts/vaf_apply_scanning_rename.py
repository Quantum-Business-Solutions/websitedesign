#!/usr/bin/env python3
"""Rename "Document conversion" to "Document scanning" in everything a visitor reads (Brian Courtney, HOME-09, confirmed by Shawn 25 Nov 2026).

    python3 scripts/vaf_apply_scanning_rename.py            # apply (idempotent)
    python3 scripts/vaf_apply_scanning_rename.py --check    # list what is still left

Kept on purpose: the facility name "Document Conversion Center" (and "conversion center / network"), web addresses (URL slugs, because the blog posts link to
/services/document-conversion and redirects load only at go-live), old-site paths in the redirect map, and blog post titles, slugs and tags
(blog posts are never edited here). Display text, page titles, descriptions, schema names and menu labels all change."""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = "--check" in sys.argv

FILES = (["brands/vanausdall.content.json", "brands/vanausdall.extra-pages.json", "brands/vanausdall.customers.json", "brands/vanausdall.llms.txt",
          "brands/vanausdall.content.py", "scripts/vaf_launch_files.py", "scripts/vaf_build.py", "scripts/vaf_links.py", "scripts/vaf_map_d.py"]
         + sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "brands/vanausdall.overrides.*.json")))
         + sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "themes/vaf/modules/*/fields.json")))
         + sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "themes/vaf/modules/*/module.html"))))

# Text that must not change. Swapped for a token first, put back last.
KEEP = [
    r"Document Conversion Center", r"document conversion center", r"[Cc]onversion [Cc]enter", r"[Cc]onversion network",
    # blog post titles and tags, which mirror posts we do not edit
    r"Document conversion services: what actually happens", r"Document conversion: what happens to your boxes",
    r"Document Conversion Services, Indiana", r"document conversion companies #2, digital document conversion #5",
    # anything address-shaped: slugs, file names, old-site paths, image names
    r"[\w/.#:-]*document-conversion[\w/.#?=-]*", r"gen-conversion[\w.-]*",
]

# (id, regex, replacement). Run in order on the text with the keep-list tokenised.
RULES = [
    ("dup-1", r"Document Conversion Document conversion and scanning serv", "Document Scanning Document scanning serv"),
    ("Title", r"Document Conversion", "Document Scanning"),
    ("Sent", r"Document conversion", "Document scanning"),
    ("lower", r"document conversion", "document scanning"),
    # services/document-scanning is a different page (scanning tools), so the renamed service page keeps "Services" in its title to stay distinct
    ("title-svc", r"Document Scanning, Indianapolis \|", "Document Scanning Services, Indianapolis |"),
    ("mgmt-and", r"(document management|management) (and|or) conversion", r"\1 \2 scanning"),
    ("mgmt-comma", r"(document management|management), conversion( and AI| and)", r"\1, scanning\2"),
]


def transform(s):
    tokens = []

    def hold(m):
        tokens.append(m.group(0))
        return "\x00%d\x00" % (len(tokens) - 1)

    for k in KEEP:
        s = re.sub(k, hold, s)
    for _id, pat, rep in RULES:
        s = re.sub(pat, rep, s)
    # VAF's own pairing "scanning and conversion" would now read "scanning and scanning" or keep the old word; keep the one word
    s = re.sub(r"([Ss]canning) (and|&) ([Ss]canning|[Cc]onversion)", r"\1", s)
    return re.sub(r"\x00(\d+)\x00", lambda m: tokens[int(m.group(1))], s)


def main():
    changed, left = 0, 0
    for f in FILES:
        p = os.path.join(ROOT, f)
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        t = transform(s)
        if f.endswith(".json"):
            json.loads(t)
        if t != s:
            if CHECK:
                left += 1
                print("still to change:", f)
            else:
                open(p, "w", encoding="utf-8").write(t)
                changed += 1
    print("files changed" if not CHECK else "files with work left", changed if not CHECK else left)
    if CHECK and not left:
        print("nothing left")


if __name__ == "__main__":
    main()
