#!/usr/bin/env python3
"""Authoring script for brands/image-2000.content.json.

Run it to regenerate the JSON that scripts/preview.py reads:

    python3 brands/image-2000.content.py

Every fact is SOURCED from image-2000.com (scraped 8 September 2026), the ClientCommand record of the weekly
Quantum and Image 2000 meetings, or Semrush. Anything we could not source is marked TO CONFIRM in a comment and
listed on the hub under To confirm. No em dashes anywhere; write it clean.
"""
import json
import os
import re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image-2000.content.json")

CLIENT = "Image 2000"
PHONE, PHONE_HREF = "800-481-2250", "tel:8004812250"          # header of image-2000.com
HQ_PHONE, HQ_PHONE_HREF = "818-781-2200", "tel:8187812200"    # Valencia direct line
PAY_URL = "https://pay.mysfsgateway.com/Image2000-0889"        # "Pay Invoices by Credit Card" link on the live site
LINKEDIN = "https://www.linkedin.com/company/image2000"

# ------------------------------------------------------------------ sourced facts (image-2000.com)
MISSION = "To facilitate and support the client's vision while providing flexible, responsive, and personal service."
TESTIMONIALS = [  # home page testimonial slider. First names only, as published.
    ["We have been with Image 2000 for over 14 years, and their level of service has always been nothing less than superb.", "Cathy Vasilev", "Contract Administrator, Cedars-Sinai Medical Center"],
    ["Give them an opportunity to earn your business. If you don't, you're doing yourself a disservice!", "Robert O.", "Image 2000 customer"],
]
# Manufacturer and technology partners named on the live site (product catalog menu, about page, software and IT pages).
MANUFACTURERS = ["Kyocera", "Copystar", "Sharp", "Toshiba", "Lexmark", "Brother", "HP", "KIP", "Canon", "Kodak Alaris", "RISO", "Formax", "Waterlogic", "Sharp NEC Displays"]
SOFTWARE_PARTNERS = ["Square 9 Softworks", "DocuWare", "FormedAI", "PaperCut"]
# From the Our Clients page on image-2000.com (graphic, 8 September 2026).
CLIENT_FIELDS = "Churches, universities, school districts, medical centers, and small, medium and large businesses"
CLIENT_PROOF = [["Over 20", "Adventist Health medical centers"], ["Over 9", "School districts in Southern California"], ["Since 1992", "Founder-owned, Valencia"], ["100", "PROs Elite dealers in the US; one is Image 2000"]]
CLIENTS = ["Children's Hospital Los Angeles", "Adventist Health", "Cedars-Sinai Medical Center", "Saugus Union School District", "Cerritos College", "El Rancho School District", "Grove Unified School District", "Cathedral of Our Lady of the Angeles", "The Universal Church", "Make-A-Wish Orange County and the Inland Empire", "Knobbe Martens", "E&J Gallo Winery", "BIG 5 Sporting Goods", "Balboa Bay Club", "Pasea Hotel and Spa", "Firefighters First Credit Union", "Financial Credit Union", "Fidelity Management Services", "GARDA", "California Motors Direct", "Manhattan Beachwear Inc.", "Sun Valley Specialty Healthcare"]
COMMUNITY = ["Henry Mayo Newhall Hospital", "Adventist Health", "Make-A-Wish", "St. Baldrick's Foundation", "Boys & Girls Clubs of America", "Saugus High School", "Pateadores", "Wish Education Foundation", "JCC of Orange County", "Single Mothers Outreach of Santa Clarita", "East Valley Family Services", "Tierra Del Sol Foundation", "Sebastian Velona Foundation", "The Giving Back Fund", "Ensign Group", "Bridgestone Living", "CFMA"]
CLIENTS_STRIP = {"type": "partners", "id": "clients", "caption": "Some of the organizations Image 2000 serves", "items": CLIENTS}
AWARDS = [  # value, title, detail. All from the awards and home pages.
    ["FY26", "Kyocera Platinum Partner", "Kyocera's FY26 Platinum Partner Award, after the FY2024 Gold Partner award and the Platinum Platter recognition ENX Magazine reported in 2024."],
    ["2016", "PROs Elite certified every year since", "One of about 100 dealers in the United States, one per market, with service results audited by PROs Elite."],
    ["5x", "Sharp Hyakuman Kai Elite Award, five in a row", "ENX Magazine counts five consecutive years, and ranks Image 2000 the 12th largest Sharp dealer in the country."],
    ["2018-24", "ENX Magazine Elite Dealer", "Seven consecutive years."],
    ["2019", "Copystar Excellence in Customer Service", "Plus the Copystar Elite Dealer Award the same year."],
    ["A", "BBB Accredited Business", "Accredited by the Better Business Bureau, A rating."],
]
LEADERS = [
    ["Rich Campbell", "President and co-owner", "Co-founded Image 2000 in 1992 and has spent 25 years developing one of the largest equipment providers in Southern California."],
    ["Joe Blatchford", "CEO and co-owner", "Brings 31 years of professional experience to his position as CEO of Image 2000, Inc."],
    ["Jeff Rudisel", "Chief Operations Officer", "32 years on the technical, distribution and sales management sides of the business."],
]
# Branches as listed in the site footer. slug, label, address 1, address 2, phone, phone href, lat, lon, region served, city for titles
LOCATIONS = [
    ["valencia", "Valencia (Corporate)", "26037 Huntington Lane", "Santa Clarita, CA 91355", "818-781-2200", "tel:8187812200", 34.437, -118.575, "the Santa Clarita Valley, the San Fernando Valley and north Los Angeles County", "Valencia"],
    ["los-angeles", "Los Angeles", "10350 Heritage Park Dr., Suite 203", "Los Angeles, CA 90670", "818-974-0237", "tel:8189740237", 33.930, -118.060, "Los Angeles and the Gateway Cities", "Los Angeles"],
    ["orange-county", "Orange County", "18022 Cowan Street, Suite 240", "Irvine, CA 92614", "714-543-5234", "tel:7145435234", 33.690, -117.830, "Irvine and Orange County", "Orange County"],
    ["inland-empire", "Inland Empire", "1520 N. Mountain Ave, Suite 203", "Ontario, CA 91762", "818-781-2200", "tel:8187812200", 34.075, -117.650, "Ontario, Riverside and San Bernardino counties", "the Inland Empire"],
    ["bakersfield", "Bakersfield", "6801 White Lane, Suite H-3", "Bakersfield, CA 93309", "661-835-4900", "tel:6618354900", 35.340, -119.050, "Bakersfield and Kern County", "Bakersfield"],
    ["fresno", "Fresno", "4910 E. Pontiac Way, Suite 102", "Fresno, CA 93726", "559-275-7476", "tel:5592757476", 36.790, -119.770, "Fresno and the Central Valley", "Fresno"],
    ["las-vegas", "Las Vegas", "3325 West Ali Baba Lane, Suite 606", "Las Vegas, NV 89118", "702-513-3864", "tel:7025133864", 36.080, -115.200, "Las Vegas and southern Nevada", "Las Vegas"],
]
LABEL_OFFSETS = {"valencia": (-86, -10), "los-angeles": (-118, 18), "orange-county": (12, 20), "inland-empire": (12, -6), "bakersfield": (12, 4), "fresno": (12, 4), "las-vegas": (12, 4)}

# Industries named on the UCaaS page ("UCaaS for different industries"): government, education, healthcare, religious establishments.
INDUSTRIES = [  # slug, name, image, one-line, body, bullets, faq
    ["government", "Government", "assets/doc-mgmt-1200.jpg",
     "Agencies print, scan and file at volume, under records rules, on budgets that go through procurement.",
     "City, county and special-district offices run on documents with retention rules attached. Image 2000 configures multifunction devices for secure release and scan to records, builds capture and workflow with Square 9 and DocuWare for permits, invoices and public records, and prices lease and purchase for a procurement process.",
     ["Secure print release and audit trails on shared devices", "Capture and workflow for permits, AP and records requests", "Elevate cloud phones for offices that serve the public", "Lease and purchase priced for procurement"],
     [["Do you work with public procurement?", "Yes. Ask your branch how Image 2000 has quoted for agencies in its territory and what the paperwork looks like."], ["Can records retention be enforced in the software?", "DocuWare and Square 9 carry retention rules and audit trails. Tell us the schedule you are held to and we build to it."]]],
    ["education", "Education", "assets/production-print-1200.jpg",
     "Schools and districts print more than almost anyone and have the least time to manage it.",
     "Classroom packets, exams, mailings and the front office all run on print. Image 2000 serves over nine school districts in Southern California, among them Saugus Union, El Rancho and Grove Unified, plus Cerritos College, and right-sizes multifunction devices for buildings, adds RISO duplicators and production print where volume justifies them, and puts the whole fleet under managed print so toner and service happen without a work order.",
     ["Managed print across buildings, with supplies from the nearest branch", "RISO duplicators and production print for high-volume packets", "Wide-format for posters, plans and signage", "Cloud phones and contact center for district offices"],
     [["Can you service several campuses?", "Yes. Seven branches across California and Nevada, with technicians dispatched from the nearest one."], ["Have you worked with districts like ours?", "Yes. Over nine school districts in Southern California, including Saugus Union, El Rancho and Grove Unified, and Cerritos College."]]],
    ["healthcare", "Healthcare", "assets/mps-2-1200.jpg",
     "Medical centers need print and fax that protect patient information and keep working at seven in the morning. Over twenty Adventist Health sites already rely on Image 2000.",
     "Medical centers print referrals, forms and records all day, across many sites. Image 2000 serves over twenty Adventist Health medical centers, Children's Hospital Los Angeles and Cedars-Sinai Medical Center, and sets up secure print release, secure fax and capture into a records system with the access controls a compliance review expects, and services every site from the nearest branch.",
     ["Secure print release and secure fax where the device supports it", "Capture and document management with role-based access", "Fleet monitoring so toner and service happen before the front desk notices", "Elevate phones with Teams integration for multi-site practices"],
     [["Are your devices and workflows HIPAA-aware?", "The devices and the document management software are configured with the controls a HIPAA review looks for: access control, audit trail and encryption where supported. Your compliance officer confirms the policy; we build to it."], ["What happens when a device fails during clinic hours?", "Call the branch. Image 2000 is a PROs Elite dealer, which means its service results are audited every year against a 95% uptime standard."]]],
    ["churches-nonprofits", "Churches and nonprofits", "assets/mailroom-printer-1200.jpg",
     "Bulletins, mailings and programs every week, on a budget that answers to a board or a congregation.",
     "Churches, ministries and nonprofits produce a remarkable amount of print: weekly bulletins, programs, mailings, curriculum. Image 2000 serves the Cathedral of Our Lady of the Angeles, The Universal Church and Make-A-Wish Orange County and the Inland Empire, and right-sizes production print and RISO duplicators for the volume you run, adds Formax folding and inserting for mailings, and keeps the cost per piece visible so the finance committee can see it too.",
     ["Production print and RISO duplicators for weekly volume", "Formax folder-inserters for member and donor mailings", "Bottleless Waterlogic water for fellowship spaces", "Lease and purchase priced for nonprofit budgets"],
     [["We are a small church. Is this for us?", "Yes. Right-sizing is the point. Bring a year of copy-shop invoices to the quote and we price a small production device beside them."], ["Do you offer nonprofit pricing?", "Ask your branch. We will price lease and purchase side by side for your real volume."]]],
]

