import re
#!/usr/bin/env python3
"""Authoring script for brands/kelly-office-solutions.content.json.

The JSON is what scripts/preview.py reads; this script is how a human writes it without
repeating forty pages by hand. Run it to regenerate the JSON:

    python3 brands/kelly-office-solutions.content.py

Every fact below is SOURCED from kellyofficesolutions.com, the brief, or Kelly's brand profile
unless marked DRAFT in a comment. DRAFT items are also listed on the hub's "To confirm" section.
No em dashes anywhere; the generator rewrites them, but write it clean.
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kelly-office-solutions.content.json")

PHONE, PHONE_HREF = "1-800-34-KELLY", "tel:18003453559"
PORTAL = "https://einfo.kellyofficesolutions.com:8890/"

# ------------------------------------------------------------------ sourced facts (kellyofficesolutions.com)
TESTIMONIALS = [
    ["We rely on Kelly Office Solutions for our entire company's printing and copying needs. We are a company with 350 employees and fourteen field offices all of which they serve. All needs are met on a timely and professional basis. It is nice to know there is still a local company here when you need them.", "Debbie Scott", "S & N Communications"],
    ["It has also been a pleasure to work with their service department. They are polite, courteous, and very responsive to our needs. Response times are fast and the level of communication has been outstanding.", "David Shelton", "Pike Electric, Inc."],
    ["Kelly Office Solutions has been one of our best vendors for six years running. The service department is prompt and efficient. In over 15 years of dealing with office equipment vendors, I have never seen a vendor that is so customer focused.", "Rick Aaronson", "Lexington Home Brands"],
    ["Aside from the quality, efficiency, and ease of use of the products we utilize from them, their attention and constant focus on customer service are in one word impressive. Mr. Murrell and others associated with Kelly Office Solutions are quick to respond to any challenge, request, or demand placed in front of them.", "Quintin Williams", "Debbie's Staffing Services"],
]
TAX_SEASON = ["I was thrilled to be able to call and get a repair on the same day. Tax season is our busiest time of year and the quick response was appreciated by all.", "Anita Henderson", "Edwards Craver Veach, PLLC"]
COMMUNITY = ["The First Tee of the Triad", "Big Brothers Big Sisters of America", "Forsyth Humane Society", "Old Salem", "Riverwood Therapeutic Riding Center", "Local chambers of commerce"]
LOCATIONS = [
    # slug, city, address 1, address 2, phone display, phone href, region label, state
    ["winston-salem", "Winston-Salem", "163 South Stratford Road", "Winston-Salem, NC 27103", "(336) 725-2566", "tel:3367252566", "the Triad"],
    ["greensboro", "Greensboro", "1040 E. Wendover Ave.", "Greensboro, NC 27405", "(336) 232-0399", "tel:3362320399", "the Triad"],
    ["charlotte", "Charlotte", "4205-B Stuart Andrew Blvd.", "Charlotte, NC 28217", "(704) 588-6891", "tel:7045886891", "the Charlotte metro"],
    ["raleigh", "Raleigh", "6001 Chapel Hill Rd, Suite 103", "Raleigh, NC 27607", "(919) 378-0172", "tel:9193780172", "the Triangle"],
    ["swansboro", "Swansboro", "109 Seth Thomas Ln", "Swansboro, NC 28584", "(252) 393-1112", "tel:2523931112", "the coast"],
]
CHARLOTTE_TOWNS = ["Charlotte", "Huntersville", "Davidson", "Mooresville", "Concord", "Pineville", "Gastonia", "Matthews", "Mint Hill", "Monroe", "Waxhaw", "Fort Mill", "Rock Hill"]
HOURS_CONFIRMED = {"greensboro", "charlotte", "raleigh"}  # M-F 8-5 stated on the live city pages
PARTNERS = ["Sharp", "Ricoh", "Savin", "Konica Minolta", "Brother", "Epson", "FP Mailing Solutions", "Dell", "DocuWare", "Datto", "WatchGuard", "Microsoft 365", "Zultys", "Wellsys", "FloWater", "Manitowoc", "Follett", "NEWCO", "Bunn"]
INDUSTRIES = [  # slug, name, image, one-line, body, bullets, faq
    ["legal", "Legal", "assets/mps-1-1200.jpg",
     "Firms print, scan and file more than almost any other business, and every page can be billed or lost.",
     "Law firms run on paper they cannot afford to misplace. Kelly configures multifunction devices for scan-to-matter and cost recovery by client code, builds DocuWare workflows for case files with retention rules, and keeps in-house print centers running for filings that outsourced print cannot turn around in time.",
     ["Scan-to-matter and cost recovery by client or matter code", "Secure print release so confidential documents are not left on the tray", "DocuWare case files with retention and audit trail", "In-house production for briefs, exhibits and closing binders"],
     [["Can you integrate with our practice management system?", "Usually. Tell us which one and we will say plainly what the integration covers before you sign anything."], ["Do you handle secure disposal of old devices?", "Ask about hard drive wiping or destruction when a device is returned. We will tell you the process for your model and what record you receive."]]],
    ["healthcare", "Healthcare", "assets/mps-2-1200.jpg",
     "Practices need print that protects patient information and keeps working at seven in the morning.",
     "Medical and dental practices print referrals, forms and records all day, often across more than one site. Kelly sets up secure print release, secure fax, and DocuWare records with the access controls a compliance review expects, and services every site from the nearest branch.",
     ["Secure print release and secure fax where the device supports it", "DocuWare patient and HR records with role-based access", "Fleet monitoring so toner and service happen before the front desk notices", "Multi-site practices served from five North Carolina branches"],
     [["Are your devices and workflows HIPAA-aware?", "DocuWare and the devices are configured with the controls a HIPAA review looks for: access control, audit trail, and encryption where the device supports it. Your compliance officer confirms the policy; we build to it."], ["What happens when a device fails during clinic hours?", "Call the branch. Devices under a Kelly agreement are dispatched first, to factory-trained technicians from the nearest branch. Ask for the response terms in writing."]]],
    ["faith-based", "Faith-based", "assets/production-print-1200.jpg",
     "Bulletins, mailings and programs every week, on a budget that answers to a congregation.",
     "Churches and ministries produce a remarkable amount of print: weekly bulletins, event programs, mailings, curriculum. Kelly right-sizes production print for the volume you run, adds folding and stapling inline, and keeps the cost per piece visible so the finance committee can see it too.",
     ["Production print with inline folding, stapling and booklet making", "Mailing equipment for member communications", "Water and coffee service for fellowship spaces", "Pricing built for nonprofit budgets, with lease and rental options"],
     [["We are a small church. Is this for us?", "Yes. Right-sizing is the point. Bring a year of copy-shop invoices to the assessment; the plan prices a small production device beside them."], ["Do you offer nonprofit pricing?", "Ask your branch. We will price lease, rental and purchase side by side for your real volume."]]],
    ["architecture", "Architecture and engineering", "assets/wide-format-1200.jpg",
     "Plans, drawings and renderings in house, in color, at the size the job site needs.",
     "Firms that send drawings out lose a day on every revision. Kelly puts wide-format printing and scanning in your office, with the color accuracy renderings need and the speed a submittal deadline needs, and keeps it under the same service agreement as your copiers.",
     ["Wide-format printing and scanning, color and mono", "Plan sets, renderings and presentation boards in house", "Document management for drawings, RFIs and submittals", "One service agreement for wide-format and office devices"],
     [["Can you scan large-format originals?", "Yes. Wide-format scanning and copying is part of the same device family, and we set it up for your drawing standards."], ["How fast can a wide-format device be installed?", "Ask your branch for a date. Installation includes network setup and operator training on the day."]]],
    ["manufacturing", "Manufacturing", "assets/it-1-1200.jpg",
     "Documents available where the work happens, approvals that do not wait on a desk, and IT handled so the plant can focus.",
     "Manufacturers run on documents as much as machines: work orders, quality records, purchase orders, compliance files. Kelly puts document workflow, print and IT under one partner, so the records are where the work happens, approvals move without a paper chase, and the business units are not carrying the IT burden.",
     ["Document workflow with DocuWare for orders, quality and compliance records", "Devices matched to the volume of each department", "Managed IT, backup and firewall so systems stay up", "Faster approvals, less time hunting for paper"],
     [["Can DocuWare handle quality and compliance records?", "Yes. Indexing, retention and audit trail are what it is for. Tell us the standard you are audited against."], ["Do you support multiple shifts?", "Service is scheduled around your production hours. Tell dispatch when the line can spare the device."]]],
]
SERVICES = [  # slug, title, nav label, image, eyebrow, hero heading (with <em>), subhead, benefits (title, body), bullets, extra sections, faq
    ["copiers", "Office products and copiers", "Copiers and printers", "assets/mps-1-1200.jpg", "Office products",
     "The right copier is the one you <em>stop thinking about</em>.",
     "Sharp, Ricoh, Savin, Konica Minolta and Brother printers, copiers, multifunction and wide-format devices, matched to your volume, networked on day one and serviced from the nearest branch.",
     [["Printers", "Desktop and workgroup printers for the pages that never touch the copier."], ["Copiers and multifunction", "Color and mono MFPs from small offices to departmental workhorses, with scanning built in."], ["Wide format", "Plans, drawings and signage in house."], ["Production", "High-volume color and mono with finishing, for organizations that print every day."]],
     ["Lease, rent or buy, priced side by side for your real volume", "Secure print release and scan-to-cloud, available on the devices we recommend", "Trade-in and takeover of devices you already own, where we support the model", "Driver downloads and online training for your team"],
     [["Which brands do you carry?", "Sharp, Ricoh and Savin, Konica Minolta, Brother and Epson, depending on the job. We recommend the device, not the badge."], ["Can we start with one device?", "Yes. Many customers start with a single MFP and add managed print when they see the report."]]],
    ["managed-print", "Managed print services", "Managed print", "assets/dispatch-1200.jpg", "Managed print",
     "Stop counting toner. <em>Start seeing the number.</em>",
     "Printing is an overlooked and undermanaged business function, and many organizations spend up to 30% more than they should on it. Managed print puts the fleet under one agreement: assessment, monitoring and reporting, supplies that arrive before they run out, and one invoice.",
     [["Reduced costs", "One agreement replaces per-device contracts, retail toner and surprise repairs."], ["Automated toner replenishment", "Devices report their own levels; supplies ship before you run out."], ["Enhanced security", "Secure print release, user authentication and device hardening, available on the devices we recommend."], ["Predictable billing", "One monthly invoice that matches your meters."], ["Maximized uptime", "Monitoring flags a failing device before your people do."]],
     ["Assessment of every device, wherever it came from", "Monitoring, with usage reports on the schedule in your agreement", "Leasing and rental options for the fleet the plan recommends", "Quarterly review of cost per page and uptime"],
     [["What does the assessment cost?", "Nothing. The assessment is free and carries no obligation, and you keep the report whether or not you buy."], ["Can you manage devices we did not buy from you?", "Often, yes. The assessment tells you which are worth keeping under agreement and which are costing more than they are worth."]]],
    ["document-management", "Document management", "Document management", "assets/gso-office-1200.jpg", "Document management",
     "Take the paper out of approvals, invoices and files, and <em>keep the audit trail</em>.",
     "DocuWare workflows configured and supported by the Kelly team in North Carolina: accounts payable routing, HR and contract files with retention rules, and search your people will use.",
     [["Reduce costs", "Fewer touches per invoice, fewer lost documents, less storage."], ["Improve security", "Role-based access and an audit trail for every document."], ["Streamline workflows", "Approvals route themselves; nothing waits in a tray."], ["Enhance compliance", "Retention rules and records that survive an audit."], ["Backup and disaster recovery", "Documents that are not in a filing cabinet when the building floods."]],
     ["Accounts payable and approval routing", "HR, contract and case files with retention", "Integration with the systems you already run", "Scanning from your existing Kelly devices"],
     [["Is DocuWare cloud or on premise?", "Either. Most customers choose cloud; we will say which fits your IT and your compliance needs."], ["How long does a first workflow take?", "Ask your branch for a plan. Accounts payable is usually first because it pays back fastest."]]],
    ["production-print", "Production print", "Production print", "assets/production-print-1200.jpg", "Production print",
     "Print rooms that hit the deadline <em>outsourcing cannot</em>.",
     "In-house color and mono production with inline finishing for schools, churches, legal and marketing departments that print every day. Control costs, print on demand, keep confidential work in the building.",
     [["Control costs", "Know the cost per piece, and stop paying rush fees."], ["On-demand printing", "Print the hundred you need today, not the thousand you might need."], ["Confidentiality", "Financials, exams and briefs never leave the building."], ["Enhanced features", "Booklet making, folding, stapling and trimming inline."], ["Consistent results", "The same color on Monday and Friday."]],
     ["High-volume color and mono production systems", "Wide-format for plans, posters and signage", "Operator training and priority service under agreement", "A cost comparison against your current outsourced spend"],
     [["What volume justifies production print?", "Bring your outsourced invoices to the assessment. Bring a year of outsourced invoices to the assessment and the plan shows the comparison."], ["Can you train our operator?", "Yes, on the day of install, and again whenever staff changes."]]],
    ["it-services", "IT services", "IT services", "assets/it-1200.jpg", "IT services",
     "Managed IT from the team that <em>already knows your network</em>.",
     "Managed IT, backup and security with Datto, WatchGuard, Dell and Microsoft 365, plus digital forensic services. Proactive monitoring, fixed monthly invoices, and a help desk with a name.",
     [["Reduced costs", "One monthly number instead of emergency invoices."], ["Proactive monitoring", "Problems found and fixed before they become tickets."], ["Optimized security", "Firewall, endpoint and email protection kept current."], ["Fixed monthly invoices", "Budgetable IT."], ["Maximized uptime", "Backup and disaster recovery you have tested."]],
     ["Managed IT and help desk", "Backup and disaster recovery with Datto", "WatchGuard firewalls, endpoint and email security", "Microsoft 365 licensing and migration", "Digital forensic services"],
     [["Do we have to move everything to you?", "No. Many customers start with backup and security and add the help desk later."], ["What is digital forensics?", "Investigation and recovery of data on devices and systems, for legal, HR and incident response. Ask to speak to the practice lead."]]],
    ["mailing", "Mailing solutions", "Mailing", "assets/postage-1200.jpg", "Mailing solutions",
     "The mailroom nobody thinks about, <em>until it stops</em>.",
     "Postage meters, folder-inserters, mailroom printers, parcel lockers and parcel shipping, with software that keeps records straight and postage discounted.",
     [["Reduced costs", "Discounted postage and fewer trips to the post office."], ["Streamline recordkeeping", "Every piece logged, every department charged correctly."], ["Increase security", "Accountable mail and secure parcel lockers."], ["Right-sized options", "From a desktop meter to a full mailroom."]],
     ["FP postage meters, the only fully IMI-compliant range", "Folder-inserters for statements and invoices", "Parcel lockers for offices, campuses and properties", "Parcel shipping and RemoteOne / MailOne software"],
     [["Can a meter save us money at low volume?", "Often, yes, on postage discounts alone. Bring a month of postage receipts to the conversation."], ["Do you service the mailing equipment?", "Yes, on the same agreement and often the same visit as your copiers."]]],
    ["pure-technology", "Pure Technology: water, ice and coffee", "Water, ice and coffee", "assets/breakroom-1200.jpg", "Pure Technology",
     "Water, ice and coffee, serviced on the <em>same visit as your copier</em>.",
     "Bottleless filtered water coolers from Wellsys and FloWater, commercial ice machines from Manitowoc and Follett, and single-cup and high-volume coffee brewers from Newco and Bunn. One invoice, one technician, one less vendor.",
     [["Water", "Bottleless coolers with filtration your people will drink."], ["Ice", "Commercial ice machines sized for your break room or your production floor."], ["Coffee", "Bean-to-cup and single-serve, with the supplies on schedule."]],
     ["Filter changes and sanitizing on a schedule", "Supplies ordered from the customer portal", "Equipment serviced by the same Kelly team", "Rental and purchase options"],
     [["Why bottleless?", "No jugs to lift, store or run out of, and filtered water from your own building supply."], ["How often are coolers sanitized?", "On the schedule the manufacturer recommends, and we log it. Ask your branch for the interval on your model."]]],
]

BLOG = []  # filled below



def desc(text, n=155):
    """Meta description: whole sentences until the next would pass n characters."""
    out = ""
    for sent in re.split(r"(?<=[.!?])\s+", text.strip()):
        if not sent:
            continue
        cand = (out + " " + sent).strip()
        if len(cand) > n:
            break
        out = cand
    return out or brief(text, n)


def teaser(text):
    """Blog teaser: the first sentence, or two when the first is short."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    t = parts[0]
    if len(t) < 60 and len(parts) > 1:
        t = t + " " + parts[1]
    return t


def brief(text, n=150):
    """First sentence, or the first clause under n characters, always ending in a period."""
    first = text.split(". ")[0].rstrip(".")
    if len(first) <= n:
        return first + "."
    cut = first[:n]
    for sep in (", ", ": ", " and ", " with "):
        i = cut.rfind(sep)
        if i > n // 2:
            return cut[:i].rstrip(",:") + "."
    return cut.rsplit(" ", 1)[0].rstrip(",:") + "."

def post(slug, category, title, standfirst, image, image_alt, chapters, faq, target, cta_href="cost-calculator.html", cta_label="Estimate your print spend"):
    BLOG.append(dict(slug=slug, category=category, title=title, standfirst=standfirst, image=image, image_alt=image_alt,
                     chapters=chapters, faq=faq, target=target, cta_href=cta_href, cta_label=cta_label))


