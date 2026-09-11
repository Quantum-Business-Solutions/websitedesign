#!/usr/bin/env python3
"""Page-level search and answer-engine audit.

Runs the same sixteen checks on (a) a live site fetched to disk and (b) the pages the
conveyor built, so a hub can show today against the build, page for page.

Usage
  # live site: a urls file plus a directory of fetched HTML named by md5(url)[:16].html
  python3 scripts/seo_audit.py live --urls urls.txt --html html/kelly --domain kellyofficesolutions.com \
      --cities "Winston-Salem,Greensboro,Charlotte,Raleigh,Swansboro,North Carolina,NC" \
      --types types.json --out brands/kelly-office-solutions.audit.json

  # the build: one direction folder of the preview output
  python3 scripts/seo_audit.py build --dir /home/user/kelly-office-solutions/showcase \
      --cities "..." --out /tmp/build.audit.json

  # fetch: download every URL in a urls file (skips files already on disk)
  python3 scripts/seo_audit.py fetch --urls urls.txt --html html/kelly

The JSON written is what preview_seo.py renders (cards, CSV, today-vs-build box).
"""
import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.request
from urllib.parse import urlparse

from lxml import html as LH

CHECKS = [
    # key, label, weight
    ("title_len", "Title length", 5),
    ("city", "City in title", 8),
    ("meta_len", "Meta length", 5),
    ("h1", "One H1", 5),
    ("h2", "Two or more H2s", 5),
    ("question", "Question headings", 8),
    ("words", "300+ words", 10),
    ("alt", "Images with alt", 4),
    ("links", "10+ internal links", 5),
    ("faq", "FAQ schema", 12),
    ("service", "Service or Article schema", 10),
    ("local", "LocalBusiness schema", 8),
    ("review", "Review schema", 4),
    ("canonical", "Canonical", 4),
    ("og", "Branded share image", 2),
    ("form", "Form or call", 5),
]
assert sum(w for _, _, w in CHECKS) == 100

FIXES = {
    "title_len": "Rewrite the title to 30 to 60 characters",
    "city": "Add the city or service area to the title",
    "meta_len": "Write a meta description of 70 to 160 characters",
    "h1": "Give the page exactly one H1",
    "h2": "Break the copy into two or more H2 sections",
    "question": "Add a heading that asks the question the page answers",
    "words": "Deepen to 300 words or more",
    "alt": "Alt text on every image",
    "links": "Link to ten or more pages on the site",
    "faq": "Add a five-question FAQ marked up as FAQPage",
    "service": "Add Service schema (or Article schema on a post)",
    "local": "Add LocalBusiness schema with the office address",
    "review": "Add Review or AggregateRating schema from real Google reviews",
    "canonical": "Set a self-referencing canonical",
    "og": "Set a branded share image (og:image)",
    "form": "Put a form or a tap-to-call number on the page",
}

QWORDS = ("what ", "why ", "how ", "when ", "where ", "who ", "which ", "should ", "can ", "do ", "does ", "is ", "are ")


def hkey(url):
    return hashlib.md5(url.encode()).hexdigest()[:16]


def fetch(urls, html_dir, delay=0.6):
    os.makedirs(html_dir, exist_ok=True)
    for u in urls:
        f = os.path.join(html_dir, hkey(u) + ".html")
        if os.path.exists(f) and os.path.getsize(f) > 0:
            continue
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"})
            with urllib.request.urlopen(req, timeout=40) as r:
                open(f, "wb").write(r.read())
            print("ok  ", u)
        except Exception as e:  # noqa: BLE001
            print("fail", u, e)
            open(f, "wb").write(b"")
        time.sleep(delay)


def _text(el):
    return re.sub(r"\s+", " ", el.text_content() if el is not None else "").strip()


def _schema_types(doc):
    types = set()
    for s in doc.xpath('//script[@type="application/ld+json"]'):
        try:
            data = json.loads(s.text or "")
        except Exception:  # noqa: BLE001
            continue
        stack = [data]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                t = x.get("@type")
                if isinstance(t, str):
                    types.add(t)
                elif isinstance(t, list):
                    types.update(str(i) for i in t)
                stack.extend(x.values())
            elif isinstance(x, list):
                stack.extend(x)
    return types


