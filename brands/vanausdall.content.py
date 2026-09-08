#!/usr/bin/env python3
"""Authoring script for brands/vanausdall.content.json.

The JSON is what scripts/preview.py reads; this script is how a human writes it without
repeating fifty pages by hand. Run it to regenerate the JSON:

    python3 brands/vanausdall.content.py

Every fact below is SOURCED from vanausdall.com (scraped 2026-09-08), the CEO Juice NPS page it
links to, or Semrush, unless marked DRAFT in a comment. DRAFT items are also listed on the hub's
"To confirm" section. No em dashes anywhere; the generator rewrites them, but write it clean.
"""
import json
import os
import re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vanausdall.content.json")

CLIENT = "Van Ausdall & Farrar"
SHORT = "VAF"
PHONE, PHONE_HREF = "(317) 634-2913", "tel:3176342913"
TOLLFREE, TOLLFREE_HREF = "(800) 467-7474", "tel:8004677474"
SUPPORT_EMAIL = "support@vanausdall.com"
SUPPLIES_EMAIL = "supplies@vanausdall.com"
IT_EMAIL = "itsupport@vanausdall.com"
SUCCESS_EMAIL = "clientsuccess@vanausdall.com"
CAREERS_URL = "https://workforcenow.cloud.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=76f18e20-dbb1-475b-98ad-e470199a4f66&ccId=19000101_000001&lang=en_US"
SITE = "https://www.vanausdall.com"
PREVIEW = "https://van-ausdall.vercel.app"
_DEEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vanausdall.seo-deep.json")
SEO_FINDINGS = json.load(open(_DEEP, encoding="utf-8")).get("findings", []) if os.path.exists(_DEEP) else []
_FULL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vanausdall.seo-full.json")
SITE_AUDIT = json.load(open(_FULL, encoding="utf-8")) if os.path.exists(_FULL) else None
if SITE_AUDIT:
    SITE_AUDIT["domain"] = "www.vanausdall.com"
    SITE_AUDIT["as_of"] = "8 September 2026"
    SITE_AUDIT["csv_href"] = "seo-audit-pages.csv"
    _BUILD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vanausdall.build-audit.json")
    SITE_AUDIT["build"] = json.load(open(_BUILD, encoding="utf-8")) if os.path.exists(_BUILD) else None
MFP_MODEL = "assets/fleet/mfp.glb" if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "vanausdall", "assets", "fleet", "mfp.glb")) else None

# ------------------------------------------------------------------ sourced facts (vanausdall.com)
# Real customer comments, imported from VAF's after-service surveys and published on /about/customer-comments.
COMMENTS = [
    ["He was incredibly efficient and personable, answering all of my questions thoroughly and thoughtfully. He also laughed at my jokes, which is always appreciated.", "Elaine", "After-service survey, June 2026"],
    ["The guy is totally awesome. He has been working on our equipment for at least 12 years and I would not want anyone else.", "Teresa", "After-service survey, May 2026"],
    ["We always look forward to Jerome coming. He is kind and professional. We always know our problem will be resolved.", "Stacy", "After-service survey, May 2026"],
    ["Brent is amazing. Always there when we need him and he is very knowledgeable and helpful. It is a pleasure to work with him.", "Megan", "After-service survey, April 2026"],
    ["He went above and beyond to ask and answer questions so we both were on the same page with the problem and ultimately the solution. He explained what we at the office needed to do differently to prevent this situation in the future as well.", "Elaine", "After-service survey, June 2026"],
    ["You guys give us top tier support and we thank you greatly.", "Megan", "After-service survey, April 2026"],
    ["He did a great job, and was very communicative prior to his arrival.", "Rick", "After-service survey, October 2025"],
    ["Mike is awesome, knowledgeable, and friendly.", "Denise", "After-service survey, February 2026"],
]
SIGMON = ["We get to take that worry, that stress, the sleepless nights around IT and security, and let them focus on why they do what they do.", "Steven Sigmon", "Director of IT, Van Ausdall & Farrar"]

# slug, city, address 1, address 2, phone display, phone href, region, lat, lon, hq
LOCATIONS = [
    ["indianapolis", "Indianapolis", "6430 E 75th Street", "Indianapolis, IN 46250", PHONE, PHONE_HREF, "central Indiana", 39.887, -86.062, True],
    ["fort-wayne", "Fort Wayne", "1241 N Wells Street", "Fort Wayne, IN 46808", "(260) 432-1547", "tel:2604321547", "northeast Indiana", 41.089, -85.145, False],
    ["evansville", "Evansville", "Local office", "Evansville, IN", "(812) 424-5736", "tel:8124245736", "southwest Indiana and the Tri-State", 37.975, -87.556, False],  # DRAFT: street address not published
]
SERVICE_AREAS = ["Indianapolis", "Carmel", "Fishers", "Noblesville", "Greenwood", "Bloomington", "Columbus", "Muncie", "Fort Wayne", "South Bend", "Evansville"]
PARTNERS = ["Canon", "Ricoh", "Kyocera", "HP", "Brother", "Fortinet", "Sophos", "Mitel", "RingCentral", "8x8", "Elevate", "Microsoft", "Datto", "KnowBe4", "Arctic Wolf", "OnBase", "Square 9", "Fujitsu", "OPEX", "Zebra", "VMware", "Juniper", "N-able", "Tenable"]

# The four pillars, in VAF's own words (vanausdall.com/partners and /indianapolis)
PILLARS = [
    ["Information", "Managed IT, cybersecurity, cloud, backup and continuity. A vCIO, 24/7 monitoring and a security operations center, from one team.", "services/managed-it.html", "Information"],
    ["Communication", "Business phone systems, unified communications and contact center, in the telecom business since 1983 with over 4,000 systems deployed.", "services/business-phone-systems.html", "Communication"],
    ["Print", "Copiers, printers, managed print and production print. Canon, Ricoh, Kyocera and HP, serviced by certified local technicians.", "services/copiers.html", "Print"],
    ["Process", "Document management, document conversion, business process and AI consulting. The paper out, the workflow in.", "services/document-management.html", "Process"],
]

CASE_STUDIES = [  # slug, org, industry, one-line (from /case-studies), metric value, metric label, full page?
    ["tippecanoe-school-corporation", "Tippecanoe School Corporation", "Education", "New print and copier fleet reduced overall equipment count and provided $1M in savings.", "$1M", "saved over the life of the contract", True],
    ["star-financial", "STAR Financial Bank", "Financial services", "STAR achieved over 70% cost savings after five months with Van Ausdall & Farrar.", "70%", "cost savings on print", True],
    ["johnson-memorial-hospital", "Johnson Memorial Health", "Healthcare", "Scan and index 1.5 million patient files in 90 days while adhering to HIPAA? We're on it.", "1.5M", "patient files scanned in 90 days", True],
    ["city-of-anderson", "City of Anderson, IN", "State and local government", "Anderson's technology refresh provides cost savings and new solutions to constituents.", "$40,000", "in annual savings", True],
    ["gailey-eye-clinic", "Gailey Eye Clinic", "Healthcare", "Van Ausdall offers Gailey expertise and time savings where it matters most.", None, None, False],
    ["aspire", "Aspire", "Healthcare", "Improved hardware solutions yield more security and big savings for Aspire.", None, None, False],
    ["shiel-sexton", "Shiel Sexton", "Engineering and construction", "New lease, new equipment, and new partner equals new efficiencies for Shiel Sexton.", None, None, False],
    ["bowen-engineering", "Bowen Engineering", "Engineering and construction", "Delivering short-term technology solutions efficiently, effectively, and economically.", None, None, False],
    ["echo-engineering", "Echo Engineering", "Engineering and construction", "Increased line output, reduced labor costs, and enhanced efficiency.", None, None, False],
    ["city-of-bloomington", "City of Bloomington, IN", "State and local government", "Enterprise content management brings higher efficiency to a busy utility department.", None, None, False],
    ["the-town-of-bargersville", "Town of Bargersville, IN", "State and local government", "Improved document workflow solutions help Bargersville prepare for now and plan for the future.", None, None, False],
    ["becks-hybrid", "Beck's Hybrids", "Manufacturing and logistics", "Van Ausdall planted new print solutions and grew real savings for Beck's Hybrids.", None, None, False],
    ["berry-global", "Berry Global", "Manufacturing and logistics", "In-house print plus better facilities management equals efficiency and cost savings for Berry Global.", None, None, False],
    ["mid-city", "Mid-City Supply", "Manufacturing and logistics", "Van Ausdall helps Mid-City Supply cut costs and improve network performance and reliability.", None, None, False],
    ["tippecanoe-school-corporation-digital-document", "Tippecanoe School Corporation (documents)", "Education", "Tippecanoe School Corporation scanned over a half-million documents with the help of Van Ausdall.", None, None, False],
    ["phalen-leadership-academy", "Phalen Leadership Academy", "Education", "Business continuity put to the test during the COVID-19 crisis.", None, None, False],
    ["pools-of-fun", "Pools of Fun", "Retail", "Reliable and secure point of sale technology positions the company for growth.", None, None, False],
    ["ellinger-riggs", "Ellinger Riggs Insurance", "Insurance", "Communications technology to keep customers on the line and seamlessly expand to new locations.", None, None, False],
]
CS_INDEX = {c[0]: c for c in CASE_STUDIES}

INDUSTRIES = [  # slug, name, image, one-line (from /industries), body, bullets, case study slugs
    ["education", "Education", "assets/team-1200.jpg",
     "Schools are tasked with developing the brightest minds, and many still run on technology from another era.",
     "Districts and schools print more than almost any organization their size, across more buildings, with an IT staff stretched thin. VAF consolidates the fleet, puts every device under one agreement, and adds the mobile and cloud printing students and staff expect. Tippecanoe School Corporation cut 1,200 devices to just over 300 and saved a million dollars over the contract.",
     ["Fleet consolidation across every building, priced as one agreement", "Mobile and cloud printing for staff and students", "Document conversion for student records with a retention policy", "Managed IT, security awareness training and continuity for the district office"],
     ["tippecanoe-school-corporation", "tippecanoe-school-corporation-digital-document", "phalen-leadership-academy"]],
    ["engineering-construction", "Engineering and construction", "assets/process-1200.jpg",
     "Field operations need technology that is flexible, efficient and cost-effective, and most of it was never designed for a job site.",
     "Firms that run projects from trailers and site offices need phones, print and IT that travel with the work. VAF supplies short-term copier rental for job sites, wide-format print for plan sets, unified communications that follow a project manager between the office and the field, and managed IT that keeps estimating and accounting up. Shiel Sexton, Bowen Engineering and Echo Engineering are on the record.",
     ["Short-term copier and printer rental for trailers and temporary offices", "Wide-format print and scan for plan sets and submittals", "Unified communications that follow the project team", "Managed IT and security for estimating, accounting and project data"],
     ["shiel-sexton", "bowen-engineering", "echo-engineering"]],
    ["financial-services", "Financial services", "assets/security-1200.jpg",
     "Banks and credit unions inherit expired leases, scattered vendors and print they cannot see. The fix starts with the assessment.",
     "When STAR Financial Bank needed a new print strategy, VAF removed expired leases, negotiated new contracts on upgraded equipment across the state, and implemented a print platform that cut waste and raised security. The result was 70% savings. The same assessment covers cybersecurity, continuity and the phone system that answers your customers.",
     ["Print assessment across every branch, with expired leases retired", "Secure print release and authenticated scanning for customer documents", "Managed detection and response, MFA and security awareness training", "Business continuity planned around the downtime a branch can survive"],
     ["star-financial"]],
    ["healthcare", "Healthcare", "assets/healthcare-print-1200.jpg",
     "Reliable, protected information is patient safety. VAF has worked in and around healthcare since 1914.",
     "Print needs that keep growing, records that must stay confidential, and communications that cannot fail when a patient needs urgent care. VAF supplies authenticated print release and scanning, tools that aid HIPAA compliance around patient records, unified communications and contact center for clinics, and a Document Conversion Center that scanned 1.5 million patient files for Johnson Memorial Health in 90 days.",
     ["Consolidated print spend, centralized management and authenticated release", "Tools to aid HIPAA compliance around patient records", "Cloud, premise and hybrid unified communications, telehealth platforms and overhead paging", "On-site or off-site document conversion with strict chain of custody"],
     ["johnson-memorial-hospital", "gailey-eye-clinic", "aspire"]],
    ["insurance", "Insurance", "assets/meeting-1200.jpg",
     "In an industry this competitive, solid business technology is the edge, and eliminating the unnecessary technology is half of it.",
     "Agencies run on documents, phone calls and the systems that connect them. VAF eliminates the technology an agency no longer needs, optimizes what it has, and builds a roadmap for the rest: document management for policy files, call recording and contact center for the phones, and managed security for the client data an agency is trusted with. Ellinger Riggs Insurance used VAF communications technology to keep customers on the line and expand to new locations.",
     ["Document management for policy and claim files with retention rules", "Call recording and contact center that meet PCI DSS requirements", "Managed security and MFA for client data", "Phone systems that expand to a new office without a new vendor"],
     ["ellinger-riggs"]],
    ["manufacturing-logistics", "Manufacturing and logistics", "assets/engineers-1200.jpg",
     "Manufacturing has advanced light years in how it communicates, stores information and manages processes. The technology has to keep up.",
     "Plants and warehouses need print where the work happens, networks that reach the floor, and documents that move without a paper chase. VAF brought in-house print and facilities management to Berry Global, planted new print solutions at Beck's Hybrids, and improved network performance and reliability for Mid-City Supply.",
     ["In-house print and facilities management for plants and distribution centers", "Networking, Wi-Fi and SD-WAN that reach the floor", "Document workflow for orders, quality and compliance records", "Managed IT and continuity for multi-site operations"],
     ["berry-global", "becks-hybrid", "mid-city"]],
    ["real-estate", "Real estate", "assets/innovation-1200.jpg",
     "The industry moved online, and the technology behind a brokerage has to keep up with the buyers who did.",
     "Brokerages and property managers live on their phones and their documents. VAF supplies cloud communications with mobility for agents who work from anywhere, document management for transaction files, and managed IT and security for offices that hold client financial information.",
     ["Cloud phone systems with mobile apps for agents in the field", "Document management for transaction and lease files", "Managed IT and security for client financial data", "Print and scan for the office, right-sized to the volume"],
     []],
    ["government", "State and local government", "assets/hq-1200.jpg",
     "Out-of-date technology that is impossible to manage is a service problem for constituents. VAF has been a preferred vendor for Indiana municipalities since 2003.",
     "Cities, towns and utilities need billing, records and communications that constituents can trust. For the City of Anderson, VAF's on-site Facilities Management program refreshed print and billing technology, added 2D bar code document security and postal optimization, and streamlined purchasing, for over $40,000 in annual savings. Bloomington's utility department and the Town of Bargersville run on VAF content management.",
     ["On-site facilities management with full-time VAF personnel", "Print and mail security for billing and records", "Enterprise content management for utilities and clerks", "Cooperative purchasing pricing through Sourcewell on Mitel communications"],
     ["city-of-anderson", "city-of-bloomington", "the-town-of-bargersville"]],
]
IND_INDEX = {i[0]: i for i in INDUSTRIES}