# ------------------------------------------------------------------ the nine posts
post("what-managed-print-costs", "Managed print", "What managed print services cost in North Carolina, and what they replace",
     "The honest answer is a range, and the range depends on four numbers you may not have in front of you. Here is how to find them and what a managed agreement usually replaces.",
     "assets/dispatch-1200.jpg", "A service dispatcher at a desk with two monitors",
     [{"id": "the-four-numbers", "title": "The four numbers that set the price", "paras": [
         "Every managed print quote is built on the same four inputs: how many devices you run, how many mono pages a month, how many color pages a month, and how much service those devices already need. If you do not know the page counts, the meter on each device does. Most organizations are surprised twice: once by the total, and again by how much of it is color.",
         "ul:Device count, including the printers under desks nobody owns;;Mono pages per month, from the meters;;Color pages per month, from the meters;;Service history: how many calls, how many days down",
         "callout:Why the assessment matters|Kelly's assessment collects these four numbers across the whole fleet, including devices we did not sell you, and hands you the report. Our recommendation is that you keep it whether or not you buy."]},
      {"id": "what-it-replaces", "title": "What a managed agreement replaces", "paras": [
         "The price only makes sense against what it removes. Under a managed agreement, toner is included and ships automatically, service is included, and you receive one invoice that matches the meters. Against that you set retail toner, per-device service contracts, emergency repairs, and the hours your own staff spend ordering supplies and chasing technicians.",
         "Printing is an overlooked and undermanaged business function, and many organizations spend up to 30% more than they should on it. The saving is rarely in the device. It is in the toner nobody tracked and the time nobody counted.",
         "pq:The saving is rarely in the device. It is in the toner nobody tracked and the time nobody counted."]},
      {"id": "cost-per-page", "title": "Cost per page, and why blended is the number to watch", "paras": [
         "Vendors quote a mono rate and a color rate. The number that matters is the blended cost per page across your real mix, because a fleet that prints 20% color can cost more per page than one printing all mono at a higher mono rate. Ask any vendor for the blended figure on your volumes, and ask how it changes if color grows.",
         "Our cost calculator uses typical North Carolina rates to show the blended figure for your volumes. It is an estimate; the assessment replaces it with your meters."]},
      {"id": "lease-rent-buy", "title": "Lease, rent or buy: how the agreement changes the total", "paras": [
         "Leasing spreads the device cost over a term and keeps the fleet current. Rental covers a season or a project without a term. Purchase is cheapest over a long life if your volume is stable. Managed print sits on top of any of the three: the agreement covers supplies and service regardless of how you acquired the device.",
         "ul:Lease: predictable, refreshes the fleet, best for steady volume;;Rental: flexible, no term, best for peaks and projects;;Buy: lowest lifetime cost for stable volume, highest up-front"]},
      {"id": "questions-to-ask", "title": "Five questions to ask before you sign", "paras": [
         "ul:What is the blended cost per page on our volumes, and what happens if color grows?;;What is the response commitment, and for which devices?;;What is included in service, and what is excluded?;;How are overages billed, and how are meters read?;;Who owns the devices at the end of the term?",
         "A good provider answers all five in writing. Kelly does, and the answers are in the plan we hand you after the assessment."]}],
     [["Is managed print only for large companies?", "No. A ten-device office often benefits most, because nobody is watching the toner."], ["Can we keep our current devices?", "Often, yes. The assessment tells you which are worth keeping under agreement."], ["How fast can an agreement start?", "Ask your branch. Monitoring can usually be installed on existing devices within days."]],
     "what does managed print services cost")

post("unraveling-ins-outs-copier-lease", "Copiers", "Copier lease vs. buy vs. rent: the decision in one page",
     "Three ways to acquire the same device, three different totals. The right one depends on your volume, your cash preference and how fast your needs change.",
     "assets/mps-1-1200.jpg", "Business people near a copier in a hallway",
     [{"id": "the-three-options", "title": "The three options, plainly", "paras": [
         "A lease spreads the cost over a fixed term, usually 36 to 60 months, and typically ends with an upgrade. A rental has no long term and is priced by the month. A purchase is a capital expense you own outright. Service and supplies are separate decisions in all three, unless you put the device under a managed print agreement.",
         "ul:Lease: fixed monthly payment, fleet stays current, best for steady, predictable volume;;Rental: month to month, best for a season, a project or an uncertain year;;Purchase: highest up-front cost, lowest lifetime cost if the device runs for many years"]},
      {"id": "kinds-of-lease", "title": "Three kinds of lease, and the end-of-term question", "paras": [
         "A fair market value lease has the lowest payment and ends with a choice: return the device, buy it at its market value, or renew. A dollar-out lease has a higher payment and ends with ownership for one dollar. An installment purchase agreement finances a purchase over the term. Before signing any of them, ask for the end-of-term buyout price in writing, and ask your accountant whether a Section 179 deduction changes the math for a purchase in the current tax year.",
         "ul:Fair market value: lowest payment, return, buy or renew at the end;;Dollar-out: higher payment, you own it at the end;;Installment purchase: financing a purchase, on your balance sheet from day one"]},
      {"id": "when-leasing-wins", "title": "When leasing wins", "paras": [
         "Leasing wins when your volume is steady and you want the fleet refreshed on a schedule. It also wins when cash is better used elsewhere. The lease payment is predictable and the technology does not age in place.",
         "callout:Watch the end of term|Ask what happens at the end: return, buy out, or renew. A lease with an automatic renewal clause and no reminder is how organizations pay for devices they no longer use."]},
      {"id": "when-renting-wins", "title": "When renting wins", "paras": [
         "Renting wins for peaks and projects: a tax season, an election cycle, a campus move, a temporary office. A firm in its busy season can rent production capacity for three months and hand it back. It also wins when a business is changing fast and does not want a five-year commitment."]},
      {"id": "when-buying-wins", "title": "When buying wins", "paras": [
         "Buying wins when volume is stable, the device will run for six or more years, and cash is available. The cost per month over the life is lowest. The risk is technology: a device bought today is the device you have in year seven.",
         "pq:The right answer is usually a mix. Lease the workhorses, rent the peak, buy the desktop printers."]},
      {"id": "what-kelly-does", "title": "How Kelly prices it", "paras": [
         "The plan we hand you after an assessment prices lease, rental and purchase side by side for your real volumes, with service and supplies shown separately so you can see what a managed agreement adds. Then you decide."]}],
     [["Can we lease from Kelly and buy the supplies elsewhere?", "You can. Most customers do not, once they see the managed rate, but it is your choice."], ["What lease terms do you offer?", "Ask your branch. Terms are matched to the device's expected life and your refresh preference."], ["Can a rental become a lease?", "Often, yes. Ask before you sign the rental so the terms allow it."]],
     "copier lease charlotte nc")

post("document-management-how-it-works-and-why-it-matters", "Document management", "Document management: how it works and why it matters",
     "A document management system is not a scanner and a folder. It is the rules that move a document from arrival to approval to archive without a person carrying it. Here is what that looks like inside a business.",
     "assets/doc-mgmt-1200.jpg", "A quality control checklist on a laptop",
     [{"id": "what-it-is", "title": "What a document management system does", "paras": [
         "Documents arrive by scan, email or upload. The system reads them, files them by the fields that matter (vendor, amount, matter, patient), routes them to whoever has to act, records every action, and archives them under a retention rule. Search finds them in seconds. Nobody carries a folder.",
         "ul:Capture from scanners, email and existing systems;;Indexing by the fields your business uses;;Workflow: approvals that route themselves;;Retention and audit trail;;Search your people will use"]},
      {"id": "accounts-payable", "title": "Why accounts payable usually goes first", "paras": [
         "Invoices are the highest-volume, most repetitive document in most organizations, and the cost of touching each one is measurable. Routing invoices to approvers automatically, matching them to purchase orders and archiving them with the approval record is the workflow with the fastest payback. It is where Kelly usually starts.",
         "pq:Accounts payable goes first because the payback is fastest."]},
      {"id": "compliance", "title": "Compliance and the audit trail", "paras": [
         "Regulators and auditors ask the same question in different words: who saw this document, who changed it, and when. A document management system answers that automatically. Retention rules keep records exactly as long as policy requires and destroy them when it says to, with the record of destruction.",
         "callout:Compliance standards a document management system supports|Access controls, audit trails, retention schedules, encryption at rest and in transit, and records of destruction. Your compliance officer sets the policy; the system enforces it."]},
      {"id": "security", "title": "Security and disaster recovery", "paras": [
         "A filing cabinet is not backed up. A document management system is, in a data center, with role-based access that a filing cabinet never had. When a pipe bursts over the records room, the records are still there."]},
      {"id": "getting-started", "title": "How Kelly builds it", "paras": [
         "Kelly configures and supports DocuWare in North Carolina, scanning from the Kelly devices you already have. We start with one workflow, usually accounts payable, prove it, then add HR, contracts or case files. Ask your branch for a plan."]}],
     [["Cloud or on premise?", "Either. Most customers choose cloud."], ["Does it work with our accounting system?", "Usually. Tell us which one and we will say what the integration covers."], ["How long does a first workflow take?", "Ask for a plan. Accounts payable usually goes first because the payback is fastest. Ask for a plan with dates."]],
     "document management compliance", "what-we-do.html#document-management", "Talk to us about document management")

post("how-managed-print-services-transforms-business", "Managed print", "The first ninety days of managed print: what changes",
     "Not a philosophy. A calendar. Here is what happens in a business in the first three months after the fleet goes under one agreement, and the three costs nobody counted before.",
     "assets/mps-2-1200.jpg", "Business people at a copier",
     [{"id": "the-three-costs", "title": "The three costs nobody counts", "paras": [
         "Retail toner bought in a hurry. Staff time spent ordering supplies and waiting on hold. Downtime while a device waits for a part. None of these appears on an invoice labelled print, which is why organizations spend up to 30% more than they should on it.",
         "ul:Toner bought retail, often the wrong cartridge;;Staff hours on ordering, tracking and chasing;;Downtime, and the workarounds around it"]},
      {"id": "days-1-30", "title": "Days 1 to 30: the assessment and the plan", "paras": [
         "The assessment walks every device, reads every meter, and records the service history. The plan that follows prices lease, rental and purchase side by side for the fleet the data recommends, which is usually fewer devices, better placed.",
         "callout:What you receive|A fleet and cost report, yours to keep, and a plan with the three acquisition options priced against your real volumes."]},
      {"id": "days-31-60", "title": "Days 31 to 60: install, connect, train", "paras": [
         "Devices arrive on a date you chose, go on the network the same day, and every user is trained before the technician leaves. Monitoring is switched on. The first toner ships before anyone asks."]},
      {"id": "days-61-90", "title": "Days 61 to 90: the first report", "paras": [
         "The first usage report shows pages, color share, uptime and cost per page by device. This is usually the first time anyone in the business has seen the number. It is also where the conversation about color policy starts.",
         "pq:The first report is usually the first time anyone in the business has seen the number."]},
      {"id": "after-90", "title": "After ninety days: the loop", "paras": [
         "Quarterly, the numbers are reviewed and the plan adjusted. If a device is underused, it moves. If color grew, the policy or the device changes. Then back to the assessment. That loop is what managed means."]}],
     [["Will we lose devices we like?", "Only if the data says they cost more than they are worth, and only if you agree."], ["Who reads the meters?", "The devices do, automatically, under monitoring."], ["What if a device fails in week two?", "Under agreement the response is same day, and The technician is factory-trained."]],
     "benefits of a managed print service")

post("workstation-management-an-overview", "Office IT", "Workstation management: why the desk PC is where most support tickets start",
     "Servers get the attention. Workstations get the tickets. Here is what managed workstation support changes for a fifty-person office, and what it costs to leave alone.",
     "assets/it-1200.jpg", "A technician checking a small office server rack",
     [{"id": "where-tickets-start", "title": "Where the tickets start", "paras": [
         "In most small and mid-sized offices the majority of IT interruptions begin at a desk: an update that did not run, a laptop that did not back up, a browser extension nobody installed on purpose. Each one costs the person an hour and someone else two.",
         "ul:Patching and updates that run on a schedule, not when someone remembers;;Endpoint security that is current;;Backup of the files that live on the machine;;Asset records: who has what, and when it is due for replacement"]},
      {"id": "what-managed-means", "title": "What managed workstation support means", "paras": [
         "Every workstation is enrolled, monitored and patched centrally. Security software reports in. Backups run and are tested. When a machine misbehaves, the help desk sees it before the user calls, and often fixes it remotely.",
         "callout:The named help desk|Kelly's IT services include a help desk with a name. Your people know who they are talking to, and so do we."]},
      {"id": "security", "title": "Security starts at the endpoint", "paras": [
         "Many breaches begin with an email opened at a desk. WatchGuard firewalls, endpoint protection and email security, kept current across every machine, close the door that is most often left open.",
         "pq:Many breaches begin with an email opened at a desk."]},
      {"id": "lifecycle", "title": "Lifecycle: replace on a plan, not on a failure", "paras": [
         "A workstation that dies on a Monday costs a day and a rush purchase. A fleet on a replacement plan costs a budget line. Managed support includes the asset record that makes the plan possible."]},
      {"id": "with-kelly", "title": "Why the copier company", "paras": [
         "Kelly's devices are already on your network, and our technicians already know your building. Adding workstation support to the same relationship means one vendor, one invoice and one number to call."]}],
     [["Do you support Mac and Windows?", "Windows workstations. Ask about Mac for your office."], ["Can you work alongside our internal IT person?", "Yes. Many customers keep one person in house and use Kelly for monitoring, patching and after-hours."], ["What does onboarding look like?", "An inventory, enrollment of every machine, then monitoring. Ask your branch for the plan."]],
     "workstation support", "what-we-do.html#it", "Talk to us about IT services")

post("clean-water-cooler-step-by-step-guide", "Pure Technology", "How to sanitize an office water cooler, step by step",
     "What to do between service visits, how often a cooler needs a proper sanitize, and the signs a cooler is overdue.",
     "assets/breakroom-1200.jpg", "An office break room with a filtered water cooler and coffee machine",
     [{"id": "how-often", "title": "How often a cooler needs sanitizing", "paras": [
         "Manufacturers recommend sanitizing coolers on a regular schedule and replacing filters on their rated interval. On bottleless units like Wellsys and FloWater, the sanitize and the filter change are largely a technician service; what the office does between visits is keep the touch points clean and watch for the signs below.",
         "callout:Ask your branch|If your cooler is under a Kelly agreement, sanitizing and filter changes are on the schedule for your model and logged. Ask for the interval."]},
      {"id": "what-you-need", "title": "What you need", "paras": [
         "ul:A sanitizer approved for food preparation surfaces, or a mild vinegar solution;;Clean cloths;;The manual, for the drip tray and any parts your model lets you remove"]},
      {"id": "the-steps", "title": "Between service visits", "paras": [
         "ul:Wipe the taps and buttons daily with the approved sanitizer;;Empty and wash the drip tray;;Wipe the exterior and the area around the unit;;If your model has a removable nozzle or tray, wash it as the manual directs;;Never drain or open a hot tank without letting it cool first;;Leave reservoir sanitizing to the scheduled technician visit",
         "pq:Clean what people touch. Leave the tank to the technician."]},
      {"id": "signs-overdue", "title": "Signs a cooler is overdue", "paras": [
         "Off taste or odor, slow flow, visible film in the drip tray, or water that is not cold. Any one means call for the sanitize and check the filter date."]},
      {"id": "why-bottleless", "title": "Why offices are moving to bottleless", "paras": [
         "No jugs to lift, store or run out of, and filtered water from your own building supply. Kelly installs and services Wellsys and FloWater coolers across North Carolina, on the same visit as your copier."]}],
     [["Can Kelly sanitize our cooler for us?", "Yes. Under a Pure Technology agreement it is on the schedule for your model and logged."], ["How do I know when the filter is due?", "The service log and the interval for your model. Ask your branch."], ["Do you service coolers you did not install?", "Often, yes. Tell the branch the make and model."]],
     "how to sanitize a water cooler", "what-we-do.html#pure", "Talk to us about water, ice and coffee")

post("all-in-one-office-printer-options-navigating-the-market-for-the-best-choice", "Copiers", "All-in-one office printers: when one device is enough, and when it is not",
     "For a small office one multifunction device can do everything. Here is how to tell whether you are that office, and what to look for in duty cycle, security and cost per page.",
     "assets/hero-1200.jpg", "A technician kneeling beside an open office copier",
     [{"id": "one-device", "title": "When one device is enough", "paras": [
         "A small team with moderate, mostly mono volume in one location is usually well served by one multifunction device that prints, copies, scans and faxes. The savings are real: one contract, one toner type, one thing to service."]},
      {"id": "when-not", "title": "When it is not", "paras": [
         "ul:Two teams who both need the device at 9am;;Color volume that grows every quarter;;Confidential printing that should not sit on a shared tray;;A second floor",
         "The fix is rarely a bigger device. It is usually two right-sized devices placed where the work is."]},
      {"id": "duty-cycle", "title": "Duty cycle, and why it matters more than speed", "paras": [
         "Every device has a recommended monthly volume. Run it at twice that and it will fail early and often. Run it at half and you overpaid. Ask for the recommended monthly volume, not the maximum, and match it to your meters.",
         "pq:Ask for the recommended monthly volume, not the maximum."]},
      {"id": "security", "title": "Security on a shared device", "paras": [
         "Secure print release, user authentication, hard drive encryption and a plan for the drive when the device leaves. These are configuration choices, and they should be made at install."]},
      {"id": "cost-per-page", "title": "The cost per page is the price", "paras": [
         "A cheap device with expensive toner costs more in a year than a dearer device with a managed rate. Ask for the blended cost per page on your volume before you compare device prices."]}],
     [["Which all-in-one brands does Kelly carry?", "Sharp, Ricoh, Savin, Konica Minolta and Brother, matched to the job."], ["Can we add managed print to a single device?", "Yes. One device, one agreement, the same monitoring and supplies."], ["Can you network it for us?", "Yes, on the day of install, with every user trained."]],
     "best all in one printer small business", "what-we-do.html#copiers", "Talk to us about copiers")

post("wide-format-printer-buying-guide-making-the-right-decision", "Wide format", "Wide-format printing in house: the volume at which it pays for itself",
     "Plans, signage and drawings from the print shop cost a day and a delivery fee each time. Here is when the device pays for itself and what to look for.",
     "assets/wide-format-1200.jpg", "A wide-format inkjet printer",
     [{"id": "who-uses-it", "title": "Who prints wide format", "paras": [
         "Architecture and engineering firms for plan sets and renderings. Contractors for site drawings. Retailers and schools for signage and posters. Marketing teams for event graphics. Anyone who sends a file out and waits a day for it."]},
      {"id": "the-math", "title": "The math", "paras": [
         "Add up a year of print-shop invoices and delivery fees, then add the hours lost waiting for revisions. Compare it to the monthly cost of a device under agreement, including ink and media. Bring a year of outsourced print invoices to the assessment; the plan shows the comparison.",
         "callout:Bring the invoices|Bring a year of outsourced print invoices to the assessment. The comparison is the plan."]},
      {"id": "what-to-look-for", "title": "What to look for", "paras": [
         "ul:Print and scan in one device, so drawings can be copied and archived;;Color accuracy for renderings, not just line work;;Media handling: rolls, sheet sizes, cutting;;Network integration with your CAD or design software;;Service under the same agreement as your office devices"]},
      {"id": "scanning", "title": "Scanning large originals", "paras": [
         "Wide-format scanning turns paper drawings into files your document management system can index. For firms with decades of archived plans, that is often the reason to buy.",
         "pq:For firms with decades of archived plans, scanning is often the reason to buy."]},
      {"id": "with-kelly", "title": "How Kelly sets it up", "paras": [
         "Installation includes network setup and operator training on the day. Ink and media can be on automatic replenishment. Service comes from the nearest of five branches, with priority for devices under agreement."]}],
     [["Can a wide-format device print on vinyl or canvas?", "Some can. Tell us what you need to print and we will recommend the media path."], ["How much space does it need?", "About the footprint of a large copier, plus room for rolls. We measure before we recommend."], ["Do you offer wide format on rental?", "Yes, for projects and peaks."]],
     "large format printer solutions", "what-we-do.html#copiers", "Talk to us about wide format")