def audit_html(raw, url, domain, cities, is_build=False, site_root=None, page_type="company", is_home=False):
    """Return a dict of measured fields for one page. url is absolute for live, relative file for build."""
    try:
        doc = LH.fromstring(raw)
    except Exception:  # noqa: BLE001
        return None
    title = _text(doc.find(".//title")) if doc.find(".//title") is not None else ""
    meta = ""
    for m in doc.xpath('//meta[translate(@name,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")="description"]'):
        meta = (m.get("content") or "").strip()
        break
    h1s = [_text(h) for h in doc.xpath("//h1")]
    h2s = [_text(h) for h in doc.xpath("//h2")]
    h3s = [_text(h) for h in doc.xpath("//h3")]
    heads = h1s + h2s + h3s
    questions = sum(1 for h in heads if h.endswith("?") or h.lower().startswith(QWORDS))
    # body words without chrome
    body = doc.find("body")
    words = 0
    if body is not None:
        for bad in body.xpath(".//script|.//style|.//nav|.//header|.//footer|.//aside|.//noscript|.//template|.//*[contains(@class,'pv-switch')]|.//*[contains(@class,'q-footer')]|.//*[contains(@class,'q-header')]|.//*[contains(@class,'cookie')]"):
            bad.drop_tree()
        words = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'&-]*", body.text_content()))
    doc = LH.fromstring(raw)  # fresh tree for the rest
    imgs = doc.xpath("//img")
    # an alt attribute that is present but empty marks a decorative image, which is correct
    no_alt = sum(1 for i in imgs if i.get("alt") is None and i.get("role") != "presentation")
    hrefs = [a.get("href") or "" for a in doc.xpath("//a[@href]")]
    internal = external = tel = 0
    for h in hrefs:
        hl = h.lower()
        if hl.startswith("tel:"):
            tel += 1
            continue
        if hl.startswith(("mailto:", "#", "javascript:")):
            continue
        if hl.startswith("http"):
            host = urlparse(h).netloc.lower().replace("www.", "")
            if domain and host.endswith(domain.replace("www.", "")):
                internal += 1
            else:
                external += 1
        else:
            internal += 1
    can = ""
    for l in doc.xpath('//link[@rel="canonical"]'):
        can = (l.get("href") or "").strip()
        break
    og = ""
    for m in doc.xpath('//meta[@property="og:image"]'):
        og = (m.get("content") or "").strip()
        break
    robots = " ".join((m.get("content") or "").lower() for m in doc.xpath('//meta[@name="robots"]'))
    types = _schema_types(doc)
    entity = entity_audit(_schema_nodes(doc), page_type, is_home)
    has_form = bool(doc.xpath("//form")) or bool(doc.xpath("//*[contains(@class,'hs-form') or contains(@class,'wpcf7') or contains(@class,'gform') or contains(@class,'pv-form')]"))
    has_video = bool(doc.xpath("//video|//iframe[contains(@src,'youtube') or contains(@src,'vimeo') or contains(@src,'wistia')]"))
    lang = (doc.get("lang") or "").strip()

    def city_in(t):
        tl = t.lower()
        return any(re.search(r"(?<![a-z])" + re.escape(c.lower()) + r"(?![a-z])", tl) for c in cities)

    if is_build:
        canonical_self = bool(can)
    else:
        u = url.rstrip("/").lower()
        canonical_self = bool(can) and can.rstrip("/").lower().replace("http://", "https://") in (u, u.replace("://www.", "://"), u.replace("://", "://www."))
    stock_og = bool(og) and bool(re.search(r"(stock|shutterstock|istock|unsplash|pexels|placeholder|default|wp-content/themes)", og.lower()))
    faq = "FAQPage" in types
    # a FAQ the visitor can see (an accordion or a list of questions) that carries no FAQPage schema: the crawler never learns it is there
    raw_text = raw.decode("utf-8", "ignore") if isinstance(raw, bytes) else raw
    faq_visible = (not faq) and len(re.findall(r">\s*([^<>]{12,160}\?)\s*<", raw_text)) >= 3
    service = bool(types & {"Service", "ITService", "ProfessionalService", "Offer", "OfferCatalog"})
    article = bool(types & {"Article", "BlogPosting", "NewsArticle", "TechArticle"})
    local = bool(types & {"LocalBusiness", "ProfessionalService", "Store", "Dentist", "HomeAndConstructionBusiness"})
    review = bool(types & {"Review", "AggregateRating", "Rating"})
    breadcrumb = "BreadcrumbList" in types
    checks = {
        "title_len": 30 <= len(title) <= 60,
        "city": city_in(title),
        "meta_len": 70 <= len(meta) <= 160,
        "h1": len(h1s) == 1,
        "h2": len(h2s) >= 2,
        "question": questions >= 1,
        "words": words >= 300,
        "alt": no_alt == 0,
        "links": internal >= 10,
        "faq": faq,
        "service": service or article,
        "local": local,
        "review": review,
        "canonical": canonical_self,
        "og": bool(og) and not stock_og,
        "form": has_form or tel > 0,
    }
    score = sum(w for k, _, w in CHECKS if checks[k])
    grade = "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "D" if score >= 40 else "F"
    values = {
        "title_len": f"{len(title)} chars", "city": "yes" if checks["city"] else "no", "meta_len": f"{len(meta)} chars" if meta else "none",
        "h1": str(len(h1s)), "h2": str(len(h2s)), "question": str(questions), "words": f"{words:,}", "alt": f"{no_alt} missing",
        "links": str(internal), "faq": "yes" if faq else ("shown, no schema" if faq_visible else "no"), "service": ("Article" if article else "yes") if checks["service"] else "no",
        "local": "yes" if local else "no", "review": "yes" if review else "no", "canonical": "yes" if canonical_self else ("other" if can else "no"),
        "og": ("stock" if stock_og else "yes") if og else "no", "form": "yes" if checks["form"] else "no",
    }
    failed = [k for k, _, _ in CHECKS if not checks[k]]
    return {
        "url": url, "title": title, "title_len": len(title), "meta": meta, "meta_len": len(meta), "h1": h1s[0] if h1s else "", "h1_count": len(h1s),
        "h2_count": len(h2s), "h3_count": len(h3s), "question_headings": questions, "words": words, "images": len(imgs), "images_no_alt": no_alt,
        "internal_links": internal, "external_links": external, "canonical": can, "canonical_self": canonical_self, "og_image": og, "stock_og": stock_og,
        "faq": faq, "faq_visible": faq_visible, "service": service, "local": local, "review": review, "article": article, "breadcrumb": breadcrumb,
        "schema": sorted(types), "entity": entity, "noindex": "noindex" in robots, "has_form": has_form, "has_video": has_video, "tel_link": tel > 0, "lang": lang,
        "checks": checks, "values": values, "score": score, "grade": grade, "failed": failed,
        "recommendations": [FIXES[k] for k in failed], "issues": len(failed),
    }


