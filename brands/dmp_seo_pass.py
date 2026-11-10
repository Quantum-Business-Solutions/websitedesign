"""SEO pass for the DMP content. finalize() in digital-monitoring-products.content.py calls apply(data, ctx) last.
DMP is a national manufacturer: nothing here adds a city. Everything is deterministic and uses only facts already in the content.

ctx keys: SITE, URL_MAP (old full URL -> new file), NEWS_MAP (old full URL -> new file), SYSTEM_BY_SEGMENT, PRODUCTS (slug -> dict), INDUSTRIES (rows)."""
import json, os, re
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
TODAY = "2026-11-09"

STOP_END = {"and", "or", "with", "of", "the", "a", "an", "to", "for", "in", "on", "by", "at", "from", "as", "that", "which", "than", "into", "its", "our", "your", "their", "is", "are", "so", "but", "plus", "such", "2", "ii", "type"}


# ---------------------------------------------------------------- descriptions
def smart_cut(text, n=155):
    """Shorten to n characters at a sentence end, else a clause end, never mid-phrase."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= n:
        return text
    cut = text[: n + 1]
    i = max(cut.rfind(". "), cut.rfind("? "), cut.rfind("! "))
    if i >= 60:
        return cut[: i + 1]
    j = max(cut.rfind("; "), cut.rfind(", "), cut.rfind(": "), cut.rfind(" - "))
    if j >= 70:
        out = cut[:j]
    else:
        out = cut[: cut.rfind(" ")]
    words = out.rstrip(",;: ").split(" ")
    while len(words) > 4 and (words[-1].lower().strip(",;:") in STOP_END or re.fullmatch(r"[\d.,]+", words[-1])):
        words.pop()
    return " ".join(words).rstrip(",;: ") + "."


# ---------------------------------------------------------------- redirects
GONE = [r"^/intranet", r"^/official-holiday-dates", r"^/new-hire-information", r"open-enrollment", r"^/ukg-ready", r"^/leadership-training-topics",
        r"^/summer-of-fun", r"^/pdt-summit-survey", r"^/contract-project-application", r"^/camera-database-test", r"^/marketing-central-request"]

# marketing landing pages and campaign pages: the nearest real equivalent
LANDING = {
    "/xv-24-with-alarmvision-webinar": "products/xv-gateways-with-alarmvision.html", "/v-6000-series-cameras-webinar": "services/video.html",
    "/xv-gateways-with-alarmvision-how-to-provide-video-to-panel-events": "products/xv-gateways-with-alarmvision.html",
    "/xv-gateways-with-alarmvision-bring-advanced-analytics-to-existing-cameras": "products/xv-gateways-with-alarmvision.html",
    "/trueorfalse": "products/xv-gateways-with-alarmvision.html", "/end-false-alarms": "products/xv-gateways-with-alarmvision.html",
    "/end-false-alarms2": "products/xv-gateways-with-alarmvision.html", "/end-false-alarms-ssn": "products/xv-gateways-with-alarmvision.html",
    "/alarmvision-case-study": "products/xv-gateways-with-alarmvision.html", "/access-control-solutions": "services/access-control.html",
    "/7inch-eyes": "products/7-inch-touchscreen-keypad.html", "/the-perfect-panel-is-here": "services/intrusion.html",
    "/dualsim-communicators": "products/dualcom.html", "/two-carriers-zero-downtime": "products/dualcom.html", "/dualsim-keeps-you-up-and-running": "products/dualcom.html",
    "/jamalert-lineup": "products/jamalert.html", "/jamalert-for-your-business": "products/jamalert.html", "/jamalert-for-your-home": "products/jamalert.html",
    "/introducing-the-vue-video-doorbell": "products/vue-video-doorbell.html", "/millions-of-cameras-are-about-to-get-smarter": "services/video.html",
    "/kit-cfa-xt75mv-quick-start-guide": "products/xt75.html", "/contact-our-international-team": "international.html", "/international-products": "international.html",
    "/harmonized-tariff-schedule-hts-system": "international.html", "/a-e-support": "support/ae-support.html", "/design-tools": "support/design-tools.html",
    "/dealer-agreement-form": "support/become-a-dealer.html", "/product-order-forms": "support/dealer-services.html", "/marketing-central": "support/marketing.html",
    "/sales-training": "training/sales-training.html", "/gsx-2026": "events.html", "/thanks-for-visiting-us-at-gsx": "events.html",
    "/thanks-for-joining-us-at-dealer-roundtable": "events.html", "/dmp-cares-4u": "about/dmp-cares.html", "/help-center": "support.html",
    "/dominate-the-market": "for-dealers.html", "/all-in-on-dmp": "why-dmp.html", "/phenomenal": "why-dmp.html",
    "/virtual-tour": "about.html", "/virtual-tour-vyanet": "about.html", "/virtual-tour-vyanet-2": "about.html", "/virtual-tour-vyanet-3": "about.html",
    "/license-entr%C3%A9": "products/entre-enterprise.html", "/single-sign-on": "products/dealer-admin.html",
    "/events": "events.html", "/about-us": "about.html", "/about-us/careers": "about/careers.html", "/products/global-products": "international.html",
    "/products": "services.html", "/support/wait-time": "support.html", "/support/dealer-services/accounting": "support/dealer-services.html",
    "/support/dealer-services/product-firmware": "support/dealer-services.html", "/support/dealer-services/dealerdigest": "support/dealer-services.html",
    "/support/become-a-dealer/apply-now": "support/become-a-dealer.html", "/training/tech-training/control-panels-hardware": "training/technical-training.html",
    "/training/tech-training/software": "training/technical-training.html", "/partners/evolon": "partners/evolon.html", "/partners/sureview": "partners.html",
    "/products/marketing-central": "support/marketing.html", "/products/international-intrusion": "international.html",
}


def redirect_table(ctx, audit_paths, pages):
    """old path -> [new file, kind]. Only paths with a real equivalent; the rest fall through to the token matcher in preview_seo."""
    SITE, URL_MAP, NEWS_MAP, PRODUCTS = ctx["SITE"], ctx["URL_MAP"], ctx["NEWS_MAP"], ctx["PRODUCTS"]
    SEG = {unquote(k).lower(): v for k, v in ctx["SYSTEM_BY_SEGMENT"].items()}
    files = {p["file"] for p in pages}
    by_last = {}
    for slug, pr in PRODUCTS.items():
        by_last[unquote(pr["dmp_path"].rstrip("/").split("/")[-1]).lower()] = f"products/{slug}.html"
        by_last[slug.lower()] = f"products/{slug}.html"
    ind = {i[0] for i in ctx["INDUSTRIES"]}
    news_last = {u.rstrip("/").split("/")[-1]: f for u, f in NEWS_MAP.items()}
    out = {}
    for path in audit_paths:
        q = unquote(path).lower()
        if any(re.search(rx, q) for rx in GONE):
            out[path] = ["", "gone"]
            continue
        if path in LANDING and LANDING[path] in files:
            out[path] = [LANDING[path], "rebuilt"]
            continue
        parts = [x for x in q.strip("/").split("/") if x]
        if not parts:
            out[path] = ["index.html", "rebuilt"]
            continue
        if SITE + path in URL_MAP or SITE + path.rstrip("/") in URL_MAP:
            out[path] = [URL_MAP.get(SITE + path) or URL_MAP[SITE + path.rstrip("/")], "rebuilt"]
            continue
        if parts[0] == "products" and len(parts) == 3 and parts[1] == "industries":
            pass
        if parts[:2] == ["products", "industries"] and len(parts) == 3 and parts[2] in ind:
            out[path] = [f"industries/{parts[2]}.html", "rebuilt"]
            continue
        if parts[0] == "products" and len(parts) >= 3:
            last = re.sub(r"int$", "", parts[-1]) if parts[-1] not in by_last else parts[-1]
            if parts[-1] in by_last:
                out[path] = [by_last[parts[-1]], "rebuilt"]
                continue
            if last in by_last:
                out[path] = [by_last[last], "rebuilt"]   # the international variant of a product keeps its product page
                continue
            seg = re.sub(r"^int-|-int$", "", parts[1])
            sysf = f"services/{SEG[seg]}.html" if seg in SEG else None
            if sysf:
                out[path] = [sysf, "merged"]
                continue
        if parts[0] == "products" and len(parts) == 2:
            seg = re.sub(r"^int-|-int$", "", parts[1])
            if seg in SEG:
                out[path] = [f"services/{SEG[seg]}.html", "rebuilt"]
                continue
        if parts[-1] in news_last and ("news" in q or "resources" in q):
            out[path] = [news_last[parts[-1]], "rebuilt"]
            continue
    return out


# ---------------------------------------------------------------- schema URLs
def map_url(u, ctx):
    """An old www.dmp.com URL -> the new absolute URL (no .html), or None."""
    SITE = ctx["SITE"]
    if not isinstance(u, str) or not u.startswith(SITE):
        return None
    if u in ctx["URL_MAP"]:
        return f"{SITE}/{ctx['URL_MAP'][u][:-5]}"
    if u in ctx["NEWS_MAP"]:
        return f"{SITE}/{ctx['NEWS_MAP'][u][:-5]}"
    path = u[len(SITE):]
    parts = [x for x in path.strip("/").split("/") if x]
    if ctx.get("FILES") and ("/".join(parts) + ".html") in ctx["FILES"]:
        return u   # already a new-site URL
    if parts and parts[0] == "products":
        seg = re.sub(r"^int-", "", parts[1]) if len(parts) > 1 else ""
        if seg in ctx["SYSTEM_BY_SEGMENT"]:
            return f"{SITE}/services/{ctx['SYSTEM_BY_SEGMENT'][seg]}"
        return f"{SITE}/services"
    return None


def abs_file_url(u, ctx):
    """'blog/x.html' or 'index.html' -> the absolute URL on the live domain."""
    SITE = ctx["SITE"]
    if isinstance(u, str) and u.endswith(".html") and not u.startswith("http"):
        return f"{SITE}/" if u == "index.html" else f"{SITE}/{u[:-5]}"
    return None


def fix_schema_urls(node, ctx):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k in ("url", "item") and isinstance(v, str):
                out[k] = map_url(v, ctx) or abs_file_url(v, ctx) or v
            else:
                out[k] = fix_schema_urls(v, ctx)
        return out
    if isinstance(node, list):
        return [fix_schema_urls(v, ctx) for v in node]
    return node



# ---------------------------------------------------------------- FAQ boilerplate
BOILER_Q = {"Does DMP sell directly to building owners?", "Where is DMP based?", "What does DMP make?", "How do I reach a person?", "How do dealers place an order?", "Where do I find datasheets and installation guides?", "Is there an international range?"}
BOILER_KEEP = {"index.html", "faq.html", "for-building-owners.html", "contact.html", "locations.html"}   # locations: "Where is DMP based?" is the page topic


FAQ_ADD = {   # page-specific answers, from facts already on the page, for pages the boilerplate removal would leave bare
    "industries.html": [["Which industries does DMP have pages for?", "Eleven kinds of building: commercial, financial institutions, retail, government, industrial and manufacturing, education, healthcare and wellness, multi-tenant, religious institutions, storage units and residential."],
                        ["Does DMP have a contact for a specific market?", "For some. The financial institutions, retail and government pages each name a dedicated DMP executive. Inside Sales, 877-757-4367, can route a question for any market, and the DMP directory shows your regional sales manager."]],
    "support/get-a-quote.html": [["What does the DMP quote form ask for?", "Your company and contact details, ZIP code and country, whether you already work with an authorized DMP dealer, and the product type you are interested in: Intrusion, Access, Fire, Video, Communicators or JamAlert."],
                                 ["Who helps with a quote?", "A nationwide network of authorized DMP dealers and a team of DMP security professionals, who guide product selection, complete solution design and planning for future growth."]],
    "industries/commercial.html": [["Who are DMP commercial keypads designed for?", "Employees and service providers: the keypads are easy to operate regardless of experience level."]],
    "industries/financial-institutions.html": [["What does DMP do for credentialing at a branch?", "Our systems streamline credentialing through integrated access control and intrusion, reduce labor through automated reporting and simplified credential administration, and simplify compliance audits."]],
    "industries/retail.html": [["Do retail systems share one set of credentials?", "Yes. Our retail systems integrate access control and intrusion so one database manages user credentials, with automated enterprise reporting."]],
    "industries/government.html": [["Does DMP have a team for government customers?", "Yes. We have a division dedicated to government customers and a national network for installation and service."]],
    "industries/industrial-manufacturing.html": [["Which systems can one industrial site combine?", "Intrusion, access control, commercial fire and video, with the full benefit of multiple security features working together."]],
    "industries/education.html": [["What does DMP offer schools?", "A broad line of security hardware and software that can be configured into a customized solution, with features tailored to protecting school facilities."]],
    "industries/healthcare-wellness.html": [["What must a healthcare provider secure besides the building?", "Patients' protected health information, as the HIPAA Privacy Rule requires, in addition to protecting property from intrusion."]],
    "industries/multi-tenant.html": [["Can residents control locks and lights remotely?", "Yes. With the Virtual Keypad app, customers can control their systems remotely, along with locks, lights, thermostats and more."]],
    "industries/religious-institutions.html": [["Which products suit a house of worship?", "The hardware shown on the page is an XT75 control panel, XV gateways with AlarmVision, a VUE Plus 6MP fisheye camera, a 5-inch touchscreen keypad, Virtual Keypad and a 1128 glassbreak detector."]],
    "industries/storage-units.html": [["How do storage facilities get security that fits?", "Storage facilities have unique security needs, and our hardware and software are designed for flexible, scalable solutions that can be configured for any application."]],
    "industries/residential.html": [["How does a homeowner control a DMP system remotely?", "With the Virtual Keypad app, customers can control the system remotely, along with locks, lights, thermostats and more."]],
    "support/become-a-dealer.html": [["How much equipment does a DMP dealer buy?", "DMP generally looks for dealers purchasing at least $5,000 to $10,000 in equipment per month."],
                                     ["How long does dealer approval take?", "Approval typically takes a few days."]],
}


def prune_faq(page):
    if page["file"] in BOILER_KEEP:
        return
    for sec in page["sections"]:
        if sec.get("type") == "faq":
            sec["items"] = [it for it in sec["items"] if it[0] not in BOILER_Q]
    if page["file"] in FAQ_ADD:
        faqs = [sec for sec in page["sections"] if sec.get("type") == "faq"]
        if faqs:
            faqs[0]["items"] = faqs[0]["items"] + [q for q in FAQ_ADD[page["file"]] if q not in faqs[0]["items"]]
    page["sections"] = [sec for sec in page["sections"] if not (sec.get("type") == "faq" and not sec.get("items"))]


# ---------------------------------------------------------------- the short answer under the H1
SHORT = {
    "services/intrusion.html": "DMP intrusion systems are built around the control panel. The XT Series, XTL Series and XR Series scale from a small business to a large site, with the XT75 hybrid panel at the small end and 96 doors of access control on the XR550. DMP builds the communicators too.",
    "services/access-control.html": "DMP access control runs from the stand-alone, cloud-based X1 Series to Entré Lite, Business, Enterprise and NOC software. Digital Key puts a credential in the mobile wallet of an Apple or Google device, and the modules support OSDP, BIN code and 1100 Series wireless, so doors and alarm zones share one platform.",
    "services/fire.html": "The XF6 is a 24V fire alarm control panel built for single-site applications, with network and optional cellular communications that send signals directly to the monitoring center. XR150FC and XR550FC fire panels, wireless smoke, heat and CO detectors, pull stations and remote annunciators complete the DMP fire range.",
    "services/video.html": "DMP video combines VUE Plus cameras, XV gateways with AlarmVision and the VK VMS video management platform, launched in September 2026. AlarmVision analytics raise alarms into XR Series panels, and camera drivers put cameras in Virtual Keypad, so video shares the accounts, apps and monitoring of the alarm system.",
    "services/communicators.html": "DMP communicators carry alarm signals over LTE, network and Wi-Fi paths, including the first alarm panel communicator for the AT&T FirstNet network, introduced in 2020. At the other end of the link, DMP builds the monitoring center equipment, from the SCS-VR virtual receiver software to the SCS-1R receiver and line cards.",
    "services/wireless.html": "DMP has made two-way wireless since 2004. The 1100 Series has been AES encrypted since 2019 and covers receivers, repeaters, door and window inputs, motion, glassbreak, panic, smoke, heat and CO devices. The 1100T and 1100TF translators let a dealer upgrade a competitor's wireless transmitters without rewiring.",
    "services/panels-keypads.html": "DMP panels and keypads are the core of a system. The range covers control panels, 7-inch and 5-inch touchscreen keypads, 9800, Thinline, Aqualite and Icon series keypads, zone and output modules, expanders, power supplies, batteries, transformers and enclosures, so a dealer can match the hardware to the size of the building.",
    "services/mobile-automation.html": "Virtual Keypad lets dealers brand a full-featured remote control for iOS, Android and the browser, while Dealer Admin handles mass panel programming and bulk firmware updates. Both are hosted in a Tier 4 data center, and DMP completes independent SOC 2 Type II examinations every year, by a licensed CPA firm.",
    "industries/commercial.html": "DMP commercial systems do more than sound an alarm. They combine intrusion, access control, fire and video on one platform, with the XR550 and XT75 panels, LTE communicators, 7-inch touchscreen keypads and Entré Enterprise software. Keypads are designed to be easy to operate for employees and service providers of any experience level.",
    "industries/financial-institutions.html": "For financial institutions, DMP integrates access control and intrusion so credentialing and reporting sit in one system. Automated reporting and simple credential administration reduce labor, compliance audits get simpler, and service calls and false alarms fall. TMSentry protects teller machines, and the 1142 panic transmitter puts a hold-up button under the counter.",
    "industries/retail.html": "DMP retail systems integrate access control and intrusion so one database manages user credentials. Cloud-based management software, with Virtual Keypad and Dealer Admin, runs multiple systems across a national footprint with a single action and automated enterprise reporting, from the XR150 panel and 1100 Series wireless receivers to VUE video doorbells.",
    "industries/government.html": "DMP technology is designed and built in the U.S.A. with U.S. and global components. A national network supports installation and service, and a division is dedicated to government customers. The library covers NDAA, BAA and TAA compliance, the NISPOM statement of compliance and encrypted cellular communications for SCIF installation.",
    "industries/industrial-manufacturing.html": "An integrated DMP system supports intrusion, access control, commercial fire and video together, so the door and the alarm run as one system with no extra wiring. Typical hardware is the XR550 panel, X1 access controllers, XV gateways with AlarmVision, VUE Plus fisheye cameras and Entré Enterprise software.",
    "industries/education.html": "DMP provides a broad line of security hardware and software that can be configured into a customized solution for school facilities. Digital Key and Bluetooth mobile credentials, SR3 readers and Entré Enterprise software manage access, so every public door can be locked in one action, with the XR550 panel and Virtual Keypad.",
    "industries/healthcare-wellness.html": "Healthcare providers must protect property from intrusion and secure patients' protected health information, as the HIPAA Privacy Rule requires. DMP systems pair the XR550 panel with Entré Enterprise access control, FirstNet-ready LTE communicators, touchscreen keypads, Virtual Keypad and the 1142 two-button wireless panic.",
    "industries/multi-tenant.html": "DMP systems for multi-dwelling units combine intrusion with fire protection, access control and video. A Digital Key credential in a phone wallet opens only what each person should reach, and customers control their systems remotely with the Virtual Keypad app, along with locks, lights and thermostats.",
    "industries/religious-institutions.html": "DMP builds products known for consistent reliability, and 100 percent of them are quality tested before shipping. A house of worship can run the full system from a small footprint: an XT75 panel, a 5-inch touchscreen keypad, glassbreak detection, XV gateways with AlarmVision, fisheye cameras and Virtual Keypad.",
    "industries/storage-units.html": "Storage facilities have unique security needs, so DMP hardware and software are designed for flexible, scalable solutions. XR550 and XR150 panels, X1 access controllers, XV gateways with AlarmVision, VUE Plus cameras and Virtual Keypad let an operator manage many panels across one site with one command.",
    "industries/residential.html": "DMP residential systems combine intrusion with fire protection and are easy to use, with Home, Sleep and Away arming in one touch. The XTLtouch and XTLplus panels, LTE communicators, 1164 synchronized smoke detectors and the VUE video doorbell are controlled remotely through Virtual Keypad, along with locks, lights and thermostats.",
}
for _k, _v in SHORT.items():
    assert 40 <= len(_v.split()) <= 55, (_k, len(_v.split()))


# ---------------------------------------------------------------- internal links to the blog
A, B, C, D, E_, F = ("blog/which-commercial-intrusion-panel.html", "blog/cellular-alarm-communication-options.html", "blog/cloud-based-access-control-dealer-guide.html",
                     "blog/add-video-verification-to-alarm-system.html", "blog/wireless-security-devices-retrofit.html", "blog/soc-2-type-ii-security-platform.html")
SENSOR = "news/small-sensor-big-save.html"
NEXT_BY_SYSTEM = {"intrusion": [A, B, E_], "panels-keypads": [A, E_], "communicators": [B, A], "access-control": [C, F], "fire": [E_, B, A],
                  "video": [D, A], "wireless": [E_, SENSOR, A], "mobile-automation": [F, C]}
SIBLINGS = {A: [B, D, E_], B: [A, E_, F], C: [F, D, A], D: [A, C, B], E_: [B, A, D], F: [C, B, A]}
NEXT_EXTRA = {"products/xt75.html": [A, B, SENSOR]}   # the XT75 is the panel in the small-sensor story


def _card(page, kicker, label):
    return [kicker, page["crumbs"][-1][0], smart_cut(page["description"], 130), label, page["file"]]


def add_links(data, ctx):
    by = {p["file"]: p for p in data["pages"]}
    systems = {f"services/{k}.html": k for k in NEXT_BY_SYSTEM}
    for slug, pr in ctx["PRODUCTS"].items():
        systems[f"products/{slug}.html"] = pr["system"]
    for f, sysk in systems.items():
        pg = by.get(f)
        if not pg:
            continue
        targets = NEXT_EXTRA.get(f) or NEXT_BY_SYSTEM.get(sysk) or [A, B]
        items = [_card(by[t], "Blog" if t.startswith("blog/") else "Customer story", "Read the guide" if t.startswith("blog/") else "Read the story") for t in targets if t in by]
        assert len(items) in (2, 3), f
        sec = {"type": "resources", "id": "read-next", "heading": "Read next", "intro": "Guides written for the dealers and specifiers who choose and install this equipment.", "items": items}
        _insert_before_form(pg, sec)
    for f, sibs in SIBLINGS.items():
        pg = by.get(f)
        if not pg:
            continue
        items = [_card(by[t], "Blog", "Read the guide") for t in sibs]
        sec = {"type": "resources", "id": "more-posts", "heading": "More from the blog", "intro": "Three more answers from the same series.", "items": items}
        _insert_before_form(pg, sec)
    home = by.get("index.html")
    if home:
        items = [_card(by[t], "Blog", "Read the guide") for t in (A, B, C)]
        sec = {"type": "resources", "id": "guides", "heading": "Guides for dealers and specifiers", "intro": "Three questions we hear most, answered up front.", "items": items}
        idx = next((i for i, s_ in enumerate(home["sections"]) if s_.get("type") == "resources"), None)
        if idx is not None:
            home["sections"].insert(idx + 1, sec)


def _insert_before_form(pg, sec):
    secs = pg["sections"]
    idx = len(secs)
    while idx > 0 and secs[idx - 1].get("type") in ("leadform", "contact", "cta"):
        idx -= 1
    secs.insert(idx, sec)


# ---------------------------------------------------------------- titles and descriptions
# DMP is a national manufacturer: titles end "| DMP" and name the product or category. Whole phrases, 30 to 60 characters, never cut.
TITLE_FIX = {
    "404.html": "Page not found: search the site or call | DMP", "accessibility.html": "Accessibility statement and WCAG 2.2 AA target | DMP",
    "assessment.html": "Dealer system-fit check: 14 questions | DMP", "stories.html": "Dealer stories: installs with DMP products | DMP",
    "trust.html": "Trust center: SOC 2 Type II and security | DMP", "stories/template-dealer-story.html": "Dealer story template: layout preview | DMP",
    "index.html": "Intrusion, access control, fire and video systems | DMP",
    "about.html": "About DMP: a U.S. security manufacturer since 1975 | DMP",
    "services.html": "Security products by system | DMP", "industries.html": "Security systems by industry | DMP",
    "contact.html": "Contact DMP: sales, tech support, customer service | DMP", "resources.html": "DMP news, announcements and resources | DMP",
    "faq.html": "Frequently asked questions about DMP systems | DMP", "blog.html": "DMP blog: guides for dealers and specifiers | DMP",
    "dealer-portal.html": "Dealer portal preview: one sign-in for dealers | DMP", "find-a-system.html": "Find a DMP system for your building | DMP",
    "for-building-owners.html": "For building owners: start with a dealer | DMP", "for-dealers.html": "For dealers: order, program and get support | DMP",
    "about/certifications.html": "Certifications: SOC 2 Type II every year | DMP", "about/dmp-cares.html": "DMP Cares: generosity as a company value | DMP",
    "partners.html": "Technology partners and integrations | DMP", "partners/evolon.html": "Evolon integration with DMP systems | DMP",
    "partners/genetec.html": "Genetec integration with DMP systems | DMP", "partners/havenlock.html": "HavenLock integration with DMP systems | DMP",
    "privacy-policy.html": "Privacy policy for dmp.com visitors | DMP", "terms-of-use.html": "Terms of use for dmp.com visitors | DMP",
    "services/intrusion.html": "Intrusion alarm systems: XT, XTL and XR panels | DMP", "services/access-control.html": "Access control: X1 cloud, Entré and Digital Key | DMP",
    "services/fire.html": "Fire alarm systems: XF6 and fire control panels | DMP", "services/video.html": "Video systems: VUE Plus cameras and AlarmVision | DMP",
    "services/communicators.html": "Alarm communicators and monitoring center receivers | DMP", "services/wireless.html": "Wireless security: AES encrypted 1100 Series | DMP",
    "services/panels-keypads.html": "Control panels, keypads and modules | DMP", "services/mobile-automation.html": "Virtual Keypad app and Dealer Admin software | DMP",
    "support.html": "Support and contacts: technical, sales, service | DMP", "support/become-a-dealer.html": "Become an authorized DMP dealer | DMP",
    "support/dealer-services.html": "Dealer services: Dealer Admin, firmware, returns | DMP", "support/get-a-quote.html": "Get a quote from DMP and authorized dealers | DMP",
    "support/private-label.html": "Private label keypads, Digital Keys and credentials | DMP", "support/tech-faqs.html": "Technical support FAQs for DMP installers | DMP",
    "support/tech-faqs/keypads.html": "Keypads technical FAQs from DMP Technical Support | DMP", "support/tech-faqs/video.html": "Video technical FAQs from DMP Technical Support | DMP",
    "support/tech-faqs/wireless.html": "Wireless technical FAQs from DMP Technical Support | DMP",
    "training/dmp-university.html": "DMP University: free on-demand training courses | DMP", "training/sales-training.html": "DMP sales training courses for dealers | DMP",
    "why-dmp.html": "Why DMP: made in the USA since 1975 | DMP",
    "blog/cloud-based-access-control-dealer-guide.html": "Cloud-based access control: a dealer guide | DMP",
    "news/jamalert-ul.html": "JamAlert achieves UL 2610 certification | DMP", "news/vault.html": "DMP introduces VAULT encrypted cloud connectivity | DMP",
    "news/vk-vms.html": "DMP launches VK VMS with AlarmVision | DMP", "news/vue-camera-line.html": "DMP launches the VUE camera line | DMP",
    "news/xr650-esx-award.html": "XR650 wins Best of Show at 2026 ESX | DMP",
}
TITLE_FIX.update({f"products/{k}.html": v + " | DMP" for k, v in {
    "digital-key-credential": "Digital Key mobile credential for access control", "entre-lite": "Entré Lite access control software",
    "entre-enterprise": "Entré Enterprise access control software", "dmp-bluetooth-reader-and-mobile-credential": "SR3 Bluetooth access control reader",
    "xt75": "XT75 hybrid intrusion and access control panel", "xt50": "XT50 hybrid intrusion panel for small business",
    "xtlplus": "XTLplus wireless control panel", "xtltouch": "XTLtouch all-in-one control panel", "xr150": "XR150 commercial and residential control panel",
    "xr550": "XR550 flagship control panel with fire and access", "xr650": "XR650 control panel, coming soon", "tmsentry": "TMSentry ATM control panel",
    "jamalert": "JamAlert cellular jamming detector", "virtual-keypad": "Virtual Keypad: remote control app for DMP systems",
    "dealer-admin": "Dealer Admin: cloud portal for DMP dealers", "remote-link": "Remote Link panel management software",
    "850": "850 Pull Station for fire alarm systems", "630f": "630F Remote Annunciator for fire systems",
    "xr150fc-2": "XR150FC fire alarm control panel", "xr550fc-2": "XR550FC fire alarm control panel",
    "v-6022wc": "V-6022WC 2MP indoor cube camera", "vue-video-doorbell": "VUE Video Doorbell with AI person detection",
    "icon-series": "Icon Series keypads for DMP alarm systems", "7000-series": "Thinline 7000 Series LCD keypads", "aqualite-series": "Aqualite Series LCD keypads",
}.items()})
DESC_FIX = {   # each ends on a whole sentence, 155 characters or fewer, and says only what the page says
    "index.html": "Digital Monitoring Products makes intrusion, access control, fire and video systems and sells them through authorized dealers across the United States.",
    "about.html": "Digital Monitoring Products has made security systems in the USA since 1975. Our mission, values, history, leaders and independent SOC 2 Type II examinations.",
    "services/access-control.html": "DMP access control runs from the stand-alone, cloud-based X1 Series to Entré enterprise software, with controllers, readers and phone-wallet credentials.",
    "services/fire.html": "DMP fire alarm control panels, detectors and communicators, led by the XF6, a 24V panel for single-site applications with network and cellular reporting.",
    "industries/government.html": "Security systems for government customers, designed and built in the U.S.A. with U.S. and global components and a national service network.",
    "industries/multi-tenant.html": "Security for multi-dwelling units that combines intrusion, fire protection, access control and video, with remote control through the Virtual Keypad app.",
    "industries/storage-units.html": "Security for storage facilities: flexible, scalable DMP hardware and software that manage many panels across one site with one command.",
    "support.html": "Four phone lines with hours: Inside Sales, Technical Support, Customer Service and SecureCom Wireless, plus FAQs, documentation and dealer services.",
    "support/tech-faqs/control-panel.html": "Control panel technical FAQs from DMP Technical Support: diagnostics codes, firmware updates, Remote Link, wireless and keypad setup.",
    "about/dmp-cares.html": "Generosity is one of our company values. DMP Cares supports worthy causes and gives our people the chance to give money, time and talent.",
    "about/certifications.html": "DMP completes an independent SOC 2 Type II examination every year for Dealer Admin and Virtual Keypad, hosted in a Tier 4 data center.",
    "international.html": "Eight authorized DMP distributors serve Benelux, Greece and Cyprus, Hungary, Latin America, Mexico, South Africa and the UK and Ireland.",
    "news/system-surveyor.html": "DMP's integration with System Surveyor lets dealers design intrusion, access control, fire and video systems on digital floor plans.",
    "news/vault.html": "VAULT, Virtual Access Using Layered Tunneling, lets dealers and enterprises use Virtual Keypad and Dealer Admin without exposing systems to the public internet.",
    "partners/evolon.html": "Evolon's AI video monitoring runs as a layer in the Virtual Keypad ecosystem, working with DMP intrusion panels and AlarmVision.",
    "partners/sureview.html": "SureView Response receives alarms from DMP SCS-1R and SCS-VR receivers and syncs panels and alarm points through Entré.",
    "partners/assa-abloy-aperio.html": "The DMP 734A module and an Aperio AH30 Gen5 hub bring battery-powered Aperio locks into the familiar DMP control experience on XR150 and XR550 panels.",
    "training/technical-training.html": "Technician and Advanced Bootcamps, Tech Training Tours and 13 instructor-led courses on XR, XT, XTL, X1, fire, COM, Dealer Admin and Virtual Keypad.",
    "blog.html": "Answers for dealers, specifiers and building owners on intrusion panels, cellular paths, cloud access control, video verification and SOC 2.",
}
for _k, _v in DESC_FIX.items():
    assert len(_v) <= 160 and _v.endswith("."), (_k, len(_v))
for _k, _v in TITLE_FIX.items():
    assert 30 <= len(_v) <= 60 and _v.endswith(" | DMP"), (_k, len(_v), _v)


def clean_title(t):
    return re.sub(r"\s*\|\s*Digital Monitoring Products(, Springfield, Missouri)?$", " | DMP", t)


CONFIRM = [
    "Article markup on blog posts and news items leaves datePublished, dateModified and author out on purpose. DMP must supply a publish date, a review date and a named author for each post; the hub's news dates can become datePublished once DMP confirms them.",
    "Organization logo: the only logo on dmp.com is an SVG. Search engines prefer a stable PNG or JPG (at least 112 by 112 pixels, on a plain background); DMP to supply one, and the markup will point at it.",
    "sameAs lists the LinkedIn, YouTube, Facebook, Crunchbase and BBB profiles that exist today (checked 9 November 2026). dmp.com does not link any of them; DMP to confirm they are official and to add them to the site footer. The BBB profile is listed, not accredited.",
]


# ---------------------------------------------------------------- entry point
def apply(data, ctx):
    pages = data["pages"]
    audit = json.load(open(os.path.join(HERE, "digital-monitoring-products.audit.json"), encoding="utf-8"))
    ctx = dict(ctx, FILES={p["file"] for p in pages})
    data["redirects"] = redirect_table(ctx, [p["path"] for p in audit["pages"]], pages)
    for pg in pages:
        pg["title"] = TITLE_FIX.get(pg["file"], clean_title(pg["title"]))
        if pg["file"] in DESC_FIX:
            pg["description"] = DESC_FIX[pg["file"]]
        if len(pg.get("description", "")) > 155:
            pg["description"] = smart_cut(pg["description"], 155)
        if pg.get("schema"):
            pg["schema"] = fix_schema_urls(pg["schema"], ctx)
        prune_faq(pg)
        if pg["file"] in SHORT and pg["sections"] and pg["sections"][0].get("type", "").startswith("hero"):
            pg["sections"][0]["subhead"] = SHORT[pg["file"]]
    add_links(data, ctx)
    for pg in pages:   # services pages: the CollectionPage carries its products as an OfferCatalog
        if pg["file"].startswith("services/"):
            lst = next((b for b in pg.get("schema", []) if b.get("@type") == "ItemList"), None)
            for b in pg.get("schema", []):
                if b.get("@type") == "CollectionPage" and lst:
                    b["url"] = f"{ctx['SITE']}/{pg['file'][:-5]}"
                    b["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": b.get("name", "") + " products",
                                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Product", "name": i["name"], "url": i["url"]}} for i in lst["itemListElement"]]}
    data.setdefault("pitch", {}).setdefault("confirm", []).extend(x for x in CONFIRM if x not in data["pitch"].get("confirm", []))
    sch = data.setdefault("schema", {})
    sch["updated"] = TODAY
    sch["sitemap_exclude"] = ["dealer-portal.html"]
    return data