post("same-day-service-what-it-means", "Service", "What same-day service means, and the questions to ask any dealer",
     "Every dealer says fast. Here is what a real service commitment looks like in writing, how to read a response-time promise, and why an audited NPS matters more than a testimonial.",
     "assets/gso-office-1200.jpg", "Inside the Kelly Greensboro office",
     [{"id": "response-vs-resolution", "title": "Response time is not resolution time", "paras": [
         "Response is when a technician is scheduled or arrives. Resolution is when the device works. A dealer can promise a fast response and still leave you down for days waiting on parts. Ask for both numbers, and ask what share of calls are resolved on the first visit.",
         "callout:Ask about parts|Whether the technician arrives with the likely parts for your model is the single biggest factor in first-visit resolution. Ask any dealer how they stock the truck."]},
      {"id": "in-writing", "title": "Get it in writing, with conditions", "paras": [
         "A real commitment names the devices it covers, the hours it applies to, and what happens when it is missed. Ask any dealer, Kelly included, for the response commitment in writing for your agreement.",
         "pq:A promise without conditions is a slogan. A promise with conditions is a contract."]},
      {"id": "nps", "title": "Why an audited NPS beats a testimonial", "paras": [
         "Anyone can post a good review. Net Promoter Score measured by an independent third party cannot be edited by the dealer. Kelly's NPS is collected and audited by CEO Juice, an independent company whose process the dealer does not control. Kelly's score is 94.4; the industry average is in the 70s."]},
      {"id": "local", "title": "Why local still matters", "paras": [
         "A technician who is forty minutes away arrives in forty minutes. Kelly serves the Triad, Charlotte and the Triangle from five branches, and customers with field offices across North Carolina from the nearest one."]},
      {"id": "questions", "title": "The questions to ask any dealer", "paras": [
         "ul:What is your response commitment, in hours, for my devices, and where is it written?;;What share of service calls do you resolve on the first visit?;;Do your technicians carry parts?;;Who measures your customer satisfaction, and can I see it?;;Where is the nearest technician to my office?"]}],
     [["Is there a response commitment on every device?", "Commitments apply to devices under a Kelly agreement. Ask your branch for the terms, in writing."], ["What about weekends?", "Ask your branch for the coverage on your agreement."], ["How do I request service?", "The customer portal, the branch number, or 1-800-34-KELLY."]],
     "office equipment repair near me charlotte", "service-support.html#request", "Request service")


INDUSTRY_HEADINGS = {"legal": "Every page <em>billed, filed or found</em>.", "healthcare": "Clinic technology that <em>works at seven in the morning</em>.", "faith-based": "Bulletins, programs and mailings, <em>on a congregation's budget</em>.", "architecture": "Plans and drawings, <em>printed in-house</em>.", "manufacturing": "Documents where the work happens, <em>IT handled</em>."}
INDUSTRY_QUOTES = {"legal": lambda: [TAX_SEASON, TESTIMONIALS[3][:3]], "healthcare": lambda: [TESTIMONIALS[1][:3], TESTIMONIALS[0][:3]], "faith-based": lambda: [TESTIMONIALS[2][:3], TAX_SEASON], "architecture": lambda: [TESTIMONIALS[0][:3], TESTIMONIALS[1][:3]], "manufacturing": lambda: [TESTIMONIALS[2][:3], TESTIMONIALS[0][:3]]}

def industry_page(slug, name, image, one, body, bullets, faq):
    return {"crumbs": [["Home", "index.html"], ["Industries", "industries.html"], [name, f"industries/{slug}.html"]], "file": f"industries/{slug}.html", "title": f"Office technology for {name.lower()} | Kelly Office Solutions",
            "description": f"{one} Copiers, managed print, document management and IT for {name.lower()} across North Carolina, from five local offices.",
            "sections": [
                {"type": "hero", "layout": "centered", "eyebrow": f"Key markets: {name}", "heading": INDUSTRY_HEADINGS.get(slug, one), "subhead": one,
                 "primary": {"label": "Request an assessment", "href": "contact.html"}, "secondary": {"label": PHONE, "href": PHONE_HREF},
                 "image": image, "image_alt": f"{name} at work", "image_w": 1200, "image_h": 800},
                {"type": "detail", "eyebrow": "What we set up", "heading": f"Built for how {name.lower()} uses paper and technology", "body": body, "bullets": bullets},
                {"type": "testimonials", "alt": True, "heading": "What customers in North Carolina say", "items": INDUSTRY_QUOTES.get(slug, lambda: [TESTIMONIALS[0][:3], TESTIMONIALS[2][:3]])()},
                {"type": "faq", "heading": f"Questions from {name.lower()}", "items": faq},
                {"type": "leadform", "alt": True, "id": "assessment", "heading": "Start with the assessment", "body": "A specialist from your nearest branch walks your fleet and your workflows, and writes it up.", "submit": "Request my assessment", "note": "A person from the nearest branch replies, not an autoresponder."},
            ]}


def location_page(slug, city, a1, a2, phone, phone_href, region):
    lat_lng = {"winston-salem": (36.0999, -80.2442), "greensboro": (36.0726, -79.7920), "charlotte": (35.2271, -80.8431), "raleigh": (35.7796, -78.6382), "swansboro": (34.6877, -77.1194)}[slug]
    eyebrow = "Headquarters" if slug == "winston-salem" else f"{city} branch"
    towns = CHARLOTTE_TOWNS if slug == "charlotte" else None
    served = ", ".join(towns[:-1]) + " and " + towns[-1] if towns else region
    area = towns if towns else region
    hours_text = "Monday to Friday, 8 to 5." if slug in HOURS_CONFIRMED else "Call the branch for hours."
    hours_schema = {"openingHoursSpecification": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "17:00"}} if slug in HOURS_CONFIRMED else {}
    return {"crumbs": [["Home", "index.html"], ["Locations", "locations.html"], [city, f"locations/{slug}.html"]], "file": f"locations/{slug}.html", "title": f"Copier Sales, Lease and Rental in {city}, NC | Kelly Office Solutions",
            "description": f"Kelly Office Solutions in {city}: copier sales, lease, rental and repair, managed print, document management and IT for businesses across {region}. {a1}, {a2}. {phone}.",
            "schema": [{"@context": "https://schema.org", "@type": "LocalBusiness", "@id": f"https://kellyofficesolutions.com/locations/{slug}#branch", "name": f"Kelly Office Solutions {city}",
                        "parentOrganization": {"@id": "https://kellyofficesolutions.com/#organization"}, "image": "https://kelly-office-solutions.vercel.app/assets/gso-office-1200.jpg",
                        "telephone": phone.replace("(", "+1-").replace(") ", "-"), "url": f"https://kellyofficesolutions.com/locations/{slug}",
                        "address": {"@type": "PostalAddress", "streetAddress": a1, "addressLocality": city, "addressRegion": "NC", "postalCode": a2.split()[-1], "addressCountry": "US"},
                        "geo": {"@type": "GeoCoordinates", "latitude": lat_lng[0], "longitude": lat_lng[1]},
                        "areaServed": area, **hours_schema,
                        "sameAs": ["https://www.linkedin.com/company/kelly-office-solutions/"]}],
            "sections": [
                {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": f"<em>{city}</em> copiers, managed print and IT, serviced locally.",
                 "subhead": f"The Kelly {city} branch serves {served} with sales, service dispatch and supplies. Call the branch, or 1-800-34-KELLY reaches all five.",
                 "primary": {"label": f"Call {phone}", "href": phone_href}, "secondary": {"label": "Request an assessment", "href": "contact.html"},
                 "image": "assets/kelly-team-1024.jpg", "image_alt": "A Kelly technician beside a Kelly service van", "image_w": 1024, "image_h": 576,
                 "badge": {"value": "Local", "label": "Technicians dispatched from this branch"}},
                {"type": "cards", "alt": True, "eyebrow": f"In {city}", "heading": f"What the {city} branch does", "items": [
                    ["Copier sales, lease and rental", f"Sharp, Ricoh, Savin, Konica Minolta and Brother devices for {city} offices, installed and networked by the local team."],
                    ["Copier and printer repair", f"Fast local response from the nearest branch across {region}, by factory-trained technicians from the nearest branch."],
                    ["Managed print", "Assessment, monitoring and automatic supplies for the whole fleet."],
                    ["Document management and IT", "DocuWare workflows, managed IT, backup and security from the same local team."],
                    ["Mailing solutions", "Postage meters, folder-inserters and parcel lockers."],
                    ["Water, ice and coffee", "Bottleless coolers, ice machines and coffee, serviced on the same visit."]]},
                {"type": "locations", "heading": f"Visit or call the {city} branch", "intro": f"{hours_text} {a1}, {a2}.", "items": [[city, a1, a2, phone, phone_href]]},
                {"type": "testimonials", "alt": True, "heading": "What North Carolina customers say", "items": [TESTIMONIALS[1][:3], TAX_SEASON]},
                {"type": "faq", "heading": f"Questions we get in {city}", "items": [
                    [f"Do you serve businesses outside {city}?", f"Yes. The {city} branch covers {region}, and customers with offices elsewhere in North Carolina are served from the nearest of our five branches."],
                    ["How fast can you get a technician to us?", "Devices under a Kelly agreement are dispatched first, from the nearest branch. Ask the branch for the response terms of your agreement, in writing."],
                    ["Can we lease a copier locally?", "Yes. The plan prices lease, rental and purchase side by side for your real volume."]]},
                {"type": "leadform", "id": "assessment", "heading": f"Start with an assessment in {city}", "body": "A specialist from the branch walks your fleet and your workflows, and writes it up.", "submit": "Request my assessment", "note": "A person from the branch replies, not an autoresponder."},
            ]}


SERVICE_TITLES = {"managed-print": "Managed Print Services in Charlotte and the Triad", "pure-technology": "Office Water, Ice and Coffee Service", "copiers": "Copiers and Printers: Sales, Lease and Rental"}
SERVICE_DISPLAY = {"it-services": "IT services", "pure-technology": "Pure Technology", "copiers": "copiers and printers", "managed-print": "managed print", "document-management": "document management", "production-print": "production print", "mailing": "mailing solutions"}


SERVICE_SLUGS = [x[0] for x in SERVICES]
SERVICE_DETAIL_IMAGE = {"copiers": "assets/printer-1200.jpg", "managed-print": "assets/mps-2-1200.jpg", "document-management": "assets/gso-office-1200.jpg", "production-print": "assets/wide-format-1200.jpg", "it-services": "assets/forensics-1200.jpg", "mailing": "assets/folder-inserter-1200.jpg", "pure-technology": "assets/coffee-1200.jpg"}


# Per-service signature modules: a process chart and a before/after for each line. Every line is on kellyofficesolutions.com
# or in the FP Mailing Solutions material already cited; nothing is a promise Kelly has not made in writing.
def _flow(fid, eyebrow, heading, intro, steps, receive_label="What you receive"):
    return {"type": "flow", "id": fid, "alt": True, "eyebrow": eyebrow, "heading": heading, "intro": intro, "receive_label": receive_label,
            "steps": [{"label": a, "when": b, "summary": c, "title": d, "body": e, "receive": f} for a, b, c, d, e, f in steps]}

def _ba(bid, heading, b_title, b_body, b_items, a_title, a_body, a_items, b_eyebrow="Today", a_eyebrow="With Kelly"):
    return {"type": "beforeafter", "id": bid, "eyebrow": "Before and after", "heading": heading,
            "before": {"eyebrow": b_eyebrow, "title": b_title, "body": b_body, "items": b_items},
            "after": {"eyebrow": a_eyebrow, "title": a_title, "body": a_body, "items": a_items}}

SERVICE_MODULES = {
    "copiers": [
        _ba("ba", "Drag to compare buying a copier with having Kelly place one",
            "A device chosen from a brochure", "Priced on the badge, not on the pages you print.",
            ["Bought on speed and price, sized by guesswork", "Networked later by whoever is free", "Toner ordered when the light comes on", "Service from a number on a sticker", "Lease, rental and purchase never compared"],
            "A device chosen from your meter counts", "Sharp, Ricoh, Savin, Konica Minolta or Brother, matched to your volume.",
            ["Right-sized from a free assessment of what you print", "Networked and every user trained on install day", "Supplies shipped on usage under managed print", "Serviced from the nearest of five North Carolina offices", "Lease, rental and purchase priced side by side"]),
        _flow("flow", "From first call to first page", "Five steps between the call and the first page", "Click a step. Each one ends with something in your hands.",
            [("Assess", "Visit 1", "Count and meter the fleet.", "A free assessment of what you have", "A specialist counts every device, reads the meters and works out cost per page, mono and color. Free and without obligation, as it says on our managed print page.", ["Fleet inventory with meters", "Cost per page by device", "The recommendation in writing"]),
             ("Recommend", "Week 1", "The device and the terms.", "The right device, priced three ways", "A model matched to your volume and finishing needs, with lease, rental and purchase shown side by side.", ["Model and configuration", "Lease, rent and buy compared", "Service and supplies shown separately"]),
             ("Install", "A date you choose", "Networked the same visit.", "Delivered, networked and trained", "The device arrives on the day you chose, joins your network, and every user is trained before the technician leaves.", ["Drivers and scan destinations set up", "Users trained on site", "Old device removed if you ask"]),
             ("Support", "Ongoing", "One number for service and supplies.", "Service and supplies from one number", "1-800-34-KELLY reaches all five offices. Request service, submit meter reads and order supplies online in under a minute each.", ["Online service request", "Meter reads and supplies online", "Technicians dispatched from the nearest branch"]),
             ("Review", "Under agreement", "Reports every six months.", "The numbers, every six months", "Under a managed print agreement, service and usage reports arrive every six months so the fleet is adjusted on evidence.", ["Service call history", "Device utilization", "Executive snapshot"])])],
    "managed-print": [
        _ba("ba", "Drag to compare a fleet that is managed with one that is not",
            "Every printer on its own", "Nobody knows what the fleet costs because nobody owns it.",
            ["Toner bought at retail when a device runs dry", "Service calls placed by whoever notices first", "No count of devices, pages or cost", "IT staff clearing jams between real work", "Devices replaced on age, not on evidence"],
            "One fleet, one report", "Monitored, supplied and reported on a schedule you can see on your invoice.",
            ["Toner ships on usage, before it runs out", "Failing devices spotted before the office does", "Cost per page by device, mono and color", "IT time returned to IT", "Consolidate, upgrade or relocate on the data, every six months"])],
    "document-management": [
        _ba("ba", "Drag to see what changes when documents live in DocuWare",
            "Paper and shared drives", "Filing cabinets, email attachments and a shared drive with three versions of everything.",
            ["Invoices approved by walking them to a desk", "Contracts found by asking who had them last", "HR files in a locked cabinet nobody can search", "Compliance evidence assembled by hand", "Remote staff waiting for a scan"],
            "Indexed, routed, searchable", "Scan from any Kelly MFP straight into workflows the office already follows.",
            ["Invoices routed for approval the moment they are scanned", "Any document found by a search, from any office", "Access by role, with a record of who saw what", "Retention rules applied automatically", "The same view at home as at the desk"]),
        _flow("flow", "How a DocuWare rollout runs", "Four stages, and the first one is a conversation", "Click a stage.",
            [("Map", "Week 1", "Where documents come from and go.", "Map how paper moves today", "We sit with the people who handle invoices, contracts and personnel files and draw how each one travels, who touches it and where it waits.", ["Process maps for the workflows chosen", "Index fields agreed per document type", "A scope you sign off"]),
             ("Configure", "Weeks 2 to 3", "Cabinets, indexes and routes.", "Build the cabinets and the routes", "Document trays, index fields, approval routes and permissions are configured to the map, and your MFPs get scan-to-DocuWare buttons.", ["Configured file cabinets", "Approval workflows", "Scan destinations on every MFP"]),
             ("Train", "Go-live week", "Everyone who touches a document.", "Train the people, not just the admins", "Short sessions by role, with the office's own documents, before the first live scan.", ["Role-based training", "Quick guides at each MFP", "A named contact for the first month"]),
             ("Refine", "First quarter", "Adjust on real use.", "Adjust on what the first quarter shows", "Routes that bottleneck get changed, new document types get added, and the next department is scoped.", ["Usage review", "Route adjustments", "Plan for the next workflow"])])],
    "production-print": [
        _ba("ba", "Drag to compare outsourcing with printing it in-house",
            "Sent to a print shop", "Two days out, a rush fee back, and a box that arrives short.",
            ["Booklets, proposals and manuals sent out", "Rush charges for the meeting that moved", "Color that varies from run to run", "Minimum quantities and leftover boxes", "Confidential documents leaving the building"],
            "Printed down the hall", "Ricoh and Savin production systems with inline finishing, operated by your own people.",
            ["Booklets stapled, folded and trimmed inline", "Print the quantity you need, the morning you need it", "Color consistency all day", "Confidential material stays in-house", "Operator training included"])],
    "it-services": [
        _ba("ba", "Drag to compare break-fix IT with managed IT",
            "Call when it breaks", "Every problem is a surprise, and every invoice is a different size.",
            ["Backups nobody has tested", "Updates applied when someone remembers", "Security that ends at the antivirus", "An hourly invoice after every outage", "The copier company and the IT firm blaming each other"],
            "Managed, monitored, one invoice", "Monitoring, backup, security and Microsoft 365 for a fixed monthly amount, from the same team that services your copiers.",
            ["Backups monitored and tested", "Patching on a schedule", "Layered security with Datto and WatchGuard", "A fixed monthly invoice", "One partner for the printer and the network it sits on"]),
        _flow("flow", "How managed IT starts", "Four steps to a network someone is watching", "Click a step.",
            [("Audit", "Week 1", "Every device, user and risk.", "A network and security audit", "Every workstation, server, user account and backup is inventoried, and the gaps are listed in plain English.", ["Asset inventory", "Risk list, ranked", "A recommendation in writing"]),
             ("Plan", "Week 2", "Fix, replace, monitor.", "A plan with a fixed monthly number", "What to fix now, what to replace, what to monitor, and the monthly amount that covers it.", ["Remediation list", "Monthly scope and price", "Microsoft 365 licensing reviewed"]),
             ("Onboard", "Weeks 3 to 4", "Agents, backup, security.", "Monitoring and protection go live", "Monitoring agents, backup and security tools are deployed, and users learn how to reach the help desk.", ["Monitoring on every device", "Backup running and verified", "Help desk live"]),
             ("Run", "Ongoing", "Reviewed on a schedule.", "Run, report and review", "Patching, backup checks and security alerts are handled as they arise, and the plan is reviewed with you on a schedule.", ["Patch and backup reports", "Security alerts handled", "Scheduled review"])])],
    "mailing": [
        _ba("ba", "Drag to compare stamps with an FP postage meter",
            "Stamps and the post office", "A trip, a queue, and full retail postage on every piece.",
            ["Retail postage on every letter", "Trips to the post office", "Hand-folded, hand-stuffed mailings", "No record of what postage was spent where", "Meter compliance nobody has checked"],
            "Metered, in the mailroom", "FP Mailing Solutions meters, folder inserters and mailroom printers through Kelly.",
            ["Save up to five cents per stamp and up to 40 percent on priority labels", "Postage printed at your desk, at commercial rates", "Folded, inserted and sealed by machine", "Postage tracked by department", "The only fully IMI-compliant meter range"])],
    "pure-technology": [
        _ba("ba", "Drag to compare jugs and a coffee service with Pure Technology",
            "Jugs, a delivery and a coffee vendor", "Two more vendors, two more invoices, and a break room that runs out.",
            ["Five-gallon jugs lifted onto a cooler", "Deliveries missed, water run out", "A coffee vendor on a separate contract", "Ice from a machine nobody services", "Nobody checking the filter date"],
            "Bottleless, filtered, serviced with the copier", "Wellsys, FloWater, Newco and Bunn equipment, on the same agreement and visit as your office technology.",
            ["Bottleless water and ice, filtered on site", "Single-cup or high-volume coffee", "Serviced on the same visit as the copier", "Filters changed on schedule", "One invoice for the whole break room"])],
}