# ── The entity graph ──────────────────────────────────────────────────────────
# The sixteen checks above read type names. These read the graph: which entities the page
# names, whether they are connected to each other, and whether the connections resolve.
# That is what makes a statement attributable to a known entity, which is what an answer
# engine needs before it will name a company. Scored separately, out of 100, so a page can
# be strong on copy and weak on structure and the report says which.

ENTITY_CHECKS = [
    # key, label, weight. Weighted so that a plugin's sitewide defaults cannot carry a page:
    # the checks that say something specific about THIS page are worth the most.
    # what the page names
    ("org", "Organization identified", 6),
    ("page_type", "Page type declared", 3),
    ("primary", "Primary entity for this kind of page", 14),
    ("website", "WebSite on the home page", 2),
    ("breadcrumb", "BreadcrumbList", 3),
    ("person", "A named Person, not a byline string", 6),
    # how they connect
    ("sameas", "sameAs to authoritative profiles", 6),
    ("provider", "Primary entity linked to the Organization", 10),
    ("area", "areaServed or a postal address", 8),
    ("author", "author linked to a Person", 8),
    ("contact", "contactPoint or telephone", 4),
    ("about", "about, mentions or serviceType naming the topic", 8),
    ("dates", "datePublished and dateModified", 8),
    # whether it holds together
    ("ids", "@id on the main entities", 4),
    ("resolve", "Every @id reference resolves", 5),
    ("clean", "No empty or placeholder values", 5),
]
assert sum(w for _, _, w in ENTITY_CHECKS) == 100