# slug, title, nav label, pillar, image, eyebrow, hero heading (with <em>), subhead, benefits (title, body), bullets, faq
SERVICES = [
    ["managed-it", "Managed IT services", "Managed IT services", "Information", "assets/gen-soc-1200.jpg", "Managed IT",
     "Your IT department, <em>without the overhead</em>.",
     "We become the extended arm of your business: vCIO guidance, 24/7 monitoring, security, backup, voice and cloud, delivered as one proactive partnership. Not a break-fix shop that shows up after something breaks.",
     [["Security built in", "Anti-virus, email and DNS filtering, managed detection and response with multi-factor authentication, security awareness training with simulated phishing, plus Microsoft and Google backup."], ["vCIO strategic guidance", "A fractional CIO for technology budgets, roadmaps and vendor decisions, with regular planning tied to your business goals."], ["24/7 monitoring and alerting", "Around-the-clock system monitoring and patch management, so issues are caught and resolved before they disrupt you."], ["Help desk and on-site support", "A responsive help desk for the day to day, and on-site technicians when you need them."], ["Microsoft and Google management", "User administration, licensing, email, collaboration and file sharing, with backup for both."], ["Co-managed IT", "Extend your existing IT team with specialty expertise, security and monitoring alongside your staff."]],
     ["One package: security, strategy and support bundled together for one predictable monthly cost", "Monthly managed clients come first, ahead of break-fix work", "24/7 security operations center with managed detection and response", "Managed continuity planned around your recovery time objective", "Managed voice, managed cloud and managed AI from the same team"],
     [["What is included in managed IT services?", "vCIO strategic guidance, 24/7 monitoring, help desk and on-site support, patch management, and security: anti-virus, email and DNS filtering, managed detection and response, multi-factor authentication, security awareness training with phishing simulations, and Microsoft and Google backup. All up, all in, as one package."], ["How is managed IT different from IT support?", "IT support is reactive: you call when something breaks. Managed IT is proactive: we monitor, patch and maintain your systems around the clock so problems are prevented, and managed clients get priority over break-fix work."], ["Do you work with companies that already have an IT team?", "Yes. Co-managed IT supplements your internal team, and standalone managed cybersecurity closes security gaps while you keep day-to-day IT in-house."], ["What is a vCIO?", "A virtual chief information officer: a fractional IT executive who provides strategic guidance, technology budgeting and planning without the cost of a full-time CIO."]]],
    ["cybersecurity", "Managed security services", "Cybersecurity", "Information", "assets/gen-soc-1200.jpg", "Vsecure managed security",
     "Security that <em>never clocks out</em>.",
     "Assessments, monitoring and response from a team that has seen it all. Every Vsecure support plan starts with EDR/XDR protection, proactive patching and monitoring, and a next-generation firewall: the coverage cyber insurers now require.",
     [["Endpoint and server protection", "Sophos Intercept X Advanced with XDR on every base plan, using EDR, XDR and MTR technologies."], ["Proactive patching and monitoring", "Software patching and monitoring from Datto, included in every Vsecure program."], ["Co-managed Fortinet security", "Firewall and Fortinet Fabric services from a Fortinet Engaged Advanced Partner with NSE-7 certified engineers and the first SD-WAN Specialization in the Great Lakes region."], ["SOC as a service", "A security operations center with trained analysts watching your network around the clock, and a dedicated security analyst option."], ["Mail security and vulnerability scanning", "Email protection and periodic scanning for the gaps attackers look for first."], ["Awareness training and compliance", "End-user cyber security awareness training and compliance management from KnowBe4, with a CISSP on staff for regulatory, planning and incident work."]],
     ["A CISSP on staff for regulatory concerns, security planning, business continuity and incident planning", "Meets the EDR/XDR, monitoring, patching and firewall requirements cyber insurers ask for", "Firewall available under a Hardware as a Service agreement or purchase", "Standalone managed cybersecurity for companies that keep IT in-house"],
     [["We already have an IT team. Can we still use your security?", "Yes. Managed cybersecurity is a standalone offering for organizations that keep day-to-day IT in-house. We compare your framework to best-in-class standards, identify the gaps, cover them, and maintain them ongoing."], ["Do you offer 24/7 security monitoring?", "Yes. Our security operations center provides SOC as a service with managed detection and response: eyes on your network around the clock."], ["Will this satisfy our cyber insurance application?", "Insurers increasingly require EDR/XDR protection, proactive monitoring, software patching and a next-generation firewall. Vsecure programs meet all four, with the firewall provided under a Hardware as a Service agreement or purchase."]]],
    ["cloud", "Cloud services", "Cloud services", "Information", "assets/cloud-1200.jpg", "Managed cloud",
     "Move out of the <em>server closet</em>.",
     "Cloud migration, infrastructure as a service, and backup and disaster recovery. Cut hardware costs and keep your data reachable from anywhere, with hosted servers, SharePoint-type solutions and highly governed file sharing through our Egnyte partnership.",
     [["Increased storage", "Unlimited storage housed away from your own servers, kept secure."], ["Business continuity", "Employees work from anywhere with real-time information when and where they need it."], ["Saves time and cost", "Less hardware to maintain and fewer people paid to manage it."]],
     ["Subscription services, co-location, cloud hosting and virtualization", "A Class V data center that sustains 200 MPH winds, with primary and secondary UPS and a backup generator", "Five internet carriers serving the data center for redundancy and bandwidth", "An IT service provider in Indiana for 25 years"],
     [["Where is our data hosted?", "Our data center is rated Class V, meeting hardened data center requirements, protected by primary and secondary distributed UPS systems and a backup generator, and served by five internet carriers."], ["Do we have to move everything at once?", "No. Most customers start with backup and file sharing, then move servers as leases and hardware age out. The assessment sets the order."]]],
    ["business-continuity", "Backup and recovery", "Backup and recovery", "Information", "assets/it-1200.jpg", "Managed continuity",
     "How long can you go <em>without operating</em>?",
     "Business continuity starts with that question. Your recovery time objective drives the solution: backup, disaster recovery, and the plan that gets you working again. Many SMBs believe they have continuity when they really only have backup. We close that gap.",
     [["Disaster recovery planning", "A written plan for IT systems, revised once or twice a year, tested with real restorations."], ["High availability and redundancy", "The proper level of redundancy for your business, decided with you, not assumed."], ["Compliance kept current", "Gramm-Leach-Bliley, HIPAA, Sarbanes-Oxley, PCI and the other regulations that shape IT policy and procedure."]],
     ["Backup with more than one instance stored off-site or in the cloud", "Restoration tests so the backups are known to work", "Battery backup that keeps routers, firewalls and servers running through an outage", "Project deployment and migration for Cisco, Microsoft, HP, Barracuda and VMware"],
     [["What is the difference between backup and continuity?", "Backup is a copy of your data. Continuity is the plan and the systems that get your people working again within the downtime you can survive. Your recovery time objective is where the conversation starts."], ["How often should a disaster recovery plan be revised?", "Once or twice a year, and after any significant change to your systems. It is one of the questions on the Technology Strength Assessment."]]],
    ["business-phone-systems", "Business phone systems", "Business phone systems", "Communication", "assets/gen-phone-1200.jpg", "Unified communications",
     "One partner for every phone, <em>since 1983</em>.",
     "VoIP, unified messaging and contact center technology for single locations and multi-office teams, designed, deployed and supported by one local partner. We do not dabble in phone systems: a dedicated engineering staff, more than 4,000 systems deployed, and Mitel Gold status seven years running.",
     [["Cloud communications", "Enterprise PBX and VoIP capability with no hardware to buy, managed and monitored 24/7, with mobility, web conferencing and secure messaging."], ["Contact center", "Caller information assembled and on the agent's screen as the call arrives, so staff work smarter and faster."], ["Call recording", "OakSi RecordX unified recording for fixed line, mobile and VoIP that meets PCI DSS requirements."], ["Audio conferencing and collaboration", "Voice and data combined: instant messaging, conference calling, document sharing and web and mobile collaboration across the organization."], ["Mobility", "Unified communications extended to smartphones and tablets, with centralized control and BYOD support."], ["Carrier services", "A vendor-neutral evaluation of SD-WAN, SIP trunking, broadband and fixed wireless, so you get one bill and one point of contact."]],
     ["Mitel MiVoice Connect, MiCloud Connect and Enterprise Contact Center Gold Certified", "RingCentral Customer Delivery Partner Certified and 8x8 Sales Engineer Certified", "Fortinet NSE 1 to 4 and Adtran ASP, ATSA, ATSP and ATSE certified", "A computer-dispatched, vendor-certified service fleet covering the Indianapolis metro and the entire state", "Sourcewell cooperative pricing, a 40% discount on Mitel products, free to eligible organizations"],
     [["Cloud or premise?", "Both, and hybrid. Through Mitel, 8x8, RingCentral and Elevate we design for how your teams actually work: single location, multi-office, or a contact center with application integration."], ["Can our smartphones join the phone system?", "Yes. Extension dialing, real-time presence and the corporate directory extend to smartphones and tablets, with centralized control."], ["Who services the system after install?", "VAF's own local engineers. We have been in the telecom business since 1983 and support every product we recommend with our own team."]]],
    ["copiers", "Copiers and printers", "Copiers and printers", "Print", "assets/gen-technician-1200.jpg", "Copier sales, lease and rental",
     "The right copier, backed by the <em>fastest service response in the state</em>.",
     "From a single multifunction printer for a startup to a fleet of production copiers across multiple locations, we help you choose the right equipment: Canon, Ricoh, Kyocera and HP, with local sales, service and support since 1914.",
     [["Canon", "Award-winning imageRUNNER ADVANCE copiers and multifunction printers for offices of every size."], ["Ricoh", "Reliable black-and-white and color MFPs with advanced document management built in."], ["Kyocera", "Low total cost of ownership with long-life components and enterprise print security."], ["HP", "LaserJet and PageWide multifunction printers for teams that need dependable everyday output."]],
     ["Lease, buy or rent, matched to your budget and workflow", "User authentication, secure print release, cloud scanning and mobile printing configured at install", "Short-term rental for events, seasonal peaks, construction trailers and temporary offices", "Supported for the life of the equipment by our Indianapolis-based Customer Care Center"],
     [["Do you sell or lease copiers?", "Both. Purchase, leasing and rental options with flexible terms, so the equipment matches your budget and workflow. Leases can include toner, service and maintenance in one rate."], ["Can you rent a copier for a short-term project?", "Yes. Short-term rentals cover events, seasonal needs, construction trailers and temporary offices throughout Indianapolis and central Indiana."], ["Do new copiers include service and maintenance?", "Every new copier agreement includes service and support options from our Customer Care Center, including preventative maintenance and same-day repairs for most metro-area calls."]]],
    ["managed-print", "Managed print services", "Managed print", "Print", "assets/print-1200.jpg", "Managed print",
     "Cut printing costs <em>up to 30%</em>, and see where.",
     "Print security, proactive fleet management and cost reduction: automated, cloud-based management for your entire printer and copier fleet. Companies often have devices from many vendors and no idea what they have, what they spend, or why. Managed print answers all three.",
     [["Stronger security", "Devices connected across a company are protected with print management software that guards data and sensitive information."], ["Proactive equipment management", "IT experts watch every device for issues and updates, instead of IT following up reactively."], ["Newer equipement kept current", "Upgrade equipment as needed under the agreement, on site and in the cloud, instead of holding antiquated hardware."], ["Valuable insight", "Know your current usage and its cost, then make the changes that cut it."], ["Time back", "Fewer hours lost to old hardware, jams and scanning workarounds."], ["Reduced cost", "One automated system beats maintaining each device on its own."]],
     ["Fleet optimization and 24/7 monitoring from our Customer Care Center", "Automated supply replenishment and predictive maintenance", "Real-time usage analytics and cost-per-page optimization", "Print security and compliance monitoring", "Energy efficiency management and regular performance reviews"],
     [["What is managed print services?", "Managed print monitors your entire printer and copier fleet, automates supply replenishment, and cuts printing costs up to 30%."], ["How much do copy and print solutions cost?", "Costs depend on equipment, print volume and service level. Every engagement starts with a free print assessment, so you see exact pricing for your office before you commit."], ["Can you manage devices we did not buy from you?", "Usually, yes. The assessment maps every device, volume and cost regardless of where it came from, and shows exactly where you save."]]],
    ["copier-service", "Copier service and repair", "Copier service and repair", "Print", "assets/gen-technician-1200.jpg", "Service and repair",
     "When the copier stops, <em>work stops</em>. We move.",
     "Certified field service technicians are on the road across Indianapolis and central Indiana every day. Our Customer Care Center processes requests Monday through Friday, 7:00am to 5:00pm, and responds within 24 hours. Remote diagnostics fix many problems without a visit at all.",
     [["Certified field technicians", "Factory-certified on Canon, Ricoh, Kyocera and HP, plus most other major brands."], ["Remote diagnostics", "Connectivity to your equipment lets engineers diagnose, and often fix, before a truck rolls."], ["25-point inspection", "A total call process with 25 points of inspection on every visit, so the next failure is caught early."]],
     ["Service and supply requests by phone, email or website", "Preventative maintenance plans with firmware and security updates", "Toner and supply replenishment and remote monitoring", "An honest repair-or-replace assessment when repair cost approaches the machine's value"],
     [["How fast can you repair my copier?", "Our Indianapolis-based technicians provide same-day service for most metro-area calls, with remote diagnostics resolving many issues without a visit."], ["What copier brands do you service?", "Canon, Ricoh, Kyocera and HP copiers and multifunction printers, and most other major office equipment brands. If you bought your equipment from another dealer, we can still help."], ["Should I repair or replace my copier?", "Our technicians assess honestly. If the repair cost approaches the value of the machine, we will recommend a replacement and can offer new, leased or pre-owned options."]]],
    ["production-print", "Production print", "Production print", "Print", "assets/print-1200.jpg", "Production press and color",
     "Your print shop, <em>one stop</em>.",
     "In-plant printing, variable data and color workflow for high-volume environments: presses, finishing, media profiles and workflow management software from one local partner. Every printed piece must have value, and digital color is finally affordable.",
     [["EFI Fiery", "EFI certified engineers, Impose and Compose, Job Master, Color Profiler Suite and Spot-On."], ["Skyline Web-to-Print", "Print Station, Product Manager, Template Manager, portal design and online editing."], ["Finishing and media", "The finishing equipment and media profiles to turn out high-quality, high-speed color that meets bottom-line demands."]],
     ["Presses for high volume, high value and high quality requirements", "Variable data for pieces that earn their postage", "Color management from profile to press", "A customizable approach to your individual needs"],
     [["Who is production print for?", "In-plant print rooms, marketing departments, schools and any organization whose outsourced print bill has become a line item. Bring a year of invoices and we will show the comparison."], ["Do you train our operators?", "Yes. EFI certified engineers set up the workflow and train your operators on the press and the software."]]],
    ["document-management", "Document management", "Document management", "Process", "assets/process-1200.jpg", "Enterprise content management",
     "Files, workflows and data <em>under one system</em>.",
     "Capture, store and automate business documents to cut paper and boost productivity. Custom Enterprise Content Management with OnBase and Square 9 captures, manages, stores, preserves and delivers information across your whole enterprise, keeping you connected and compliant.",
     [["Automated forms processing", "Exchange information automatically with anyone, anywhere, in any format, with Kofax intelligent capture."], ["Content management and workflow", "OnBase ECM and Square 9 Smart Search integrate with the productivity tools you already run."], ["Document scanning", "Workgroup, low-volume and high-volume scanners for any size document, in color or black and white."], ["Document finishing", "Pro-Bind thermal binding equipment and supplies for professional documents every time."]],
     ["Information governance: seamless workflow, streamlined sharing and reduced cost", "Accounts payable, HR onboarding and contract automation", "Records retention schedules that survive an audit", "Scanning from your existing VAF multifunction devices"],
     [["Which platforms do you implement?", "OnBase by Hyland and Square 9 Smart Search, with Kofax intelligent capture for forms. We recommend the platform after the assessment, not before."], ["Where do most organizations start?", "Accounts payable or a records backlog. Both pay back fastest, and both are questions on the Technology Strength Assessment."]]],
    ["document-conversion", "Document conversion", "Document conversion", "Process", "assets/gen-conversion-1200.jpg", "Document Conversion Center",
     "Paper out. <em>Searchable records in.</em>",
     "Paperless digital imaging and secure electronic storage from VAF's ultra-secure Document Conversion Center inside our 57,000-square-foot Indianapolis headquarters. Scan, index and retrieve your business documents without the cost of on-site or off-site storage.",
     [["Secure facility", "Not open to the public. Keycard access, background-checked staff, electronic badging."], ["Closed network", "Scanning and QC workstations are not internet accessible. Deliverables on encrypted media or secure transfer."], ["Chain of custody", "Strict documentation from pickup through processing and return or certified destruction."], ["Page-for-page QC", "Every document verified, every index value validated, every searchable PDF tested."]],
     ["Pickup and staging with a unique box identifier and signed custody", "Prep, imaging, reassembly and reconstruction to original condition", "Indexing keyed or digitally captured from every image", "Deliverables in TIF, PDF or searchable PDF, to your statement of work"],
     [["How secure is the conversion center?", "It sits inside VAF's single-tenant corporate facility. Access is by keycard, limited to conversion, management, sales and service personnel who have passed a detailed background check, and the scanning network is independent of VAF's own IT infrastructure and not internet accessible."], ["Can you handle patient records?", "Yes. For Johnson Memorial Health we inventoried, scanned and indexed 1.5 million patient files in 90 days, inside budget, with a certificate of destruction for the paper."]]],
    ["ai-consulting", "AI consulting", "AI consulting", "Process", "assets/ai-1200.jpg", "AI strategy and governance",
     "AI is already in your workplace. <em>Is it governed?</em>",
     "From strategy to governance: adopt AI responsibly, protect client trust and company data, and stay ahead of the competition. Employees are using AI every day whether you approved it or not. The biggest risk is not AI. It is the lack of guardrails.",
     [["Approved tools", "Which AI solutions are authorized for business use."], ["Data boundaries", "What types of information should never be entered into AI systems."], ["Human review requirements", "When AI-generated content requires sign-off before use."], ["Incident reporting", "A simple process for flagging and resolving AI misuse quickly."]],
     ["An AI Acceptable Use Policy and Framework your employees can understand and follow", "High-impact automation opportunities identified from the business problem, not the tool", "A responsible AI roadmap, starting with the free Technology Strength Assessment", "Guidance, governance and risk management from the partner that already runs your technology"],
     [["Where do we start with AI?", "With the business problem: the friction, the repeatable processes, the places where AI actually pays off. Then AI readiness: a policy and guardrails that let your team adopt it safely, then the use cases that deliver."], ["Is the AI playbook free?", "Yes. The 2026 CIO AI Playbook is a step-by-step guide to secure, strategic AI implementation, and the Technology Strength Assessment is complimentary."]]],
]
SERVICE_INDEX = {s[0]: s for s in SERVICES}
SERVICE_SLUGS = [s[0] for s in SERVICES]

BLOG = []


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
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    t = parts[0]
    if len(t) < 60 and len(parts) > 1:
        t = t + " " + parts[1]
    return t


def brief(text, n=150):
    first = text.split(". ")[0].rstrip(".")
    if len(first) <= n:
        return first + "."
    cut = first[:n]
    for sep in (", ", ": ", " and ", " with "):
        i = cut.rfind(sep)
        if i > n // 2:
            return cut[:i].rstrip(",:") + "."
    return cut.rsplit(" ", 1)[0].rstrip(",:") + "."


def post(slug, category, title, standfirst, image, image_alt, chapters, faq, target, cta_href="technology-strength-assessment.html", cta_label="Take the Technology Strength Assessment"):
    BLOG.append(dict(slug=slug, category=category, title=title, standfirst=standfirst, image=image, image_alt=image_alt,
                     chapters=chapters, faq=faq, target=target, cta_href=cta_href, cta_label=cta_label))


# ------------------------------------------------------------------ the six posts
# Each is aimed at a term vanausdall.com already ranks for (Semrush, 2026-09-08) or a question their pages already answer.
post("what-is-a-vcio", "Managed IT", "What a vCIO does, and when a 50-person company needs one",
     "A virtual chief information officer is a fractional executive, not a help desk. Here is what the role produces, what it costs relative to a hire, and the signs a business has outgrown IT without a strategy.",
     "assets/gen-hero-1200.jpg", "A technician with a tablet in front of server racks at dusk",
     [{"id": "the-role", "title": "The role, plainly", "paras": [
         "A vCIO is a fractional IT executive who provides strategic guidance, technology budgeting and planning without the cost of a full-time CIO. The help desk keeps today working. The vCIO decides what next year looks like: which systems to retire, what to budget, which vendors to keep, and how the technology plan lines up with the business plan.",
         "ul:A technology roadmap tied to your business goals;;An annual budget with the surprises taken out;;Vendor decisions made once, on evidence;;Regular planning meetings, not a call when something breaks",
         "callout:Where it sits in managed IT|VAF's managed IT bundle pairs vCIO guidance with the operational side: 24/7 monitoring, patching, help desk, on-site support and security. One partner accountable for the whole environment."]},
      {"id": "signs", "title": "Five signs you have outgrown IT without a strategy", "paras": [
         "ul:The IT budget is whatever last year cost plus the emergencies;;Nobody can list every system the business depends on;;A cyber insurance application asked questions nobody could answer;;Software and operating systems are in end-of-life status and still running;;Decisions about the cloud, phones and security are made by whoever the vendor called last",
         "Any two of these is a planning gap, not a staffing gap. Hiring another technician fixes neither."]},
      {"id": "cost", "title": "What it costs, against the alternative", "paras": [
         "A full-time CIO is a six-figure salary for work that a mid-sized company needs a few days a month. A vCIO delivers the planning cadence, the budget and the roadmap as part of a managed agreement, for a predictable monthly cost that also covers the monitoring and the help desk.",
         "pq:The vCIO is the part of managed IT that keeps the rest of it from being a very expensive way to react."]},
      {"id": "first-90-days", "title": "The first ninety days", "paras": [
         "It starts with the Technology Strength Assessment: information, print, process and communication, scored in ten to fifteen minutes online and then walked on site. The roadmap that follows says what to eliminate, what to optimize and what to leverage. Then the monitoring and security go live, and the planning meetings begin.",
         "ul:Assessment and scorecard;;Roadmap: eliminate, optimize, leverage;;Monitoring, patching and security deployed;;First budget and planning review"]}],
     [["Do we still need our internal IT person?", "Often, yes. Co-managed IT extends your team with specialty expertise, monitoring and security. The vCIO plans with them, not around them."], ["How often do we meet the vCIO?", "Regular planning tied to your business calendar, typically quarterly at minimum, and whenever a decision with a budget attached comes up."], ["Is the assessment really free?", "Yes. The Technology Strength Assessment is complimentary and takes ten to fifteen minutes to complete."]],
     "what is a vcio")

post("business-phone-systems-buyers-guide", "Communication", "Business phone systems in 2026: cloud, premise or hybrid, and how to choose",
     "The phone system decision is a five-year decision. Here is what changed, what each option costs you in flexibility, and the eight questions to ask before you sign with anyone, including us.",
     "assets/gen-phone-1200.jpg", "A professional on a desk phone and headset in a modern office",
     [{"id": "what-changed", "title": "What changed", "paras": [
         "The primary advantage of unified communications is one application for voice, chat, email, video and collaboration from any device. That is now the baseline, not the premium. What separates systems is reliability, how well the mobile app works when someone leaves the building, and whether the contact center features your customers feel are included or bolted on.",
         "callout:The sizes it fits|Single locations, multi-office teams and contact centers with application integration all run on the same platforms now. The design differs; the vendor should not."]},
      {"id": "three-options", "title": "Cloud, premise or hybrid", "paras": [
         "Cloud communications give you enterprise PBX and VoIP with no hardware to purchase or upgrade, managed and monitored 24/7, with advanced mobility, web conferencing and secure instant messaging through browsers and mobile devices. Premise systems still suit organizations with specific integration, compliance or connectivity needs. Hybrid keeps a premise core and adds cloud mobility on top.",
         "ul:Cloud: no capital investment, upgrades included, best mobility;;Premise: control and integration, capital cost, your own resilience to plan;;Hybrid: a premise core with cloud mobility, common in healthcare and government"]},
      {"id": "features", "title": "The features that actually get used", "paras": [
         "ul:Mobility: extension dialing, presence and the corporate directory on smartphones;;Contact center: caller information on the agent's screen as the call arrives;;Call recording that meets PCI DSS requirements;;Conferencing and collaboration with instant recording;;A disaster recovery plan for the phone system itself",
         "pq:Ask to see the mobile app used by a real customer, not a demo account."]},
      {"id": "eight-questions", "title": "Eight questions to ask any vendor", "paras": [
         "ul:Who installs it, and who answers when it breaks?;;How many systems have you deployed, and since when?;;What certifications do your engineers hold on this platform?;;Is the mobile app included or licensed separately?;;What happens to calls when the internet is down?;;Can call recording meet our compliance requirement?;;Is cooperative purchasing pricing available to us?;;What does year three cost, not year one?",
         "VAF has been in the telecom business since 1983, has deployed more than 4,000 systems, and holds Mitel Gold status for seven consecutive years, which places the company in the top 7% of 1,400 Mitel partners in North America. We support every system we install with our own local engineers."]}],
     [["Can we keep our phone numbers?", "Yes. Number porting is part of every deployment."], ["What about internet and carrier services?", "VAF's carrier evaluation is vendor neutral: SD-WAN, SIP trunking, broadband, fixed wireless and more, so you get one bill and one point of contact."], ["Do you serve outside Indianapolis?", "Our computer-dispatched, vendor-certified service fleet covers the Indianapolis metro area and the entire state of Indiana."]],
     "business phone systems", "services/business-phone-systems.html", "Talk to us about phone systems")

post("document-conversion-services-what-to-expect", "Process", "Document conversion services: what actually happens to your boxes",
     "Scanning is the easy part. The chain of custody, the indexing and the quality control are what make the files usable, and what keep you compliant. Here is the process, step by step.",
     "assets/gen-conversion-1200.jpg", "Boxes of records staged for scanning",
     [{"id": "why-convert", "title": "Why organizations convert", "paras": [
         "On-site storage consumes work space. Off-site storage is a monthly bill that never ends. Neither is searchable, and neither survives a demolition schedule. Document conversion replaces both with paperless, digital imaging and secure electronic storage, after a review of your retention policy that often means keeping less than you thought.",
         "callout:The retention review comes first|For Johnson Memorial Health, the law allowed everything older than 2009 to be properly destroyed. Scanning only what the policy required is how the project came in on budget."]},
      {"id": "chain-of-custody", "title": "Pickup, staging and chain of custody", "paras": [
         "Every container gets a unique box identifier at pickup, logged into a manifest and tracked through the imaging process. Batch separator sheets are created for each box, initialed at each stage. Chain of custody documentation is signed by the custodian of the records and by the VAF representative.",
         "ul:Unique box ID per container;;Manifest and batch logs;;Signed custody at handover;;Dashboard monitoring at box and batch level"]},
      {"id": "prep-and-imaging", "title": "Prep, imaging and reassembly", "paras": [
         "Staples and clips come out, separator sheets go in, small pages are taped to carrier sheets. Production scanners image every page. Then documents are reassembled to their original condition, staples replaced, separators removed, folders back in their containers, with the separator count validated against the batch.",
         "pq:If you asked for the paper back, it comes back the way it left."]},
      {"id": "indexing-and-qc", "title": "Indexing, quality control and the deliverable", "paras": [
         "Index fields are keyed or digitally captured from every image. A page-for-page quality control process confirms every page was captured. The deliverable is built to your statement of work, TIF, PDF or searchable PDF, tested for corruption, validated against the box and batch logs, and delivered on encrypted media or by secure transfer. If the paper is to be destroyed, you receive a certificate of destruction."]},
      {"id": "the-facility", "title": "Where it happens", "paras": [
         "VAF's Document Conversion Center sits inside the company's 57,000-square-foot, single-tenant headquarters in Indianapolis. Access is by keycard, limited to conversion, management, sales and service personnel who have passed a detailed background check. The conversion network is closed and not internet accessible, and data is backed up daily to a secure server room with regulatory-compliant off-site hosting available."]}],
     [["Can you scan on our site instead?", "Yes. Specialists can inventory and index on site, then either scan there or transport records to the conversion center under signed custody."], ["What formats do we receive?", "TIF, PDF or searchable PDF, to your statement of work, on CD, DVD or encrypted external drive, or by secure file transfer."], ["How long does a project take?", "It depends on volume and indexing depth. The Johnson Memorial project scanned 1.5 million files in 90 days."]],
     "document conversion services", "services/document-conversion.html", "Talk to us about document conversion")

post("physical-intrusion-detection-systems", "Security", "Physical intrusion detection: what it is, and why IT should own it now",
     "Video surveillance used to be a specialist's coaxial system. Today it is IP devices on your network, which makes it an IT decision with an IT budget. Here is what a modern system does and how it fits with the rest of your security.",
     "assets/security-1200.jpg", "A compliance and security concept image",
     [{"id": "what-it-is", "title": "What a physical intrusion detection system does", "paras": [
         "It captures activity throughout and around the perimeter of your office, detects entry where none should happen, and alerts the right people. Traditional systems were highly specialized and difficult to deploy and manage. IP-based, network-connected devices simplify the solution, and can bridge the gap between an existing coaxial system and a new IP system.",
         "ul:Cameras and sensors on the network, not a separate wiring plant;;Alerts to phones and the security operations center;;Recording with retention you control;;Integration with access control and visitor management"]},
      {"id": "why-it", "title": "Why IT should own it", "paras": [
         "Because the devices are on the network. A camera is an endpoint with a default password, firmware and an internet connection. Managed as part of IT it is patched, segmented and monitored. Managed by nobody it is the way in.",
         "pq:A camera nobody patches is not security. It is an unlocked door with a lens."]},
      {"id": "with-cyber", "title": "Physical and cyber, one plan", "paras": [
         "The Technology Strength Assessment asks whether visitors are screened, whether inbound packages are tracked from dock to desk, and whether you run periodic vulnerability scans. Those questions belong together. A security plan that stops at the firewall leaves the server room door out of scope.",
         "callout:Where VAF fits|Physical security is part of the Information pillar alongside managed IT, managed security and cloud, so the cameras, the network they sit on and the analysts who watch the alerts are one team."]},
      {"id": "questions", "title": "Questions before you buy", "paras": [
         "ul:Will this integrate with our existing coaxial system, or replace it?;;Who patches the cameras and how often?;;Where is video stored, and for how long?;;Who is alerted, and what do they do?;;Is this covered by our managed IT agreement?"]}],
     [["Can you reuse our existing cameras?", "Often. IP-based offerings can bridge a traditional coaxial system and a new IP system, so the transition can be staged."], ["Who monitors the alerts?", "Your team, VAF's security operations center, or both, depending on the plan you choose."], ["Is this part of managed IT?", "It can be. Physical security is delivered by the same Information team that runs managed IT and managed security."]],
     "physical intrusion detection", "services/cybersecurity.html", "Talk to us about security")