# The service lines. slug, nav label, short, one-line, image, eyebrow, hero heading (with <em>), subhead, benefits [[t,b]], included [..], faq [[q,a]], partner caption
SERVICES = [
    ["office-technology", "Copiers, printers and office technology", "Office technology", "Multifunction copiers, printers, wide-format, scanners and displays from an eleven-manufacturer portfolio.", "assets/mps-1-1200.jpg", "Office technology",
     "The right device is the one you <em>stop thinking about</em>.",
     "Kyocera, Copystar, Sharp, Toshiba, Lexmark, Brother and HP multifunction copiers and printers, KIP and Canon wide-format, Kodak Alaris scanners and Sharp NEC displays, matched to your volume, networked on day one and serviced from the nearest of seven branches.",
     [["Multifunction copiers", "Color and mono MFPs from small offices to departmental workhorses, with scanning built in."], ["Printers", "Desktop and workgroup printers for the pages that never touch the copier."], ["Wide format", "KIP and Canon large-format for plans, drawings and signage in house."], ["Scanners and displays", "Kodak Alaris scanners and Sharp NEC displays."]],
     ["Lease or buy, priced side by side for your real volume", "An eleven-manufacturer portfolio, so the recommendation fits the job rather than the badge", "Secure print release and scan-to-cloud on the devices we recommend", "Drivers, manuals and training for your team on the support page"],
     [["Which brands do you carry?", "Kyocera, Copystar, Sharp, Toshiba, Lexmark, Brother, HP, KIP, Canon large format, Kodak Alaris, RISO, Formax, Waterlogic and Sharp NEC displays. We recommend the device, not the badge."], ["Can we start with one device?", "Yes. Many customers start with a single MFP and add managed print when they see the numbers."], ["Do you service what you sell?", "Yes, from the nearest of seven branches, by technicians whose results are audited every year under the PROs Elite program."]], "Manufacturers we sell and service"],
    ["managed-print", "Managed print services", "Managed print", "Your in-house printing and your entire fleet of printers, managed under one agreement.", "assets/dispatch-1200.jpg", "Managed print",
     "Stop counting toner. <em>Start seeing the number.</em>",
     "Image 2000 manages your in-house printing and your entire fleet of printers: every device under one agreement, supplies and service from the nearest branch, and meter reads that match the invoice.",
     [["One agreement", "Replaces per-device contracts, retail toner and surprise repairs."], ["Supplies in a minute", "Toner and parts ordered from the support page or the portal, shipped from the nearest branch."], ["Meters collected", "Meter reads by web form or the self-service portal, so invoices match what you printed. Ask about automatic collection."], ["Audited service", "Service results audited every year against the PROs Elite 95% uptime standard."], ["Predictable billing", "One monthly invoice for the whole fleet."]],
     ["Every device on the fleet inventoried, wherever it came from", "Monitoring, with usage and service reporting", "Supplies ordered online, shipped from the nearest branch", "Lease and purchase options for the fleet the quote recommends"],
     [["Can you manage devices we did not buy from you?", "Often, yes. The quote covers your whole fleet and says which devices are worth keeping under agreement."], ["How do meter reads work?", "By the meter form on the support page or in the self-service portal, in thirty seconds. Ask your branch about automatic collection."], ["What does the quote cost?", "Nothing. Request a quote, a specialist from your nearest branch replies, and the numbers are yours whether or not you buy."]], "Manufacturers under managed print"],
    ["software-solutions", "Document management and workflow", "Software solutions", "Capture, content management, digital web forms and workflow automation with Square 9, DocuWare and FormedAI.", "assets/doc-mgmt-1200.jpg", "Software solutions",
     "Take the paper out of approvals, invoices and files, and <em>keep the audit trail</em>.",
     "Image 2000 has become a creative force in premise and cloud content management, with enterprise partners Square 9 Softworks, DocuWare and FormedAI. Capture automation, electronic content management, digital web forms and workflow automation, integrated with the multifunction devices you already have.",
     [["Capture automation", "Scans, emails, faxes and forms read by OCR, classified and indexed automatically, then put into motion."], ["Content management", "Cloud or on premise. Capture, retrieve, share, archive and manage every document with granular, user-based security."], ["Digital web forms", "Drag-and-drop forms with rules and logic, so the data arrives complete and compliant."], ["Workflow automation", "Custom document routes and approvals, designed in a browser, with automatic reminders."], ["AP automation", "Invoices captured, matched and routed for approval without the paper chase."]],
     ["Integration with QuickBooks, Dropbox, Salesforce, Dynamics and more", "Integration with your multifunction devices for scan-to-workflow", "Granular security and full visibility into business output", "Web-based designers for forms and workflows"],
     [["Cloud or on premise?", "Either. Most customers choose cloud; we will say which fits your IT and your compliance needs."], ["Which platforms do you implement?", "Square 9 Softworks, DocuWare and FormedAI, chosen for the job."], ["How long does a first workflow take?", "Ask your branch for a plan. Accounts payable is usually first because it pays back fastest."]], "Software partners"],
    ["managed-it", "Managed IT services", "Managed IT", "Fully managed IT, security, backup and cloud for a flat monthly fee, with 24/7 peace of mind.", "assets/it-1200.jpg", "Managed IT",
     "Don't leave it <em>to chance</em>.",
     "Our fully managed IT services suite is designed to provide you with 24/7 peace of mind. We monitor your systems, apply patches, protect against viruses, and make sure backups are performing, catching and fixing the little problems before they become big ones, in many cases before you know there is an issue.",
     [["Managed IT services", "Certified technicians design, maintain and monitor your entire IT infrastructure for a flat monthly fee."], ["Managed security", "Enterprise-level protection for a predictable monthly fee, kept current against new intrusion methods."], ["Business continuity and disaster recovery", "Data backed up, encrypted and stored in multiple locations, with remote server failover snapshots."], ["Cloud solutions", "Work at any time, from anywhere, on any internet-ready device."], ["IT consulting", "An IT road map, network assessments, virtualization, email and collaboration, budgeting and compliance."]],
     ["Network infrastructure, LAN, WAN and wireless", "Server, desktop and data-center virtualization", "Exchange, SharePoint and Microsoft collaboration", "Anti-malware, anti-spam, firewall and web filtering", "Disaster recovery analysis and business continuity planning", "Delivered with our managed IT partner, The Core Group"],
     [["Do we have to move everything to you?", "No. Many customers start with backup and security and add the help desk later."], ["Who does the work?", "Image 2000 delivers managed IT with its partner The Core Group. Ask your branch how the relationship works day to day."], ["How is it priced?", "A flat monthly fee for managed IT, managed security and business continuity, so IT becomes a budget line rather than a surprise."]], "Delivered with"],
    ["ucaas", "Cloud phones and UCaaS", "UCaaS", "Elevate cloud phone service, video, chat and contact center for in-office and mobile teams.", "assets/ucaas-devices-1200.jpg", "UCaaS: unified connectivity",
     "One communication experience, <em>in the office and on the road</em>.",
     "Phone service, video conferencing, chat and file management for every employee through Image 2000's Elevate UCaaS solutions. A desktop app, a mobile app and pre-configured desk phones, with Microsoft Teams integration and single sign-on.",
     [["High reliability", "Elevate delivers 99.999% reliability, so you are never out of touch."], ["Lower costs", "No phone system hardware to buy, install, manage, upgrade or replace."], ["Increased flexibility", "Collaborate from anywhere, on any device."], ["Simplified management", "Elevate scales with the needs of your business."], ["Business continuity", "Stay connected even when the power goes out."]],
     ["Desktop app for calls, chat, video and file sharing on Mac or PC", "Mobile app for Apple and Android", "Pre-configured desk phones that work wherever they are plugged in", "Microsoft Teams collaboration hub and single sign-on with Microsoft 365", "Integrated SMS and advanced call routing", "Contact Center: calls, web chat, email and SMS in one application, with real-time dashboards"],
     [["Can we keep our numbers?", "Yes. Ask for the phone assessment and we cover porting, phones and timing."], ["Does it work with Teams?", "Yes. Elevate manages chat, file sharing and video conferencing inside Teams, with single sign-on using your Microsoft 365 credentials."], ["What is the Contact Center?", "Advanced call handling for teams that serve customers: queues, skills, multi-site and remote agents, post-call surveys and CRM integration, inside Elevate."]], "Powered by"],
    ["production-print", "Production print, wide format and mailing", "Production and mailing", "RISO duplicators, production print, KIP and Canon wide-format, and Formax mailing equipment.", "assets/production-1200.jpg", "Production, wide format and mailing",
     "Print rooms that hit the deadline <em>outsourcing cannot</em>.",
     "In-house production print and RISO high-speed duplicators for organizations that print every day, KIP and Canon large-format for plans and posters, and Formax folders and inserters for the mailroom. Control costs, print on demand, keep confidential work in the building.",
     [["Control costs", "Know the cost per piece, and stop paying rush fees."], ["On-demand printing", "Print the hundred you need today, not the thousand you might need."], ["Confidentiality", "Financials, exams and mailings never leave the building."], ["Wide format in house", "Plans, drawings, posters and signage the same day."], ["Mailroom throughput", "Folding, inserting and sealing at machine speed."]],
     ["RISO ComColor inkjet and RZ duplicators", "Production print with inline finishing", "KIP and Canon large-format printers and scanners", "Formax folding, inserting and mailing equipment", "Operator training and priority service under agreement"],
     [["What volume justifies production print?", "Bring your outsourced invoices to the quote. The comparison usually answers it."], ["Do you sell RISO?", "Yes. RISO duplicators and ComColor printers are in the catalogue, and Image 2000 is one of the dealers people find when they search for them."], ["Can you train our operator?", "Yes, on the day of install, and again whenever staff changes."]], "Manufacturers"],
    ["water", "Bottleless water coolers", "Water", "Waterlogic bottleless drinking water, ice and sparkling water, with a free trial.", "assets/water-cooler-1200.jpg", "Waterlogic bottleless water",
     "Clean, great-tasting water, <em>without the bottles</em>.",
     "Switch to bottleless drinking water for clean, great-tasting water, ice and sparkling water at a fraction of the cost of bottled water and delivery services. Ask about the free trial: Image 2000 installs a bottleless system at no cost and no obligation.",
     [["Free trial", "A bottleless system installed at no cost and no obligation, so you can see why it is popular."], ["Filtered from your supply", "No jugs to lift, store or run out of."], ["Ice and sparkling", "Still, sparkling and ice from one unit."], ["Serviced with your copier", "One vendor, one call, one technician."]],
     ["Waterlogic bottleless coolers for offices, clinics, schools and more", "Filter changes on a schedule", "Ask about rental and purchase options", "Supplies ordered from the support page"],
     [["Why bottleless?", "No jugs to lift, store or run out of, and filtered water from your own building supply at a fraction of the cost of bottled delivery."], ["How does the free trial work?", "We install one of our bottleless systems at no cost and no obligation. Request the trial from the contact page."]], "Partner"],
]
SERVICE_INDEX = {s[0]: s for s in SERVICES}
SERVICE_DETAIL_IMAGE = {"office-technology": "assets/printer-1200.jpg", "managed-print": "assets/mps-2-1200.jpg", "software-solutions": "assets/gso-office-1200.jpg", "managed-it": "assets/it-1200.jpg", "ucaas": "assets/hero-1200.jpg", "production-print": "assets/wide-format-real-1200.jpg", "water": "assets/water-cooler-1200.jpg"}
SERVICE_PARTNERS = {"office-technology": ["Kyocera", "Copystar", "Sharp", "Toshiba", "Lexmark", "Brother", "HP", "KIP", "Canon", "Kodak Alaris", "Sharp NEC Displays"], "managed-print": ["Kyocera", "Copystar", "Sharp", "Toshiba", "Lexmark", "Brother", "HP"], "software-solutions": SOFTWARE_PARTNERS, "managed-it": ["The Core Group"], "ucaas": ["Elevate", "Microsoft Teams"], "production-print": ["RISO", "KIP", "Canon", "Formax"], "water": ["Waterlogic"]}
SUPPORT = "support.html"


def desc(text, n=155):
    """Meta description: whole sentences until the next would pass n characters."""
    text = re.sub(r"<[^>]+>", "", text)
    out = ""
    for sent in re.split(r"(?<=[.!?])\s+", text.strip()):
        if not sent:
            continue
        cand = (out + " " + sent).strip()
        if len(cand) > n:
            break
        out = cand
    return out or text[:n]


def brief(text, n=150):
    text = re.sub(r"<[^>]+>", "", text)
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(" ", 1)[0]
    return cut.rstrip(",.;:") + "."


LEADFORM = {"type": "leadform", "alt": True, "id": "quote", "heading": "Request a quote", "body": "Tell us what you print, what you run and where you are. A specialist from the nearest branch replies with numbers, not a pitch.", "submit": "Request a quote", "note": "A person from your nearest branch replies, not an autoresponder."}
QUOTE = {"label": "Request a quote", "href": "contact.html"}
SECOND = {"label": "Estimate your print spend", "href": "cost-calculator.html"}
SUPPORT_LINKS = [["Request service", SUPPORT + "#request"], ["Submit a meter read", SUPPORT + "#meters"], ["Order supplies", SUPPORT + "#supplies"], ["Pay an invoice", PAY_URL], ["Self-service portal", SUPPORT + "#portal"], ["Screen share with support", SUPPORT + "#screenshare"]]

WHEEL_ITEMS = [[s[1], s[3], f"services/{s[0]}.html", s[2]] for s in SERVICES]

FLOW = {"type": "flow", "id": "flow", "eyebrow": "How an engagement runs", "heading": "Four stages, and every one of them hands you something",
    "intro": "Click a stage. Nothing here is a sales step dressed up as a process; each one leaves you with something you keep.",
    "steps": [
        {"label": "Quote", "when": "Week 1", "summary": "Your fleet, your volume, two prices.", "title": "A specialist counts what you have and prices what you need",
         "body": "Every device located, your volume and your current invoices in hand, and a conversation with the people who print most. The quote prices lease and purchase side by side for your real usage, and the numbers are yours whether or not you buy.",
         "receive": ["Fleet inventory and volume", "Lease and purchase side by side", "The recommendation, in writing"]},
        {"label": "Install and connect", "when": "A date you choose", "summary": "Networked and trained the same visit.", "title": "Devices arrive on the day you chose",
         "body": "On the network the day they arrive, every user trained before the technician leaves, monitoring switched on where the device supports it, the first supplies on the shelf.",
         "receive": ["Install and training completed on site", "Drivers and manuals linked on the support page", "Meter collection set up"]},
        {"label": "Support", "when": "Ongoing", "summary": "Service, supplies, meters and invoices, one click deep.", "title": "The support page is the fast lane",
         "body": "Request service, submit a meter read, order supplies, pay an invoice by card, open the self-service portal or start a screen share. Each one under a minute, each one answered by a person at the nearest branch.",
         "receive": ["Service requests tracked to resolution", "Supplies ordered online, shipped from the nearest branch", "Service results audited yearly under PROs Elite"]},
        {"label": "Review", "when": "On schedule", "summary": "What moved, what to change, then back to stage one.", "title": "A look at what moved",
         "body": "Usage, uptime and what changed since the last look, then adjustments if the business moved: a device relocated, a workflow added, a branch opened. The cycle starts again from a known number.",
         "receive": ["Usage and service history, explained", "Adjustments to the plan", "A fresh baseline for the next period"]}]}