def service_page(slug, title, navlabel, image, eyebrow, heading, subhead, benefits, bullets, faq):
    secs = [
        {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": heading, "subhead": subhead,
         "primary": {"label": "Request an assessment", "href": "contact.html"}, "secondary": {"label": "Request service", "href": "service-support.html#request"},
         "image": image, "image_alt": title, "image_w": 1200, "image_h": 800},
        {"type": "cards", "alt": True, "eyebrow": "Benefits", "heading": f"What changes with Kelly {SERVICE_DISPLAY.get(slug, title.lower().split(':')[0])}", "items": benefits},
        {"type": "detail", "eyebrow": "What is included", "heading": "What you get", "body": "In one agreement, on one invoice: " + ", ".join(b[0][0].lower() + b[0][1:] for b in benefits) + ". The list below is what arrives, and when. Nothing on it is an add-on.", "bullets": bullets, "image": SERVICE_DETAIL_IMAGE.get(slug, image), "flip": True},
    ]
    for i, m in enumerate(SERVICE_MODULES.get(slug, [])):
        secs.insert(2 + i, m)
    if slug == "production-print":
        secs.insert(2, {"type": "video", "heading": "Production print, in ninety seconds", "intro": "Josh from Kelly walks through what an in-house production system does.", "video": "assets/production-print-josh.mp4", "poster": "assets/vimeo-poster.jpg", "caption": "From kellyofficesolutions.com"})
    if slug == "managed-print":
        secs.insert(2, {"type": "process", "eyebrow": "How managed print works at Kelly", "heading": "Three stages you can see on your invoice", "stages": [
            ["Assessment", "Produces: a fleet and cost report, yours to keep."],
            ["Monitoring and reporting", "Produces: toner before it runs out, and service and usage reports every six months."],
            ["Leasing and rental", "Produces: the fleet the data recommends, priced lease, rental or purchase, side by side."]]})
        secs.insert(3, {"type": "flow", "id": "assessment-steps", "alt": True, "eyebrow": "The assessment, step by step", "heading": "Four steps, and you keep the report either way", "intro": "The four steps on our managed print page, and what each one leaves you with.",
            "receive_label": "What you leave with",
            "steps": [
                {"label": "Assess", "when": "Step 1", "summary": "The fleet you have.", "title": "Assess the fleet you have", "body": "A Kelly specialist evaluates your current imaging fleet for size, efficiency and cost, and talks with the people who use it about how the work flows.", "receive": ["Every device counted, located and metered", "Cost per page by device, mono and color", "Interviews with the staff who print most"]},
                {"label": "Plan", "when": "Step 2", "summary": "The fleet you should have.", "title": "Plan the fleet you should have", "body": "Recommendations to make workflows run smoother: consolidating or upgrading devices, moving a copier closer to the people who use it, or retiring the one that costs more than it is worth.", "receive": ["Consolidate, upgrade or relocate", "Priced as lease, rental or purchase", "Nothing replaced that the data does not justify"]},
                {"label": "Measure", "when": "Step 3", "summary": "Agree what success looks like.", "title": "Agree what success looks like", "body": "Lower supply and maintenance cost, or IT time back for real work. We agree the measure with you and show how the data will prove it.", "receive": ["Targets you set, not ones we pick", "Baseline captured before anything changes", "Reporting that shows the movement"]},
                {"label": "Manage", "when": "Step 4", "summary": "Problems never reach your staff.", "title": "Manage it so problems never reach your staff", "body": "Next steps reviewed with your team, then a proactive approach that spots a failing device or an empty toner before anyone in the office does.", "receive": ["Monitoring on every device", "Supplies shipped on usage, not on a call", "Priority service under agreement"]}]})
        secs.insert(4, {"type": "cards", "eyebrow": "Monitoring and reporting", "heading": "Five reports, every six months, in plain English", "intro": "Depending on fleet size you receive service and usage reports with detailed summaries. These are the five.",
            "items": [["Service call history", "Every call, who made it, what the issue was and when it was resolved."],
                      ["Supplies order", "Exactly what you spend on toner and supplies, so you can budget for it."],
                      ["Device utilization", "Which devices carry the load and which sit idle, so you can consolidate or upgrade with evidence."],
                      ["Device list and charts", "Every printer and copier, where it sits, and its mono and color counts."],
                      ["Executive snapshot", "Overall fleet performance with red flags for overuse or age, and the plan to resolve them before they stop work."]]})
        secs.append({"type": "comparison", "heading": "Lease, rent or buy?", "intro": "The plan prices all three for your real volume. Here is how they usually compare.",
                     "columns": [{"label": "Lease", "recommended": True}, {"label": "Rent"}, {"label": "Buy"}],
                     "rows": [["Best for", "Steady volume, a fleet kept current", "Peaks, projects, uncertain years", "Stable volume, long device life"],
                              ["Term", "36 to 60 months, typically", "Month to month", "None"],
                              ["Up-front cost", "Low", "Low", "Highest"],
                              ["Lifetime cost", "Moderate", "Highest per month", "Lowest if the device runs for years"],
                              ["Technology refresh", "Built in at end of term", "Any time", "When you buy again"],
                              ["Service and supplies", "Managed agreement, or separate", "Usually included", "Managed agreement, or separate"]],
                     "note": "Terms and rates are set in the plan after the assessment. Nothing here is a quote."})
    secs += [
        {"type": "testimonials", "alt": True, "heading": "What customers say", "items": [TESTIMONIALS[(SERVICE_SLUGS.index(slug)) % 4][:3], ([TAX_SEASON] + [t[:3] for t in TESTIMONIALS])[(SERVICE_SLUGS.index(slug) + 2) % 5]]},
        {"type": "faq", "heading": "Questions we get about " + SERVICE_DISPLAY.get(slug, title.lower().split(":")[0]), "items": faq},
        {"type": "leadform", "alt": True, "id": "assessment", "heading": "Start with the assessment", "body": "A specialist from your nearest branch walks your fleet and your workflows, and writes it up.", "submit": "Request my assessment", "note": "A person from the nearest branch replies, not an autoresponder."},
    ]
    return {"file": f"services/{slug}.html", "title": f"{SERVICE_TITLES.get(slug, title)} | Kelly Office Solutions", "description": desc(subhead), "crumbs": [["Home", "index.html"], ["Services", "what-we-do.html"], [navlabel, f"services/{slug}.html"]], "sections": secs}


def blog_post_page(p, others):
    related = [[o["category"], o["title"], teaser(o["standfirst"]), f"blog/{o['slug']}.html", o["image"]] for o in others[:3]]
    faq_items = p["faq"]
    return {"file": f"blog/{p['slug']}.html", "title": f"{p['title']} | Kelly Office Solutions", "description": desc(p["standfirst"]),
            "schema": [{"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["standfirst"],
                        "image": f"https://kelly-office-solutions.vercel.app/{p['image']}", "author": {"@type": "Organization", "name": "Kelly Office Solutions"},
                        "publisher": {"@id": "https://kellyofficesolutions.com/#organization"}, "mainEntityOfPage": f"https://kellyofficesolutions.com/blog/{p['slug']}",
                        "datePublished": "2026-09-01", "dateModified": "2026-09-06", "articleSection": p["category"]}],
            "sections": [
                {"type": "article", "category": p["category"], "heading": p["title"], "standfirst": p["standfirst"], "image": p["image"], "image_alt": p["image_alt"],
                 "date_label": "September 2026", "read": f"{max(4, sum(len(' '.join(c['paras'])) for c in p['chapters']) // 1100)} min read", "chapters": p["chapters"],
                 "author": {"name": "The Kelly team", "role": "Service and sales, North Carolina"}},
                {"type": "faq", "alt": True, "heading": "Questions this guide gets asked", "items": faq_items},
                {"type": "leadform", "id": "guide", "heading": p["cta_label"], "body": "Tell us a little about your office and the nearest branch will call to set a time. Or estimate first with the cost calculator.", "submit": "Request my assessment", "note": "A person from the nearest branch replies, not an autoresponder."},
                {"type": "related", "heading": "Keep reading", "items": related},
            ]}


