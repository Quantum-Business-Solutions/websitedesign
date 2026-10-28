#!/usr/bin/env python3
"""Compare an old vanausdall.com page with its rebuilt page: which headings, list items and paragraphs of the old page
are missing from the new one. Containment test on content words (a unit counts as present if 70% of its words appear on the new page).

    python3 scripts/vaf_coverage.py <old-path> <new-slug>      e.g.  /information  solutions-information
"""
import re, subprocess, sys
from html.parser import HTMLParser

STOP = set("the and for with that this from your you our are have has will can all any not but its their they them been more most into out about over than when what which who how also each other such only one two per via".split())


def fetch(url):
    return subprocess.run(["curl", "-s", "-L", "--max-time", "40", url], capture_output=True).stdout.decode("utf-8", "replace")


class Units(HTMLParser):
    """Visible text units from <main> (old site) or the whole body (new site), skipping nav/header/footer/script/style."""
    def __init__(self, main_only):
        super().__init__(); self.u = []; self.buf = ""; self.skip = 0; self.tag = None; self.main_only = main_only; self.in_main = not main_only; self.depth_main = 0
    def handle_starttag(self, t, a):
        if t in ("script", "style", "noscript", "nav", "footer", "header", "svg", "form"): self.skip += 1
        if t == "main" and self.main_only: self.in_main = True
        if t in ("h1", "h2", "h3", "h4", "p", "li", "td", "summary", "blockquote"): self.flush(); self.tag = t
    def handle_endtag(self, t):
        if t in ("script", "style", "noscript", "nav", "footer", "header", "svg", "form") and self.skip: self.skip -= 1
        if t in ("h1", "h2", "h3", "h4", "p", "li", "td", "summary", "blockquote"): self.flush()
    def handle_data(self, d):
        if self.in_main and not self.skip: self.buf += d
    def flush(self):
        s = re.sub(r"\s+", " ", self.buf).strip()
        if s and self.tag: self.u.append((self.tag, s))
        self.buf = ""; self.tag = None


def words(s):
    return [w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 3 and w not in STOP]


def main(old, new):
    ho = fetch("https://www.vanausdall.com" + old); hn = fetch(f"https://50498425.hs-sites.com/{new}?c={abs(hash(new))%10**6}")
    o = Units(True); o.feed(ho); n = Units(False); n.feed(hn)
    new_words = set(words(" ".join(s for _, s in n.u)))
    units = [(t, s) for t, s in o.u if len(words(s)) >= 3 and not re.search(r"cookie|privacy|©|copyright|skip to", s, re.I)]
    miss = []
    for t, s in units:
        w = set(words(s))
        if w and len(w & new_words) / len(w) < 0.7: miss.append((t, s))
    print(f"{old} -> /{new}: old units {len(units)}, new units {len(n.u)}, words old {sum(len(words(s)) for _, s in units)} new {len(new_words)}")
    print(f"  covered {len(units) - len(miss)} of {len(units)}; missing {len(miss)}")
    for t, s in miss[:25]: print(f"   [{t}] {s[:170]}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