ENTITY_FIXES = {
    "org": "Add Organization schema naming the company",
    "page_type": "Declare the page type (WebPage, Article, CollectionPage)",
    "primary": "Add the entity this page is about (Service, LocalBusiness, Article or Product)",
    "website": "Add WebSite schema on the home page",
    "breadcrumb": "Add BreadcrumbList so the hierarchy is machine-readable",
    "person": "Name the expert or author as a Person, with a URL that identifies them",
    "sameas": "Add sameAs to the company's LinkedIn, Google Business Profile and other authoritative profiles",
    "provider": "Link this page's entity to the Organization (provider, publisher or parentOrganization)",
    "area": "Add areaServed or a postal address to the entity",
    "author": "Point author at a Person object, not a plain string",
    "contact": "Add contactPoint or a telephone to the Organization",
    "about": "Name what the page is about with about, mentions or serviceType",
    "dates": "Add datePublished and dateModified",
    "ids": "Give the main entities a stable @id so they can be referenced",
    "resolve": "Point every @id reference at an entity that exists",
    "clean": "Remove empty and placeholder values from the markup",
}

ORG_T = {"Organization", "Corporation", "LocalBusiness", "ProfessionalService", "Store", "OfficeEquipmentStore",
         "HomeAndConstructionBusiness", "MedicalBusiness", "FinancialService", "AutomotiveBusiness", "NGO", "EducationalOrganization"}
LOCAL_T = {"LocalBusiness", "ProfessionalService", "Store", "OfficeEquipmentStore", "HomeAndConstructionBusiness",
           "MedicalBusiness", "FinancialService", "AutomotiveBusiness", "Dentist", "Place"}
ARTICLE_T = {"Article", "BlogPosting", "NewsArticle", "TechArticle", "Report", "ScholarlyArticle"}
SERVICE_T = {"Service", "ITService", "FinancialProduct", "Offer", "OfferCatalog", "Product", "SoftwareApplication", "Course"}
PAGE_T = {"WebPage", "CollectionPage", "AboutPage", "ContactPage", "ProfilePage", "FAQPage", "QAPage", "ItemPage", "SearchResultsPage", "CheckoutPage"}
PLACEHOLDER = re.compile(r"(?i)\b(lorem ipsum|tbd|your company|company name here|example\.com|placeholder|coming soon)\b")
# what the page's primary entity should be, by the type the conveyor assigns
PRIMARY_FOR = {
    "service": SERVICE_T, "industry": SERVICE_T, "product": SERVICE_T, "form": SERVICE_T,
    "city": LOCAL_T, "post": ARTICLE_T, "company": ORG_T,
}


def _schema_nodes(doc):
    """Every JSON-LD object that declares a @type, nesting and @graph included, as dicts."""
    nodes = []
    for s in doc.xpath('//script[@type="application/ld+json"]'):
        try:
            data = json.loads(s.text or "")
        except Exception:  # noqa: BLE001
            continue
        stack = [data]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                if x.get("@type"):
                    nodes.append(x)
                stack.extend(x.values())
            elif isinstance(x, list):
                stack.extend(x)
    return nodes


def _tset(node):
    t = (node or {}).get("@type")
    return {t} if isinstance(t, str) else {str(i) for i in t} if isinstance(t, list) else set()


def _first(nodes, wanted):
    for n in nodes:
        if _tset(n) & wanted:
            return n
    return None


def _has(node, *props):
    """True when the node carries one of these properties with something in it."""
    if not node:
        return False
    for pr in props:
        v = node.get(pr)
        if v in (None, "", [], {}):
            continue
        if isinstance(v, str) and not v.strip():
            continue
        return True
    return False


def _links_person(node, prop="author"):
    """A property pointing at a Person or Organization object or reference, not a bare string."""
    if not node:
        return False
    v = node.get(prop)
    for x in (v if isinstance(v, list) else [v]):
        if isinstance(x, dict) and (_tset(x) & {"Person", "Organization"} or x.get("@id")):
            return True
    return False