# slug, group, title, image, one-line, body (from kellyofficesolutions.com, rewritten), benefits [[title, body]], bullets, faq [[q, a]], brands
PRODUCT_GROUPS = ["Print and imaging", "Mail and shipping", "Water, ice and coffee", "Technology and software"]
PRODUCTS = [
    ["printers", "Print and imaging", "Printers", "assets/printer-1200.jpg",
     "Single-function printers, sized to how many your office needs.",
     "Single-function printers are an essential part of an imaging fleet, and the easiest part to over-buy. Before the next purchase, the question is how many printers the office truly needs to keep work moving, whether they should be color or mono, and what each one costs to own once maintenance and consumables are counted. Your Kelly representative presents options that fit your output and your budget.",
     [["Right-sized", "How many, where, and color or mono, decided from your real volume."], ["Total cost of ownership", "Price, maintenance and consumables, so the cheap device does not cost the most."], ["Serviced locally", "Installed, networked and supported from the nearest Kelly branch."]],
     ["Color and mono, desktop to workgroup", "Sharp, Brother, Epson, Ricoh, Savin and Konica Minolta", "Drivers and manuals linked from our support page", "Can join a managed print agreement"],
     [["Should we buy printers or a multifunction device?", "Often one multifunction device replaces several printers and costs less to run. The assessment shows the numbers for your office."], ["Do you service printers we bought elsewhere?", "Often, yes. Ask the branch with the model number."]],
     ["Brother", "Epson", "Sharp", "Ricoh", "Savin", "Konica Minolta"]],
    ["copiers", "Print and imaging", "Copiers", "assets/mps-1-1200.jpg",
     "Modern office copiers with software that does more than duplicate.",
     "Producing copies is still part of daily work, so a copier is standard equipment for most teams. The devices have moved a long way from their origins: with software and integrations, an upgraded office copier scans to your systems, controls who prints what, and reports its own usage. Kelly matches the device to your volume and keeps it running.",
     [["Software and integrations", "Scan to email, folders and document management; user codes and secure release."], ["Matched to volume", "Speed and duty cycle chosen from your meter reads, not a brochure."], ["Serviced same day", "Under a Kelly agreement, by factory-trained technicians from the nearest branch."]],
     ["Ricoh, Savin, Konica Minolta and Sharp", "Lease, rent or buy", "Networked and trained on install day", "Meter reads read automatically under agreement"],
     [["Lease or buy?", "Depends on volume and how long you will keep it. Our lease, rent or buy guide walks through it, and the assessment prices all three."], ["How fast is service?", "Fast local response from the nearest branch across our North Carolina service area."]],
     ["Sharp", "Ricoh", "Savin", "Konica Minolta"]],
    ["multifunction-printers", "Print and imaging", "Multifunction printers", "assets/hero-1200.jpg",
     "Print, scan, copy and fax in one device, networked to the whole team.",
     "The versatility of multifunction printers makes them the workhorse of most offices. One device prints, scans, copies and faxes, so you maintain and supply one machine instead of four. Networked to every workstation, one MFP can serve a team or a whole small office, and printing costs drop with it.",
     [["One device, four jobs", "Print, scan, copy and fax, with one set of consumables."], ["Lower running cost", "Maintenance and supplies for one machine rather than several."], ["Networked to everyone", "Every workstation prints to it; scans land where the work is."]],
     ["A3 and A4, color and mono", "Secure print release and user authentication", "Scan to DocuWare, email and cloud folders", "Included in managed print reporting"],
     [["What size MFP do we need?", "Volume and the biggest paper you print decide it. The assessment counts both."], ["Can it replace our fax line?", "Most MFPs fax, and many offices move to scan-to-email instead. Ask the branch what fits."]],
     ["Sharp", "Ricoh", "Savin", "Konica Minolta", "Brother"]],
    ["wide-format-printers", "Print and imaging", "Wide format printers", "assets/wide-format-1200.jpg",
     "Signage, window graphics and blueprints, printed in-house instead of outsourced.",
     "Sometimes a letter-size sheet does not cut it. Large print jobs are a reality for many industries, and outsourcing them adds up. A wide format printer produces large-scale, high-resolution output in-house: signage for a medical practice, advertising for a storefront window, or blueprints for an engineering firm.",
     [["Stop outsourcing", "Print the poster, the plan set and the banner the day you need it."], ["High resolution", "Crisp output at large sizes for graphics and technical drawings alike."], ["Right media", "Paper, vinyl and technical stock, chosen for the job."]],
     ["Epson and Ricoh wide format", "Architects, engineers, schools, retailers and churches", "Serviced from the nearest branch", "Ink and media on the supplies portal"],
     [["Is a wide format printer worth it for a small firm?", "If you outsource plan sets or signage more than a few times a month, usually yes. Bring last year's print invoices to the assessment."], ["Can you scan large drawings too?", "Some models scan and copy large format. Tell us what you need to capture."]],
     ["Epson", "Ricoh"]],
    ["production-printers", "Print and imaging", "Production printers", "assets/production-print-1200.jpg",
     "High-volume print with booklet, binding and stapling finishing, in-house.",
     "Need to print at high volume or produce a specific finished piece, a booklet or a manual? Production printers are designed for large quantities and offer finishing options like binding and stapling. Schools, churches, legal and marketing departments bring the print shop in-house and control the schedule.",
     [["Volume without the wait", "Thousands of pages an hour, finished as they print."], ["Finishing inline", "Booklets, stapling, folding and binding on the device."], ["Color you can trust", "Consistent color from the first sheet to the last."]],
     ["Ricoh and Savin production systems", "Booklet makers, stackers and folders", "Operator training included", "Watch Josh walk through a system on the production print page"],
     [["How is this different from a big copier?", "Speed, paper handling, finishing and color consistency. A production system is built to run all day."], ["Can we rent one for a season?", "Yes. Rental fits a busy season or a project."]],
     ["Ricoh", "Savin"]],
    ["postage-meters", "Mail and shipping", "Postage meters", "assets/postage-1200.jpg",
     "Weigh, rate and print exact postage, at commercial rates, from your own mailroom.",
     "Postage meters have become standard for businesses that send medium or large volumes of mail. They are digitally connected, automate mailroom processes, and weigh, rate and print exact postage. A meter earns discounted rates compared to stamps. Kelly partners with FP Mailing Solutions, whose meter range is fully IMI compliant.",
     [["Discounted postage", "Commercial rates on every piece; savings on stamps and priority labels add up."], ["Exact postage", "Weighed and rated automatically, so nothing is over- or under-paid."], ["IMI compliant", "FP's range meets the current USPS standard, so the meter stays usable."]],
     ["FP Mailing Solutions meters", "Password-protected usage tracking", "Reporting for budgets and chargebacks", "RemoteOne and MailOne software options"],
     [["How much mail justifies a meter?", "If someone is buying stamps or making post office runs every week, a meter usually pays for itself. Ask the branch to size it."], ["What does IMI compliant mean?", "USPS's current standard for postage evidencing. FP's line meets it fully, so you are not buying a meter with an expiry date."]],
     ["FP Mailing Solutions"]],
    ["folder-inserters", "Mail and shipping", "Folder inserters", "assets/folder-inserter-1200.jpg",
     "Fold, stuff and seal large mailings automatically, accurately and fast.",
     "Folder inserters process and send large volumes of mail quickly. An adjustable feeder and automated folding and inserting system replace the manual labor of stuffing each envelope, so invoices, statements and direct mail go out faster and more accurately. Ideal for any office that processes customer invoices or marketing mailings regularly.",
     [["Hours back", "The envelope stuffing afternoon disappears."], ["Accuracy", "The right pages in the right envelope, every time."], ["Speed", "Large runs finished in a fraction of the manual time."]],
     ["FP folder inserters, sized to your run", "Invoices, statements, notices and direct mail", "Pairs with a postage meter and mailroom printer", "Installed and trained by Kelly"],
     [["What volume makes a folder inserter worthwhile?", "Regular runs of a few hundred pieces or more. Tell us your monthly mailings and we will size it."], ["Can it handle different insert sets?", "Yes. Multiple feeders handle different inserts per envelope."]],
     ["FP Mailing Solutions"]],
    ["mailroom-printers", "Mail and shipping", "Mailroom printers", "assets/mailroom-printer-1200.jpg",
     "Envelope, address and label printers with a lower cost per print than your MFP.",
     "Printers designed for mailroom work, envelope printers, address printers and label printers, are essential for businesses that send direct mail. They offer a low cost per print compared with an office multifunction device, with the speed and versatility a mailroom needs. If your office prints envelopes, address labels or return labels regularly, a dedicated mailroom printer is the answer.",
     [["Lower cost per print", "Cheaper than running envelopes through the office copier."], ["Fast", "Built for runs of envelopes and labels, not the occasional sheet."], ["Compact", "Sits on the mailroom counter beside the meter."]],
     ["FP envelope, address and label printers", "Direct mail, statements and returns", "Pairs with folder inserters and meters", "Supplies through the Kelly portal"],
     [["Why not use the copier for envelopes?", "It works, slowly, and costs more per envelope. A mailroom printer is built for it."], ["Do you set it up with our mailing software?", "Yes. Installation includes the mailing workflow."]],
     ["FP Mailing Solutions"]],
    ["parcel-lockers", "Mail and shipping", "Parcel lockers", "assets/lockers-1200.jpg",
     "Secure, contactless package pickup for offices, campuses and properties.",
     "Parcel lockers provide a secure, practical and contactless way to receive packages. E-commerce has multiplied parcel volume, and anyone who accepts items on behalf of recipients, property managers, campuses, offices, feels it. Lockers benefit the whole chain, from carrier to recipient, and have become the expected solution since the pandemic.",
     [["Secure", "Packages wait behind a locked door, not on a desk."], ["Contactless", "Recipients collect with a code, on their schedule."], ["Less staff time", "No more signing for, storing and chasing parcels."]],
     ["Indoor and outdoor configurations", "Offices, apartments, campuses and clinics", "Notifications to recipients", "Installed and supported by Kelly"],
     [["Who uses parcel lockers?", "Property managers, campuses, multi-tenant offices and any reception that has become a package room."], ["Do lockers need power and network?", "Yes for notifications and codes. We plan the location with you."]],
     ["FP Mailing Solutions"]],
    ["mailing-software", "Mail and shipping", "Mailing software: parcel shipping, FP Sign, RemoteOne and MailOne", "assets/it-1-1200.jpg",
     "Ship with tracking, sign documents electronically, and account for every dollar of postage.",
     "FP Parcel Shipping is a step-by-step online program that produces shipping labels with tracking and offers insurance for extra security. FP Sign lets businesses exchange, sign and manage critical documents online, which suits legal, accounting and medical work. RemoteOne manages, tracks and routes mail from anywhere, and MailOne gives accounting departments integrated mailing, shipping and three-tier cost accounting for FP equipment.",
     [["Parcel shipping", "Labels with tracking and optional insurance from your desk."], ["FP Sign", "Contracts, offers, forms and certificates signed digitally and reliably."], ["RemoteOne and MailOne", "Remote mail management, and postage accounting that reduces spend."]],
     ["Works with FP meters and mailroom equipment", "Three-tier accounting for chargebacks", "Legal, accounting and medical use cases for e-signature", "Set up and trained by Kelly"],
     [["Do we need FP hardware to use the software?", "MailOne extends FP equipment. Parcel Shipping and FP Sign can be discussed on their own. Ask the branch."], ["Is FP Sign legally valid?", "Electronic signatures are widely accepted. Confirm requirements for your specific documents with your counsel."]],
     ["FP Mailing Solutions"]],
    ["mailroom-accessories", "Mail and shipping", "Mailroom accessories", "assets/gso-office-1200.jpg",
     "Pressure sealers, letter openers, joggers, scales and furniture that make the mailroom run.",
     "Alongside meters, inserters and printers, the FP partnership lets Kelly supply the rest of the mailroom: pressure sealers for secure, tamper-evident documents; letter openers running from 24,000 to 40,000 pieces an hour; mailroom furniture that steadies equipment and cuts service calls; paper joggers that align stacks for accurate processing; power line conditioners for stable supply; and postal scales for exact postage.",
     [["Pressure sealers", "Quick, secure, tamper-evident mailings."], ["Letter openers", "Models from 24,000 to 40,000 pieces an hour."], ["Scales, joggers and furniture", "The supporting cast that keeps the equipment accurate and up."]],
     ["Pressure sealers and letter openers", "Paper joggers and postal scales", "Power line conditioners", "Mailroom furniture"],
     [["Do small offices need any of this?", "Usually a scale and a sealer. The rest scales with volume."]],
     ["FP Mailing Solutions"]],
    ["water-coolers", "Water, ice and coffee", "Water coolers", "assets/water-1200.jpg",
     "Purified water on tap, for the office that wants people hydrated and at their desks.",
     "Employers are required to provide drinking water, but lukewarm tap water impresses neither customers nor staff. Purified water tastes better and keeps people hydrated, and the walk to the cooler and back is a small reset that helps focus. A water cooler is one of the most affordable upgrades an office can make, and cheaper than stocking sodas.",
     [["Purified, filtered water", "Bottleless systems from Wellsys and FloWater, no jugs to lift or store."], ["Sanitizing on schedule", "Under a Kelly agreement, cleaning and filter changes are scheduled and logged."], ["Serviced with your copier", "One visit, one invoice, one number."]],
     ["Wellsys and FloWater bottleless coolers", "Hot, cold and sparkling options by model", "Filters and cups on the supplies portal", "Cleaning guide on our blog"],
     [["Bottleless or bottled?", "Bottleless filters your building water, so there is nothing to deliver, lift or run out of. It is what we install most."], ["How often is it cleaned?", "On the schedule for your model under agreement. Ask the branch for the interval."]],
     ["Wellsys", "FloWater"]],
    ["ice-machines", "Water, ice and coffee", "Ice machines", "assets/ice-1200.jpg",
     "Energy-efficient commercial ice, up to 125 pounds a day, from a compact footprint.",
     "Kelly's ice machines are energy-efficient, reliable and built with sanitation and purity as the priorities. Compact units deliver up to 125 pounds of ice a day, with a wide selection of water filters, serving systems and accessories. Ordering is easy, delivery is fast, and installation is professional and simple.",
     [["Up to 125 lb a day", "Enough for a busy office or clinic, from a small footprint."], ["Sanitation first", "Built and filtered for clean, pure ice."], ["Installed and serviced", "Delivery, installation and support from the branch."]],
     ["Manitowoc and Follett", "Filters, serving systems and accessories", "Compact footprint", "Serviced on the same visit as your other equipment"],
     [["Where does an office put an ice machine?", "Breakroom, clinic supply room, or beside the water cooler. It needs water, power and a drain."], ["How is it cleaned?", "On a schedule under agreement, with filter changes logged."]],
     ["Manitowoc", "Follett"]],
    ["coffee-brewers", "Water, ice and coffee", "Coffee brewers", "assets/coffee-1200.jpg",
     "Single-cup to high-volume brewers, with beans and supplies delivered on your schedule.",
     "A coffee break helps people recharge, and a cup offered to a visitor is hospitality that builds a reputation. Whether you want a single-cup brewer or a higher-volume machine, Kelly carries brewers from leading brands that are customizable, easy to use and energy-efficient, and delivers the beans, filters and cups to go with them.",
     [["Single-cup to high volume", "Sized to the office, from the front desk to the plant breakroom."], ["Supplies on schedule", "Beans, filters and cups ordered on the portal or delivered on a cadence."], ["One vendor", "Coffee, water and copier serviced by the same people."]],
     ["Newco and Bunn brewers", "Bean-to-cup and single-serve options", "Supplies on the Kelly portal", "Serviced from the nearest branch"],
     [["Do you supply the coffee too?", "Yes. Beans, filters and cups, on a schedule or on demand."], ["Can we try a brewer first?", "Ask the branch. Trials are often possible."]],
     ["NEWCO"]],
    ["managed-it", "Technology and software", "Managed IT services", "assets/it-1-1200.jpg",
     "Monitoring, security, backup and support for a fixed monthly invoice.",
     "Managing an IT infrastructure, hardware, software, network and security, is costly and time-consuming, and an in-house expert can be the highest-paid person on staff. Managed IT from Kelly puts your systems under proactive monitoring and maintenance, on site and remote, for a fixed monthly invoice, so your teams focus on the work instead of the interruptions.",
     [["Proactive monitoring", "Issues found and fixed before they become problems; patches and updates handled."], ["Security", "Protection against ransomware, breaches and downtime, with WatchGuard and Datto."], ["Fixed monthly invoice", "Service, support and maintenance under one predictable bill."]],
     ["Remote monitoring, security and network management", "Intrusion prevention and detection", "Managed cloud, backup, retention and restore", "Workstation and server management", "Disaster planning, wireless, telecom carrier and vendor consulting", "Project management and consultation"],
     [["What does Managed IT include?", "Remote monitoring, security management, network management, intrusion prevention and detection, managed cloud, backup and restore, workstation and server management, consultation, project management, disaster planning, telecom carrier consulting, wireless implementation and vendor management."], ["Do you replace our IT person?", "Often we extend them. The assessment shows what should be managed and what should stay in-house."]],
     ["Datto", "WatchGuard", "Dell", "Microsoft 365", "Zultys"]],
    ["digital-forensics", "Technology and software", "Digital forensic services", "assets/forensics-1200.jpg",
     "Court-recognized examiners who recover, preserve and interpret digital evidence.",
     "Digital forensics reveals what a user did: documents accessed, deleted or transferred, and internet activity. Kelly's examiners are current and former law enforcement officers specializing in cyber operations, hold numerous forensic certifications, and have been recognized as experts in state and federal courts. They recover voice, video, image and metadata from mobile devices, even when deleted, and conduct social media research and archiving for legal cases.",
     [["Breach response analysis", "Indicators of compromise, incident timeline, network and account information, malware and vulnerabilities."], ["Mobile device investigations", "Forensic images of phones and tablets; keyword, pattern, PII and card data searches."], ["Employee misuse investigations", "Reviews of users accused of violating policy and acceptable use."]],
     ["Indicator of Compromise checks on disk and in memory", "RapidCheck for point-of-sale compromise and card exposure", "Litigation support, depositions and expert testimony", "Information security monitoring and electronic discovery", "Law enforcement support"],
     [["Who hires digital forensics?", "Attorneys in civil and criminal matters, employers investigating misconduct, and organizations responding to a breach."], ["Will the findings hold up in court?", "Our examiners have been recognized as computer forensics experts in state and federal courts and provide expert witness testimony."]],
     []],
    ["docuware", "Technology and software", "DocuWare document management", "assets/doc-mgmt-1200.jpg",
     "Cloud document management: find any file in seconds, route approvals automatically.",
     "Every day a company creates contracts, proposals, invoices, manuals and more, scattered across devices and filing cabinets. A document management system creates, stores, indexes, protects, tracks and retrieves digital files, in the cloud, from anywhere, in seconds. Kelly configures and supports DocuWare for North Carolina offices: accounts payable routing, HR files, contracts, with the compliance controls legal, accounting and healthcare require.",
     [["Reduce costs", "Gartner puts a lost document at $120 and a reproduced one at $220. Storage space goes too."], ["Security and compliance", "Control who sees what, with a full activity trail for regulated industries."], ["Automated workflows", "Scanned documents route to the right person for review, approval and payment."]],
     ["DocuWare cloud, configured by the Kelly team", "Version control and audit trail", "Backup and disaster recovery built in", "Integrates with your MFPs' scan workflows"],
     [["How long does a DocuWare rollout take?", "Depends on the first workflow. Accounts payable is the usual start. Ask the branch for a scoping call."], ["Does it work with our copiers?", "Yes. Scan straight into indexed DocuWare workflows from Kelly MFPs."]],
     ["DocuWare"]],
]
PRODUCT_HEADINGS = {'printers': 'Printers that <em>earn their desk space</em>.', 'copiers': 'Copiers that <em>do more than copy</em>.', 'multifunction-printers': 'One device. <em>Print, scan, copy, fax.</em>', 'wide-format-printers': 'Big print, <em>printed in-house</em>.', 'production-printers': 'Your print shop, <em>down the hall</em>.', 'postage-meters': 'Exact postage, <em>at commercial rates</em>.', 'folder-inserters': 'The envelope-stuffing afternoon, <em>gone</em>.', 'mailroom-printers': 'Envelopes and labels, <em>done right</em>.', 'parcel-lockers': 'Packages, <em>secured and collected</em>.', 'mailing-software': 'Ship, sign and account, <em>from one screen</em>.', 'mailroom-accessories': 'Everything else <em>the mailroom needs</em>.', 'water-coolers': 'Better water, <em>no jugs</em>.', 'ice-machines': '125 pounds of ice a day, <em>from a small footprint</em>.', 'coffee-brewers': 'Good coffee, <em>and someone who brings the beans</em>.', 'managed-it': 'IT that is <em>watched before it breaks</em>.', 'digital-forensics': 'Digital evidence, <em>recognized in court</em>.', 'docuware': 'Any document, <em>in seconds</em>.'}
PRODUCT_INDEX = {p[0]: p for p in PRODUCTS}


def product_page(slug, group, title, image, one, body, benefits, bullets, faq, brands):
    siblings = [q for q in PRODUCTS if q[1] == group and q[0] != slug][:3]
    extra = []
    if slug == "multifunction-printers":
        extra.append(dict(STORY3D, id="device", alt=True, cta=None))
    if slug in ("copiers", "printers", "production-printers", "wide-format-printers"):
        extra.append(dict(FLEET, alt=True, heading="The rest of the fleet"))
    secs = [
        {"type": "hero", "layout": "split", "eyebrow": group, "heading": PRODUCT_HEADINGS[slug], "subhead": one,
         "primary": {"label": "Request a quote", "href": "contact.html"}, "secondary": {"label": "Talk with your branch", "href": "locations.html"},
         "image": image, "image_alt": title, "image_w": 1200, "image_h": 800},
        {"type": "detail", "eyebrow": "What to know", "heading": f"About {title.lower() if not title.startswith(('DocuWare', 'FP')) else title}", "body": body, "bullets": bullets, "image": image, "flip": True},
        {"type": "cards", "alt": True, "eyebrow": "Why it matters", "heading": f"What {title.split(':')[0].lower() if not title.startswith('DocuWare') else 'DocuWare'} changes", "items": benefits},
    ]
    secs[2:2] = extra
    if brands:
        secs.append({"type": "partners", "caption": "Brands Kelly carries for this", "items": brands})
    secs.append({"type": "faq", "eyebrow": "Questions", "heading": "Asked on most first calls", "items": faq})
    if siblings:
        secs.append({"type": "resources", "alt": True, "heading": f"More in {group.lower()}", "intro": "Every product Kelly sells is serviced by Kelly.", "items": [[q[1], q[2], brief(q[4], 110), "See the product", f"products/{q[0]}.html"] for q in siblings]})
    secs.append({"type": "leadform", "id": "quote", "heading": f"Get a quote on {title.split(':')[0].lower() if not title.startswith('DocuWare') else 'DocuWare'}", "body": "Tell us the volume and the office. A specialist from the nearest branch replies with options and prices.", "submit": "Request a quote", "note": "No obligation. We answer the phone too: " + PHONE + "."})
    return {"file": f"products/{slug}.html", "title": f"{title.split(':')[0]} | Kelly Office Solutions, North Carolina", "description": brief(one + " " + body, 155),
            "crumbs": [["Home", "index.html"], ["Products", "products.html"], [title.split(':')[0], f"products/{slug}.html"]], "sections": secs}


def products_index():
    secs = [{"type": "hero", "layout": "centered", "eyebrow": "Products", "heading": "Every product Kelly sells, <em>serviced by Kelly</em>.", "subhead": "Copiers to coffee brewers, postage meters to parcel lockers, managed IT to digital forensics. One partner, five North Carolina branches, one number.",
             "primary": {"label": "Request an assessment", "href": "contact.html"}, "secondary": {"label": "Estimate your print spend", "href": "cost-calculator.html"}}]
    secs.append(dict(FLEET, alt=True))
    for i, g in enumerate(PRODUCT_GROUPS):
        items = [[p[2], brief(p[4], 120), f"products/{p[0]}.html"] for p in PRODUCTS if p[1] == g]
        intro = {"Print and imaging": "Sharp, Ricoh, Savin, Konica Minolta, Brother and Epson devices, matched to your volume.",
                 "Mail and shipping": "Through our partnership with FP Mailing Solutions, the whole mailroom from one supplier.",
                 "Water, ice and coffee": "Pure Technology: the breakroom, serviced on the same visit as the copier.",
                 "Technology and software": "Managed IT, digital forensics and DocuWare, from the same people who service your fleet."}[g]
        secs.append({"type": "services", "id": g.lower().replace(" ", "-").replace(",", ""), "alt": bool(i % 2), "heading": g, "intro": intro, "items": items})
    secs.append({"type": "leadform", "alt": True, "id": "quote", "heading": "Not sure which product?", "body": "Start with the assessment. A specialist walks the office, counts what you have and prices what you need.", "submit": "Request an assessment", "note": "A person from the nearest branch replies."})
    return {"file": "products.html", "title": "Products | Copiers, printers, mailing, water, ice, coffee and IT | Kelly Office Solutions", "description": "Every product Kelly Office Solutions sells and services in North Carolina: printers, copiers, MFPs, wide format, production print, postage meters, folder inserters, parcel lockers, water coolers, ice machines, coffee brewers, managed IT, digital forensics and DocuWare.",
            "crumbs": [["Home", "index.html"], ["Products", "products.html"]], "sections": secs}


import os
MFP_MODEL = "assets/fleet/mfp.glb" if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "kelly-office-solutions", "assets", "fleet", "mfp.glb")) else None

WHEEL_ITEMS = [[x[1], brief(x[6], 140), f"services/{x[0]}.html", x[2]] for x in SERVICES]

FLOW_ENGAGEMENT = {"type": "flow", "id": "flow", "eyebrow": "How an engagement runs", "heading": "Five stages, and every one of them hands you something",
    "intro": "Click a stage. Nothing here is a sales step dressed up as a process; each one produces a document you keep.",
    "steps": [
        {"label": "Assessment", "when": "Week 1", "summary": "Free. One visit, one report.", "title": "A specialist walks the office and counts what you have",
         "body": "Every device located and metered, cost per page by device, and a conversation with the people who print most. Free and without obligation, as it says on our managed print page. You keep the report whether or not you buy.",
         "receive": ["Fleet inventory with meter counts", "Cost per page, mono and color, by device", "The recommendation, in writing"]},
        {"label": "Plan", "when": "Week 2", "summary": "Lease, rent or buy, side by side.", "title": "A right-sized plan priced three ways",
         "body": "Consolidate, upgrade or relocate, with lease, rental and purchase priced on your real volume. Nothing is replaced that the data does not justify.",
         "receive": ["Device plan with placements", "Lease, rental and purchase side by side", "Service and supplies shown separately"]},
        {"label": "Install and connect", "when": "A date you choose", "summary": "Networked and trained the same visit.", "title": "Devices arrive on the day you chose",
         "body": "On the network the day they arrive, every user trained before the technician leaves, monitoring switched on, the first toner shipped before anyone asks.",
         "receive": ["Install and training completed on site", "Monitoring live on every device", "Supplies on automatic replenishment"]},
        {"label": "Monitor and supply", "when": "Ongoing", "summary": "Toner before it runs out.", "title": "The fleet reports on itself",
         "body": "Devices report their own levels and faults. Supplies ship on usage, not on a call. Service and usage reports arrive on the schedule in your agreement, every six months on our managed print page.",
         "receive": ["Supplies shipped on usage", "Service call history and supplies order reports", "Device utilization and executive snapshot"]},
        {"label": "Review", "when": "On schedule", "summary": "Cost per page and uptime, then back to stage one.", "title": "A look at what moved",
         "body": "Cost per page, uptime and what changed since the last report, then adjustments to the plan if the business moved. The cycle starts again from a known number.",
         "receive": ["The five reports, explained in plain English", "Adjustments to the plan", "A fresh baseline for the next period"]}]}

FLEET = {"type": "fleet", "id": "fleet", "heading": "The fleet, at a glance", "intro": "Every device family Kelly sells and services. Generated product renders for the preview; your real models replace them.",
    "items": [
        {"title": "Multifunction copiers", "band": "Workgroup to department", "brands": "Sharp, Ricoh, Savin, Konica Minolta", "image": "assets/fleet/mfp.png", "bullets": ["Print, scan, copy, fax", "Secure release and scan to DocuWare"], "href": "products/multifunction-printers.html"},
        {"title": "Desktop printers", "band": "Desk and small team", "brands": "Brother, Epson, Ricoh", "image": "assets/fleet/printer.png", "bullets": ["Color and mono", "Joins a managed print agreement"], "href": "products/printers.html"},
        {"title": "Wide format", "band": "Plans, posters, signage", "brands": "Epson, Ricoh", "image": "assets/fleet/wide-format.png", "bullets": ["Stop outsourcing plan sets", "Technical and graphics media"], "href": "products/wide-format-printers.html"},
        {"title": "Production print", "band": "High volume, inline finishing", "brands": "Ricoh, Savin", "image": "assets/fleet/production.png", "bullets": ["Booklets, stapling, folding", "Color consistency all day"], "href": "products/production-printers.html"},
        {"title": "Postage meters", "band": "Mailroom", "brands": "FP Mailing Solutions", "image": "assets/fleet/postage.png", "bullets": ["Commercial postage rates", "Fully IMI compliant"], "href": "products/postage-meters.html"},
        {"title": "Water and coffee", "band": "Breakroom", "brands": "Wellsys, FloWater, Newco, Bunn", "image": "assets/fleet/breakroom.png", "bullets": ["Bottleless, filtered", "Serviced with your copier"], "href": "products/water-coolers.html"}]}