post("ai-acceptable-use-policy", "AI", "The AI acceptable use policy every business needs this year, section by section",
     "Employees are already pasting things into AI tools. A policy is not a barrier to innovation; it is the foundation for it. Here are the four sections a usable policy needs and the mistakes that make policies get ignored.",
     "assets/ai-1200.jpg", "A person holding a phone showing an AI assistant",
     [{"id": "the-risk", "title": "The risk of doing nothing", "paras": [
         "Without clear guidelines, even well-intentioned employees can expose sensitive data, violate compliance requirements or create legal liability. The common scenarios are mundane: confidential client data pasted into a public tool, AI-generated content sent to a customer without review, no way to report misuse, no list of which tools are approved.",
         "pq:The biggest risk is not AI itself. It is the lack of guardrails."]},
      {"id": "four-sections", "title": "The four sections", "paras": [
         "ul:Approved tools: which AI solutions are authorized for business use, and how a new one gets added;;Data boundaries: what information must never be entered into an AI system, in plain categories people recognize;;Human review: when AI-generated content requires sign-off before use, and by whom;;Incident reporting: a simple process for flagging and resolving misuse quickly, without blame",
         "callout:Keep it readable|A policy nobody can follow is a policy nobody follows. VAF's AI Acceptable Use Framework is written to be understood by every employee, not only by counsel."]},
      {"id": "mistakes", "title": "Three mistakes that get policies ignored", "paras": [
         "Banning everything, so people use personal devices instead. Writing it once and never updating the approved-tool list. Making the reporting process a confession rather than a fix.",
         "ul:A ban without an approved alternative moves the risk off your network, not out of your business;;The approved list changes quarterly; the policy has to say how;;Reporting must be safe, fast and lead to a fix"]},
      {"id": "beyond-policy", "title": "After the policy: readiness and use cases", "paras": [
         "The policy is AI readiness. What follows is the business problem: the friction, the repeatable processes, the places where automation actually pays off. That is where a responsible AI roadmap starts, and the free Technology Strength Assessment is how VAF starts it.",
         "ul:Policy and guardrails;;High-impact automation opportunities identified;;A responsible AI roadmap with owners and dates"]}],
     [["Do we need a lawyer to write this?", "Counsel should review it. The framework itself is a business document, written so employees can follow it."], ["Which tools should be approved?", "The ones with contractual data protections your organization can live with, for the tasks people actually do. The assessment surfaces which tasks those are."], ["Is there a template?", "The 2026 CIO AI Playbook walks through secure, strategic AI implementation step by step, and it is free."]],
     "ai acceptable use policy", "cio-ai-playbook.html", "Download the CIO AI Playbook")

post("copier-lease-vs-buy-indianapolis", "Print", "Copier lease vs. buy vs. rent in Indianapolis: the decision in one page",
     "Three ways to acquire the same device, three different totals. Most Indianapolis businesses lease. Here is when that is right, when it is not, and what to check at the end of the term.",
     "assets/copier-1200.jpg", "A business copier in an Indianapolis office",
     [{"id": "the-three", "title": "The three options, plainly", "paras": [
         "Leasing preserves capital, keeps monthly costs predictable, and lets you upgrade equipment at the end of every term. Lease agreements can include toner, service and maintenance in one rate. Buying makes sense when you plan to keep equipment long term or have capital budget to use; add a service agreement to protect the investment. Renting covers events, seasonal peaks, construction trailers and temporary offices without a long-term commitment.",
         "ul:Lease: predictable, fleet stays current, one rate can include service and toner;;Buy: lowest lifetime cost for stable volume, highest up-front;;Rent: month to month, for peaks, projects and trailers"]},
      {"id": "when-leasing-wins", "title": "When leasing wins", "paras": [
         "Steady volume, a preference for predictable monthly cost, and a fleet you want refreshed on a schedule. Most Indianapolis businesses lease their copiers for exactly those reasons.",
         "callout:Check the end of term|Ask what happens at the end: return, buy out, or renew. Expired leases still being paid is one of the first things the assessment finds. STAR Financial Bank was being overcharged for expired leases and outdated equipment before VAF removed them and negotiated new contracts statewide."]},
      {"id": "when-buying-wins", "title": "When buying wins", "paras": [
         "Stable volume, capital available, and a device that will run for many years. The cost per month over the life is lowest. The risk is that the device you buy today is the device you have in year seven."]},
      {"id": "when-renting-wins", "title": "When renting wins", "paras": [
         "A construction trailer, a seasonal peak, a temporary office, an event. Short-term copier rental is available throughout Indianapolis and central Indiana, and a rental can move into a lease when the project becomes permanent.",
         "pq:Lease the workhorses, rent the trailer, buy the device that never moves."]},
      {"id": "how-vaf-prices", "title": "How VAF prices it", "paras": [
         "Every engagement starts with a free print assessment: devices, volumes and costs mapped, then exactly where you save, with purchase, lease and rental priced for your real office. Canon, Ricoh, Kyocera and HP, supported for the life of the equipment by our Indianapolis Customer Care Center."]}],
     [["Can a lease include service and toner?", "Yes. Lease agreements can include toner, service and maintenance in one rate."], ["Can we rent for a construction project?", "Yes. Short-term rentals cover construction trailers, events, seasonal needs and temporary offices."], ["Do you take over devices from another vendor?", "Usually. The assessment covers every device regardless of where it came from and shows which are worth keeping."]],
     "copier lease indianapolis", "print-assessment.html", "Request the free print assessment")


# ------------------------------------------------------------------ six placeholder posts adapted from the category guides written for Kelly Office Solutions
KELLY_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kelly-office-solutions.content.json")
ADAPT = [("Kelly Office Solutions", "Van Ausdall & Farrar"), ("Kelly's", "VAF's"), ("Kelly", "VAF"), ("North Carolina", "Indiana"), ("the Triad, Charlotte and the Triangle", "Indianapolis, Fort Wayne and Evansville"),
         ("Winston-Salem", "Indianapolis"), ("Greensboro", "Fort Wayne"), ("Charlotte", "Indianapolis"), ("Raleigh", "Evansville"), ("five branches", "three offices"), ("five North Carolina offices", "three Indiana offices"), ("five offices", "three offices"), ("the branch", "the office"), ("your branch", "the Indianapolis office"), ("nearest branch", "nearest office"),
         ("Sharp, Ricoh, Savin, Konica Minolta and Brother", "Canon, Ricoh, Kyocera and HP"), ("Sharp, Ricoh, Savin, Konica Minolta, Brother and Epson", "Canon, Ricoh, Kyocera, HP and Brother"), ("Sharp, Ricoh and Savin, Konica Minolta, Brother and Epson", "Canon, Ricoh, Kyocera and HP"), ("Ricoh and Savin", "Canon and Ricoh"), ("Sharp", "Canon"), ("Savin", "Ricoh"), ("Konica Minolta", "Kyocera"),
         ("1-800-34-KELLY", "(317) 634-2913"), ("94.4", "93.4"), ("the industry average is in the 70s", "the average US company scores 10"), ("The industry average is in the 70s.", "The average US company scores 10."), ("DocuWare", "OnBase"), ("WatchGuard", "Fortinet"), ("Datto and WatchGuard", "Datto and Fortinet"), ("Wellsys and FloWater", "our partners"),
         ("since 1947", "since 1914"), ("factory-trained", "certified"), ("service-support.html#request", "support.html#request"), ("cost-calculator.html", "cost-calculator.html"), ("what-we-do.html#document-management", "services/document-management.html"), ("what-we-do.html#it", "services/managed-it.html"), ("what-we-do.html#copiers", "services/copiers.html"), ("assessment.html", "print-assessment.html")]
ADAPT_IMG = {"assets/dispatch-1200.jpg": "assets/support-1200.jpg", "assets/mps-2-1200.jpg": "assets/copier-1200.jpg", "assets/it-1200.jpg": "assets/it-1200.jpg", "assets/hero-1200.jpg": "assets/print-1200.jpg", "assets/wide-format-1200.jpg": "assets/process-1200.jpg", "assets/gso-office-1200.jpg": "assets/hq-1200.jpg", "assets/doc-mgmt-1200.jpg": "assets/healthcare-process-1200.jpg"}
ADAPT_SLUGS = ["what-managed-print-costs", "how-managed-print-services-transforms-business", "workstation-management-an-overview", "same-day-service-what-it-means", "all-in-one-office-printer-options-navigating-the-market-for-the-best-choice", "wide-format-printer-buying-guide-making-the-right-decision"]

def _adapt(x):
    if isinstance(x, str):
        for a, b in ADAPT:
            x = x.replace(a, b)
        return x
    if isinstance(x, list):
        return [_adapt(i) for i in x]
    if isinstance(x, dict):
        return {k: _adapt(v) for k, v in x.items()}
    return x

def adapted_posts():
    if not os.path.exists(KELLY_JSON):
        return
    kc = json.load(open(KELLY_JSON, encoding="utf-8"))
    for pg in kc["pages"]:
        if not pg["file"].startswith("blog/"):
            continue
        slug = pg["file"][5:-5]
        if slug not in ADAPT_SLUGS:
            continue
        art = next(sec for sec in pg["sections"] if sec["type"] == "article")
        faq = next((sec for sec in pg["sections"] if sec["type"] == "faq"), {"items": []})
        title = _adapt(art["heading"]).replace("in Indiana, and what they replace", "in Indiana, and what they replace")
        if slug == "what-managed-print-costs":
            title = "What managed print services cost in Indiana, and what they replace"
        chapters = _adapt(art["chapters"])
        post(slug, _adapt(art["category"]), title, _adapt(art["standfirst"]), ADAPT_IMG.get(art["image"], "assets/print-1200.jpg"), _adapt(art.get("image_alt", "")), chapters, _adapt(faq["items"]), slug.replace("-", " "),
             "print-assessment.html", "Request the free print assessment")

adapted_posts()


# ------------------------------------------------------------------ signature modules
def _flow(fid, eyebrow, heading, intro, steps, receive_label="What you receive"):
    return {"type": "flow", "id": fid, "alt": True, "eyebrow": eyebrow, "heading": heading, "intro": intro, "receive_label": receive_label,
            "steps": [{"label": a, "when": b, "summary": c, "title": d, "body": e, "receive": f} for a, b, c, d, e, f in steps]}


def _ba(bid, heading, b_title, b_body, b_items, a_title, a_body, a_items, b_eyebrow="Today", a_eyebrow="With VAF"):
    return {"type": "beforeafter", "id": bid, "bg": "#0f1e33", "eyebrow": "Before and after", "heading": heading,
            "before": {"eyebrow": b_eyebrow, "title": b_title, "body": b_body, "items": b_items},
            "after": {"eyebrow": a_eyebrow, "title": a_title, "body": a_body, "items": a_items}}


# VAF's own process, in their words: the Technology Strength Assessment, then eliminate, optimize, leverage;
# then "We Implement" and "We Monitor 24/7" from the print page.
FLOW_ENGAGEMENT = {"type": "flow", "id": "flow", "eyebrow": "How an engagement runs", "heading": "Four stages, and every one of them hands you something",
    "intro": "Click a stage. It starts with the Technology Strength Assessment and ends with a partner who is watching.",
    "steps": [
        {"label": "Assess", "when": "10 to 15 minutes, then a visit", "summary": "Your Technology Strength Score.", "title": "Know your Technology Strength Score",
         "body": "Four assessments in two parts each: information, print, process and communication. Ten to fifteen minutes online, then a specialist walks the office and confirms the answers against what is actually running.",
         "receive": ["A Technology Summary Scorecard", "Every device, system and vendor inventoried", "The gaps, in plain English"]},
        {"label": "Roadmap", "when": "Week 2", "summary": "Eliminate. Optimize. Leverage.", "title": "A roadmap that grows with you",
         "body": "What to eliminate because you do not need it, what to optimize because you already own it, and what to leverage to grow. Priced, sequenced, and tied to your business goals.",
         "receive": ["Eliminate, optimize and leverage lists", "Options priced side by side", "A sequence with dates"]},
        {"label": "Implement", "when": "A date you choose", "summary": "Handled for you.", "title": "We implement",
         "body": "Right-sized equipment, software, security and supplies, installed by VAF's own local people. Users trained before the technician leaves. Numbers ported. Monitoring switched on.",
         "receive": ["Install and training completed on site", "Monitoring live on every device", "One point of contact for every line"]},
        {"label": "Monitor", "when": "Ongoing", "summary": "24/7, from Indianapolis.", "title": "We monitor 24/7",
         "body": "Proactive monitoring, predictive maintenance and fast local repair keep you running. The Customer Care Center processes requests Monday through Friday, 7:00am to 5:00pm, and responds within 24 hours.",
         "receive": ["Alerts handled before they become tickets", "Supplies before they run out", "A 25-point inspection on every service call"]}]}

SEAL = {"type": "seal", "id": "seal", "tone": "dark", "eyebrow": "What every VAF customer gets", "heading": "Not a slogan. A list you can check.",
    "intro": "Each line is on vanausdall.com or in an audited third-party report today. Nothing here is aspirational.",
    "items": [["1914", "Serving Indiana since 1914", "Chosen as a distributor for the Thomas Edison Company. Privately owned in Indianapolis ever since."],
              ["93.4", "A service score audited by someone else", "Net Promoter Score collected and audited by CEO Juice. World Class every year since 2019. The average US company scores 10."],
              ["SOC 2", "SOC 2 certified", "Our SOC for Service Organizations certification means we meet the highest standards for protecting your data."],
              ["Gold", "Mitel Gold, seven years running", "Top 7% of 1,400 Mitel partners in North America. In the telecom business since 1983, over 4,000 systems deployed."],
              ["250+", "Years of IT experience on staff", "The Vsecure IT team collectively, with CISSP personnel and NSE-7 certified Fortinet engineers."],
              ["25", "Points of inspection, every call", "A total call process on every service visit, so the next failure is caught early."],
              ["24 hr", "Response from the Customer Care Center", "Requests processed Monday through Friday, 7:00am to 5:00pm, and answered within 24 hours."],
              ["57,000", "Square feet of headquarters", "Built in 2006 at 6430 E 75th Street, home to the secure Document Conversion Center."]],
    "source": "Sources: vanausdall.com (about, why VAF, copy print, support, document conversion pages), CEO Juice NPS report, SOC 2 certification as displayed on vanausdall.com."}

BEFORE_AFTER = {"type": "beforeafter", "id": "ba", "bg": "#0f1e33", "eyebrow": "One roof", "heading": "Drag to see what changes when the office has one number to call",
    "before": {"eyebrow": "Today, in most offices", "title": "Five vendors, five invoices", "body": "Nobody owns the whole picture, so nobody sees the cost.",
               "items": ["A copier dealer, an IT firm and a phone company who blame each other", "Toner bought at retail when a device runs dry", "Backups nobody has tested and a firewall nobody patches", "Records in a storage room scheduled for demolition", "Employees using AI tools nobody approved"]},
    "after": {"eyebrow": "With VAF", "title": "Everything under one roof", "body": "Information, communication, print and process from one Indiana partner since 1914.",
              "items": ["Copiers, print, IT and phones under one agreement and one Customer Care Center", "Supplies shipped on usage, 24/7 monitoring, 25-point inspections", "vCIO, security operations center and managed continuity", "Records scanned, indexed and searchable, paper destroyed with a certificate", "An AI acceptable use policy and a roadmap"]}}

WHEEL_ITEMS = [[p[0], p[1], p[2], p[3]] for p in PILLARS]

HERO_LAYERED = {"type": "hero-layered", "id": "hero", "eyebrow": "Business technology simplified, since 1914",
    "heading": "Everything your business runs on, <em>under one roof</em>.",
    "subhead": "IT support, copiers and print, phone systems, document workflow and AI guidance for Indiana businesses. One local partner, one assessment to start, one number to call.",
    "primary": {"label": "Take the Technology Strength Assessment", "href": "technology-strength-assessment.html"}, "secondary": {"label": "Schedule a consultation", "href": "contact.html"},
    "bg": "#0f1e33", "image": "assets/gen-hero-plate-2100.jpg", "image_w": 2100, "image_h": 891,
    **({"model": MFP_MODEL, "poster": "assets/fleet/mfp.png", "model_alt": "A multifunction copier, rotating. Drag to turn it."} if MFP_MODEL else {}),
    "stats": [["1914", "Serving Indiana since"], ["93.4", "Net Promoter Score, audited"], ["SOC 2", "Certified service organization"], ["4,000+", "Phone systems deployed since 1983"]],
    "card_a": {"eyebrow": "Start here", "title": "The Technology Strength Assessment", "body": "Ten to fifteen minutes. Information, print, process and communication, scored.", "items": ["What to eliminate", "What to optimize", "What to leverage to grow"], "href": "technology-strength-assessment.html", "label": "How it works"},
    "card_b": {"eyebrow": "Already a customer?", "title": "The Client Service Center", "body": "A person answers. Monday to Friday, 7 to 5.", "links": [["Request support", "support.html#request"], ["Order supplies", "support.html#supplies"], ["IT support", "support.html#it"], [f"Call {PHONE}", PHONE_HREF]]},
    "note": "The photography here is generated for the preview and labelled as such; a shoot at the 75th Street headquarters and with technicians in the field replaces it in the build, along with Canon, Ricoh, Kyocera and HP product models."}

HOTSPOTS = {"type": "hotspots", "id": "office", "eyebrow": "The whole office", "heading": "Four pillars, one floor plan", "intro": "Click a number. Everything an office runs on, and the VAF page for each.",
    "image": "assets/office-iso-1600.jpg", "image_w": 1600, "image_h": 893, "alt": "An overhead illustration of an office with a copier room, a server room, a records room, a lounge and desks",
    "items": [
        {"x": 27, "y": 46, "k": "Print", "title": "The copier room", "body": "Canon, Ricoh, Kyocera and HP multifunction devices under one managed print agreement, with supplies that arrive before they run out.", "href": "services/copiers.html", "label": "Copiers and managed print"},
        {"x": 82, "y": 14, "k": "Information", "title": "The server room", "body": "Managed IT, Vsecure cybersecurity, cloud and continuity. Monitored 24/7 from Indianapolis, with a vCIO planning what comes next.", "href": "services/managed-it.html", "label": "Managed IT services"},
        {"x": 93, "y": 42, "k": "Communication", "title": "The desk phone", "body": "Mitel, RingCentral, 8x8 and Elevate unified communications that follow your people to their smartphones. In telecom since 1983.", "href": "services/business-phone-systems.html", "label": "Business phone systems"},
        {"x": 64, "y": 71, "k": "Process", "title": "The scan station", "body": "Every multifunction device scans straight into OnBase or Square 9 workflows: accounts payable, HR, contracts, records.", "href": "services/document-management.html", "label": "Document management"},
        {"x": 88, "y": 66, "k": "Process", "title": "The records wall", "body": "Boxes of paper become searchable records at the secure Document Conversion Center, with a certificate of destruction at the end.", "href": "services/document-conversion.html", "label": "Document conversion"},
        {"x": 16, "y": 58, "k": "Print", "title": "The desks", "body": "Desktop printers right-sized to how many the office needs, folded into the same managed print report as the copiers.", "href": "services/managed-print.html", "label": "Managed print"},
        {"x": 62, "y": 38, "k": "Process", "title": "The meeting area", "body": "Where AI shows up first: drafting, summarizing, automating. An acceptable use policy and a roadmap before the tools.", "href": "services/ai-consulting.html", "label": "AI consulting"}]}

CUSTOMER_WALL = {"type": "partners", "id": "customers", "caption": "Trusted across Indiana: on the record in our case studies", "items": ["Tippecanoe School Corporation", "STAR Financial Bank", "Johnson Memorial Health", "City of Anderson", "City of Bloomington", "Berry Global", "Beck's Hybrids", "Shiel Sexton", "Bowen Engineering", "Gailey Eye Clinic", "Town of Bargersville", "Mid-City Supply", "Phalen Leadership Academy", "Ellinger Riggs Insurance"]}

NUMBERS = {"type": "stats", "id": "numbers", "alt": True, "items": [["1,500,000", "Patient files scanned in 90 days for Johnson Memorial Health"], ["1,000,000", "Dollars saved over one contract for Tippecanoe School Corporation"], ["4,000", "Phone systems deployed since 1983"], ["250", "Years of combined IT experience on the Vsecure team"]]}

PILLARS_CARDS = {"type": "cards", "id": "pillars", "eyebrow": "Four pillars", "heading": "Information, communication, print and process, from one partner",
    "items": [[p[0], p[1]] for p in PILLARS]}

FLEET = {"type": "fleet", "id": "fleet", "heading": "The fleet, at a glance", "intro": "Every device family VAF sells and services. Generated product renders for the preview; Canon, Ricoh, Kyocera and HP models replace them.",
    "items": [
        {"title": "Multifunction copiers", "band": "Workgroup to department", "brands": "Canon, Ricoh, Kyocera, HP", "image": "assets/fleet/mfp.png", "bullets": ["Print, scan, copy, fax", "Secure release and scan to OnBase"], "href": "services/copiers.html", "label": "Copiers and printers"},
        {"title": "Desktop printers", "band": "Desk and small team", "brands": "HP, Brother, Kyocera", "image": "assets/fleet/printer.png", "bullets": ["Color and mono", "Folded into managed print"], "href": "services/managed-print.html", "label": "Managed print"},
        {"title": "Wide format", "band": "Plans, posters, signage", "brands": "Canon, HP", "image": "assets/fleet/wide-format.png", "bullets": ["Plan sets in house", "Engineering and construction"], "href": "industries/engineering-construction.html", "label": "Engineering and construction"},
        {"title": "Production print", "band": "High volume, inline finishing", "brands": "EFI Fiery, Skyline web-to-print", "image": "assets/fleet/production.png", "bullets": ["Variable data", "Color management from profile to press"], "href": "services/production-print.html", "label": "Production print"}]}

PROOF = {"type": "proof", "id": "proof", "tone": "dark", "eyebrow": "Measured, not claimed", "value": "93.4", "text": "Net Promoter Score, collected and audited by CEO Juice from VAF customers after every service call. World Class, above 70, every year since 2019. The average US company scores 10.", "source": "CEO Juice is an independent company with an audited process. The numbers cannot be changed, even when a customer scores us low in error."}

FILM = {"type": "video", "id": "film", "eyebrow": "Who we are", "heading": "Privately owned in Indianapolis since 1914", "intro": "Filmed with VAF people at the 75th Street headquarters.", "youtube": "i-q4U5SnvaM", "poster": "assets/careers-1200.jpg", "title": "What it's like to work at Van Ausdall & Farrar", "caption": "VAF's own film, from vanausdall.com"}

MODEL3D = {"type": "model3d", "id": "model", "alt": False, "eyebrow": "Take a closer look", "heading": "Walk around one before it arrives", "intro": "A generated stand-in multifunction device for the preview. Drag to rotate. Canon, Ricoh, Kyocera and HP product imagery replaces it in the build.", "poster": "assets/mfp-poster-1200.jpg", "alt": "A white and charcoal multifunction copier on a cabinet, rotatable", "cta": {"label": "See copiers and printers", "href": "services/copiers.html"}, **({"model": MFP_MODEL} if MFP_MODEL else {})}

TABS_MARKETS = {"type": "tabs", "id": "markets", "eyebrow": "Industries", "heading": "Built around how your industry runs",
    "items": [{"label": i[1], "title": i[1], "body": i[4], "bullets": i[5][:3], "image": i[2], "image_alt": i[1], "href": f"industries/{i[0]}.html", "link_label": f"Technology for {i[1].lower()}"} for i in INDUSTRIES]}

MAP = {"type": "map", "id": "map", "outline": "IN", "alt": "Map of Indiana with Van Ausdall & Farrar offices", "heading": "Three offices, one service fleet, the whole state", "intro": "Headquartered in Indianapolis with offices in Fort Wayne and Evansville. A computer-dispatched, vendor-certified service fleet covers the Indianapolis metro and the entire state of Indiana.", "ring": 44,
       "items": [{"name": "Indianapolis", "lon": -86.062, "lat": 39.887, "href": "locations/indianapolis.html", "sub": "6430 E 75th Street, headquarters", "hq": True, "label_dx": 10, "label_dy": 4},
                 {"name": "Fort Wayne", "lon": -85.145, "lat": 41.089, "href": "locations/fort-wayne.html", "sub": "1241 N Wells Street", "label_dx": -96, "label_dy": -10},
                 {"name": "Evansville", "lon": -87.556, "lat": 37.975, "href": "locations/evansville.html", "sub": "(812) 424-5736", "label_dx": 10, "label_dy": 16}]}

