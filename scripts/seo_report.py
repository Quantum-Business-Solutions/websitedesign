#!/usr/bin/env python3
"""Render the client-facing SEO and AEO analysis as one HTML page, top findings first.

    python3 scripts/seo_report.py --brand brands/<slug>.md --basic <seo.json> --deep <seo-deep.json> \
        --client "Van Ausdall & Farrar" --domain vanausdall.com --accent "#2A71AF" --out <client-repo>/seo-report.html

Inputs are the two JSON files the analysis subagent writes (process/seo-aeo-analysis.md has the
contract). Every section renders only when its data exists, so a partial pull still produces a
page. The page carries the client's accent, a ranked findings scorecard at the top, then the
evidence in the order a buyer reads it: where you stand, competitors, opportunities, questions
people ask (AEO), page audit, AI answer visibility, backlinks, local, the 90-day plan, and what
we measure. No em dashes anywhere in the output; the renderer rewrites them.
"""
from __future__ import annotations

import argparse
import html
import json
import re

SEVERITY = {"critical": ("Critical", "#b42318"), "high": ("High", "#c4320a"), "medium": ("Medium", "#b54708"), "low": ("Low", "#175cd3")}


def E(x) -> str:
    s = "" if x is None else str(x)
    s = re.sub(r"\s*[—–]\s*", ", ", s)
    return html.escape(s, quote=True)


def fmt(n):
    if n is None or n == "":
        return "not pulled"
    if isinstance(n, (int, float)):
        return f"{n:,.0f}" if float(n).is_integer() else f"{n:,.2f}"
    return str(n)