def entity_audit(nodes, page_type, is_home=False):
    """Score the graph on one page out of 100: the entities it names, how they connect, whether
    the connections resolve. Checks that cannot apply to this kind of page are left out of the
    total rather than failed, so a booking form is not marked down for having no author.
    Returns the same shape as the sixteen readiness checks."""
    ids = {str(n.get("@id")) for n in nodes if n.get("@id")}
    refs = []
    for n in nodes:
        for v in n.values():
            for x in (v if isinstance(v, list) else [v]):
                if isinstance(x, dict) and set(x.keys()) <= {"@id", "@type"} and x.get("@id"):
                    refs.append(str(x["@id"]))
    # only a bare fragment can be judged from one page; a full URL may live on another page
    dangling = sorted({r for r in refs if r.startswith("#") and r not in ids})

    org = _first(nodes, ORG_T)
    person = _first(nodes, {"Person"})
    article = _first(nodes, ARTICLE_T)
    primary = _first(nodes, PRIMARY_FOR.get(page_type, ORG_T))
    page_node = _first(nodes, PAGE_T)
    breadcrumb = _first(nodes, {"BreadcrumbList"})
    website = _first(nodes, {"WebSite"})

    blank = 0
    for n in nodes:
        for k, v in n.items():
            if k.startswith("@"):
                continue
            if v in ("", [], {}) or (isinstance(v, str) and PLACEHOLDER.search(v)):
                blank += 1

    # the primary entity is connected to the company when it says so, or when it IS the company
    linked = _has(primary, "provider", "publisher", "parentOrganization", "brand", "seller", "worksFor", "author")
    if primary is not None and org is not None and primary is org:
        linked = True

    checks = {
        "org": bool(org),
        "page_type": bool(page_node) or bool(article),
        "primary": bool(primary),
        "website": bool(website),
        "breadcrumb": bool(breadcrumb),
        "person": bool(person) and _has(person, "name"),
        "sameas": _has(org, "sameAs"),
        "provider": bool(primary) and linked,
        "area": _has(primary, "areaServed", "address", "location", "serviceArea") or _has(org, "address", "areaServed"),
        "author": _links_person(article) if article else _has(person, "worksFor", "jobTitle", "url"),
        "contact": _has(org, "contactPoint", "telephone", "email"),
        "about": _has(primary, "about", "mentions", "keywords", "articleSection", "serviceType", "audience", "hasOfferCatalog")
                 or _has(page_node, "about", "mentions", "keywords", "significantLink"),
        "dates": (_has(article, "datePublished") and _has(article, "dateModified")) if article
                 else (_has(primary, "dateModified", "datePublished") or _has(page_node, "dateModified", "datePublished")),
        "ids": bool(ids),
        "resolve": not dangling,
        "clean": blank == 0,
    }

    # what this kind of page cannot be expected to carry
    na = set()
    if not is_home:
        na.add("website")
    else:
        na.add("breadcrumb")
    if page_type != "post":
        na.add("author")
    if page_type not in ("post", "company"):
        na.add("person")
    if page_type == "form":
        na |= {"about", "dates", "breadcrumb"}
    if page_type == "post":
        na.add("area")

    applied = [(k, w) for k, _, w in ENTITY_CHECKS if k not in na]
    total = sum(w for _, w in applied) or 1
    score = round(sum(w for k, w in applied if checks[k]) / total * 100)
    grade = "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "D" if score >= 40 else "F"
    failed = [k for k, _ in applied if not checks[k]]
    sameas_n = org.get("sameAs") if org else None
    values = {
        "org": (sorted(_tset(org))[0] if org else "no"),
        "page_type": (sorted(_tset(page_node))[0] if page_node else ("article" if article else "no")),
        "primary": (sorted(_tset(primary))[0] if primary else "no"),
        "website": "yes" if website else "no",
        "breadcrumb": "yes" if breadcrumb else "no",
        "person": (str(person.get("name"))[:40] if checks["person"] else "no"),
        "sameas": (f"{len(sameas_n) if isinstance(sameas_n, list) else 1} profiles" if checks["sameas"] else "no"),
        "provider": "yes" if checks["provider"] else "no",
        "area": "yes" if checks["area"] else "no",
        "author": "yes" if checks["author"] else "no",
        "contact": "yes" if checks["contact"] else "no",
        "about": "yes" if checks["about"] else "no",
        "dates": "yes" if checks["dates"] else "no",
        "ids": (str(len(ids)) if ids else "none"),
        "resolve": "yes" if checks["resolve"] else f"{len(dangling)} dangling",
        "clean": "yes" if blank == 0 else f"{blank} empty",
    }
    return {
        "score": score, "grade": grade, "checks": checks, "values": values, "failed": failed, "na": sorted(na),
        "recommendations": [ENTITY_FIXES[k] for k in failed], "nodes": len(nodes), "ids": len(ids), "dangling": len(dangling),
        "types": sorted({t for n in nodes for t in _tset(n)}),
    }