TIMELINE = {"type": "timeline", "id": "story", "eyebrow": "The story", "heading": "From an Edison dealership to Indiana's largest office technology provider",
    "items": [["1914", "Oscar K. Van Ausdall", "Chosen as an Edison Business Phonograph dealer for the state of Indiana. The Thomas Edison Company invented the wax cylinder dictating machine."],
              ["1940", "Carl F. Farrar", "Joins as general manager and partner, later buying the business. Mr. Van Ausdall stays on until retiring in 1957 at 73."],
              ["1960", "Clyde von Grimmenstein", "Becomes president after joining in sales in 1950, and stays active until retiring at 84."],
              ["1983", "Telecom", "VAF enters the telephone business. More than 4,000 systems deployed since."],
              ["1994", "Eric von Grimmenstein", "Grew up in the business, joined in 1977 after Purdue, and becomes president."],
              ["2006", "6430 E 75th Street", "The 57,000-square-foot corporate headquarters opens in Indianapolis."],
              ["Today", "Four pillars, one roof", "Information, communication, print and process for Indiana and the Midwest. Privately owned, still in Indianapolis."]]}

VALUES = {"type": "values", "id": "values", "alt": True, "eyebrow": "Mission and vision", "heading": "What the company is for",
    "items": [["Mission", "Provide value-driven technology solutions while delivering a world class customer experience and have a positive impact on our community."],
              ["Vision", "To implement technology to improve the human experience."],
              ["Measured, not claimed", "Our Net Promoter Score is collected and audited by CEO Juice, an independent company whose process we do not control. It is 93.4. The average US company scores 10, and anything above 70 is World Class."]]}

CS_QUOTE = {"type": "casestudy", "id": "casestudy", "tone": "dark", "eyebrow": "Case study", "heading": "1,200 devices became 300, and a school corporation saved a million dollars",
    "quote": "Tippecanoe was won over by Van Ausdall's process. By cutting overall equipment from 1,200 machines to just over 300 new machines, the school corporation has seen $1,000,000 in savings over the life of the contract.",
    "attribution": "Tippecanoe School Corporation case study, vanausdall.com",
    "metrics": [["Devices", "1,200 to 300", "Fleet consolidated across every building"], ["Savings", "$1M", "Over the life of the contract"], ["IT time", "20%", "Of IT staff time was going to print issues"], ["Vendors", "10 to 1", "Copy and print vendors replaced by one"]]}


def service_page(slug, title, navlabel, pillar, image, eyebrow, heading, subhead, benefits, bullets, faq):
    secs = [
        {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": heading, "subhead": subhead,
         "primary": {"label": "Schedule a consultation", "href": "contact.html"}, "secondary": {"label": "Take the assessment", "href": "technology-strength-assessment.html"},
         "image": image, "image_alt": title, "image_w": 1200, "image_h": 800},
        {"type": "cards", "alt": True, "eyebrow": "What is included", "heading": f"What changes with VAF {title.lower()}", "items": benefits},
        {"type": "detail", "eyebrow": "The specifics", "heading": "What you get, and what it rests on", "body": "Everything below is on vanausdall.com today or in a certification we hold. Nothing on the list is an add-on.", "bullets": bullets, "image": SERVICE_DETAIL_IMAGE.get(slug, image), "flip": True},
    ]
    for i, m in enumerate(SERVICE_MODULES.get(slug, [])):
        secs.insert(2 + i, m)
    if slug == "copiers":
        secs.insert(3, dict(FLEET, alt=False, heading="The rest of the fleet"))
        secs.insert(2, dict(MODEL3D, alt=True, heading="Walk around one", intro="A generated stand-in for the preview. Drag to rotate; your Canon, Ricoh, Kyocera and HP models replace it."))
    if slug == "managed-it":
        secs.insert(2, {"type": "proof", "id": "proof", "alt": True, "eyebrow": "In our own words", "value": "24/7", "text": SIGMON[0], "source": f"{SIGMON[1]}, {SIGMON[2]}"})
    if slug == "managed-print":
        secs.insert(2, {"type": "process", "eyebrow": "How it works", "heading": "Three steps, from the copy print page", "stages": [
            ["Free print assessment", "Produces: your devices, volumes and costs mapped, and exactly where you save."],
            ["We implement", "Produces: right-sized copiers and printers, software, security and supplies, handled for you."],
            ["We monitor 24/7", "Produces: proactive monitoring, predictive maintenance and fast local repair."]]})
        secs.insert(3, {"type": "stats", "alt": True, "items": [["100+", "Years in business"], ["30%", "Average printing cost reduction"], ["24/7", "Proactive support and monitoring"], ["25", "Point inspections on every call"]]})
        secs.append({"type": "comparison", "heading": "Lease, rent or buy?", "intro": "The assessment prices all three for your real volume. Here is how they usually compare.",
                     "columns": [{"label": "Lease", "recommended": True}, {"label": "Rent"}, {"label": "Buy"}],
                     "rows": [["Best for", "Steady volume, a fleet kept current", "Peaks, projects, construction trailers", "Stable volume, long device life"],
                              ["Term", "Fixed, with an upgrade at the end", "Month to month", "None"],
                              ["Up-front cost", "Low", "Low", "Highest"],
                              ["Lifetime cost", "Moderate", "Highest per month", "Lowest if the device runs for years"],
                              ["Service and toner", "Can be included in one rate", "Usually included", "Add a service agreement"]],
                     "note": "Terms and rates are set after the assessment. Nothing here is a quote."})
    cs = [c for c in CASE_STUDIES if c[6] and c[0] in SERVICE_CASES.get(slug, [])]
    if cs:
        c = cs[0]
        secs.append({"type": "casestudy", "eyebrow": "Case study", "heading": c[3], "quote": CS_QUOTES[c[0]], "attribution": f"{c[1]} case study, vanausdall.com",
                     "metrics": CS_METRICS[c[0]]})
    secs += [
        {"type": "testimonials", "alt": True, "heading": "What customers say after a service call", "items": [COMMENTS[SERVICE_SLUGS.index(slug) % len(COMMENTS)], COMMENTS[(SERVICE_SLUGS.index(slug) + 3) % len(COMMENTS)]]},
        {"type": "faq", "heading": "Questions we get about " + navlabel.lower(), "items": faq},
        {"type": "leadform", "alt": True, "id": "consult", "heading": "Speak with a solutions expert", "body": "Tell us a little about your organization. A person from the Indianapolis office replies to set a time, not an autoresponder.", "submit": "Schedule my consultation", "note": f"Or call {PHONE}, Monday through Friday, 7:00am to 5:00pm."},
    ]
    service_schema = {"@context": "https://schema.org", "@type": "Service", "@id": f"{SITE}/services/{slug}#service", "name": title, "serviceType": title,
                      "description": re.sub(r"<[^>]+>", "", subhead), "provider": {"@id": f"{SITE}/#organization"},
                      "areaServed": [{"@type": "State", "name": "Indiana"}, {"@type": "City", "name": "Indianapolis"}, {"@type": "City", "name": "Fort Wayne"}, {"@type": "City", "name": "Evansville"}],
                      "url": f"{SITE}/services/{slug}", "category": pillar}
    return {"file": f"services/{slug}.html", "title": f"{SERVICE_TITLES.get(slug, title)} | Van Ausdall & Farrar", "description": desc(subhead), "schema": [service_schema], "crumbs": [["Home", "index.html"], ["Solutions", "solutions.html"], [navlabel, f"services/{slug}.html"]], "sections": secs}


SERVICE_TITLES = {"managed-it": "Indianapolis Managed IT Services and vCIO", "business-phone-systems": "Business Phone Systems in Indianapolis and Indiana", "copiers": "Copier Sales, Lease and Rental in Indianapolis", "managed-print": "Managed Print Services in Indianapolis", "copier-service": "Copier Service and Repair in Indianapolis", "document-conversion": "Document Conversion and Scanning Services, Indianapolis", "cybersecurity": "Managed Cybersecurity and SOC as a Service, Indiana", "cloud": "Cloud Services in Indianapolis", "ai-consulting": "AI Consulting for Indiana Businesses"}
SERVICE_DETAIL_IMAGE = {"managed-it": "assets/gen-hero-1200.jpg", "cybersecurity": "assets/security-1200.jpg", "cloud": "assets/gen-hero-1200.jpg", "business-continuity": "assets/security-1200.jpg", "business-phone-systems": "assets/healthcare-comms-1200.jpg", "copiers": "assets/team-1200.jpg", "managed-print": "assets/copier-1200.jpg", "copier-service": "assets/print-1200.jpg", "production-print": "assets/team-1200.jpg", "document-management": "assets/healthcare-process-1200.jpg", "document-conversion": "assets/hq-1200.jpg", "ai-consulting": "assets/ai-hand-1200.jpg"}
SERVICE_CASES = {"managed-print": ["tippecanoe-school-corporation"], "copiers": ["star-financial"], "document-conversion": ["johnson-memorial-hospital"], "document-management": ["city-of-anderson"], "managed-it": [], "business-phone-systems": []}
CS_QUOTES = {
    "tippecanoe-school-corporation": "Tippecanoe was won over by Van Ausdall's process. By cutting overall equipment from 1,200 machines to just over 300 new machines, the school corporation has seen $1,000,000 in savings over the life of the contract.",
    "star-financial": "Through the Technology Strength Assessment process, Van Ausdall & Farrar removed the expired leases and negotiated new contracts on upgraded equipment across the state. STAR Financial Bank experienced a 70% cost savings over their original arrangement.",
    "johnson-memorial-hospital": "Van Ausdall was able to scan over 1.5 million files in just 90 days. Once the project was finished and all files were indexed, the paper files were safely destroyed and Van Ausdall issued a certificate of destruction.",
    "city-of-anderson": "The onsite updated equipment, software and process improvements that were installed, implemented and maintained by Van Ausdall & Farrar have created over $40,000 in annual savings.",
}
CS_METRICS = {
    "tippecanoe-school-corporation": [["Devices", "1,200 to 300", "Fleet consolidated across every building"], ["Savings", "$1M", "Over the life of the contract"], ["IT time", "20%", "Of IT staff time had gone to print issues"], ["Vendors", "10 to 1", "Copy and print vendors replaced by one"]],
    "star-financial": [["Savings", "70%", "Over the original arrangement"], ["Time", "5 months", "To phase one results"], ["Contracts", "1", "Vendor and location managing every contract"], ["Next", "DM and MPS", "Document and print management being added"]],
    "johnson-memorial-hospital": [["Files", "1.5M", "Patient records scanned and indexed"], ["Time", "90 days", "From inventory to certificate of destruction"], ["Boxes", "500+", "Against an initial estimate of 100"], ["Budget", "Under", "By scanning only what retention required"]],
    "city-of-anderson": [["Savings", "$40,000", "Every year"], ["Since", "2003", "A preferred vendor to the city"], ["Security", "2D bar code", "Document security on print and mail"], ["Purchasing", "1 site manager", "Departmental purchases streamlined through FM"]],
}

SERVICE_MODULES = {
    "managed-it": [
        _ba("ba", "Drag to compare break-fix IT with a managed partnership",
            "Call when it breaks", "Every problem is a surprise, and every invoice is a different size.",
            ["Backups nobody has tested", "Updates applied when someone remembers", "Security that ends at the antivirus", "An hourly invoice after every outage", "No plan, no budget, no roadmap"],
            "Managed, monitored, one package", "Security, strategy and support bundled together for one predictable monthly cost.",
            ["Backups monitored and restoration tested", "Patching on a schedule, 24/7 monitoring", "MDR, MFA, awareness training and a SOC", "One monthly number", "A vCIO with a roadmap and a budget"]),
        _flow("flow", "How managed IT starts", "Four steps to a network someone is watching", "Click a step.",
            [("Assess", "Week 1", "Your Technology Strength Score.", "The information assessment", "Vulnerability scans, MFA, password policy, backup, patching, firewall reviews, disaster recovery and end-of-life systems: the twenty questions on the assessment, answered and verified.", ["A scorecard", "Every system and risk listed", "A recommendation in writing"]),
             ("Plan", "Week 2", "Eliminate, optimize, leverage.", "A plan with a fixed monthly number", "What to fix now, what to replace, what to monitor, and the monthly amount that covers it.", ["Remediation list, ranked", "Monthly scope and price", "Microsoft or Google licensing reviewed"]),
             ("Onboard", "Weeks 3 to 4", "Agents, backup, security.", "Monitoring and protection go live", "Monitoring agents, backup, MDR and MFA are deployed, awareness training begins, and users learn how to reach the help desk.", ["Monitoring on every device", "Backup running and verified", "Help desk live"]),
             ("Run", "Ongoing", "Reviewed with your vCIO.", "Run, report and review", "Patching, backup checks and security alerts are handled as they arise. The vCIO reviews the roadmap and the budget with you on a schedule.", ["Patch and backup reports", "Security alerts handled by the SOC", "Scheduled vCIO planning"])])],
    "managed-print": [
        _ba("ba", "Drag to compare a fleet that is managed with one that is not",
            "Every printer on its own", "Nobody knows what the fleet costs because nobody owns it.",
            ["Toner bought at retail when a device runs dry", "Service calls placed by whoever notices first", "No count of devices, pages or cost", "IT staff clearing jams between real work", "Devices replaced on age, not on evidence"],
            "One fleet, one report", "Monitored, supplied and reported on, with a 25-point inspection on every call.",
            ["Supplies replenished automatically", "Failing devices spotted before the office does", "Cost per page by device, mono and color", "IT time returned to IT", "Consolidate or upgrade on the data"])],
    "copiers": [
        _flow("flow", "From first call to first page", "Four steps between the call and the first page", "Click a step. Each one ends with something in your hands.",
            [("Assess", "Visit 1", "Devices, volumes and costs.", "A free print assessment", "We map your devices, volumes and costs, then show exactly where you save. Free and without obligation.", ["Fleet inventory with volumes", "Cost by device", "The recommendation in writing"]),
             ("Recommend", "Week 1", "The device and the terms.", "The right device, priced three ways", "Canon, Ricoh, Kyocera or HP matched to your volume and security requirements, with purchase, lease and rental shown side by side.", ["Model and configuration", "Lease, rent and buy compared", "Service and supplies shown"]),
             ("Install", "A date you choose", "Configured and trained.", "Delivered, configured, trained", "User authentication, secure print release, cloud scanning and mobile printing configured, and every user trained before the technician leaves.", ["Drivers and scan destinations set up", "Users trained on site", "Old device removed if you ask"]),
             ("Support", "Ongoing", "One Customer Care Center.", "Supported for the life of the equipment", "Request service by phone, email or website. The Customer Care Center responds within 24 hours, and technicians perform a 25-point inspection on every visit.", ["Same-day service for most metro calls", "Remote diagnostics", "Preventative maintenance plans"])])],
    "business-phone-systems": [
        _ba("ba", "Drag to compare point solutions with unified communications",
            "Six applications for six jobs", "Phone, chat, email, video, conferencing and collaboration, each from a different vendor.",
            ["A desk phone that stops at the door", "Conferencing on a separate license", "No record of who called or why", "Six applications to train and support", "A carrier bill nobody has audited"],
            "One application, one partner", "Voice, chat, video and collaboration from any device, managed and monitored 24/7.",
            ["Smartphones on the corporate system with presence and directory", "Conferencing and collaboration built in", "Call recording that meets PCI DSS", "One vendor, one training, one support line since 1983", "A vendor-neutral carrier evaluation and one bill"])],
    "document-conversion": [
        _flow("flow", "The closed-loop process", "Seven stages, with signed custody at every handover", "Click a stage. This is the process from the document conversion page.",
            [("Pickup", "Day 1", "A box ID and a signature.", "Pickup and staging", "A unique box identifier is assigned to each container, logged into a manifest and tracked throughout. Chain of custody is signed by the records custodian and the VAF representative.", ["Manifest", "Signed custody", "Batch separator sheets per box"]),
             ("Prep", "Week 1", "Staples out, separators in.", "Document prep", "Binding elements removed, separator sheets placed to mark document boundaries, small pages taped to carrier sheets.", ["Prepped batches", "Document boundaries marked", "Exceptions handled"]),
             ("Image", "Weeks 1 to N", "Production scanning.", "Document imaging", "Every page imaged on production scanning equipment inside the closed conversion network.", ["Images per batch", "Batch-level tracking", "Team lead sign-off"]),
             ("Reassemble", "Same week", "Back to original condition.", "Reassembly and reconstruction", "Staples and clips replaced, separators removed, documents back in folders and containers, separator counts validated.", ["Documents as they arrived", "Counts validated", "Containers ready to return"]),
             ("Verify", "Same week", "Page for page.", "Imaging QC", "A page-for-page quality control process ensures every page was captured at the highest quality.", ["QC log", "Recaptures completed", "Separator count validated"]),
             ("Index", "Weeks 2 to N", "Keyed or captured.", "Indexing", "Index fields keyed or digitally captured from every image, to the statement of work.", ["Index values per document", "Validated against images", "Searchable where specified"]),
             ("Deliver", "Final week", "Tested, encrypted, certified.", "Deliverable creation and QC", "TIF, PDF or searchable PDF, tested for corruption and validated against box and batch logs. Delivered on encrypted media or by secure transfer. Certificate of destruction if the paper is destroyed.", ["Deliverable media", "Validation report", "Certificate of destruction"])])],
    "cybersecurity": [
        _ba("ba", "Drag to compare basic antivirus with Vsecure coverage",
            "Antivirus and hope", "The coverage most small businesses had five years ago, and insurers no longer accept.",
            ["Antivirus with signatures updated when someone remembers", "Patching by whoever has time", "A firewall installed once and never reviewed", "No one watching at 2am", "Cyber insurance application questions nobody can answer"],
            "The new basic coverage", "EDR/XDR, proactive patching and monitoring, and a next-generation firewall, with a SOC watching.",
            ["Sophos Intercept X Advanced with XDR on every base plan", "Patching and monitoring from Datto", "Co-managed Fortinet firewall and Fabric services", "SOC as a service with a dedicated analyst option", "Insurer requirements met, with a CISSP to help with planning"])],
}

INDUSTRY_HEADINGS = {"education": "Fewer devices, <em>more of the budget in classrooms</em>.", "engineering-construction": "Technology that works <em>from the trailer</em>.", "financial-services": "Expired leases out. <em>Security in.</em>", "healthcare": "Protected information is <em>patient safety</em>.", "insurance": "Eliminate, optimize, <em>then compete</em>.", "manufacturing-logistics": "Print, network and documents <em>where the work happens</em>.", "real-estate": "Technology that <em>closes from anywhere</em>.", "government": "Service levels constituents <em>can trust</em>."}


def industry_page(slug, name, image, one, body, bullets, cases):
    secs = [
        {"type": "hero", "layout": "centered", "eyebrow": f"Industries: {name}", "heading": INDUSTRY_HEADINGS.get(slug, one), "subhead": one,
         "primary": {"label": "Schedule a consultation", "href": "contact.html"}, "secondary": {"label": "Take the assessment", "href": "technology-strength-assessment.html"},
         "image": image, "image_alt": f"{name} at work", "image_w": 1200, "image_h": 800},
        {"type": "detail", "eyebrow": "What we set up", "heading": f"Built for how {name.lower()} runs", "body": body, "bullets": bullets},
    ]
    full = [CS_INDEX[c] for c in cases if CS_INDEX[c][6]]
    if full:
        c = full[0]
        secs.append({"type": "casestudy", "alt": True, "eyebrow": "Case study", "heading": c[3], "quote": CS_QUOTES[c[0]], "attribution": f"{c[1]} case study, vanausdall.com", "metrics": CS_METRICS[c[0]]})
    if cases:
        secs.append({"type": "resources", "heading": f"{name} customers on the record", "intro": "Every case study is published on vanausdall.com today.", "items": [[CS_INDEX[c][2], CS_INDEX[c][1], CS_INDEX[c][3], "Read the case study", f"case-studies/{c}.html"] for c in cases]})
    secs += [
        {"type": "testimonials", "alt": True, "heading": "What customers say after a service call", "items": [COMMENTS[INDUSTRIES.index(IND_INDEX[slug]) % len(COMMENTS)], COMMENTS[(INDUSTRIES.index(IND_INDEX[slug]) + 4) % len(COMMENTS)]]},
        {"type": "leadform", "id": "consult", "heading": "Start with the Technology Strength Assessment", "body": f"Ten to fifteen minutes, then a specialist who knows {name.lower()} walks it with you.", "submit": "Schedule my consultation", "note": "A person from the Indianapolis office replies, not an autoresponder."},
    ]
    orgs = ", ".join(CS_INDEX[c][1] for c in cases) if cases else "Customers across Indiana"
    first = re.split(r"(?<=[.!?])\s+", body)[0]
    faq = [[f"What does Van Ausdall & Farrar do for {name.lower()} organizations?", first + " " + " ".join(re.split(r"(?<=[.!?])\s+", body)[1:3])],
           [f"Which {name.lower()} customers work with Van Ausdall & Farrar?", f"{orgs} are on the record in our published case studies, with the numbers."],
           [f"What is included for {name.lower()}?", "; ".join(bullets) + ". All of it under one agreement with one Customer Care Center."],
           [f"Does Van Ausdall & Farrar serve {name.lower()} across Indiana?", f"Yes. Indianapolis, Fort Wayne, Evansville and every town between, with a service fleet that covers the entire state and {name.lower()} customers throughout the Midwest served from Indianapolis."],
           ["How does an engagement start?", "With the free Technology Strength Assessment: ten to fifteen minutes online, then a specialist who knows " + name.lower() + " walks the results with you and writes a roadmap of what to eliminate, optimize and leverage."]]
    secs.insert(len(secs) - 1, {"type": "faq", "alt": True, "heading": f"Questions {name.lower()} leaders ask us", "items": faq})
    secs.insert(2, {"type": "detail", "alt": True, "eyebrow": "The first ninety days", "heading": f"What changes first for {name.lower()}", "body": f"Every {name.lower()} engagement begins with the same three steps. First, the Technology Strength Assessment maps every device, contract, phone line and workflow you have today, so nothing is bought until it is understood. Second, the assessment produces a written roadmap sorted into eliminate, optimize and leverage, with the savings and the risks named. Third, the roadmap becomes one agreement: copiers, print, IT, phones and document services under one Customer Care Center, answered within 24 hours, with a 25-point inspection on every service call. {first}", "bullets": ["Week one: the assessment and a device-by-device inventory", "Weeks two to four: the roadmap, priced, with owners", "Month two: consolidation and installation, building by building", "Month three: the first quarterly review against the numbers"]})
    service_schema = {"@context": "https://schema.org", "@type": "Service", "name": f"Technology solutions for {name.lower()}", "serviceType": f"Office technology for {name.lower()}", "provider": {"@type": "Organization", "name": "Van Ausdall & Farrar, Inc.", "url": SITE}, "areaServed": {"@type": "State", "name": "Indiana"}, "audience": {"@type": "Audience", "audienceType": name}, "description": one}
    return {"crumbs": [["Home", "index.html"], ["Industries", "industries.html"], [name, f"industries/{slug}.html"]], "file": f"industries/{slug}.html", "title": f"Technology solutions for {name.lower()} | Van Ausdall & Farrar", "schema": [service_schema],
            "description": desc(f"{one} Managed IT, print, communications and process solutions for {name.lower()} across Indiana and the Midwest, from Van Ausdall & Farrar."), "sections": secs}


