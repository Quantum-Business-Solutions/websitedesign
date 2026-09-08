#!/usr/bin/env python3
"""Authoring script for brands/nexus-network-technologies.content.json.

Run it to regenerate the JSON that scripts/preview.py reads:

    python3 brands/nexus-network-technologies.content.py

Every fact is SOURCED from nexusnt.com (scraped 8 September 2026), the 7/21/2026 call notes in the Nexus
proposal repo, or the proposal canvases QBS already showed Nexus. Items that come only from the proposal
(not from Nexus's own site) are marked PROPOSAL in comments and listed on the hub under To confirm.
No em dashes anywhere; write it clean.
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nexus-network-technologies.content.json")
PHONE, PHONE_HREF = "(919) 897-2700", "tel:9198972700"
EMAIL = "support@nexusnt.com"
ADDRESS = ["630 Davis Drive, Suite 220", "Morrisville, NC 27560"]
HOURS = "Monday to Friday, 8am to 5pm"
CLIENT_REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nexuswebsite")

# ------------------------------------------------------------------ sourced facts (nexusnt.com)
# Survey responses from clients who submitted support tickets, quoted on nexusnt.com. Role and company type only; Nexus does not name them.
VOICES = [
    ["Nexus brings incredible value to the table. They offer attentive and responsive support, understand and care about security, ensure uptime, offer a local presence, have a plan to deal with inevitable failures, employ a smart, knowledgeable and friendly team, all at a reasonable and fair price. There are no compromises. How do you walk away from that?", "CIO", "AI platform"],
    ["Escalations are handled quickly, leadership is accessible, and we are never left waiting for answers. We certainly do not stay up at night worrying about our infrastructure because we know Nexus has it covered.", "Director of Data and Business Intelligence", "Tower development company"],
    ["From the CEO seat, they have reduced the chaos. We no longer worry about systems we do not fully understand. Our performance has improved, costs are predictable, and their team provides true concierge-level service. Simply put, we do not worry about IT anymore.", "CEO", "Healthcare practice management firm"],
    ["Competitive IT providers contact me daily. I have never thought twice about switching. They are a valued part of our team.", "Business Operations Manager", "Biomarker measurement platform"],
    ["Mike Schwarzbauer, owner of Nexus, has visited our site numerous times, making it a point to understand our business himself. Based on our excellent partnership and their expertise, we continue to increase our support hours with them.", "Director of IT", "Genomic amplification technology developer"],
    ["Before Nexus, our team had zero confidence in our IT provider. With Nexus, we have 100% confidence. Nexus has become the standard by which we now assess any third party vendor.", "President and CEO", "Camp for children with serious medical conditions"],
    ["If I had to sum up our overall experience with Nexus in two words, they would be methodical and proactive.", "Vice President", "Real estate management company"],
    ["As a small office, we appreciate the personal relationship with Nexus and the feeling that we are not just another client.", "Office Manager", "Wholesale building supply company"],
    ["They modernized our outdated file infrastructure, reducing costs to about one tenth of what we were paying previously, while improving access and flexibility for our employees.", "Director of IT", "Non-profit foundation for a research park"],
    ["They even helped us reduce our Internet Service Provider costs by 60%.", "Facility Manager", "Furniture manufacturer"],
    ["Since day one, Nexus has brought calm to the chaos. We are always able to reach someone and every single person we have dealt with is equally helpful.", "Director of Audiology", "Sinus center"],
    ["If you need an IT partner and you want things done right the first time, call Nexus. If you want an expert tech bench, call Nexus.", "IT Director", "Law firm"],
]
# Use cases published on nexusnt.com (How We're Different).
CASES = [
    ["Growing real estate company, 35 employees", "Onboarding a new employee meant buying a computer, delivering it to the MSP, waiting for an engineer to configure it, then delivering it again.", "Workstation automation", "The new employee receives the computer, logs in, and it configures itself and installs the designated software. Faster onboarding, happier staff."],
    ["Regulated materials storage firm, rapidly growing", "Launching a brand new regulated facility while navigating validation, SOP documentation and investor scrutiny, with no formal disaster recovery framework.", "ISP coordination, enterprise network and Wi-Fi with automated failover, validated monitoring, managed IT support and a formal disaster recovery and backup SOP", "A stable, audit-ready IT foundation that supported vendor and investor due diligence, aligned a UK expansion, and set a QBR reporting cadence."],
    ["Growing small to mid-size firm", "A security incident raised the risk of reputational harm and cost the firm confidence in its security framework.", "Advanced security for network design, delivered as Network as a Service with managed services", "Reduced security risk and restored confidence."],
    ["Established engineering firm, 20 years, 20 employees", "On-premise servers at end of life: replace them with a large capital purchase, or move to the cloud.", "Serverless infrastructure", "Applications and files in the cloud, an upgraded network, secure work from anywhere without a VPN, and technology moved from a variable capital expense to a manageable operating expense."],
]
PARTNERS = ["Fortinet", "Cisco", "Meraki", "Aruba", "Dell", "Microsoft", "Azure", "AWS", "VMware", "Huntress"]
COMPLIANCE = ["NIST", "HIPAA", "FDA", "cGMP"]
TEAM = [["Mike Schwarzbauer", "Founder and President", "assets/team/mike.jpg", "An IT industry veteran whose career includes systems engineering, project engineering and senior IT leadership. Mike founded Nexus to give companies a partner that makes customer advocacy a priority."],
        ["Shane Bull", "Strategic Account Manager", "assets/team/shane.jpg", "Helps businesses grow by improving financial results, protecting assets and building risk management into growth plans."],
        ["Ronnie Watson", "Services Delivery Manager", "assets/team/ronnie.jpg", "Eighteen years in managed services, running the team that answers the first call."]]

# The eight lines. Five are live on nexusnt.com today; three come from the proposal's brand house and are marked PROPOSAL.
# slug, nav label, short, one-line, image, eyebrow, heading, subhead, benefits [[t,b]], included [..], faq [[q,a]], proposal?
SERVICES = [
    ["managed-it", "Managed IT and Support", "Managed IT", "Take IT off your plate, as little or as much as you need, with security built in.", "assets/rack-1200.jpg", "Managed IT and Support",
     "Performance <em>without interruption</em>.", "Peace of mind for leadership when uptime and security matter, and a positive experience for the people who need help. Real engineers on the first call, and a plan that gets you out of the break-fix cycle.",
     [["Top-shelf support", "Experienced engineers on the first call, not a help desk reading a script. US-based."], ["First-call resolution in 15 minutes", "The target Nexus publishes and staffs for."], ["24x7 monitoring", "Network, servers, workstations, cloud and security watched around the clock, so issues are prevented rather than reported."], ["Quarterly business review", "A regular technical assessment so the environment stays consistent, current and ahead of problems."], ["Annual technology and network assessment", "A full review of network, applications and devices against technical and management risk."], ["IT infrastructure budgeting", "A technology roadmap and a multi-year budget that align with your business goals."]],
     ["Central management and setup of all workstations, with Microsoft 365 licensing", "Same-day computer builds: the new employee logs in and the machine configures itself", "Regular diagnostic review to find low-performing machines", "Cloud-managed workstations with remote access", "BitLocker drive encryption", "Azure self-service password resets", "Microsoft 365 review and hardening", "Serverless print automation", "Threat analysis, patching, multi-factor authentication, email malware protection and web filtering"],
     [["Is support US-based?", "Yes. A dedicated team of experienced engineers based in the United States."], ["Does it work for a hybrid workforce?", "Yes. Centralized management, next-generation office security and performance monitoring are built for people who work from more than one place."], ["Can you work alongside our internal IT team?", "Yes. Co-managed support beside your team, or fully managed IT, and you can move between them."], ["How is Nexus different from a typical MSP?", "Short hold times, experienced people who fix it the first time, a network stack that follows a security framework, and a proactive approach that ends the constant break-fix cycle."]], False],
    ["networking", "Networking", "Network as a Service", "The full network stack as a predictable monthly service, with turnkey security included.", "assets/rack-1200.jpg", "Network as a Service",
     "A network is only invisible <em>when it works</em>.", "Hardware, software, management tools, licenses, internet access, backups and lifecycle services in one flat monthly rate. Designed for security from the ground up, refreshed on a schedule, and replaced the same day if a component fails.",
     [["Reduce costs", "No capital purchase of hardware, software or licensing, and no surprise network purchases through the term."], ["Improve security", "Least privilege, microsegmentation, layered network isolation and log ingestion for threat hunting, built into the fabric."], ["Increase performance", "A built-in refresh cycle keeps you on the current generation of equipment."], ["Ensure continuity", "Same-day replacement of a failed component, guaranteed, where manufacturers can take weeks."], ["Minimize downtime", "24/7/365 proactive monitoring that tracks failures and reduced performance between devices."], ["Amplify productivity", "Scheduled maintenance and troubleshooting leave your plate."]],
     ["Network design and installation for your space", "Managed switching and Wi-Fi", "Turnkey network security in the fabric, not sold separately", "Internet access coordinated with the carriers", "Firmware and security patching included", "Monthly, annual or five-year payment options", "Move-in and set-up support for a new space"],
     [["What is Network as a Service?", "A subscription model for the whole network: hardware, software, management tools, licenses, backups, internet access and lifecycle services, all included at a flat monthly rate."], ["Is support included?", "Yes, from Nexus engineers. If a component stops working properly, Nexus guarantees same-day replacement."], ["What payment options are there?", "Monthly, annually, or fully upfront for five years, with discounts on the annual and five-year options."], ["We are moving offices. Can you help?", "Yes. Nexus provides the plans and execution for a move, and the service model gives you quick set-up, monitoring and simple billing."]], False],
    ["cybersecurity", "Cybersecurity", "Cybersecurity", "Layered protection from edge to endpoint, aligned to the NIST Cybersecurity Framework.", "assets/rack-1200.jpg", "Cybersecurity",
     "Security that <em>will not surprise you</em>.", "The edge firewall is only the first line. Nexus designs networks on a least-privilege model, keeps device types separate, inspects traffic between them, monitors for indicators of compromise and trains the people who are now the endpoints.",
     [["Least privilege by design", "Everything is untrusted and blocked unless explicitly granted."], ["Microsegmentation", "Devices of different types and functions are kept apart."], ["Inter-network firewall", "Anti-malware and intrusion prevention on traffic between segments."], ["SIEM and SOC monitoring", "Alerts, automated response and remediation when an indicator of compromise appears."], ["Security awareness training", "A baseline phishing campaign, training, regular simulations and an annual refresher."], ["Cloud-to-cloud backup", "Because Microsoft, Google, Salesforce, Box and Dropbox all recommend a third-party backup in their terms."]],
     ["Spam and advanced content filtering", "Antivirus and breach detection and response", "Multi-factor authentication", "Patching", "BitLocker encryption", "Password protection and management", "Customized NIST CSF cybersecurity reports in the quarterly business review", "Cyber liability insurance application assistance"],
     [["Do you help with compliance?", "Yes. HIPAA, PCI, FDA 21 CFR Part 11 and GMP, with the network configuration, group policy and security policy paperwork provided by Nexus."], ["What happens in an incident?", "Nexus is alerted, automatically responds to maintain network integrity, and remediates every system that requires it. Your team is informed throughout."], ["Do you train staff?", "Yes. An initial phishing campaign sets the baseline, everyone gets entry-level training, simulations continue at moderate and high difficulty, and anyone who engages gets more."], ["Can you help with cyber insurance?", "Yes. Nexus helps with the application and works with your insurance agent."]], False],
    ["meeting-spaces", "Meeting Spaces", "Nexus Collab", "Rooms that are meeting-ready every time, as a subscription.", "assets/meeting-1200.jpg", "Meeting Spaces: Nexus Collab",
     "Walk in, press one button, and it <em>just works</em>.", "Nexus Collab is a turnkey, subscription-based answer to meeting technology for in-room and remote attendees. Nexus assesses, procures, installs, monitors and stands on call, with a fixed monthly fee and a built-in equipment refresh.",
     [["Needs and planning assessment", "A walk-through of your rooms and a plan for near-term and long-term goals. Rooms up to 30 by 30 feet."], ["On-site installation and testing", "Installed and tested for day-one performance."], ["Updates and monitoring", "Remote monitoring and automated updates in off hours."], ["Current equipment", "Displays, AV bar, microphones, cameras, room scheduler and meeting controls, compatible with Zoom or Teams."], ["On-call support", "Nexus AV experts with full remote access."], ["Fixed monthly fee", "No billing surprises, and the equipment is maintained for the length of the contract."]],
     ["Huddle rooms, conference rooms and mobile meeting set-ups", "A mobile AV option to move from space to space", "Demonstration meeting and huddle rooms at the Nexus office in Morrisville", "Zoom and Teams compatible"],
     [["Can we see it working first?", "Yes. Nexus has demonstration meeting and huddle rooms set up in its office. Contact Shane Bull to schedule a demo."], ["What does it cost?", "A fixed monthly fee, with the equipment maintained for the length of the contract."], ["Does the equipment get refreshed?", "Yes. The contract has a built-in refresh cycle."], ["Which platforms?", "Zoom and Teams, with rooms designed around how your team meets."]], False],
    ["site-intelligence", "Site Intelligence Platform", "Site Intelligence", "Cameras, access control and identity management as one turnkey platform.", "assets/hero-plate-1200.jpg", "Site Intelligence Platform",
     "Security <em>without sacrificing convenience</em>.", "Business risk extends to your physical space. Cameras, access control and modern identity management, backed by the Nexus network and on-call support, installed in two to three weeks with one installation fee and a preset monthly fee.",
     [["Turnkey, with on-call support", "Nexus assesses, procures, oversees installation, trains your staff and is your on-call team."], ["Lower business risk", "Access, employee transitions, deliveries and surveillance streamlined, with monitoring that can reduce workers' compensation risk."], ["Access from anywhere", "Mobile credentials, facial recognition, and remote video and audio visitor access from desktop or phone."], ["AI-enabled equipment", "Facial detection and license plate recognition, on weatherproof and tamper-resistant hardware."], ["One screen", "Multiple cameras and door controls in a single view."], ["Predictable billing", "One installation fee, one preset monthly fee."]],
     ["Cameras, NVRs, control hubs, smart readers, locks, doorbells, key fobs and intercoms", "Entry method, timing and access history tracked", "Installation handled with approved vendors", "Equipment refresh at the end of the term, or an upgrade after two years"],
     [["How long does installation take?", "Typically two to three weeks after the contract is signed."], ["Do we need our own cabler?", "No. Nexus handles installation with approved vendors."], ["Can we see several cameras at once?", "Yes, in a single view with the door controls."], ["Is upgraded equipment included?", "Equipment can be refreshed at the end of the term, or upgraded after two years on a new term."]], False],
    ["consultation-projects", "Consultation and Projects", "Virtual CIO and projects", "A virtual CIO for strategy and budgeting, or a lead engineer for one project, at a fixed price.", "assets/meeting-1200.jpg", "Consultation and Project Services",
     "Exactly what you need, <em>when you need it</em>.", "A virtual CIO who works as an extension of your leadership team, or a lead engineer assigned to one project and priced as a fixed fee with no change orders. Nexus meets you where you are.",
     [["Finance and budgeting", "An audit of existing spend and a multi-year IT budget plan."], ["Audit of IT operations and risk", "How you use IT today, what you will need, and the risks in the current workflow."], ["Present and execute", "A full plan for your executive committee, then delivery with your people and outside vendors."], ["Fixed project pricing", "Quotes are fixed fees. No change orders, and a guarantee to make it work within the budget."], ["A lead engineer per project", "Planned around your business processes so day-to-day work is not disrupted."], ["Vendor neutral", "Advice based on years of engineering experience, not on what is in stock."]],
     ["Cloud migrations and configuration", "Server, virtualization and email upgrades and migrations", "Networking and Wi-Fi upgrades, with wireless heat mapping", "Microsoft 365 security hardening", "HIPAA and PII compliance", "Security testing and configuration overhaul"],
     [["We are not sure what we need. Can you help?", "Yes. Nexus audits the current set-up, the challenges and the goals, and proposes the path."], ["We have had security incidents.", "Nexus identifies the weaknesses, fixes them quickly and automates security so you leave the incident cycle."], ["The Wi-Fi is spotty.", "Wireless heat mapping finds the problem areas and drives the design."], ["How are projects priced?", "Flat rates. Fixed fees, no change orders, a budget you can plan around."]], False],
    ["digital-signage", "Digital Signage", "Nexus Engage", "Screens that speak for your brand, managed from one place.", "assets/hero-plate-1200.jpg", "Digital Signage: Nexus Engage",
     "Every screen <em>on brand, on time</em>.", "Lobby displays, wayfinding, menus and internal messaging, scheduled and controlled centrally across every location, with the hardware provided and the screens kept on and current.",  # PROPOSAL
     [["Display hardware", "The right screens and players for each space."], ["Content management", "Update everything from one dashboard, or have Nexus manage it."], ["Templates and scheduling", "On-brand content, published on time."], ["Multi-site rollout", "Consistent deployment across locations."], ["Managed support", "Screens stay on and current."], ["On the Nexus network", "Signage rides the same secured network as everything else."]],
     ["Lobby, wayfinding, menu and internal messaging screens", "Central control of every screen", "Hardware, players and mounting", "Content templates in your brand"],
     [["Can we manage content ourselves?", "Yes, from one dashboard, or Nexus manages it for you."], ["Multiple sites?", "Yes. Consistent content across all locations from one place."], ["Do you provide the hardware?", "Yes. Displays and players, installed."]], True],
    ["building-systems", "Cabling, Audio and Cellular", "Building systems", "The wiring in the walls, sound that fills the space and cell signal in every corner.", "assets/rack-1200.jpg", "Structured Cabling, Building Audio and Cellular",
     "The systems <em>in the walls</em>, done right the first time.", "Structured cabling and low voltage, paging and background audio, and cellular enhancement so the phone works everywhere in the building. One installer for everything that connects to the network.",  # PROPOSAL
     [["Structured cabling and low voltage", "Documented, labelled and tested. The foundation the network stands on."], ["Office and building audio", "Paging, background music and sound that fills the space."], ["Cellular enhancement", "Reliable signal in every corner of the building."], ["One installer", "The same team that designs the network runs the cable it depends on."], ["Move-in ready", "Planned with the network for a new space."], ["Documented", "Every run recorded, so the next change is quick."]],
     ["Cable plant design and installation", "Patch panels and racks", "Paging and background music systems", "Cellular signal boosters and distributed antennas"],
     [["Do you handle the cabling with a network install?", "Yes. Structured cabling and low voltage are part of the Nexus brand house, so one partner does the whole install."], ["Can you fix bad cell signal inside?", "Yes. Cellular enhancement systems bring reliable signal to every corner of the building."]], True],
]
SERVICE_SLUGS = [s[0] for s in SERVICES]
INDUSTRIES = [  # slug, name, image, one-line, body, bullets, faq
    ["life-sciences", "Life sciences", "assets/lab-1200.jpg", "Regulated, audited and never nine to five.",
     "Nexus's internal security division is led by senior security engineers with experience across HIPAA, PCI, FDA 21 CFR Part 11 and GMP. Networks are designed for compliance from day one, monitored around the clock, and reported on monthly, with NIST CSF reports in every quarterly review.",
     ["Audit and compliance assistance for FDA, PCI, HIPAA and GMP", "Complete compliance paperwork: network configuration, strategy and design, group policy, security design and policies", "Monthly reporting on security, endpoints, hardware lifecycle, software and network monitoring", "Validated machine controls", "Cyber liability insurance assistance", "Disaster recovery and business continuity"],
     [["Can you work inside a validated environment?", "Yes. Nexus has coordinated with environmental monitoring and validation vendors on regulated builds, and the SOP approach is written for it."], ["Do you support labs that run overnight?", "Yes. Critical infrastructure is monitored 24x7, 365 days a year, and most potential issues raise an alert within minutes."]]],
    ["professional-services", "Professional services", "assets/meeting-1200.jpg", "When time is revenue, IT problems are expensive.",
     "Law, accounting, architecture, engineering, real estate and advisory firms take IT management off their plate with Nexus, with as little or as much support as they need, and meeting rooms that work the first time.",
     ["Managed IT and helpdesk from real engineers", "Meeting rooms that are ready every time", "Secure work from anywhere without a VPN", "Fixed-price projects for moves and migrations", "Mac specialists for Mac-based firms"],
     [["We are a Mac shop.", "Nexus has assigned Mac specialists to Mac-based clients, and one calls that specialist very responsive and knowledgeable."], ["Can you help with an office move?", "Yes. Nexus coordinates the carriers and internet providers, designs the network for the new space and has it running on move-in day."]]],
    ["manufacturing", "Manufacturing and warehousing", "assets/warehouse-1200.jpg", "Always-on connectivity for production-ready environments.",
     "Real-time visibility, inventory management and coordination across operations depend on networks that do not drop. Nexus builds purpose-built networks for manufacturing, warehousing and flex space, with Wi-Fi that reaches the far racks and cameras and access control on the same fabric.",
     ["Enterprise network and Wi-Fi with automated failover", "Site Intelligence Platform: cameras and access control", "Cellular enhancement for the floor", "Structured cabling for new and expanded space", "24x7 monitoring"],
     [["Can you cover a large floor with Wi-Fi?", "Yes. Wireless heat mapping drives the design, and monitoring tracks performance between devices."], ["Do you handle the cameras too?", "Yes. The Site Intelligence Platform puts cameras, door controls and access history on one screen."]]],
    ["growing-businesses", "Growing businesses", "assets/hero-plate-1200.jpg", "A just-right option for the rest.",
     "From consultation and project support to full managed services and strategy, Nexus offers a flexible model for organizations that do not fit a category: non-profits, camps, agencies, wholesalers, healthcare practices and investment firms among its clients.",
     ["Start with one service and grow into the brand house", "Co-managed or fully managed", "A virtual CIO when you need strategy, not a full-time hire", "Fixed-price projects"],
     [["We only need help with part of our IT.", "That is fine. Many clients start with one service and add more as they grow."], ["Are we too small?", "Nexus would rather serve a smaller number of good-fit clients well. Ask; the answer will be honest either way."]]],
]


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


LEADFORM = {"type": "leadform", "alt": True, "id": "conversation", "heading": "Start with a conversation", "body": "Not a pitch. Nexus asks about your environment, your people and what keeps you up at night, and says honestly whether it is the right fit.", "submit": "Start the conversation", "note": "A Nexus engineer or Shane replies within one business day."}
VOICES_SHORT = [v for v in VOICES if len(v[0]) < 200]


def _flow(fid, eyebrow, heading, intro, steps, receive_label="What you receive"):
    return {"type": "flow", "id": fid, "alt": True, "eyebrow": eyebrow, "heading": heading, "intro": intro, "receive_label": receive_label,
            "steps": [{"label": a, "when": b, "summary": c, "title": d, "body": e, "receive": f} for a, b, c, d, e, f in steps]}


def _ba(bid, heading, b_title, b_body, b_items, a_title, a_body, a_items, b_eyebrow="A typical MSP", a_eyebrow="With Nexus"):
    return {"type": "beforeafter", "id": bid, "eyebrow": "Before and after", "heading": heading,
            "before": {"eyebrow": b_eyebrow, "title": b_title, "body": b_body, "items": b_items},
            "after": {"eyebrow": a_eyebrow, "title": a_title, "body": a_body, "items": a_items}}


# Per-service charts and comparisons. Every line is on nexusnt.com or in a published client quote.
SERVICE_MODULES = {
    "managed-it": [
        _ba("ba", "Drag to compare a typical MSP with Nexus managed IT",
            "A ticket, a script, an escalation", "You describe the problem three times before someone who can fix it hears it.",
            ["A help desk reading a script", "Long hold times and outages", "Escalate, wait, escalate again", "Break-fix invoices you cannot budget", "The owner is a name on a website"],
            "An engineer on the first call", "Properly staffed with experienced people who fix it the first time.",
            ["First-call resolution in 15 minutes, the published target", "Short hold times, US-based engineers", "24x7 monitoring so problems are prevented, not reported", "Quarterly business review and an annual assessment", "The owner has visited clients' sites himself, in a client's words"]),
        _flow("flow", "How managed IT starts", "Four steps from the first conversation to a quiet network", "Click a step.",
              [["Conversation", "Week 1", "Curious, not a pitch.", "A conversation about how your business runs", "Nexus does not use sales words or techniques. The first meeting is a conversation to uncover what the issues really are, and whether Nexus is the right fit. Sometimes it is not, and Nexus says so.", ["An honest read on fit", "The questions Nexus will need answered", "No proposal until both sides want one"]],
               ["Assess", "Weeks 1 to 2", "Environment, risks, goals.", "An assessment of the environment you have", "Network, applications, devices and workflow, against technical and management risk. The same annual assessment Nexus runs for every managed client, done first.", ["A written picture of the environment", "The risks, ranked", "A fixed-fee plan for what to fix first"]],
               ["Onboard", "Weeks 3 to 6", "Weekly meetings, everything documented.", "Standardize, secure and document", "Onboarding runs with weekly meetings, in a client's words thorough and easing the transition. Workstations come under central management, MFA and encryption are turned on, and the network stack is brought to the security framework.", ["Weekly onboarding meetings", "Documented environment", "Monitoring live on every device"]],
               ["Manage and review", "Ongoing", "24x7 monitoring, QBR every quarter.", "Monitoring around the clock, a review every quarter", "Nexus watches network, servers, workstations, cloud and security 24x7. Every quarter, a business review with a technical assessment and NIST CSF reporting; every year, the full assessment again.", ["Quarterly business review", "Annual technology and network assessment", "A roadmap and a multi-year budget"]]])],
    "networking": [
        _ba("ba", "Drag to compare owning a network with Network as a Service",
            "Buy it, own it, hope", "Capital spent up front, then equipment ages until it fails.",
            ["A capital purchase every five to seven years", "Firmware and patching when someone remembers", "A failed switch and a manufacturer RMA measured in weeks", "Security bolted on after the fact", "Surprise purchases through the term"],
            "One flat monthly rate, everything included", "Hardware, software, licenses, internet, backups and lifecycle in one number.",
            ["No capital expense", "Patching and firmware included", "Same-day replacement of a failed component, guaranteed", "Security built into the fabric: least privilege, microsegmentation, threat hunting", "A scheduled refresh so you never run old equipment"]),
        _flow("flow", "How a network is delivered", "Survey, design, deploy, support", "Click a step.",
              [["Survey", "Week 1", "Sites and requirements.", "A survey of the sites and how you work", "Nexus assesses each location, the applications that run on the network, guest access, video and any research or automation devices. Wireless heat mapping where coverage matters.", ["Site survey and heat map", "Requirements written down", "Carrier and internet options"]],
               ["Design", "Week 2", "For performance and security.", "Engineered for performance and security", "Least privilege, microsegmentation, an inter-network firewall and layered isolation, designed in rather than added.", ["Network design", "Security design", "A flat monthly price"]],
               ["Deploy", "Move-in or a date you choose", "Clean, documented install.", "A clean, documented installation", "Configured, installed, labelled and documented, coordinated with the carrier so internet is live on the day.", ["Installed and tested", "Documentation", "Monitoring switched on"]],
               ["Support", "Ongoing", "24/7/365 monitoring.", "Monitored and replaced the same day", "Failures and reduced performance between devices are tracked around the clock. If a component fails, Nexus replaces it the same day.", ["24/7/365 monitoring", "Same-day replacement guarantee", "Scheduled refresh"]]])],
    "cybersecurity": [
        _ba("ba", "Drag to compare castle-and-moat security with edge-to-endpoint",
            "A firewall at the edge, trust inside", "Anything inside the perimeter is assumed safe. That assumption is how breaches spread.",
            ["One edge firewall", "Flat network: every device sees every other", "Antivirus, and hope", "Training once, if ever", "Backups the cloud provider is assumed to keep"],
            "Layered, least privilege, monitored", "Everything untrusted until granted, and every layer reports to the same fabric.",
            ["Least privilege model", "Microsegmentation between device types", "Inter-network firewall with intrusion prevention", "SIEM and SOC monitoring with automated response", "Phishing baseline, training, simulations and an annual refresher", "Cloud-to-cloud backup"]),
        _flow("flow", "How security is raised", "Assess, harden, monitor, respond", "Click a step.",
              [["Assess", "Week 1", "Gaps, ranked by risk.", "Identify the gaps and rank the risk", "Network, endpoints, email, cloud and people, against the NIST Cybersecurity Framework.", ["A gap list against NIST CSF", "Risk ranked", "A fixed-fee plan"]],
               ["Harden", "Weeks 2 to 4", "Systems and people.", "Close the gaps across systems and people", "MFA, encryption, patching, filtering, segmentation, and the baseline phishing campaign that starts the training programme.", ["MFA and BitLocker on", "Segmented network", "Training baseline set"]],
               ["Monitor", "Ongoing", "24/7 detection.", "Watch everything, all the time", "SIEM and SOC monitoring across the environment. When an indicator of compromise appears, Nexus is alerted and responds automatically to keep the network intact.", ["24/7 monitoring", "Automated response", "Monthly security reporting for regulated clients"]],
               ["Report", "Quarterly", "NIST CSF in the QBR.", "Report in the quarterly review", "Customized cybersecurity reports based on the NIST framework in every quarterly business review, plus help with the cyber insurance application.", ["Quarterly NIST CSF report", "Cyber insurance assistance", "An updated plan"]]])],
    "meeting-spaces": [
        _ba("ba", "Drag to compare the usual conference room with a Nexus Collab room",
            "Ten minutes of cables", "Every meeting starts with someone fixing the room.",
            ["A different setup in every room", "Cables, adapters and a laptop on the table", "Remote attendees who cannot hear", "Nobody to call when it fails", "Equipment bought once and never updated"],
            "One button, every room, every time", "The same simple room everywhere, monitored and kept current.",
            ["One-touch join on Zoom or Teams", "Displays, AV bar, microphones, cameras and scheduler included", "Remote monitoring and off-hours updates", "AV experts on call with remote access", "Fixed monthly fee with a built-in refresh"]),
        _flow("flow", "How a room becomes meeting-ready", "Assess, install, monitor, support", "Click a step.",
              [["Assess", "Week 1", "A walk-through of your rooms.", "Needs and planning assessment", "Conversations and a walk-through of the facility, then a plan for near-term and long-term goals. Rooms up to 30 by 30 feet, and a mobile option for spaces that change.", ["Room-by-room plan", "Equipment list", "Fixed monthly price"]],
               ["Install", "A date you choose", "Installed and tested.", "On-site installation and testing", "Nexus installs and tests every room for day-one performance.", ["Rooms installed", "Tested with your platform", "Staff shown the one button"]],
               ["Monitor", "Ongoing", "Updates in off hours.", "Updates and monitoring", "Equipment is monitored remotely and updated automatically outside working hours.", ["Remote monitoring", "Automated updates", "Latest features"]],
               ["Support", "When needed", "On call, with remote access.", "On-call support", "Nexus AV experts are on call with full remote access to prevent meeting mishaps.", ["On-call AV experts", "Remote fixes", "Equipment refresh in the contract"]]])],
    "site-intelligence": [
        _ba("ba", "Drag to compare keys and a DVR with the Site Intelligence Platform",
            "Keys, fobs and a DVR in a closet", "Nobody knows who came in, and the footage is found after the fact.",
            ["Physical keys that leave with former employees", "A DVR nobody checks", "No record of who entered, or when", "Visitors and deliveries handled by whoever is nearest", "A capital purchase, then obsolescence"],
            "Every door and camera on one screen", "Access, identity and video, from a desk or a phone.",
            ["Mobile credentials and facial recognition", "Entry method, time and history tracked", "Remote video and audio visitor access", "AI features: facial detection, license plate recognition", "One installation fee, one preset monthly fee, refresh at term end"]),
        _flow("flow", "How the platform goes in", "Assess, install, train, support", "Click a step.",
              [["Assess", "Week 1", "Doors, cameras, risks.", "An assessment of your security needs", "Every door, delivery point and camera position, and the risks the platform should address, from unauthorized access to workers' compensation exposure.", ["A site plan", "Equipment list", "One installation fee and the monthly fee"]],
               ["Install", "Weeks 2 to 3", "Two to three weeks, typically.", "Procured and installed", "Nexus procures the equipment and oversees installation with approved vendors. Typical delivery is two to three weeks from signing.", ["Cameras, readers, locks and hubs installed", "On the Nexus network", "Tested"]],
               ["Train", "Install week", "Your staff, on the platform.", "Staff trained", "Your team learns the single view, mobile credentials and visitor access.", ["Trained administrators", "Access rules set", "History reporting"]],
               ["Support", "Ongoing", "On call.", "On-call support and refresh", "Nexus is your on-call support team, and the equipment can be refreshed at the end of the term or upgraded after two years.", ["On-call support", "Refresh at term end", "Upgrade path"]]])],
    "consultation-projects": [
        _ba("ba", "Drag to compare a time-and-materials project with a Nexus fixed-fee project",
            "An estimate, then change orders", "The budget is a guess and the invoice is a surprise.",
            ["Hourly estimates", "Change orders as scope becomes clear", "Whoever is free does the work", "Business disrupted during the change", "No one accountable for the outcome"],
            "A fixed fee and a lead engineer", "Quoted once, planned around your processes, delivered within the budget.",
            ["Fixed fees, no change orders", "A guarantee to make it work within the budget allocated", "A lead engineer who plans and executes", "Aligned with your business processes so day-to-day is not disrupted", "Security and reliability as the operating focus"]),
        _flow("flow", "How a virtual CIO engagement runs", "Audit, budget, present, execute", "Click a step.",
              [["Audit", "Weeks 1 to 2", "Operations, spend and risk.", "Audit IT operations, risk and spend", "How the business uses IT today, future needs, potential risks in the workflow, and an audit of existing expenditure with finance.", ["IT and risk assessment", "Spend audit", "Efficiency recommendations"]],
               ["Budget", "Week 3", "Multi-year plan.", "A multi-year IT budget", "A budget plan that avoids wasted resources and aligns technology with business goals, built with your finance team.", ["Multi-year budget", "Roadmap", "Priorities"]],
               ["Present", "Week 4", "To the executive committee.", "A plan presented to leadership", "A full-scale plan presented to your executive committee, with the case for each move.", ["Executive presentation", "Decisions recorded", "Owners assigned"]],
               ["Execute", "Ongoing", "With your people and vendors.", "Execution with internal resources and outside vendors", "Nexus works with your internal team and outside vendors to implement the changes and make sure deliverables are met.", ["Implementation", "Vendor coordination", "Deliverables tracked"]]])],
    "digital-signage": [
        _flow("flow", "How signage rolls out", "Plan, install, publish, manage", "Click a step.",
              [["Plan", "Week 1", "Screens, content, goals.", "Map screens, content and goals", "Which spaces get a screen, what each one says, and who updates it.", ["Screen plan", "Content plan", "Fixed price"]],
               ["Install", "Weeks 2 to 3", "Displays and players.", "Displays and players installed", "Cleanly deployed on the Nexus network.", ["Installed screens", "Central control live", "Tested"]],
               ["Publish", "Week 3", "On brand, scheduled.", "On-brand content, scheduled centrally", "Templates in your brand, scheduled and published from one dashboard.", ["Templates", "Schedule", "Training"]],
               ["Manage", "Ongoing", "Kept on and current.", "Ongoing updates and support", "Nexus keeps the screens on and current, or you manage content yourself.", ["Managed support", "Content updates", "Multi-site consistency"]]])],
    "building-systems": [
        _flow("flow", "How the systems in the walls are delivered", "Survey, design, install, document", "Click a step.",
              [["Survey", "Week 1", "Paths, sound, signal.", "A survey of cable paths, acoustics and cell signal", "Where the cable can run, where the sound needs to reach, and where the phone drops.", ["Survey", "Signal map", "Fixed price"]],
               ["Design", "Week 2", "With the network.", "Designed alongside the network", "Cable plant, audio zones and cellular coverage designed with the network they serve.", ["Design", "Bill of materials", "Schedule"]],
               ["Install", "A date you choose", "Labelled and tested.", "Installed, labelled and tested", "Runs pulled, terminated, labelled and tested; speakers and antennas placed and tuned.", ["Installed systems", "Test results", "Clean closet"]],
               ["Document", "At handover", "Every run recorded.", "Everything documented", "Every run, zone and antenna recorded, so the next change is quick and nobody guesses.", ["As-built documentation", "Labels", "Support"]]])],
}


def service_page(slug, navlabel, short, one, image, eyebrow, heading, subhead, benefits, included, faq, proposal):
    secs = [
        {"type": "hero", "layout": "split", "eyebrow": eyebrow, "heading": heading, "subhead": subhead,
         "primary": {"label": "Start the conversation", "href": "contact.html"}, "secondary": {"label": "All services", "href": "services.html"},
         "image": image, "image_alt": navlabel, "image_w": 1200, "image_h": 800},
        {"type": "cards", "alt": True, "eyebrow": "What changes", "heading": f"What changes with Nexus {short.lower() if short[0].isupper() and not short.startswith('Nexus') else short}", "items": benefits},
    ]
    secs += SERVICE_MODULES.get(slug, [])
    secs.append({"type": "detail", "eyebrow": "What is included", "heading": "What you get", "body": ("From the proposal's brand house, to be confirmed with Nexus. " if proposal else "") + "Delivered, secured and supported by the same team as everything else your business runs on. One partner, one point of contact, one point of accountability.", "bullets": included, "image": image, "flip": True})
    secs.append({"type": "testimonials", "alt": True, "heading": "In clients' words", "items": [VOICES[1][:3], VOICES[3][:3], VOICES[7][:3]] if slug in ("managed-it", "consultation-projects") else [VOICES[0][:3], VOICES[2][:3], VOICES[6][:3]]})
    secs.append({"type": "faq", "heading": f"Questions about {navlabel.lower() if not navlabel.startswith('Nexus') else navlabel}", "items": faq})
    secs.append(LEADFORM)
    return {"file": f"services/{slug}.html", "title": f"{navlabel} | Nexus Network Technologies, Raleigh-Durham", "description": desc(f"{one} {subhead}"),
            "crumbs": [["Home", "index.html"], ["Services", "services.html"], [navlabel, f"services/{slug}.html"]], "sections": secs}


def industry_page(slug, name, image, one, body, bullets, faq):
    return {"file": f"industries/{slug}.html", "title": f"IT for {name.lower()} | Nexus Network Technologies", "description": desc(f"{one} {body}"),
            "crumbs": [["Home", "index.html"], ["Industries", "industries.html"], [name, f"industries/{slug}.html"]],
            "sections": [
                {"type": "hero", "layout": "centered", "eyebrow": f"Industries: {name}", "heading": one, "subhead": brief(body, 220), "primary": {"label": "Start the conversation", "href": "contact.html"}},
                {"type": "detail", "eyebrow": "What Nexus sets up", "heading": f"Built for how {name.lower()} runs", "body": body, "bullets": bullets, "image": image},
                {"type": "testimonials", "alt": True, "heading": "From clients in this space", "items": INDUSTRY_QUOTES[slug]},
                {"type": "faq", "heading": f"Questions from {name.lower()}", "items": faq},
                LEADFORM]}


INDUSTRY_QUOTES = {"life-sciences": [VOICES[3][:3], VOICES[4][:3]], "professional-services": [VOICES[6][:3], VOICES[11][:3]], "manufacturing": [VOICES[9][:3], VOICES[7][:3]], "growing-businesses": [VOICES[5][:3], VOICES[10][:3]]}

SWITCH_MODEL = "assets/fleet/switch.glb" if os.path.exists(os.path.join(CLIENT_REPO, "assets", "fleet", "switch.glb")) else None

WHEEL_ITEMS = [[s[1], s[3], f"services/{s[0]}.html", s[2]] for s in SERVICES]

FLOW_ENGAGEMENT = {"type": "flow", "id": "flow", "eyebrow": "How Nexus works with you", "heading": "It starts as a conversation, and every stage hands you something",
    "intro": "Nexus does not use sales words. Click a stage to see what actually happens and what you leave with.",
    "steps": [
        {"label": "Conversation", "when": "First meeting", "summary": "Curious, not a pitch.", "title": "A conversation about how your business runs",
         "body": "The first meeting is inquisitive: what is working, what is not, what the last provider did, and what enterprise-level would mean for you. Nexus will say if it is not the right fit. Some prospects hear that, and that is okay.",
         "receive": ["An honest read on fit", "The questions Nexus needs answered", "No proposal until both sides want one"]},
        {"label": "Assess", "when": "Weeks 1 to 2", "summary": "Environment, risk, spend.", "title": "The environment you have, written down",
         "body": "Network, applications, devices, workflow and spend, ranked by technical and management risk. The same assessment Nexus runs annually for managed clients, done first and shared whether or not you proceed.",
         "receive": ["A written picture of the environment", "Risks, ranked", "A fixed-fee plan for what to fix first"]},
        {"label": "Plan", "when": "Week 3", "summary": "Fixed fees. No change orders.", "title": "A plan you can budget",
         "body": "Project quotes are fixed fees with no change orders, and Nexus guarantees to make it work within the budget. Ongoing services are flat monthly rates with everything included.",
         "receive": ["Fixed project fees", "Flat monthly rates", "A multi-year budget if you want one"]},
        {"label": "Onboard", "when": "Weeks 4 to 8", "summary": "Weekly meetings, everything documented.", "title": "Standardize, secure, document",
         "body": "Weekly onboarding meetings, in a client's words thorough and easing the transition. Central management, MFA and encryption on, network brought to the security framework, monitoring live.",
         "receive": ["Weekly onboarding meetings", "Documented environment", "Monitoring on every device"]},
        {"label": "Manage and review", "when": "Ongoing", "summary": "24x7, and a review every quarter.", "title": "Watched around the clock, reviewed every quarter",
         "body": "Nexus monitors network, servers, workstations, cloud and security 24x7 and reviews the business every quarter with a technical assessment and NIST CSF reporting. Every year, the full assessment again.",
         "receive": ["Quarterly business review", "Annual technology and network assessment", "A roadmap that moves with the business"]}]}

FLEET = {"type": "fleet", "id": "fleet", "heading": "Everything the office runs on", "intro": "Generated product renders for the preview; Nexus's own equipment and partner imagery replace them.",
    "items": [
        {"title": "The network core", "band": "Network as a Service", "brands": "Fortinet, Cisco, Meraki, Aruba", "image": "assets/fleet/switch.png", "bullets": ["Flat monthly rate, everything included", "Same-day replacement, guaranteed"], "href": "services/networking.html"},
        {"title": "Wi-Fi that reaches", "band": "Networking", "brands": "Meraki, Aruba", "image": "assets/fleet/ap.png", "bullets": ["Heat-mapped design", "Guest, staff and device networks kept apart"], "href": "services/networking.html"},
        {"title": "Meeting rooms", "band": "Nexus Collab", "brands": "Zoom and Teams rooms", "image": "assets/fleet/collab.png", "bullets": ["One-touch join", "Fixed monthly fee with refresh"], "href": "services/meeting-spaces.html"},
        {"title": "Cameras and doors", "band": "Site Intelligence Platform", "brands": "AI-enabled cameras and readers", "image": "assets/fleet/site.png", "bullets": ["Mobile credentials", "Installed in two to three weeks"], "href": "services/site-intelligence.html"},
        {"title": "The edge", "band": "Cybersecurity", "brands": "Fortinet, Huntress", "image": "assets/fleet/firewall.png", "bullets": ["Least privilege by design", "SIEM and SOC monitoring"], "href": "services/cybersecurity.html"},
        {"title": "Screens that speak", "band": "Nexus Engage", "brands": "Commercial displays and players", "image": "assets/fleet/signage.png", "bullets": ["Central control", "Multi-site rollout"], "href": "services/digital-signage.html"}]}

SEAL = {"type": "seal", "id": "seal", "eyebrow": "What every Nexus client gets", "heading": "Not adjectives. Commitments you can check.",
    "intro": "Each line is published on nexusnt.com or written into a Nexus agreement today.",
    "items": [["15 min", "First-call resolution in 15 minutes", "The published target, staffed with experienced engineers rather than a scripted help desk."],
              ["24x7", "Monitoring and analysis around the clock", "Network, servers, workstations, cloud and security, so issues are prevented before they arise."],
              ["Same day", "Same-day replacement on Network as a Service", "Guaranteed. Manufacturers can take weeks."],
              ["US", "US-based engineers", "A dedicated team of experienced engineers in the United States."],
              ["NIST", "Aligned to the NIST Cybersecurity Framework", "Customized NIST CSF reports in every quarterly business review."],
              ["Fixed", "Fixed-fee projects", "No change orders, and a guarantee to make it work within the budget."],
              ["QBR", "A quarterly business review", "A regular technical assessment, and a full technology and network assessment every year."],
              ["1 day", "A reply within one business day", "Every enquiry on the contact page is answered within the same business day."]],
    "source": "Sources: nexusnt.com (home, managed services, networking, consultation and contact pages), September 2026."}

BEFORE_AFTER = {"type": "beforeafter", "id": "ba", "eyebrow": "Not another MSP", "heading": "Drag to see the difference between an MSP and a partner",
    "before": {"eyebrow": "Just another MSP", "title": "You are a ticket number", "body": "Scripted support, private-equity roll-ups, and the cheapest quote wins.",
               "items": ["A help desk reading a script", "Escalate, wait, escalate again", "The salesperson you never hear from again", "An owner you have never met", "Price cuts to win, corners cut to deliver", "Network today, someone else for the screens, the doors and the sound"]},
    "after": {"eyebrow": "Nexus", "title": "You are connected to the people", "body": "Founder-owned, selective, and accountable for everything that connects.",
              "items": ["Engineers on the first call, 15-minute resolution target", "Leadership accessible, escalations handled quickly, in a client's words", "The founder has visited clients' sites himself", "Not private-equity backed; a company that would rather serve fewer clients well", "We do not lose on price, and we do not discount to win", "Network, security, rooms, screens, doors, sound and cable from one team"]}}

HOTSPOTS = {"type": "hotspots", "id": "building", "eyebrow": "One core, every system attached", "heading": "Eight systems, one building, one partner", "intro": "Click a number. Everything a building runs on, and the Nexus page for each.",
    "image": "assets/office-iso-1600.jpg", "image_w": 1600, "image_h": 900, "alt": "An isometric illustration of an office floor with a network closet, a conference room, a lobby screen, desks and cameras, connected by green cable runs",
    "items": [
        {"x": 52, "y": 46, "k": "Network as a Service", "title": "The network closet", "body": "The core: switches, firewall and Wi-Fi controllers on a flat monthly rate, replaced the same day if anything fails.", "href": "services/networking.html", "label": "Networking"},
        {"x": 17, "y": 40, "k": "Nexus Collab", "title": "The conference room", "body": "One-touch join, monitored and updated in off hours.", "href": "services/meeting-spaces.html", "label": "Meeting spaces"},
        {"x": 45, "y": 76, "k": "Nexus Engage", "title": "The lobby screen", "body": "On-brand content, scheduled centrally across every location.", "href": "services/digital-signage.html", "label": "Digital signage"},
        {"x": 91, "y": 44, "k": "Site Intelligence", "title": "The door and the camera", "body": "Mobile credentials, visitor access and video on one screen.", "href": "services/site-intelligence.html", "label": "Site Intelligence Platform"},
        {"x": 69, "y": 40, "k": "Managed IT", "title": "The desks", "body": "Workstations centrally managed, built the same day, encrypted and monitored.", "href": "services/managed-it.html", "label": "Managed IT"},
        {"x": 52, "y": 12, "k": "Cybersecurity", "title": "Every layer, edge to endpoint", "body": "Least privilege, segmentation, SIEM and SOC monitoring, and people trained as the endpoints they are.", "href": "services/cybersecurity.html", "label": "Cybersecurity"},
        {"x": 40, "y": 22, "k": "Cabling, audio, cellular", "title": "In the walls and ceiling", "body": "Structured cabling, paging and background audio, and cell signal in every corner.", "href": "services/building-systems.html", "label": "Building systems"},
        {"x": 24, "y": 56, "k": "Virtual CIO", "title": "The leadership table", "body": "Strategy, budgeting and fixed-fee projects from an engineer who sits with your leadership.", "href": "services/consultation-projects.html", "label": "Consultation and projects"}]}

HERO_LAYERED = {"type": "hero-layered", "id": "hero", "eyebrow": "Raleigh-Durham. Founder-owned. Not another MSP.",
    "heading": "Secure, reliable, performant networks, from people you are <em>actually connected to</em>.",
    "subhead": "Nexus is the connection point: the network in the walls, the security around it, the rooms, screens and doors that run on it, and the engineers who answer on the first call. One partner for growing businesses in the Triangle and the Carolinas.",
    "primary": {"label": "Start the conversation", "href": "contact.html"}, "secondary": {"label": "See how Nexus is different", "href": "why-nexus.html"},
    "image": "assets/hero-plate-2100.jpg", "image_w": 2100, "image_h": 900,
    **({"model": SWITCH_MODEL, "poster": "assets/fleet/switch.png", "model_alt": "A network switch stack with a firewall, rotating. Drag to turn it."} if SWITCH_MODEL else {}),
    "stats": [["15", "Minutes to first-call resolution, the target"], ["24x7", "Monitoring and analysis"], ["5", "Star client satisfaction rating"], ["1", "Partner for eight systems"]],
    "card_a": {"eyebrow": "Start here", "title": "A conversation, not a pitch", "body": "Tell us how your business runs. We will say honestly whether we are the right fit.", "items": ["Engineers, not salespeople", "An assessment you keep either way", "Fixed fees, no change orders"], "href": "contact.html", "label": "Start the conversation"},
    "card_b": {"eyebrow": "Already a client?", "title": "Support", "body": "Real engineers, first call.", "links": [["Request support", "contact.html#form"], ["Email support", f"mailto:{EMAIL}"], ["Call " + PHONE, PHONE_HREF], ["Client resources", "why-nexus.html"]]},
    "note": "Preview photography, renders and the 3D device are generated and labelled as such; Nexus's own imagery replaces them."}

STORY3D = {"type": "story3d", "id": "device", "alt": False, "eyebrow": "Inside the closet", "heading": "What secure, reliable and performant actually looks like",
    "intro": "Scroll, and the stack turns to the part being described. A generated stand-in for the preview; Nexus's partner equipment replaces it.",
    "poster": "assets/fleet/switch.png", "alt": "A network switch stack with a firewall that turns as you scroll", "hint": "Drag to turn",
    "cta": {"label": "Network as a Service", "href": "services/networking.html"},
    "steps": [
        {"k": "The core", "title": "Switching designed for least privilege", "orbit": "30deg 70deg 100%", "body": "Device types live on separate segments, and nothing talks to anything unless explicitly allowed. That is how one compromised device stays one compromised device.", "points": ["Microsegmentation", "Layered isolation", "Current-generation equipment on a refresh cycle"]},
        {"k": "The edge", "title": "A firewall that inspects between segments, not just at the door", "orbit": "-50deg 75deg 104%", "body": "Anti-malware and intrusion prevention run on traffic between networks, and logs feed threat hunting and the SOC.", "points": ["Inter-network firewall", "Log ingestion for threat hunting", "SIEM and SOC monitoring"]},
        {"k": "The cable", "title": "Labelled, tested, documented", "orbit": "0deg 45deg 110%", "body": "Structured cabling from the same team that designed the network. Every run recorded, so the next change is quick and nobody guesses.", "points": ["Structured cabling and low voltage", "As-built documentation", "Clean closet"]},
        {"k": "The guarantee", "title": "If it fails, it is replaced the same day", "orbit": "200deg 78deg 108%", "body": "Monitored 24/7/365, and if a component stops working, Nexus guarantees same-day replacement where manufacturers can take weeks.", "points": ["24/7/365 monitoring", "Same-day replacement", "Everything in one flat monthly rate"]}],
    **({"model": SWITCH_MODEL} if SWITCH_MODEL else {})}


def build():
    brand = {
        "accent": "#8ABB2A", "ink_secondary": "#0B1B22", "chrome": "dark", "chrome_bg": "#0B1B22",
        "logo": "assets/nexus-logo.svg", "logo_alt": "Nexus Network Technologies", "logo_w": 188, "logo_h": 45,
        "logo_note": "Current vector mark, green gradient. Works on light and dark grounds. Keep or evolve is an open decision (7/21 notes).",
        "phone": PHONE, "phone_href": PHONE_HREF, "email": EMAIL,
        "utility": [{"label": "Request support", "href": "contact.html#form"}, {"label": "Email support", "href": f"mailto:{EMAIL}"}, {"label": "Why Nexus", "href": "why-nexus.html"}],
        "cta": {"label": "Start the conversation", "href": "contact.html"},
        "sticky": {"primary": "Start the conversation", "primary_href": "contact.html", "secondary": "Call Nexus", "secondary_href": PHONE_HREF},
        "launcher": {"label": "Already a client?", "eyebrow": "Support", "title": "What do you need today?", "links": [["Request support", "contact.html#form"], ["Email support", f"mailto:{EMAIL}"], ["Call " + PHONE, PHONE_HREF], ["Book a Collab demo", "services/meeting-spaces.html"]], "note": "An engineer replies. Monday to Friday, 8am to 5pm, and monitoring never stops.", "phone": PHONE, "phone_href": PHONE_HREF},
        "social": {"linkedin": "https://www.linkedin.com/company/nexus-network-technologies/"},
        "tagline": "Service that surprises you. Security that will not. Founder-owned in Raleigh-Durham, serving growing businesses across the Triangle and the Carolinas.",
        "footer_columns": [
            {"title": "Services", "links": [[s[1], f"services/{s[0]}.html"] for s in SERVICES] + [["All services", "services.html"]]},
            {"title": "Industries", "links": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES]},
            {"title": "Clients", "links": [["Request support", "contact.html#form"], ["Email support", f"mailto:{EMAIL}"], ["What clients say", "voices.html"], ["Results", "why-nexus.html#results"]]},
            {"title": "Company", "links": [["Why Nexus", "why-nexus.html"], ["About", "about.html"], ["Location", "location.html"], ["FAQ", "faq.html"], ["Contact", "contact.html"]]},
        ],
        "legal": [["Privacy", "https://www.nexusnt.com/"]],
    }
    schema = {"org_name": "Nexus Network Technologies", "org_url": "https://www.nexusnt.com", "org_logo": "https://www.nexusnt.com/wp-content/uploads/2022/11/nexus-logo.svg",
              "org_description": "Founder-owned managed IT, network as a service, cybersecurity, meeting room, site intelligence and virtual CIO partner based in Morrisville, North Carolina, serving growing businesses across the Triangle and the Carolinas.",
              "sameAs": ["https://www.linkedin.com/company/nexus-networking-technologies/"], "telephone": "+1-919-897-2700",
              "short_name": "Nexus", "title_city": "Raleigh-Durham", "cities": ["Raleigh", "Durham", "Cary", "Morrisville", "Triangle", "Chapel Hill", "North Carolina", "NC", "Carolinas"],
              "area_served": [{"@type": "City", "name": "Raleigh"}, {"@type": "City", "name": "Durham"}, {"@type": "City", "name": "Cary"}, {"@type": "City", "name": "Morrisville"}, {"@type": "State", "name": "North Carolina"}],
              "meta_tail": "Nexus Network Technologies, founder-owned in Morrisville, serving the Triangle and the Carolinas.",
              "local": [{"slug": "morrisville", "name": "Nexus Network Technologies", "street": ADDRESS[0], "city": "Morrisville", "region": "NC", "postal": "27560", "telephone": "+1-919-897-2700",
                         "openingHours": "Mo-Fr 08:00-17:00", "lat": 35.824, "lon": -78.826}]}
    nav = [
        {"label": "Services", "href": "services.html", "mega": True,
         "groups": [{"title": "Run", "items": [[s[1], f"services/{s[0]}.html"] for s in SERVICES[:3]]},
                    {"title": "Spaces", "items": [[s[1], f"services/{s[0]}.html"] for s in SERVICES[3:5]] + [[SERVICES[6][1], f"services/{SERVICES[6][0]}.html"]]},
                    {"title": "Build and plan", "items": [[SERVICES[5][1], f"services/{SERVICES[5][0]}.html"], [SERVICES[7][1], f"services/{SERVICES[7][0]}.html"], ["All services", "services.html"]]}],
         "featured": {"eyebrow": "Not sure where to start?", "title": "Start with a conversation", "body": "Not a pitch. Nexus asks how your business runs and says honestly whether it is the right fit.", "href": "contact.html", "label": "Start the conversation"}},
        {"label": "Industries", "href": "industries.html", "children": [[i[1], f"industries/{i[0]}.html"] for i in INDUSTRIES] + [["All industries", "industries.html"]]},
        {"label": "Why Nexus", "href": "why-nexus.html", "children": [["How we are different", "why-nexus.html"], ["Results", "why-nexus.html#results"], ["What clients say", "voices.html"], ["Security approach", "services/cybersecurity.html"]]},
        {"label": "About", "href": "about.html", "children": [["About Nexus", "about.html"], ["Location", "location.html"], ["FAQ", "faq.html"], ["Contact", "contact.html"]]},
    ]

    pages = []
    services_list = [[s[1], s[3], f"services/{s[0]}.html"] for s in SERVICES]
    # ---------------- home
    pages.append({"file": "index.html", "title": "Nexus Network Technologies | Managed IT, networks, security and meeting rooms, Raleigh-Durham",
                  "compose": {
                      "clean": ["hero-light", "partners", "seal", "wheel", "is-this-you", "flow", "results", "map", "voices", "faq", "contact"],
                      "showcase": ["hero", "partners", "wheel", "fleet", "ba", "flow", "building", "device", "proof", "results", "map", "voices", "faq", "contact"],
                      "press": ["hero-light", "story", "services", "seal", "voices", "flow", "results", "map", "faq", "contact"]},
                  "description": "Founder-owned in Raleigh-Durham. Managed IT with 15-minute first-call resolution, Network as a Service with same-day replacement, layered cybersecurity, meeting rooms and site intelligence for growing businesses in the Triangle and the Carolinas.",
                  "sections": [
        {"type": "hero", "id": "hero-light", "layout": "split", "eyebrow": "Raleigh-Durham. Founder-owned. Not another MSP.",
         "stats": [["15", "Minutes to first-call resolution"], ["24x7", "Monitoring"], ["5", "Star satisfaction rating"], ["8", "Systems, one partner"]],
         "ribbon": ["Founder-owned, not private-equity backed", "NIST Cybersecurity Framework aligned", "US-based engineers on the first call"],
         "variants": {"press": {"stats": None, "ribbon": ["Morrisville, North Carolina", "Founder-owned", "Service that surprises you. Security that will not."]}},
         "heading": "Secure, reliable, performant networks, from people you are <em>actually connected to</em>.",
         "subhead": "Nexus is the connection point: the network, the security, the rooms, screens and doors that run on it, and the engineers who answer on the first call. One partner for growing businesses in the Triangle and the Carolinas.",
         "primary": {"label": "Start the conversation", "href": "contact.html"}, "secondary": {"label": "See how Nexus is different", "href": "why-nexus.html"},
         "note": "Generated preview imagery, labelled as such", "image": "assets/rack-1200.jpg", "image_alt": "An engineer dressing green patch cables into a rack of switches", "image_w": 1200, "image_h": 800},
        HERO_LAYERED,
        {"type": "partners", "id": "partners", "caption": "Technology partners", "items": PARTNERS},
        SEAL,
        {"type": "wheel", "id": "wheel", "eyebrow": "One core, every system attached", "heading": "Everything a business runs on, from one accountable team", "intro": "Hover a segment. Eight lines, one partner, one point of accountability.", "items": WHEEL_ITEMS, "panel_eyebrow": "Hover a segment", "link_label": "See the service"},
        {"type": "checklist", "id": "is-this-you", "alt": True, "eyebrow": "Is this you?", "heading": "Six signs you have an MSP, not a partner", "intro": "Check what sounds familiar. Nobody is watching.",
         "items": ["You explain the problem to a help desk before anyone who can fix it hears it", "A ticket has been escalated more than once this month", "You have never met the owner of your IT company", "The network was bought once and nobody has patched the switches since", "A meeting started late because the room did not work", "Nobody can tell you who came through the side door on Saturday"],
         "messages": ["Check what sounds familiar.", "One is normal.", "Two is worth a conversation.", "Three or more, and you are paying for an MSP and getting a ticket queue."], "cta_label": "Start the conversation", "cta_href": "contact.html"},
        {"type": "services", "id": "services", "heading": "Everything a business runs on, from one accountable team", "intro": "Most providers sell one thing. Nexus connects the whole building and keeps it running, so you have one relationship instead of six vendors pointing at each other.", "items": services_list},
        FLEET, BEFORE_AFTER, FLOW_ENGAGEMENT, HOTSPOTS, STORY3D,
        {"type": "proof", "id": "proof", "alt": True, "eyebrow": "The published target", "value": "15", "text": "Minutes to first-call resolution. Because experienced engineers answer the first call, issues are resolved quickly rather than escalated.", "source": "Published on nexusnt.com alongside a 5-star client satisfaction rating and 24x7 monitoring. Ask Nexus for the current numbers."},
        {"type": "cards", "id": "results", "alt": True, "eyebrow": "Results", "heading": "Four engagements, in Nexus's own published words", "intro": "Client, challenge, what Nexus did, and what changed.", "items": [[c[0], f"{c[1]} Nexus delivered {c[2][0].lower() + c[2][1:]}. {c[3]}"] for c in CASES]},
        {"type": "map", "id": "map", "heading": "One office in Morrisville, one team across the Triangle and the Carolinas", "intro": "Based in Raleigh-Durham and working on site and remotely with clients within about 75 miles, and further for clients who ask.", "ring": 75,
         "items": [{"name": "Morrisville", "lon": -78.826, "lat": 35.824, "href": "location.html", "sub": "630 Davis Drive, Suite 220", "hq": True, "label_dx": -80, "label_dy": -12}]},
        {"type": "testimonials", "id": "voices", "alt": True, "layout": "feature", "eyebrow": "What clients say", "heading": "Survey answers from people who use Nexus every day", "items": [VOICES[0][:3], VOICES[2][:3], VOICES[5][:3], VOICES[3][:3]]},
        {"type": "timeline", "id": "story", "eyebrow": "The story", "heading": "From the network company to the one partner who connects it all", "items": [["Founded", "Mike founds Nexus", "Amid the rapid expansion of MSPs, to give companies a partner that makes customer advocacy a priority."], ["Today", "Eight systems, one team", "Managed IT, networks, security, meeting rooms, site intelligence, signage, audio, cabling and a virtual CIO, from Morrisville."], ["Still", "Founder-owned", "Not private-equity backed, and choosing to serve fewer clients well."]]},
        {"type": "faq", "id": "faq", "alt": True, "heading": "Questions we get on the first call", "items": [
            ["Are you just another MSP?", "No, and that is the point. Founder-owned, not private-equity backed, engineers on the first call with a 15-minute resolution target, and one team for the network, security, rooms, screens, doors and cable. Nexus would rather serve fewer clients well than take anybody."],
            ["Where do you work?", "From Morrisville, across the Triangle and the Carolinas, on site and remotely. Clients within about 75 miles of Raleigh-Durham are the home territory; ask if you are further out."],
            ["Can we start small?", "Yes. Many clients start with managed IT or the network and add rooms, security and doors later. Co-managed alongside your own IT team works too."],
            ["How do you price?", "Ongoing services are flat monthly rates with everything included. Projects are fixed fees with no change orders. Nexus does not discount to win."],
            ["How fast is support?", "The published target is first-call resolution in 15 minutes, from US-based engineers, with monitoring around the clock. Enquiries are answered within one business day."]]},
        {"type": "contact", "id": "contact", "heading": "Start the conversation", "body": "Tell us how your business runs and what IT has been like. Nexus asks questions, not sales questions, and says honestly whether it is the right fit.", "options": ["Managed IT and support", "Network as a Service", "Cybersecurity", "Meeting spaces", "Site Intelligence Platform", "Virtual CIO or a project", "I am a client and need support"], "submit": "Start the conversation", "note": "A Nexus engineer or Shane replies within one business day."},
    ]})
    # ---------------- services index
    pages.append({"file": "services.html", "title": "Services | Nexus Network Technologies", "description": "Managed IT, Network as a Service, cybersecurity, Nexus Collab meeting rooms, the Site Intelligence Platform, virtual CIO and projects, digital signage, cabling, audio and cellular. One accountable team in Raleigh-Durham.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Services", "heading": "Eight systems a building runs on. <em>One point of accountability.</em>", "subhead": "Every line below is delivered, secured and supported by the same team, so nothing falls between vendors.", "primary": {"label": "Start the conversation", "href": "contact.html"}},
        {"type": "wheel", "id": "wheel", "eyebrow": "The brand house", "heading": "Hover a segment", "intro": "Each line has its own page.", "items": WHEEL_ITEMS, "panel_eyebrow": "Hover a segment", "link_label": "See the service"},
        dict(HOTSPOTS, alt=True),
        {"type": "resources", "heading": "The eight lines", "intro": "What changes, what is included, and the questions people ask.", "items": [[s[2], s[1], s[3], f"See {s[1]}", f"services/{s[0]}.html"] for s in SERVICES]},
        {"type": "testimonials", "alt": True, "heading": "In clients' words", "items": [VOICES[0][:3], VOICES[8][:3], VOICES[9][:3]]},
        LEADFORM]})
    for s in SERVICES:
        pages.append(service_page(*s))
    # ---------------- industries
    pages.append({"file": "industries.html", "title": "Industries | Nexus Network Technologies", "description": "Life sciences, professional services, manufacturing and warehousing, and growing businesses of every kind. A just-right option for each.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Industries", "heading": "From life sciences to professional services, a <em>just-right</em> option.", "subhead": "Regulated labs, billable-hour firms, always-on floors, and organizations that fit no category. Nexus meets each where it is.", "primary": {"label": "Start the conversation", "href": "contact.html"}},
        {"type": "resources", "heading": "Who Nexus serves", "intro": "Each has its own page.", "items": [[i[1], i[1], i[3], f"IT for {i[1].lower()}", f"industries/{i[0]}.html"] for i in INDUSTRIES]},
        {"type": "partners", "caption": "Compliance frameworks Nexus works within", "items": COMPLIANCE},
        {"type": "testimonials", "alt": True, "heading": "From clients across these industries", "items": [VOICES[4][:3], VOICES[2][:3], VOICES[11][:3]]},
        LEADFORM]})
    for i in INDUSTRIES:
        pages.append(industry_page(*i))
    # ---------------- why nexus
    pages.append({"file": "why-nexus.html", "title": "Why Nexus | How we are different", "description": "Individual engineers, not a scripted help desk. First-call resolution in 15 minutes. A 5-star satisfaction rating. Networks that meet the NIST framework from day one. Four published results.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "How we are different", "heading": "We built the company we <em>could not find anywhere else</em>.", "subhead": "Customer advocacy and real support that does not disrupt your business. Here is what separates Nexus from typical managed services, and four engagements that show it.", "primary": {"label": "Start the conversation", "href": "contact.html"}},
        SEAL,
        BEFORE_AFTER,
        {"type": "cards", "id": "results", "alt": True, "eyebrow": "Results", "heading": "Four engagements, in Nexus's own published words", "intro": "Client, challenge, what Nexus did, and what changed.", "items": [[c[0], f"{c[1]} Nexus delivered {c[2][0].lower() + c[2][1:]}. {c[3]}"] for c in CASES]},
        {"type": "casestudy", "eyebrow": "One in full", "heading": "A regulated facility, launched audit-ready", "quote": VOICES[4][0] if False else "From initial start-up through ongoing operations, we have had an excellent experience with Nexus. They have been instrumental in assisting us with ensuring operational compliance, consistently demonstrating a high level of understanding of the regulated space.", "attribution": "Director of IT, regulated materials storage provider", "metrics": [["Launch", "Day one", "Compliant network on move-in"], ["Cadence", "QBR", "Ongoing reporting established"], ["Reach", "UK", "Expansion aligned"]]},
        {"type": "testimonials", "heading": "More from clients", "items": [VOICES[6][:3], VOICES[7][:3], VOICES[10][:3]]},
        LEADFORM]})
    # ---------------- voices
    pages.append({"file": "voices.html", "title": "What clients say | Nexus Network Technologies", "description": "Survey responses from clients who submitted support tickets and were asked what delighted them. Roles and organization types, in their own words.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "What clients say", "heading": "When clients can rely on their IT, <em>it is a win</em>.", "subhead": "These are survey responses from clients who submitted support tickets and were asked one question: was there anything in particular we did that delighted you?", "primary": {"label": "Start the conversation", "href": "contact.html"}},
        {"type": "testimonials", "heading": "In their words", "items": [v[:3] for v in VOICES]},
        LEADFORM]})
    # ---------------- about
    pages.append({"file": "about.html", "title": "About Nexus | Founder-owned IT engineers in Raleigh-Durham", "description": "A collective of IT engineers and consultants in Raleigh-Durham who believe calling IT should not be met with a heavy sigh. Founded by Mike Schwarzbauer. Founder-owned, not private-equity backed.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "About Nexus", "heading": "A collective of engineers who believe <em>calling IT should not be met with a sigh</em>.", "subhead": "Based in Raleigh-Durham, working on site and remotely, translating business problems into technical solutions and building relationships for the long term. Founder-owned, and staying that way.", "primary": {"label": "Start the conversation", "href": "contact.html"}},
        {"type": "stats", "alt": True, "items": [["15", "Minutes to first-call resolution, the target"], ["24x7", "Monitoring, 365 days"], ["5", "Star client satisfaction rating"], ["1", "Owner, who still visits clients"]]},
        {"type": "timeline", "eyebrow": "The story", "heading": "From the network company to the one partner who connects it all", "items": [["Founded", "Mike founds Nexus", "Amid the rapid expansion of managed services, to give companies a partner that makes customer advocacy a priority."], ["Grown", "From networks to the whole building", "Managed IT, security, Collab meeting rooms, the Site Intelligence Platform and a virtual CIO practice, each added because clients asked."], ["Today", "Founder-owned, selective", "Not private-equity backed. A company that would rather have fewer great-fit clients than many it cannot serve well."]]},
        {"type": "leadership", "id": "team", "heading": "The people", "intro": "Three of the people you will actually talk to.", "people": [[t[0], t[1]] for t in TEAM], "orgs_intro": "Technology partners", "orgs": PARTNERS},
        {"type": "values", "alt": True, "eyebrow": "How Nexus describes itself", "heading": "Approachable. Intentional. Protective.", "items": [["Approachable", "The word the team chose for itself, and the reason a client called the team approachable and knowledgeable and willing to take on any challenge."], ["Intentional", "Methodical and proactive, in a client's words. Plans laid out before anything changes."], ["Protective", "Of its people, its clients, its brand and its vendor relationships. Security first, and no discounting to win."], ["Growth-minded", "A partner of the client's company, there to help it grow, with a virtual CIO when strategy is what is needed."]]},
        {"type": "casestudy", "eyebrow": "In the founder's words", "heading": "Proactive, so problems do not happen in the first place", "quote": "At Nexus, we believe in taking proactive measures to prevent issues from happening in the first place. This, combined with our unique vision to be an extension of our client's organization, allows our clients to experience peace of mind.", "attribution": "Mike Schwarzbauer, Founder and President", "metrics": [["Support", "US", "Based engineers"], ["Target", "15 min", "First-call resolution"], ["Watch", "24x7", "Monitoring"]]},
        {"type": "cards", "alt": True, "heading": "Industries we know best", "items": [[i[1], i[3]] for i in INDUSTRIES]},
        {"type": "cta", "heading": "Talk to an engineer, not a salesperson", "subhead": "Nexus asks how your business runs, and says honestly whether it is the right fit.", "primary": {"label": "Start the conversation", "href": "contact.html"}},
    ]})
    # ---------------- location
    pages.append({"file": "location.html", "title": "Location | Nexus Network Technologies, Morrisville, NC", "description": "630 Davis Drive, Suite 220, Morrisville, NC 27560. (919) 897-2700. Monday to Friday, 8am to 5pm. Serving the Triangle and the Carolinas on site and remotely.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Location", "heading": "Morrisville, in the middle of <em>the Triangle</em>.", "subhead": "Between Raleigh, Durham and Chapel Hill, with demonstration meeting and huddle rooms you can visit. Engineers work on site across the region and remotely.", "primary": {"label": "Start the conversation", "href": "contact.html"}},
        {"type": "locations", "detailed": True, "heading": "Where we are", "intro": HOURS + ". Monitoring runs around the clock.", "items": [["Nexus Network Technologies", ADDRESS[0], ADDRESS[1], PHONE, PHONE_HREF]]},
        {"type": "map", "heading": "Where Nexus works", "intro": "Clients within about 75 miles of Raleigh-Durham are the home territory. Further afield, ask.", "ring": 75, "items": [{"name": "Morrisville", "lon": -78.826, "lat": 35.824, "href": "location.html", "sub": ADDRESS[0], "hq": True, "label_dx": -80, "label_dy": -12}]},
        {"type": "faq", "heading": "Coverage questions", "items": [["Do you cover my town?", "The Triangle is home. Nexus serves clients across the Carolinas and has supported multi-site clients further out, so ask; the answer will be honest either way."], ["Can we visit?", "Yes. Nexus has demonstration meeting and huddle rooms set up in the Morrisville office. Contact Shane Bull to schedule."], ["Is support remote or on site?", "Both. Monitoring and most support are remote; engineers come on site when it matters, and the founder has been known to visit himself."]]},
        LEADFORM]})
    # ---------------- faq
    pages.append({"file": "faq.html", "title": "FAQ | Nexus Network Technologies", "description": "Answers to the questions people ask Nexus first: fit, pricing, response times, compliance, moving offices, starting small.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "FAQ", "heading": "Questions, <em>answered plainly</em>.", "subhead": "If yours is not here, ask. A person replies within one business day."},
        {"type": "faq", "heading": "Working with Nexus", "items": [
            ["How is Nexus different from a typical MSP?", "Short hold times, experienced engineers who fix it the first time, a network stack that follows a security framework, and a proactive approach that ends the break-fix cycle. Founder-owned and not private-equity backed."],
            ["How do you price?", "Ongoing services are flat monthly rates with everything included. Projects are fixed fees with no change orders and a guarantee to work within the budget. Network as a Service can be paid monthly, annually or five years upfront, with discounts on the longer terms."],
            ["How fast is support?", "The published target is first-call resolution in 15 minutes from US-based engineers. Monitoring runs 24x7, 365 days a year."],
            ["Do you handle compliance?", "Yes. HIPAA, PCI, FDA 21 CFR Part 11 and GMP, aligned to the NIST Cybersecurity Framework, with the paperwork provided and NIST reports in every quarterly review."],
            ["We are moving offices.", "Nexus coordinates carriers and internet providers, designs the network for the new space, and can add cabling, meeting rooms, signage and access control so everything is ready on move-in day."],
            ["Can we start with one thing?", "Yes. Many clients start with managed IT or the network and grow into the rest, or run co-managed alongside their own IT team."],
            ["Are you the right fit for us?", "Maybe not, and Nexus will say so. It would rather serve fewer great-fit clients well than take anybody."]]},
        LEADFORM]})
    # ---------------- contact
    pages.append({"file": "contact.html", "title": "Contact | Nexus Network Technologies", "description": "Start a conversation with Nexus. 630 Davis Drive, Suite 220, Morrisville, NC 27560. (919) 897-2700. support@nexusnt.com. A reply within one business day.",
                  "sections": [
        {"type": "hero", "layout": "centered", "eyebrow": "Contact", "heading": "Start the conversation, or <em>just call</em>.", "subhead": "Tell us how your business runs. Nexus asks questions, not sales questions, and replies within one business day."},
        {"type": "contact", "id": "form", "heading": "Start the conversation", "body": "Choose what you are thinking about, or tell us you are a client who needs support.", "options": ["Managed IT and support", "Network as a Service", "Cybersecurity", "Meeting spaces (Nexus Collab)", "Site Intelligence Platform", "Virtual CIO or a project", "Digital signage, cabling, audio or cellular", "I am a client and need support"], "submit": "Start the conversation", "note": "A Nexus engineer or Shane replies within one business day. Existing clients: support@nexusnt.com reaches the team directly."},
        {"type": "locations", "alt": True, "heading": "Or come and see the rooms", "intro": "Demonstration meeting and huddle rooms are set up in the office. " + HOURS + ".", "items": [["Nexus Network Technologies", ADDRESS[0], ADDRESS[1], PHONE, PHONE_HREF]]},
    ]})

    pitch = {
        "qbs_contact": {"name": "Shawn Peterson", "email": "shawn@thequantumleap.business", "phone": "(712) 389-4639"},
        "prepared_for": "Mike Schwarzbauer, Shane Bull and Lin Cashwell, Nexus Network Technologies",
        "heard_intro": "Everything here comes from the July 21 call, your current site and the proposal you have already seen. Tell us where it is wrong; your words outrank ours.",
        "heard": ["Nexus is the connection: between technologies, and between you and the client. A bond, a win-win, not a transaction. Every page is written from that idea.",
                  "Not private-equity backed, founder-owned for about thirty years, and selective on purpose. The site says so in the first screen.",
                  "Mike's three words are secure, reliable and performant, at an enterprise level. They are the headline, and the 3D network closet on the Showcase home shows what they mean.",
                  "Approachable, intentional, protective, grounded. The voice is a conversation, never sales words. No exclamation marks anywhere.",
                  "Strategy over visuals. The plan and the proof come first on this hub; the three directions are a menu, not the pitch."],
        "found": ["nexusnt.com earns about 22 organic visits a month on 53 ranking keywords (Semrush, 8 September 2026). The market is not finding Nexus through search at all; almost every visitor already knows the name.",
                  "There is no blog and no page that answers a buyer's question. The site describes services well but never appears when a Triangle business asks how to choose an IT provider.",
                  "The testimonials page is the strongest asset on the site: sixteen detailed quotes with roles and organization types, updated in June 2026. It is buried two levels deep. The preview puts those voices on every page.",
                  "The contact forms are already HubSpot forms, so the preview's forms wire to the CRM you have. The site itself is WordPress with a cookie banner and a page-load overlay.",
                  "The AV as-a-Service page blocks pinch-zoom on phones (maximum-scale set to 1), which fails WCAG 1.4.4.",
                  "Digital signage, building audio, cellular and structured cabling appear in the proposal's brand house but not on the live site. They are built here as pages and flagged under To confirm."],
        "pick_reasons": [["Mike decides on feel, and the feeling has to be enterprise-level", "Showcase is the one that looks like the networks Nexus builds: a dark, layered hero with a live network of connection points, the switch stack turning as you read what secure, reliable and performant mean."],
                         ["The name is the idea", "The network canvas behind the hero draws connection points and lines. It is a literal picture of Nexus, and it is the only direction where the brand idea is visible before a word is read."],
                         ["Proof over adjectives", "The seal, the before/after, the process chart and the published results carry the whole argument. Showcase gives them the most room."]],
        "pick_change": "Showcase's warmth comes from the imagery and motion, not the type. If the room wants the Connective's warmer, more human feel, we would keep Showcase's structure and swap in Press's serif for headings, which is a one-line change.",
        "alternatives": [["Quantum Clean", "If enterprise means restraint: white ground, humanist sans, hairline cards, the proof doing all the talking. The fastest and quietest of the three."],
                         ["Quantum Press", "The Connective as an editorial site: warm paper, a serif, founder story high on the page. The most human of the three and the least like any MSP in the Carolinas."]],
        "plan": [["Before anything", "Eight buyer conversations from your client list, at our cost, findings delivered in person within two weeks. If the market already sees Nexus as a full-stack partner, we say so and stop."],
                 ["Week 1", "Choose a direction. Confirm the items under To confirm. Decide keep or evolve on the logo."],
                 ["Weeks 2 to 3", "Copy from Mike, Shane and Lin in your words, and the interview findings written into the pages. Photography of the team, the office and the demonstration rooms."],
                 ["Weeks 3 to 5", "Build in your HubSpot, forms to named people, every redirect tested."],
                 ["Week 6", "QA on the same 110-check gate this preview passed, then launch. Month one after launch: the service-mix email to your existing base, where the first return comes from."]],
        "search": {"heading": "Where Nexus stands in search today, and what changes", "intro": "Measured before we touched anything, so the work can be judged against it.", "as_of": "Semrush and live HTML, 8 September 2026",
                   "today_stats": [["22", "Organic visits a month"], ["53", "Keywords ranking"], ["0", "Pages answering a buyer's question"], ["16", "Client quotes, two levels deep"]],
                   "today": ["The market cannot find Nexus. About 22 visits a month from search, on 53 keywords, almost all of them the company name.",
                             "No blog, no FAQ page, no page built around a question a Triangle buyer types: managed IT Raleigh, IT support Durham, network as a service, conference room AV Raleigh.",
                             "The strongest content on the site, sixteen client quotes with roles and industries, sits at how-were-different/what-our-clients-are-saying, two clicks from anywhere.",
                             "One Organization record in schema, no LocalBusiness record tying Nexus to Morrisville and the Triangle for search and AI assistants.",
                             "The AV page blocks pinch-zoom; the site runs a cookie banner and a page-load overlay on every visit."],
                   "after": ["Twenty-three pages, each built around one thing a buyer asks, with titles that name the place: Managed IT and Support, Raleigh-Durham; Network as a Service in the Triangle.",
                             "Client voices on every service and industry page, with a dedicated page for all sixteen, so the proof is one click from anywhere.",
                             "LocalBusiness and Organization markup, FAQ markup on every FAQ, BreadcrumbList on every nested page.",
                             "A FAQ page and eight service FAQs written the way people ask AI assistants, so Nexus is the cited answer rather than absent.",
                             "Forms to HubSpot with a named owner, no cookie banner theatre, no overlay, pinch-zoom allowed.",
                             "A blog is deliberately not part of the launch scope; the interview findings decide what gets written first."],
                   "keep": [["/", "/", "Home: title rewritten with place and service"], ["/services/managed-services/", "/services/managed-it.html", "Redirect"], ["/services/network-as-a-service/", "/services/networking.html", "Redirect"], ["/services/av-as-a-service/", "/services/meeting-spaces.html", "Redirect"], ["/services/site-intelligence-platform/", "/services/site-intelligence.html", "Redirect"], ["/services/consultation-project-services/", "/services/consultation-projects.html", "Redirect"], ["/security-approach/", "/services/cybersecurity.html", "Redirect"], ["/how-were-different/what-our-clients-are-saying/", "/voices.html", "Redirect"], ["/industries-served/", "/industries.html", "Redirect, plus four industry pages"]],
                   "note": "Every URL that exists today gets a permanent redirect, tested individually at launch. Numbers from Semrush's US database; a market this small moves with a handful of rankings, so the six-month measure is the interview-led questions Nexus starts ranking for, not the total."},
        "confirm": ["The founding year. The notes say about thirty years founder-owned; the timeline says Founded without a year until you give us one.",
                    "Digital signage (Nexus Engage), building audio, cellular enhancement and structured cabling. They come from the proposal's brand house, not from nexusnt.com. Keep, rename or drop.",
                    "The service radius. The proposal FAQ says about 75 miles of Raleigh-Durham, expanding across the Carolinas and Virginia. The map ring uses 75 miles.",
                    "The 5-star satisfaction rating and the 15-minute first-call resolution target. Both are on nexusnt.com; tell us how they are measured so the preview can say so.",
                    "50+ businesses served appears in the proposal. It is not on these pages until confirmed.",
                    "The client quotes. All sixteen are public on your site; confirm each organization is happy to be quoted on the new site, and whether any will go on the record by name.",
                    "The logo: keep, or evolve. The preview uses the current mark unchanged.",
                    "Reply within an hour, any time of day, was said on the call. The site says one business day. We have printed one business day until you decide."],
        "footer": "Prepared for Mike Schwarzbauer, Shane Bull and Lin Cashwell. Nothing here is live or indexed. Every number and claim we could source comes from nexusnt.com, the July 21 call or public data. Items from the proposal alone are listed under To confirm. Photographs, renders and the 3D device are generated and labelled as such; your own imagery replaces them.",
    }
    _FAQ_EXTRA = {
        "about.html": ("Questions about Nexus", [
            ["Who founded Nexus?", "Mike Schwarzbauer, to give companies an IT partner that treats customer advocacy as the priority rather than ticket volume."],
            ["Is Nexus owned by private equity?", "No. Nexus is founder-owned and intends to stay that way, choosing to serve fewer clients well."],
            ["Where is Nexus based?", "630 Davis Drive, Suite 220, Morrisville, North Carolina, between Raleigh, Durham and Chapel Hill, with demonstration meeting rooms you can visit."]]),
        "contact.html": ("Before you write", [
            ["How do I reach support?", "Existing clients email support@nexusnt.com or call (919) 897-2700. New conversations start with the form on this page."],
            ["Where is the office?", "630 Davis Drive, Suite 220, Morrisville, NC 27560. Monday to Friday, 8am to 5pm."],
            ["When will someone reply?", "Within one business day, from a person at Nexus."]]),
        "industries.html": ("Industry questions", [
            ["Which industries does Nexus serve?", "Life sciences, professional services, manufacturing and warehousing, and growing businesses of every kind across the Triangle and the Carolinas."],
            ["Can you work in regulated environments?", "Yes. Life sciences clients rely on Nexus for audit-ready, compliant environments, and clients have credited the team's compliance knowledge in vendor and investor due diligence."],
            ["My industry is not listed.", "Ask. The industry pages show how the same eight services fit different operations; the first conversation fits them to yours."]]),
        "services.html": ("Questions about the services", [
            ["What does Nexus offer?", "Managed IT, Network as a Service, cybersecurity, Nexus Collab meeting rooms, the Site Intelligence Platform, virtual CIO and projects, digital signage, and cabling, audio and cellular."],
            ["Can we start with one service?", "Yes. Many clients begin with managed IT or the network and add the rooms, security and building systems as they grow."],
            ["Who answers when we call?", "An engineer who knows your environment, not a scripted help desk."]]),
        "voices.html": ("About these comments", [
            ["Where do these quotes come from?", "Survey responses from clients who submitted support tickets and were asked what delighted them, shown with their role and organization type."],
            ["Are they edited?", "Only for length. The words are the clients' own."],
            ["Can I speak to a reference?", "Yes. Ask, and Nexus will connect you with a client in a similar industry."]]),
        "why-nexus.html": ("How Nexus is different", [
            ["What does first-call resolution in 15 minutes mean?", "Most support requests are resolved on the first call by the engineer who answers, typically within fifteen minutes, rather than logged and queued."],
            ["What does founder-owned change for a client?", "Decisions are made by the people who serve you, with no private-equity growth targets pushing ticket volume over relationships."],
            ["How does Nexus approach security?", "Networks are built to the NIST framework from day one, with layered protection and monitoring included rather than sold as add-ons."]]),
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
    return {"client": "Nexus Network Technologies", "slug": "nexus-network-technologies", "domain_hint": "nexusnt.com",
            "brand": brand, "schema": schema, "nav": nav, "pages": pages, "pitch": pitch}


if __name__ == "__main__":
    data = build()
    with open(OUT, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}: {len(data['pages'])} pages")