FLEET = {"type": "fleet", "id": "fleet", "heading": "Everything the office runs on", "intro": "Every device family Image 2000 sells and services. Generated product renders for the preview; your real models replace them.",
    "items": [
        {"title": "Multifunction copiers", "band": "Workgroup to department", "brands": "Kyocera, Copystar, Sharp, Toshiba, Lexmark", "image": "assets/fleet/mfp.png", "bullets": ["Print, scan, copy, fax", "Secure release and scan to workflow"], "href": "services/office-technology.html", "label": "Office technology"},
        {"title": "Desktop printers", "band": "Desk and small team", "brands": "Brother, HP, Lexmark, Kyocera", "image": "assets/fleet/printer.png", "bullets": ["Color and mono", "Joins a managed print agreement"], "href": "services/managed-print.html", "label": "Managed print"},
        {"title": "Wide format", "band": "Plans, posters, signage", "brands": "KIP, Canon", "image": "assets/fleet/wide-format.png", "bullets": ["Stop outsourcing plan sets", "Technical and graphics media"], "href": "services/production-print.html", "label": "Wide format"},
        {"title": "Production and duplicators", "band": "High volume, inline finishing", "brands": "RISO, Kyocera, Sharp", "image": "assets/fleet/production.png", "bullets": ["Booklets, stapling, folding", "RISO speed for packets and mailings"], "href": "services/production-print.html", "label": "Production print"},
        {"title": "Mailing equipment", "band": "Mailroom", "brands": "Formax", "image": "assets/fleet/postage.png", "bullets": ["Folder-inserters and sealers", "Serviced with your copier"], "href": "services/production-print.html", "label": "Mailing"},
        {"title": "Bottleless water", "band": "Breakroom", "brands": "Waterlogic", "image": "assets/water-cooler-1200.jpg", "bullets": ["Still, sparkling and ice", "Free trial"], "href": "services/water.html", "label": "Water"}]}

SEAL = {"type": "seal", "id": "seal", "eyebrow": "What every Image 2000 customer gets", "heading": "Not a slogan. A list you can check.",
    "intro": "Each line is on image-2000.com today, with a year and a source. Nothing here is aspirational.",
    "items": [["1992", "Founder-owned since 1992", "Rich Campbell and Joe Blatchford still own and run the company they started in Valencia."],
              ["100", "One of about 100 PROs Elite dealers", "Only one dealer in any market earns it. Image 2000 has, every year since 2016."],
              ["95%", "Audited uptime above 95%", "The PROs Elite standard, monitored and audited by PROs, not reported by us."],
              ["7", "Seven branches, one number", "Valencia, Los Angeles, Orange County, the Inland Empire, Bakersfield, Fresno and Las Vegas. Local dispatch, parts and warehousing."],
              ["11", "An eleven-manufacturer portfolio", "The recommendation fits the job, not the badge."],
              ["A", "BBB accredited, A rating", "Accredited by the Better Business Bureau."],
              ["12th", "Largest Sharp dealer in the country", "By ENX Magazine's 2024 Elite Dealers profile, with the Hyakuman Kai Elite Award five years in a row and Kyocera Platinum Partner status."],
              ["1", "One partner for the whole office", "Copiers, print, workflow software, IT, phones and water from one company, one number."]],
    "source": "Sources: image-2000.com home, why, awards, about and locations pages, 8 September 2026; PROs Elite program description as published there; ENX Magazine Elite Dealers 2024 profile of Image 2000."}

BEFORE_AFTER = {"type": "beforeafter", "id": "ba", "eyebrow": "One partner", "heading": "Drag to see what changes when the office has one number to call",
    "before": {"eyebrow": "Today, in most offices", "title": "Six vendors, six contracts", "body": "Nobody owns the whole picture, so nobody sees the cost.",
               "items": ["A copier company, a printer reseller and a toner site", "An IT firm that blames the copier company", "A phone company on a five-year contract", "A water delivery every other Tuesday", "Five numbers to call and nobody who knows your name", "Toner ordered in a hurry at retail"]},
    "after": {"eyebrow": "With Image 2000", "title": "One partner, one number", "body": "Copiers to water, serviced by the same people from the nearest branch.",
              "items": ["Copiers, printers, wide format and production under one agreement", "Document workflow and managed IT from the same team", "Elevate cloud phones, no hardware to own", "Waterlogic bottleless water, serviced with the copier", "800-481-2250 reaches all seven branches", "Supplies ordered in a minute from the support page"]}}

HOTSPOTS = {"type": "hotspots", "id": "office", "eyebrow": "The whole office", "heading": "Six lines, one floor plan", "intro": "Click a number. Everything an office runs on, and the Image 2000 page for each.",
    "image": "assets/isometric-office-seven-lines-1600.jpg", "image_w": 1600, "image_h": 893, "alt": "An overhead illustration of an office with a copier room, a break room, a server room, a mailroom and desks",
    "items": [
        {"x": 27, "y": 46, "k": "Copiers and production", "title": "The copier room", "body": "Multifunction devices and a production system with inline finishing, on one agreement.", "href": "services/office-technology.html", "label": "Office technology"},
        {"x": 47, "y": 21, "k": "Bottleless water", "title": "The break room", "body": "Waterlogic still, sparkling and ice, serviced on the same visit as the copier. Free trial.", "href": "services/water.html", "label": "Water"},
        {"x": 82, "y": 14, "k": "Managed IT", "title": "The server room", "body": "Monitoring, patching, backup, security and cloud for a flat monthly fee.", "href": "services/managed-it.html", "label": "Managed IT"},
        {"x": 73, "y": 58, "k": "Mailing and wide format", "title": "The mailroom", "body": "Formax folder-inserters, RISO duplicators and KIP wide-format, in house.", "href": "services/production-print.html", "label": "Production and mailing"},
        {"x": 16, "y": 58, "k": "Cloud phones", "title": "The desks", "body": "Elevate desk phones, desktop and mobile apps, Teams integration. No phone system to own.", "href": "services/ucaas.html", "label": "UCaaS"},
        {"x": 64, "y": 71, "k": "Document workflow", "title": "Scan to workflow", "body": "Every MFP scans straight into Square 9 or DocuWare: accounts payable, HR, records.", "href": "services/software-solutions.html", "label": "Software solutions"}]}

STORY3D = {"type": "story3d", "id": "device", "alt": False, "eyebrow": "Take a closer look", "heading": "Walk around one before it arrives",
    "intro": "Scroll, and the device turns to the part being described. A generated Sharp-style stand-in for the preview; the manufacturers' product models replace it in the build.",
    "poster": "assets/fleet/mfp.png", "model": "assets/fleet/mfp.glb", "alt": "A Sharp-style multifunction copier that turns as you scroll", "hint": "Drag to turn",
    "cta": {"label": "See office technology", "href": "services/office-technology.html"},
    "steps": [
        {"k": "The panel", "title": "One screen for print, scan and release", "orbit": "28deg 72deg 100%", "body": "A tilting color touchscreen where people print, copy, scan and release held jobs with a badge or code. Scan to email or straight into Square 9 or DocuWare from the same screen.", "points": ["Secure print release", "Scan to workflow", "Trained on install day"]},
        {"k": "The feeder", "title": "Stacks in, indexed files out", "orbit": "0deg 40deg 108%", "body": "Mixed paper goes in the top. Named, indexed files land in the right folder or workflow, so accounts payable, HR and records stop living in filing cabinets.", "points": ["Duplex scanning", "OCR into your document management", "Routing rules set up by Image 2000"]},
        {"k": "The paper path", "title": "Trays sized to how the office prints", "orbit": "-62deg 80deg 104%", "body": "Under a managed print agreement, Supplies come from the nearest branch and meter reads feed the invoice, so what you pay matches what you printed.", "points": ["Supplies ordered in a minute", "Meter reads by form or portal", "One agreement for the fleet"]},
        {"k": "The service side", "title": "Serviced to an audited standard", "orbit": "200deg 76deg 108%", "body": "Image 2000 is a PROs Elite dealer, which means its service results are monitored and audited every year against a 95% uptime standard, and the call goes to the nearest of seven branches.", "points": ["Audited service results", "Local dispatch, parts and warehousing", "Dispatched from the nearest branch"]}]}

HERO_LAYERED = {"type": "hero-layered", "id": "hero", "eyebrow": "Valencia, California. Founder-owned since 1992.",
    "heading": "Office technology from the dealer <em>recognized for service year after year</em>.",
    "subhead": "Copiers and printers, managed print, document workflow, managed IT, cloud phones and bottleless water. One West Coast partner, seven branches, one number to call.",
    "primary": QUOTE, "secondary": SECOND,
    "image": "assets/hq-plate-dark-2100.jpg", "image_w": 2100, "image_h": 891, "video": "assets/hero-valencia.mp4",
    "model": "assets/fleet/mfp.glb", "poster": "assets/fleet/mfp.png", "model_alt": "A Sharp-style multifunction copier, rotating. Drag to turn it.",
    "stats": [["1992", "Founder-owned since"], ["7", "Branches, California and Nevada"], ["11", "Manufacturers in the portfolio"], ["2016", "PROs Elite certified every year since"]],
    "card_a": {"eyebrow": "Start here", "title": "Request a quote", "body": "Your fleet, your volume, lease and purchase side by side. The numbers are yours either way.", "items": ["Every device counted", "Lease and purchase on one page", "A person from the nearest branch replies"], "href": "contact.html", "label": "Request a quote"},
    "card_b": {"eyebrow": "Already a customer?", "title": "The fast lane", "body": "Under a minute each. A person replies.", "links": SUPPORT_LINKS[:4]},
    "note": "The film is a generated push-in on Image 2000's own Valencia headquarters. Other preview photography and the 3D device are generated and labelled as such."}


def service_page(slug, navlabel, short, one, image, eyebrow, heading, subhead, benefits, included, faq, partner_caption):
    display = short.lower() if short not in ("UCaaS",) else short
    secs = [
        {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": heading, "subhead": subhead, "primary": QUOTE, "secondary": {"label": "Request service", "href": SUPPORT + "#request"},
         "image": image, "image_alt": navlabel, "image_w": 1200, "image_h": 800},
        {"type": "partners", "caption": partner_caption, "items": SERVICE_PARTNERS[slug]},
        {"type": "cards", "alt": True, "eyebrow": "What changes", "heading": f"What changes with Image 2000 {display}", "items": benefits},
        {"type": "detail", "eyebrow": "What is included", "heading": "What you get", "body": "The list below is what arrives, and when. Nothing on it is an add-on.", "bullets": included, "image": SERVICE_DETAIL_IMAGE.get(slug, image), "image_alt": navlabel, "flip": True},
    ]
    if slug == "managed-print":
        secs.insert(3, {"type": "process", "eyebrow": "How managed print works", "heading": "Three stages you can see on your invoice", "stages": [
            ["Quote", "Produces: a fleet inventory and lease and purchase prices, yours to keep."],
            ["Monitor and supply", "Produces: supplies and service from one agreement, meter reads that match the invoice."],
            ["Review", "Produces: usage and service history explained, and a plan adjusted if the business moved."]]})
        secs.append({"type": "comparison", "heading": "Lease or buy?", "intro": "The quote prices both for your real volume. Here is how they usually compare.",
                     "columns": [{"label": "Lease", "recommended": True}, {"label": "Buy"}],
                     "rows": [["Best for", "Steady volume, a fleet kept current", "Stable volume, long device life"],
                              ["Term", "36 to 60 months, typically", "None"],
                              ["Up-front cost", "Low", "Highest"],
                              ["Lifetime cost", "Moderate", "Lowest if the device runs for years"],
                              ["Technology refresh", "Built in at end of term", "When you buy again"],
                              ["Service and supplies", "Managed agreement, or separate", "Managed agreement, or separate"]],
                     "note": "Terms and rates are set in the quote. Nothing here is a price."})
    if slug == "office-technology":
        secs.insert(3, FLEET)
    if slug == "software-solutions":
        secs.insert(3, {"type": "tabs", "id": "capabilities", "eyebrow": "Four capabilities", "heading": "Capture, manage, form, route",
            "items": [
                {"label": "Capture", "title": "Capture automation", "body": "Streamline the way your business captures critical information. Scans, emails, fax, digital forms and raw data are captured, classified, validated and transformed into usable information through automated workflows.", "bullets": ["Advanced data extraction with several OCR technologies", "Documents identified by predefined attributes and matched to the right template", "Integration with your multifunction devices"], "image": "assets/doc-mgmt-1200.jpg", "image_alt": "A scanned document being indexed", "href": "contact.html", "link_label": "Ask about capture"},
                {"label": "Manage", "title": "Electronic content management", "body": "Strategies, methods and tools for centrally storing, managing and sharing all content in an organization, paper and digital, in the cloud or on premise.", "bullets": ["Integration with QuickBooks, Dropbox, Salesforce and Dynamics", "Granular, user-based security and auditing", "Capture, retrieve, share, archive and manage from one place"], "image": "assets/gso-office-1200.jpg", "image_alt": "An office team working with digital files", "href": "contact.html", "link_label": "Ask about content management"},
                {"label": "Forms", "title": "Digital web forms", "body": "Intuitive web forms that eliminate repetitive data entry while ensuring corporate and governmental compliance, gathering only the relevant data.", "bullets": ["Drag-and-drop designer for text boxes, drop-downs and images", "Rules and logic that change the layout based on selections", "Real-time engagement with your audience"], "image": "assets/it-1200.jpg", "image_alt": "A web form on a laptop", "href": "contact.html", "link_label": "Ask about web forms"},
                {"label": "Route", "title": "Workflow automation", "body": "Customized document routes that fit your business, so approval processes and daily routines run themselves and can be monitored from anywhere.", "bullets": ["Web-based graphical designer", "Automatic email reminders on your schedule", "Approval processes tracked end to end"], "image": "assets/mps-2-1200.jpg", "image_alt": "Documents moving through an approval workflow", "href": "contact.html", "link_label": "Ask about workflow"}]})
    if slug == "ucaas":
        secs.insert(3, {"type": "cards", "eyebrow": "Three ways to answer", "heading": "Desktop, mobile and desk phone, one service", "items": [["Desktop app", "Place calls, chat, host or join a video conference and share files from a Mac or PC."], ["Mobile app", "Switch your workspace to any Apple or Android device."], ["Desk phone", "Pre-configured phones connect to Elevate wherever they are plugged in."]]})
        secs.append({"type": "cards", "alt": True, "eyebrow": "Contact Center and Elevate", "heading": "For teams that serve customers all day", "intro": "Contact Center improves customer interactions for businesses of all sizes.", "items": [["One application", "Calls, web chat, email and SMS handled in a single application, with employee collaboration alongside."], ["Multi-site and remote", "Support multiple locations and remote employees from one portal, anywhere, any time."], ["Real-time dashboards", "Service levels and team performance by queue, team or employee, with historical reports."], ["Outreach and surveys", "Outbound dialing, campaign capabilities and post-call surveys, integrated with CRM and WFM systems."]]})
    if slug == "water":
        secs.insert(3, {"type": "checklist", "id": "water-check", "alt": True, "eyebrow": "What's in your water?", "heading": "We should talk if any of these is true in your workplace", "intro": "Check what sounds familiar.",
            "items": ["Someone lifts a five-gallon jug onto a cooler every week", "The delivery comes whether you need it or not", "The break room runs out on the busiest day", "Visitors, patients or students drink from a tap nobody has tested", "Sparkling water comes in cans, by the case", "Ice comes from a machine nobody cleans"],
            "messages": ["Check what sounds familiar.", "One is normal.", "Two is worth a free trial.", "Three or more, and bottleless pays for itself. Ask for the trial."], "cta_label": "Request a free trial", "cta_href": "contact.html"})
    secs += [
        {"type": "testimonials", "alt": True, "heading": "What customers say", "items": [t[:3] for t in TESTIMONIALS]},
        {"type": "faq", "heading": f"Questions we get about {display}", "items": faq},
        dict(LEADFORM, alt=True),
    ]
    return {"file": f"services/{slug}.html", "title": f"{navlabel} | {CLIENT}", "description": desc(subhead), "crumbs": [["Home", "index.html"], ["Services", "what-we-do.html"], [short, f"services/{slug}.html"]], "sections": secs}