def table(headers, rows, cls="tbl"):
    if not rows:
        return ""
    th = "".join(f"<th scope=\"col\">{E(h)}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tblwrap" tabindex="0"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def yn(v):
    if v is None:
        return '<span class="na">not pulled</span>'
    return '<span class="ok">yes</span>' if v else '<span class="bad">no</span>'


def section(sid, eyebrow, heading, body, intro=""):
    if not body:
        return ""
    return f'<section id="{sid}"><div class="wrap"><p class="eyebrow">{E(eyebrow)}</p><h2>{E(heading)}</h2>{f"<p class=lead>{E(intro)}</p>" if intro else ""}{body}</div></section>'


def render(basic: dict, deep: dict, client: str, domain: str, accent: str, as_of: str, prepared_for: str, hub_href: str = "index.html") -> str:
    findings = deep.get("findings") or []
    stats = basic.get("summary_stats") or []
    # ---------------- top findings
    cards = []
    for f in findings:
        sev = str(f.get("severity", "medium")).lower()
        label, color = SEVERITY.get(sev, SEVERITY["medium"])
        cards.append(
            f'<article class="finding"><div class="rank">{E(f.get("rank", ""))}</div><div class="fbody"><span class="sev" style="--sev:{color}">{label}</span>'
            f'<h3>{E(f.get("title", ""))}</h3><dl><div><dt>Evidence</dt><dd>{E(f.get("evidence", ""))}</dd></div><div><dt>What it costs</dt><dd>{E(f.get("impact", ""))}</dd></div>'
            f'<div><dt>What we do</dt><dd>{E(f.get("action", ""))}</dd></div></dl></div></article>')
    top = ""
    if cards:
        counts = {}
        for f in findings:
            counts[str(f.get("severity", "medium")).lower()] = counts.get(str(f.get("severity", "medium")).lower(), 0) + 1
        chips = "".join(f'<span class="chip" style="--sev:{SEVERITY[k][1]}">{counts[k]} {SEVERITY[k][0].lower()}</span>' for k in ("critical", "high", "medium", "low") if counts.get(k))
        top = f'<div class="chips">{chips}</div><div class="findings">{"".join(cards)}</div>'
    tiles = "".join(f'<div class="stile"><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l in stats)
    # ---------------- competitors
    comp_rows = [[E(c.get("domain")), fmt(c.get("traffic")), fmt(c.get("keywords")), fmt(c.get("authority"))] for c in (basic.get("competitors") or [])]
    comp = table(["Domain", "Organic visits a month", "Keywords", "Authority Score"], comp_rows)
    # ---------------- opportunities
    opp_rows = [[E(o.get("keyword")), fmt(o.get("volume")), fmt(o.get("kd")), E(o.get("vaf_position")), E(o.get("top_competitor"))] for o in (basic.get("opportunities") or [])]
    opp = table(["Keyword", "Searches a month", "Difficulty", f"{E(client.split()[0])} today", "Who ranks"], opp_rows)
    # ---------------- clusters
    cl_html = ""
    for c in deep.get("clusters") or []:
        rows = [[E(t.get("keyword")), fmt(t.get("volume")), fmt(t.get("kd")), fmt(t.get("cpc")), E(t.get("intent", ""))] for t in (c.get("terms") or [])]
        if rows:
            cl_html += f'<h3>{E(c.get("pillar", ""))}<small> seed: {E(c.get("seed", ""))}</small></h3>' + table(["Keyword", "Searches a month", "Difficulty", "CPC", "Intent"], rows)
    # ---------------- questions
    q_html = ""
    for q in deep.get("questions") or []:
        items = q.get("items") or []
        if items:
            q_html += f'<div class="qcol"><h3>{E(q.get("seed", ""))}</h3><ul>' + "".join(f'<li>{E(i.get("question"))} <span class="vol">{fmt(i.get("volume"))} a month</span></li>' for i in items) + "</ul></div>"
    if q_html:
        q_html = f'<div class="qgrid">{q_html}</div>'
    # ---------------- page audit
    pa_rows = []
    for p in deep.get("page_audit") or []:
        pa_rows.append([f'<code>{E(p.get("url"))}</code>', f'{E(p.get("title", ""))}<br><small>{fmt(p.get("title_len"))} chars</small>', yn(p.get("has_city_in_title")), fmt(p.get("meta_len")), E(p.get("h1", "")), fmt(p.get("h2_count")), E(", ".join(p.get("schema_types") or []) or "none"), yn(p.get("has_faq")), fmt(p.get("words"))])
    pa = table(["Page", "Title", "City in title", "Meta length", "H1", "H2s", "Schema", "FAQ", "Words"], pa_rows)
    ca_rows = [[E(c.get("domain")), f'<code>{E(c.get("url"))}</code>', E(c.get("title", "")), fmt(c.get("words")), E(", ".join(c.get("schema_types") or []) or "none"), yn(c.get("has_faq")), yn(c.get("shows_pricing")), yn(c.get("shows_reviews")), yn(c.get("form_above_fold"))] for c in (deep.get("competitor_audit") or [])]
    ca = table(["Competitor", "Page", "Title", "Words", "Schema", "FAQ", "Pricing", "Reviews", "Form above fold"], ca_rows)
    # ---------------- AI visibility
    ai_rows = [[E(a.get("query")), E(", ".join((a.get("top_domains") or [])[:10])), yn(a.get("vaf_present")), E(a.get("vaf_position", ""))] for a in (deep.get("ai_visibility") or [])]
    ai = table(["Query", "Top results", f"{E(client.split()[0])} present", "Position"], ai_rows)
    robots = deep.get("robots") or {}
    rb = ""
    if robots:
        bots = robots.get("ai_crawlers_allowed") or {}
        rb = '<div class="robots"><h3>AI crawlers in robots.txt</h3><ul>' + "".join(f'<li>{E(k)}: {yn(v)}</li>' for k, v in bots.items()) + f'<li>Sitemap declared: {yn(robots.get("sitemap_declared"))}</li></ul></div>'
    # ---------------- backlinks
    bl = basic.get("backlinks") or {}
    bl_rows = []
    if bl.get("vaf"):
        bl_rows.append([E(domain), fmt(bl["vaf"].get("authority")), fmt(bl["vaf"].get("ref_domains")), fmt(bl["vaf"].get("backlinks"))])
    for c in bl.get("competitors") or []:
        bl_rows.append([E(c.get("domain")), fmt(c.get("authority")), fmt(c.get("ref_domains")), fmt(c.get("backlinks"))])
    for d, o in ((deep.get("backlinks") or {}).get("overview") or {}).items():
        bl_rows.append([E(d), fmt(o.get("authority")), fmt(o.get("ref_domains")), fmt(o.get("backlinks"))])
    blt = table(["Domain", "Authority Score", "Referring domains", "Backlinks"], bl_rows)
    refs = (deep.get("backlinks") or {}).get("vaf_top_refdomains") or []
    reft = table(["Referring domain", "Domain score"], [[E(r.get("domain")), fmt(r.get("score"))] for r in refs])
    # ---------------- reviews / local
    rv = "".join(f'<li><b>{E(r.get("source"))}</b>: {E(r.get("what_the_result_shows"))}</li>' for r in (deep.get("reviews") or []))
    rv = f"<ul>{rv}</ul>" if rv else ""
    # ---------------- technical + implications from the basic pass
    tech = "".join(f"<li>{E(t)}</li>" for t in (basic.get("technical") or []))
    impl = "".join(f"<li>{E(t)}</li>" for t in (basic.get("implications") or []))
    # ---------------- 90-day plan and measurement
    plan = [
        ("Days 1 to 10", "Baseline locked: this report, a Semrush project on the domain, Search Console verified, Google Business Profile claimed for all offices. Every URL that earns a visitor mapped to its redirect."),
        ("Days 10 to 45", "Build: one page per money term (Indianapolis managed IT, managed print, copier lease, business phone systems), FAQ and Service schema on every solution page, LocalBusiness on every office, the blog moved to real URLs. Forms into the CRM."),
        ("Days 45 to 60", "Launch with 301s tested one by one. Sitemap resubmitted. AI crawlers allowed. Internal links from the home page to the four money pages."),
        ("Days 60 to 90", "Content: two posts a month against the question keywords above, each answering the question in the first sentence. Citations requested from partners and associations that already link to competitors."),
        ("Day 30, 60, 90", "Reads against this baseline: organic visits, non-brand share, top-100 and top-10 counts for the target terms, AI answer presence for the eight queries, leads created in the CRM. The same report, re-run."),
    ]
    plan_html = "".join(f'<div class="step"><div class="when">{E(w)}</div><p>{E(t)}</p></div>' for w, t in plan)
    measure = [
        ["Organic visits a month", "Semrush domain overview, monthly", "Up against the baseline, with non-brand share rising"],
        ["Non-brand share of visits", "Semrush organic keywords, branded filter", "From about 20% toward 40% by day 90"],
        ["Top-100 and top-10 rankings for the target terms", "Semrush position tracking on the clusters above", "Every target term in the top 100 by day 60; the low-difficulty terms in the top 10 by day 90"],
        ["AI answer presence", "The eight queries above, re-run monthly", "Named in at least half by day 90"],
        ["Leads created", "HubSpot forms and the assessment", "Every submission a contact, with source"],
        ["Page health", "The launch gate (verify.mjs), every page", "80 or better, every page, every read"],
    ]
    mt = table(["What we measure", "How", "What good looks like"], [[E(a), E(b), E(c)] for a, b, c in measure])

    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>SEO and AI search analysis of {E(domain)} | prepared for {E(client)}</title>
<style>:root{{--accent:{E(accent)};--ink:#1c1f24;--muted:#5b616b;--line:#dfe6ee;--alt:#eef4fa;--navy:#0f1e33}}*{{box-sizing:border-box}}body{{margin:0;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:#fff}}
.wrap{{max-width:1040px;margin:0 auto;padding:0 24px}}section{{padding:56px 0;border-top:1px solid var(--line)}}section:nth-of-type(even){{background:var(--alt)}}
.top{{display:flex;justify-content:space-between;align-items:center;gap:16px;border-bottom:1px solid var(--line);padding:14px 24px;flex-wrap:wrap}}.top a{{text-decoration:none;font-weight:600;color:var(--accent)}}
.eyebrow{{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:700;margin:0 0 12px}}h1{{font-size:clamp(34px,4.4vw,52px);line-height:1.05;letter-spacing:-.02em;margin:0 0 18px}}h2{{font-size:30px;line-height:1.15;letter-spacing:-.01em;margin:0 0 14px}}h3{{font-size:19px;margin:30px 0 8px}}h3 small{{font-weight:400;color:var(--muted);font-size:14px;margin-left:8px}}
.lead{{font-size:18px;color:var(--muted);max-width:760px;margin:0 0 22px}}.hero{{background:var(--navy);color:#fff;padding:64px 0}}.hero .eyebrow,.hero .lead{{color:rgba(255,255,255,.85)}}.hero h1{{color:#fff}}
.stiles{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:28px}}.stile{{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:12px;padding:18px 20px}}.stile b{{display:block;font-size:34px;line-height:1;letter-spacing:-.02em;color:#fff}}.stile span{{display:block;margin-top:8px;font-size:13.5px;color:rgba(255,255,255,.8)}}
.chips{{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 22px}}.chip,.sev{{display:inline-block;font-size:12.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#fff;background:var(--sev);border-radius:999px;padding:4px 10px}}
.findings{{display:grid;gap:14px}}.finding{{display:grid;grid-template-columns:56px 1fr;gap:16px;background:#fff;border:1px solid var(--line);border-left:5px solid var(--accent);border-radius:12px;padding:20px 22px;box-shadow:0 10px 30px rgba(0,0,0,.05)}}.finding .rank{{font-size:34px;font-weight:800;color:var(--accent);line-height:1}}.finding h3{{margin:8px 0 10px;font-size:20px}}
.finding dl{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:0}}.finding dt{{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:700}}.finding dd{{margin:4px 0 0;font-size:15px}}
.tblwrap{{overflow-x:auto;margin:14px 0 6px}}table{{width:100%;border-collapse:collapse;font-size:14.5px;background:#fff}}th,td{{text-align:left;padding:9px 11px;border-bottom:1px solid var(--line);vertical-align:top}}th{{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);background:#f6f8fa}}code{{font-size:13px;background:#f3f4f6;padding:1px 5px;border-radius:4px}}
.ok{{color:#067647;font-weight:700}}.bad{{color:#b42318;font-weight:700}}.na{{color:var(--muted)}}.vol{{color:var(--muted);font-size:13px}}
.qgrid{{display:grid;grid-template-columns:repeat(2,1fr);gap:22px}}.qcol h3{{margin-top:8px}}ul{{padding-left:18px}}li{{margin:6px 0}}
.steps{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}}.step{{background:#fff;border:1px solid var(--line);border-top:3px solid var(--accent);border-radius:12px;padding:16px 18px}}.step .when{{font-weight:700;color:var(--accent);margin-bottom:6px}}.step p{{margin:0;font-size:14.5px}}
.note{{background:#fff;border-left:4px solid var(--accent);padding:12px 18px;color:var(--muted);margin:24px 0 0}}
@media(max-width:900px){{.stiles,.steps,.qgrid,.finding dl{{grid-template-columns:1fr 1fr}}}}@media(max-width:600px){{.stiles,.steps,.qgrid,.finding dl{{grid-template-columns:1fr}}.finding{{grid-template-columns:40px 1fr}}}}</style></head>
<body><div class="top"><a href="{E(hub_href)}">&larr; Back to the three directions</a><span class="eyebrow" style="margin:0">Quantum Business Solutions for {E(client)}</span></div>
<div class="hero"><div class="wrap"><p class="eyebrow">Search and AI answers, measured {E(as_of)}</p><h1>Where {E(domain)} stands, and what it is worth to fix</h1>
<p class="lead">Every number here came from a Semrush or Firecrawl pull. Where a pull was not made, the table says so. This is the baseline the engagement is measured against at 30, 60 and 90 days.</p><div class="stiles">{tiles}</div></div></div>
{section("findings", "Top findings", "Ranked by what they cost, with the fix", top, "Each finding carries its evidence, what it costs today, and what the build or the 90-day plan does about it.")}
{section("today", "Where the traffic comes from", "Today, in numbers", "<ul>" + tech + "</ul>" if tech else "")}
{section("competitors", "Competitors", "Who earns the visits you should be earning", comp, "Indiana office-technology and managed-IT providers competing for the same terms.")}
{section("opportunities", "Keyword opportunities", "The terms worth a page each", opp, "Volume and difficulty from Semrush. Where a competitor ranks and the client does not, the gap is a missing page, not missing authority.")}
{section("clusters", "Keyword clusters by pillar", "What each pillar's page has to answer", cl_html, "Each cluster becomes one page plus its FAQ. The terms are the headings.")}
{section("questions", "Questions people ask", "The answers AI assistants and Google both want", q_html, "Each question becomes an FAQ item marked up as FAQPage, answered in the first sentence.")}
{section("audit", "Page audit", "What the pages say to a crawler today", pa + (("<h3>The same pages at the competitors</h3>" + ca) if ca else ""))}
{section("ai", "AI answer visibility", "Who is named when someone asks", ai + rb, "Live results for the questions a buyer types. Presence here is the AEO scoreboard.")}
{section("backlinks", "Backlinks", "Authority is level; pages are the gap", blt + (("<h3>Strongest referring domains</h3>" + reft) if reft else ""))}
{section("local", "Local and reviews", "What a buyer sees next to the map", rv)}
{section("plan", "The 90-day plan", "What happens, in order", f'<div class="steps">{plan_html}</div>')}
{section("measure", "What we measure", "The same report, re-run at 30, 60 and 90 days", mt)}
{section("implications", "What this means for the build", "In one list", "<ul>" + impl + "</ul>" if impl else "")}
<section><div class="wrap"><div class="note">Prepared for {E(prepared_for)}. Nothing here is a promise of rankings or traffic; those depend on the market and on what is published after launch. What is promised is that nothing about the build is the reason they do not come, and that every number above is re-measured against this page.</div></div></section>
</body></html>'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--basic", required=True)
    ap.add_argument("--deep", default=None)
    ap.add_argument("--client", required=True)
    ap.add_argument("--domain", required=True)
    ap.add_argument("--accent", default="#2A71AF")
    ap.add_argument("--as-of", default="")
    ap.add_argument("--prepared-for", default="")
    ap.add_argument("--hub", default="index.html")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    basic = json.load(open(a.basic, encoding="utf-8"))
    deep = json.load(open(a.deep, encoding="utf-8")) if a.deep else {}
    page = render(basic, deep, a.client, a.domain, a.accent, a.as_of, a.prepared_for or a.client, a.hub)
    assert "—" not in page and "–" not in page
    open(a.out, "w", encoding="utf-8").write(page)
    print(f"wrote {a.out}: {len(deep.get('findings') or [])} findings, {len(page):,} bytes")


if __name__ == "__main__":
    main()