def site_checks(domain, urls):
    """Technical facts measured live, not authored: scheme and host redirects, robots policy for AI crawlers, llms.txt, sitemap size."""
    import urllib.error
    out = {"domain": domain, "sitemap_urls": len(urls)}

    def head(url):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; QBS-audit)"}, method="GET")
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status, r.geturl(), r.read(200000).decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            return e.code, url, ""
        except Exception:  # noqa: BLE001
            return None, url, ""
    bare = domain.replace("www.", "")
    st, final, _ = head(f"http://{bare}/")
    out["http_redirects_to_https"] = bool(final and final.startswith("https://"))
    st1, f1, _ = head(f"https://{bare}/")
    st2, f2, _ = head(f"https://www.{bare}/")
    hosts = {urlparse(f).netloc for f in (f1, f2) if f}
    out["one_canonical_host"] = len(hosts) == 1
    out["canonical_host"] = sorted(hosts)[0] if hosts else ""
    st, _, robots = head(f"{f1 or 'https://' + bare}robots.txt" if (f1 or "").endswith("/") else f"https://{bare}/robots.txt")
    out["robots_status"] = st
    blocks = {}
    agent = None
    for line in robots.splitlines():
        line = line.split("#")[0].strip()
        if not line:
            continue
        k, _, v = line.partition(":")
        k, v = k.strip().lower(), v.strip()
        if k == "user-agent":
            agent = v.lower()
        elif k == "disallow" and agent is not None:
            blocks.setdefault(agent, []).append(v)
        elif k == "crawl-delay":
            out["crawl_delay"] = v
    for bot in ("gptbot", "claudebot", "perplexitybot", "google-extended", "bingbot", "googlebot"):
        rules = blocks.get(bot, blocks.get("*", []))
        out[f"allows_{bot}"] = "/" not in rules
    out["sitemap_declared"] = "sitemap:" in robots.lower()
    st, _, _ = head(f"https://{out['canonical_host'] or bare}/llms.txt")
    out["llms_txt"] = st == 200
    return out


def classify(path, rules):
    """rules: list of [regex, type]; first match wins. Default 'company'."""
    for rx, t in rules:
        if re.search(rx, path):
            return t
    return "company"


def live(a):
    urls = [u.strip() for u in open(a.urls, encoding="utf-8") if u.strip()]
    cities = [c.strip() for c in a.cities.split(",") if c.strip()]
    rules = json.load(open(a.types, encoding="utf-8")) if a.types else []
    skip = re.compile(a.skip) if a.skip else None
    pages = []
    for u in urls:
        path = urlparse(u).path or "/"
        if skip and skip.search(u):
            continue
        f = os.path.join(a.html, hkey(u) + ".html")
        if not os.path.exists(f) or os.path.getsize(f) == 0:
            print("missing", u, file=sys.stderr)
            continue
        raw = open(f, "rb").read()
        ptype = classify(path, rules)
        r = audit_html(raw, u, a.domain, cities, page_type=ptype, is_home=(path in ("/", "")))
        if not r:
            continue
        r["path"] = path
        r["type"] = ptype
        pages.append(r)
    out = {"domain": a.domain, "measured": a.date, "count": len(pages), "pages": pages, "summary": summarize(pages)}
    if not a.no_site:
        out["site"] = site_checks(a.domain, urls)
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out["summary"], indent=1))


def build(a):
    cities = [c.strip() for c in a.cities.split(",") if c.strip()]
    rules = json.load(open(a.types, encoding="utf-8")) if a.types else []
    pages = []
    for root, _, files in os.walk(a.dir):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(root, fn), a.dir).replace(os.sep, "/")
            raw = open(os.path.join(root, fn), "rb").read()
            ptype = classify("/" + rel, rules)
            r = audit_html(raw, rel, "", cities, is_build=True, page_type=ptype, is_home=(rel == "index.html"))
            if not r:
                continue
            r["path"] = "/" + rel
            r["type"] = ptype
            pages.append(r)
    pages.sort(key=lambda p: p["path"])
    out = {"dir": a.dir, "count": len(pages), "pages": pages, "summary": summarize(pages)}
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out["summary"], indent=1))