BRANDS = [  # slug, name, group, one-line, body, catalogue label
    ["sharp", "Sharp", "Copiers and printers", "Hyakuman Kai Elite dealer, 2021 through 2024, and the 12th largest Sharp dealer in the country.", "Sharp multifunction copiers, printers and production systems, plus Sharp NEC displays. Image 2000 has been recognized by Sharp with the Hyakuman Kai Elite Award four years running and is the 12th largest Sharp dealer in the United States, so parts, training and escalation paths are deep.", "Sharp catalogue"],
    ["kyocera", "Kyocera", "Copiers and printers", "FY26 Platinum Partner. ECOSYS and TASKalfa devices with long-life components.", "Kyocera ECOSYS printers and TASKalfa multifunction systems, known for long-life drums and low running costs. Image 2000 is a Kyocera FY26 Platinum Partner, with Platinum Platter and Gold Partner recognitions before it.", "Kyocera catalogue"],
    ["toshiba", "Toshiba", "Copiers and printers", "e-STUDIO multifunction systems.", "Toshiba e-STUDIO color and mono multifunction systems for workgroups and departments.", "Toshiba catalogue"],
    ["lexmark", "Lexmark", "Copiers and printers", "A4 printers and multifunction devices for offices and branches.", "Lexmark printers and A4 multifunction devices for offices, branches and retail counters.", "Lexmark catalogue"],
    ["hp", "HP", "Copiers and printers", "LaserJet, PageWide and DesignJet.", "HP LaserJet and PageWide printers and multifunction devices, ScanJet scanners and DesignJet wide format.", "HP catalogue"],
    ["brother", "Brother", "Copiers and printers", "Desktop printers and compact multifunction devices.", "Brother desktop printers and compact multifunction devices for desks and small teams.", "Brother catalogue"],
    ["kip", "KIP", "Wide format", "Wide format print systems for technical documents.", "KIP wide format systems for plan sets and technical documents in architecture, engineering and construction.", "KIP catalogue"],
    ["canon-large-format", "Canon large format", "Wide format", "imagePROGRAF large format printers.", "Canon imagePROGRAF large format printers for technical and graphics output.", "Canon large format catalogue"],
    ["kodak-alaris", "Kodak Alaris", "Scanning", "Document scanners for capture at volume.", "Kodak Alaris document scanners, from desktop to production capture, feeding DocuWare and Square 9 workflows.", "Kodak Alaris catalogue"],
    ["riso", "RISO", "Production", "High-speed inkjet for volume at low cost per page.", "RISO ComColor high-speed inkjet systems for forms, mailers and volume printing at a low cost per page.", "RISO catalogue"],
    ["formax", "Formax", "Mailing", "Folder inserters and mailroom equipment.", "Formax folder inserters, letter openers, pressure sealers and mailroom equipment.", "Formax catalogue"],
    ["waterlogic", "Waterlogic", "Breakroom", "Bottleless water coolers with a free trial.", "Waterlogic bottleless water, ice and sparkling water dispensers, installed free on trial.", "Waterlogic catalogue"],
    ["sharp-nec", "Sharp NEC displays", "Displays", "Commercial displays for lobbies, classrooms and meeting rooms.", "Sharp NEC commercial displays and interactive boards for lobbies, classrooms, meeting rooms and signage.", "Sharp NEC catalogue"],
]


def brand_page(slug, name, group, one, body, label):
    img = {"Wide format": "assets/wide-format-1200.jpg", "Scanning": "assets/doc-mgmt-1200.jpg", "Production": "assets/production-1200.jpg", "Mailing": "assets/mailroom-printer-1200.jpg", "Breakroom": "assets/water-cooler-1200.jpg", "Displays": "assets/hq-1200.jpg"}.get(group, "assets/printer-1200.jpg")
    return {"file": f"brands/{slug}.html", "title": f"{name} from Image 2000 | {group}", "description": desc(f"{one} {body}"),
            "crumbs": [["Home", "index.html"], ["Brands", "brands.html"], [name, f"brands/{slug}.html"]],
            "sections": [
                {"type": "hero", "layout": "split", "eyebrow": f"Brands: {name}", "heading": f"{name}, <em>sold and serviced locally</em>.", "subhead": body, "primary": {"label": "Request a quote", "href": "contact.html"}, "secondary": {"label": label, "href": "https://www.image-2000.com/product-catalogs"}, "image": img, "image_alt": name, "image_w": 1200, "image_h": 800},
                {"type": "cards", "alt": True, "heading": f"Why buy {name} from Image 2000", "items": [["Recommended, not pushed", "Eleven manufacturers means the badge is chosen for the job."], ["Local service", "Seven branches with local dispatch, parts and warehousing."], ["Audited results", "PROs Elite certified every year since 2016."], ["Lease, rent or buy", "Priced side by side with five leasing partners."]]},
                {"type": "faq", "heading": f"Questions about {name}", "items": [
                    [f"Which {name} equipment does Image 2000 place?", f"{body} The specialist matches the model to the volume, finishing and software the office runs."],
                    [f"Where can I see {name} equipment?", "At any of the seven branches: Santa Clarita, Los Angeles, Orange County, the Inland Empire, Bakersfield, Fresno and Las Vegas. The nearest branch can also demonstrate on site."],
                    [f"How is {name} equipment priced?", "Lease, rent or buy, priced side by side with five leasing partners, with supplies and service on one agreement if the device comes under managed print."],
                    ["Where are the drivers?", "Sharp and Kyocera downloads are linked from the customer support page; ask the branch for others."],
                    [f"Does Image 2000 stock {name} supplies and parts?", f"Yes. Toner and parts for the {name} devices it places are warehoused at the branches, and supply orders and meter reads go through the customer support page or the branch."],
                    ["Can it join managed print?", "Yes. Any device Image 2000 places can come under one agreement, with supplies, service and reporting on one invoice."]]},
                LEADFORM]}




def industry_page(slug, name, image, one, body, bullets, faq):
    return {"file": f"industries/{slug}.html", "title": f"Office technology for {name.lower()} | {CLIENT}", "description": desc(one + " " + body),
            "crumbs": [["Home", "index.html"], ["Industries", "industries.html"], [name, f"industries/{slug}.html"]],
            "sections": [
                {"type": "hero", "layout": "split", "eyebrow": name, "heading": f"Office technology built around how <em>{name.lower()}</em> works.", "subhead": one, "primary": QUOTE, "secondary": SECOND, "image": image, "image_alt": name, "image_w": 1200, "image_h": 800},
                {"type": "detail", "alt": True, "eyebrow": "What we do here", "heading": f"How Image 2000 works with {name.lower()}", "body": body, "bullets": bullets},
                {"type": "services", "heading": "The lines that matter most here", "intro": "Each has its own page.", "items": [[SERVICE_INDEX[s][1], SERVICE_INDEX[s][3], f"services/{s}.html"] for s in ("office-technology", "managed-print", "software-solutions", "ucaas")]},
                {"type": "testimonials", "alt": True, "heading": "What customers say", "items": [t[:3] for t in TESTIMONIALS]},
                {"type": "faq", "heading": f"Questions from {name.lower()}", "items": list(faq) + [[f"Where does Image 2000 serve {name.lower()} customers?", "From seven branches in Santa Clarita, Los Angeles, Orange County, the Inland Empire, Bakersfield, Fresno and Las Vegas, with technicians dispatched from the nearest one and one agreement covering every site."]]},
                LEADFORM]}


def location_page(slug, label, a1, a2, phone, phone_href, lat, lon, region, city):
    hq = slug == "valencia"
    eyebrow = "Headquarters" if hq else f"{city} branch"
    state = "NV" if "NV" in a2 else "CA"
    return {"crumbs": [["Home", "index.html"], ["Locations", "locations.html"], [label, f"locations/{slug}.html"]], "file": f"locations/{slug}.html",
            "title": f"Copier Sales, Lease and Service in {city}, {state} | {CLIENT}",
            "description": f"Image 2000 in {city}: copier and printer sales, lease and repair, managed print, document workflow, managed IT and cloud phones for businesses across {region}. {a1}, {a2}. {phone}.",
            "schema": [{"@context": "https://schema.org", "@type": "LocalBusiness", "@id": f"https://www.image-2000.com/locations/{slug}#branch", "name": f"Image 2000 {label}",
                        "parentOrganization": {"@id": "https://www.image-2000.com/#organization"}, "image": "https://image2000.vercel.app/assets/hq-1200.jpg",
                        "telephone": "+1-" + phone, "url": f"https://www.image-2000.com/locations/{slug}",
                        "address": {"@type": "PostalAddress", "streetAddress": a1, "addressLocality": a2.split(",")[0], "addressRegion": state, "postalCode": a2.split()[-1], "addressCountry": "US"},
                        "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon},
                        "areaServed": region, "sameAs": [LINKEDIN]}],
            "sections": [
                {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": f"<em>{city}</em> copiers, managed print and IT, serviced locally.",
                 "subhead": f"The Image 2000 {label} branch serves {region} with sales, local service dispatch, parts and supplies. Call the branch, or {PHONE} reaches all seven.",
                 "primary": {"label": f"Call {phone}", "href": phone_href}, "secondary": QUOTE,
                 "image": "assets/hq-1200.jpg" if hq else "assets/dispatch-1200.jpg", "image_alt": "The Image 2000 headquarters in Valencia, California" if hq else "A technician servicing an office copier", "image_w": 1200, "image_h": 800,
                 "badge": {"value": "Local", "label": "Dispatch, parts and warehousing at this branch"}},
                {"type": "cards", "alt": True, "eyebrow": f"In {city}", "heading": f"What the {label} branch does", "items": [
                    ["Copier and printer sales and lease", f"Kyocera, Sharp, Toshiba, Lexmark, Brother and HP devices for {city} offices, installed and networked by the local team."],
                    ["Copier and printer repair", "Local dispatch by technicians whose results are audited every year under the PROs Elite program."],
                    ["Managed print", "Your in-house printing and your entire fleet of printers under one agreement."],
                    ["Document workflow and IT", "Square 9 and DocuWare workflows, managed IT and cloud phones from the same team."],
                    ["Production, wide format and mailing", "RISO, KIP, Canon and Formax equipment for print rooms and mailrooms."],
                    ["Bottleless water", "Waterlogic coolers with a free trial, serviced on the same visit."]]},
                {"type": "locations", "heading": f"Visit or call the {label} branch", "intro": f"{a1}, {a2}. Call the branch for hours.", "items": [[label, a1, a2, phone, phone_href]]},
                {"type": "testimonials", "alt": True, "heading": "What customers say", "items": [t[:3] for t in TESTIMONIALS]},
                {"type": "faq", "heading": f"Questions we get in {city}", "items": [
                    [f"Do you serve businesses outside {city}?", f"Yes. The {label} branch covers {region}, and customers with offices elsewhere in California or Nevada are served from the nearest of seven branches."],
                    ["How fast can you get a technician to us?", "From this branch, with local parts and warehousing. Image 2000 is a PROs Elite dealer, so its service results are audited every year against a 95% uptime standard. Ask the branch for the response terms of your agreement, in writing."],
                    ["Can we lease a copier locally?", "Yes. The quote prices lease and purchase side by side for your real volume."]]},
                {"type": "leadform", "id": "quote", "heading": f"Request a quote in {city}", "body": "A specialist from the branch counts what you have and prices what you need.", "submit": "Request a quote", "note": "A person from the branch replies, not an autoresponder."},
            ]}


