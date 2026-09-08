"""The chooser page for scripts/preview.py, in the shape Revolution's preview proved:
the three directions with their real specs, our pick with reasons tied to what the client
said, the alternatives, a side-by-side compare, every page, the plan, and a way to answer.
Kept in its own module so the markup can be edited without touching the page renderer."""
from __future__ import annotations

import html
import re

import reskin


def _e(s) -> str:
    s = "" if s is None else str(s)
    s = re.sub(r"\s*[—–]\s*", ", ", s)
    return html.escape(s, quote=True)


def _pname(pg: dict) -> str:
    return "Home" if pg["file"] == "index.html" else pg["title"].split("|")[0].strip()


def _slug(theme: str) -> str:
    return theme.replace("Quantum ", "").lower()


def _ground(bg: str) -> str:
    lum = reskin.relative_luminance(bg)
    if lum < 0.18:
        return "Dark"
    if lum < 0.93:
        return "Warm paper"
    return "White"


def hub(content, themes, recommend, base, roles, standard, client_tokens, out_dir=None):
    import os
    b = content["brand"]
    pitch = content.get("pitch", {})
    ds_link = '<a href="design-system.html">Design system</a>' if out_dir and os.path.exists(os.path.join(out_dir, "design-system.html")) else ""
    ink = reskin.darken_until(b["accent"], "#f6f7f6")
    # The hub wears the client's scheme: their ground, their text colour, their accent. Neutrals lean toward the accent hue.
    acc = b["accent"].lstrip("#"); ar, ag, ab = int(acc[0:2], 16), int(acc[2:4], 16), int(acc[4:6], 16)
    def mix(hex_a, hex_b, k):
        a = hex_a.lstrip("#"); c = hex_b.lstrip("#")
        return "#" + "".join(f"{round(int(a[i:i+2], 16) * (1 - k) + int(c[i:i+2], 16) * k):02x}" for i in (0, 2, 4))
    fg = b.get("ink_secondary") or "#1e2124"
    if reskin.contrast_ratio(fg, "#ffffff") < 7:
        fg = "#1e2124"
    muted = mix(fg, "#ffffff", 0.42)
    border = mix(b["accent"], "#ffffff", 0.84)
    alt_bg = mix(b["accent"], "#ffffff", 0.91)
    navy = mix(b["accent"], "#0b1220", 0.72)
    dark_chrome = b.get("chrome") == "dark"
    chrome = b.get("chrome_bg", "#111") if dark_chrome else "#ffffff"
    chrome_fg = "#ffffff" if dark_chrome else fg
    chrome_muted = "rgba(255,255,255,.82)" if dark_chrome else muted
    chrome_hover = "rgba(255,255,255,.08)" if dark_chrome else alt_bg
    btn_fg = reskin.best_on(b["accent"])
    dark_css = ("@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]){--bg:#0e1412;--bg-alt:#141b18;--fg:#e6ebe7;--muted:#9cab9f;--border:#243328;--ink:" + b["accent"] + "}}\n"
                ":root[data-theme=\"dark\"]{--bg:#0e1412;--bg-alt:#141b18;--fg:#e6ebe7;--muted:#9cab9f;--border:#243328;--ink:" + b["accent"] + "}") if dark_chrome else ""
    n = len(themes)

    specs = []
    for i, t in enumerate(themes, 1):
        css, tok = client_tokens(t, b)
        nat = reskin.parse_native(css)
        short = t.replace("Quantum ", "")
        face = (nat.get("--q-serif") or "").split(",")[0].strip("'\"")
        rec = '<span class="rec">our recommendation</span>' if t == recommend else ""
        thumb = f"screenshots/{_slug(t)}-home-1440.jpg"
        has_thumb = bool(out_dir) and os.path.exists(os.path.join(out_dir, thumb))
        thumb_html = (f'<a class="thumb" href="{_slug(t)}/index.html" target="_blank" rel="noopener"><img src="{thumb}" alt="{_e(short)} home page at desktop width" width="720" height="450" loading="lazy"></a>'
                      if has_thumb else "")
        specs.append(
            '<article class="dir">' + thumb_html + '<div class="dir-h">'
            f'<span class="n">{i} / {n}</span><h2 class="h3">{_e(short)}</h2>{rec}<p>{_e(roles.get(t, ""))}</p></div>'
            '<details class="specd"><summary>Design specifics</summary><dl class="spec">'
            f'<div><dt>Headings</dt><dd>{_e(face)}</dd></div>'
            f'<div><dt>Ground</dt><dd>{_e(_ground(nat["--bg"]))}</dd></div>'
            f'<div><dt>Page width</dt><dd>{_e(nat.get("--maxw", "1240px"))}</dd></div>'
            f'<div><dt>Corners</dt><dd>{_e(nat.get("--radius", "8px"))}</dd></div></dl></details>'
            f'<a class="btn" href="{_slug(t)}/index.html" target="_blank" rel="noopener">Open {_e(short)}</a></article>')

    pick = recommend or themes[0]
    pick_short, pick_slug = pick.replace("Quantum ", ""), _slug(pick)
    reasons = "".join(f'<div class="why"><h3 class="h4">{_e(h)}</h3><p>{_e(t)}</p></div>' for h, t in pitch.get("pick_reasons" if recommend else "choose_reasons", pitch.get("pick_reasons", [])))
    alts = "".join(
        f'<a class="alt" href="{_slug(t)}/index.html" target="_blank" rel="noopener"><h3 class="h4">{_e(t.replace("Quantum ", ""))}</h3>'
        f'<p>{_e(why)}</p><span>Open {_e(t.replace("Quantum ", ""))}</span></a>'
        for t, why in pitch.get("alternatives", []))
    sr = pitch.get("search")
    search_html = ""
    if sr:
        tiles = "".join(f'<div class="stile"><b>{_e(v)}</b><span>{_e(l)}</span></div>' for v, l in sr.get("today_stats", []))
        sev_col = {"critical": "#b42318", "high": "#c4320a", "medium": "#b54708", "low": "#175cd3"}
        fcards = "".join(
            f'<article class="fnd"><div class="rk">{_e(f.get("rank", i + 1))}</div><div><span class="sevc" style="--sev:{sev_col.get(str(f.get("severity", "medium")).lower(), "#b54708")}">{_e(str(f.get("severity", "medium")).capitalize())}</span>'
            f'<h3 class="h4">{_e(f.get("title", ""))}</h3><p><b>Evidence:</b> {_e(f.get("evidence", ""))}</p><p><b>What it costs:</b> {_e(f.get("impact", ""))}</p><p><b>What we do:</b> {_e(f.get("action", ""))}</p></div></article>'
            for i, f in enumerate(sr.get("findings", [])[:5]))
        findings_html = (f'<h3 class="h3" style="margin-top:34px">{_e(sr.get("findings_heading", "Top findings, ranked by what they cost"))}</h3><div class="fnds">{fcards}</div>') if fcards else ""
        today = "".join(f"<li>{_e(x)}</li>" for x in sr.get("today", []))
        after = "".join(f"<li>{_e(x)}</li>" for x in sr.get("after", []))
        keep = "".join(f"<tr><td><code>{_e(o)}</code></td><td><code>{_e(n)}</code></td><td>{_e(w)}</td></tr>" for o, n, w in sr.get("keep", []))
        keep_tbl = (f'<div class="tblwrap" tabindex="0"><table class="seo"><thead><tr><th scope="col">Today</th><th scope="col">After launch (301)</th><th scope="col">What it ranks for now</th></tr></thead><tbody>{keep}</tbody></table></div>' if keep else "")
        search_html = f'''<section id="search"><div class="wrap"><p class="eyebrow">Search and AI answers</p><h2>{_e(sr.get("heading", "Where you stand today, and what changes"))}</h2><p class="lead">{_e(sr.get("intro", ""))}</p>
<div class="stiles">{tiles}</div>
{findings_html}
<div class="two" style="margin-top:34px"><div><h3 class="h3">Today <span class="asof">{_e(sr.get("as_of", ""))}</span></h3><ul>{today}</ul></div><div><h3 class="h3">After launch</h3><ul>{after}</ul></div></div>
{('<h3 class="h3" style="margin-top:34px">' + _e(sr.get("keep_heading", "Every page that earns a visitor today keeps earning it")) + '</h3>') if keep else ""}{keep_tbl}
{('<p style="margin-top:26px"><a class="btn" href="' + _e(sr["report_href"]) + '" target="_blank" rel="noopener">' + _e(sr.get("report_label", "Read the full SEO analysis")) + '</a></p>') if sr.get("report_href") else ""}
<div class="change" style="margin-top:22px"><strong>What we do not promise:</strong> {_e(sr.get("note", "Rankings or traffic. Those depend on the market and the content you publish after launch. We promise the inputs, and we measure the result against this baseline at 30, 60 and 90 days."))}</div></div></section>'''
    _n_saved = n
    # ---------------- whole-site audit: every page of the current site, every check, scored (vertical cards, no sideways scroll)
    audit_html = ""
    sa = (sr or {}).get("site_audit") if sr else None
    if sa and sa.get("rows"):
        sm = sa.get("summary", {}); rows = sa["rows"]; n = len(rows); site = sa.get("site", {})
        gcol = {"A": "#1b7f4b", "B": "#2e7d32", "C": "#b54708", "D": "#c4320a", "F": "#b42318"}
        def pill(label, val, ok):
            return f'<span class="pl {"ok" if ok else "bad"}"><i>{_e(label)}</i>{_e(str(val))}</span>'
        bmap = ((sa.get("migration") or {}).get("map")) or {}
        brows = {("/" + r["url"].lstrip("/")): r for r in ((sa.get("build") or {}).get("rows") or [])}
        slugs = [_slug(t) for t in themes]
        names = [t.replace("Quantum ", "") for t in themes]
        CHECKS = [("Title length", lambda r: 30 <= r["title_len"] <= 60, lambda r: f'{r["title_len"]} chars'), ("City in title", lambda r: r["city"], lambda r: "yes" if r["city"] else "no"),
                  ("Meta length", lambda r: 70 <= r["meta_len"] <= 160, lambda r: f'{r["meta_len"]} chars'), ("One H1", lambda r: r["h1_count"] == 1, lambda r: str(r["h1_count"])),
                  ("Two or more H2s", lambda r: r["h2_count"] >= 2, lambda r: str(r["h2_count"])), ("Question headings", lambda r: r["question_headings"] > 0, lambda r: str(r["question_headings"])),
                  ("300+ words", lambda r: r["words"] >= 300, lambda r: f'{r["words"]:,}'), ("Images with alt", lambda r: r["images_no_alt"] == 0, lambda r: f'{r["images_no_alt"]} missing'),
                  ("10+ internal links", lambda r: r["internal_links"] >= 10, lambda r: str(r["internal_links"])), ("FAQ schema", lambda r: r["faq"], lambda r: "yes" if r["faq"] else "no"),
                  ("Service or Article schema", lambda r: r["service"] or r.get("article"), lambda r: "yes" if (r["service"] or r.get("article")) else "no"), ("LocalBusiness schema", lambda r: r["local"], lambda r: "yes" if r["local"] else "no"),
                  ("Review schema", lambda r: r["review"], lambda r: "yes" if r["review"] else "no"), ("Canonical", lambda r: r["canonical"], lambda r: "yes" if r["canonical"] else "no"),
                  ("Branded share image", lambda r: not r["stock_og"], lambda r: "no" if r["stock_og"] else "yes"), ("Form or call", lambda r: r["has_form"] or r["tel_link"], lambda r: "yes" if (r["has_form"] or r["tel_link"]) else "no")]
        cards = []
        for r in rows:
            bf = bmap.get(r["url"]); bb = brows.get("/" + bf) if bf else None
            chips = "".join(f'<span class="sch">{_e(t.strip())}</span>' for t in (r.get("schema") or "").split(",") if t.strip() and t.strip() not in ("City", "GeoCoordinates", "PostalAddress", "Question", "Answer")) or '<span class="sch none">no schema beyond address</span>'
            pills = ""; fixed = 0
            grp_fixed, grp_open, grp_pass = [], [], []
            for label, ok, val in CHECKS:
                t_ok = bool(ok(r)); b_ok = bool(ok(bb)) if bb else None
                if bb is not None and not t_ok and b_ok:
                    fixed += 1
                    grp_fixed.append(f'<span class="pl3 ok"><i>{_e(label)}</i>{_e(val(r))} <em aria-hidden="true"></em> {_e(val(bb))}</span>')
                elif (bb is not None and not b_ok) or (bb is None and not t_ok):
                    grp_open.append(f'<span class="pl3 bad"><i>{_e(label)}</i>{_e(val(bb) if bb is not None else val(r))}</span>')
                else:
                    grp_pass.append(f'<span class="pl3 pass"><i>{_e(label)}</i>{_e(val(bb) if bb is not None else val(r))}</span>')
            pills = ""
            if grp_fixed:
                pills += f'<div class="grp"><h5>Fixed in the build <span>{len(grp_fixed)}</span></h5><div class="pills">{"".join(grp_fixed)}</div></div>'
            if grp_open:
                pills += f'<div class="grp"><h5>{"Still open" if bb is not None else "Failing today"} <span>{len(grp_open)}</span></h5><div class="pills">{"".join(grp_open)}</div>' + ('<p class="fine" style="margin:6px 0 0">Review schema waits for the Google review program; we do not mark up self-published testimonials.</p>' if bb is not None and any("Review" in x for x in grp_open) and len(grp_open) == 1 else "") + "</div>"
            if grp_pass:
                pills += f'<details class="grp pass"><summary>{len(grp_pass)} checks already passing</summary><div class="pills">{"".join(grp_pass)}</div></details>'
            DID = {"Title length": lambda r, bb: f"Retitled to {bb['title_len']} characters (was {r['title_len']})", "City in title": lambda r, bb: "City added to the title", "Meta length": lambda r, bb: f"Meta description rewritten to {bb['meta_len']} characters (was {r['meta_len']})",
                   "One H1": lambda r, bb: "Exactly one H1", "Two or more H2s": lambda r, bb: f"{bb['h2_count']} H2 section{'s' if bb['h2_count'] != 1 else ''} (was {r['h2_count']})", "Question headings": lambda r, bb: f"{bb['question_headings']} question-form heading{'s' if bb['question_headings'] != 1 else ''} an assistant can quote (was {r['question_headings']})",
                   "300+ words": lambda r, bb: f"Copy grew from {r['words']} to {bb['words']:,} words", "Images with alt": lambda r, bb: "Alt text on every image", "10+ internal links": lambda r, bb: f"{bb['internal_links']} internal links (was {r['internal_links']})",
                   "FAQ schema": lambda r, bb: "FAQ marked up as FAQPage, with question-form headings", "Service or Article schema": lambda r, bb: ("Article schema" if bb.get("article") else "Service schema declaring what the page offers"), "LocalBusiness schema": lambda r, bb: "LocalBusiness schema for the Indianapolis office",
                   "Review schema": lambda r, bb: "Review schema", "Canonical": lambda r, bb: "Self-referencing canonical", "Branded share image": lambda r, bb: "Branded share image", "Form or call": lambda r, bb: "Form and click-to-call on the page"}
            if bb is not None:
                did = [DID[label](r, bb) for label, ok, val in CHECKS if not bool(ok(r)) and bool(ok(bb))]
                if bb["words"] > r["words"] * 1.3 and "300+ words" not in [l for l, ok, v in CHECKS if not bool(ok(r)) and bool(ok(bb))]:
                    did.append(f"Copy grew from {r['words']} to {bb['words']:,} words")
                did.append("Organization schema with sameAs, logo and founding date on every page")
                did_html = "".join(f"<li>{_e(x)}</li>" for x in did[:7])
                links = "".join(f'<a class="nb" href="{sl}/{_e(bf)}" target="_blank" rel="noopener">{_e(nm)}</a>' for sl, nm in zip(slugs, names))
                bscore = f'<div class="pg-score build"><span class="k">In the build</span><b style="--g:{gcol.get(bb["grade"], "#b54708")}">{bb["score"]}<i>{_e(bb["grade"])}</i></b><span>{fixed} check{"s" if fixed != 1 else ""} fixed</span></div>'
                side = (f'<div class="pg-new"><h4>What we did on this page</h4><ul class="did">{did_html}</ul>'
                        f'<div class="cmplinks"><a class="lb" href="https://{_e(sa.get("domain", ""))}{_e(r["url"])}" target="_blank" rel="noopener">Live page today</a><span class="vs">vs</span>{links}</div>'
                        f'<p class="fine" style="margin:8px 0 0">New URL: /{_e(bf)}. New title: {_e(bb.get("title", ""))}</p></div>')
            else:
                bscore = '<div class="pg-score build"><span class="k">In the build</span><b style="--g:#5b616b">&ndash;</b><span>retired, 301</span></div>'
                side = f'<div class="pg-new"><h4>What we did on this page</h4><ul class="did"><li>Retired. The content was out of date (COVID notices, kiosk pages, an old survey).</li><li>The URL redirects to the nearest live page so no link or ranking is lost.</li></ul><div class="cmplinks"><a class="lb" href="https://{_e(sa.get("domain", ""))}{_e(r["url"])}" target="_blank" rel="noopener">Live page today</a></div></div>'
            head_scores = (f'<div class="scores"><div class="sc"><span class="k">Today</span><b style="--g:{gcol.get(r["grade"], "#b54708")}">{r["score"]}<i>{_e(r["grade"])}</i></b></div><span class="to" aria-hidden="true"></span>'
                           + (f'<div class="sc"><span class="k">The build</span><b style="--g:{gcol.get(bb["grade"], "#b54708")}">{bb["score"]}<i>{_e(bb["grade"])}</i></b></div><span class="fx">{fixed} check{"s" if fixed != 1 else ""} fixed</span>' if bb is not None else '<div class="sc"><span class="k">The build</span><b style="--g:#5b616b">n/a</b></div><span class="fx">retired, 301</span>') + "</div>")
            cards.append(f'<article class="pg cmp3" data-q="{_e((r["url"] + " " + r["title"] + " " + r["h1"] + " " + r["type"]).lower())}" data-issues="{r.get("issues", 0)}" data-type="{_e(r["type"])}" data-score="{r["score"]}" data-words="{r["words"]}" data-url="{_e(r["url"])}">'
                         f'<header class="pg-head"><div class="pg-id"><a href="https://{_e(sa.get("domain", ""))}{_e(r["url"])}" target="_blank" rel="noopener">{_e(r["url"])}</a><small>{_e(r["title"])}</small><span class="type">{_e(r["type"])} page</span></div>{head_scores}</header>'
                         f'<div class="pg-body"><div class="pg-checks">{pills}</div>{side}</div></article>')
        g = sm.get("grades", {})
        a_tiles = "".join(f'<div class="stile"><b>{_e(v)}</b><span>{_e(l)}</span></div>' for v, l in [
            (f'{sm.get("avg_score", 0)}', "average readiness score out of 100"), (f'{g.get("A", 0) + g.get("B", 0)} of {n}', "pages scoring B or better"), (f'{g.get("D", 0) + g.get("F", 0)} of {n}', "pages scoring D or F"), (f'{sm.get("faq", 0)} of {n}', "pages with FAQPage schema"),
            (f'{sm.get("service", 0)} of {n}', "pages with Service schema"), (f'{sm.get("review", 0)}', "pages with Review or rating schema"), (f'{sm.get("question_headings", 0)} of {n}', "pages with a question-form heading"), (f'{sm.get("thin", 0)} of {n}', "pages under 300 words")])
        bd = sa.get("build") or {}
        build_html = ""
        if bd.get("summary"):
            bs = bd["summary"]; bg = bs.get("grades", {}); bn = bs.get("pages", 0)
            mig = sa.get("migration") or {}
            def _cmp(label, today, build):
                return f'<div class="cmp-row"><span class="lbl">{_e(label)}</span><span class="today">{_e(today)}</span><span class="arrow" aria-hidden="true"></span><span class="build">{_e(build)}</span></div>'
            rows_cmp = _cmp("Average readiness score", f'{sm.get("avg_score", 0)} of 100', f'{bs.get("avg_score", 0)} of 100') + _cmp("Pages scoring A", f'{g.get("A", 0)} of {n}', f'{bg.get("A", 0)} of {bn}') + _cmp("Pages scoring D or F", f'{g.get("D", 0) + g.get("F", 0)} of {n}', f'{bg.get("D", 0) + bg.get("F", 0)} of {bn}') + _cmp("Pages with FAQPage schema", f'{sm.get("faq", 0)} of {n}', f'{bs.get("faq", 0)} of {bn}') + _cmp("Pages with Service or Article schema", f'{sm.get("service", 0) + sm.get("article", 0)} of {n}', f'{bs.get("service", 0) + bs.get("article", 0)} of {bn}') + _cmp("Pages with LocalBusiness schema", f'{sm.get("local", 0)} of {n}', f'{bs.get("local", 0)} of {bn}') + _cmp("Pages with a question-form heading", f'{sm.get("question_headings", 0)} of {n}', f'{bs.get("question_headings", 0)} of {bn}') + _cmp("Pages under 300 words", f'{sm.get("thin", 0)} of {n}', f'{bs.get("thin", 0)} of {bn}') + _cmp("Titles with the city in them", f'{sm.get("city_in_title", 0)} of {n}', f'{bs.get("city_in_title", 0)} of {bn}')
            per_opt = "".join(f'<span class="opt"><b>{_e(k)}</b> {v.get("avg_score", 0)} average, {v.get("grades", {}).get("A", 0)} of {v.get("pages", 0)} A</span>' for k, v in (bd.get("per_option") or {}).items())
            mig_line = (f'<p class="fine" style="margin-top:14px">Page for page: {mig.get("redirects", 0)} URLs on vanausdall.com map to a page in the build ({mig.get("pages", 0)} rebuilt from their current copy, the rest merged into a stronger page); {len(mig.get("retired", []))} retired pages (COVID notices, kiosk pages, a survey) redirect to the nearest page. The 301 map is in the download.</p>') if mig else ""
            build_html = (f'<div class="cmpbox"><div class="cmphead"><h3 class="h3">The same seventeen checks, run on the build</h3><p>Every recommendation on the cards below is already in place on all three options. The scores on the right are the build, scored by the same script.</p></div>'
                          f'<div class="cmp-rows"><div class="cmp-row head"><span class="lbl"></span><span class="today">vanausdall.com today</span><span class="arrow"></span><span class="build">The build, any option</span></div>{rows_cmp}</div>'
                          f'<div class="opts">{per_opt}</div>{mig_line}'
                          f'<p class="fine">What is deliberately not marked up: Review and AggregateRating. Those wait for the Google review program, because marking up self-published testimonials is against Google&#39;s guidelines and we will not do it. That is the six points between the build and 100.</p></div>')
        def _site(ok, label):
            return f'<li class="{"ok" if ok else "bad"}"><b>{"Yes" if ok else "No"}</b> {_e(label)}</li>'
        site_html = "<ul class=\"sitechk\">" + _site(site.get("https", True), "Served over HTTPS with one canonical host") + _site(site.get("robots_allows_all", True), "robots.txt allows Google and all four AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended)") + _site(site.get("sitemap", True), f"Sitemap declared, {site.get('sitemap_urls', 0)} URLs") + _site(not site.get("sitemap_blog_query_urls"), f"Blog posts on clean URLs ({site.get('sitemap_blog_query_urls', 0)} are blog?p= query strings today)") + _site(site.get("llms_txt", False), "llms.txt published for AI assistants") + _site(sm.get("breadcrumb", 0) > 0, "BreadcrumbList schema anywhere on the site") + _site(sm.get("article", 0) > 0, "Article or BlogPosting schema anywhere on the site") + _site(False, "sameAs links in the Organization schema to LinkedIn, Facebook, YouTube") + "</ul>"
        types_opts = "".join(f'<option value="{t}">{t.capitalize()} pages ({sm.get("by_type", {}).get(t, {}).get("pages", 0)}, average {sm.get("by_type", {}).get(t, {}).get("avg", 0)})</option>' for t in ("service", "city", "company", "case study", "policy"))
        csv_btn = ((f'<a class="btn small" href="{_e(sa["csv_href"])}" download>Download the spreadsheet (CSV)</a>') if sa.get("csv_href") else "") + ('<a class="btn small" href="redirects.csv" download style="background:transparent;border:1px solid var(--accent);color:var(--ink)">Download the 301 map (CSV)</a>' if (sa.get("migration") or {}).get("map") else "")
        audit_js = '<script>(function(){var w=document.getElementById("alist");if(!w)return;var q=document.getElementById("aq"),pb=document.getElementById("aprob"),ty=document.getElementById("atype"),so=document.getElementById("asort"),c=document.getElementById("acount"),cards=Array.prototype.slice.call(w.children);function f(){var s=(q.value||"").toLowerCase(),p=pb.checked,tv=ty.value,n=0;cards.forEach(function(r){var ok=(!s||r.getAttribute("data-q").indexOf(s)>-1)&&(!p||+r.getAttribute("data-issues")>=5)&&(!tv||r.getAttribute("data-type")===tv);r.hidden=!ok;if(ok)n++});c.textContent=n+" of "+cards.length+" pages"}function srt(){var v=so.value;cards.sort(function(a,b){if(v==="score-asc")return +a.getAttribute("data-score")-+b.getAttribute("data-score");if(v==="score-desc")return +b.getAttribute("data-score")-+a.getAttribute("data-score");if(v==="words")return +a.getAttribute("data-words")-+b.getAttribute("data-words");return a.getAttribute("data-url").localeCompare(b.getAttribute("data-url"))});cards.forEach(function(r){w.appendChild(r)})}q.addEventListener("input",f);pb.addEventListener("change",f);ty.addEventListener("change",f);so.addEventListener("change",srt);srt()})();</script>'
        audit_html = (f'<section id="audit"><div class="wrap wide"><p class="eyebrow">Every page on {_e(sa.get("domain", "the current site"))}</p><h2>{n} pages today, and the page that replaces each one</h2><p class="lead">Every URL in the sitemap except blog posts and PDFs, fetched {_e(sa.get("as_of", ""))} and parsed for title, meta description, headings, words, images, links and JSON-LD schema. Each page gets a readiness score out of 100 across seventeen checks, weighted toward what answer engines read: FAQ schema, Service schema, question-form headings and depth. Red is a check the page fails today. The fixes for each page are on the right.</p>'
                      f'<div class="stiles eight">{a_tiles}</div>{build_html}'
                      f'<h3 class="h3" style="margin-top:30px">Site-wide checks</h3>{site_html}'
                      f'<div class="afilter"><input type="search" id="aq" placeholder="Filter by URL, title or H1" aria-label="Filter pages"><select id="atype" aria-label="Page type"><option value="">All page types</option>{types_opts}</select><select id="asort" aria-label="Sort"><option value="score-asc">Lowest score first</option><option value="score-desc">Highest score first</option><option value="words">Fewest words first</option><option value="url">By URL</option></select><label><input type="checkbox" id="aprob"> Only pages failing five or more checks</label><span id="acount" aria-live="polite">{n} pages</span>{csv_btn}</div>'
                      f'<div class="pglist" id="alist">{"".join(cards)}</div>'
                      f'<p class="fine">Scoring weights: FAQPage schema 14, Service or Article schema 10, at least 300 words 10, question-form headings 8, title length 6, city in title 6, Review schema 6, meta length 5, one H1 5, two or more H2s 5, depth over 600 words 4, LocalBusiness 4, alt text 4, form or call 4, internal links 3, canonical 3, branded share image 3. Grades: A 85 and up, B 70, C 55, D 40, F below. Word counts exclude navigation, header and footer. Image alt counts include the logo.</p>'
                      f'</div></section>{audit_js}')
    n = _n_saved
    heard = "".join(f"<li>{_e(x)}</li>" for x in pitch.get("heard", []))
    confirm = "".join(f"<li>{_e(x)}</li>" for x in pitch.get("confirm", []))
    heard_intro = pitch.get("heard_intro", "Tell us if any of this is wrong. It outranks our house defaults.")
    found = "".join(f"<li>{_e(x)}</li>" for x in pitch.get("found", []))
    plan = "".join(f'<div class="step"><div class="when">{_e(w)}</div><p>{_e(what)}</p></div>' for w, what in pitch.get("plan", []))
    pages = content["pages"]
    page_opts = "".join(f'<option value="{_e(pg["file"])}">{_e(_pname(pg))}</option>' for pg in pages)
    frames = "".join(
        f'<figure><figcaption>{_e(t.replace("Quantum ", ""))}</figcaption><div class="scale">'
        f'<iframe title="{_e(t.replace("Quantum ", ""))} preview" loading="lazy" src="{_slug(t)}/index.html" data-dir="{_slug(t)}" width="1440" height="1000"></iframe></div>'
        f'<a class="open" href="{_slug(t)}/index.html" target="_blank" rel="noopener" data-dir="{_slug(t)}">Open full size</a></figure>'
        for t in themes)
    every = ""
    for t in themes:
        every += f'<div class="col"><h3 class="h4">{_e(t.replace("Quantum ", ""))}</h3>' + "".join(
            f'<a href="{_slug(t)}/{pg["file"]}" target="_blank" rel="noopener">{_e(_pname(pg))}</a>' for pg in pages) + "</div>"
    qc = pitch.get("qbs_contact", {})
    std = ('<a class="alt" href="standard.html" target="_blank" rel="noopener"><h3 class="h4">The Quantum Website Standard</h3>'
           '<p>The ten things every site we build is guaranteed to have at launch, and the evidence you receive for each.</p><span>Open</span></a>') if standard else ""
    phone_href = re.sub(r"[^0-9+]", "", qc.get("phone", ""))

    css = f"""
:root{{--bg:#ffffff;--bg-alt:{alt_bg};--fg:{fg};--muted:{muted};--border:{border};--accent:{b["accent"]};--ink:{ink};--chrome:{chrome};--chrome-fg:{chrome_fg};--chrome-muted:{chrome_muted};--chrome-hover:{chrome_hover};--btn-fg:{btn_fg};--navy:{navy}}}
{dark_css}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 Inter,system-ui,sans-serif}}
a{{color:var(--ink)}}
.skip{{position:absolute;top:-200px;left:8px;background:var(--accent);color:var(--btn-fg);padding:10px 16px;border-radius:6px}}.skip:focus{{top:8px}}
html{{scroll-padding-top:80px}}
.top{{background:var(--chrome);color:var(--chrome-fg);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:20}}
@media(max-width:900px){{.top{{position:static}}html{{scroll-padding-top:12px}}}}.top .wrap{{display:flex;align-items:center;justify-content:space-between;gap:14px;min-height:64px}}.top img{{height:36px}}
.top nav{{display:flex;gap:4px;flex-wrap:wrap}}.top nav a{{color:var(--chrome-muted);text-decoration:none;font-size:13.5px;padding:10px 10px;border-radius:8px;min-height:44px;display:inline-flex;align-items:center}}.top nav a:hover{{color:var(--chrome-fg);background:var(--chrome-hover)}}
.wrap{{max-width:1040px;margin:0 auto;padding:0 24px}}
section{{padding:64px 0;border-bottom:1px solid var(--border)}}
.eyebrow{{font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink);font-weight:600;margin:0 0 14px}}
h1{{font-size:clamp(32px,5vw,52px);line-height:1.04;letter-spacing:-.02em;margin:0 0 16px;text-wrap:balance;max-width:20ch}}
h2{{font-size:clamp(24px,3vw,34px);line-height:1.1;letter-spacing:-.02em;margin:0 0 12px;text-wrap:balance}}
h3,.h3{{font-size:22px;margin:0 0 6px;letter-spacing:-.01em}}h4,.h4{{font-size:16px;margin:0 0 6px}}.dir h2.h3{{font-size:22px;line-height:1.2}}
.confirm li{{margin:10px 0}}
.lead{{color:var(--muted);max-width:62ch;margin:0 0 28px;font-size:17px}}
.dirs{{display:grid;grid-template-columns:repeat({n},1fr);gap:18px}}
.dir{{border:1px solid var(--border);border-radius:14px;padding:24px;background:var(--bg-alt);display:flex;flex-direction:column;gap:18px}}
.dir .n{{font-size:13px;color:var(--muted);letter-spacing:.08em}}.dir p{{margin:6px 0 0;color:var(--muted);font-size:14.5px}}
.rec{{display:inline-block;margin:6px 0 0;font-size:13px;font-weight:600;letter-spacing:.04em;color:var(--ink);border:1px solid var(--accent);border-radius:999px;padding:2px 10px;vertical-align:middle}}
.spec{{display:grid;grid-template-columns:1fr 1fr;gap:10px 16px;margin:0}}.spec dt{{font-size:13px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}}.spec dd{{margin:2px 0 0;font-weight:600;font-size:14.5px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:10px 18px;background:var(--accent);color:var(--btn-fg);border-radius:8px;text-decoration:none;font-weight:600;margin-top:auto}}
.btn:hover{{filter:brightness(.95)}}
.pick{{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:start}}
.why{{padding:16px 0;border-top:1px solid var(--border)}}.why:last-of-type{{border-bottom:1px solid var(--border)}}.why p{{margin:4px 0 0;color:var(--muted);font-size:15px}}
.change{{background:var(--bg-alt);border:1px solid var(--border);border-radius:12px;padding:20px 22px;margin-top:22px;font-size:15px}}
.alts{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}.alts.single{{grid-template-columns:1fr;max-width:560px}}.alt{{display:block;border:1px solid var(--border);border-radius:12px;padding:20px 22px;text-decoration:none;color:inherit;background:var(--bg-alt)}}.alt:hover{{border-color:var(--accent)}}.alt p{{color:var(--muted);font-size:14.5px;margin:0 0 10px}}.alt span{{font-weight:600;color:var(--ink);font-size:14px}}
.cmp-bar{{display:flex;gap:14px;align-items:center;margin:0 0 18px;flex-wrap:wrap}}select{{font:inherit;font-size:16px;padding:10px 12px;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--fg);min-height:44px}}
.frames{{display:grid;grid-template-columns:repeat({n},1fr);gap:14px}}.frames figure{{margin:0}}.frames figcaption{{font-size:13px;color:var(--muted);margin:0 0 8px;font-weight:600}}
.frames .scale{{width:100%;aspect-ratio:1440/1000;overflow:hidden;border:1px solid var(--border);border-radius:12px;background:#fff;position:relative}}
.frames iframe{{width:1440px;height:1000px;border:0;transform-origin:0 0;position:absolute;left:0;top:0;pointer-events:none}}
.frames .open{{display:inline-flex;align-items:center;min-height:44px;font-size:14px;font-weight:600;text-decoration:none;color:var(--ink)}}
.cmp-note{{display:none;color:var(--muted);font-size:14.5px}}
.thumb{{display:block;border-radius:10px;overflow:hidden;border:1px solid var(--border);aspect-ratio:16/10;background:#fff}}.thumb img{{width:100%;height:100%;object-fit:cover;object-position:top;display:block}}
.specd summary{{cursor:pointer;font-size:13.5px;color:var(--muted);min-height:44px;display:flex;align-items:center;list-style:none}}.specd summary::-webkit-details-marker{{display:none}}.specd summary::before{{content:"+";margin-right:8px;color:var(--ink);font-weight:700}}.specd[open] summary::before{{content:"\2212"}}
.specd .spec{{margin-top:8px}}
.every{{display:grid;grid-template-columns:repeat({n},1fr);gap:24px}}.every .col a{{display:flex;align-items:center;min-height:44px;text-decoration:none;color:var(--fg);border-top:1px solid var(--border);font-size:15px}}.every .col a:hover{{color:var(--ink)}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:40px}}
.stiles{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:26px}}.stile{{border:1px solid var(--border);border-radius:12px;padding:18px 20px;background:var(--bg-alt)}}.stile b{{display:block;font-size:34px;line-height:1;letter-spacing:-.02em;color:var(--ink)}}.stile span{{display:block;margin-top:8px;font-size:13.5px;color:var(--muted)}}
.asof{{font-size:13px;color:var(--muted);font-weight:400;margin-left:8px}}
.tblwrap{{overflow-x:auto;margin-top:14px}}table.seo{{width:100%;border-collapse:collapse;font-size:14.5px}}table.seo th,table.seo td{{text-align:left;padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top}}table.seo th{{font-size:12.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}}table.seo code{{font-size:13px;background:var(--bg-alt);padding:2px 6px;border-radius:6px}}
@media(max-width:767px){{.stiles{{grid-template-columns:1fr 1fr}}}}
.stiles.eight{{grid-template-columns:repeat(4,1fr)}}.afilter{{display:flex;flex-wrap:wrap;align-items:center;gap:14px 18px;margin:26px 0 14px}}.afilter input[type=search]{{flex:1 1 260px;min-height:44px;padding:0 14px;border:1px solid var(--border);border-radius:10px;font:inherit;background:#fff;color:var(--ink)}}.afilter label{{display:flex;align-items:center;gap:8px;font-size:14.5px;color:var(--fg)}}.afilter input[type=checkbox]{{width:18px;height:18px;accent-color:var(--accent)}}#acount{{font-size:14px;color:var(--muted)}}.btn.small{{padding:10px 16px;font-size:14px}}
.tblwrap.audit{{max-height:720px;overflow:auto;border:1px solid var(--border);border-radius:12px;background:#fff}}table.audit{{font-size:13.5px;border-collapse:separate;border-spacing:0;min-width:1040px;width:100%}}table.audit thead th{{position:sticky;top:0;background:var(--navy);color:#fff;z-index:2;cursor:pointer;user-select:none;padding:12px 10px;text-align:left;font-size:12px;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap}}table.audit thead th[aria-sort=ascending]::after{{content:" \\2191"}}table.audit thead th[aria-sort=descending]::after{{content:" \\2193"}}table.audit tbody th{{text-align:left;font-weight:500;padding:9px 10px;border-bottom:1px solid var(--border);min-width:300px;max-width:420px}}table.audit tbody th a{{color:var(--accent);text-decoration:none;font-weight:600;word-break:break-all}}table.audit tbody th small{{display:block;color:var(--muted);font-size:12px;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:400px}}table.audit td{{padding:9px 10px;border-bottom:1px solid var(--border);text-align:center;white-space:nowrap}}table.audit td.ok{{color:#1b7f4b;font-weight:600}}table.audit td.bad{{color:#b3261e;font-weight:600;background:#fdf1f0}}table.audit td.iss b{{display:inline-block;min-width:28px;padding:2px 8px;border-radius:999px;background:var(--bg-alt);color:var(--ink)}}table.audit tbody tr:hover td,table.audit tbody tr:hover th{{background:var(--bg-alt)}}table.audit tbody tr:hover td.bad{{background:#f8e3e1}}.fine{{font-size:13px;color:var(--muted);margin-top:14px}}
@media(max-width:1024px){{.stiles.eight{{grid-template-columns:repeat(2,1fr)}}}}
.wrap.wide{{max-width:1360px}}.sitechk{{list-style:none;padding:0;margin:12px 0 0;display:grid;grid-template-columns:repeat(2,1fr);gap:8px 22px}}.sitechk li{{display:flex;gap:10px;align-items:baseline;font-size:14.5px;padding:8px 12px;border-radius:8px;background:#fff;border:1px solid var(--border)}}.sitechk li b{{min-width:34px;font-size:13px}}.sitechk li.ok b{{color:#1b7f4b}}.sitechk li.bad b{{color:#b3261e}}.afilter select{{min-height:44px;padding:0 12px;border:1px solid var(--border);border-radius:10px;font:inherit;background:#fff;color:var(--ink)}}
@media(max-width:767px){{.sitechk{{grid-template-columns:1fr}}}}
.sch{{display:inline-block;font-size:11px;padding:2px 7px;border-radius:999px;background:var(--bg-alt);color:var(--ink);margin:1px 3px 1px 0;border:1px solid var(--border)}}.sch.none{{color:#b3261e;background:#fdf1f0;border-color:#f3c9c5}}
.cmpbox{{margin-top:28px;background:var(--navy);color:#fff;border-radius:16px;padding:26px 28px}}.cmpbox .h3,.cmpbox h3{{color:#fff;margin:0 0 6px}}.cmphead p{{margin:0 0 18px;color:rgba(255,255,255,.85);max-width:760px}}.cmp-rows{{display:grid;gap:6px}}.cmp-row{{display:grid;grid-template-columns:1.6fr 1fr 40px 1fr;align-items:center;gap:10px;padding:9px 12px;border-radius:10px;background:rgba(255,255,255,.06)}}.cmp-row.head{{background:none;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.7);padding-bottom:0}}.cmp-row .lbl{{font-weight:600}}.cmp-row .today{{color:#ffb4a8;font-weight:700;text-align:right}}.cmp-row .build{{color:#8fe3b0;font-weight:800;font-size:17px}}.cmp-row .arrow{{width:40px;height:2px;background:rgba(255,255,255,.35);justify-self:center;position:relative}}.cmp-row .arrow::after{{content:"";position:absolute;right:-1px;top:-4px;border:5px solid transparent;border-left-color:rgba(255,255,255,.35)}}.cmp-row.head .arrow{{background:none}}.cmp-row.head .arrow::after{{display:none}}.opts{{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}}.opts .opt{{background:rgba(255,255,255,.1);border-radius:999px;padding:6px 12px;font-size:13.5px}}.cmpbox .fine{{color:rgba(255,255,255,.75)}}
@media(max-width:700px){{.cmp-row{{grid-template-columns:1fr 1fr;gap:4px}}.cmp-row .lbl{{grid-column:1/-1}}.cmp-row .arrow{{display:none}}.cmp-row .today{{text-align:left}}}}
.pg.cmp2{{grid-template-columns:minmax(220px,1.1fr) 150px minmax(320px,2.6fr) minmax(220px,1.2fr)}}.pg-scores{{display:grid;gap:10px}}.pg-score .k{{display:block;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}}.pg-score.build b{{box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 25%,transparent)}}
.pg-checks .legend{{flex-basis:100%;font-size:12px;color:var(--muted);margin-bottom:2px}}.pg-checks .legend b{{font-weight:700}}.pg-checks .legend b.bad{{color:#b3261e}}.pg-checks .legend b.ok{{color:#1b7f4b}}.pg-checks .legend em,.pl2 em{{display:inline-block;width:14px;height:2px;background:var(--border);vertical-align:middle;margin:0 2px;position:relative}}.pl2 em::after,.pg-checks .legend em::after{{content:"";position:absolute;right:-1px;top:-3px;border:4px solid transparent;border-left-color:var(--border)}}
.pl2{{display:inline-flex;align-items:center;gap:5px;font-size:12.5px;line-height:1;padding:6px 9px;border-radius:8px;border:1px solid var(--border);background:#fff;color:var(--ink);white-space:nowrap}}.pl2 i{{font-style:normal;color:var(--muted);font-size:11.5px;margin-right:2px}}.pl2 b{{font-weight:700}}.pl2 b.bad{{color:#b3261e}}.pl2 b.ok{{color:#1b7f4b}}
.pg-new h4{{margin:0 0 6px;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}.pg-new .np a{{font-weight:700;color:var(--accent);text-decoration:none;word-break:break-all;font-size:14px}}.pg-new .np{{margin:0}}.pg-new .open{{margin:0;font-size:13.5px}}.pg-new .open a{{display:inline-block;margin-right:6px;padding:4px 10px;border-radius:999px;background:var(--accent);color:#fff;text-decoration:none;font-weight:600;font-size:12.5px}}
@media(max-width:1100px){{.pg.cmp2{{grid-template-columns:1fr 150px}}.pg.cmp2 .pg-checks,.pg.cmp2 .pg-new{{grid-column:1/-1}}}}@media(max-width:600px){{.pg.cmp2{{grid-template-columns:1fr}}}}
.did{{margin:0 0 10px;padding-left:16px}}.did li{{font-size:13px;line-height:1.4;margin:0 0 3px;color:var(--fg)}}.cmplinks{{display:flex;flex-wrap:wrap;align-items:center;gap:6px}}.cmplinks a{{display:inline-block;padding:6px 11px;border-radius:999px;text-decoration:none;font-weight:600;font-size:12.5px}}.cmplinks .lb{{background:#fff;border:1px solid var(--border);color:var(--ink)}}.cmplinks .nb{{background:var(--accent);color:#fff}}.cmplinks .vs{{font-size:12px;color:var(--muted);margin:0 2px}}
.pg.cmp3{{display:block;padding:0;overflow:hidden}}.pg-head{{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px 24px;padding:16px 22px;border-bottom:1px solid var(--border);background:var(--bg-alt)}}.pg-head .pg-id a{{font-size:16px}}.pg-head .pg-id small{{max-width:640px}}
.scores{{display:flex;align-items:center;gap:12px}}.scores .sc{{text-align:center}}.scores .k{{display:block;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:3px}}.scores b{{display:inline-flex;align-items:baseline;gap:6px;font-size:22px;color:#fff;background:var(--g);border-radius:9px;padding:6px 11px;line-height:1}}.scores b i{{font-style:normal;font-size:12px;opacity:.9;border-left:1px solid rgba(255,255,255,.4);padding-left:6px}}.scores .to{{width:26px;height:2px;background:var(--border);position:relative;margin-top:14px}}.scores .to::after{{content:"";position:absolute;right:-1px;top:-4px;border:5px solid transparent;border-left-color:var(--border)}}.scores .fx{{font-size:13px;color:#1b7f4b;font-weight:700;margin-left:6px;margin-top:14px}}
.pg-body{{display:grid;grid-template-columns:minmax(320px,1.6fr) minmax(280px,1fr);gap:22px 32px;padding:18px 22px 20px}}.pg-body .pg-checks{{display:grid;gap:12px;align-content:start}}
.grp h5{{margin:0 0 6px;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}.grp h5 span{{display:inline-block;min-width:20px;text-align:center;background:var(--bg-alt);border-radius:999px;padding:1px 7px;margin-left:4px;color:var(--ink)}}.pills{{display:flex;flex-wrap:wrap;gap:6px}}
.pl3{{display:inline-flex;align-items:center;gap:5px;font-size:12.5px;line-height:1;padding:6px 9px;border-radius:8px;border:1px solid var(--border);background:#fff;color:var(--ink);white-space:nowrap}}.pl3 i{{font-style:normal;color:var(--muted);font-size:11.5px;margin-right:2px}}.pl3.ok{{border-color:#bfe3cc;background:#eef8f1;color:#14532d;font-weight:600}}.pl3.ok em{{display:inline-block;width:12px;height:2px;background:#8fcfa4;vertical-align:middle;position:relative}}.pl3.ok em::after{{content:"";position:absolute;right:-1px;top:-3px;border:4px solid transparent;border-left-color:#8fcfa4}}.pl3.bad{{border-color:#f3c9c5;background:#fdf1f0;color:#8f1d16;font-weight:600}}.pl3.pass{{color:var(--muted);background:var(--bg-alt)}}
details.grp summary{{cursor:pointer;font-size:12.5px;color:var(--muted);list-style:none;display:inline-block;padding:5px 10px;border:1px dashed var(--border);border-radius:999px}}details.grp summary::-webkit-details-marker{{display:none}}details.grp[open] summary{{margin-bottom:8px}}
@media(max-width:900px){{.pg-body{{grid-template-columns:1fr}}}}
.pglist{{display:grid;gap:12px;margin-top:6px}}.pg{{display:grid;grid-template-columns:minmax(240px,1.35fr) 104px minmax(300px,2.4fr) minmax(260px,1.6fr);gap:0 22px;align-items:start;background:#fff;border:1px solid var(--border);border-radius:14px;padding:18px 20px}}.pg[hidden]{{display:none}}
.pg-id a{{font-weight:700;color:var(--accent);text-decoration:none;word-break:break-all;font-size:15px}}.pg-id small{{display:block;color:var(--muted);font-size:13px;margin-top:3px;line-height:1.4}}.pg-id .type{{display:inline-block;margin-top:8px;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);border:1px solid var(--border);border-radius:999px;padding:2px 8px}}.pg-id .schs{{margin-top:8px}}
.pg-score{{text-align:center}}.pg-score b{{display:inline-flex;align-items:baseline;gap:6px;font-size:26px;color:#fff;background:var(--g);border-radius:10px;padding:8px 12px;line-height:1}}.pg-score b i{{font-style:normal;font-size:13px;opacity:.9;border-left:1px solid rgba(255,255,255,.4);padding-left:6px}}.pg-score span{{display:block;font-size:11.5px;color:var(--muted);margin-top:4px}}
.pg-checks{{display:flex;flex-wrap:wrap;gap:6px}}.pl{{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;line-height:1;padding:6px 9px;border-radius:8px;border:1px solid var(--border);background:var(--bg-alt);color:var(--ink);white-space:nowrap}}.pl i{{font-style:normal;color:var(--muted);font-size:11.5px}}.pl.ok{{border-color:#bfe3cc;background:#eef8f1}}.pl.ok::before{{content:"";width:7px;height:7px;border-radius:50%;background:#1b7f4b}}.pl.bad{{border-color:#f3c9c5;background:#fdf1f0;color:#8f1d16;font-weight:600}}.pl.bad i{{color:#a8433c}}.pl.bad::before{{content:"";width:7px;height:7px;border-radius:50%;background:#b3261e}}
.pg-recs h4{{margin:0 0 6px;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}.pg-recs ul{{margin:0;padding-left:16px}}.pg-recs li{{font-size:13.5px;line-height:1.4;margin:0 0 4px;color:var(--fg)}}
@media(max-width:1100px){{.pg{{grid-template-columns:1fr 104px;gap:14px 18px}}.pg-checks,.pg-recs{{grid-column:1/-1}}}}@media(max-width:600px){{.pg{{grid-template-columns:1fr}}.pg-score{{text-align:left}}}}



section.band{{background:var(--navy);color:#fff}}section.band .eyebrow{{color:#fff;opacity:.85}}section.band h1,section.band h2{{color:#fff}}section.band .lead{{color:rgba(255,255,255,.85)}}.dir{{border-top:4px solid var(--accent);background:#fff;box-shadow:0 12px 34px rgba(0,0,0,.07)}}.why{{border-left:3px solid var(--accent);padding-left:16px}}.stile b{{color:var(--accent)}}.stile{{background:#fff;border-top:3px solid var(--accent)}}.turn{{background:var(--navy);color:#fff;border-color:var(--navy)}}.turn .eyebrow{{color:#fff;opacity:.85}}.turn h2{{color:#fff}}.turn .lead{{color:rgba(255,255,255,.85)}}.change{{border-left:4px solid var(--accent)}}section:nth-of-type(even):not(.band){{background:var(--bg-alt)}}.fnds{{display:grid;gap:12px;margin-top:16px}}.fnd{{display:grid;grid-template-columns:48px 1fr;gap:14px;background:#fff;border:1px solid var(--border);border-left:5px solid var(--accent);border-radius:12px;padding:18px 20px}}.fnd .rk{{font-size:30px;font-weight:800;color:var(--accent);line-height:1}}.fnd h3{{margin:6px 0 8px}}.fnd p{{margin:4px 0;font-size:14.5px;color:var(--fg)}}.sevc{{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#fff;background:var(--sev);border-radius:999px;padding:3px 9px}}ul{{margin:0;padding-left:18px}}li{{margin:8px 0;color:var(--fg)}}li::marker{{color:var(--accent)}}
.plan{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}}.step{{border-top:2px solid var(--accent);padding-top:12px}}.when{{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink);font-weight:700}}.step p{{margin:8px 0 0;font-size:14.5px;color:var(--muted)}}
.turn{{background:var(--bg-alt);border:1px solid var(--border);border-radius:14px;padding:28px}}.turn a.btn{{margin:0 12px 12px 0}}
footer{{padding:36px 0 80px;color:var(--muted);font-size:13.5px;max-width:66ch}}
select{{max-width:100%}}
@media(max-width:900px){{.dirs,.every,.plan{{grid-template-columns:1fr}}.pick,.alts,.two{{grid-template-columns:1fr}}.frames,.cmp-bar{{display:none}}.cmp-note{{display:block}}}}
"""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_e(content["client"])}, three website directions</title>
<meta name="description" content="Three complete website directions for {_e(content["client"])}, prepared by Quantum Business Solutions.">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{_e(base)}/">
<meta property="og:title" content="{_e(content["client"])}, three website directions">
<meta property="og:image" content="{_e(base)}/assets/hero-og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<style>{css}</style></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap"><img src="{_e(b["logo"])}" alt="{_e(content["client"])}" height="36" width="99"><nav aria-label="Sections"><a href="#three">The three</a><a href="#pick">{"Our pick" if recommend else "How to choose"}</a><a href="#compare">Compare</a><a href="#search">Search</a><a href="#audit">Every page audited</a><a href="#heard">Fixed</a><a href="#confirm">To confirm</a><a href="#every">Every page</a><a href="#plan">The plan</a><a href="#turn">Your turn</a>{ds_link}</nav></div></header>
<main id="main">
<section class="band"><div class="wrap"><p class="eyebrow">Quantum Business Solutions for {_e(content["client"])}</p><h1>Same site. Three ways to design it.</h1>
<p class="lead">Each one is the whole site, not a home page and two mockups: every page is built and live in all three. The words are the same in all three and the composition is not, so the decision in front of you is about direction, not copy. Open any one, then use the switcher pinned to the bottom of the page to flip between all three without losing your place.</p></div></section>
<section id="three"><div class="wrap"><p class="eyebrow">The three</p><div class="dirs">{"".join(specs)}</div></div></section>
<section id="pick"><div class="wrap"><p class="eyebrow">{"Our recommendation" if recommend else "How to choose"}</p><div class="pick"><div><h2>{("We would build " + _e(pick_short)) if recommend else _e(pitch.get("choose_heading", "Three directions. Your call."))}</h2><p class="lead">{_e(roles.get(pick, "")) if recommend else _e(pitch.get("choose_intro", ""))}</p>{reasons}{('<div class="change"><strong>The one thing we would change:</strong> ' + _e(pitch.get("pick_change", "")) + '</div><p style="margin-top:22px"><a class="btn" href="' + pick_slug + '/index.html" target="_blank" rel="noopener">Open ' + _e(pick_short) + '</a></p>') if recommend else ""}</div>
<div><h3 class="h3" style="font-size:18px;margin-bottom:14px">{"If you would rather not" if recommend else "The three, in one line each"}</h3><div class="alts" style="grid-template-columns:1fr">{alts}</div></div></div></div></section>
<section id="compare"><div class="wrap"><p class="eyebrow">Side by side</p><h2>The same page, all three at once</h2><div class="cmp-bar"><label for="cmp">Pick a page</label><select id="cmp">{page_opts}</select></div><p class="cmp-note">Side by side needs a wider screen. On a phone, open each direction from the cards above.</p><div class="frames">{frames}</div></div></section>
{search_html}
{audit_html}
<section id="heard"><div class="wrap"><div class="two"><div><p class="eyebrow">What we are treating as fixed</p><h2>What your site and brand profile already say</h2><p class="lead" style="margin-bottom:12px">{_e(heard_intro)}</p><ul>{heard}</ul></div><div><p class="eyebrow">What we found</p><h2>And what we would do about it</h2><ul>{found}</ul></div></div></div></section>
<section id="confirm"><div class="wrap"><p class="eyebrow">To confirm with you</p><h2>Ten things we wrote as a draft, not a fact</h2><p class="lead">Each of these appears on the pages. None is built until you confirm or correct it.</p><ul class="confirm">{confirm}</ul></div></section>
<section id="every"><div class="wrap"><p class="eyebrow">Every page</p><h2>Built and live in all three</h2><div class="every">{every}</div></div></section>
<section id="plan"><div class="wrap"><p class="eyebrow">The plan</p><h2>From a choice to a live site</h2><div class="plan">{plan}</div>{('<div class="alts single" style="margin-top:28px">' + std + '</div>') if std else ""}</div></section>
<section id="turn"><div class="wrap"><div class="turn"><p class="eyebrow">Your turn</p><h2>Tell us which one, and what you would change</h2><p class="lead" style="margin-bottom:18px">Reply with the direction and anything on any page you would change. Nothing is locked until you say so.</p><a class="btn" href="mailto:{_e(qc.get("email", ""))}?subject={_e(content["client"])}%20website%20direction">Email {_e(qc.get("name", "us"))}</a><a class="btn" style="background:transparent;border:1px solid var(--accent);color:var(--ink)" href="tel:{_e(phone_href)}">Call {_e(qc.get("phone", ""))}</a></div></div></section>
</main>
<footer class="wrap">{_e(pitch.get("footer", "Prepared for " + pitch.get("prepared_for", content["client"]) + ". Nothing here is live or indexed."))}</footer>
<script>
(function () {{
  function fit() {{ document.querySelectorAll('.frames .scale').forEach(function (s) {{ var f = s.querySelector('iframe'); if (f) f.style.transform = 'scale(' + (s.clientWidth / 1440) + ')'; }}); }}
  fit(); window.addEventListener('resize', fit);
  document.getElementById('cmp').addEventListener('change', function (e) {{
    document.querySelectorAll('.frames iframe').forEach(function (f) {{ f.src = f.dataset.dir + '/' + e.target.value; }});
    document.querySelectorAll('.frames .open').forEach(function (a) {{ a.href = a.dataset.dir + '/' + e.target.value; }});
  }});
}})();
</script>
</body></html>
"""