def case_study_page(slug, org, industry, one, mv, ml, chapters, next_slug):
    n = CS_INDEX[next_slug]
    art = {"@context": "https://schema.org", "@type": "Article", "headline": f"{org}: {one}", "description": one, "author": {"@type": "Organization", "name": "Van Ausdall & Farrar, Inc."}, "publisher": {"@type": "Organization", "name": "Van Ausdall & Farrar, Inc.", "url": SITE}, "about": {"@type": "Organization", "name": org}, "articleSection": industry}
    cs_faq = {"type": "faq", "alt": True, "heading": f"Questions about the {org} results", "items": [[f"What did {org} achieve with Van Ausdall & Farrar?", one], ["What was the measurable result?", f"{mv} {ml}, as published in the case study on vanausdall.com."], [f"Which services did {org} use?", chapters[0]["paras"][0][:360]], ["Can we get results like these?", "Every one of these engagements started with the free Technology Strength Assessment. A specialist maps your devices, contracts and workflows and shows where the savings are before you commit."]]}
    return {"file": f"case-studies/{slug}.html", "title": f"{org} case study | Van Ausdall & Farrar", "description": desc(one + " " + chapters[0]["paras"][0]), "schema": [art],
            "crumbs": [["Home", "index.html"], ["Case studies", "case-studies.html"], [org, f"case-studies/{slug}.html"]],
            "sections": [
                {"type": "article", "category": industry, "crumb_label": "Case studies", "crumb_href": "case-studies.html", "heading": org, "standfirst": one, "image": CS_IMAGE[slug], "image_alt": f"{org} case study", "date_label": "Case study", "read": "4 min read", "chapters": chapters,
                 "author": {"name": "Van Ausdall & Farrar", "role": "Published case study, vanausdall.com"}},
                {"type": "casestudy", "alt": True, "eyebrow": "The numbers", "heading": one, "quote": CS_QUOTES[slug], "attribution": f"{org} case study, vanausdall.com", "metrics": CS_METRICS[slug]},
                cs_faq,
                {"type": "leadform", "id": "consult", "heading": "Want results like these?", "body": "Every one of these engagements started with the Technology Strength Assessment. Yours can too.", "submit": "Schedule my consultation", "note": "A person from the Indianapolis office replies, not an autoresponder."},
                {"type": "related", "heading": "More case studies", "items": [[n[2], n[1], n[3], f"case-studies/{n[0]}.html", CS_IMAGE[n[0]]]]},
            ]}


CS_IMAGE = {"tippecanoe-school-corporation": "assets/team-1200.jpg", "star-financial": "assets/security-1200.jpg", "johnson-memorial-hospital": "assets/healthcare-process-1200.jpg", "city-of-anderson": "assets/hq-1200.jpg"}
CS_CHAPTERS = {
    "tippecanoe-school-corporation": [
        {"id": "the-company", "title": "The company", "paras": ["Tippecanoe School Corporation serves more than 13,000 students. A school system with that many students created infrastructure challenges across all of its locations. Tippecanoe was coordinating more than 10 different copy and print vendors, and costs were inconsistent and growing as a result. Managing all of those vendors had become increasingly problematic for the administrative IT staff, who were working with limited resources."]},
        {"id": "the-objective", "title": "The objective", "paras": ["Consolidate the number of vendors, centralize internal decision making, increase maintenance and support efficiency, and control costs. IT staff was spending 20% of their time servicing print issues. The fleet held over 600 single-function printers and over 200 copiers.", "ul:Consolidate vendors;;Centralize decisions;;Free IT time;;Control cost"]},
        {"id": "the-strategy", "title": "The strategy", "paras": ["Van Ausdall & Farrar completed a Technology Strength Assessment to find which areas of the current technology needed to be eliminated, optimized, or leveraged for a future program. After the review, Van Ausdall recommended copy and print management solutions and print application solutions that streamlined print and copy functions, provided mobile printing, integrated cloud printing, and eliminated over 900 outdated machines that were too costly to maintain and service.", "callout:The assessment is the method|Eliminate, optimize, leverage. The same three words on every VAF engagement."]},
        {"id": "the-results", "title": "The results", "paras": ["By cutting overall equipment from 1,200 machines to just over 300 new machines, the school corporation has seen $1,000,000 in savings over the life of the contract. Increased efficiency, better time management and a more centralized communication system made daily tasks more manageable. Because the project was so successful, Van Ausdall & Farrar is working on other projects the Tippecanoe team had not had time to address.", "pq:1,200 machines became just over 300."]},
    ],
    "star-financial": [
        {"id": "the-company", "title": "The company", "paras": ["STAR Financial Bank, based in Fort Wayne, Indiana, recognized its need for a new print partner. By analyzing lease schedules across locations around the state, the bank realized it needed to streamline vendor relationships to cut costs and simplify contracts."]},
        {"id": "the-objective", "title": "The objective", "paras": ["STAR's print vendor was slow to respond and not proactive. It was also apparent that STAR was being overcharged for expired leases and outdated equipment that no longer served its needs. STAR needed a partner to assess the current equipment, eliminate technology it did not need, optimize what it had, and negotiate new lease contracts for everything, in all locations across the state."]},
        {"id": "the-strategy", "title": "The strategy", "paras": ["Through the Technology Strength Assessment process, Van Ausdall & Farrar removed the expired leases and negotiated new contracts on upgraded equipment across the state. Van Ausdall also increased print security by implementing a new print platform, which cut down on the extraneous print waste STAR was incurring.", "callout:Expired leases|Still being paid for, still not serving the bank. The assessment found them; the contracts removed them."]},
        {"id": "the-results", "title": "The results", "paras": ["Once phase one of the print strategy was complete, STAR Financial Bank experienced a 70% cost savings over the original arrangement. Contracts became simple and effective, managed through one location and one vendor. STAR is working with Van Ausdall to add document management and a more robust print management solution.", "pq:70% savings, one vendor, one location for every contract."]},
    ],
    "johnson-memorial-hospital": [
        {"id": "the-company", "title": "The company", "paras": ["Johnson Memorial Health is a nationally recognized healthcare network based in Johnson County, Indiana. Its main campus in Franklin has been the county's only hospital since 1947. With the ever-changing demands of patient care and privacy laws, Johnson Memorial needed to respond to a patient record problem, and called Van Ausdall & Farrar."]},
        {"id": "the-objective", "title": "The objective", "paras": ["A big project, a short timeline and a tight budget. Patient paper records from 2009 to 2013 had to be digitized. The storage location was scheduled for demolition. The solution had to maintain patient confidentiality under HIPAA and adhere to the record retention policy, and the whole project had to finish in 90 days. The initial estimate was 100 banker-size boxes. After careful inventory, there were over 500."]},
        {"id": "the-strategy", "title": "The strategy", "paras": ["Document conversion specialists came on site to inventory and index every box. Records then went to Van Ausdall's corporate office for systematic scanning. Since the law allowed everything older than 2009 to be properly destroyed, Van Ausdall stayed inside the budget by keeping only the files required by law. Over 1.5 million files were scanned in 90 days. Once the project was finished and all files indexed, the paper files were safely destroyed and Van Ausdall issued a certificate of destruction.", "callout:Retention first|Scanning only what the policy required is how a project five times larger than estimated came in on budget."]},
        {"id": "the-results", "title": "The results", "paras": ["All files were inventoried, scanned and indexed within 90 days and inside the allotted budget. The clerks responsible for the records can pull files quickly and securely, increasing their efficiency in daily tasks. A cost-effective approach to records management and document conversion let Johnson Memorial meet a high-pressure deadline while staying under budget.", "pq:1.5 million files. 90 days. Under budget."]},
    ],
    "city-of-anderson": [
        {"id": "the-organization", "title": "The organization", "paras": ["The City of Anderson was founded in 1844 and has grown to over 56,000 residents. Agriculture and manufacturing have been mainstays in the community and a primary reason for its growth. Much of the city's technology had become too antiquated to meet constituents' needs, and the city needed a trusted partner to meet today's service levels and provide for growth."]},
        {"id": "the-objective", "title": "The objective", "paras": ["Van Ausdall & Farrar has been a preferred vendor for the City of Anderson since 2003. City employees engaged Van Ausdall to discuss the technology challenges constituents were raising: data security, billing presentation and timelines, purchasing, and community stewardship."]},
        {"id": "the-strategy", "title": "The strategy", "paras": ["The City co-authored a scope of work with Van Ausdall. A priority in Van Ausdall's Facilities Management program was a sustainable print strategy to meet print and mail security concerns. With on-site, full-time Van Ausdall personnel in place, the team implemented a print and billing technology refresh, postal optimization, 2D bar code document security, and groundwork for GIS in communications. Van Ausdall also streamlined purchasing and recovered significant costs, so the city funneled all departmental purchasing through its FM site manager.", "callout:On site, full time|Facilities Management means VAF people inside the customer's building, not a truck that visits."]},
        {"id": "the-results", "title": "The results", "paras": ["The on-site updated equipment, software and process improvements installed, implemented and maintained by Van Ausdall & Farrar have created over $40,000 in annual savings. Print and mail document security was strengthened, departmental purchases were streamlined through FM oversight with fewer vendors to manage, and Van Ausdall coordinated community involvement in charity initiatives benefiting a women's shelter and shop-with-a-cop programs.", "pq:Over $40,000 in annual savings, and fewer vendors for the city to manage."]},
    ],
}