def summarize(pages):
    n = len(pages) or 1
    s = {
        "count": len(pages),
        "avg_score": round(sum(p["score"] for p in pages) / n),
        "grade_a": sum(1 for p in pages if p["grade"] == "A"),
        "grade_b_plus": sum(1 for p in pages if p["grade"] in "AB"),
        "grade_d_f": sum(1 for p in pages if p["grade"] in "DF"),
        "faq": sum(1 for p in pages if p["faq"]),
        "service_or_article": sum(1 for p in pages if p["service"] or p["article"]),
        "local": sum(1 for p in pages if p["local"]),
        "review": sum(1 for p in pages if p["review"]),
        "question": sum(1 for p in pages if p["question_headings"] > 0),
        "under_300": sum(1 for p in pages if p["words"] < 300),
        "city_title": sum(1 for p in pages if p["checks"]["city"]),
        "breadcrumb": sum(1 for p in pages if p["breadcrumb"]),
        "no_alt_pages": sum(1 for p in pages if p["images_no_alt"] > 0),
        "avg_words": round(sum(p["words"] for p in pages) / n),
        "entity_avg": round(sum(p["entity"]["score"] for p in pages) / n),
        "entity_a": sum(1 for p in pages if p["entity"]["grade"] == "A"),
        "entity_d_f": sum(1 for p in pages if p["entity"]["grade"] in "DF"),
    }
    # how many pages pass each entity check, so a finding can name the one that is missing everywhere
    s["entity_checks"] = {k: {"pass": sum(1 for p in pages if k not in p["entity"]["na"] and p["entity"]["checks"][k]),
                              "of": sum(1 for p in pages if k not in p["entity"]["na"])} for k, _, _ in ENTITY_CHECKS}
    s["schema_types"] = dict(sorted(
        ((t, sum(1 for p in pages if t in p["schema"])) for t in {t for p in pages for t in p["schema"]}),
        key=lambda kv: -kv[1]))
    by_type = {}
    for p in pages:
        t = by_type.setdefault(p["type"], {"count": 0, "score": 0, "ent": 0})
        t["count"] += 1
        t["score"] += p["score"]
        t["ent"] += p["entity"]["score"]
    s["by_type"] = {k: {"count": v["count"], "avg": round(v["score"] / v["count"]), "entity": round(v["ent"] / v["count"])} for k, v in by_type.items()}
    return s


def to_csv(audit, path):
    cols = ["url", "type", "title", "title_len", "city", "meta", "meta_len", "h1", "h1_count", "h2_count", "h3_count", "question_headings", "words", "images", "images_no_alt",
            "internal_links", "external_links", "canonical", "canonical_self", "og_image", "stock_og", "faq", "faq_visible", "entity_score", "entity_grade", "entity_missing", "schema_nodes", "service", "local", "review", "article", "breadcrumb", "schema",
            "noindex", "has_form", "has_video", "tel_link", "score", "grade", "recommendations", "issues"]
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(cols)
    for p in audit["pages"]:
        row = []
        for c in cols:
            if c == "city":
                row.append(p["checks"]["city"])
            elif c == "schema":
                row.append(", ".join(p["schema"]))
            elif c == "recommendations":
                row.append(" | ".join(p["recommendations"] + p["entity"]["recommendations"]))
            elif c == "entity_score":
                row.append(p["entity"]["score"])
            elif c == "entity_grade":
                row.append(p["entity"]["grade"])
            elif c == "entity_missing":
                row.append(", ".join(p["entity"]["failed"]))
            elif c == "schema_nodes":
                row.append(p["entity"]["nodes"])
            else:
                row.append(p.get(c, ""))
        w.writerow(row)
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch"); f.add_argument("--urls", required=True); f.add_argument("--html", required=True); f.add_argument("--delay", type=float, default=0.6)
    l = sub.add_parser("live"); l.add_argument("--urls", required=True); l.add_argument("--html", required=True); l.add_argument("--domain", required=True)
    l.add_argument("--cities", default=""); l.add_argument("--types"); l.add_argument("--skip", help="regex of URLs to leave out (feeds, attachments)")
    l.add_argument("--date", default=time.strftime("%-d %B %Y")); l.add_argument("--out", required=True); l.add_argument("--no-site", action="store_true", help="skip the live technical checks")
    b = sub.add_parser("build"); b.add_argument("--dir", required=True); b.add_argument("--cities", default=""); b.add_argument("--types"); b.add_argument("--out", required=True)
    c = sub.add_parser("csv"); c.add_argument("--audit", required=True); c.add_argument("--out", required=True)
    a = p.parse_args(argv)
    if a.cmd == "fetch":
        fetch([u.strip() for u in open(a.urls, encoding="utf-8") if u.strip()], a.html, a.delay)
    elif a.cmd == "live":
        live(a)
    elif a.cmd == "build":
        build(a)
    elif a.cmd == "csv":
        to_csv(json.load(open(a.audit, encoding="utf-8")), a.out)


if __name__ == "__main__":
    main()