def build():
    brand = {
        "accent": "#384AD3", "ink_secondary": "#0B1B3A", "chrome": "dark", "chrome_bg": "#0B1B3A",
        "type_from": {"Quantum Showcase": "Quantum Clean"},  # Shawn, 2026-09-08: Clean's typefaces on the Showcase layout
        "logo": "assets/image-2000-logo-white.png", "logo_alt": "Image 2000", "logo_w": 1200, "logo_h": 225,
        "logo_note": "White-on-navy variant made for the preview header from the navy and light-blue wordmark with the line 'Technology, Document Management, Consulting'. Fetched from the live site as a JPEG on white and cut out for the preview. Ask for the vector.",
        "phone": PHONE, "phone_href": PHONE_HREF, "email": "",
        "utility": [{"label": "Customer support", "href": SUPPORT}, {"label": "Request service", "href": SUPPORT + "#request"}, {"label": "Meter reads", "href": SUPPORT + "#meters"}, {"label": "Order supplies", "href": SUPPORT + "#supplies"}, {"label": "Pay an invoice", "href": PAY_URL}],
        "cta": QUOTE,
        "sticky": {"primary": "Request a quote", "primary_href": "contact.html", "secondary": "Call Image 2000", "secondary_href": PHONE_HREF},
        "launcher": {"label": "Already a customer?", "eyebrow": "Customer support", "title": "What do you need today?", "links": SUPPORT_LINKS, "note": "A person from the nearest branch replies. Under an Image 2000 agreement your call is dispatched locally.", "phone": PHONE, "phone_href": PHONE_HREF},
        "social": {"linkedin": LINKEDIN, "instagram": "https://www.instagram.com/image2000inc/", "facebook": "https://www.facebook.com/Image-2000-Inc-127054597339857/"},
        "tagline": "Founder-owned in Valencia, California since 1992. Copiers, print, workflow, IT, phones and water for offices across California and Nevada, from seven branches.",
        "footer_columns": [
            {"title": "Services", "links": [[s[2], f"services/{s[0]}.html"] for s in SERVICES] + [["All services", "what-we-do.html"]]},
            {"title": "Customer support", "links": SUPPORT_LINKS + [["Drivers and manuals", SUPPORT + "#drivers"]]},
            {"title": "Industries", "links": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES] + [["Cost calculator", "cost-calculator.html"]]},
            {"title": "Company", "links": [["Why Image 2000", "why-image-2000.html"], ["Brands", "brands.html"], ["About", "about.html"], ["Locations", "locations.html"], ["Careers", "careers.html"], ["FAQ", "faq.html"], ["Contact", "contact.html"]]},
        ],
        "legal": [["Privacy policy", "https://www.image-2000.com/privacypolicy"]],
    }
    schema = {"org_name": "Image 2000, Inc.", "org_url": "https://www.image-2000.com",
              "org_logo": "https://static.wixstatic.com/media/f6aae5_ad6a954630594047b870865f2c60d3d1~mv2.jpg",
              "org_description": "Founder-owned office technology and managed services dealer headquartered in Valencia, California, serving Southern California, the Central Valley and Las Vegas from seven branches since 1992. Copiers and printers, managed print, document management and workflow, managed IT, UCaaS and bottleless water.",
              "sameAs": [LINKEDIN, "https://www.instagram.com/image2000inc/", "https://www.facebook.com/Image-2000-Inc-127054597339857/", "https://www.bbb.org/us/ca/santa-clarita/profile/office-equipment/image-2000-1216-96000143", "https://www.yelp.com/biz/image-2000-valencia"],
              "telephone": "+1-800-481-2250"}
    schema.update({"founded": "1992", "short_name": "Image 2000", "title_city": "California",
                   "cities": ["Santa Clarita", "Valencia", "Los Angeles", "Orange County", "Irvine", "Inland Empire", "Ontario", "Bakersfield", "Fresno", "Las Vegas", "Southern California", "Central Valley", "California", "Nevada", "CA", "NV"],
                   "area_served": [{"@type": "State", "name": "California"}, {"@type": "State", "name": "Nevada"}],
                   "meta_tail": "Image 2000, founder-owned office technology since 1992, seven branches across California and Las Vegas.",
                   "local": [{"slug": l[0], "name": f"Image 2000 {l[1]}", "street": l[2], "city": l[3].rsplit(",", 1)[0], "region": l[3].split(",")[-1].split()[0], "postal": l[3].split()[-1],
                              "telephone": "+1-" + l[4], "lat": l[6], "lon": l[7]} for l in LOCATIONS]})
    nav = [
        {"label": "Services", "href": "what-we-do.html", "mega": True,
         "groups": [{"title": "Print", "items": [[SERVICE_INDEX[s][2], f"services/{s}.html"] for s in ("office-technology", "managed-print", "production-print")]},
                    {"title": "Work", "items": [[SERVICE_INDEX[s][2], f"services/{s}.html"] for s in ("software-solutions", "managed-it", "ucaas")]},
                    {"title": "Office", "items": [["Water", "services/water.html"], ["Cost calculator", "cost-calculator.html"], ["All services", "what-we-do.html"]]}],
         "featured": {"eyebrow": "Not sure what you need?", "title": "Start with a quote", "body": "A specialist counts what you have and prices what you need, lease and purchase side by side.", "href": "contact.html", "label": "Request a quote"}},
        {"label": "Industries", "href": "industries.html", "children": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES] + [["All industries", "industries.html"]]},
        {"label": "Why Image 2000", "href": "why-image-2000.html", "children": [["PROs Elite and awards", "why-image-2000.html"], ["Manufacturers", "why-image-2000.html#manufacturers"], ["What customers say", "why-image-2000.html#voices"], ["Community", "about.html#community"]]},
        {"label": "Support", "href": SUPPORT, "children": [[l, h] for l, h in SUPPORT_LINKS] + [["Drivers and manuals", SUPPORT + "#drivers"]]},
        {"label": "About", "href": "about.html", "children": [["About Image 2000", "about.html"], ["Leadership", "about.html#team"], ["Locations", "locations.html"], ["Careers", "careers.html"], ["FAQ", "faq.html"], ["Contact", "contact.html"]]},
    ]

    map_items = [{"name": l[1].replace(" (Corporate)", ""), "lon": l[7], "lat": l[6], "href": f"locations/{l[0]}.html", "sub": l[2], "hq": l[0] == "valencia", "label_dx": LABEL_OFFSETS[l[0]][0], "label_dy": LABEL_OFFSETS[l[0]][1]} for l in LOCATIONS]
    MAP = {"type": "map", "id": "map", "region": "west", "ring": 30, "alt": "Map of California and Nevada with the seven Image 2000 branches", "heading": "Seven branches, one number, most of California and Las Vegas", "intro": f"Technicians, parts and supplies are dispatched from the branch nearest you. Call the branch directly or {PHONE}, which reaches all seven.", "items": map_items}

    pages = []
    # ---------------- home
    pages.append({"file": "index.html", "title": "Image 2000 | Copiers, managed print, IT and office technology in Southern California",
                  "compose": {
                      "clean": ["hero-film", "partners", "seal", "wheel", "is-this-you", "flow", "clients", "map", "voices", "faq", "contact"],
                      "showcase": ["hero", "partners", "wheel", "fleet", "ba", "flow", "office", "device", "proof", "clients", "map", "voices", "contact"],
                      "press": ["hero-light", "story", "services", "seal", "clients", "voices", "flow", "map", "faq", "contact"]},
                  "description": "Founder-owned in Valencia, California since 1992 and PROs Elite certified every year since 2016. Copiers and printers, managed print, document workflow, managed IT, cloud phones and bottleless water from seven branches across California and Las Vegas.",
                  "sections": [
        {"type": "hero", "id": "hero-light", "layout": "split", "eyebrow": "Valencia, California. Founder-owned since 1992.",
         "stats": [["1992", "Founder-owned since"], ["7", "Branches, California and Nevada"], ["11", "Manufacturers in the portfolio"], ["2016", "PROs Elite certified every year since"]],
         "ribbon": ["Kyocera FY26 Platinum Partner", "Sharp Hyakuman Kai Elite Award, five years running", "BBB accredited, A rating"],
         "variants": {"press": {"stats": None, "ribbon": ["Valencia, California. Since 1992.", "PROs Elite certified every year since 2016", "Kyocera FY26 Platinum Partner"]}},
         "heading": "Office technology from the dealer <em>recognized for service year after year</em>.",
         "subhead": "Copiers and printers, managed print, document workflow, managed IT, cloud phones and bottleless water. One West Coast partner, seven branches, one number to call.",
         "primary": QUOTE, "secondary": SECOND,
         "note": "Kyocera, Copystar, Sharp, Toshiba, Lexmark, Brother, HP, KIP, Canon, Kodak Alaris, RISO, Formax and Waterlogic dealer",
         "image": "assets/hq-1200.jpg", "image_alt": "The Image 2000 headquarters in Valencia, California, seen from above", "image_w": 1200, "image_h": 800,
         "badge": {"value": "PROs Elite", "label": "Certified every year since 2016"}},
        HERO_LAYERED,
        {"type": "hero-video", "id": "hero-film", "eyebrow": "Valencia, California. Founder-owned since 1992.", "heading": "Office technology from the dealer <em>recognized for service year after year</em>.",
         "subhead": "Copiers and printers, managed print, document workflow, managed IT, cloud phones and bottleless water. One West Coast partner, seven branches, one number to call.",
         "primary": QUOTE, "secondary": SECOND, "video": "assets/hero-valencia.mp4", "poster": "assets/hq-plate-dark-2100.jpg",
         "note": "The film is a generated push-in on Image 2000's own Valencia headquarters, labelled as such."},
        {"type": "partners", "id": "partners", "caption": "Manufacturers and technology partners", "items": MANUFACTURERS + SOFTWARE_PARTNERS},
        SEAL,
        {"type": "wheel", "id": "wheel", "eyebrow": "One partner", "heading": "Everything an office runs on, from one partner", "intro": "Hover a segment. Seven lines, one relationship, one number.", "items": WHEEL_ITEMS, "hub": "Image 2000", "hub_sub": "one partner", "ring": "EVERYTHING AN OFFICE RUNS ON"},
        {"type": "checklist", "id": "is-this-you", "alt": True, "eyebrow": "Is this you?", "heading": "Six signs your office spends more on print and technology than it knows",
         "intro": "Check what sounds familiar. Nobody is watching.",
         "items": ["Someone orders toner from a retail site when a device runs out", "Nobody knows what a page costs, mono or color", "More than one vendor services your devices", "A device has been down for more than a day this year", "The phone system is on hardware nobody wants to touch", "The copier company and the IT company blame each other"],
         "messages": ["Check what sounds familiar.", "One is normal.", "Two is a pattern.", "Three or more is money leaving the building every month. The quote finds how much."],
         "cta_label": "Request a quote", "cta_href": "contact.html"},
        {"type": "services", "id": "services", "heading": "Everything an office runs on, from one partner",
         "intro": "Most dealers sell copiers. Image 2000 connects the whole office and keeps it running, so you have one relationship instead of six vendors.",
         "items": [[s[1], s[3], f"services/{s[0]}.html"] for s in SERVICES]},
        FLOW, FLEET, BEFORE_AFTER, HOTSPOTS, STORY3D, CLIENTS_STRIP,
        {"type": "proof", "id": "proof", "alt": True, "eyebrow": "Audited, not claimed", "value": "95%+", "text": "Uptime for customers of a PROs Elite dealer, the result of technician training and service techniques audited by PROs. Image 2000 has earned the certification every year since 2016.", "source": "PROs Elite program description as published on image-2000.com. Only one dealer in any market earns it; about 100 in the United States."},
        MAP,
        {"type": "testimonials", "id": "voices", "alt": True, "layout": "feature", "eyebrow": "What customers say", "heading": "Customers, in their own words", "items": [t[:3] for t in TESTIMONIALS]},
        {"type": "timeline", "id": "story", "eyebrow": "The story", "heading": "From one shared philosophy to seven branches", "items": [["1992", "Two principals, one philosophy", "Richard Campbell and Joseph Blatchford set out to become exceptionally core-competent, so clients could rely on their expertise to cut through the glut of hardware and software flooding the market.", "assets/team/owners-600.jpg"], ["2016", "PROs Elite, and every year since", "One of about 100 dealers in the United States, with service results audited yearly."], ["2024", "12th largest Sharp dealer in the country", "ENX Magazine's Elite Dealers profile: five Hyakuman Kai Elite awards in a row, Kyocera Platinum Platter, mailing among the fastest-growing lines."], ["Today", "Seven branches, eleven manufacturers", "Valencia to Las Vegas. Copiers to water, one number.", "assets/hq-600.jpg"]]},
        {"type": "faq", "id": "faq", "alt": True, "heading": "Questions we get on the first call", "items": [
            ["How fast do you respond to a service call?", "From the nearest of seven branches, with local dispatch, parts and warehousing. Image 2000 is a PROs Elite dealer, which means its service results are monitored and audited every year against a 95% uptime standard. Ask the branch for the response terms in writing."],
            ["Can you take over devices we bought from someone else?", "Often, yes. The quote covers your whole fleet regardless of where it came from and says honestly which devices are worth keeping under agreement."],
            ["Lease or buy?", "Depends on volume, cash preference and how fast your needs change. The quote prices both side by side for your actual usage."],
            ["Do you serve offices outside Southern California?", "Seven branches cover Los Angeles, Orange County, the Inland Empire, the Santa Clarita Valley, Bakersfield, Fresno and Las Vegas. If you are further afield, ask; the answer will be honest either way."],
            ["Which manufacturers do you carry?", "Kyocera, Copystar, Sharp, Toshiba, Lexmark, Brother, HP, KIP, Canon large format, Kodak Alaris, RISO, Formax, Waterlogic and Sharp NEC displays. The recommendation fits the job, not the badge."]]},
        {"type": "contact", "id": "contact", "heading": "Request a quote", "body": "Tell us what you print, what you run and where you are. A specialist from the nearest branch replies with lease and purchase side by side. The numbers are yours whether or not you buy.",
         "options": ["Copiers and printers", "Managed print", "Document management and workflow", "Managed IT", "Cloud phones (UCaaS)", "Production, wide format or mailing", "Bottleless water free trial", "I am a customer and need support"], "submit": "Request a quote", "note": "A person from the nearest branch replies, not an autoresponder."},
    ]})
    # ---------------- services index + service pages
    pages.append({"file": "what-we-do.html", "title": f"Services | {CLIENT}", "description": "Seven service lines, one partner: copiers and office technology, managed print, document management and workflow, managed IT, cloud phones, production and mailing, and bottleless water.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Services", "heading": "Seven lines an office runs on. <em>One point of accountability.</em>", "subhead": "Every line below is sold, installed and serviced by the same company from the nearest of seven branches, so nothing falls between vendors.", "primary": QUOTE},
        {"type": "wheel", "id": "wheel", "eyebrow": "One partner", "heading": "Hover a segment", "intro": "Each line has its own page.", "items": WHEEL_ITEMS, "hub": "Image 2000", "hub_sub": "one partner", "ring": "EVERYTHING AN OFFICE RUNS ON", "panel_eyebrow": "Hover a segment", "link_label": "See the service"},
        dict(HOTSPOTS, alt=True),
        {"type": "resources", "heading": "The seven lines", "intro": "What changes, what is included, and the questions people ask.", "items": [[s[2], s[1], s[3], f"See {s[2].lower() if s[2] != 'UCaaS' else s[2]}", f"services/{s[0]}.html"] for s in SERVICES[:6]]},
        {"type": "resources", "alt": True, "heading": "And the break room", "intro": "Serviced on the same visit as the copier.", "items": [[SERVICES[6][2], SERVICES[6][1], SERVICES[6][3], "See bottleless water", f"services/{SERVICES[6][0]}.html"], ["Tool", "Print cost calculator", "Three sliders, a typical-rate estimate, and the quote replaces every number with yours.", "Estimate your print spend", "cost-calculator.html"], ["Support", "Customer support", "Service, meters, supplies, invoices, portal and screen share, one click deep.", "Open the fast lane", SUPPORT]]},
        {"type": "testimonials", "alt": True, "heading": "In customers' words", "items": [t[:3] for t in TESTIMONIALS]},
        LEADFORM]})
    for s in SERVICES:
        pages.append(service_page(*s))
    # ---------------- why
    pages.append({"file": "why-image-2000.html", "title": f"Why Image 2000 | PROs Elite certified, award-winning service", "description": "Only one dealer in any market earns PROs Elite status, and about 100 in the United States. Image 2000 has, every year since 2016, alongside Kyocera Platinum Partner, Sharp Hyakuman Kai and ENX Elite Dealer awards.",
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Why Image 2000", "heading": "Work with a company recognized <em>year after year</em> for superior service.", "subhead": "Every award on this page has a year and a source. The PROs Elite certification is the one that matters most, because someone other than us audits it.", "primary": QUOTE, "secondary": {"label": "See the awards", "href": "#awards"}, "image": "assets/hq-1200.jpg", "image_alt": "The Image 2000 headquarters in Valencia, California", "image_w": 1200, "image_h": 800, "badge": {"value": "2016", "label": "PROs Elite certified every year since"}},
        SEAL,
        {"type": "detail", "id": "pros-elite", "alt": True, "eyebrow": "What is PROs Elite?", "heading": "The national symbol of recognition in the office imaging industry", "body": "Only one dealer in any market is awarded this distinction, and only 100 dealers in the United States and select international markets earn PROs Elite status. The dealer agrees to have its service results continuously monitored and audited by the PROs Performance Improvement Virtual Operations Tool, and must earn certification through demonstrated service excellence, year after year, to keep it.",
         "bullets": ["Uptime in excess of 95%, from technician training and servicing techniques audited by PROs", "A locally owned dealer with local dispatch, local spare parts, local warehousing and complete account management", "Service management trained in advanced service management skills; the whole organization trained in customer relations", "Executive team trained in customer-focused leadership and strategic planning", "Annual roundtables with other PROs Elite dealers on the strategic issues facing office imaging customers", "Certification earned annually, so the experience stays consistent"],
         "image": "assets/pros-elite-circle.png", "image_alt": "The PROs Elite certified dealer mark", "image_w": 600, "image_h": 600},
        {"type": "cards", "id": "awards", "eyebrow": "Awards", "heading": "Six recognitions, each with a year", "intro": "From the awards page on image-2000.com.", "items": [[f"{a[1]} ({a[0]})", a[2]] for a in AWARDS]},
        {"type": "stats", "id": "clients-proof", "alt": True, "items": CLIENT_PROOF},
        CLIENTS_STRIP,
        BEFORE_AFTER,
        {"type": "partners", "id": "manufacturers", "caption": "Manufacturers and technology partners", "items": MANUFACTURERS + SOFTWARE_PARTNERS},
        {"type": "casestudy", "eyebrow": "In the founders' words", "heading": "Exceptionally core-competent, so clients can rely on our expertise", "quote": "By leveraging our many software solutions partners, and a diverse, 11-manufacturer product offering, we guarantee that the dollars you spend on document management, and its relevant technologies, will buy the best value in our industry.", "attribution": "Our Story, image-2000.com", "metrics": [["Since", "1992", "Founder-owned"], ["Sharp", "12th", "Largest Sharp dealer in the US (ENX Magazine, 2024)"]]},
        {"type": "testimonials", "id": "voices", "alt": True, "layout": "feature", "eyebrow": "What customers say", "heading": "Customers, in their own words", "items": [t[:3] for t in TESTIMONIALS]},
        LEADFORM]})
    # ---------------- industries
    pages.append({"file": "industries.html", "title": f"Industries | {CLIENT}", "description": "Churches, universities, school districts, medical centers and businesses of every size. Office technology built around how each one uses paper, records and phones.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Industries", "heading": "No business is <em>too small or too large</em>.", "subhead": "Churches, universities, school districts, medical centers and businesses of every size, in Image 2000's own words. Schools, hospitals, congregations and agencies print differently, file differently and buy differently. Each has its own page.", "primary": QUOTE},
        {"type": "resources", "heading": "Who Image 2000 serves", "intro": "The fields Image 2000 names on its clients page, and the ones it knows best.", "items": [[i[1], i[1], i[3], f"Office technology for {i[1].lower()}", f"industries/{i[0]}.html"] for i in INDUSTRIES[:3]]},
        {"type": "tabs", "id": "markets", "alt": True, "eyebrow": "Side by side", "heading": "What changes from one industry to the next",
         "items": [{"label": i[1].split(" and ")[0], "title": i[1], "body": i[4], "bullets": i[5][:3], "image": i[2], "image_alt": i[1], "href": f"industries/{i[0]}.html", "link_label": f"Office technology for {i[1].lower()}"} for i in INDUSTRIES]},
        CLIENTS_STRIP,
        {"type": "resources", "heading": "And the fourth", "intro": "Weekly volume on a board's budget, for the congregations Image 2000 already serves.", "items": [[INDUSTRIES[3][1], INDUSTRIES[3][1], INDUSTRIES[3][3], f"Office technology for {INDUSTRIES[3][1].lower()}", f"industries/{INDUSTRIES[3][0]}.html"]]},
        {"type": "testimonials", "alt": True, "heading": "What customers say", "items": [t[:3] for t in TESTIMONIALS]},
        LEADFORM]})
    for i in INDUSTRIES:
        pages.append(industry_page(*i))
    # ---------------- support
    pages.append({"file": SUPPORT, "title": f"Customer support | {CLIENT}", "description": "Request service, submit a meter read, order supplies, pay an invoice by credit card, open the self-service portal or start a screen share. Drivers and manuals for Sharp and Kyocera.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Customer support", "heading": "Already a customer? <em>How can we help you today?</em>", "subhead": "Everything an existing customer needs, one click deep. A person from the nearest of seven branches replies.", "primary": {"label": "Request service", "href": "#request"}, "secondary": {"label": f"Call {PHONE}", "href": PHONE_HREF}},
        {"type": "band", "eyebrow": "The fast lane", "heading": "Six things, under a minute each", "subhead": "Or call. A person answers.", "items": [["Request service", "Tell us the device and what it is doing", "#request"], ["Submit a meter read", "Thirty seconds, or automatic", "#meters"], ["Order supplies", "Toner and parts from the nearest branch", "#supplies"], ["Pay an invoice", "By credit card, on the secure payment page", PAY_URL], ["Self-service portal", "Account, equipment, orders and service calls", "#portal"], ["Screen share", "Let a technician see what you see", "#screenshare"]]},
        {"type": "detail", "id": "request", "eyebrow": "Service", "heading": "Request service", "body": "Tell us the device and what it is doing. Dispatch at the nearest branch confirms a window, and a technician comes with local parts.", "bullets": ["Local dispatch, parts and warehousing at all seven branches", "Technicians for Kyocera, Copystar, Sharp, Toshiba, Lexmark, Brother, HP, KIP, Canon and RISO", "Service results audited yearly under the PROs Elite program"], "form": {"fields": ["Company", "Equipment number", "Contact name and phone", "What is happening"], "submit": "Request service"}},
        {"type": "detail", "id": "meters", "alt": True, "eyebrow": "Meters", "heading": "Submit a meter read", "body": "Send a read in thirty seconds, or ask about automatic meter collection so you never do it again.", "bullets": ["Web form or automatic collection", "Reads feed billing directly, so invoices match usage", "Usage reporting on managed fleets"], "form": {"fields": ["Company", "Equipment number", "Meter reading"], "submit": "Send meter read"}},
        {"type": "detail", "id": "supplies", "eyebrow": "Supplies", "heading": "Order supplies", "body": "Toner and parts for your devices, shipped from the nearest branch or delivered on your service visit.", "bullets": ["Genuine supplies for every device we sell", "Ordered online or by phone, shipped from the nearest branch", "Billed with your service agreement"], "form": {"fields": ["Company", "Equipment number", "What you need"], "submit": "Order supplies"}},
        {"type": "cards", "id": "portal", "alt": True, "eyebrow": "Self-service portal", "heading": "Your account, online", "intro": "The E-Info customer portal on image-2000.com today. Your account manager sets up access at install.", "items": [["Account information", "View and manage your account details."], ["Service calls", "Place a service call and communicate with the technician on that call."], ["Supplies and orders", "Order supplies and view order status."], ["Equipment and meters", "View equipment information and submit meter readings."]]},
        {"type": "detail", "id": "screenshare", "eyebrow": "Screen share", "heading": "Customer support screen share", "body": "For software, driver and scan-to-email questions, a technician can see what you see. Call the branch or request a session and we send the link.", "bullets": ["Driver installs and print queues", "Scan to email, scan to folder and scan to workflow set-up", "Software questions on Square 9, DocuWare and Elevate"], "form": {"fields": ["Company", "Contact name and phone", "What you need help with"], "submit": "Request a screen share"}},
        {"type": "resources", "id": "drivers", "alt": True, "heading": "Drivers and manuals", "intro": "The manufacturer download pages our technicians use. Bookmark the one for your device.",
         "items": [["Drivers", "Sharp", "Sharp Business Products downloads: drivers, manuals and software.", "Sharp downloads", "https://business.sharpusa.com/product-downloads"],
                   ["Drivers", "Kyocera", "Kyocera Document Solutions downloads: drivers and manuals.", "Kyocera downloads", "https://www.kyoceradocumentsolutions.us/en/support/downloads.html"],
                   ["Drivers", "Toshiba", "Toshiba e-STUDIO drivers and manuals.", "Toshiba downloads", "https://business.toshiba.com/support/drivers-and-manuals"],
                   ["Drivers", "Lexmark", "Copier and printer drivers and manuals.", "Lexmark support", "https://support.lexmark.com/en_us.html"],
                   ["Drivers", "Brother", "Print drivers for Brother devices.", "Brother support", "https://www.brother-usa.com/brother-support/driver-downloads"],
                   ["Drivers", "HP", "Printer drivers, manuals and safety data sheets.", "HP support", "https://support.hp.com/us-en/drivers/printers"]]},
        {"type": "faq", "heading": "Service questions", "items": [["What response time can we expect?", "Ask your branch for the response commitment in your agreement, in writing. We would rather give you the real number than print a round one. What we can say is that PROs audits our service results every year against a 95% uptime standard."], ["Do you service devices you did not sell?", "Often, yes. Ask, and we will say plainly which models we support to our own standard."], ["How do I pay an invoice?", "By credit card on the secure payment page linked above, or ask your branch about other options."]]},
    ]})
    # ---------------- cost calculator
    pages.append({"file": "cost-calculator.html", "title": f"Print cost calculator | {CLIENT}", "description": "Estimate what your office spends on printing today: devices, mono and color pages, staff time. Typical rates; the quote replaces them with your meters.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Cost calculator", "heading": "What does your office <em>really</em> spend on print?", "subhead": "Move three sliders. The estimate uses typical rates for toner, service and the staff time nobody counts. The quote replaces every number here with yours."},
        {"type": "calculator", "id": "calc", "alt": True, "eyebrow": "Estimate", "heading": "Your print spend, estimated", "intro": "Devices, mono pages and color pages a month. That is all it needs.",
         "rates": {"mono_cpp": 0.018, "color_cpp": 0.09, "minutes_per_device_week": 25, "hourly": 28, "managed_saving": 0.2, "saving_label": "Illustrative saving at 20% under managed print. Industry estimates vary; the quote gives your number."},
         "note": "Estimates only, using typical rates. Nothing here is a quote. The quote gives you the real figure from your meters and your invoices.",
         "cta_label": "Get the real number: request a quote", "cta_href": "contact.html"},
        {"type": "comparison", "heading": "Lease or buy?", "intro": "The quote prices both for your real volume. Here is how they usually compare.",
         "columns": [{"label": "Lease", "recommended": True}, {"label": "Buy"}],
         "rows": [["Best for", "Steady volume, a fleet kept current", "Stable volume, long device life"], ["Term", "36 to 60 months, typically", "None"], ["Up-front cost", "Low", "Highest"], ["Lifetime cost", "Moderate", "Lowest if the device runs for years"], ["Technology refresh", "Built in at end of term", "When you buy again"], ["Service and supplies", "Managed agreement, or separate", "Managed agreement, or separate"]],
         "note": "Terms and rates are set in the quote."},
        {"type": "faq", "alt": True, "heading": "About the estimate", "items": [["Where do the rates come from?", "Typical industry per-page rates for toner and service, and a modest allowance for the staff time spent ordering supplies and chasing repairs. They are for orientation only."], ["Why does staff time count?", "Because it is real money that never appears on a print invoice. Someone orders the toner and waits on hold for the technician."], ["How do I get the real number?", "Request a quote. We count every device, collect your invoices and hand you the numbers."]]},
        {"type": "leadform", "id": "quote", "heading": "Get the real number", "body": "A specialist from your nearest branch counts what you have and prices what you need. The numbers are yours whether or not you buy.", "submit": "Request a quote", "note": "A person from the nearest branch replies, not an autoresponder."},
    ]})
    # ---------------- about
    pages.append({"file": "about.html", "title": f"About Image 2000 | Founder-owned office technology in Valencia, California since 1992", "description": "In 1992 a shared philosophy about the future of office technology brought Richard Campbell and Joseph Blatchford together. Thirty-three years later they still own the company, now seven branches across California and Las Vegas.",
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "About Image 2000", "heading": "A shared philosophy about the future of office technology, <em>since 1992</em>.", "subhead": "Principals Richard Campbell and Joseph Blatchford set out to become exceptionally core-competent, so clients could rely on their expertise to cut through the glut of hardware and software flooding the market. Over thirty years, they have consistently done just that.", "primary": QUOTE, "secondary": {"label": "Meet the leadership", "href": "#team"}, "image": "assets/team/owners-1200.jpg", "image_alt": "Rich Campbell and Joe Blatchford, co-owners of Image 2000, at the front door of the Valencia headquarters", "image_w": 1200, "image_h": 800, "badge": {"value": "1992", "label": "Founder-owned since"}},
        {"type": "stats", "alt": True, "items": [["1992", "Founded in Valencia, California"], ["7", "Branches across California and Nevada"], ["11", "Manufacturers in the portfolio"], ["2016", "PROs Elite certified every year since"]]},
        {"type": "casestudy", "eyebrow": "Our mission", "heading": "Flexible, responsive and personal", "quote": MISSION, "attribution": "Image 2000 mission statement", "metrics": [["Big enough", "7", "Branches to matter"], ["Small enough", "2", "Owners who still run it"]]},
        {"type": "timeline", "eyebrow": "The story", "heading": "From one shared philosophy to seven branches", "items": [["1992", "Two principals, one philosophy", "Richard Campbell and Joseph Blatchford come together around a shared view of where office technology is going, and a goal: to be so core-competent that clients can rely on them to choose."], ["Growth", "From copiers to the whole office", "Managed print, document management and workflow, managed IT, UCaaS and bottleless water, each added because clients asked."], ["2016", "PROs Elite, and every year since", "One of about 100 dealers in the United States with service results audited annually."], ["Today", "Seven branches, still founder-owned", "Headquartered in the Santa Clarita Valley, serving Southern California, the Central Valley and Las Vegas."]]},
        {"type": "leadership", "id": "team", "heading": "The leadership", "intro": "The two founders, and the operator who runs the day to day.", "people": [[t[0], t[1]] for t in LEADERS], "orgs_intro": "Manufacturer and technology partners", "orgs": MANUFACTURERS + SOFTWARE_PARTNERS},
        {"type": "cards", "alt": True, "eyebrow": "The leadership, in a little more detail", "heading": "Three people you will hear from", "items": [[f"{t[0]}, {t[1]}", t[2]] for t in LEADERS]},
        {"type": "values", "eyebrow": "How Image 2000 describes itself", "heading": "Listening, trust, and the latest cost-reduction strategies", "items": [["Listening", "A staunch commitment to enhancing each client's business is best achieved by listening to and supporting their vision."], ["Trust", "An environment built on trust, with the aim of using today's technologies to elevate the future growth and profitability of every client."], ["Core competence", "Deep expertise in a rapidly evolving landscape, so the recommendation fits the job rather than the badge, with service results audited by PROs Elite every year since 2016."]]},
        {"type": "cards", "id": "community", "eyebrow": "Community", "heading": "Big enough to matter, small enough to care", "intro": "Image 2000 actively supports organizations across its territories, from the Santa Clarita Valley to Orange County.", "items": [["Health", "Henry Mayo Newhall Hospital, Adventist Health, Make-A-Wish and the St. Baldrick's Foundation."], ["Youth and education", "Boys & Girls Clubs of America, Saugus High School, Pateadores, the Wish Education Foundation and the JCC of Orange County."], ["Community", "Single Mothers Outreach of Santa Clarita, East Valley Family Services, the Tierra Del Sol Foundation, the Sebastian Velona Foundation and The Giving Back Fund."]]},
        {"type": "partners", "id": "supports", "caption": "Image 2000 actively supports", "items": COMMUNITY},
        LEADFORM,
        {"type": "cta", "heading": "Talk to the nearest branch", "subhead": "Seven branches across California and Nevada. One number reaches all of them.", "primary": {"label": f"Call {PHONE}", "href": PHONE_HREF}},
    ]})
    # ---------------- careers
    pages.append({"file": "careers.html", "title": f"Careers | {CLIENT}", "description": "Image 2000 is one of the fastest growing providers of digital imaging and document management solutions in Southern California and Las Vegas. Sales Account Executive openings at every branch.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Join our team", "heading": "One of the fastest growing providers in <em>Southern California and Las Vegas</em>.", "subhead": "Image 2000 offers exceptional pricing and service to its customers, and it is hiring the people who deliver it.", "primary": {"label": "See openings", "href": "#openings"}},
        {"type": "cards", "id": "openings", "alt": True, "eyebrow": "Current openings", "heading": "Sales Account Executive, every branch", "intro": "Technicians, operations, warehouse, administrative and accounting: no current openings. Check back soon.", "items": [[l[1], f"Sales Account Executive, {l[2]}, {l[3]}."] for l in LOCATIONS] + [["Every branch", "Technicians, operations, warehouse, administrative and accounting: no current openings. Check back soon."]]},
        {"type": "values", "eyebrow": "Why here", "heading": "What it is like to work for a PROs Elite dealer", "items": [["Trained", "Service management trained in advanced service management; the whole organization trained in customer relations."], ["Audited", "Service results monitored and audited yearly, so good work is visible."], ["Local", "Seven branches with local dispatch, parts and warehousing. You serve the people down the street."], ["Founder-owned", "The two people who started the company in 1992 still run it."]]},
        {"type": "leadform", "id": "apply", "heading": "Apply", "body": "Tell us the branch, the role and how to reach you. A person replies.", "fields": [["Name", "text", "name"], ["Email", "email", "email"], ["Phone", "tel", "tel"], ["Branch and role", "text", "organization"]], "submit": "Send my details", "note": "A person replies, not an autoresponder."},
    ]})
    # ---------------- locations
    pages.append({"file": "locations.html", "title": f"Locations | Image 2000 branches in California and Las Vegas", "description": "Headquartered in Valencia with branches in Los Angeles, Orange County, the Inland Empire, Bakersfield, Fresno and Las Vegas. Local technicians, parts and supplies at every one.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Locations", "heading": "Seven branches. <em>Local dispatch at every one.</em>", "subhead": f"Headquartered in the Santa Clarita Valley, with branches serving Southern California, the Central Valley and Las Vegas. Call the branch nearest you, or {PHONE} reaches all of them.", "primary": {"label": f"Call {PHONE}", "href": PHONE_HREF}},
        MAP,
        {"type": "locations", "detailed": True, "heading": "Where we are", "intro": "Each location is a full branch: sales, service dispatch, parts and supplies. Each has its own page.", "items": [[l[1], l[2], l[3], l[4], l[5]] for l in LOCATIONS]},
        {"type": "faq", "heading": "Coverage questions", "items": [["Do you cover my town?", "Los Angeles, Orange County, the Inland Empire, the Santa Clarita Valley, Bakersfield, Fresno and Las Vegas are home territory, and customers with offices elsewhere in California or Nevada are served from the nearest branch. Ask; we will say honestly whether we can meet our own standard where you are."], ["Can I see a device before I decide?", "Ask your branch. Bring a sample of what you print and we will run it on the device you are considering."]]},
        LEADFORM]})
    for l in LOCATIONS:
        pages.append(location_page(*l))
    # ---------------- faq
    pages.append({"file": "faq.html", "title": f"FAQ | {CLIENT}", "description": "Answers to the questions people ask Image 2000 first: response times, taking over devices, lease versus buy, coverage, manufacturers, managed IT and cloud phones.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "FAQ", "heading": "Questions, <em>answered plainly</em>.", "subhead": "If yours is not here, ask. A person from the nearest branch replies."},
        {"type": "faq", "heading": "Working with Image 2000", "items": [
            ["How fast do you respond to a service call?", "From the nearest of seven branches, with local dispatch, parts and warehousing. Image 2000 is a PROs Elite dealer, which means its service results are monitored and audited every year against a 95% uptime standard. Ask the branch for the response terms in writing."],
            ["Can you take over devices we bought from someone else?", "Often, yes. The quote covers your whole fleet regardless of where it came from."],
            ["Lease or buy?", "The quote prices both side by side for your actual usage. Leases in this industry typically run 36 to 60 months; purchase suits stable volume and long device life."],
            ["Which manufacturers do you carry?", "Kyocera, Copystar, Sharp, Toshiba, Lexmark, Brother, HP, KIP, Canon large format, Kodak Alaris, RISO, Formax, Waterlogic and Sharp NEC displays."],
            ["Do you do IT and phones as well as copiers?", "Yes. Managed IT, managed security, backup and cloud with our partner The Core Group, and Elevate cloud phones with Teams integration. Many customers start with print and add the rest."],
            ["Where are you?", "Valencia (headquarters), Los Angeles, Orange County, the Inland Empire, Bakersfield, Fresno and Las Vegas."],
            ["How do I order supplies or request service?", "The support page: service, meter reads, supplies, invoices, the self-service portal and screen share, each under a minute."]]},
        LEADFORM]})
    # ---------------- contact
    pages.append({"file": "contact.html", "title": f"Contact | Request a quote | {CLIENT}", "description": f"Request a quote from Image 2000, or call {PHONE}. Headquarters at 26037 Huntington Lane, Santa Clarita, CA 91355, with branches in Los Angeles, Orange County, the Inland Empire, Bakersfield, Fresno and Las Vegas.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Contact", "heading": "Request a quote, or <em>just call</em>.", "subhead": f"Tell us what you print, what you run and where you are. A specialist from the nearest branch replies with numbers, not a pitch. Or call {PHONE}."},
        {"type": "contact", "id": "form", "heading": "Request a quote", "body": "Choose what you are thinking about, or tell us you are a customer who needs support.", "options": ["Copiers and printers", "Managed print", "Document management and workflow", "Managed IT", "Cloud phones (UCaaS)", "Production, wide format or mailing", "Bottleless water free trial", "I am a customer and need support"], "submit": "Request a quote", "note": f"A person from the nearest branch replies, not an autoresponder. Existing customers: the support page is faster, or call {PHONE}."},
        {"type": "locations", "alt": True, "heading": "Or call the branch nearest you", "intro": "Seven branches across California and Nevada. Call the branch for hours.", "items": [[l[1], l[2], l[3], l[4], l[5]] for l in LOCATIONS]},
    ]})

    pitch = {
        "qbs_contact": {"name": "Shawn Peterson", "email": "shawn@thequantumleap.business", "phone": "(712) 389-4639"},
        "prepared_for": "Joe Blatchford, Rich Campbell, Charles Turner and Raimie Stein, Image 2000",
        "heard_intro": "Everything here comes from image-2000.com, the weekly Quantum and Image 2000 meetings, and public data. We have not yet asked the design questions; tell us where this is wrong, and your words outrank ours.",
        "heard": ["Service is the story. PROs Elite every year since 2016, Kyocera Platinum, Sharp Hyakuman Kai four years running, ENX Elite Dealer seven years running. The current site knows this and buries it under a slider. Every direction here leads with it, with a year and a source on each award.",
                  "Existing customers are most of the traffic. Service, meter reads, supplies, invoices, the portal and screen share are one click deep on every page, in a fast lane, the way they are in the current menu.",
                  "The five cross-sell segments you built in HubSpot with Marko (copiers, IT networking, mailing equipment, managed services, resell equipment) each get a page here, so the sequences have somewhere to land that is not the home page.",
                  "Request a quote is your call to action, and the preview keeps your words. We would rather add a soft path, the cost calculator, than change the hard one.",
                  "Founder-owned since 1992, still run by the two people who started it. The about page puts Rich and Joe at the front door of the Valencia building, because the photograph exists and it says more than the copy."],
        "found": ["image-2000.com earns about 490 organic visits a month on 103 keywords (Semrush, 8 September 2026). About 89% of that is people searching the company name. The market is not finding Image 2000 through search; almost every visitor already knows it.",
                  "The only non-brand commercial traffic lands on Wix product pages: RISO duplicators (position 8 for 'riso printer for sale') and KIP wide-format. Those URLs need redirects or a kept catalogue, and RISO deserves a page.",
                  "There is no blog content, no FAQ and no page that answers a buyer's question: copier lease Los Angeles, managed print services Orange County, Kyocera dealer Bakersfield. The site describes products well and never appears when a buyer asks how to choose.",
                  "The site is Wix. The hero and the three service tiles are images of text, the home h1 is set in all caps, the Software Solutions page lives at /copy-of-managed-it, and phone numbers are not tappable on iPhones because the page sets format-detection to none.",
                  "The branch count disagrees with itself: seven in the footer, eight on the about page (including Portland), nine on the team page. The preview uses the seven with addresses and asks you to confirm.",
                  "The awards page is the strongest content on the site and it is two clicks deep. Here the PROs Elite explanation, in your words, is the second section of Why Image 2000.",
                  "Your Our Clients page is a single image, so search engines cannot read Children's Hospital Los Angeles, Adventist Health, Cedars-Sinai or the nine school districts. Here they are text on the home page, the Why page and every industry page."],
        "choose_heading": "Three directions. Your call.",
        "choose_intro": "The words, the pages and the proof are identical in all three. What differs is the register: how plain, how modern, how established Image 2000 reads. Open each one on your phone, click through the pages your customers use, and tell us which one feels like Image 2000.",
        "choose_reasons": [["If clarity is the argument", "Clean: blue on white, a humanist sans, hairline cards. It reads like the most organized dealer in the market, and it is the fastest to build in HubSpot."],
                           ["If modern is the argument", "Showcase: the layered hero over your own building, a device rail you can scroll, a copier that turns as you read, pill buttons and floating cards. A 33-year-old dealer that looks like the newest one in the market. Set in Clean's typefaces, so the two share a voice."],
                           ["If established is the argument", "Press: warm paper, a serif, the founders' story high on the page. Editorial and unhurried. Nobody in office technology looks like this, which is the point."]],
        "pick_reasons": [["Blue on white is already the brand", "Clean keeps the measured blue as the accent on a white ground, sets everything in a humanist sans, and lets the awards and the support links do the talking. It reads like the most organized dealer in the market, which is the argument."],
                         ["The buyer is comparing", "An office manager or IT director with three quotes open wants clarity: what you sell, who services it, what it costs, who answers the phone. Clean puts those four answers above the fold on every page."],
                         ["It is the fastest to build in HubSpot", "Clean uses the theme's standard modules with the fewest custom pieces, so it ships soonest and your team can edit every section without a developer."]],
        "pick_change": "If the room wants more energy, we keep Clean's structure and borrow Showcase's layered hero and device rail for the home page only. That is a one-line change in the content file.",
        "alternatives": [["Quantum Showcase", "The stretch: a layered hero over the Valencia building, a device fleet you can scroll, a 3D copier that turns as you read, pill buttons and floating cards. A 33-year-old dealer that looks like the newest one in the market."],
                         ["Quantum Press", "The wildcard: warm paper, a serif, the founders' story high on the page. Editorial and unhurried. Nobody in office technology looks like this, which is the point."]],
        "plan": [["Weeks 1 to 2", "Choose a direction. Confirm the items under To confirm. Answer the four design questions, especially the promise: what does this site have to make a visitor believe? Semrush project and Search Console access set up on day one."],
                 ["Weeks 3 to 4", "Copy from Joe, Rich and Raimie in your words, page by page. Photography of the branches, the technicians and the vans. The RISO and KIP product pages decided: keep as a catalogue or redirect."],
                 ["Weeks 5 to 7", "Build in your HubSpot: theme, templates, every page. Forms to named people at each branch, the support fast lane wired to the portal and the payment page, LocalBusiness markup on all seven branches."],
                 ["Weeks 8 to 9", "Review rounds with your team, redirects for every URL on the map below, QA on the same gate this preview passed, and a test submission through every form."],
                 ["Week 10", "Launch, with the baseline captured the day before. Month one: the five cross-sell sequences pointed at their new pages, and the first article aimed at the RISO and copier lease terms you already rank for."]],
        "search": {"heading": "Where Image 2000 stands in search today, and what changes", "intro": "Measured before we touched anything, so the work can be judged against it.", "as_of": "Semrush US database and live HTML, 8 September 2026",
                   "today_stats": [["490", "Organic visits a month"], ["103", "Keywords ranking"], ["89%", "Of traffic from the company name"], ["0", "Pages answering a buyer's question"]],
                   "today": ["The market cannot find Image 2000. About 490 visits a month from search, and almost nine in ten of them typed the company name.",
                             "The only non-brand traffic is RISO and KIP product pages, ranking on page one for 'riso printer for sale' and 'kip 660'.",
                             "No blog, no FAQ, no service page with a place name in its title. A buyer in Fresno or Irvine searching for a copier lease does not see Image 2000.",
                             "One Organization record in schema, no LocalBusiness record for any of the seven branches.",
                             "Hero and service tiles are images of text; the site runs a cookie banner; phone numbers are not tappable on iPhones."],
                   "after": ["Thirty pages, each built around one thing a buyer asks, with titles that name the place: Copier Sales, Lease and Service in Fresno; Managed Print Services in Orange County.",
                             "Seven branch pages with LocalBusiness markup, addresses, phones and the lines each branch sells.",
                             "A RISO, wide-format and mailing page, so the one search term that already works has a real landing page.",
                             "FAQ markup on every FAQ, BreadcrumbList on every nested page, Organization markup naming Image 2000, Inc.",
                             "The support fast lane on every page, tappable phone numbers, no cookie theatre.",
                             "A blog is deliberately not in the launch scope. Month one after launch decides the first three articles from the cross-sell segments."],
                   "keep": [["/", "/", "Home: title rewritten with place and service"], ["/whyimage2000", "/why-image-2000.html", "Redirect"], ["/product-catalogs", "/services/office-technology.html", "Redirect"], ["/copy-of-managed-it", "/services/software-solutions.html", "Redirect"], ["/managed-it", "/services/managed-it.html", "Redirect"], ["/ucaas", "/services/ucaas.html", "Redirect"], ["/waterlogic", "/services/water.html", "Redirect"], ["/customer-services", "/support.html", "Redirect, plus the five support tasks"], ["/locations, /santa-clarita, /irvine ...", "/locations.html, /locations/<branch>.html", "Redirect, one per branch"], ["/product-page/rz1090-riso, /product-page/kip-650-kip-660", "/services/production-print.html", "Redirect or keep the catalogue; the only non-brand traffic"]],
                   "note": "Every URL that exists today gets a permanent redirect, tested individually at launch. Numbers from Semrush's US database; a market this small moves with a handful of rankings, so the six-month measure is the place-named service queries Image 2000 starts ranking for, not the total."},
        "confirm": ["The branch count. The footer lists seven with addresses; the about page says eight including Portland, Oregon; the team page says nine. The preview uses the seven.",
                    "The promise. We have not asked the four design questions. What does this site have to make a visitor believe?",
                    "The testimonials and client names. Cathy Vasilev of Cedars-Sinai is attributed in full on your Our Clients graphic; Robert O. is first name only. The 22 client names and the Adventist Health and school district counts come from that graphic. Confirm every one may appear on the new site.",
                    "The manufacturer list. The site says an eleven-manufacturer portfolio; the catalogue menu lists thirteen brands plus HP products. The preview names what the catalogue names.",
                    "How to present The Core Group (managed IT) and Elevate (UCaaS). Both are named as partners on the live site. Partner, white-label, or Image 2000's own service?",
                    "Response times, technician counts, devices under management and customer counts. None are published, so none appear. If you have them, they belong in the seal.",
                    "'Southern California's #1 dealer for all your office solutions' is the current headline. Keep it, qualify it, or replace it with the audited PROs Elite claim, which is what the preview does.",
                    "The E-Info self-service portal URL and the pay-by-card page. The preview links the payment page from the live site and describes the portal without a link.",
                    "The logo. The preview uses the current wordmark cut out from a JPEG. A vector file, and a light-ground and dark-ground variant, are needed for the build.",
                    "Managed print specifics. Automatic meter collection, supplies replenishment on usage and rental terms are common in the industry but not published on your site, so the preview does not claim them. Tell us what your agreements actually include.",
                    "Industries. Government, education, healthcare and religious organizations come from your UCaaS page. Confirm they are the four you want to lead with for the whole company, or name others.",
                    "Photography. The Valencia aerial and the owners' photograph are yours; everything else is generated and labelled. Branch exteriors, technicians and vans would replace most of it."],
        "footer": "Prepared for Joe Blatchford, Rich Campbell, Charles Turner and Raimie Stein. Nothing here is live or indexed. Every number and claim we could source comes from image-2000.com, the weekly meeting record or public data. Items we could not source are listed under To confirm. Photographs other than the Valencia headquarters and the owners, the renders and the 3D device are generated and labelled as such; your own imagery replaces them.",
    }
    pages.append({"file": "brands.html", "title": "Brands | Image 2000 carries eleven manufacturers", "description": "Sharp, Kyocera, Toshiba, Lexmark, HP, Brother, KIP, Canon large format, Kodak Alaris, RISO, Formax, Waterlogic and Sharp NEC. The badge follows the job.",
                  "crumbs": [["Home", "index.html"], ["Brands", "brands.html"]],
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Brands", "heading": "Eleven manufacturers, so the badge <em>follows the job</em>.", "subhead": "Sharp and Kyocera lead, with the awards to show for it. The rest are there so the recommendation is about your work, not our inventory.", "primary": QUOTE},
        dict(FLEET, alt=True),
        {"type": "resources", "heading": "Every brand", "intro": "Each has its own page and a catalogue.", "items": [[b[2], b[1], b[3], f"See {b[1]}", f"brands/{b[0]}.html"] for b in BRANDS]},
        {"type": "partners", "caption": "Manufacturer and software partners", "items": MANUFACTURERS + SOFTWARE_PARTNERS},
        {"type": "faq", "heading": "Brand questions", "items": [
            ["Why carry eleven print brands?", "So the device fits the work rather than the other way round. A law office, a print shop and a school district need different machines, and one brand rarely covers all three well."],
            ["Which brand should I pick?", "Start with the volume, the finishing and the software you run, and the specialist will narrow it to two devices. The brand pages say what each line is best at."],
            ["Do you service brands you did not sell?", "Ask the nearest branch. Many of the represented lines can be serviced regardless of where the device was bought."]]},
        LEADFORM]})
    for b in BRANDS:
        pages.append(brand_page(*b))
    _FAQ_EXTRA = {
        "what-we-do.html": ("How the service lines fit", [
            ["What does Image 2000 do?", "Copiers and office technology from eleven manufacturers, managed print, document management and workflow, managed IT, cloud phones, production and mailing, and bottleless water."],
            ["Do I have to take everything?", "No. Most customers start with the print fleet and add lines as the relationship earns it."],
            ["Where does Image 2000 work?", "From seven branches: Valencia, Los Angeles, Orange County, the Inland Empire, Bakersfield, Fresno and Las Vegas."]]),
        "why-image-2000.html": ("Why Image 2000", [
            ["What is PROs Elite?", "An independent certification of dealer service performance held by about 100 dealers in the United States, one per market. Image 2000 has held it every year since 2016."],
            ["Is Image 2000 independent?", "Yes. Founded in 1992 by Richard Campbell and Joseph Blatchford, who still own the company, headquartered in Valencia."],
            ["How is service measured?", "By response, first-visit fix and retention, the numbers the PROs Elite audit and the manufacturer awards on this site are based on."]]),
        "industries.html": ("Industry questions", [
            ["Which industries does Image 2000 serve most?", "Churches, universities, school districts, medical centers and businesses of every size across Southern California, the Central Valley and Las Vegas."],
            ["My industry is not listed.", "The industry pages show how the same services fit different workflows; the quote adapts them to yours."],
            ["Do you have references in my industry?", "Yes. Over twenty Adventist Health medical centers, more than nine Southern California school districts, and the organizations named on this site. Ask the nearest branch for one in your field."]]),
        "about.html": ("Questions about Image 2000", [
            ["When was Image 2000 founded?", "In 1992, by Richard Campbell and Joseph Blatchford, in the Santa Clarita Valley, where the company is still headquartered."],
            ["Where are the offices?", "Seven: Valencia, Los Angeles, Orange County, the Inland Empire, Bakersfield, Fresno and Las Vegas. Technicians are dispatched from the nearest one."],
            ["Which manufacturers does Image 2000 represent?", "Kyocera, Copystar, Sharp, Toshiba, Lexmark, Brother, HP, KIP, Canon, Kodak Alaris, RISO, Formax, Waterlogic and Sharp NEC Displays, with Square 9, DocuWare, FormedAI and PaperCut for software."]]),
        "careers.html": ("Working at Image 2000", [
            ["What roles does Image 2000 hire for?", "Sales Account Executives at every branch, plus field service technicians, IT engineers, customer care and administration as openings arise."],
            ["Where would I work?", "Any of the seven branches in California and Las Vegas, with field roles covering the customers nearest that branch."],
            ["How do I apply?", "Use the form on this page. A person from Image 2000 reads every application and replies."],
            ["What is it like to work at Image 2000?", "A founder-owned dealer since 1992 where technicians, sales and support work in the same building as the people who own the company. Training on the manufacturers' lines is part of the job."]]),
        "contact.html": ("Before you write", [
            ["Which branch should I contact?", "The nearest of the seven. 800-481-2250 reaches all of them."],
            ["How do I request service, supplies or a meter read?", "Existing customers use the customer support page or call the branch. New customers start with the form here."],
            ["Who replies?", "A person from the branch, during business hours, Monday to Friday. The form is not an autoresponder."]]),
    }
    for _pg in pages:
        if _pg["file"] in _FAQ_EXTRA and not any(x.get("type") == "faq" for x in _pg["sections"]):
            _h, _items = _FAQ_EXTRA[_pg["file"]]
            _faq = {"type": "faq", "id": "faq", "heading": _h, "items": _items}
            _secs = _pg["sections"]
            if _secs and _secs[-1].get("type") in ("leadform", "cta", "contact"):
                _secs.insert(len(_secs) - 1, _faq)
            else:
                _secs.append(_faq)
    return {"client": CLIENT, "slug": "image-2000", "domain_hint": "image-2000.com",
            "brand": brand, "schema": schema, "nav": nav, "pages": pages, "pitch": pitch}


if __name__ == "__main__":
    data = build()
    with open(OUT, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}: {len(data['pages'])} pages")