def location_page(slug, city, a1, a2, phone, phone_href, region, lat, lon, hq):
    eyebrow = "Corporate headquarters" if hq else f"{city} office"
    has_addr = a1 != "Local office"
    hours = "Monday through Friday, 7:00am to 5:00pm." if hq else "Call the office for hours."
    schema = {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": f"{SITE}/locations/{slug}#office", "name": f"Van Ausdall & Farrar {city}",
              "parentOrganization": {"@id": f"{SITE}/#organization"}, "image": f"{PREVIEW}/assets/hq-1200.jpg",
              "telephone": phone.replace("(", "+1-").replace(") ", "-"), "url": f"{SITE}/locations/{slug}",
              "address": {"@type": "PostalAddress", "addressLocality": city, "addressRegion": "IN", "addressCountry": "US", **({"streetAddress": a1, "postalCode": a2.split()[-1]} if has_addr else {})},
              "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon}, "areaServed": region,
              "sameAs": ["https://www.linkedin.com/company/van-ausdall-&-farrar"]}
    if hq:
        schema["openingHoursSpecification"] = {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:00", "closes": "17:00"}
    local = {"indianapolis": "As Indiana's capital and largest office market, Indianapolis is home to VAF's corporate headquarters at 6430 E 75th Street, and to the state's largest team of copier, print, IT and communications specialists.",
             "fort-wayne": "Fort Wayne's manufacturing and defense employers run on dependable office technology, and VAF has kept northeast Indiana running since 1914. STAR Financial Bank, based in Fort Wayne, is on the record with 70% print savings.",
             "evansville": "Evansville is the commercial center of southwest Indiana, home to logistics, healthcare and manufacturing employers that depend on reliable office technology. VAF has served Evansville and the Tri-State area since 1914, with a local office for copier sales, service and repair."}[slug]
    return {"crumbs": [["Home", "index.html"], ["Locations", "locations.html"], [city, f"locations/{slug}.html"]], "file": f"locations/{slug}.html", "title": f"Office Technology, Copiers and Managed IT in {city}, IN | Van Ausdall & Farrar",
            "description": f"Van Ausdall & Farrar in {city}: copier sales, service and repair, managed print, managed IT and business phone systems for {region}. {phone}.",
            "schema": [schema, {"@context": "https://schema.org", "@type": "Service", "name": f"Office technology, copiers and managed IT in {city}", "serviceType": "Managed IT, copiers, managed print and business phone systems", "provider": {"@type": "Organization", "name": "Van Ausdall & Farrar, Inc.", "url": SITE}, "areaServed": {"@type": "City", "name": city}, "description": f"Copiers, managed print, managed IT and business phone systems for organizations in {city} and {region}."}],
            "sections": [
                {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": f"<em>{city}</em> copiers, managed IT and phone systems, serviced locally.",
                 "subhead": local, "primary": {"label": f"Call {phone}", "href": phone_href}, "secondary": {"label": "Schedule a consultation", "href": "contact.html"},
                 "image": "assets/gen-hq-1200.jpg" if hq else "assets/gen-technician-1200.jpg", "image_alt": "The headquarters building with a service van outside" if hq else "A VAF technician servicing a copier", "image_w": 1200, "image_h": 800,
                 "badge": {"value": "Local", "label": "Technicians dispatched from this office"}},
                {"type": "cards", "alt": True, "eyebrow": f"In {city}", "heading": f"What the {city} office does", "items": [
                    ["Copier sales, lease and rental", f"Canon, Ricoh, Kyocera and HP devices for {city} offices, installed and configured by the local team."],
                    ["Copier service and repair", "Certified field technicians, remote diagnostics, and a 25-point inspection on every visit."],
                    ["Managed print", "Fleet monitoring, automatic supplies and cost reduction up to 30%."],
                    ["Managed IT and security", "vCIO, 24/7 monitoring, SOC as a service and managed continuity."],
                    ["Business phone systems", "Mitel, RingCentral, 8x8 and Elevate, in the telecom business since 1983."],
                    ["Document management and conversion", "OnBase, Square 9 and the secure Document Conversion Center in Indianapolis."]]},
                {"type": "locations", "heading": f"Visit or call the {city} office", "intro": f"{hours} " + (f"{a1}, {a2}." if has_addr else f"{city}, Indiana. Street address on request."), "items": [[city, a1 if has_addr else "Serving " + region, a2, phone, phone_href]]},
                {"type": "testimonials", "alt": True, "heading": "What customers say after a service call", "items": [COMMENTS[2], COMMENTS[3]]},
                {"type": "faq", "heading": f"Questions we get in {city}", "items": [
                    [f"Do you serve businesses outside {city}?", f"Yes. The {city} office covers {region}, and our computer-dispatched, vendor-certified service fleet covers the entire state of Indiana."],
                    ["How fast can you get a technician to us?", "Same-day service for most metro-area calls, with remote diagnostics resolving many issues without a visit. The Customer Care Center responds within 24 hours."],
                    ["Can we lease a copier locally?", "Yes. Purchase, lease and rental are priced side by side after a free print assessment."]]},
                {"type": "leadform", "id": "consult", "heading": f"Start with a consultation in {city}", "body": "A specialist from the office replies to set a time.", "submit": "Schedule my consultation", "note": "A person replies, not an autoresponder."},
            ]}


def blog_post_page(p, others):
    related = [[o["category"], o["title"], teaser(o["standfirst"]), f"blog/{o['slug']}.html", o["image"]] for o in others[:3]]
    return {"file": f"blog/{p['slug']}.html", "title": f"{p['title']} | Van Ausdall & Farrar", "description": desc(p["standfirst"]),
            "schema": [{"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["standfirst"],
                        "image": f"{PREVIEW}/{p['image']}", "author": {"@type": "Organization", "name": CLIENT},
                        "publisher": {"@id": f"{SITE}/#organization"}, "mainEntityOfPage": f"{SITE}/blog/{p['slug']}",
                        "datePublished": "2026-09-08", "dateModified": "2026-09-08", "articleSection": p["category"]}],
            "sections": [
                {"type": "article", "category": p["category"], "heading": p["title"], "standfirst": p["standfirst"], "image": p["image"], "image_alt": p["image_alt"],
                 "date_label": "September 2026", "read": f"{max(4, sum(len(' '.join(c['paras'])) for c in p['chapters']) // 1100)} min read", "chapters": p["chapters"],
                 "author": {"name": "The VAF team", "role": "Indianapolis, Indiana"}},
                {"type": "faq", "alt": True, "heading": "Questions this guide gets asked", "items": p["faq"]},
                {"type": "leadform", "id": "guide", "heading": p["cta_label"], "body": "Tell us a little about your organization and a person from the Indianapolis office will call to set a time.", "submit": "Schedule my consultation", "note": "A person replies, not an autoresponder."},
                {"type": "related", "heading": "Keep reading", "items": related},
            ]}


def build():
    brand = {
        "accent": "#2A71AF", "ink_secondary": "#403D39", "short": SHORT, "type_from": {"showcase": "clean"}, "bg_alt": "#eef4fa", "navy": "#0f1e33",
        "logo": "assets/logo-600.png", "logo_alt": "Van Ausdall & Farrar, Business Technology Simplified", "logo_w": 600, "logo_h": 119,
        "logo_note": "Charcoal wordmark with a blue striped V: built for a light ground. Ask for a vector and a reversed variant for dark bands.",
        "phone": PHONE, "phone_href": PHONE_HREF, "email": SUCCESS_EMAIL,
        "utility": [{"label": "Client Service Center", "href": "support.html"}, {"label": "Request support", "href": "support.html#request"}, {"label": "Order supplies", "href": "support.html#supplies"}, {"label": "Careers", "href": "careers.html"}],
        "cta": {"label": "Schedule a consultation", "href": "contact.html"},
        "sticky": {"primary": "Take the assessment", "primary_href": "technology-strength-assessment.html", "secondary": "Call VAF", "secondary_href": PHONE_HREF},
        "launcher": {"label": "Already a customer?", "eyebrow": "Client Service Center", "title": "What do you need today?", "links": [["Request support", "support.html#request"], ["Order supplies", "support.html#supplies"], ["IT support", "support.html#it"], ["Training videos", "https://www.vanausdall.com/communication/customer-training-videos"]], "note": "The Customer Care Center processes requests Monday through Friday, 7:00am to 5:00pm, and responds within 24 hours."},
        "social": {"linkedin": "https://www.linkedin.com/company/van-ausdall-&-farrar", "facebook": "https://www.facebook.com/Vanausdallinc/", "instagram": "https://www.instagram.com/vanausdallinc/"},
        "tagline": "Business technology simplified. Indiana's largest full-service office technology provider, privately owned in Indianapolis since 1914.",
        "footer_columns": [
            {"title": "Solutions", "links": [[s[2], f"services/{s[0]}.html"] for s in SERVICES]},
            {"title": "Industries", "links": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES]},
            {"title": "Support", "links": [["Client Service Center", "support.html"], ["Request support", "support.html#request"], ["Order supplies", "support.html#supplies"], ["Technology Strength Assessment", "technology-strength-assessment.html"], ["Free print assessment", "print-assessment.html"], ["Cost calculator", "cost-calculator.html"]]},
            {"title": "Company", "links": [["About VAF", "about.html"], ["Case studies", "case-studies.html"], ["Partners", "partners.html"], ["Locations", "locations.html"], ["Careers", "careers.html"], ["News and insights", "blog.html"], ["Contact", "contact.html"]]},
        ],
        "legal": [["Privacy", f"{SITE}/policies/privacy"], ["Terms of service", f"{SITE}/policies/terms-of-service"], ["Cookie policy", f"{SITE}/policies/cookie"]],
    }
    schema = {"org_name": "Van Ausdall & Farrar, Inc.", "org_url": SITE,
              "org_logo": f"{SITE}/images/logo.png",
              "org_description": "Indiana's largest full-service office technology provider, privately owned in Indianapolis since 1914: managed IT and cybersecurity, business phone systems, copiers and managed print, document management and conversion, and AI consulting.",
              "sameAs": ["https://www.linkedin.com/company/van-ausdall-&-farrar", "https://www.facebook.com/Vanausdallinc/", "https://www.instagram.com/vanausdallinc/", "https://goo.gl/maps/ekbY63gHTu56ifBd8"],
              "telephone": "+1-317-634-2913", "foundingDate": "1914", "slogan": "Business technology simplified", "areaServed": {"@type": "State", "name": "Indiana"},
              "hq": {"name": "Van Ausdall & Farrar Indianapolis", "streetAddress": "6430 E 75th Street", "addressLocality": "Indianapolis", "addressRegion": "IN", "postalCode": "46250", "lat": 39.887, "lon": -86.062, "hours": ["07:00", "17:00"]}}
    schema["sameAs"].append("https://www.youtube.com/@vanausdallfarrar6346")
    nav = [
        {"label": "Solutions", "href": "solutions.html", "mega": True,
         "groups": [{"title": p[0], "items": [[s[2], f"services/{s[0]}.html"] for s in SERVICES if s[3] == p[0]]} for p in PILLARS],
         "featured": {"eyebrow": "Not sure where to start?", "title": "Know your Technology Strength Score", "body": "Ten to fifteen minutes. Information, print, process and communication, scored, with a roadmap of what to eliminate, optimize and leverage.", "href": "technology-strength-assessment.html", "label": "Take the assessment"}},
        {"label": "Industries", "href": "industries.html", "children": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES]},
        {"label": "Case studies", "href": "case-studies.html"},
        {"label": "Resources", "href": "blog.html", "children": [["News and insights", "blog.html"], ["Technology Strength Assessment", "technology-strength-assessment.html"], ["Free print assessment", "print-assessment.html"], ["Print cost calculator", "cost-calculator.html"], ["2026 CIO AI Playbook", "cio-ai-playbook.html"]]},
        {"label": "About", "href": "about.html", "children": [["About VAF", "about.html"], ["Partners", "partners.html"], ["Locations", "locations.html"], ["Careers", "careers.html"], ["Contact", "contact.html"]]},
        {"label": "Support", "href": "support.html"},
    ]

    pages = []
    # ---------------- home
    pages.append({"file": "index.html", "title": "Van Ausdall & Farrar | Managed IT, copiers, phone systems and office technology in Indianapolis",
                  "compose": {
                      "clean": ["hero-light", "partners", "pillars", "seal", "customers", "story", "office", "fleet", "numbers", "ba", "flow", "model", "proof", "casestudy", "is-this-you", "markets", "map", "voices", "film", "faq", "contact"],
                      "showcase": ["hero", "partners", "pillars", "customers", "fleet", "numbers", "ba", "flow", "office", "model", "seal", "story", "proof", "casestudy", "markets", "map", "voices", "film", "faq", "contact"],
                      "press": ["hero-light", "story", "pillars", "customers", "seal", "office", "fleet", "numbers", "ba", "flow", "model", "proof", "casestudy", "voices", "film", "markets", "map", "faq", "contact"]},
                  "description": "Indiana's largest full-service office technology provider since 1914. Managed IT and cybersecurity, business phone systems, copiers and managed print, document management and AI consulting for Indianapolis and the Midwest.",
                  "sections": [
        {"type": "hero", "id": "hero-light", "layout": "split", "eyebrow": "Business technology simplified, since 1914",
         "stats": [["1914", "Serving Indiana since"], ["93.4", "Net Promoter Score, audited"], ["SOC 2", "Certified service organization"], ["4,000+", "Phone systems deployed since 1983"]],
         "ribbon": ["SOC 2 certified", "NPS 93.4, audited by CEO Juice. World Class since 2019", "Mitel Gold, seven consecutive years"],
         "variants": {"press": {"stats": None, "ribbon": ["Indianapolis, Indiana. Since 1914.", "SOC 2 certified", "NPS 93.4, audited by CEO Juice"]}},
         "heading": "Everything your business runs on, <em>under one roof</em>.",
         "subhead": "IT support, copiers and print, phone systems, document workflow and AI guidance for Indiana businesses. One local partner, one assessment to start, one number to call.",
         "primary": {"label": "Take the Technology Strength Assessment", "href": "technology-strength-assessment.html"}, "secondary": {"label": "Schedule a consultation", "href": "contact.html"},
         "note": "Canon, Ricoh, Kyocera, HP, Mitel, Fortinet, Sophos and Microsoft partner", "image": "assets/gen-technician-1200.jpg", "image_alt": "A VAF technician replacing a toner unit in a bright office while the office manager looks on", "image_w": 1200, "image_h": 800,
         "badge": {"value": "93.4", "label": "Net Promoter Score, independently audited"}},
        HERO_LAYERED,
        {"type": "wheel", "id": "wheel", "eyebrow": "Four pillars", "heading": "Information, communication, print and process, from one partner", "intro": "Hover a segment. Four pillars, one agreement, one Customer Care Center.", "items": WHEEL_ITEMS, "hub": SHORT, "hub_sub": "one roof", "ring": "BUSINESS TECHNOLOGY SIMPLIFIED"},
        FLOW_ENGAGEMENT, SEAL, BEFORE_AFTER, HOTSPOTS, FLEET, MODEL3D, PROOF, FILM, PILLARS_CARDS, CUSTOMER_WALL, NUMBERS, CS_QUOTE, TABS_MARKETS, MAP, TIMELINE,
        {"type": "partners", "id": "partners", "caption": "Technology partners, including Gartner Magic Quadrant leaders", "items": PARTNERS},
        {"type": "checklist", "id": "is-this-you", "alt": True, "eyebrow": "Is this you?", "heading": "Six questions from the Technology Strength Assessment",
         "intro": "Check the ones you cannot answer yes to. They are six of the eighty.",
         "items": ["Is your server data backed up nightly with more than one copy off-site or in the cloud?", "Do you have a procedure to test that your backups actually restore?", "Do you know how much you spend annually on printer supplies and service?", "Do you have a written disaster recovery plan for your phone system?", "Does your company have a formal records retention schedule?", "Do you have a written AI acceptable use policy?"],
         "messages": ["Check what you cannot answer yes to.", "One is normal.", "Two is a pattern.", "Three or more is the reason the assessment exists. Ten to fifteen minutes gives you the full score."],
         "cta_label": "Take the assessment", "cta_href": "technology-strength-assessment.html"},
        {"type": "services", "id": "services", "heading": "Everything an office runs on, from one partner",
         "intro": "Most providers sell one of these. VAF has sold and serviced all of them in Indiana for a very long time, and answers the phone for all of them at one number.",
         "items": [[s[1], brief(s[7]), f"services/{s[0]}.html"] for s in SERVICES]},
        {"type": "testimonials", "id": "voices", "alt": True, "layout": "feature", "eyebrow": "Real customer comments", "heading": "Imported directly from our after-service surveys", "items": COMMENTS[:5]},
        {"type": "faq", "id": "faq", "alt": True, "heading": "Questions we get on the first call", "items": [
            ["Do you only work with large companies?", "No. From a single multifunction printer for a startup to a fleet of production copiers across multiple locations, and from a ten-person office on managed IT to a school corporation with 13,000 students."],
            ["Can you take over equipment or systems from another vendor?", "Usually. The Technology Strength Assessment covers everything you run regardless of where it came from, and the roadmap says honestly what to eliminate, what to optimize and what to leverage."],
            ["How fast do you respond?", "The Customer Care Center processes requests Monday through Friday, 7:00am to 5:00pm, and responds within 24 hours. Same-day service for most Indianapolis metro copier calls. Managed IT is monitored 24/7."],
            ["Do you serve outside Indianapolis?", "Yes. Offices in Indianapolis, Fort Wayne and Evansville, and a computer-dispatched, vendor-certified service fleet that covers the entire state of Indiana and customers throughout the Midwest."]]},
        {"type": "contact", "id": "contact", "heading": "Speak with a solutions expert", "body": "Tell us what you run and what is not working. A person from the Indianapolis office replies to set a time. Or start with the ten-minute assessment.",
         "options": ["Managed IT and security", "Business phone systems", "Copiers and managed print", "Document management or conversion", "AI consulting", "Something else"], "submit": "Schedule my consultation", "note": f"Or call {PHONE}, Monday through Friday, 7:00am to 5:00pm."},
    ]})
    # ---------------- solutions overview + service pages
    pages.append({"file": "solutions.html", "title": "Solutions | Van Ausdall & Farrar", "description": "Four pillars, twelve solutions, one partner: managed IT, cybersecurity, cloud, backup and recovery, business phone systems, copiers, managed print, copier service, production print, document management, document conversion and AI consulting.",
                  "crumbs": [["Home", "index.html"], ["Solutions", "solutions.html"]],
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Solutions", "heading": "Four pillars. Twelve solutions. <em>One roof.</em>", "subhead": "Every line below is designed, installed, serviced and supported by VAF's own people in Indiana. Most customers start with one pillar and add from there.", "primary": {"label": "Take the assessment", "href": "technology-strength-assessment.html"}},
        dict(PILLARS_CARDS, alt=True),
        HOTSPOTS,
    ] + [
        {"type": "services", "id": p[0].lower(), "alt": bool(i % 2), "heading": p[0], "intro": p[1], "items": [[s[1], brief(s[7]), f"services/{s[0]}.html"] for s in SERVICES if s[3] == p[0]]} for i, p in enumerate(PILLARS)
    ] + [
        {"type": "testimonials", "heading": "What customers say", "items": [COMMENTS[0], COMMENTS[1]]},
        {"type": "leadform", "alt": True, "id": "consult", "heading": "Not sure where to start? Start with the score.", "body": "Ten to fifteen minutes online, then a specialist walks it with you.", "submit": "Take the assessment", "note": "A person from the Indianapolis office replies, not an autoresponder."},
    ]})
    for s in SERVICES:
        pages.append(service_page(*s))
    # ---------------- industries
    pages.append({"file": "industries.html", "title": "Industries | Van Ausdall & Farrar", "description": "Technology solutions built around how education, engineering and construction, financial services, healthcare, insurance, manufacturing and logistics, real estate and state and local government run in Indiana.",
                  "crumbs": [["Home", "index.html"], ["Industries", "industries.html"]],
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Industries", "heading": "Built around <em>how your industry runs</em>.", "subhead": "Eight markets where VAF has done the work many times, with the case studies to show for it. If yours is not here, the assessment still starts the same way.", "primary": {"label": "Schedule a consultation", "href": "contact.html"}},
        TABS_MARKETS,
        {"type": "resources", "alt": True, "heading": "Eight industries", "intro": "Each page covers what we set up, who is on the record, and how to start.", "items": [["Industry", i[1], i[3], f"Technology for {i[1].lower()}", f"industries/{i[0]}.html"] for i in INDUSTRIES]},
        {"type": "leadform", "id": "consult", "heading": "Start with the Technology Strength Assessment", "body": "Ten to fifteen minutes, then a specialist who knows your industry walks it with you.", "submit": "Schedule my consultation", "note": "A person from the Indianapolis office replies, not an autoresponder."},
    ]})
    for i in INDUSTRIES:
        pages.append(industry_page(*i))
    # ---------------- case studies
    pages.append({"file": "case-studies.html", "title": "Case studies | Van Ausdall & Farrar", "description": "Eighteen published case studies: a school corporation that saved $1M, a bank that cut print costs 70%, a hospital that scanned 1.5 million files in 90 days, a city saving $40,000 a year, and more.",
                  "crumbs": [["Home", "index.html"], ["Case studies", "case-studies.html"]],
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Case studies", "heading": "Cost savings and outcomes, <em>on the record</em>.", "subhead": "Eighteen Indiana organizations, by industry. Four are written up in full here; the rest are one line each until the PDFs are migrated."},
        {"type": "stats", "tone": "dark", "items": [["$1M", "Saved by Tippecanoe School Corporation"], ["70%", "Print cost savings at STAR Financial Bank"], ["1.5M", "Patient files scanned in 90 days for Johnson Memorial"], ["$40,000", "Annual savings for the City of Anderson"]]},
        {"type": "related", "heading": "Written up in full", "items": [[c[2], c[1], c[3], f"case-studies/{c[0]}.html", CS_IMAGE[c[0]]] for c in CASE_STUDIES if c[6]]},
        {"type": "resources", "alt": True, "heading": "Every case study by industry", "intro": "Each is published on vanausdall.com with a PDF today; the PDFs migrate into pages in the build.", "items": [[c[2], c[1], c[3], "Read the case study" if c[6] else "PDF on vanausdall.com", f"case-studies/{c[0]}.html" if c[6] else f"{SITE}/case-studies/{c[0]}"] for c in CASE_STUDIES]},
        {"type": "faq", "heading": "Questions about the results", "items": [["How much did Tippecanoe School Corporation save with Van Ausdall & Farrar?", "$1,000,000 over the life of the contract, by consolidating 1,200 printers and copiers to just over 300 and replacing more than 10 vendors with one."], ["How much did STAR Financial Bank save on print?", "70% over the original arrangement after phase one, once expired leases were removed and contracts renegotiated statewide."], ["How fast can Van Ausdall & Farrar scan patient records?", "1.5 million files in 90 days for Johnson Memorial Health, inside budget, with a certificate of destruction for the paper."]]},
        {"type": "leadform", "id": "consult", "heading": "Want results like these?", "body": "Every one of these engagements started with the Technology Strength Assessment.", "submit": "Schedule my consultation", "note": "A person from the Indianapolis office replies, not an autoresponder."},
    ]})
    full_cs = [c for c in CASE_STUDIES if c[6]]
    for i, c in enumerate(full_cs):
        pages.append(case_study_page(c[0], c[1], c[2], c[3], c[4], c[5], CS_CHAPTERS[c[0]], full_cs[(i + 1) % len(full_cs)][0]))
    # ---------------- tools: TSA, print assessment, calculator, playbook
    pages.append({"file": "technology-strength-assessment.html", "title": "Technology Strength Assessment | Know your score | Van Ausdall & Farrar", "description": "Do you know your Technology Strength Score? Ten to fifteen minutes across information, print, process and communication, then a roadmap of what to eliminate, optimize and leverage. Complimentary.",
                  "crumbs": [["Home", "index.html"], ["Technology Strength Assessment", "technology-strength-assessment.html"]],
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Technology Strength Assessment", "heading": "Do you know your <em>Technology Strength Score</em>?", "subhead": "Knowing your score shows how technology can improve your business and where to focus. The assessment covers information, print, process and communication in ten to fifteen minutes, and it is complimentary.", "primary": {"label": "Start the assessment", "href": "#assess"}, "secondary": {"label": "Schedule a consultation instead", "href": "contact.html"}, "image": "assets/meeting-1200.jpg", "image_alt": "Business people reviewing a technology scorecard at a table", "image_w": 1200, "image_h": 800},
        {"type": "process", "alt": True, "eyebrow": "Four assessments, two parts each", "heading": "What the assessment covers", "stages": [["Information", "Vulnerability scans, MFA, backup, patching, firewall reviews, disaster recovery, end-of-life systems, onboarding and offboarding, multi-cloud policy."], ["Print", "Print strategy, networked devices, annual spend, security concerns, authentication, unclaimed jobs, backup devices, management reporting."], ["Process", "Records retention, centralized repository, paper-based processes, AP and HR automation, visitor and package tracking, print submission tools."], ["Communication", "PoE, internet redundancy, phone system disaster recovery, remote users, cloud PBX, smartphone integration, call recording, contact center, Teams, Wi-Fi."]]},
        FLOW_ENGAGEMENT,
        {"type": "checklist", "id": "assess", "eyebrow": "A sample", "heading": "Ten of the eighty questions", "intro": "Check the ones you can answer yes to. The full assessment scores all four areas.",
         "items": ["We execute periodic vulnerability scans", "MFA is enabled for administrator and user accounts", "Server data is backed up nightly with a copy off-site or in the cloud", "We test that backups restore", "We have a written disaster recovery plan revised once or twice a year", "We know how much we spend annually on printer supplies and service", "Our MFPs authenticate users before releasing print", "We have a formal records retention schedule we execute", "Our smartphones are connected to the corporate phone system", "We have a disaster recovery plan for the phone system"],
         "messages": ["Check what is true today.", "A start.", "Most organizations land here.", "Strong. The full assessment finds what is left."],
         "cta_label": "Take the full assessment", "cta_href": "contact.html"},
        {"type": "cards", "alt": True, "eyebrow": "What you receive", "heading": "The scorecard, in three parts", "items": [["Eliminate", "The technology you pay for and do not need."], ["Optimize", "What you already own that could do more."], ["Leverage", "The improvements that grow the business, sequenced and priced."]]},
        {"type": "faq", "heading": "Questions about the assessment", "items": [["What does it cost?", "Nothing. The assessment is complimentary."], ["How long does it take?", "Ten to fifteen minutes online. You can save for later and finish another day. A specialist then walks the results with you."], ["Who sees my answers?", "Your VAF technology advisor, whose average tenure with the company is fifteen years."]]},
        {"type": "leadform", "alt": True, "id": "consult", "heading": "Request the full assessment", "body": "A technology advisor from the Indianapolis office replies to set it up.", "submit": "Request my assessment", "note": "A person replies, not an autoresponder."},
    ]})
    pages.append({"file": "print-assessment.html", "title": "Free print assessment | Van Ausdall & Farrar", "schema": [{"@context": "https://schema.org", "@type": "Service", "name": "Free print assessment", "serviceType": "Print fleet assessment", "provider": {"@type": "Organization", "name": "Van Ausdall & Farrar, Inc.", "url": SITE}, "areaServed": {"@type": "State", "name": "Indiana"}, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": "A complimentary device-by-device assessment of print volumes, costs and staff time, with a written recommendation."}], "description": "Uncover hidden costs, identify inefficiencies and optimize your printing. A free print assessment from Van Ausdall & Farrar: comprehensive analysis, cost reduction strategies, tailored recommendations. No obligation.",
                  "crumbs": [["Home", "index.html"], ["Free print assessment", "print-assessment.html"]],
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Free print assessment", "heading": "Ready to optimize your <em>print environment</em>?", "subhead": "Uncover hidden costs, identify inefficiencies and optimize your printing processes. Every print engagement starts here, so you see exact pricing for your office before you commit.", "primary": {"label": "Request the assessment", "href": "#request"}, "secondary": {"label": "Estimate first", "href": "cost-calculator.html"}, "image": "assets/copier-1200.jpg", "image_alt": "An office copier", "image_w": 1200, "image_h": 800},
        {"type": "cards", "alt": True, "eyebrow": "What is included", "heading": "Four things, in writing", "items": [["Comprehensive analysis", "Your current print environment evaluated: hardware, usage patterns and expenses."], ["Cost reduction strategies", "Where to lower printing costs through optimized configurations and resource allocation."], ["Efficiency improvements", "Ways to streamline print workflows and reduce waste."], ["Tailored recommendations", "Personalized to your business needs, with purchase, lease and rental priced side by side."]]},
        {"type": "process", "eyebrow": "How it works", "heading": "Three steps", "stages": [["Free print assessment", "We map your devices, volumes and costs, then show exactly where you save."], ["We implement", "Right-sized copiers and printers, software, security and supplies, handled for you."], ["We monitor 24/7", "Proactive monitoring, predictive maintenance and fast local repair keep you running."]]},
        {"type": "casestudy", "alt": True, "eyebrow": "In action", "heading": CS_INDEX["tippecanoe-school-corporation"][3], "quote": CS_QUOTES["tippecanoe-school-corporation"], "attribution": "Tippecanoe School Corporation case study, vanausdall.com", "metrics": CS_METRICS["tippecanoe-school-corporation"]},
        {"type": "leadform", "id": "request", "heading": "Request your free print assessment", "body": "Let us help you unlock the full potential of your printing infrastructure.", "submit": "Request my assessment", "note": f"Or call {PHONE} or toll-free {TOLLFREE}, Monday through Friday, 7:00am to 5:00pm."},
    ]})
    pages.append({"file": "cost-calculator.html", "title": "Print cost calculator | Van Ausdall & Farrar", "description": "Estimate what your office spends on printing today: devices, mono and color pages, staff time. Typical Indiana rates; the free print assessment replaces them with your real numbers.",
                  "crumbs": [["Home", "index.html"], ["Print cost calculator", "cost-calculator.html"]],
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Cost calculator", "heading": "What does your office <em>really</em> spend on print?", "subhead": "Move three sliders. The estimate uses typical rates for toner, service and the staff time nobody counts. The free print assessment replaces every number here with yours."},
        {"type": "calculator", "id": "calc", "alt": True, "eyebrow": "Estimate", "heading": "Your print spend, estimated", "intro": "Devices, mono pages and color pages a month. That is all it needs.",
         "rates": {"mono_cpp": 0.018, "color_cpp": 0.09, "minutes_per_device_week": 25, "hourly": 28, "managed_saving": 0.30, "saving_label": "Potential saving at up to 30% (the figure on VAF's copy print page)"},
         "note": "Estimates only, using typical industry rates for orientation. Nothing here is a quote. The free print assessment gives you the real figure from your devices and your invoices.",
         "cta_label": "Get the real number: request the free print assessment", "cta_href": "print-assessment.html"},
        {"type": "comparison", "heading": "Lease, rent or buy?", "intro": "The assessment prices all three for your real volume. Here is how they usually compare.",
         "columns": [{"label": "Lease", "recommended": True}, {"label": "Rent"}, {"label": "Buy"}],
         "rows": [["Best for", "Steady volume, a fleet kept current", "Peaks, projects, construction trailers", "Stable volume, long device life"], ["Term", "Fixed, with an upgrade at the end", "Month to month", "None"], ["Up-front cost", "Low", "Low", "Highest"], ["Lifetime cost", "Moderate", "Highest per month", "Lowest if the device runs for years"], ["Service and toner", "Can be included in one rate", "Usually included", "Add a service agreement"]],
         "note": "Terms and rates are set after the assessment."},
        {"type": "faq", "alt": True, "heading": "About the estimate", "items": [["Where do the rates come from?", "Typical industry per-page rates for toner and service, and a modest allowance for the staff time spent ordering supplies and chasing repairs. Orientation only."], ["Why does staff time count?", "Because it is real money that never appears on a print invoice. Tippecanoe's IT staff were spending 20% of their time on print issues."], ["How do I get the real number?", "Request the free print assessment. We map every device, volume and cost and show exactly where you save."]]},
        {"type": "leadform", "id": "request", "heading": "Get the real number", "body": "A specialist maps your devices, volumes and costs. No obligation.", "submit": "Request my assessment", "note": "A person from the Indianapolis office replies, not an autoresponder."},
    ]})
    pages.append({"file": "cio-ai-playbook.html", "title": "2026 CIO AI Playbook | Van Ausdall & Farrar", "description": "Is your business ready for AI in 2026? Get the 2026 CIO AI Playbook, a step-by-step guide to secure, strategic AI implementation, from Van Ausdall & Farrar.",
                  "crumbs": [["Home", "index.html"], ["2026 CIO AI Playbook", "cio-ai-playbook.html"]],
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Free download", "heading": "Is your business ready for <em>AI in 2026</em>?", "subhead": "The 2026 CIO AI Playbook is a step-by-step guide to secure, strategic AI implementation: policy, guardrails, the use cases that pay, and the order to do them in.", "primary": {"label": "Download the playbook", "href": "#download"}, "secondary": {"label": "AI consulting", "href": "services/ai-consulting.html"}, "image": "assets/ai-hand-1200.jpg", "image_alt": "A hand holding illuminated letters spelling AI", "image_w": 1200, "image_h": 800},
        {"type": "cards", "alt": True, "eyebrow": "Inside", "heading": "What the playbook covers", "items": [["The risk of doing nothing", "The four scenarios that expose data or create liability in ordinary offices."], ["The acceptable use framework", "Approved tools, data boundaries, human review and incident reporting."], ["Readiness before use cases", "Why the policy comes first, and how to find the automation that actually pays."], ["A roadmap", "Guidance, governance and risk management, with owners and dates."]]},
        {"type": "leadform", "id": "download", "heading": "Download your free playbook", "body": "Tell us where to send it. A technology advisor follows up once, to offer the Technology Strength Assessment.", "submit": "Send me the playbook", "note": "No spam. One follow-up from a person in Indianapolis."},
        {"type": "faq", "alt": True, "heading": "Questions", "items": [["Is it really free?", "Yes."], ["Who is it for?", "CIOs, IT directors, owners and operations leaders at small and mid-sized businesses and non-profits."], ["What comes after the playbook?", "AI readiness: a policy and guardrails, then the use cases that deliver. VAF's AI consulting starts with the free Technology Strength Assessment."]]},
    ]})
    # ---------------- about, partners, careers
    pages.append({"file": "about.html", "title": "About Van Ausdall & Farrar | Indiana's office technology provider since 1914", "description": "From a Thomas Edison Company distributorship in 1914 to Indiana's largest full-service business technology provider. Privately owned in Indianapolis, an audited NPS of 93.4, SOC 2 certified, Mitel Gold seven years running.",
                  "crumbs": [["Home", "index.html"], ["About", "about.html"]],
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "About VAF", "heading": "Helping customers succeed <em>since 1914</em>.", "subhead": "In 1914, Van Ausdall & Farrar was chosen as a distributor for the Thomas Edison Company. Today it is one of the largest privately owned office solutions companies in Indiana, with a 57,000-square-foot headquarters in Indianapolis and a long-standing tradition of partnering with the most respected manufacturers in the industry.", "primary": {"label": "Why VAF", "href": "#why"}, "secondary": {"label": "Careers", "href": "careers.html"}, "image": "assets/gen-hq-1200.jpg", "image_alt": "A modern two-story headquarters building with a service van outside", "image_w": 1200, "image_h": 800},
        {"type": "stats", "tone": "dark", "items": [["1914", "Chosen as a Thomas Edison Company distributor"], ["93.4", "Net Promoter Score, audited by CEO Juice"], ["SOC 2", "Certified service organization"], ["57,000", "Square feet of headquarters, built 2006"]]},
        TIMELINE,
        VALUES,
        {"type": "detail", "id": "why", "eyebrow": "Why VAF", "heading": "Experience you will profit from", "body": "More than a century in business, through two world wars, two pandemics and a few bad Colts teams. We know how to evolve and adapt to disruptive technology when we recognize it. We only support the industry-recognized leaders in each area we serve, including Gartner Magic Quadrant leaders like Fortinet, Sophos, 8x8 and RingCentral, and we fully support every product we recommend with our own local team.",
         "bullets": ["Vsecure IT staff with over 250 years of combined IT experience and CISSP personnel on staff", "In the telecom business since 1983 with over 4,000 systems deployed and a dedicated engineering staff", "Mitel Gold for seven consecutive years, the top 7% of 1,400 partners in North America", "Fortinet Engaged Advanced Partner with NSE-7 certified engineers and the first SD-WAN Specialization in the Great Lakes region", "Average tenure of IT and UC sales staff of 15 years, with over 150 years of industry experience"],
         "image": "assets/engineers-1200.jpg", "image_alt": "Two engineers at work in a data center", "flip": True},
        {"type": "proof", "id": "nps", "alt": True, "eyebrow": "Measured, not claimed", "value": "93.4", "text": "Net Promoter Score, collected and audited by CEO Juice from VAF customers after every service call. World Class, above 70, every year since 2019. Costco scores 79. The average US company scores 10.", "source": "CEO Juice is an independent company with an audited process; the numbers cannot be changed even if a customer scored us low in error."},
        {"type": "leadership", "id": "leadership", "heading": "Leadership", "intro": "Eric von Grimmenstein grew up in the business. After graduating from Purdue University he began as a sales representative in 1977 and became president in 1994.", "people": [["Eric von Grimmenstein", "President"], ["Steven Sigmon", "Director of IT"]], "orgs_intro": "VAF's mission includes a positive impact on the community: paid volunteer hours for employees, and charity initiatives coordinated with customers like the City of Anderson.", "orgs": ["Women's shelter fundraising", "Shop with a cop programs", "Paid volunteer hours", "Sourcewell cooperative purchasing for public and non-profit customers"]},
        {"type": "video", "id": "film", "eyebrow": "Life at VAF", "heading": "What it is like to work here", "intro": "Filmed with VAF people in Indianapolis.", "youtube": "i-q4U5SnvaM", "poster": "assets/careers-1200.jpg", "title": "What it's like to work at Van Ausdall & Farrar", "caption": "VAF's own film, from the careers page"},
        {"type": "testimonials", "alt": True, "heading": "Real customer comments", "items": COMMENTS[4:8]},
        {"type": "faq", "heading": "Questions people ask about Van Ausdall & Farrar", "items": [["Who owns Van Ausdall & Farrar?", "Van Ausdall & Farrar, Inc. is privately owned and operated in Indianapolis. Eric von Grimmenstein, who joined in 1977, has been president since 1994."], ["How long has Van Ausdall & Farrar been in business?", "Since 1914, when Oscar K. Van Ausdall was chosen as an Edison Business Phonograph dealer for Indiana. The company has been in the telecom business since 1983."], ["Where is Van Ausdall & Farrar located?", "Headquarters at 6430 E 75th Street, Indianapolis, IN 46250, with offices in Fort Wayne and Evansville and a service fleet covering the entire state."], ["What does Van Ausdall & Farrar do?", "Managed IT and cybersecurity, business phone systems, copiers and managed print, document management and conversion, and AI consulting, for businesses, schools, hospitals and municipalities across Indiana and the Midwest."]]},
        {"type": "cta", "heading": "Work here", "subhead": "Privately owned and operated in Indianapolis, and looking for people who take ownership, keep learning and have some fun while they are at it.", "primary": {"label": "See careers", "href": "careers.html"}},
    ]})
    pages.append({"file": "partners.html", "title": "Partners | Van Ausdall & Farrar", "description": "Fortinet, Mitel, Canon, HP, OnBase and more. Van Ausdall & Farrar's solution partners are among the best in the business, including Gartner Magic Quadrant leaders, so your technology stack is too.",
                  "crumbs": [["Home", "index.html"], ["Partners", "partners.html"]],
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Partners", "heading": "World-class partnerships, <em>by pillar</em>.", "subhead": "We only support the industry-recognized leaders in each area of technology we serve, and we re-evaluate the partnerships regularly. By representing the very best, it is uncommon that we have to apologize for a deficiency in our partners or our technology."},
        {"type": "partners", "caption": "Technology partners", "items": PARTNERS},
        {"type": "cards", "alt": True, "eyebrow": "Information", "heading": "Information partners", "items": [["Fortinet", "Engaged Advanced Partner, NSE-7 engineers, first SD-WAN Specialization in the Great Lakes region."], ["Sophos", "Intercept X Advanced with XDR on every Vsecure base plan."], ["Microsoft", "Licensing, administration, collaboration and backup."], ["Datto", "Patching, monitoring, backup and continuity."], ["KnowBe4", "Security awareness training and compliance management."], ["Arctic Wolf, Tenable, VMware, Juniper, N-able", "Detection and response, vulnerability management, virtualization, networking and RMM."]]},
        {"type": "cards", "eyebrow": "Communication", "heading": "Communication partners", "items": [["Mitel", "MiExclusive Gold Partner seven consecutive years; MiVoice Connect, MiCloud Connect and Enterprise Contact Center Gold Certified."], ["RingCentral", "Customer Delivery Partner Certified."], ["8x8", "Sales Engineer Certified; a Gartner Magic Quadrant leader."], ["Elevate", "AI cloud communications with 99.999% uptime reliability."]]},
        {"type": "cards", "alt": True, "eyebrow": "Print", "heading": "Print partners", "items": [["Canon", "imageRUNNER ADVANCE copiers and multifunction printers."], ["Ricoh", "Black-and-white and color MFPs with document management built in."], ["Kyocera", "Low total cost of ownership and enterprise print security."], ["HP", "LaserJet and PageWide multifunction printers."], ["Brother and Zebra", "Desktop and label printing."], ["EFI Fiery and Skyline", "Production color management and web-to-print."]]},
        {"type": "cards", "eyebrow": "Process", "heading": "Process partners", "items": [["OnBase by Hyland", "Enterprise content management and Unity Forms."], ["Square 9", "Smart Search document management."], ["Kofax", "Intelligent capture and exchange for automated forms processing."], ["OPEX, Fujitsu and Canon", "Production scanners for the Document Conversion Center."]]},
        {"type": "faq", "alt": True, "heading": "Questions about our partners", "items": [["Which copier brands does Van Ausdall & Farrar sell and service?", "Canon, Ricoh, Kyocera and HP copiers and multifunction printers, plus Brother and Zebra printers, and most other major office equipment brands for service."], ["Which phone systems does Van Ausdall & Farrar install?", "Mitel (MiExclusive Gold Partner), RingCentral, 8x8 and Elevate cloud communications, with Fortinet networking and a vendor-neutral carrier evaluation."], ["Which security vendors does Van Ausdall & Farrar use?", "Fortinet firewalls and Fabric, Sophos Intercept X with XDR, Datto patching and monitoring, KnowBe4 awareness training, and Arctic Wolf and Tenable for detection and vulnerability management."]]},
        {"type": "leadform", "alt": True, "id": "consult", "heading": "Speak with a solutions expert", "body": "Tell us what you run today. A technology advisor replies to set a time.", "submit": "Schedule my consultation", "note": "A person from the Indianapolis office replies, not an autoresponder."},
    ]})
    pages.append({"file": "careers.html", "title": "Careers | Van Ausdall & Farrar, Indianapolis", "description": "Build your career with a company that has been finding better ways forward since 1914. Privately owned in Indianapolis. Accountability, customer experience, together. Competitive benefits, generous PTO, paid volunteer hours.",
                  "crumbs": [["Home", "index.html"], ["Careers", "careers.html"]],
                  "sections": [
        {"type": "hero", "layout": "split", "eyebrow": "Find your place at VAF", "heading": "Your next bright idea? <em>Working here.</em>", "subhead": "We have been part of the Indianapolis business community since 1914, back when our story began as a distributor for the Thomas Edison Company. A lot has changed. One thing has not: great people are what keep us going.", "primary": {"label": "View open positions", "href": CAREERS_URL}, "secondary": {"label": "Explore benefits", "href": "#benefits"}, "image": "assets/careers-1200.jpg", "image_alt": "VAF team members at work", "image_w": 1200, "image_h": 800},
        {"type": "video", "id": "film", "alt": True, "eyebrow": "See what life at VAF looks like", "heading": "What it is like to work at Van Ausdall & Farrar", "youtube": "i-q4U5SnvaM", "poster": "assets/careers-1200.jpg", "title": "What it's like to work at Van Ausdall & Farrar", "caption": "VAF's own film"},
        {"type": "values", "eyebrow": "Who shines at VAF", "heading": "A, C, T", "items": [["Accountability. Do it right.", "Own your work. Follow through. Do what you say you are going to do."], ["Customer experience. Do it better.", "Stay curious. Look for opportunities to improve. Do not settle for that is how we have always done it."], ["Together. Do it together.", "Help your teammates. Share the wins. Step in when someone needs you. And yes, have some fun while you are at it."]]},
        {"type": "cards", "alt": True, "id": "benefits", "eyebrow": "A few bright spots", "heading": "What comes with the job", "items": [["Competitive benefits", "Medical, dental, vision, 401(k) match and more."], ["Time to recharge", "Generous PTO, paid holidays and a personal holiday."], ["Grow with us", "Opportunities to learn, advance and grow your career."], ["Give back", "Paid volunteer hours and opportunities to support our community."], ["Hard work gets noticed", "Recognition programs, employee celebrations and incentives."], ["We're local", "Privately owned and operated right here in Indianapolis."]]},
        {"type": "cta", "heading": "Think you would shine here?", "subhead": "Bring your ideas, your drive and your willingness to learn. We will bring the opportunities, the support and a team that wants to see you succeed. Van Ausdall & Farrar is an Equal Opportunity Employer.", "primary": {"label": "Explore careers at VAF", "href": CAREERS_URL}},
    ]})
    # ---------------- support, locations, contact
    pages.append({"file": "support.html", "title": "Client Service Center | Support, supplies and repair | Van Ausdall & Farrar", "description": "Request copier service, repair or supplies in Indiana. The Customer Care Center processes requests Monday through Friday, 7:00am to 5:00pm, and responds within 24 hours. Call (317) 634-2913.",
                  "crumbs": [["Home", "index.html"], ["Client Service Center", "support.html"]],
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Client Service Center", "heading": "Already a customer? <em>This is the fast lane.</em>", "subhead": "Have a problem or concern? Our Customer Care Center serves our entire customer base, processes requests Monday through Friday, 7:00am to 5:00pm, and responds within 24 hours.", "primary": {"label": "Request support", "href": "#request"}, "secondary": {"label": f"Call {PHONE}", "href": PHONE_HREF}},
        {"type": "band", "eyebrow": "Fast lane", "heading": "Four things, under a minute each", "subhead": "Or call. A person answers.", "items": [["Request support", "Copier, printer, phone or dictation", "#request"], ["Order supplies", "Toner and parts for your devices", "#supplies"], ["IT support", "Managed IT and Vsecure customers", "#it"], ["Training videos", "Phone system how-to videos", "https://www.vanausdall.com/communication/customer-training-videos"]]},
        {"type": "detail", "id": "request", "eyebrow": "Support", "heading": "Request support", "body": "Tell us the equipment and what it is doing. Certified technicians service Canon, Ricoh, Kyocera and HP across Indianapolis and the state, and remote diagnostics resolve many issues without a visit.", "bullets": ["Same-day service for most Indianapolis metro calls", "25 points of inspection on every visit", f"Email {SUPPORT_EMAIL} or call {PHONE}, toll-free {TOLLFREE}, fax (317) 638-1843"], "form": {"fields": ["Company", "Type of equipment (phone, dictation, hardware or software, copier, printer, fax)", "What is it doing?"], "submit": "Request support"}},
        {"type": "detail", "id": "supplies", "alt": True, "eyebrow": "Supplies", "heading": "Order supplies", "body": "Toner and parts for the devices we support, shipped from Indianapolis. Under a managed print agreement, supplies replenish automatically before you run out.", "bullets": [f"Email {SUPPLIES_EMAIL}", "Automatic replenishment on managed fleets", "One invoice with your service agreement"], "form": {"fields": ["Company", "Device model or serial", "Item and quantity"], "submit": "Order supplies"}},
        {"type": "detail", "id": "it", "eyebrow": "IT support", "heading": "IT support", "body": "For managed IT and Vsecure customers. Monitored 24/7; the help desk handles the day to day and dispatches on-site technicians when needed.", "bullets": [f"Email {IT_EMAIL}", "Managed clients come first, ahead of break-fix work", "Security incidents go to the security operations center"], "form": {"fields": ["Company", "User and device", "What is happening?"], "submit": "Open a ticket"}},
        {"type": "locations", "alt": True, "heading": "Or call the office", "intro": f"Toll-free {TOLLFREE} reaches the Customer Care Center.", "items": [[l[1], l[2] if l[2] != "Local office" else "Serving " + l[6], l[3], l[4], l[5]] for l in LOCATIONS]},
        {"type": "testimonials", "heading": "What customers say after a service call", "items": [COMMENTS[1], COMMENTS[6]]},
        {"type": "faq", "alt": True, "heading": "Service questions", "items": [["What response time can we expect?", "The Customer Care Center responds within 24 hours of receipt, with same-day service for most metro-area copier calls. Ask for the terms of your agreement in writing."], ["Do you service equipment you did not sell?", "Yes, most major office equipment brands. If you bought your equipment from another dealer, we can still help."], ["Should I repair or replace?", "Our technicians assess honestly. If the repair cost approaches the value of the machine, we will say so and offer new, leased or pre-owned options."]]},
    ]})
    pages.append({"file": "locations.html", "title": "Locations | Van Ausdall & Farrar", "description": "Headquartered in Indianapolis with offices in Fort Wayne and Evansville, and a service fleet covering the entire state of Indiana: Carmel, Fishers, Noblesville, Greenwood, Bloomington, Columbus, Muncie, South Bend and more.",
                  "crumbs": [["Home", "index.html"], ["Locations", "locations.html"]],
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Locations", "heading": "Three offices. <em>The whole state.</em>", "subhead": "Headquartered in Indianapolis with offices in Fort Wayne and Evansville. A computer-dispatched, vendor-certified service fleet covers the Indianapolis metro and the entire state of Indiana.", "primary": {"label": f"Call {PHONE}", "href": PHONE_HREF}},
        MAP,
        {"type": "locations", "detailed": True, "heading": "Where we are", "intro": "Each office has its own page.", "items": [[l[1], l[2] if l[2] != "Local office" else "Serving " + l[6], l[3], l[4], l[5]] for l in LOCATIONS]},
        {"type": "cards", "alt": True, "eyebrow": "Service areas", "heading": "Cities we serve every week", "items": [[c, "Copier sales, service and repair, managed print, managed IT and business phone systems."] for c in SERVICE_AREAS[:9]]},
        {"type": "faq", "heading": "Coverage questions", "items": [["Do you cover my town?", "Indianapolis, Carmel, Fishers, Noblesville, Greenwood, Bloomington, Columbus, Muncie, Fort Wayne, South Bend, Evansville and the towns between. The service fleet covers the entire state, and customers throughout the Midwest are served from Indianapolis."], ["Can I see a device before I decide?", "Ask your technology advisor. Bring a sample of what you print and we will run it on the device you are considering."]]},
        {"type": "leadform", "alt": True, "id": "consult", "heading": "Speak with a solutions expert", "body": "A technology advisor from the nearest office replies to set a time.", "submit": "Schedule my consultation", "note": "A person replies, not an autoresponder."},
    ]})
    for l in LOCATIONS:
        pages.append(location_page(*l))
    # ---------------- blog listing + posts
    pages.append({"file": "blog.html", "title": "News and insights | Van Ausdall & Farrar", "description": "Plain-spoken guides on managed IT, cybersecurity, business phone systems, document conversion, copiers and AI governance, from the Van Ausdall & Farrar team in Indianapolis.",
                  "crumbs": [["Home", "index.html"], ["News and insights", "blog.html"]],
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "News and insights", "heading": "What we tell customers <em>before they ask</em>", "subhead": "Twelve guides from the people who install and service the systems. No jargon, no vendor pitch. Six are placeholders adapted from our category guides until VAF's own posts migrate."},
        {"type": "related", "heading": "The guides", "intro": "Start with the phone system guide or the AI policy.", "items": [[p["category"], p["title"], teaser(p["standfirst"]), f"blog/{p['slug']}.html", p["image"]] for p in BLOG]},
        {"type": "leadform", "alt": True, "id": "consult", "heading": "Start with the Technology Strength Assessment", "body": "Ten to fifteen minutes. Complimentary. A specialist walks the results with you.", "submit": "Request my assessment", "note": "A person from the Indianapolis office replies."},
    ]})
    for i, p in enumerate(BLOG):
        pages.append(blog_post_page(p, BLOG[i + 1:] + BLOG[:i]))
    # ---------------- contact
    pages.append({"file": "contact.html", "title": "Contact Van Ausdall & Farrar | Indianapolis, Fort Wayne, Evansville", "description": "Speak with a solutions expert. Indianapolis headquarters at 6430 E 75th Street, (317) 634-2913. Offices in Fort Wayne and Evansville. Or start with the Technology Strength Assessment.",
                  "crumbs": [["Home", "index.html"], ["Contact", "contact.html"]],
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Connect with us", "heading": "Speak with a solutions expert, or <em>just call</em>.", "subhead": "Our innovation experts improve your business efficiency by eliminating technology you do not need, optimizing what you have, and creating a technology improvement roadmap that grows with you. It all starts with the Technology Strength Assessment."},
        {"type": "contact", "id": "form", "heading": "Let's talk", "body": "Tell us a little about your organization and a person from the Indianapolis office will call to set a time.", "options": ["Managed IT and security", "Business phone systems", "Copiers and managed print", "Document management or conversion", "AI consulting", "Something else"], "submit": "Schedule my consultation", "note": f"Or call {PHONE}, Monday through Friday, 7:00am to 5:00pm. Existing customers: the Client Service Center is faster."},
        {"type": "locations", "alt": True, "heading": "Our offices", "intro": f"Toll-free {TOLLFREE}. Client success: {SUCCESS_EMAIL}.", "items": [[l[1], l[2] if l[2] != "Local office" else "Serving " + l[6], l[3], l[4], l[5]] for l in LOCATIONS]},
    ]})

    # ---------------- page for page: every vanausdall.com URL gets a counterpart, then every page is normalised
    import sys as _sys
    _sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
    from migrate_pages import fix_title, fix_desc, build_migrated, link_sections
    _extract = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vanausdall.pages.json"), encoding="utf-8"))
    COVERED = {"/": "index.html", "/about/": "about.html", "/about/why": "about.html", "/about/history": "about.html", "/about/customer-comments": "about.html", "/net-promoter-score": "about.html",
               "/contact/": "contact.html", "/contact/careers": "careers.html", "/get-started": "contact.html", "/customer-care": "support.html", "/support/": "support.html", "/vaf-auto-support": "support.html",
               "/partners": "partners.html", "/best-in-class-partners": "partners.html", "/solutions": "solutions.html", "/blog": "blog.html", "/industries/": "industries.html", "/case-studies/": "case-studies.html",
               "/technology-strength-assessment": "technology-strength-assessment.html", "/assessment/": "technology-strength-assessment.html", "/print/free-print-assessment": "print-assessment.html",
               "/information/managed-it-services": "services/managed-it.html", "/information/cloud-solutions": "services/cloud.html", "/information/data-security": "services/cybersecurity.html", "/business-continuity-compliance": "services/business-continuity.html",
               "/communication/business-phone-systems": "services/business-phone-systems.html", "/copiers/": "services/copiers.html", "/copier-service-repair": "services/copier-service.html", "/print/managed-print-services": "services/managed-print.html", "/managed-print": "services/managed-print.html",
               "/production-print": "services/production-print.html", "/document-management": "services/document-management.html", "/document-conversion/": "services/document-conversion.html", "/ai": "services/ai-consulting.html",
               "/industries/education-technology-solutions": "industries/education.html", "/industries/engineering-construction-technology-solutions": "industries/engineering-construction.html", "/industries/financial-technology-services": "industries/financial-services.html", "/industries/government-technology-solutions": "industries/government.html", "/industries/healthcare-technology-solutions": "industries/healthcare.html", "/industries/insurance-technology-solutions": "industries/insurance.html", "/industries/manufacturing-logistics-technology-solutions": "industries/manufacturing-logistics.html", "/industries/real-estate-technology-solutions": "industries/real-estate.html",
               "/indianapolis/": "locations/indianapolis.html", "/fort-wayne/": "locations/fort-wayne.html", "/evansville/": "locations/evansville.html",
               "/case-studies/tippecanoe-school-corporation": "case-studies/tippecanoe-school-corporation.html", "/case-studies/star-financial": "case-studies/star-financial.html", "/case-studies/johnson-memorial-hospital": "case-studies/johnson-memorial-hospital.html", "/case-studies/city-of-anderson": "case-studies/city-of-anderson.html"}
    RETIRE = {"/covid-19-information", "/vaf-coronavirus-covid-19-policy", "/kiosk-assembly", "/kiosk-demo", "/kiosk-quote", "/tw-telecom", "/survey"}
    IMAGES = {"Information": "assets/gen-soc-1200.jpg", "Communication": "assets/gen-phone-1200.jpg", "Print": "assets/copier-1200.jpg", "Process": "assets/gen-conversion-1200.jpg", "city": "assets/gen-hq-1200.jpg", "case study": "assets/team-1200.jpg", "default": "assets/gen-hq-1200.jpg"}
    BLURBS = {p[0]: p[1] + " Every VAF service is delivered under one agreement with one Customer Care Center, so the copier technician, the network engineer and the phone specialist answer to the same account team." for p in PILLARS}
    BLURBS["default"] = "Van Ausdall & Farrar has served Indiana since 1914 with four pillars under one roof: information, communication, print and process. One agreement, one Customer Care Center, one account team for every device and every service."
    migrated, REDIRECTS = build_migrated(_extract, {p["file"] for p in pages}, COVERED, RETIRE, IMAGES, PHONE, BLURBS,
                                         {"Solutions": "solutions.html", "Locations": "locations.html", "Case studies": "case-studies.html", "About": "about.html", "Policies": "about.html", "Industries": "industries.html"})
    pages += migrated
    def _insert(pg, sec):
        last = pg["sections"][-1]["type"] if pg["sections"] else ""
        if last in ("leadform", "contact", "locations", "related", "cta"):
            pg["sections"].insert(len(pg["sections"]) - 1, sec)
        else:
            pg["sections"].append(sec)
    for f, sec in link_sections(migrated).items():
        pg = next((p for p in pages if p["file"] == f), None)
        if pg:
            _insert(pg, sec)
    TSA = "Most engagements start with the free Technology Strength Assessment: ten to fifteen minutes online, then a specialist walks the results with you and writes a roadmap of what to eliminate, optimize and leverage."
    FAQ_EXTRA = {
        "blog.html": {"type": "faq", "alt": True, "heading": "Questions about News and insights", "items": [["How often does Van Ausdall & Farrar publish?", "About once a week, and it has for three years. Each guide is aimed at a question customers ask on the first call, from what managed print costs to whether to lease or buy a copier."], ["Who writes the guides?", "The VAF team in Indianapolis: technology advisors, service managers and the security team, with the author named on each post."], ["Can we ask for a topic?", f"Yes. Email {SUCCESS_EMAIL} or call {PHONE}. If three customers ask the same question, it becomes a guide."]]},
        "careers.html": {"type": "faq", "alt": True, "heading": "Questions about working at Van Ausdall & Farrar", "items": [["Where are the jobs?", "Indianapolis headquarters at 6430 E 75th Street, the Fort Wayne and Evansville offices, and field service roles across Indiana."], ["What are the benefits?", "Medical, dental and vision, a 401(k) with match, generous paid time off and paid volunteer hours, in a privately owned company where the average technology advisor has been here fifteen years."], ["How do I apply?", f"Send a resume to {SUCCESS_EMAIL} or apply through the listing. A person replies, not an autoresponder."]]},
        "contact.html": {"type": "faq", "alt": True, "heading": "Questions before you call", "items": [["What are your hours?", f"Monday through Friday, 7:00am to 5:00pm at {PHONE}. Existing customers reach the Client Service Center the same way, or through the Customer Care app."], ["Where are the offices?", "Headquarters at 6430 E 75th Street, Indianapolis, IN 46250, with offices in Fort Wayne and Evansville. The service fleet covers the entire state."], ["How fast do you respond?", "Requests are processed and answered within 24 hours. Most metro-area copier calls are same day."], ["I am not sure what I need. Where do I start?", TSA]]},
        "industries.html": {"type": "faq", "alt": True, "heading": "Questions about industry solutions", "items": [["Which industries does Van Ausdall & Farrar serve?", "Education, engineering and construction, financial services, healthcare, insurance, manufacturing and logistics, real estate, and state and local government, across Indiana and the Midwest."], ["Why does the industry matter for office technology?", "Because a hospital's records retention, a school's print volume and a job site's phones each fail in their own way. The industry pages describe what VAF sets up for each and who is on the record."], ["Do you have references in my industry?", "Eighteen published case studies, from Tippecanoe School Corporation to STAR Financial Bank and Johnson Memorial Health. Each industry page lists its own."]]},
        "solutions.html": {"type": "faq", "alt": True, "heading": "Questions about our solutions", "items": [["What does Van Ausdall & Farrar actually sell?", "Four pillars under one agreement: information (managed IT, cybersecurity, cloud, backup), communication (business phone systems and unified communications), print (copiers, managed print, production print) and process (document management, conversion and AI consulting)."], ["Can we buy one service, or is it all or nothing?", "Either. Most customers start with one pillar, usually copiers or managed IT, and add the others as contracts expire, because one invoice and one Customer Care Center is easier."], ["How do we know what we need?", TSA]]},
        "print-assessment.html": {"type": "faq", "alt": True, "heading": "Questions about the print assessment", "items": [["What does the print assessment cost?", "Nothing. It is complimentary and there is no obligation."], ["What does it include?", "A device-by-device map of your fleet, volumes and costs per page, supply spend, service history and staff time, with a written recommendation of what to consolidate, replace or manage."], ["How long does it take?", "Two to three weeks, most of it monitoring software collecting real volumes. A specialist then walks the findings with you in one meeting."], ["What happens after?", "You keep the report. If you want VAF to act on it, managed print starts with a fleet plan and supplies shipped on usage."]]},
    }
    EXTRA_SECTIONS = {
        "contact.html": {"type": "detail", "alt": True, "eyebrow": "What happens next", "heading": "Send the form, and here is what happens", "body": "A person from the Indianapolis office reads it the same business day and calls to set a time; there is no autoresponder and no sales sequence. If the question is about an existing device or agreement, it is routed to the Client Service Center, which answers within 24 hours and dispatches a certified technician locally. If it is a new need, a technology advisor, whose average tenure with the company is fifteen years, walks the Technology Strength Assessment with you: ten to fifteen minutes on your devices, contracts, phones and workflows, then a written roadmap of what to eliminate, optimize and leverage. You keep the roadmap either way.", "bullets": ["Same-day reply from a named person in Indianapolis", "Service requests answered within 24 hours", "Assessment first, quote second", "Offices in Indianapolis, Fort Wayne and Evansville; the fleet covers the state"]},
        "cio-ai-playbook.html": {"type": "detail", "alt": True, "eyebrow": "What is inside", "heading": "Nine chapters, written for the person who has to decide", "body": "The playbook walks a CIO or owner from the first question, is our data ready, to the last, how do we measure it. It covers an AI acceptable use policy, the governance guardrails that keep employees productive without exposing customer data, the use cases that pay back first in a mid-sized company, how to evaluate vendors and models, what the security team needs before anything is switched on, and a ninety-day plan with owners and checkpoints. Each chapter ends with a one-page checklist you can take into a leadership meeting.", "bullets": ["Readiness: data, identity and the questions to ask before any pilot", "Policy: an acceptable use policy template and the guardrails that make it real", "Use cases: the six that pay back first in a fifty to five-hundred person company", "Security: what the SOC and the vCIO need before launch", "The ninety-day plan, with owners and checkpoints", "Measurement: the four numbers to report to the board"]},
    }
    TITLES = {
        "index.html": "Van Ausdall & Farrar | Indianapolis Office Technology", "about.html": "About Van Ausdall & Farrar, Indianapolis", "contact.html": "Contact Van Ausdall & Farrar, Indianapolis", "careers.html": "Careers at Van Ausdall & Farrar, Indianapolis",
        "solutions.html": "Technology Solutions Indianapolis | Van Ausdall & Farrar", "industries.html": "Industries We Serve in Indiana | Van Ausdall & Farrar", "locations.html": "Locations Across Indiana | Van Ausdall & Farrar", "partners.html": "Technology Partners, Indianapolis | Van Ausdall & Farrar",
        "support.html": "Client Service Center, Indianapolis | Van Ausdall & Farrar", "technology-strength-assessment.html": "Tech Strength Assessment, Indiana | Van Ausdall & Farrar", "print-assessment.html": "Free Print Assessment, Indianapolis | Van Ausdall & Farrar", "cost-calculator.html": "Print Cost Calculator, Indianapolis | Van Ausdall & Farrar",
        "cio-ai-playbook.html": "2026 CIO AI Playbook, Indiana | Van Ausdall & Farrar", "blog.html": "News and Insights, Indianapolis | Van Ausdall & Farrar", "case-studies.html": "Case Studies Across Indiana | Van Ausdall & Farrar",
        "services/managed-it.html": "Managed IT Services Indianapolis | Van Ausdall & Farrar", "services/business-phone-systems.html": "Business Phone Systems Indianapolis | Van Ausdall & Farrar", "services/copiers.html": "Copier Sales and Lease, Indianapolis | Van Ausdall & Farrar", "services/managed-print.html": "Managed Print Services Indianapolis | Van Ausdall & Farrar",
        "services/copier-service.html": "Copier Repair Service, Indianapolis | Van Ausdall & Farrar", "services/document-conversion.html": "Document Conversion, Indianapolis | Van Ausdall & Farrar", "services/cybersecurity.html": "Managed Cybersecurity, Indianapolis | Van Ausdall & Farrar", "services/cloud.html": "Cloud Services in Indianapolis | Van Ausdall & Farrar",
        "services/ai-consulting.html": "AI Consulting for Indiana Businesses | Van Ausdall & Farrar", "services/business-continuity.html": "Backup and Recovery, Indianapolis | Van Ausdall & Farrar", "services/document-management.html": "Document Management, Indianapolis | Van Ausdall & Farrar", "services/production-print.html": "Production Print, Indianapolis | Van Ausdall & Farrar",
        "industries/education.html": "Education Technology, Indiana | Van Ausdall & Farrar", "industries/engineering-construction.html": "Construction Technology, Indiana | Van Ausdall & Farrar", "industries/financial-services.html": "Financial Services IT, Indiana | Van Ausdall & Farrar", "industries/government.html": "Government Technology, Indiana | Van Ausdall & Farrar",
        "industries/healthcare.html": "Healthcare Technology, Indiana | Van Ausdall & Farrar", "industries/insurance.html": "Insurance Technology, Indiana | Van Ausdall & Farrar", "industries/manufacturing-logistics.html": "Manufacturing Technology, Indiana | Van Ausdall & Farrar", "industries/real-estate.html": "Real Estate Technology, Indiana | Van Ausdall & Farrar",
        "locations/indianapolis.html": "Copiers and Managed IT, Indianapolis | Van Ausdall & Farrar", "locations/fort-wayne.html": "Copiers and Managed IT, Fort Wayne IN | Van Ausdall & Farrar", "locations/evansville.html": "Copiers and Managed IT, Evansville IN | Van Ausdall & Farrar",
        "blog/ai-acceptable-use-policy.html": "AI Acceptable Use Policy, Indiana Guide | Van Ausdall & Farrar", "blog/all-in-one-office-printer-options-navigating-the-market-for-the-best-choice.html": "All-in-One Office Printers, Indianapolis | Van Ausdall & Farrar", "blog/business-phone-systems-buyers-guide.html": "Business Phone Systems Guide, Indiana | Van Ausdall & Farrar",
        "blog/copier-lease-vs-buy-indianapolis.html": "Copier Lease vs Buy in Indianapolis | Van Ausdall & Farrar", "blog/document-conversion-services-what-to-expect.html": "Document Conversion Services, Indiana | Van Ausdall & Farrar", "blog/how-managed-print-services-transforms-business.html": "First 90 Days of Managed Print, Indiana | Van Ausdall & Farrar",
        "blog/physical-intrusion-detection-systems.html": "Physical Intrusion Detection, Indiana | Van Ausdall & Farrar", "blog/same-day-service-what-it-means.html": "Same-Day Copier Service in Indianapolis | Van Ausdall & Farrar", "blog/what-is-a-vcio.html": "What a vCIO Does, Indianapolis Guide | Van Ausdall & Farrar",
        "blog/what-managed-print-costs.html": "Managed Print Services Cost in Indiana | Van Ausdall & Farrar", "blog/wide-format-printer-buying-guide-making-the-right-decision.html": "Wide-Format Printers, Indianapolis Guide | Van Ausdall & Farrar", "blog/workstation-management-an-overview.html": "Workstation Management, Indianapolis | Van Ausdall & Farrar",
    }
    for pg in pages:
        if pg["file"] in FAQ_EXTRA and not any(s.get("type") == "faq" for s in pg["sections"]):
            _insert(pg, FAQ_EXTRA[pg["file"]])
        if pg["file"] in EXTRA_SECTIONS:
            pg["sections"].insert(1, EXTRA_SECTIONS[pg["file"]])
        pg["title"] = TITLES.get(pg["file"]) or fix_title(pg["title"])
        pg["description"] = fix_desc(pg.get("description", ""))
    MIGRATION = {"pages": len(migrated), "redirects": len(REDIRECTS), "retired": sorted(RETIRE), "map": REDIRECTS}
    brand["legal"] = [["Privacy", "policies/privacy.html"], ["Terms of service", "policies/terms-of-service.html"], ["Cookie policy", "policies/cookie.html"]]

    pitch = {
        "qbs_contact": {"name": "Shawn Peterson", "email": "shawn@thequantumleap.business", "phone": "(712) 389-4639"},
        "prepared_for": "Brian Courtney and the Van Ausdall & Farrar team",
        "heard_intro": "From Brian's call with Patrick on 1 September, and from vanausdall.com, the CEO Juice report it links to, and Semrush. Tell us if any of it is wrong; it outranks our house defaults.",
        "heard": [
            "Your focus has moved to the website, SEO and generative AI search. You are being outpaced by competitors in search, and the president has noticed the company not appearing. (Brian, 1 September)",
            "You want marketing qualified leads tracked through the website, and the solutions page reworked so it ranks in AI search and LLM answers. (Brian, 1 September)",
            "A paid LinkedIn campaign spiked traffic and converted nobody, so the budget stays targeted rather than bigger. Predictability and return on the spend matter more than reach. (Brian, 1 September)",
            "The current site was rebuilt in 2021 by a month-to-month partner at about $1,200 a month, with reporting but little advice, and one blog post a month. (Brian, 1 September)",
            "You asked for a good, better, best proposal. Our three packages are Launch, Growth and Transform; this preview is built to the Growth page count, and the plan below fits a fourth-quarter start. (Brian, 1 September)",
            "Brian deals with the marketing company and decides on the website; others weigh in eventually. (Brian, 1 September)",
            "Business Technology Simplified is the line under the logo, and Everything under one roof since 1914 is the hero. Both are on every direction. We are not recommending one; you choose.",
            "Your four pillars, Information, Communication, Print and Process, organize the partners page and the city pages. They are the navigation now.",
            "The Technology Strength Assessment is your signature process. It is the primary call to action on every page, ahead of Schedule a consultation.",
            "Your customers come to the site for the Client Service Center: support, supplies and IT support. Those stay one click from the top of every page.",
            "The blue in the logo is the accent everywhere, measured off the live site. The wordmark is charcoal on white, so the header stays light in all three directions.",
            "Eighteen case studies with real numbers exist. Four are written in full; all eighteen are listed and linked.",
            "Real customer comments from your after-service surveys, and the CEO Juice NPS of 93.4, are the social proof, exactly as you present them today."],
        "found": [
            "Four in five organic visits are people searching your name. The home page earns 85% of the site's traffic. The site is a phone book for people who already know you.",
            "The pages earning strangers today are the Fort Wayne and Evansville managed IT pages and a blog post on physical intrusion detection. Indianapolis, the headquarters market, has 28 ranking keywords, none above 140 searches a month.",
            "Business phone systems, 9,900 searches a month, ranks 25 through the Fort Wayne page. That is the single largest term within reach, and the new phone systems page and guide are aimed at it.",
            "Your forms work but land nowhere: the form script uses a hidden honeypot field and there is no CRM integration, so a lead from 1,081 monthly visits is an email, not a record. Every form here becomes a HubSpot form that creates a contact.",
            "Four Indiana competitors (Taylored, The AME Group, Braden, Leap Managed IT) each earn 1.5 to 2 times your traffic from 3 to 7 times your keyword footprint. Leap is number 1 for managed it services indianapolis (1,000 searches a month) and it support indianapolis (880). You are not in the top 100 for either.",
            "Your authority is competitive: Authority Score 21 and 486 referring domains against Leap at 24 and 471. The gap is missing pages, not missing links. Every page here is built for a term you can win.",
            "Leap's new copier brand, leapcopierprinter.com, already sits at 9 for copier lease indianapolis, one place above your copy print page at 10.",
            "324 blog posts, 55% of your sitemap, live on query-string URLs (blog?p=...) that cannot carry their own titles, images or schema cleanly. Every post gets a real URL now, and every earning URL gets a redirect.",
            "Nine directories of city pages (Indianapolis, Carmel, Fishers, Noblesville, Greenwood, Bloomington, Columbus, Muncie, South Bend) share near-identical copy. Three real offices get real pages with LocalBusiness markup; the rest become a service area list.",
            "Your own photography is limited to stock-style imagery on the live site, so the preview uses generated stand-ins that show the scenes we would shoot: a technician with a customer, the conversion center, the headquarters, the operations room. A half-day shoot replaces them and makes the site un-copyable."],
        "choose_heading": "Three directions. Your call.",
        "choose_intro": "The words, the pages and the proof are identical in all three. What differs is the register: how plain, how modern, how established the company reads. Open each one on your phone, click through the pages your customers use, and tell us which one feels like Van Ausdall & Farrar.",
        "choose_reasons": [
            ["If Business Technology Simplified is the promise", "Clean is the plainest-spoken: a humanist sans, generous white space, one action per section. Credible to a CIO and to an office manager alike."],
            ["If technology partner is the story", "Showcase: a display grotesque, bigger rhythm, the rotating device in the hero, the fleet rail and the floor plan front and center. The modern managed technology partner."],
            ["If 1914 is the story", "Press: an editorial serif on warm paper, the narrowest measure, the most institutional. Edison, four generations of leadership and an audited service score land harder in a serif. Nobody in your category looks like this."],
            ["Whichever you choose", "Every page, every case study, the Technology Strength Assessment, the SEO plan and the redirects come with it. Mix is allowed: a Showcase hero on a Clean site is a normal request."]],
        "alternatives": [
            ["Quantum Clean", "The clear one. Light, humanist sans, maximum clarity. Says simplified without saying it."],
            ["Quantum Showcase", "The technology-partner one. Same light ground, a display grotesque and bigger rhythm, with the 3D device, the fleet and the floor plan."],
            ["Quantum Press", "The established one. Editorial serif on warm paper. 1914, Edison, four generations, an audited score."]],
        "plan": [
            ["Week 1", "Choose a direction. Confirm the items under To confirm. Send the logo as a vector."],
            ["Weeks 2 to 3", "Copy for every page, from your practice leaders and from you, in your words. Photography scheduled at the headquarters and in the field."],
            ["Weeks 3 to 5", "Build in HubSpot: theme cloned and re-skinned, blog templates assigned, every page built, forms wired to named people, the assessment as a multi-step form that scores."],
            ["Week 6", "Quality gate on every page, on a real phone. Redirects tested individually. You edit a page yourself in the walkthrough."],
            ["Launch, then 90 days", "Go live. Reads at 30, 60 and 90 days against the baseline below, with what we would change next."]],
        "search": {
            "heading": "Where you stand in search today, and what changes",
            "intro": "Measured before we touched anything, so the work can be judged against it. Numbers from Semrush and from vanausdall.com on 8 September 2026.",
            "as_of": "Semrush US database and live HTML, 8 September 2026",
            "report_href": "seo-report.html", "report_label": "Read the full SEO and AI search analysis",
            "findings": SEO_FINDINGS[:5],
            "site_audit": SITE_AUDIT,
            "today_stats": [["1,081", "Organic visits a month; competitors earn 1,555 to 2,094"], ["80%", "Of them from people searching your name"], ["0", "Top-100 rankings for managed it services indianapolis (1,000 a month)"], ["21", "Authority Score, against Leap at 24 and Taylored at 27"]],
            "today": [
                "Four visits in five come from branded searches: van ausdall & farrar, van ausdall and farrar, van ausdall. The home page earns 85% of the site's traffic.",
                "The best non-brand page is the Fort Wayne managed IT page: 49 keywords, position 6 for managed it services fort wayne. Evansville managed IT ranks 2 for managed it evansville. Indianapolis, the headquarters market, has no top-100 ranking for managed it services indianapolis (1,000 a month), it support indianapolis (880) or it services indianapolis (880). Leap Managed IT is number 1 for all three.",
                "Four Indiana competitors each earn 1.5 to 2 times your traffic: Taylored 2,094 visits from 2,711 keywords, The AME Group 2,007, Braden 1,807, Leap 1,555. Your authority (21, 486 referring domains) is in the same band as theirs, so the gap is pages, not links.",
                "Managed print services (4,400 searches a month, difficulty 16) and copier lease (2,400, difficulty 19) have no VAF page ranking at all. Leap's copier brand is already above you for copier lease indianapolis.",
                "Business phone systems (9,900 searches a month) ranks 25, through the Fort Wayne page rather than the phone systems page.",
                "A blog post on physical intrusion detection is the second-highest traffic URL on the site. Document conversion posts rank 2 to 7 for document conversion companies and document conversion service.",
                "324 of the 586 URLs in your sitemap are blog?p=... query-string posts that share one page's title and image; 90 more are PDFs.",
                "The home page og:image is a stock AI hand image, and the customer comments page describes the company as trusted since 1974.",
                "Forms work but have no CRM integration; the home page title omits Indianapolis and carries one Organization schema block with no LocalBusiness or Service markup.",
                "No LocalBusiness markup for Indianapolis, Fort Wayne or Evansville, so search and AI assistants cannot tie the offices to their cities.",
            ],
            "after": [
                "Every URL that earns a visitor today keeps earning it: a permanent redirect for each one, tested individually at launch (the table below).",
                "Three office pages with LocalBusiness markup, hours where you state them, and the cities each office serves, plus a service area list for the nine cities that had thin pages.",
                "A business phone systems page and a buyer's guide aimed at the 9,900-a-month term you already sit at 25 for (no competitor is in the top 100), a managed IT page with Indianapolis in the title, and standalone managed print and copier pages for the 4,400 and 2,400-a-month terms with no VAF page today.",
                "Twelve guides on real URLs with BlogPosting markup, six of them aimed at terms you rank for on page one or two: document conversion, physical intrusion detection, vCIO, AI policy, copier lease, phone systems. Every solution page carries Service schema, every page with questions carries FAQPage schema, and every office page LocalBusiness, so search engines and AI assistants can read what the page says.",
                "Titles and descriptions written for the terms you already rank for: Indianapolis Managed IT Services and vCIO; Copier Sales, Lease and Rental in Indianapolis; Document Conversion and Scanning Services, Indianapolis.",
                "Organization markup on the home page with your LinkedIn, Facebook, Instagram and Google Business profiles as sameAs, so an AI assistant asked about Van Ausdall resolves to the right company, founded 1914.",
                "Every page under 80 kB of HTML before images, lazy-loading below the fold, pinch-zoom allowed, 16 px inputs, 44 px targets, one H1. Scored on our gate before you see it.",
                "HubSpot forms that create a contact, notify a named person and show a thank-you page. A Technology Strength Assessment that scores as a multi-step form and lands in the CRM.",
            ],
            "keep_heading": "Every page that earns a visitor today keeps earning it",
            "keep": [
                ["/fort-wayne/managed-it-solutions-fort-wayne-in", "/locations/fort-wayne", "managed it services fort wayne #6, 49 keywords"],
                ["/evansville/managed-it-solutions-evansville-in", "/locations/evansville", "managed it evansville #2, 26 keywords"],
                ["/fort-wayne/business-phone-systems-in-fort-wayne-in", "/services/business-phone-systems", "business phone systems #25 (9,900 a month)"],
                ["/fort-wayne/cloud-solutions-fort-wayne-in", "/services/cloud", "cloud services management fort wayne indiana #2"],
                ["/blog?p=what-are-the-benefits-of-a-physical-intrusion-detection-system-240503", "/blog/physical-intrusion-detection-systems", "physical intrusion detection #6; second-highest traffic URL"],
                ["/blog?p=document-conversion-the-key-to-unlocking-efficiency-and-accessibility-241101", "/blog/document-conversion-services-what-to-expect", "document conversion companies #2, digital document conversion #5"],
                ["/communication/business-phone-systems", "/services/business-phone-systems", "voip phone systems indianapolis #5"],
                ["/knowbe4/free-phish-alert-button", "keep as is", "phish alert button #15 (390 a month)"],
                ["/contact/, /support/", "/contact, /support", "branded and phone-number terms"],
            ],
            "note": "Rankings or traffic. Those depend on the market and on what you publish after launch. What we promise is that nothing about the build is the reason they do not come, that every number above is re-measured at 30, 60 and 90 days, and that you see the same report we do.",
        },
        "confirm": [
            "The Evansville office. Your contact and support pages list a phone number but no street address. We built the page with the phone and the region; send the address or tell us it is a service point.",
            "Hours. Indianapolis states 7:00am to 5:00pm; Fort Wayne and Evansville do not. The office pages say call for hours until you confirm.",
            "The response commitment. Your copier pages say same-day service for most metro-area calls and a 24-hour response from the Customer Care Center. We printed both exactly as written; tell us if you want them tightened or removed.",
            "Copier brands. The home and copier pages name Canon, Ricoh, Kyocera and HP; the partners page adds Brother and Zebra. We used all six on the partners page and the four on the copier pages.",
            "The founding line. The customer comments page says trusted since 1974; everything else says 1914. We used 1914 everywhere.",
            "The 112 years. Your history page states it as a number, which goes stale every January. We wrote since 1914 instead.",
            "Steven Sigmon's quote and title, from your managed IT page, are used on the IT page and the About page. Confirm the spelling and that he is happy to be named.",
            "The eighteen case studies. Four are written in full from your pages; the other fourteen are one line each and link to your PDFs until the content is migrated.",
            "The Technology Strength Assessment. We reproduced ten of the eighty questions as a checklist. In the build it becomes a scored multi-step form; tell us how the scorecard is calculated today.",
            "Blog. Six guides are new drafts aimed at terms you rank for. Six more are placeholders adapted from the category guides we wrote for another dealer, to show the blog at its real size; they are replaced by your 324 existing posts, migrated to clean URLs with their original dates.",
            "The calculator's rates are typical figures for orientation; replace them with yours or keep the disclaimer.",
            "Permission to reproduce the customer comments, which are already public on your site, with first names as shown.",
            "Who approves. Brian decides on the website and others weigh in eventually; tell us who, so the copy and go-live approvals do not wait.",
            "The current partner's contract. Month to month at about $1,200; the plan assumes a fourth-quarter start with redirects handled before anything is switched off."],
        "footer": "Prepared for Brian Courtney and the Van Ausdall & Farrar team, following the 1 September call with Patrick Dodge. Nothing here is live or indexed. Every number we could source comes from vanausdall.com, the CEO Juice report it links to, or Semrush on 8 September 2026. Where we drafted a process or a commitment we think you make, it is listed under To confirm. Hero and service photographs are generated stand-ins for the preview, marked as such, until a half-day shoot at the headquarters and in the field; secondary imagery is from your site today; partner logos are the ones on your partners page.",
    }
    pitch["migration"] = MIGRATION
    if pitch["search"].get("site_audit"):
        pitch["search"]["site_audit"]["migration"] = MIGRATION
    content = {"client": CLIENT, "slug": "vanausdall", "domain_hint": "vanausdall.com",
               "brand": brand, "schema": schema, "nav": nav, "pages": pages, "pitch": pitch}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(content, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"wrote {OUT}: {len(pages)} pages, {len(BLOG)} posts")


if __name__ == "__main__":
    build()
