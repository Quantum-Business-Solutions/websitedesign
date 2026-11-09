#!/usr/bin/env python3
"""Digital Monitoring Products (dmp.com): three website directions.

Sourcing note. www.dmp.com serves its pages only after a JavaScript bot challenge, which this run does not script around.
What was readable: robots.txt, the XML sitemaps (page, product category and industry URLs), and the Client Command
SEO/AEO analysis dated 13 September 2026 (brief.seo). Every fact below comes from one of those or from the brief. Anything
else is listed under pitch["confirm"]. Product names are the ones in the sitemap URLs.

Run:  python3 brands/digital-monitoring-products.content.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "digital-monitoring-products.content.json")
CLIENT_REPO = os.path.join(HERE, "..", "..", "out-digital-monitoring-products")

CLIENT = "Digital Monitoring Products"
SHORT = "DMP"
PHONE, PHONE_HREF = "", "contact.html"   # not published in anything we could read: see confirm
FOUNDED = ""                             # not sourced: see confirm
REGION = "midwest"

TESTIMONIALS = []   # none published in what we could read
PARTNERS = []
TEAM = []

# slug, nav label, short, one-line, image, eyebrow, heading, subhead, benefits [[t,b]], included [..], faq [[q,a]]
SERVICES = [
    ["intrusion", "Intrusion Systems", "intrusion systems",
     "Control panels, keypads and modules for intrusion alarm systems.",
     "assets/office-dusk-2100.jpg", "Intrusion",
     "Intrusion systems built around <em>the control panel</em>.",
     "DMP lists its intrusion line by panel: the XR150, XR550 and XR650, the XT30, XT50 and XT75, the XTLtouch and XTLplus, and the X1 Series.",
     [["Panels by size", "The XR, XT and X1 families sit side by side, so a dealer can match the panel to the building instead of the other way round."],
      ["Keypads and modules", "Keypads, modules and expanders, and power supplies each have a category of their own."],
      ["One platform", "The same panels connect to DMP's communicators, Virtual Keypad and monitoring."]],
     ["Control panels", "Keypads including a 7 inch touchscreen keypad", "Modules and expanders", "Power supplies", "Communicators for cell and network reporting"],
     [["Which intrusion panels does DMP make?", "The product pages name the XR150, XR550, XR650, XT30, XT50, XT75, XTLtouch, XTLplus and X1 Series panels."],
      ["Who installs DMP intrusion systems?", "DMP sells through dealers. The dealer admin and marketing central pages on dmp.com are for them."],
      ["Where can I see the full range?", "The intrusion category on the products page lists every panel, keypad and module."]]],
    ["access-control", "Access Control", "access control",
     "Access control systems and the software that runs them.",
     "assets/camera-reader.png", "Access control",
     "Doors that answer <em>to the same system</em> as the alarm.",
     "DMP lists access control as its own product category, with Entré software and the 734 access module among the pages people read most.",
     [["Software included in the range", "Entré software has its own product page alongside the hardware."],
      ["Modules on the panel", "The 734 access module is one of the pages that already earns search traffic."],
      ["Alarm and doors together", "Access control sits in the same catalogue as intrusion, fire and video, so one dealer can quote all of it."]],
     ["Access control panels and modules", "Entré software", "Keypads and readers", "Integration with intrusion and video"],
     [["What is access control?", "A system that decides who can open which door and when, and keeps a record. DMP's access control category is where its products for that are listed."],
      ["Does DMP have software for access control?", "Yes. Entré software has a page of its own on dmp.com."],
      ["Is there a version for outside the United States?", "The sitemap lists a separate international access control page."]]],
    ["fire", "Fire Systems", "fire systems",
     "Fire alarm control panels and the equipment around them.",
     "assets/rack-1200.jpg", "Fire",
     "Fire alarm systems, <em>listed in the same catalogue</em> as everything else.",
     "DMP lists fire as its own product category, led by the XF6 fire control panel.",
     [["A dedicated panel", "The XF6 fire control panel has its own page."],
      ["Monitored", "Fire signals can be reported through DMP's communicators and monitoring centre products."],
      ["Same dealer, same platform", "Fire sits beside intrusion and access in one product range."]],
     ["XF6 fire control panel", "Communicators for cell and network reporting", "Modules, expanders and power supplies"],
     [["Which fire panel does DMP make?", "The XF6 fire control panel is the one named on the product pages."],
      ["Can fire alarms be monitored?", "DMP lists communicators and a monitoring centre category for reporting alarms."],
      ["How does a building owner start?", "Through a DMP dealer. The contact page will route the enquiry."]]],
    ["video", "Video", "video",
     "Cameras and a video doorbell that join the alarm system.",
     "assets/lab-1200.jpg", "Video",
     "Video that <em>shares the account</em> with the alarm.",
     "DMP lists Vue cameras and the Vue video doorbell in its video category.",
     [["Vue cameras", "Cameras are a named line, with their own product page."],
      ["Vue video doorbell", "A doorbell for the front door sits in the same category."],
      ["One app", "Video is reached through the same mobile platforms as the alarm."]],
     ["Vue cameras", "Vue video doorbell", "Mobile access through Virtual Keypad"],
     [["What video products does DMP make?", "Vue cameras and the Vue video doorbell are the ones named on dmp.com."],
      ["Is there an international range?", "The sitemap lists a separate international video page."],
      ["Where do I see live video?", "In the mobile platforms DMP lists on its products page."]]],
    ["communicators", "Communicators and Monitoring", "communicators and monitoring",
     "Cell and network communicators, and the monitoring centre category.",
     "assets/warehouse-1200.jpg", "Communicators",
     "A signal that <em>reaches the monitoring centre</em>.",
     "DMP lists cell and network communicators as one category and monitoring centre as another.",
     [["Cell and network", "Communicators report over a cellular or network path."],
      ["Monitoring centre", "A category for the people and software at the receiving end."],
      ["International versions", "The sitemap lists a separate international communicators page."]],
     ["Cell and network communicators", "Monitoring centre products", "Panels and keypads that report through them"],
     [["What does a communicator do?", "It carries the alarm signal from the panel to the monitoring centre."],
      ["Does DMP run a monitoring centre?", "The product category exists on dmp.com. The details are on the To confirm list."],
      ["Who sets it up?", "The dealer who installs the system."]]],
    ["wireless", "Wireless", "wireless security",
     "Wireless devices for DMP systems.",
     "assets/wireless-ap.png", "Wireless",
     "Wireless devices <em>that join the wired system</em>.",
     "DMP lists wireless as its own category, with an international version.",
     [["A category of its own", "Wireless products are grouped, not scattered across other pages."],
      ["Fits the panels", "Wireless connects to DMP control panels."],
      ["For retrofit and new work", "A dealer chooses wired or wireless per opening."]],
     ["Wireless devices", "Receivers and modules", "Compatible control panels"],
     [["Which wireless products does DMP list?", "The wireless category on the products page lists them."],
      ["Does it work with every panel?", "Check the product page for the panel in question; compatibility is on the To confirm list."],
      ["Is there an international version?", "Yes, the sitemap lists one."]]],
    ["panels-keypads", "Panels and Keypads", "panels and keypads",
     "Control panels, keypads, modules and power supplies.",
     "assets/office-dusk-2100.jpg", "Hardware",
     "The hardware <em>every system starts with</em>.",
     "Control panels, keypads, modules and expanders, and power supplies are four categories on dmp.com, each with an international version.",
     [["Panels", "The control panel category covers the intrusion, access and fire panels."],
      ["Keypads", "Including a 7 inch touchscreen keypad."],
      ["Modules and power", "Expanders and power supplies complete the system."]],
     ["Control panels", "Keypads", "Modules and expanders", "Power supplies"],
     [["How do I choose a panel?", "Start from the building and the number of zones and doors, then match the panel family. A DMP dealer does this."],
      ["Where are the datasheets?", "On each product page and in the resource library on dmp.com."],
      ["Are there international versions?", "Yes. The sitemap lists an international page for each of these categories."]]],
    ["mobile-automation", "Virtual Keypad and Automation", "Virtual Keypad and automation",
     "Mobile platforms, Virtual Keypad and automation.",
     "assets/lab-1200.jpg", "Mobile",
     "Control the system <em>from a phone</em>.",
     "DMP lists mobile platforms, Virtual Keypad and automation as categories on its products page.",
     [["Virtual Keypad", "The keypad on a phone, with its own page."],
      ["Mobile platforms", "Where the alarm, access and video accounts come together."],
      ["Automation", "A category of its own for lighting and building controls."]],
     ["Virtual Keypad", "Mobile platforms", "Automation"],
     [["What is Virtual Keypad?", "DMP's mobile keypad. It has its own page on dmp.com."],
      ["Does it work with video?", "DMP lists video and mobile platforms together."],
      ["Who activates it?", "The dealer who installed the system."]]],
]

# slug, name, image, one-line, body, bullets, faq
INDUSTRIES = [
    ["commercial", "Commercial", "assets/office-dusk-2100.jpg", "Offices and mixed-use buildings.",
     "Commercial buildings combine intrusion, access, fire and video. DMP lists commercial as its first industry.",
     ["Intrusion and access on one panel family", "Fire reported alongside", "Video at the entrances"],
     [["Which DMP products suit commercial buildings?", "Panels, access control, fire and video are all listed. A dealer will specify."]]],
    ["financial-institutions", "Financial institutions", "assets/lab-1200.jpg", "Banks and credit unions.",
     "Financial institutions need doors, vaults and cameras that report to one place. DMP lists them as an industry.",
     ["Access control for staff areas", "Intrusion with monitoring", "Video at the branch"],
     [["Does DMP serve banks?", "Financial institutions have their own page on dmp.com."]]],
    ["retail", "Retail", "assets/warehouse-1200.jpg", "Stores and shopping centres.",
     "Retail sites open and close every day and hold stock. DMP lists retail as an industry.",
     ["Arm and disarm by schedule", "Video at the door", "Fire reported"],
     [["Can a chain run many stores?", "Ask a dealer how accounts are grouped."]]],
    ["government", "Government", "assets/rack-1200.jpg", "Public buildings and agencies.",
     "Public buildings need to know who is inside and when. DMP lists government as an industry.",
     ["Access control with records", "Intrusion after hours", "Fire and video"],
     [["Is there a government page?", "Yes, on dmp.com under industries."]]],
    ["education", "Education", "assets/lab-1200.jpg", "Schools, colleges and universities.",
     "Campuses have many doors and many people. DMP lists education as an industry.",
     ["Doors by schedule", "Fire on every building", "Video at the entrances"],
     [["Does DMP list education?", "Yes, education has a page of its own."]]],
    ["healthcare-wellness", "Healthcare and wellness", "assets/office-dusk-2100.jpg", "Clinics, hospitals and wellness sites.",
     "Healthcare sites control access to people and to supplies. DMP lists healthcare and wellness as an industry.",
     ["Restricted areas", "Fire reported", "Video where permitted"],
     [["Is there a healthcare page?", "Yes, under industries on dmp.com."]]],
    ["religious-institutions", "Religious institutions", "assets/warehouse-1200.jpg", "Churches and other places of worship.",
     "Places of worship are open at set times and often unattended. DMP lists religious institutions as an industry.",
     ["Open and close by schedule", "Fire reported", "Remote control from a phone"],
     [["Does DMP serve places of worship?", "Yes, they have a page on dmp.com."]]],
    ["storage-units", "Storage units", "assets/rack-1200.jpg", "Self-storage facilities.",
     "Storage sites run on gates, doors and records of who came and went. DMP lists storage units as an industry.",
     ["Access control by unit", "Intrusion per door", "Video at the gate"],
     [["Is storage a DMP industry?", "Yes, it has its own page."]]],
]

# ------------------------------------------------------------------ helpers
def desc(text, n=155):
    if len(text) <= n:
        return text
    cut = text[:n]
    return cut[:cut.rfind(" ")].rstrip(",;:") + "."


def brief(text, n=150):
    if len(text) <= n:
        return text
    cut = text[:n]
    i = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    return cut[:i + 1] if i > 60 else cut[:cut.rfind(" ")].rstrip(",;:") + "."


COMMON_FAQ = {
    "who": ["Does DMP sell directly to building owners?", "DMP sells through dealers. A building owner starts with the contact form on this site, and a person at DMP replies."],
    "where": ["Where is DMP based?", "Digital Monitoring Products is headquartered in Springfield, Missouri."],
    "what": ["What does DMP make?", "Intrusion, access control, fire and video systems, with the communicators, keypads, wireless devices, Virtual Keypad and automation that go with them."],
    "intl": ["Is there an international range?", "dmp.com lists a global page and international versions of several categories, including control panels, keypads, modules, power supplies, communicators, video and wireless."],
    "person": ["How do I reach a person?", "Use the contact form on this site. A person replies, and the form asks only who you are and what you are specifying."],
    "docs": ["Where do I find datasheets and white papers?", "dmp.com has a resource library of white papers, marketing literature and training videos, all listed in its sitemap."],
}


def cf(*keys):
    return [COMMON_FAQ[k] for k in keys]


CTA = {"label": "Contact DMP", "href": "contact.html"}
LEADFORM = {"type": "leadform", "alt": True, "id": "start", "heading": "Tell DMP what you are specifying",
            "body": "Say who you are, what the building is and which products you are looking at. A person replies.",
            "submit": "Send to DMP", "note": "A person replies, not an autoresponder."}


def service_page(slug, navlabel, short, one, image, eyebrow, heading, subhead, benefits, included, faq):
    secs = [
        {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": heading, "subhead": subhead,
         "primary": CTA, "secondary": {"label": "All products", "href": "services.html"},
         "image": image, "image_alt": navlabel + " (generated stand-in image)", "image_w": 1200, "image_h": 800},
        {"type": "cards", "alt": True, "eyebrow": "What DMP lists", "heading": f"What to know about {short}", "items": benefits},
        {"type": "detail", "eyebrow": "In this category", "heading": "What is in the range", "body": one, "bullets": included, "image": image, "flip": True},
        {"type": "services", "heading": "Lines that pair with this one", "intro": "Each has its own page.",
         "items": [[x[1], x[3], f"services/{x[0]}.html"] for x in SERVICES if x[0] != slug][:3]},
        {"type": "faq", "heading": f"Questions about {navlabel.lower()}", "items": list(faq) + cf("who", "person", "docs", "intl")},
        LEADFORM,
    ]
    return {"file": f"services/{slug}.html", "title": f"{navlabel} | {CLIENT}, Springfield, Missouri",
            "description": desc(f"{one} {subhead} From Digital Monitoring Products in Springfield, Missouri."),
            "crumbs": [["Home", "index.html"], ["Products", "services.html"], [navlabel, f"services/{slug}.html"]], "sections": secs}


def industry_page(slug, name, image, one, body, bullets, faq):
    return {"file": f"industries/{slug}.html", "title": f"Security systems for {name.lower()} | {CLIENT}, Springfield, Missouri",
            "description": desc(f"{one} {body} Digital Monitoring Products, Springfield, Missouri.", 158),
            "crumbs": [["Home", "index.html"], ["Industries", "industries.html"], [name, f"industries/{slug}.html"]],
            "sections": [
                {"type": "hero", "layout": "split", "eyebrow": name, "heading": f"Security systems for <em>{name.lower()}</em>.", "subhead": one,
                 "primary": CTA, "secondary": {"label": "All products", "href": "services.html"}, "image": image, "image_alt": name + " (generated stand-in image)", "image_w": 1200, "image_h": 800},
                {"type": "detail", "alt": True, "eyebrow": "What matters here", "heading": f"How {name.lower()} use DMP", "body": body, "bullets": bullets},
                {"type": "services", "heading": "The product lines that matter most here", "intro": "Each has its own page.",
                 "items": [[SERVICE_INDEX[s][1], SERVICE_INDEX[s][3], f"services/{s}.html"] for s in ("intrusion", "access-control", "fire", "video")]},
                {"type": "faq", "heading": f"Questions from {name.lower()}", "items": list(faq) + cf("who", "what", "person", "docs", "intl")},
                LEADFORM]}


SERVICE_INDEX = {s[0]: s for s in SERVICES}
WHEEL_ITEMS = [[s[1], brief(s[3], 140), f"services/{s[0]}.html", s[1]] for s in SERVICES]


def build():
    brand = {
        # Measured from dmp.com on 9 Nov 2026 (Firecrawl branding read of the home page): yellow #FFD23D on black #000003,
        # HCo Gotham SSm (licensed, so Montserrat stands in), square cards and inputs with pill-shaped buttons, the white "light" logo for a dark header.
        "accent": "#FFD23D", "ink_secondary": "#000003", "chrome": "dark", "chrome_bg": "#0b0b0c",
        "fonts": {"heading": "HCo Gotham SSm", "body": "HCo Gotham SSm"}, "radius": 0, "button_radius": 999,
        "logo": "assets/dmp-logo.svg", "logo_alt": CLIENT, "logo_w": 100, "logo_h": 37,
        "logo_note": "DMP's own logo SVG from dmp.com (white, built for a dark ground). Send the full-colour version for light bands.",
        "phone": PHONE, "phone_href": PHONE_HREF, "email": "",
        "utility": [{"label": "For dealers", "href": "contact.html"}],
        "cta": CTA,
        "sticky": {"primary": "Contact DMP", "primary_href": "contact.html", "secondary": "Products", "secondary_href": "services.html"},
        "launcher": {"label": "Already a dealer?", "eyebrow": "The fast lane", "title": "What do you need today?",
                     "links": [["Products", "services.html"], ["Contact DMP", "contact.html"]], "note": "", "phone": PHONE, "phone_href": PHONE_HREF},
        "social": {}, "tagline": "Security, fire, access control and video, made in Springfield, Missouri.",
        "footer_columns": [
            {"title": "Products", "links": [[s[1], f"services/{s[0]}.html"] for s in SERVICES]},
            {"title": "Industries", "links": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES]},
            {"title": "Company", "links": [["About", "about.html"], ["Locations", "locations.html"], ["FAQ", "faq.html"], ["Contact", "contact.html"]]},
        ],
        "legal": [],
    }
    schema = {"org_name": CLIENT, "org_url": "https://www.dmp.com", "org_logo": "https://www.dmp.com/static/logo-light.DC983iDA.svg",
              "org_description": "Digital Monitoring Products designs and builds intrusion, access control, fire and video security systems, sold through dealers, and is headquartered in Springfield, Missouri.",
              "sameAs": [], "telephone": ""}
    schema.update({"short_name": "DMP", "title_city": "Springfield, Missouri", "cities": ["Springfield", "Springfield, Missouri", "Missouri", "MO"],
                   "area_served": [{"@type": "Country", "name": "United States"}],
                   "meta_tail": "Digital Monitoring Products, Springfield, Missouri.", "local": []})
    nav = [
        {"label": "Products", "href": "services.html", "children": [[s[1], f"services/{s[0]}.html"] for s in SERVICES]},
        {"label": "Industries", "href": "industries.html", "children": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES]},
        {"label": "About", "href": "about.html", "children": [["About", "about.html"], ["Locations", "locations.html"], ["FAQ", "faq.html"], ["Contact", "contact.html"]]},
    ]
    pages = []
    pages.append({"file": "index.html", "title": f"{CLIENT} | Security, fire, access and video from Springfield, Missouri",
                  "description": "Digital Monitoring Products, Springfield, Missouri: intrusion, access control, fire and video systems, with communicators, Virtual Keypad and monitoring. Contact DMP.",
                  "sections": [
        {"type": "hero", "id": "hero-light", "layout": "split", "eyebrow": "Springfield, Missouri",
         "heading": "Security, fire, access and video, <em>from one manufacturer</em>.",
         "subhead": "Digital Monitoring Products makes control panels, keypads, communicators, access control, fire and video, and sells them through dealers.",
         "primary": CTA, "secondary": {"label": "See the products", "href": "services.html"},
         "note": "Generated preview imagery, labelled as such", "image": "assets/hero-1200.jpg", "image_alt": "A meeting room (generated stand-in image)", "image_w": 1200, "image_h": 800},
        {"type": "wheel", "id": "wheel", "eyebrow": "One range", "heading": "Eight product lines, one catalogue", "intro": "Hover a segment.",
         "items": WHEEL_ITEMS, "panel_eyebrow": "Hover a segment", "link_label": "See the product line"},
        {"type": "services", "id": "services", "heading": "The product lines", "intro": "Each has its own page, in DMP's own category names.",
         "items": [[s[1], s[3], f"services/{s[0]}.html"] for s in SERVICES]},
        {"type": "cards", "id": "industries", "alt": True, "eyebrow": "Industries", "heading": "Built for the buildings people work in",
         "intro": "DMP names these industries on its own site. Each has a page.",
         "items": [[i[1], i[3]] for i in INDUSTRIES[:6]]},
        {"type": "faq", "id": "faq", "heading": "Questions we get on the first call", "items": [
            ["Who does DMP sell to?", "Through dealers. The dealer admin and marketing central pages on dmp.com are for them."],
            ["Where is DMP based?", "Springfield, Missouri."],
            ["Which systems does DMP make?", "Intrusion, access control, fire and video, with communicators, keypads, wireless, Virtual Keypad and automation."]]},
        {"type": "contact", "id": "contact", "heading": "Talk to DMP", "body": "Tell us who you are and what you are specifying. A person replies.",
         "options": ["I am a dealer", "I am specifying a building", "I own a building", "Something else"], "submit": "Send to DMP",
         "note": "A person replies, not an autoresponder."},
    ]})
    pages.append({"file": "services.html", "title": f"Products | {CLIENT}, Springfield, Missouri",
                  "description": "Eight product lines from Digital Monitoring Products in Springfield, Missouri: intrusion, access control, fire, video, communicators, wireless, panels and keypads, Virtual Keypad.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Products", "heading": "Eight lines, <em>one manufacturer</em>.",
         "subhead": "Every line below is listed on dmp.com under its own category.", "primary": CTA},
        {"type": "resources", "heading": "The product lines", "intro": "Each page names what DMP lists in that category.",
         "items": [[s[5], s[1], s[3], "See the line", f"services/{s[0]}.html"] for s in SERVICES]},
        {"type": "faq", "heading": "Questions about the range", "items": cf("what", "who", "intl", "docs", "person")},
        LEADFORM]})
    for s in SERVICES:
        pages.append(service_page(*s))
    pages.append({"file": "industries.html", "title": f"Industries | {CLIENT}, Springfield, Missouri",
                  "description": "Commercial, financial, retail, government, education, healthcare, religious and storage: the industries Digital Monitoring Products names, each with its own page.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Industries", "heading": "Eight kinds of building, <em>each with a page</em>.",
         "subhead": "These are the industries DMP names on its own site.", "primary": CTA},
        {"type": "resources", "heading": "Who DMP builds for", "intro": "Choose the nearest match.",
         "items": [[i[1], i[1], i[3], f"Security for {i[1].lower()}", f"industries/{i[0]}.html"] for i in INDUSTRIES]},
        {"type": "faq", "heading": "Questions about industries", "items": [["Which industries does DMP name?", "Commercial, financial institutions, retail, government, industrial manufacturing, education, healthcare and wellness, multi-tenant, religious institutions, storage units and residential are all listed on dmp.com. This preview gives eight of them a page."]] + cf("what", "who", "person")},
        LEADFORM]})
    for i in INDUSTRIES:
        pages.append(industry_page(*i))
    pages.append({"file": "about.html", "title": f"About {CLIENT} | Security manufacturer in Springfield, Missouri",
                  "description": "Digital Monitoring Products is headquartered in Springfield, Missouri. About the company, its certifications, careers and community work, as listed on dmp.com.",
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "About DMP", "heading": "A manufacturer <em>headquartered in Springfield</em>, Missouri.",
         "subhead": "dmp.com lists pages for certifications, careers and DMP Cares under About us.", "primary": CTA,
         "image": "assets/warehouse-1200.jpg", "image_alt": "A warehouse floor (generated stand-in image)", "image_w": 1200, "image_h": 800},
        {"type": "cards", "alt": True, "eyebrow": "On dmp.com", "heading": "Where to read more", "items": [
            ["Certifications", "A page of its own under About us."], ["Careers", "A page of its own under About us."], ["DMP Cares", "A page of its own under About us."]]},
        {"type": "detail", "eyebrow": "What DMP lists", "heading": "The company, as dmp.com names it", "body": "The pages under About us on dmp.com are certifications, careers and DMP Cares. This preview points to them and does not restate them until DMP confirms the copy.",
         "bullets": ["Certifications", "Careers", "DMP Cares", "A global page for markets outside the United States", "Events", "A resource library"]},
        {"type": "faq", "id": "faq", "heading": "Questions about DMP", "items": cf("where", "what", "who", "intl", "person", "docs")},
        LEADFORM]})
    pages.append({"file": "locations.html", "title": f"Locations | {CLIENT}, Springfield, Missouri",
                  "description": "Digital Monitoring Products is headquartered in Springfield, Missouri. A global page on dmp.com covers markets outside the United States.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Locations", "heading": "Headquartered in <em>Springfield, Missouri</em>.",
         "subhead": "The street address and phone number are on the To confirm list; they will appear here once confirmed.", "primary": CTA},
        {"type": "faq", "id": "faq", "heading": "Where DMP works", "items": cf("where", "intl", "who", "what", "person")},
        LEADFORM]})
    pages.append({"file": "faq.html", "title": f"FAQ | {CLIENT}, Springfield, Missouri",
                  "description": "Answers to the first questions about Digital Monitoring Products in Springfield, Missouri: who it sells to, what it makes, and how to reach a person.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "FAQ", "heading": "Questions, <em>answered plainly</em>.", "subhead": "If yours is not here, ask. A person replies."},
        {"type": "faq", "heading": "About DMP", "items": cf("what", "who", "where", "intl", "person", "docs")},
        LEADFORM]})
    pages.append({"file": "contact.html", "title": f"Contact | {CLIENT}, Springfield, Missouri",
                  "description": "Contact Digital Monitoring Products in Springfield, Missouri. Tell DMP who you are and what you are specifying, and a person replies.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Contact", "heading": "Tell DMP <em>what you are specifying</em>.",
         "subhead": "Dealers, specifiers and building owners all start in the same place."},
        {"type": "contact", "id": "form", "heading": "Contact DMP", "body": "Choose what fits best. A person replies.",
         "options": ["I am a dealer", "I am specifying a building", "I own a building", "Something else"], "submit": "Send to DMP",
         "note": "A person replies, not an autoresponder."},
        {"type": "detail", "alt": True, "eyebrow": "What to include", "heading": "Say it once, plainly", "body": "The form is short. These details help the person who reads it.",
         "bullets": ["Whether you are a dealer, a specifier or a building owner", "The kind of building and the industry", "Which product lines you are looking at", "Your company and a way to reach you"]},
        {"type": "faq", "heading": "Before you write", "items": cf("person", "who", "where", "what", "docs", "intl")},
    ]})

    pitch = {
        "qbs_contact": {"name": "Shawn", "email": "shawn@thequantumleap.business"},
        "prepared_for": "Digital Monitoring Products",
        "heard_intro": "There is no design brief from DMP yet. Everything here comes from what dmp.com publishes in its sitemap and from the SEO and AEO analysis in the portal. Tell us where it is wrong; your words outrank ours.",
        "heard": ["No stated promise, likes or dislikes yet. The promise line on the home page is ours and is unconfirmed.",
                  "DMP is a current Quantum client with a HubSpot CRM, marketing, sales and service launch under way, so the site has to feed that: forms that create records, one place for dealers to start.",
                  "Every claim stays tied to dmp.com. Where we could not read it, we said so on the list below instead of guessing."],
        "found": ["dmp.com earns about 24,493 organic visits a month on 7,462 keywords, but 66 percent of that is people already searching the brand (Semrush, 13 September 2026).",
                  "The apex domain answers with a 307, the home page had no title, no H1 and no canonical when crawled, and no robots.txt or sitemap was readable at dmp.com.",
                  "DMP appeared in none of nine buyer searches run from Springfield, Missouri, and was named in none of the AI answers.",
                  "No schema, no sameAs links, no address and no tappable phone number were found. Authority is not the problem: 1,916 referring domains, Authority Score 39.",
                  "There is no blog or insights section, and no page answers a buyer's question in a buyer's words.",
                  "The pages that earn the traffic are product and support pages, such as dealer admin, the 734 access module and the control panels index."],
        "choose_heading": "Three directions. Your call.",
        "choose_intro": "The words and the pages are the same in all three. What differs is the register. Open each one and tell us which feels like DMP.",
        "pick_reasons": [["The audience is dealers and specifiers", "They scan a catalogue to find a panel or a module. Clean puts the product names and categories first and stays out of the way."],
                         ["The site is large", "dmp.com lists dozens of product pages and a deep resource library. A plain, fast, high-contrast layout carries that better than a showy one."],
                         ["The brand is already strong", "DMP's yellow on black carries the page. Clean keeps the surface plain so the yellow is the only loud thing on it."]],
        "pick_change": "Send the full-colour logo and the Gotham licence or a web-font file, so the headings are DMP's own face and not the closest free one.",
        "alternatives": [["Quantum Showcase", "The safe, image-led choice: layered, sales-forward, and the one that shows the most photography once DMP supplies its own."],
                         ["Quantum Press", "The wildcard: serif and editorial, so a manufacturer reads like an established company."]],
        "plan": [["Days 1 to 10", "Serve the site at one canonical host with a 301, publish robots.txt and a sitemap, add titles, one H1 per page and Organization plus LocalBusiness schema."],
                 ["Days 10 to 30", "Confirm the items below, supply the logo and photography, and sign off copy for every product line."],
                 ["Days 30 to 45", "Build the eight product line pages with FAQ markup, Service schema and an enquiry form on each."],
                 ["Days 45 to 60", "Build the Springfield, Missouri page and add sameAs links to LinkedIn, Crunchbase, BBB and YouTube."],
                 ["Days 60 to 90", "Publish the about, careers and news pages and the first three answer posts on access control, fire alarm and video."],
                 ["Day 90", "Re-run the same nine Springfield searches, the same six AI questions and the same page audit against the baseline."]],
        "search": {"heading": "Where you stand in search today, and what changes", "intro": "Measured before we touched anything.", "as_of": "13 September 2026",
                   "today_stats": [["24,493", "Organic visits a month"], ["7,462", "Organic keywords"], ["0 of 9", "Top-ten results in Springfield"], ["39", "Authority Score"]],
                   "today": [], "after": [], "keep": [], "note": ""},
        "confirm": [
            "Everything on dmp.com page by page. www.dmp.com serves pages only after a JavaScript bot challenge, so this run read the sitemap, robots.txt and the portal SEO analysis only. Every page was written from product and category names, not from DMP's own copy. All copy needs DMP review.",
            "The promise. There is no brief from DMP, so the home page line is ours and unconfirmed.",
            "Typeface. DMP sets its site in HCo Gotham SSm, a licensed face we cannot ship. Montserrat stands in. The logo, yellow and black are read from dmp.com; please confirm they are the current brand.",
            "Legal name, street address and phone number. None were readable, so none appear. The mobile menu shows a \"Call\" link with no number until the phone is supplied.",
            "The year DMP was founded, staff counts, certifications and awards. None are sourced, so none appear.",
            "Testimonials, partners, team and customer names. None were readable, so none appear.",
            "Product claims. Each product line lists only the names that appear in the sitemap. Specifications, listings and compatibility need DMP's product team.",
            "The industries. Eight of eleven are used. Industrial manufacturing, multi-tenant and residential are left out and can be added.",
            "Whether DMP operates its own monitoring centre, and how dealers should be described.",
            "Social profiles. The SEO analysis names LinkedIn, Crunchbase, BBB, YouTube and Facebook but gives no URLs, so none are linked.",
            "Photography. Every image is a generated stand-in from the Quantum library and is labelled as such.",
            "The 307 on the apex domain and the bot challenge. Confirm with DMP's IT whether the challenge will stay once the new site is live, because it also blocks search crawlers."],
        "footer": "Prepared for Digital Monitoring Products. Nothing here is live or indexed. Photographs are generated stand-ins and labelled as such.",
    }
    return {"client": CLIENT, "slug": "digital-monitoring-products", "domain_hint": "dmp.com", "brand": brand, "schema": schema, "nav": nav, "pages": pages, "pitch": pitch}


if __name__ == "__main__":
    data = build()
    with open(OUT, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}: {len(data['pages'])} pages")