SEAL = {"type": "seal", "id": "seal", "eyebrow": "What every Kelly customer gets", "heading": "Not a slogan. A list you can check.",
    "intro": "Each line is on our site or in our agreements today. Nothing here is aspirational.",
    "items": [["Free", "A free, no-obligation assessment", "One visit, one report, yours to keep whether or not you buy."],
              ["94.4", "A service score audited by someone else", "Net Promoter Score collected and audited by CEO Juice. The industry average sits in the 70s."],
              ["1947", "Family-owned since 1947", "Headquartered in Winston-Salem and still independent while the industry consolidated."],
              ["5", "Five North Carolina offices", "Winston-Salem, Greensboro, Charlotte, Raleigh and Swansboro. Technicians dispatched from the nearest one."],
              ["1", "One invoice for the whole office", "Copiers, print, IT, mailing, water and coffee under one agreement and one number."],
              ["A+", "BBB accredited, rated A+", "Accredited by the Better Business Bureau."],
              ["IMI", "The only fully IMI-compliant meter range", "Through our partnership with FP Mailing Solutions."],
              ["6 mo", "Reports every six months", "Service call history, supplies, device utilization, device list and charts, executive snapshot."]],
    "source": "Sources: kellyofficesolutions.com (managed print, mailing, about pages), CEO Juice, the Better Business Bureau."}

BEFORE_AFTER = {"type": "beforeafter", "id": "ba", "eyebrow": "One partner", "heading": "Drag to see what changes when the office has one number to call",
    "before": {"eyebrow": "Today, in most offices", "title": "Seven vendors, seven invoices", "body": "Nobody owns the whole picture, so nobody sees the cost.",
               "items": ["A copier company, a printer reseller and a toner site", "An IT firm that blames the copier company", "A postage meter on its own contract", "A water delivery and a coffee service", "Four numbers to call and nobody who knows your name", "Toner ordered in a hurry at retail"]},
    "after": {"eyebrow": "With Kelly", "title": "One partner, one invoice, one number", "body": "Copiers to coffee, serviced by the same people on the same visit.",
              "items": ["Copiers, printers and production print under one agreement", "Managed IT and DocuWare from the same team", "FP postage meters, lockers and mailroom equipment", "Water, ice and coffee serviced with the copier", "1-800-34-KELLY reaches all five offices", "Supplies shipped on usage before they run out"]}}

HOTSPOTS = {"type": "hotspots", "id": "office", "eyebrow": "The whole office", "heading": "Seven lines, one floor plan", "intro": "Click a number. Everything an office runs on, and the Kelly page for each.",
    "image": "assets/office-iso-1600.jpg", "image_w": 1600, "image_h": 893, "alt": "An overhead illustration of an office with a copier room, a break room, a server room, a mailroom and desks",
    "items": [
        {"x": 27, "y": 46, "k": "Copiers and production", "title": "The copier room", "body": "Multifunction devices and a production system with inline finishing, on one agreement.", "href": "products/multifunction-printers.html", "label": "Multifunction printers"},
        {"x": 47, "y": 21, "k": "Water, ice and coffee", "title": "The break room", "body": "Bottleless water, ice and single-cup or high-volume coffee, serviced on the same visit as the copier.", "href": "services/pure-technology.html", "label": "Pure Technology"},
        {"x": 82, "y": 14, "k": "Managed IT", "title": "The server room", "body": "Monitoring, backup, security and Microsoft 365 for a fixed monthly invoice.", "href": "products/managed-it.html", "label": "Managed IT services"},
        {"x": 73, "y": 58, "k": "Mailing", "title": "The mailroom", "body": "FP postage meters, folder inserters and mailroom printers that cost less per piece than the office copier.", "href": "products/postage-meters.html", "label": "Postage meters"},
        {"x": 88, "y": 66, "k": "Parcel lockers", "title": "The package wall", "body": "Secure, contactless pickup for offices, campuses and properties.", "href": "products/parcel-lockers.html", "label": "Parcel lockers"},
        {"x": 16, "y": 58, "k": "Desktop printers", "title": "The desks", "body": "Single-function printers, right-sized to how many the office needs and folded into managed print.", "href": "products/printers.html", "label": "Printers"},
        {"x": 64, "y": 71, "k": "Document management", "title": "Scan to DocuWare", "body": "Every MFP scans straight into indexed workflows: accounts payable, HR, contracts.", "href": "products/docuware.html", "label": "DocuWare"}]}

STORY3D = {"type": "story3d", "id": "device", "alt": False, "eyebrow": "Take a closer look", "heading": "Walk around one before it arrives",
    "intro": "Scroll, and the device turns to the part being described. A generated Sharp-style stand-in for the preview; Sharp product models replace it in the build.",
    "poster": "assets/fleet/mfp.png", "alt": "A Sharp-style multifunction copier that turns as you scroll", "hint": "Drag to turn",
    "cta": {"label": "See multifunction printers", "href": "products/multifunction-printers.html"},
    "steps": [
        {"k": "The panel", "title": "One screen for print, scan and release", "orbit": "28deg 72deg 100%", "body": "A tilting color touchscreen where people print, copy, scan and release held jobs with a badge or code. Scan to email or straight into DocuWare from the same screen.", "points": ["Secure print release", "Scan to DocuWare workflows", "Trained on install day"]},
        {"k": "The feeder", "title": "Stacks in, indexed files out", "orbit": "0deg 40deg 108%", "body": "Mixed paper goes in the top. Named, indexed files land in the right folder or workflow, so accounts payable, HR and contracts stop living in filing cabinets.", "points": ["Duplex scanning", "Optical character recognition into DocuWare", "Routing rules set up by Kelly"]},
        {"k": "The paper path", "title": "Trays sized to how the office prints", "orbit": "-62deg 80deg 104%", "body": "Under a managed print agreement the device reports its own levels. Toner ships on usage, before anyone notices it is low, and the six-month reports show what each tray actually carried.", "points": ["Supplies shipped on usage", "Meter reads taken automatically", "Utilization in the six-month report"]},
        {"k": "The service side", "title": "Monitored, so the fault is seen first", "orbit": "200deg 76deg 108%", "body": "Every device on agreement is monitored. A failing part or a jam pattern is often on a Kelly technician's list before anyone in the office calls, and the call goes to the nearest of five offices.", "points": ["Monitoring on every device", "Priority service under agreement", "Dispatched from the nearest office"]}],
    **({"model": MFP_MODEL} if MFP_MODEL else {})}

HERO_LAYERED = {"type": "hero-layered", "id": "hero", "eyebrow": "Moving business forward since 1947",
    "heading": "Fully connected office systems, serviced by people who <em>answer the phone</em>.",
    "subhead": "Copiers and print, document management, IT, mailing, and the water and coffee that keep an office running. One North Carolina partner, five offices, one number to call.",
    "primary": {"label": "Request an assessment", "href": "contact.html"}, "secondary": {"label": "Estimate your print spend", "href": "cost-calculator.html"},
    "image": "assets/hero-plate-2100.jpg", "image_w": 2100, "image_h": 891,
    **({"model": MFP_MODEL, "poster": "assets/fleet/mfp.png", "model_alt": "A Sharp-style multifunction copier, rotating. Drag to turn it."} if MFP_MODEL else {}),
    "stats": [["1947", "Family-owned since"], ["94.4", "Net Promoter Score, audited"], ["4,000", "Customers, approximately"], ["5", "North Carolina offices"]],
    "card_a": {"eyebrow": "Start here", "title": "The free assessment", "body": "One visit. One report, yours to keep whether or not you buy.", "items": ["Every device counted and metered", "Cost per page, mono and color", "Lease, rental and purchase side by side"], "href": "assessment.html", "label": "How it works"},
    "card_b": {"eyebrow": "Already a customer?", "title": "The fast lane", "body": "Under a minute each. A person replies.", "links": [["Request service", "service-support.html#request"], ["Meter reads", "service-support.html#meters"], ["Order supplies", "service-support.html#supplies"], ["Customer portal", PORTAL]]},
    "note": "Preview photography and the 3D device are generated and labelled as such; Kelly's own imagery and Sharp product models replace them."}


def build():
    brand = {
        "accent": "#65BC7B", "ink_secondary": "#000545", "chrome": "dark", "chrome_bg": "#000545",
        "type_from": {"Quantum Showcase": "Quantum Clean"},  # Shawn 2026-09-08: Clean's type on the Showcase layout
        "logo": "assets/kelly-logo.png", "logo_alt": "Kelly Office Solutions", "logo_w": 300, "logo_h": 109,
        "logo_note": "300x109 raster with white subtext: built for a dark ground. Ask for a vector and a light-ground variant.",
        "phone": PHONE, "phone_href": PHONE_HREF, "email": "info@kellyofficesolutions.com",
        "utility": [{"label": "Customer portal", "href": PORTAL}, {"label": "Request service", "href": "service-support.html#request"}, {"label": "Meter reads", "href": "service-support.html#meters"}, {"label": "Order supplies", "href": "service-support.html#supplies"}],
        "cta": {"label": "Request an assessment", "href": "contact.html"},
        "sticky": {"primary": "Get an assessment", "primary_href": "contact.html", "secondary": "Call Kelly", "secondary_href": PHONE_HREF},
        "launcher": {"label": "Already a customer?", "eyebrow": "The fast lane", "title": "What do you need today?", "links": [["Request service", "service-support.html#request"], ["Meter reads", "service-support.html#meters"], ["Order supplies", "service-support.html#supplies"], ["Customer portal", PORTAL]], "note": "A person from the nearest branch replies. Under a Kelly agreement your call is dispatched first."},
        "social": {"linkedin": "https://www.linkedin.com/company/kelly-office-solutions/", "facebook": "https://www.facebook.com/KellyOfficeSolutions", "x": "https://twitter.com/kellyofficesolu"},
        "tagline": "Moving business forward since 1947. Family-owned, headquartered in Winston-Salem, and still answering the phone ourselves.",
        "footer_columns": [
            {"title": "Products", "links": [["All products", "products.html"]] + [[p[2].split(":")[0], f"products/{p[0]}.html"] for p in PRODUCTS if p[1] in ("Print and imaging", "Water, ice and coffee")]},
            {"title": "Services", "links": [[s[2], f"services/{s[0]}.html"] for s in SERVICES]},
            {"title": "Customers", "links": [["Customer portal", PORTAL], ["Request service", "service-support.html#request"], ["Meter reads", "service-support.html#meters"], ["Copier supplies", "service-support.html#supplies"], ["Coffee and water supplies", "service-support.html#supplies"], ["Cost calculator", "cost-calculator.html"]]},
            {"title": "Company", "links": [["About Kelly", "about.html"], ["Key markets", "industries.html"], ["Locations", "locations.html"], ["Careers", "careers.html"], ["Blog", "blog.html"], ["Contact", "contact.html"]]},
        ],
        "legal": [["Privacy policy", "https://kellyofficesolutions.com/privacy-policy/"]],
    }
    schema = {"org_name": "Kelly Office Solutions", "org_url": "https://kellyofficesolutions.com",
              "org_logo": "https://kellyofficesolutions.com/wp-content/uploads/2020/12/Kelly-Office-Solutions-Logo-copy-3.png",
              "org_description": "Family-owned office technology company headquartered in Winston-Salem, North Carolina, since 1947: copiers and managed print, document management, production print, IT services, mailing solutions, and water, ice and coffee service.",
              "sameAs": ["https://www.linkedin.com/company/kelly-office-solutions/", "https://www.facebook.com/KellyOfficeSolutions", "https://twitter.com/kellyofficesolu"],
              "telephone": "+1-800-345-3559"}
    nav = [
        {"label": "Products", "href": "products.html", "mega": True,
         "groups": [{"title": g, "items": [[p[2].split(":")[0], f"products/{p[0]}.html"] for p in PRODUCTS if p[1] == g]} for g in PRODUCT_GROUPS],
         "featured": {"eyebrow": "Not sure what you need?", "title": "Start with a free assessment", "body": "A specialist counts what you have and prices what you need. You keep the report either way.", "href": "assessment.html", "label": "How the assessment works"}},
        {"label": "Services", "href": "what-we-do.html", "children": [[x[2], f"services/{x[0]}.html"] for x in SERVICES] + [["Supplies and service", "service-support.html"]]},
        {"label": "Industries", "href": "industries.html", "children": [[x[1], f"industries/{x[0]}.html"] for x in INDUSTRIES] + [["All key markets", "industries.html"]]},
        {"label": "Resources", "href": "blog.html", "children": [["Blog", "blog.html"], ["Cost calculator", "cost-calculator.html"], ["The assessment", "assessment.html"], ["Drivers, manuals and training", "service-support.html#drivers"]]},
        {"label": "About", "href": "about.html", "children": [["About Kelly", "about.html"], ["Locations", "locations.html"], ["Careers", "careers.html"], ["Contact", "contact.html"]]},
    ]

    pages = []
    # ---------------- home
    pages.append({"file": "index.html", "title": "Kelly Office Solutions | Copiers, managed print, IT and office technology in North Carolina",
                  "compose": {
                      "clean": ["hero-light", "partners", "seal", "wheel", "is-this-you", "flow", "map", "voices", "film", "faq", "contact"],
                      "showcase": ["hero", "partners", "wheel", "fleet", "ba", "flow", "office", "device", "proof", "map", "voices", "film", "contact"],
                      "press": ["hero-light", "story", "services", "seal", "voices", "film", "flow", "map", "faq", "contact"]},
                  "description": "Family-owned since 1947 and headquartered in Winston-Salem. Copiers and managed print, document management, IT, mailing, water and coffee for North Carolina businesses, from five local offices, with Fast local response from the nearest branch.",
                  "sections": [
        {"type": "hero", "id": "hero-light", "layout": "split", "eyebrow": "Moving business forward since 1947",
         "stats": [["1947", "Family-owned since"], ["94.4", "Net Promoter Score, audited"], ["4,000", "Customers, approximately"], ["5", "North Carolina offices"]],
         "ribbon": ["BBB accredited, rated A+", "NPS 94.4, audited by CEO Juice. Industry average in the 70s", "Five North Carolina offices, one number"],
         "variants": {"press": {"stats": None, "ribbon": ["Winston-Salem, North Carolina. Since 1947.", "BBB accredited, rated A+", "NPS 94.4, audited by CEO Juice"]}},
         "heading": "Fully connected office systems, serviced by people who <em>answer the phone</em>.",
         "subhead": "Copiers and print, document management, IT, mailing, and the water and coffee that keep an office running. One North Carolina partner, five locations, one number to call.",
         "primary": {"label": "Request an assessment", "href": "contact.html"}, "secondary": {"label": "Estimate your print spend", "href": "cost-calculator.html"},
         "note": "Sharp, Ricoh, Savin, Konica Minolta, Brother and Epson dealer", "image": "assets/hero-1200.jpg", "image_alt": "A technician kneeling beside an open office copier, replacing a toner unit", "image_w": 1200, "image_h": 800,
         "badge": {"value": "94.4", "label": "Net Promoter Score, independently audited"}},
        HERO_LAYERED,
        {"type": "wheel", "id": "wheel", "eyebrow": "One partner", "heading": "Everything an office runs on, from one partner", "intro": "Hover a segment. Seven lines, one agreement, one number.", "items": WHEEL_ITEMS, "hub": "Kelly", "hub_sub": "one partner", "ring": "EVERYTHING AN OFFICE RUNS ON"},
        FLOW_ENGAGEMENT, FLEET, SEAL, BEFORE_AFTER, HOTSPOTS,
        {"type": "partners", "id": "partners", "caption": "Technology partners", "items": PARTNERS},
        {"type": "stats", "id": "stats", "alt": True, "items": [["1947", "Family-owned since"], ["94.4", "NPS, audited by CEO Juice (industry average: 70s)"], ["4,000", "Customers, approximately"], ["5", "Locations: Winston-Salem, Greensboro, Charlotte, Raleigh and Swansboro"]]},
        {"type": "checklist", "id": "is-this-you", "alt": True, "eyebrow": "Is this you?", "heading": "Six signs your office spends more on print than it knows",
         "intro": "Check what sounds familiar. Nobody is watching.",
         "items": ["Someone orders toner from a retail site when a device runs out", "Nobody knows what a page costs, mono or color", "More than one vendor services your devices", "A device has been down for more than a day this year", "Confidential documents sit on a shared output tray", "The copier company and the IT company blame each other"],
         "messages": ["Check what sounds familiar.", "One is normal.", "Two is a pattern.", "Three or more is money leaving the building every month. The assessment finds how much."],
         "cta_label": "Request an assessment", "cta_href": "contact.html"},
        {"type": "services", "id": "services", "heading": "Everything an office runs on, from one partner",
         "intro": "Most dealers sell copiers. Kelly connects the whole office and keeps it running, so you have one relationship instead of seven vendors.",
         "items": [[s[1], brief(s[6]), f"services/{s[0]}.html"] for s in SERVICES]},
        {"type": "video", "id": "film", "alt": False, "eyebrow": "Who we are", "heading": "Thirty seconds on Kelly", "intro": "Family-owned since 1947, headquartered in Winston-Salem, with branches in Greensboro, Charlotte, Raleigh and Swansboro.", "vimeo": "271855836", "poster": "assets/vimeo-poster.jpg", "title": "Kelly Office Solutions", "caption": "Kelly's own film, from kellyofficesolutions.com"},
        {"type": "process", "id": "process", "eyebrow": "How we would stage an engagement", "heading": "Five stages, and every one of them hands you something",
         "stages": [["Assessment", "Produces: a fleet and cost report, yours to keep."], ["Plan", "Produces: a right-sized device plan with lease, rental or purchase priced side by side."], ["Install and connect", "Produces: every device on your network, every user trained, on a date you chose."], ["Monitor and supply", "Produces: toner that arrives before it runs out, and usage reports on the schedule in your agreement."], ["Review", "Produces: a quarterly look at cost per page and uptime, then back to stage one if anything moved."]]},
        STORY3D,
        {"type": "model3d", "id": "model", "alt": False, "eyebrow": "Take a closer look", "heading": "Walk around one before it arrives", "intro": "A generated Sharp-style multifunction device for the preview. Drag to rotate. Your real models, with Sharp product imagery, replace it in the build.", "poster": "assets/mfp-poster-1200.jpg", "alt": "A white and charcoal multifunction copier on a cabinet, rotatable", "cta": {"label": "See multifunction printers", "href": "products/multifunction-printers.html"}, **({"model": MFP_MODEL} if MFP_MODEL else {})},
        {"type": "testimonials", "id": "voices", "alt": True, "layout": "feature", "eyebrow": "What customers say", "heading": "Customers, in their own words", "items": [TAX_SEASON] + [t[:3] for t in TESTIMONIALS]},
        {"type": "proof", "id": "proof", "alt": True, "eyebrow": "Measured, not claimed", "value": "94.4", "text": "Net Promoter Score, collected and audited by CEO Juice from Kelly customers after every service call. The industry average sits in the 70s.", "source": "Audited quarterly by an independent third party. Ask us for the latest report."},
        {"type": "map", "id": "map", "heading": "Five offices, one number, most of North Carolina", "intro": "Technicians are dispatched from the branch nearest you. Call the branch directly or 1-800-34-KELLY, which reaches all five.", "ring": 40,
         "items": [{"name": "Winston-Salem", "lon": -80.244, "lat": 36.10, "href": "locations/winston-salem.html", "sub": "163 South Stratford Road", "hq": True, "label_dx": -92, "label_dy": -12},
                   {"name": "Greensboro", "lon": -79.79, "lat": 36.07, "href": "locations/greensboro.html", "sub": "1040 E. Wendover Ave.", "label_dx": 10, "label_dy": -10},
                   {"name": "Raleigh", "lon": -78.64, "lat": 35.78, "href": "locations/raleigh.html", "sub": "6001 Chapel Hill Rd, Suite 103", "label_dx": 10, "label_dy": 4},
                   {"name": "Charlotte", "lon": -80.84, "lat": 35.23, "href": "locations/charlotte.html", "sub": "4205-B Stuart Andrew Blvd.", "label_dx": -62, "label_dy": 20},
                   {"name": "Swansboro", "lon": -77.12, "lat": 34.69, "href": "locations/swansboro.html", "sub": "109 Seth Thomas Ln", "label_dx": 10, "label_dy": 14}]},
        {"type": "timeline", "id": "story", "eyebrow": "The story", "heading": "From one office to five, and from copiers to the whole office", "items": [["1947", "Kelly opens", "Selling and servicing office equipment in Winston-Salem."], ["A+", "BBB accredited", "Accredited by the Better Business Bureau and rated A+."], ["Today", "Five offices, seven lines", "Winston-Salem, Greensboro, Charlotte, Raleigh and Swansboro. Copiers to coffee, one number."]]},
        {"type": "tabs", "id": "markets", "eyebrow": "Key markets", "heading": "Built around how your industry uses paper",
         "items": [{"label": i[1], "title": i[1], "body": i[4], "bullets": i[5][:3], "image": i[2], "image_alt": i[1], "href": f"industries/{i[0]}.html", "link_label": f"Office technology for {i[1].lower()}"} for i in INDUSTRIES]},
        {"type": "band", "id": "fastlane", "eyebrow": "Supplies and service", "heading": "Already a customer? This is the fast lane.",
         "subhead": "Request service, send a meter read or order copier and coffee supplies in under a minute. A named technician, not a queue.",
         "items": [["Request service", "Fast local response from the nearest branch", "service-support.html#request"], ["Meter reads", "Or let us read them automatically", "service-support.html#meters"], ["Copier supplies", "Toner and parts, shipped before you run out", "service-support.html#supplies"], ["Coffee and water supplies", "Beans, filters and cups on your schedule", "service-support.html#supplies"]]},
        {"type": "locations", "id": "branches", "heading": "Five North Carolina locations", "intro": "Every one staffed with local technicians. Call the branch, or 1-800-34-KELLY reaches all of them.",
         "items": [[l[1], l[2], l[3], l[4], l[5]] for l in LOCATIONS]},
        {"type": "faq", "id": "faq", "alt": True, "heading": "Questions we get on the first call", "items": [
            ["How fast do you respond to a service call?", "From the nearest of five branches, with priority for devices under a Kelly service agreement. Ask the branch for the response terms in writing. Our NPS of 94.4 is audited by an independent third party, so the service claim is checked by someone other than us."],
            ["Can you take over devices we bought from someone else?", "Often, yes. The assessment covers your whole fleet regardless of where it came from, and the plan tells you honestly which devices are worth keeping under service and which are costing more than they are worth."],
            ["Lease, rent or buy?", "Depends on volume, cash preference and how fast your needs change. The plan prices all three side by side for your actual usage so you can compare, and rentals cover seasonal peaks without a long commitment."],
            ["Do you serve offices outside the Triad and Charlotte?", "Our five locations cover the Triad, Charlotte and the Triangle, and customers with field offices across North Carolina are served from the nearest branch. If you are further afield, ask your nearest branch."]]},
        {"type": "contact", "id": "contact", "heading": "Start with the assessment", "body": "A specialist walks your fleet and your workflows. You keep the report whether or not you buy. About an hour of your time.",
         "options": ["Copiers and print", "Managed print assessment", "Document management", "IT services", "Mailing", "Water, ice and coffee"], "submit": "Request my assessment", "note": "A person from the nearest branch replies, not an autoresponder."},
    ]})
    # ---------------- what we do (overview) + service pages
    pages.append({"file": "what-we-do.html", "title": "What we do | Kelly Office Solutions", "description": "Seven service lines, one partner: copiers and office products, managed print, document management, production print, IT services, mailing solutions, and water, ice and coffee.",
                  "sections": [
        {"type": "wheel", "id": "wheel", "eyebrow": "The seven lines", "heading": "Everything an office runs on, from one partner", "intro": "Hover a segment to read it. Each line has its own page.", "items": WHEEL_ITEMS, "hub": "Kelly", "hub_sub": "one partner"},
        HOTSPOTS,
        {"type": "hero", "layout": "centered", "eyebrow": "What we do", "heading": "Seven things an office runs on. One partner who <em>answers the phone</em>.", "subhead": "Every line below is installed, serviced and supplied by Kelly people from five North Carolina offices. Mix and match; most customers start with print and add from there.", "primary": {"label": "Request an assessment", "href": "contact.html"}},
        {"type": "resources", "heading": "The seven lines", "intro": "Each one has its own page, with what changes and what is included.", "items": [[s[4], s[1], brief(s[6]), "Read more", f"services/{s[0]}.html"] for s in SERVICES[:6]]},
        {"type": "detail", "id": "pure", "alt": True, "eyebrow": "Pure Technology", "heading": SERVICES[6][1], "body": SERVICES[6][6], "bullets": SERVICES[6][8], "image": SERVICES[6][3], "image_alt": "An office break room"},
        {"type": "testimonials", "heading": "What customers say", "items": [TESTIMONIALS[0][:3], TESTIMONIALS[2][:3]]},
        {"type": "leadform", "alt": True, "id": "assessment", "heading": "Not sure where to start? Start with the assessment.", "body": "One visit, one report on what your office really spends.", "submit": "Request my assessment", "note": "A person from the nearest branch replies, not an autoresponder."},
    ]})
    for s in SERVICES:
        pages.append(service_page(*s))
    # ---------------- products (every product Kelly sells, one page each)
    pages.append(products_index())
    for pr in PRODUCTS:
        pages.append(product_page(*pr))
    # ---------------- industries index + pages
    pages.append({"file": "industries.html", "title": "Key markets | Kelly Office Solutions", "description": "Office technology built around how legal, healthcare, faith-based, architecture and manufacturing organizations in North Carolina use paper and technology.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Key markets", "heading": "Built around how your industry <em>uses paper</em>.", "subhead": "Five markets where Kelly has done the work many times. If yours is not here, the assessment still starts the same way.", "primary": {"label": "Request an assessment", "href": "contact.html"}},
        {"type": "resources", "heading": "Five markets", "intro": "Each page covers what we set up, what customers ask, and how to start.", "items": [["Key market", i[1], i[3], f"Office technology for {i[1].lower()}", f"industries/{i[0]}.html"] for i in INDUSTRIES]},
        {"type": "testimonials", "alt": True, "heading": "Across North Carolina", "items": [TESTIMONIALS[0][:3], TAX_SEASON]},
        {"type": "leadform", "id": "assessment", "heading": "Start with the assessment", "body": "A specialist from your nearest branch walks your fleet and your workflows, and writes it up.", "submit": "Request my assessment", "note": "A person from the nearest branch replies, not an autoresponder."},
    ]})
    for i in INDUSTRIES:
        pages.append(industry_page(*i))
    # ---------------- service & support
    pages.append({"file": "service-support.html", "title": "Supplies and service | Kelly Office Solutions", "description": "Request service, send meter reads and order copier, coffee and water supplies. Fast local response from the nearest branch across Winston-Salem, Greensboro, Charlotte and Raleigh.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Supplies and service", "heading": "Already a customer? <em>This is the fast lane.</em>", "subhead": "Everything an existing customer needs, one click deep. Fast local response from the nearest of five branches, by factory-trained technicians.", "primary": {"label": "Request service", "href": "#request"}, "secondary": {"label": f"Call {PHONE}", "href": PHONE_HREF}},
        {"type": "band", "eyebrow": "Fast lane", "heading": "Four things, under a minute each", "subhead": "Or call. A person answers.", "items": [["Request service", "Fast local response from the nearest branch", "#request"], ["Meter reads", "Send a read, or let us read them automatically", "#meters"], ["Copier supplies", "Toner and parts, shipped before you run out", "#supplies"], ["Coffee and water supplies", "Beans, filters and cups on your schedule", "#supplies"]]},
        {"type": "detail", "id": "request", "eyebrow": "Service", "heading": "Request service", "body": "Tell us the device and what it is doing. Dispatch confirms a window for customers under a Kelly agreement, and a factory-trained technician comes from the nearest branch.", "bullets": ["Fast local response from the nearest branch, in all five territories", "Technicians for Sharp, Ricoh, Savin, Konica Minolta, Brother and Epson", "Every call tracked in the customer portal"], "form": {"fields": ["Company", "Device serial or location", "What is it doing?"], "submit": "Request service"}},
        {"type": "detail", "id": "meters", "alt": True, "eyebrow": "Meters", "heading": "Meter reads", "body": "Send a read in thirty seconds, or ask about automatic meter collection so you never do it again.", "bullets": ["Web form, email or automatic collection", "Reads feed billing directly, so invoices match usage", "Usage reports on managed fleets, on the schedule in your agreement"], "form": {"fields": ["Company", "Device serial", "Meter reading"], "submit": "Send meter read"}},
        {"type": "detail", "id": "supplies", "eyebrow": "Supplies", "heading": "Copier, coffee and water supplies", "body": "Toner and parts for your devices, beans and filters for your break room, shipped from the nearest branch or delivered on your service visit.", "bullets": ["Genuine supplies for every device we sell", "Automatic replenishment on managed fleets", "Coffee, cups, filters and sanitizing kits", "One invoice with your service agreement"], "form": {"fields": ["Company", "Device or item", "Quantity"], "submit": "Order supplies"}},
        {"type": "testimonials", "alt": True, "heading": "What customers say about service", "items": [TESTIMONIALS[1][:3], TAX_SEASON]},
        {"type": "faq", "heading": "Service questions", "items": [["What response time can we expect?", "Ask your branch for the response commitment in your agreement, in writing. We would rather give you the real number than print a round one."], ["Do you service devices you did not sell?", "Often, yes. Ask, and we will say plainly which models we support to our own standard."], ["How do I get access to the customer portal?", "Your account manager sets it up at install. If you have lost access, call the branch and they will reset it while you are on the phone."]]},
        {"type": "resources", "id": "drivers", "alt": True, "heading": "Drivers, manuals and training", "intro": "The manufacturer pages our technicians use. Bookmark the one for your device.",
         "items": [["Drivers", "Brother", "Print drivers for Brother devices.", "Brother support", "https://www.brother-usa.com/brother-support/driver-downloads"],
                   ["Drivers", "Canon", "Drivers and product manuals.", "Canon support", "https://www.usa.canon.com/internet/portal/us/home/support"],
                   ["Drivers", "Epson", "Drivers and product manuals.", "Epson support", "https://epson.com/Support/sl/s"],
                   ["Drivers", "HP", "Printer drivers, manuals and safety data sheets.", "HP support", "https://support.hp.com/us-en/drivers/printers"],
                   ["Drivers", "Konica Minolta", "Drivers, manuals and safety data sheets.", "Konica Minolta support", "https://kmbs.konicaminolta.us/kmbs/support-downloads/user-manuals"],
                   ["Drivers", "Kyocera", "Copier and printer drivers and manuals.", "Kyocera support", "https://www.kyoceradocumentsolutions.us/"],
                   ["Drivers", "Lexmark", "Copier and printer drivers and manuals.", "Lexmark support", "https://support.lexmark.com/en_us.html"],
                   ["Drivers", "Samsung", "Drivers, operation manuals and software.", "Samsung support", "https://www.samsung.com/us/support/downloads/"],
                   ["Training", "Savin how-to videos", "Free online training for Savin copiers and printers.", "Watch", "https://howto.ricoh-usa.com/savin/"]]},
    ]})
    # ---------------- cost calculator + assessment
    pages.append({"file": "cost-calculator.html", "title": "Print cost calculator | Kelly Office Solutions", "description": "Estimate what your office spends on printing today: devices, mono and color pages, staff time. Typical North Carolina rates; the assessment replaces them with your meters.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Cost calculator", "heading": "What does your office <em>really</em> spend on print?", "subhead": "Move three sliders. The estimate uses typical North Carolina rates for toner, service and the staff time nobody counts. The assessment replaces every number here with yours."},
        {"type": "calculator", "id": "calc", "alt": True, "eyebrow": "Estimate", "heading": "Your print spend, estimated", "intro": "Devices, mono pages and color pages a month. That is all it needs.",
         "rates": {"mono_cpp": 0.018, "color_cpp": 0.09, "minutes_per_device_week": 25, "hourly": 28, "managed_saving": 0.30, "saving_label": "Potential saving at up to 30% (the figure on Kelly's managed print page)"},
         "note": "Estimates only, using typical rates. Nothing here is a quote. The assessment gives you the real figure from your meters and your invoices.",
         "cta_label": "Get the real number: request an assessment", "cta_href": "contact.html"},
        {"type": "comparison", "heading": "Lease, rent or buy?", "intro": "The plan prices all three for your real volume. Here is how they usually compare.",
         "columns": [{"label": "Lease", "recommended": True}, {"label": "Rent"}, {"label": "Buy"}],
         "rows": [["Best for", "Steady volume, a fleet kept current", "Peaks, projects, uncertain years", "Stable volume, long device life"], ["Term", "36 to 60 months, typically", "Month to month", "None"], ["Up-front cost", "Low", "Low", "Highest"], ["Lifetime cost", "Moderate", "Highest per month", "Lowest if the device runs for years"], ["Technology refresh", "Built in at end of term", "Any time", "When you buy again"], ["Service and supplies", "Managed agreement, or separate", "Usually included", "Managed agreement, or separate"]],
         "note": "Terms and rates are set in the plan after the assessment."},
        {"type": "faq", "alt": True, "heading": "About the estimate", "items": [["Where do the rates come from?", "Typical industry per-page rates for toner and service, and a modest allowance for the staff time spent ordering supplies and chasing repairs. They are for orientation only."], ["Why does staff time count?", "Because it is real money that never appears on a print invoice. Someone orders the toner and waits on hold for the technician."], ["How do I get the real number?", "Request the assessment. We read every meter, collect every invoice and hand you the report."]]},
        {"type": "leadform", "id": "assessment", "heading": "Get the real number", "body": "A specialist from your nearest branch walks your fleet and your workflows, and writes it up. You keep the report whether or not you buy.", "submit": "Request my assessment", "note": "A person from the nearest branch replies, not an autoresponder."},
    ]})
    pages.append({"file": "assessment.html", "title": "The Kelly Assessment: One Visit, One Report | Kelly Office Solutions", "description": "One visit, one report: every device, every meter, every invoice, and a plan that prices lease, rental and purchase side by side. You keep the report whether or not you buy.",
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "The assessment", "heading": "One visit. One report. <em>Yours to keep.</em>", "subhead": "A specialist walks your fleet and your workflows, reads every meter, collects your invoices, and writes up what your office really spends and what would change. About an hour of your time.", "primary": {"label": "Request an assessment", "href": "contact.html"}, "secondary": {"label": "Estimate first", "href": "cost-calculator.html"}, "image": "assets/gso-office-1200.jpg", "image_alt": "Inside the Kelly Greensboro office", "image_w": 1200, "image_h": 900},
        {"type": "process", "alt": True, "eyebrow": "What happens", "heading": "Five stages, and every one of them hands you something", "stages": [["Assessment", "Produces: a fleet and cost report, yours to keep."], ["Plan", "Produces: a right-sized device plan with lease, rental or purchase priced side by side."], ["Install and connect", "Produces: every device on your network, every user trained, on a date you chose."], ["Monitor and supply", "Produces: toner that arrives before it runs out, and usage reports on the schedule in your agreement."], ["Review", "Produces: a quarterly look at cost per page and uptime, then back to stage one if anything moved."]]},
        {"type": "cards", "eyebrow": "What you receive", "heading": "The report, in four parts", "items": [["Fleet inventory", "Every device, where it sits, its age, its meter, and who services it today."], ["Cost per page", "Mono, color and blended, by device and for the fleet, against typical rates."], ["Service history", "Calls, downtime and the devices that cause them."], ["The plan", "The fleet the data recommends, priced lease, rental and purchase, side by side."]]},
        {"type": "checklist", "alt": True, "id": "ready", "eyebrow": "Before we visit", "heading": "Four things that make the hour count", "intro": "None is required. Each one makes the report sharper.", "items": ["A list of devices, or a walk-through of where they are", "Last year's toner and service invoices", "The name of whoever orders supplies today", "Any device that has been down more than a day this year"], "messages": ["Check what you can bring.", "One helps.", "Two is a good start.", "Three or more and the report will be exact."], "cta_label": "Request an assessment", "cta_href": "contact.html"},
        {"type": "faq", "heading": "Questions about the assessment", "items": [["What does it cost?", "Nothing. The assessment is free and carries no obligation, and you keep the report whether or not you buy."], ["How long does it take?", "About an hour of your time on site, and a few days for the report."], ["Do you assess devices you did not sell?", "Yes. The report covers the whole fleet, and says which devices are worth keeping."]]},
        {"type": "leadform", "alt": True, "id": "assessment", "heading": "Request the assessment", "body": "A specialist from your nearest branch replies to set a time.", "submit": "Request my assessment", "note": "A person from the nearest branch replies, not an autoresponder."},
    ]})
    # ---------------- about, careers
    pages.append({"file": "about.html", "title": "About Kelly | Family-owned office technology since 1947, Winston-Salem", "description": "Kelly Office Solutions has served North Carolina since 1947: co-owners Tim Renegar and Peter Kelly, about 90 people, five offices, an audited NPS of 94.4, and a long record of community support in the Triad.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "About Kelly", "heading": "Family-owned since 1947. <em>Still local, on purpose.</em>", "subhead": "Kelly started in 1947 selling office equipment and stayed independent while most of the industry consolidated. Today about 90 people across five North Carolina offices serve some 4,000 customers, and the phone is still answered by someone who works here.", "primary": {"label": "Meet the owners", "href": "#leadership"}, "image": "assets/kelly-team-1024.jpg", "image_alt": "A Kelly technician beside a Kelly service van", "image_w": 1024, "image_h": 576},
        {"type": "stats", "alt": True, "items": [["1947", "Founded in North Carolina"], ["90", "People, approximately, across five offices"], ["94.4", "Net Promoter Score, audited by CEO Juice"], ["4,000", "Customers, approximately"]]},
        {"type": "video", "id": "film", "eyebrow": "Who we are", "heading": "Thirty seconds on Kelly", "intro": "Family-owned since 1947, headquartered in Winston-Salem, with branches in Greensboro, Charlotte, Raleigh and Swansboro.", "vimeo": "271855836", "poster": "assets/vimeo-poster.jpg", "title": "Kelly Office Solutions", "caption": "Kelly's own film, from kellyofficesolutions.com"},
        {"type": "timeline", "eyebrow": "The story", "heading": "From one office to five, and from copiers to the whole office", "items": [["1947", "Kelly opens", "Selling and servicing office equipment in Winston-Salem."], ["A+", "BBB accredited", "Accredited by the Better Business Bureau and rated A+."], ["Today", "Five offices, seven lines", "Winston-Salem, Greensboro, Charlotte, Raleigh and Swansboro. Copiers to coffee, one number."]]},
        {"type": "leadership", "id": "leadership", "heading": "The owners", "intro": "Tim and Peter are co-owners of Kelly Office Solutions, with over 45 years of experience in the industry.", "people": [["Tim Renegar", "Co-owner"], ["Peter Kelly", "Co-owner"]], "orgs_intro": "Kelly supports the organizations that serve its communities, and is a sponsor and member of the local chambers.", "orgs": COMMUNITY},
        {"type": "values", "alt": True, "eyebrow": "What we believe", "heading": "Mission, vision and the standard we hold ourselves to", "items": [["Mission", "To help our customers achieve the vision and success of their business."], ["Vision", "To seek out new technologies and innovations to deliver the best solution to our customer with integrity."], ["Measured, not claimed", "Our Net Promoter Score is collected and audited by CEO Juice, an independent company whose process we do not control. It is 94.4. The industry average is in the 70s."]]},
        {"type": "casestudy", "eyebrow": "What customers say", "heading": "A repair the same day, in a customer's words", "quote": TAX_SEASON[0], "attribution": f"{TAX_SEASON[1]}, {TAX_SEASON[2]}", "metrics": [["Since", "1947", "Independent and family-owned"], ["BBB", "A+", "Accredited since 1960"], ["Offices", "4", "Winston-Salem, Greensboro, Charlotte, Raleigh"], ["Service", "Same day", "Under a Kelly agreement, all five territories"]]},
        {"type": "cards", "alt": True, "id": "markets", "eyebrow": "Key markets", "heading": "The industries we know best", "items": [[i[1], i[3]] for i in INDUSTRIES] + [["Professional services", "Accounting and staffing firms with seasonal peaks, and a technician who calls back the same day in tax season."]]},
        {"type": "cta", "heading": "Work here", "subhead": "Kelly is always looking for energetic, creative problem solvers with an outstanding work ethic and advanced customer service skills.", "primary": {"label": "See careers", "href": "careers.html"}},
    ]})
    pages.append({"file": "careers.html", "title": "Careers | Kelly Office Solutions", "description": "Kelly Office Solutions is always looking for energetic, creative problem solvers with an outstanding work ethic and advanced customer service skills. Headquartered in Winston-Salem, with branches in Greensboro, Charlotte, Raleigh and Swansboro.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Careers", "heading": "Work for a company that <em>still answers the phone</em>.", "subhead": "About 90 people, five North Carolina offices, family-owned since 1947, and a customer score of 94.4 that an outside firm audits. Technicians, sales, dispatch and admin. We look for problem solvers who like customers. Kelly is an equal opportunity employer. ", "primary": {"label": "Ask about open roles", "href": "contact.html"}},
        {"type": "values", "alt": True, "eyebrow": "What we offer", "heading": "A family-friendly place to do serious work", "items": [["Competitive salary", "And a generous benefits package with a 401K plan."], ["Five offices", "Headquartered in Winston-Salem, with branches in Greensboro, Charlotte, Raleigh and Swansboro."], ["Equal opportunity", "We are an equal opportunity employer and appreciate a diverse workforce and environment. Candidates must be authorized to work in the United States."]]},
        {"type": "cards", "eyebrow": "Openings", "heading": "Roles we hire for", "items": [["Field service technician", "Factory training on the brands we sell, a van, a territory and a dispatcher who knows your name."], ["Account representative", "Walk offices, run assessments, price lease, rental and purchase side by side."], ["Dispatch and customer care", "The people who answer the phone. Every call, every meter read, every supply order."], ["Warehouse and delivery", "Devices staged, delivered and installed on the date the customer chose."]]},
        {"type": "leadform", "id": "apply", "heading": "Tell us about yourself", "body": "No opening listed that fits? Send a note anyway; we keep applications on file. A person replies.", "submit": "Send", "note": "Or email info@kellyofficesolutions.com with a resume attached.",
         "fields": [["Name", "text", "name"], ["Email", "email", "email"], ["Phone", "tel", "tel"], ["Role you are interested in", "text", "organization-title"], ["Link to your resume or LinkedIn", "url", "url"]]},
    ]})
    # ---------------- locations index + pages
    pages.append({"file": "locations.html", "title": "Locations | Kelly Office Solutions", "description": "Five North Carolina offices with local technicians: Winston-Salem (headquarters), Greensboro, Charlotte, Raleigh and Swansboro. Copier, print, IT and coffee service from the Triad to the coast.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Locations", "heading": "Five offices. <em>Local technicians at every one.</em>", "subhead": "Headquartered in Winston-Salem, with branches in Greensboro, Charlotte, Raleigh and Swansboro. Call the branch nearest you, or 1-800-34-KELLY reaches all of them.", "primary": {"label": f"Call {PHONE}", "href": PHONE_HREF}},
        {"type": "locations", "detailed": True, "heading": "Where we are", "intro": "Each location is a full branch: sales, service dispatch and supplies. Each has its own page.", "items": [[l[1], l[2], l[3], l[4], l[5]] for l in LOCATIONS]},
        {"type": "resources", "alt": True, "heading": "Branch pages", "intro": "What each branch does, who it serves, and how to reach it.", "items": [[l[6], f"Kelly {l[1]}", f"{l[2]}, {l[3]}. {l[4]}.", f"About the {l[1]} branch", f"locations/{l[0]}.html"] for l in LOCATIONS]},
        {"type": "faq", "heading": "Coverage questions", "items": [["Do you cover my town?", "The Triad, Charlotte, the Triangle and the coast around Swansboro are our home territories, and customers with field offices across North Carolina are served from the nearest branch. Ask your branch; we will say honestly whether we can meet our own response standard where you are."], ["Can I see a device before I decide?", "Ask your branch. Bring a sample of what you print and we will run it on the device you are considering."]]},
        {"type": "leadform", "alt": True, "id": "assessment", "heading": "Start with the assessment", "body": "A specialist from your nearest branch walks your fleet and your workflows, and writes it up.", "submit": "Request my assessment", "note": "A person from the nearest branch replies, not an autoresponder."},
    ]})
    for l in LOCATIONS:
        pages.append(location_page(*l))
    # ---------------- blog listing + posts
    pages.append({"file": "blog.html", "title": "Blog | Kelly Office Solutions", "description": "Plain-spoken guides on managed print, copiers, document management, office IT and the break room, from the Kelly team in North Carolina.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Blog", "heading": "What we tell customers <em>before they ask</em>", "subhead": "Nine guides from the people who service the machines. No jargon, no vendor pitch."},
        {"type": "related", "heading": "The guides", "intro": "Start with what managed print costs, or how to read a lease.", "items": [[p["category"], p["title"], teaser(p["standfirst"]), f"blog/{p['slug']}.html", p["image"]] for p in BLOG]},
        {"type": "leadform", "alt": True, "id": "assessment", "heading": "Start with the assessment", "body": "A specialist from your nearest branch walks your fleet and your workflows, and writes it up. Free, no obligation, and you keep the report.", "submit": "Request my assessment", "note": "A person from the nearest branch replies."},
    ]})
    for i, p in enumerate(BLOG):
        pages.append(blog_post_page(p, BLOG[i + 1:] + BLOG[:i]))
    # ---------------- contact
    pages.append({"file": "contact.html", "title": "Contact | Kelly Office Solutions", "description": "Request an assessment or talk to the nearest Kelly branch. Winston-Salem, Greensboro, Charlotte and Raleigh, or 1-800-34-KELLY.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Contact", "heading": "Start with the assessment, or <em>just call</em>.", "subhead": "A specialist walks your fleet and your workflows. About an hour of your time, and the report is yours."},
        {"type": "contact", "id": "form", "heading": "Request an assessment", "body": "Tell us a little about your office and the nearest branch will call to set a time.", "options": ["Copiers and print", "Managed print assessment", "Document management", "IT services", "Mailing", "Water, ice and coffee"], "submit": "Request my assessment", "note": "A person from the nearest branch replies, not an autoresponder."},
        {"type": "locations", "alt": True, "heading": "Or call the branch", "intro": "1-800-34-KELLY reaches all five.", "items": [[l[1], l[2], l[3], l[4], l[5]] for l in LOCATIONS]},
    ]})

    pitch = {
        "qbs_contact": {"name": "Shawn Peterson", "email": "shawn@thequantumleap.business", "phone": "(712) 389-4639"},
        "prepared_for": "Claudia Coleman, Director of Marketing",
        "heard_intro": "We have not interviewed you yet. Everything here comes from your current site and your brand profile. Tell us if any of it is wrong; it outranks our house defaults.",
        "heard": [
            "Green and navy are the brand; the logo carries both, and it is built for a dark ground, so the header and footer are navy in every direction.",
            "Your existing customers come to the site to request service, send meter reads and order supplies. Those stay one click from the top of every page.",
            "Seven service lines all survive, including Pure Technology and mailing. Each has its own page now.",
            "Headquartered in Winston-Salem, with branches in Greensboro, Charlotte and Raleigh (your careers page says so).",
            "Your key markets are faith-based, legal, architecture, healthcare and manufacturing. Each has its own page now.",
            "Tim Renegar and Peter Kelly are the co-owners; the community organizations you support are named on your About page. Both are on the new About page.",
            "The tone is approachable authority: proof points over hype, North Carolina references, urgent but not pushy."],
        "found": [
            "About 80% of your organic visits are people searching your name. The site is a phone book for people who already know you.",
            "The only page earning strangers today is the Charlotte location page. Every direction now has five location pages with local business schema.",
            "The blog ranks 24 to 94 on real terms and is thin. There are nine full guides now, each aimed at a term you already rank for on page two or three.",
            "There was nothing to try for a visitor who is not ready to call. There is a cost calculator, an assessment page and an is-this-you checklist now.",
            "Your two videos were not on the preview. The brand film and the production print video are now.",
            "There is effectively no photography of your people or offices beyond the van and the Greensboro office. A half-day shoot per office is the single thing that makes the site un-copyable."],
        "pick_reasons": [
            ["Your brand voice is approachable authority", "Clean is the plainest-spoken of the three: a humanist sans, generous white space, one action per section."],
            ["You have 4,000 customers using the site as a tool", "Clean puts the customer fast lane and the phone number where they are found first, and stays fast to scan on a phone."],
            ["Green and navy", "Clean gives the navy the chrome and the green the actions, so both brand colors do real work instead of competing."]],
        "pick_change": "Clean's type can read a little quiet on the home page. We would borrow Showcase's larger heading scale for the hero and the section openers, and keep Clean's rhythm everywhere else.",
        "alternatives": [
            ["Quantum Showcase", "If you want the site to say modern dealer moving into IT first: same ground, a display typeface, wider measure and bigger rhythm."],
            ["Quantum Press", "If heritage is the story: an editorial serif on warm paper, the narrowest measure and the most catalogue-like. Nobody in your category looks like this."]],
        "plan": [
            ["Week 1", "Choose a direction. Confirm the items under To confirm. Send the logo as a vector."],
            ["Weeks 2 to 3", "Copy for every page, from your service leadership and from you, in your words. Photography scheduled at all five offices."],
            ["Weeks 3 to 5", "Build in your HubSpot: theme cloned and re-skinned, blog templates assigned, every page built, forms wired to named people."],
            ["Week 6", "Quality gate on every page, on a real phone. Redirects tested. You edit a page yourself in the walkthrough."],
            ["Launch, then 90 days", "Go live. Reads at 30, 60 and 90 days against the baseline, with what we would change next."]],
        "search": {
            "heading": "Where you stand in search today, and what changes",
            "intro": "Measured before we touched anything, so the work can be judged against it. Numbers from Semrush and from your live home page on 6 and 7 September 2026.",
            "as_of": "Semrush, 6 September 2026; live HTML, 7 September 2026",
            "today_stats": [["521", "Organic visits a month"], ["80%", "Of them from people searching your name"], ["638", "Keywords ranking, most on page two or beyond"], ["1", "Page earning strangers: the Charlotte contact page"]],
            "today": [
                "The site is a phone book for people who already know the name. Four visits in five come from branded searches.",
                "One page earns non-branded traffic: the Charlotte contact page, at #1 for copiers charlotte and top ten for copier lease and rental in Charlotte. Managed print ranks #6 for managed print services charlotte nc; mailing solutions #9 for a 390-a-month term.",
                "The blog ranks between 24 and 94 on real terms it could own, including how to sanitize a water cooler (260 searches a month, position 46).",
                "No LocalBusiness markup for any of the five branches, so search and AI assistants cannot tie the branches to their towns.",
                "The home page title is the company name and a year; no service or place word in it. The description ends with an email address.",
                "The home page is 1.6 MB of HTML with 158 script tags and 32 stylesheets, and none of its 29 images is lazy-loaded.",
                "A viewport tag blocks pinch-zoom (maximum-scale, user-scalable no), which fails WCAG 1.4.4 on every phone.",
                "Forms are a third-party Jotform embed with a captcha; submissions do not land in a CRM record.",
            ],
            "after": [
                "Every URL that earns a visitor today keeps earning it: a permanent redirect for each one, tested individually at launch (the table below).",
                "Five branch pages with LocalBusiness markup, hours where you state them, and the towns each branch serves, starting with the 13 named on the Charlotte page.",
                "17 product pages and a catalogue for terms that have no page today: postage meters, folder inserters, parcel lockers, ice machines, coffee brewers, wide format, production print.",
                "Nine posts on their existing slugs, rewritten to answer the question in the first sentence, with BlogPosting markup and a real author.",
                "Titles and descriptions written for the terms you already rank for: Managed Print Services in Charlotte and the Triad; Copier Sales, Lease and Rental in Charlotte, NC.",
                "Organization markup on the home page with your LinkedIn, Facebook, X and Google Business profiles as sameAs, so an AI assistant asked about Kelly resolves to the right company.",
                "Every page under 80 kB of HTML before images, lazy-loading below the fold, pinch-zoom allowed, 16 px inputs, 44 px targets, one H1. Scored on our gate before you see it; the scores travel with the site.",
                "HubSpot forms that create a contact, notify a named person, and show a thank-you page. A calculator whose result you can email.",
            ],
            "keep_heading": "Every page that earns a visitor today keeps earning it",
            "keep": [
                ["/contact-us/charlotte/", "/locations/charlotte", "copiers charlotte #1, office equipment company charlotte #3, copier rentals charlotte nc #6, copier lease charlotte nc #8"],
                ["/managed-print-services/", "/services/managed-print", "managed print services charlotte nc #6"],
                ["/mailing-solutions/", "/services/mailing", "mailing solutions #9 (390 a month)"],
                ["/water/, /ice/, /coffee/", "/products/water-coolers, /products/ice-machines, /products/coffee-brewers", "water kelly #3, office ice dispenser #9"],
                ["/key-markets/legal-organizations/", "/industries/legal", "legal print terms at 23 and 30, difficulty 1 to 2"],
                ["/contact-us/greensboro/, /contact-us/", "/locations/greensboro, /contact", "branded and Greensboro terms"],
                ["blog posts, all", "/blog/<same slug>", "document management compliance, benefits of managed print, workstation support, sanitize a water cooler (260 a month at 46)"],
            ],
            "note": "Rankings or traffic. Those depend on the market and on what you publish after launch. What we promise is that nothing about the build is the reason they do not come, that every number above is re-measured at 30, 60 and 90 days, and that you see the same report we do.",
        },
        "confirm": [
                        "The BBB wording. We have written BBB-accredited, rated A+, and left the accreditation year off until you confirm it.",
            "Swansboro. Your contact page lists a fifth office at 109 Seth Thomas Ln. We have built it as a branch; tell us if it is a service point instead.",
            "The response commitment. Your site never states one, so we have not printed one. If you want same-day in writing, give us the wording and the conditions.",
            "Parts on the truck. We removed the claim that technicians carry parts for the models you sell until you confirm the stocking policy.",
            "Report cadence. Your managed print page says every six months; we have used that and removed monthly. Confirm.",
            "Winston-Salem and Swansboro hours. Greensboro, Charlotte and Raleigh state 8 to 5 on your site; the other two do not.",
            "Blog dates. The nine posts keep your live slugs; give us the original publish dates so the schema does not claim they are new.",
            "The Ricoh standing. Your profile says sixth-largest Ricoh dealer in the Southeast; we left it off until Ricoh confirms it.",
            "Manufacturer authorizations to show: Sharp, Ricoh, Savin, Konica Minolta, Brother, Epson, Dell, as on your site today.",
            "Branch hours for each location. The location pages carry a placeholder of 8 to 5, Monday to Friday.",
            "The tagline. Moving Business Forward Since 1947 is on your site today; Office Technology Done Right Since 1947 has also been used.",
            "Your assessment process, stage by stage, and what each stage hands the customer. We drafted five stages from your three; they are ours until you replace them.",
            "The customer count and where they are: about 4,000, most in North Carolina, or nationwide?",
            "Permission to use the five testimonials on your current site, and their spellings.",
            "The cost calculator's rates. They are typical North Carolina figures for orientation; replace them with yours or keep the disclaimer."],
        "footer": "Prepared for Claudia Coleman, Director of Marketing. Nothing here is live or indexed. Every number we could source comes from your current site, your brand profile or public data. Several service commitments on these pages (response time, the assessment report, the staged process, calculator rates) are our draft of what we think you do, and they are listed under To confirm. Photographs are yours where they exist on your site today (the van, the Greensboro office, the service pages); the rest are generated stand-ins until your own photography exists. Partner logos are the ones on your current site.",
    }
    content = {"client": "Kelly Office Solutions", "slug": "kelly-office-solutions", "domain_hint": "kellyofficesolutions.com",
               "brand": brand, "schema": schema, "nav": nav, "pages": pages, "pitch": pitch}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(content, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"wrote {OUT}: {len(pages)} pages, {len(BLOG)} posts")


if __name__ == "__main__":
    build()
