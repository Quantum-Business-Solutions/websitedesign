"""Pop pass 2: signature modules for the industry, company, support, partner, training, blog, portal, finder and audience pages.

Registered in preview.py as RENDER_POP2 (section renderers), POP2_CSS, POP2_JS and augment(content) (called once in main(),
right after the content file is loaded). augment() inserts or swaps sections on specific pages from facts already in the content
file, so no content file needs editing and every number or sentence shown traces back to text that is already on the site.

New section types
  p2-day        "A day in a <industry> building": vertical scroll timeline of 4 to 5 moments, each tied to a real DMP capability
  p2-outcomes   outcome checklist with big check icons beside a floating product image
  p2-cta        bold closing band with two actions
  p2-numbers    huge animated numerals (about)
  p2-leaders    leadership grid grouped by title, with a hover reveal of what each person leads (about)
  p2-quote      full-bleed photo with a pull quote (about)
  p2-router     "Who are you?" router that reveals the exact next step (contact)
  p2-chooser    "start here" chooser with live filter (support hub)
  p2-faqgrid    visible grid of the technical FAQ categories with answer counts (support hub)
  p2-partners   partner network (DMP at the centre) plus designed partner cards (partners hub)
  p2-board      calendar-style board of upcoming sessions (training hub)
  p2-toc        sticky table of contents (blog posts)
  p2-takeaways  dark "Key takeaways" callout (blog posts)
  p2-path       dealer path from application to first order (for dealers)
  p2-stack      spec-pack file stack (for specifiers)
  p2-flip       six questions as flip cards (for building owners)
  p2-platform   one panel, one app, four systems (why DMP)
and two wrappers: the dealer portal gains a labelled sample-data dashboard after sign-in, the product finder gains
"why this" chips and a compare tray.

Everything reads the theme variables, so Showcase, Clean and Press pick it up. Server HTML is complete without JS; JS only
upgrades. prefers-reduced-motion: no counting, drawing, floating or flipping animation. No external libraries.
Rules: no em or en dashes, nothing under 13px, 44px tap targets, no horizontal overflow at 390/768/1024/1440.
"""
from __future__ import annotations

import json
import re
from datetime import date

# ------------------------------------------------------------------------------------------------ icons

_IC = {
    "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M16 7l3 3M14 9l2 2"/>',
    "door": '<path d="M6 21V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v17M3 21h18"/><path d="M14.5 12.5h.01"/>',
    "lock": '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.500-3.200 7.800-8 9-4.800-1.200-8-4.500-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "alert": '<path d="M6 17V11a6 6 0 0 1 12 0v6l2 2H4z"/><path d="M10 21h4"/>',
    "phone": '<rect x="7" y="2.500" width="10" height="19" rx="2.500"/><path d="M11 18.500h2"/>',
    "doc": '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>',
    "signal": '<circle cx="12" cy="12" r="1.800"/><path d="M7.500 7.500a6.400 6.400 0 0 0 0 9M16.500 7.500a6.400 6.400 0 0 1 0 9M4.500 4.500a10.600 10.600 0 0 0 0 15M19.500 4.500a10.600 10.600 0 0 1 0 15"/>',
    "camera": '<path d="M3 7.500h13v9H3zM16 10.500l5-3v9l-5-3"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 12.500l9 5 9-5M3 16.500l9 5 9-5"/>',
    "keypad": '<rect x="5" y="3" width="14" height="18" rx="2.500"/><path d="M9 8h.01M12 8h.01M15 8h.01M9 12h.01M12 12h.01M15 12h.01M9 16h.01M12 16h.01M15 16h.01"/>',
    "check": '<path d="M5 12.500l4.500 4.500L19 7.500"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "users": '<circle cx="9" cy="8" r="3.500"/><path d="M2.500 20c0-3.600 2.900-6 6.500-6s6.500 2.400 6.500 6M16 5a3.400 3.400 0 0 1 0 6.600M18 14.500c2.300.7 3.500 2.700 3.500 5"/>',
    "server": '<rect x="3" y="4" width="18" height="6" rx="1.500"/><rect x="3" y="14" width="18" height="6" rx="1.500"/><path d="M7 7h.01M7 17h.01"/>',
    "report": '<path d="M5 3h14v18H5z"/><path d="M9 16v-3M12 16V8M15 16v-5"/>',
    "home": '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10M10 20v-6h4v6"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.500 3 14.500 0 18M12 3c-3 3.500-3 14.500 0 18"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "cart": '<path d="M3 4h2l2.400 11h10.200L20 8H6.200"/><circle cx="9" cy="19.500" r="1.400"/><circle cx="17" cy="19.500" r="1.400"/>',
    "cap": '<path d="M2.500 9L12 4.500 21.500 9 12 13.500z"/><path d="M6 11.500V16c0 1.400 2.700 3 6 3s6-1.600 6-3v-4.500"/>',
    "wrench": '<path d="M14.500 6.500a4 4 0 0 0 5 5L21 13l-8 8-3-3 8-8zM3 21l4-4"/>',
    "build": '<path d="M4 21V5l8-2v18M12 21V9l8 2v10M2 21h20"/><path d="M8 8h.01M8 12h.01M8 16h.01M16 14h.01M16 18h.01"/>',
    "pin": '<path d="M12 21s7-6.200 7-11.500A7 7 0 0 0 5 9.500C5 14.800 12 21 12 21z"/><circle cx="12" cy="9.500" r="2.500"/>',
    "plug": '<path d="M9 3v5M15 3v5M6 8h12v4a6 6 0 0 1-12 0zM12 18v3"/>',
    "megaphone": '<path d="M4 10v4h3l7 4V6L7 10z"/><path d="M17.500 9.500a4 4 0 0 1 0 5M19.500 7a7.500 7.500 0 0 1 0 10"/>',
    "quote": '<path d="M5 3h14v18l-3-2-2 2-2-2-2 2-2-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
    "star": '<path d="M12 3l2.700 5.600 6.100.9-4.400 4.300 1 6.100L12 17l-5.400 2.900 1-6.100L3.200 9.500l6.100-.9z"/>',
    "box": '<path d="M3 7.500l9-4.500 9 4.500v9l-9 4.500-9-4.500z"/><path d="M3 7.500l9 4.500 9-4.500M12 12v9"/>',
    "cal": '<rect x="3.500" y="5" width="17" height="15.500" rx="2"/><path d="M3.500 10h17M8 3v4M16 3v4"/>',
}


def ico(key, size=26, sw=1.7):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_IC.get(key, _IC["shield"])}</svg>')


def _slug(x):
    return re.sub(r"[^a-z0-9]+", "-", str(x).lower()).strip("-")


def _tel(n):
    return "tel:+1" + re.sub(r"\D", "", n)


def _head(E, s, center=False, tag="h2"):
    eb = f'<div class="q-eyebrow"{" style=justify-content:center" if center else ""}>{E(s["eyebrow"])}</div>' if s.get("eyebrow") else ""
    intro = f'<p class="q-lead p2-intro"{" style=margin-left:auto;margin-right:auto" if center else ""}>{E(s["intro"])}</p>' if s.get("intro") else ""
    h = f'<{tag} class="q-h2 p2-h2">{E(s["heading"])}</{tag}>' if s.get("heading") else ""
    return f'<div class="p2-head{" p2-center" if center else ""}">{eb}{h}{intro}</div>'


# ------------------------------------------------------------------------------------------------ industry data
# Each moment: (kicker, title, text, icon, optional link). Text is DMP's own wording from the industry page, its FAQ or its stat line.

IND_NOUN = {"commercial": "A day in a commercial building", "financial-institutions": "A day at a financial institution", "retail": "A day in retail",
            "government": "A day in a government facility", "industrial-manufacturing": "A day at an industrial site", "education": "A day in a school",
            "healthcare-wellness": "A day in a healthcare building", "multi-tenant": "A day in a multi-tenant building",
            "religious-institutions": "A day at a house of worship", "storage-units": "A day at a storage facility", "residential": "A day at home"}

IND_DAY = {
    "commercial": [
        ("Arrive", "Keypads anyone can use", "Our systems are designed with employees and service providers in mind, so keypads are easy to operate regardless of experience level.", "keypad", "products/7-inch-touchscreen-keypad.html"),
        ("All day", "Five systems, one manufacturer", "Intrusion, fire, access, wireless and video from one manufacturer, so a blanket of security does much more than sound an alarm.", "layers", "services.html"),
        ("When a path fails", "A backup path, instantly", "DMP Adaptive Technology moves communication from the primary to a backup path instantly.", "bolt", "products/xr550.html"),
        ("Always connected", "Up to eight paths to the monitoring service", "The XR550 Series supports up to eight communication paths between the panel and the monitoring service. The XT Series carries network, cellular and dial-up on board.", "signal", "products/xt75.html"),
    ],
    "financial-institutions": [
        ("Open the branch", "Credentialing that streamlines itself", "Integrated access control and intrusion streamline credentialing and simplify credential administration.", "key", "services/access-control.html"),
        ("Every message", "Encrypted from panel to device", "128-bit or 256-bit AES encryption secures alarm communications across the network, and from the panel to each duress and access device.", "lock", "products/xr550.html"),
        ("Off the public internet", "VAULT keeps panels private", "A secure, private, encrypted site-to-site connection to the SecureCom infrastructure, so security panels never touch the public internet.", "shield", "products/virtual-keypad.html"),
        ("At the teller machine", "A panel made for it", "TMSentry is a compact panel developed for teller machine security.", "box", "products/tmsentry.html"),
        ("Audit day", "Automated reporting", "Automated reporting reduces labor and simplifies compliance audits, and the system reduces service calls and false alarms.", "report", "industries/financial-institutions.html#needs"),
    ],
    "retail": [
        ("Open the store", "One database for every credential", "Access control and intrusion are integrated, so one database manages user credentials.", "key", "services/access-control.html"),
        ("A delivery arrives", "Fewer false alarms", "Reduce false alarms from unattended deliveries and employee turnover.", "alert", "industries/retail.html#needs"),
        ("Between service visits", "Fewer battery calls", "Decrease service calls for battery replacements.", "signal", "industries/retail.html#needs"),
        ("Across every store", "One screen for the enterprise", "Virtual Keypad handles enterprise-wide system and user management from a single screen, and cloud-based software runs multiple systems across a national footprint with a single action.", "globe", "products/virtual-keypad.html"),
        ("End of the week", "Automated enterprise reporting", "Retail systems come with automated enterprise reporting.", "report", "products/dealer-admin.html"),
    ],
    "government": [
        ("At the door", "A keypad that hides the code", "A high-security touchscreen keypad with randomized digit location and a privacy filter.", "keypad", "industries/government.html#needs"),
        ("Secure areas", "Sensors for SCIFs", "MAGNASPHERE L2 Series High Security Sensors meet UL 634 Level 2 for SCIFs and other secure applications, sold to dealers through DMP.", "lock", "industries/government.html#needs"),
        ("On the network", "256-bit AES built in", "The XR550E has built-in 256-bit AES encryption, communicating by network, digital dialer and LTE cellular, including AT&T FirstNet.", "signal", "products/xr550.html"),
        ("Compliance review", "A published white paper", "A published white paper covers NDAA, BAA and TAA compliance.", "doc", "industries/government.html#needs"),
        ("Where it is built", "Designed and built in the U.S.A.", "Technology designed and built in the U.S.A. with U.S. and global components, and a division dedicated to government customers.", "flag", "about.html"),
    ],
    "industrial-manufacturing": [
        ("At the gate", "Doors and alarm, no extra wires", "XR Series panels communicate with X1 access control units without any additional wiring.", "door", "products/x1.html"),
        ("On the floor", "One unified solution", "Manage intrusion and access control together in one unified solution.", "layers", "products/xr550.html"),
        ("Something moves", "Cameras that trigger the panel", "AlarmVision turns cameras into smart motion detectors that trigger panel responses and alarms in real time.", "camera", "products/xv-gateways-with-alarmvision.html"),
        ("Data in transit", "Encrypted local and cloud", "Encrypted local and cloud communications.", "lock", "industries/industrial-manufacturing.html#needs"),
    ],
    "education": [
        ("Arrive", "A phone is the credential", "Students and staff use their smartphones as access credentials, through mobile wallet credentials.", "phone", "products/mobile-credential.html"),
        ("All day", "Four systems in one panel", "The XR550 is an integrated panel that combines access, intrusion, fire and video in one system.", "layers", "products/xr550.html"),
        ("If it happens", "Start a lockdown three ways", "Authorized staff can start a lockdown from the Virtual Keypad app, a system keypad or any PC running Entré software.", "alert", "products/virtual-keypad.html"),
        ("In one action", "Every public door locked", "The lockdown locks all public doors and restricts access to authorized users.", "lock", "products/entre-enterprise.html"),
    ],
    "healthcare-wellness": [
        ("Open the building", "Four systems, one panel", "The XR550 combines access, intrusion, fire and video, built for environments where encrypted data is required.", "layers", "products/xr550.html"),
        ("Protect the records", "Patients' information, secured", "Healthcare providers have the additional responsibility of securing patients' protected health information, as the HIPAA Privacy Rule requires.", "shield", "industries/healthcare-wellness.html#needs"),
        ("Three paths out", "Network, dialer and LTE", "Communication by network, digital dialer and LTE cellular, including AT&T FirstNet.", "signal", "products/263lte-firstnet.html"),
        ("On public safety's network", "FirstNet approved", "We offer communicators approved for the FirstNet public-safety network, a more reliable network experience than a commercial wireless network.", "bolt", "products/263lte-firstnet.html"),
    ],
    "multi-tenant": [
        ("A resident arrives", "A key on the phone", "Mobile wallet credentials for residents and staff.", "phone", "products/digital-key-credential.html"),
        ("At the pool", "Access to only what it should open", "Virtual Keypad's Access Only user gives basic access without viewing events or video, changing door lock status or receiving push notifications, suited to pools, fitness centers and community rooms.", "key", "products/virtual-keypad.html"),
        ("Away from home", "Control it from anywhere", "With the Virtual Keypad app, customers can control their systems remotely, along with locks, lights, thermostats and more.", "home", "products/virtual-keypad.html"),
        ("Under one roof", "Intrusion, fire, access and video", "Systems built from our components combine intrusion with fire protection, access control and video.", "layers", "products/x1.html"),
    ],
    "religious-institutions": [
        ("Small footprint", "The full system inside", "The XT75 integrates intrusion, access control and AlarmVision in a small footprint.", "box", "products/xt75.html"),
        ("Movement on camera", "Smart motion detectors", "AlarmVision integrates cameras, analytics and XT75 or XR Series panels, creating smart motion detectors.", "camera", "products/xv-gateways-with-alarmvision.html"),
        ("Every week", "Easy to manage", "Complete, easy-to-manage systems that integrate intrusion, access control and video surveillance.", "keypad", "industries/religious-institutions.html#needs"),
        ("Before it ships", "Tested, every product", "100 percent of DMP products are quality tested before shipping.", "check", "about.html"),
    ],
    "storage-units": [
        ("Many panels", "One network, one site", "XR to XR communication: panels across a single site work together over the same network.", "network", "products/xr550.html"),
        ("Open and close", "Arm and disarm together", "Simultaneous arming and disarming across the site.", "clock", "products/xr550.html"),
        ("If it is needed", "Site-wide lockdown", "Fire exits and site-wide lockdowns, with no additional wiring or install labor.", "alert", "products/xr550.html"),
        ("Watching the aisles", "Cameras that respond", "AlarmVision with XT75 or XR Series panels triggers responses in real time.", "camera", "products/xv-gateways-with-alarmvision.html"),
    ],
    "residential": [
        ("Leaving", "Home, Sleep or Away", "One-touch access to three arming levels: Home, Sleep and Away.", "home", "products/xtltouch.html"),
        ("A false alarm", "Silence it, stay armed", "The False Alarm Question silences an alarm while keeping the system armed, and cancels false alarms quickly.", "alert", "products/xtlplus.html"),
        ("From anywhere", "Remote control, locks, lights", "With the Virtual Keypad app, customers can control the system remotely, along with locks, lights, thermostats and more.", "phone", "products/virtual-keypad.html"),
        ("Installing it", "All wireless", "XTLplus residential packages are all-wireless solutions for easy, flexible installation, and XTLtouch is the enhanced all-in-one wireless burglary panel.", "box", "products/xtlplus.html"),
    ],
}
_IC["network"] = _IC["signal"]
_IC["flag"] = '<path d="M5 21V4M5 4h13l-2 4 2 4H5"/>'

IND_CTA = {"commercial": "commercial security", "financial-institutions": "financial institution security", "retail": "retail security", "government": "government security",
           "industrial-manufacturing": "industrial security", "education": "school security", "healthcare-wellness": "healthcare security", "multi-tenant": "multi-tenant security",
           "religious-institutions": "house of worship security", "storage-units": "storage facility security", "residential": "home security"}
CHECK = '<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="2.600" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path pathLength="1" d="M5 12.500l4.500 4.500L19 7.500"/></svg>'


# ------------------------------------------------------------------------------------------------ renderers: industry

def _day(s, ctx):
    E, L = ctx["E"], ctx["L"]
    items = []
    for i, (k, t, x, ic, href) in enumerate(s["moments"]):
        link = f'<a class="p2-more" href="{E(L(href))}">See how<span aria-hidden="true"> &rarr;</span></a>' if href else ""
        items.append(f'<li class="p2-m" style="--i:{i}"><span class="p2-node" aria-hidden="true">{ico(ic, 24)}</span>'
                     f'<div class="p2-mc"><span class="p2-mk"><b>{i + 1:02d}</b>{E(k)}</span><h3>{E(t)}</h3><p>{E(x)}</p>{link}</div></li>')
    return (f'{ctx["sec_open"](s, "p2-day")} <div class="q-container p2-dgrid"><div class="p2-dside">'
            f'{_head(E, s)}<div class="p2-dhint" aria-hidden="true"><span></span>Scroll the day</div></div>'
            f'<ol class="p2-tl" data-p2="tl">{"".join(items)}</ol></div></section>')


def _outcomes(s, ctx):
    E, rel = ctx["E"], ctx["rel"]
    rows = "".join(f'<li class="p2-oc" style="--i:{i}"><span class="p2-chk" aria-hidden="true">{CHECK}</span>'
                   f'<div><b>{E(t)}{"<em>" + E(g) + "</em>" if g else ""}</b>{"<span>" + E(x) + "</span>" if x else ""}</div></li>' for i, (t, x, g) in enumerate(s["items"]))
    light = " p2-light" if str(s.get("image", "")).lower().endswith(".jpg") else ""
    img = (f'<figure class="p2-prod{light}"><span class="p2-halo" aria-hidden="true"></span><img src="{E(rel(s["image"]))}" alt="{E(s.get("image_alt", ""))}" width="900" height="700" loading="lazy" decoding="async">'
           f'<figcaption>{E(s.get("caption", ""))}</figcaption></figure>') if s.get("image") else ""
    return (f'{ctx["sec_open"](s, "p2-out")} <div class="q-container p2-ogrid">{img}<div>{_head(E, s)}'
            f'<ul class="p2-oclist" data-p2="reveal">{rows}</ul></div></div></section>')


def _cta(s, ctx):
    E, L = ctx["E"], ctx["L"]
    a, b = s.get("primary"), s.get("secondary")
    btns = ""
    if a:
        btns += f'<a class="p2-b p2-b1" href="{E(L(a["href"]))}">{E(a["label"])}<span aria-hidden="true">{ico("arrow", 20, 2.2)}</span></a>'
    if b:
        btns += f'<a class="p2-b p2-b2" href="{E(L(b["href"]))}">{E(b["label"])}</a>'
    note = f'<p class="p2-cnote">{E(s["note"])}</p>' if s.get("note") else ""
    eb = f'<div class="p2-ceb">{E(s["eyebrow"])}</div>' if s.get("eyebrow") else ""
    return (f'<section class="q-section p2-cta"{(" id=" + chr(34) + E(s["id"]) + chr(34)) if s.get("id") else ""}><span class="p2-cbg" aria-hidden="true"></span><div class="q-container p2-cwrap">'
            f'<div class="p2-ctxt">{eb}<h2>{E(s["heading"])}</h2>{"<p>" + E(s["body"]) + "</p>" if s.get("body") else ""}</div>'
            f'<div class="p2-cbtns">{btns}{note}</div></div></section>')


# ------------------------------------------------------------------------------------------------ renderers: about

def _numbers(s, ctx):
    E = ctx["E"]
    cells = []
    for i, (v, suf, lab) in enumerate(s["items"]):
        cells.append(f'<li class="p2-nm" style="--i:{i}"><b class="p2-big" data-to="{E(v)}" data-suf="{E(suf)}">{E(v)}{E(suf)}</b><span>{E(lab)}</span></li>')
    return (f'{ctx["sec_open"](s, "p2-nums")} <div class="q-container">{_head(E, s, True)}'
            f'<ul class="p2-ngrid" data-p2="nums">{"".join(cells)}</ul>'
            f'{"<p class=p2-nsrc>" + E(s["src"]) + "</p>" if s.get("src") else ""}</div></section>')


def _leaders(s, ctx):
    E = ctx["E"]
    groups = [("Executive team", []), ("Executive vice presidents", []), ("Vice presidents", [])]
    for n, r in s["people"]:
        g = 0 if r.startswith("Chief") else 1 if r.startswith("Executive Vice") else 2
        m = re.search(r" of (.+)$", r)
        groups[g][1].append((n, r, m.group(1) if m else ""))
    out = []
    for gname, ppl in groups:
        if not ppl:
            continue
        cards = []
        for i, (n, r, lead) in enumerate(ppl):
            ini = "".join(w[0] for w in n.split()[:2])
            reveal = (f'<span class="p2-lrev"><i>Leads</i><b>{E(lead)}</b></span>' if lead else f'<span class="p2-lrev p2-lrev-r"><i>Role</i><b>{E(r)}</b></span>')
            cards.append(f'<li class="p2-lp" tabindex="0" style="--i:{i}"><span class="p2-lmono" aria-hidden="true"><em>{E(ini)}</em></span>'
                         f'<span class="p2-lname">{E(n)}</span><span class="p2-ltitle">{E(r)}</span>{reveal}</li>')
        out.append(f'<div class="p2-lgroup"><h3 class="p2-lgh"><span>{E(gname)}</span><i>{len(ppl)}</i></h3><ul class="p2-lgrid">{"".join(cards)}</ul></div>')
    orgs = "".join(f"<span>{E(o)}</span>" for o in s.get("orgs", []))
    orgs_html = f'<div class="p2-orgs"><p>{E(s.get("orgs_intro", ""))}</p><div>{orgs}</div></div>' if orgs else ""
    return f'{ctx["sec_open"](s, "p2-leaders")} <div class="q-container">{_head(E, s)}{"".join(out)}{orgs_html}</div></section>'


def _quote(s, ctx):
    E, rel = ctx["E"], ctx["rel"]
    return (f'<section class="q-section p2-quote"{(" id=" + chr(34) + E(s["id"]) + chr(34)) if s.get("id") else ""}><img class="p2-qimg" src="{E(rel(s["image"]))}" alt="{E(s.get("image_alt", ""))}" width="1200" height="800" loading="lazy" decoding="async">'
            f'<span class="p2-qshade" aria-hidden="true"></span><div class="q-container p2-qwrap"><span class="p2-qmark" aria-hidden="true">&ldquo;</span>'
            f'<blockquote><p class="p2-qtext">{E(s["quote"])}</p><p class="p2-qsub">{E(s["sub"])}</p>'
            f'<footer>{E(s["cite"])}</footer></blockquote></div></section>')


# ------------------------------------------------------------------------------------------------ renderers: contact, support

def _router(s, ctx):
    E, L = ctx["E"], ctx["L"]
    pick, panels = [], []
    for i, p in enumerate(s["roles"]):
        pid = f'p2rt-{p["key"]}'
        pick.append(f'<button type="button" class="p2-rt-pick" role="tab" aria-selected="false" aria-controls="{pid}" id="{pid}-t" data-k="{pid}">'
                    f'<span class="p2-rt-i">{ico(p["icon"], 26)}</span><span class="p2-rt-t"><b>{E(p["label"])}</b><small>{E(p["hint"])}</small></span>'
                    f'<span class="p2-rt-a" aria-hidden="true">{ico("arrow", 20, 2)}</span></button>')
        acts = []
        for a in p["actions"]:
            if a.get("tel"):
                hrs = f'<span class="p2-act-side"><span class="p2-hrs">{E(a["hours"])}</span><span class="p2-open" data-hours="{E(a["hours"])}" hidden></span></span>'
                acts.append(f'<li class="p2-act p2-act-tel"><a href="{E(_tel(a["tel"]))}"><span class="p2-act-i">{ico("phone", 22)}</span>'
                            f'<span class="p2-act-t"><b>{E(a["label"])}</b><em>{E(a["tel"])}</em><small>{E(a["text"])}</small></span></a>{hrs}</li>')
            else:
                ext = ' rel="noopener"' if str(a["href"]).startswith("http") else ""
                acts.append(f'<li class="p2-act"><a href="{E(L(a["href"]))}"{ext}><span class="p2-act-i">{ico(a.get("icon", "arrow"), 22)}</span>'
                            f'<span class="p2-act-t"><b>{E(a["label"])}</b><small>{E(a["text"])}</small></span><span class="p2-act-go" aria-hidden="true">{ico("arrow", 18, 2.2)}</span></a></li>')
        panels.append(f'<div class="p2-rt-panel" id="{pid}" role="tabpanel" aria-labelledby="{pid}-t"><div class="p2-rt-ph"><span class="p2-rt-no">{i + 1:02d}</span>'
                      f'<h3>{E(p["title"])}</h3><p>{E(p["lead"])}</p></div><ul class="p2-acts">{"".join(acts)}</ul></div>')
    return (f'{ctx["sec_open"](s, "p2-router")} <div class="q-container" id="{E(s.get("id", "router"))}">{_head(E, s)}'
            f'<div class="p2-rt" data-p2="router"><div class="p2-rt-picks" role="tablist" aria-label="Who are you?">{"".join(pick)}</div>'
            f'<div class="p2-rt-stage" aria-live="polite"><div class="p2-rt-empty" aria-hidden="true"><span>{ico("users", 40, 1.4)}</span><b>Pick one</b>'
            f'<small>We show the exact next step: the right line, the right form or the right page.</small></div>{"".join(panels)}</div></div>'
            f'<p class="p2-rt-note">{E(s.get("note", ""))}</p></div></section>')


def _chooser(s, ctx):
    E, L = ctx["E"], ctx["L"]
    needs = "".join(f'<li><a class="p2-need" href="{E(L(n["href"]))}"{" rel=noopener" if str(n["href"]).startswith("http") else ""}><span class="p2-need-i">{ico(n["icon"], 28)}</span>'
                    f'<span class="p2-need-t"><b>{E(n["label"])}</b><small>{E(n["text"])}</small></span><span class="p2-need-go" aria-hidden="true">{ico("arrow", 20, 2.2)}</span></a></li>' for n in s["needs"])
    idx = [{"t": n["t"], "d": n["d"], "h": L(n["h"]), "k": n.get("k", "")} for n in s["index"]]
    idx_json = json.dumps(idx, ensure_ascii=False).replace("</", "<\\/")
    return (f'{ctx["sec_open"](s, "p2-choose")} <div class="q-container">{_head(E, s)}'
            f'<div class="p2-search" data-p2="chooser"><label class="p2-slab" for="p2-q">What do you need help with?</label>'
            f'<div class="p2-sbox"><span aria-hidden="true">{ico("wrench", 22)}</span><input id="p2-q" type="search" autocomplete="off" spellcheck="false" placeholder="{E(s.get("placeholder", ""))}" aria-controls="p2-res">'
            f'<kbd aria-hidden="true">Enter</kbd></div>'
            f'<ul id="p2-res" class="p2-res" hidden aria-live="polite"></ul><p class="p2-sempty" hidden>No match for that. Technical Support picks up at {E(s.get("tech", ""))}.</p>'
            f'<script type="application/json" class="p2-idx">{idx_json}</script></div>'
            f'<div class="p2-needs-h"><span>The four most common needs</span></div><ul class="p2-needs">{needs}</ul></div></section>')


def _faqgrid(s, ctx):
    E, L = ctx["E"], ctx["L"]
    cells = "".join(f'<li><a class="p2-fc" href="{E(L(c["href"]))}"><span class="p2-fc-i">{ico(c["icon"], 26)}</span><b>{E(c["title"])}</b><small>{E(c["text"])}</small>'
                    f'<span class="p2-fc-n">{c["n"]}<i> answers</i></span></a></li>' for c in s["cats"])
    return f'{ctx["sec_open"](s, "p2-fg")} <div class="q-container">{_head(E, s)}<ul class="p2-fgrid">{cells}</ul></div></section>'


# ------------------------------------------------------------------------------------------------ renderers: partners, training

def _partners(s, ctx):
    E, L = ctx["E"], ctx["L"]
    n = len(s["items"])
    import math
    pills, lines, cards = [], [], []
    for i, it in enumerate(s["items"]):
        a = -math.pi / 2 + i * 2 * math.pi / n
        x, y = 50 + 39 * math.cos(a), 50 + 37 * math.sin(a)
        lines.append(f'<line x1="50" y1="50" x2="{x:.2f}" y2="{y:.2f}" style="--d:{i * .4:.1f}s"/><circle class="p2-pulse" r="1.1" style="--d:{i * .4:.1f}s" cx="50" cy="50"><animate attributeName="cx" from="50" to="{x:.2f}" dur="3.2s" begin="{i * .4:.1f}s" repeatCount="indefinite"/><animate attributeName="cy" from="50" to="{y:.2f}" dur="3.2s" begin="{i * .4:.1f}s" repeatCount="indefinite"/></circle>')
        pills.append(f'<a class="p2-pn" href="{E(L(it["href"]))}" style="left:{x:.2f}%;top:{y:.2f}%"><span class="p2-pn-i">{ico(it["icon"], 22)}</span><b>{E(it["name"])}</b><small>{E(it["cat"])}</small></a>')
        chips = "".join(f"<span>{E(c)}</span>" for c in it["works"])
        req = f'<p class="p2-pc-req"><i>Dealer needs</i>{E(it["req"])}</p>' if it.get("req") else ""
        cards.append(f'<li><a class="p2-pc" href="{E(L(it["href"]))}"><span class="p2-pc-top"><span class="p2-pc-i">{ico(it["icon"], 26)}</span><span class="p2-pc-cat">{E(it["cat"])}</span></span>'
                     f'<h3>{E(it["name"])}</h3><p>{E(it["text"])}</p><div class="p2-pc-w"><i>Integrates with</i><div>{chips}</div></div>{req}'
                     f'<span class="p2-pc-go">Integration details<span aria-hidden="true"> &rarr;</span></span></a></li>')
    return (f'{ctx["sec_open"](s, "p2-pn-sec")} <div class="q-container">{_head(E, s, True)}'
            f'<div class="p2-net"><svg class="p2-net-l" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true" focusable="false"><ellipse cx="50" cy="50" rx="39" ry="37"/>{"".join(lines)}</svg>'
            f'<div class="p2-hub"><span class="p2-hub-r" aria-hidden="true"></span><span class="p2-hub-r r2" aria-hidden="true"></span><b>DMP</b><small>{E(s.get("hub", ""))}</small></div>{"".join(pills)}</div>'
            f'<ul class="p2-pcards">{"".join(cards)}</ul></div></section>')


def _board(s, ctx):
    E, L = ctx["E"], ctx["L"]
    months = []
    cur = None
    for it in s["sessions"]:
        if cur is None or cur["m"] != it["month"]:
            cur = {"m": it["month"], "items": []}
            months.append(cur)
        cur["items"].append(it)
    cols = []
    for mo in months:
        tix = []
        for it in mo["items"]:
            tix.append(f'<li class="p2-tk" data-end="{E(it["end"])}"><span class="p2-tk-d"><b>{E(it["d1"])}<em>to</em>{E(it["d2"])}</b><i>{E(it["dow"])}</i></span>'
                       f'<span class="p2-tk-b"><span class="p2-tk-k">{E(it["kind"])}</span><b>{E(it["title"])}</b><small>{ico("pin", 14, 2)}{E(it["where"])}</small>'
                       f'<span class="p2-tk-s">{E(it["text"])}</span></span><span class="p2-tk-next" hidden>Next up</span></li>')
        cols.append(f'<li class="p2-mo"><div class="p2-mo-h"><b>{E(mo["m"].split()[0])}</b><span>{E(mo["m"].split()[1])}</span></div><ul>{"".join(tix)}</ul></li>')
    cta = f'<div class="p2-board-cta"><a class="q-btn" href="{E(L(s["cta"]["href"]))}">{E(s["cta"]["label"])}</a><p>{E(s.get("note", ""))}</p></div>' if s.get("cta") else ""
    return (f'{ctx["sec_open"](s, "p2-board")} <div class="q-container">{_head(E, s)}<ol class="p2-months" data-p2="board">{"".join(cols)}</ol>{cta}</div></section>')


# ------------------------------------------------------------------------------------------------ renderers: blog

def _toc(s, ctx):
    E = ctx["E"]
    links = "".join(f'<a href="#{E(i)}" data-t="{E(i)}" title="{E(t)}"><b>{n + 1}</b><span>{E(t)}</span></a>' for n, (i, t) in enumerate(s["items"]))
    return (f'<nav class="p2-toc" data-p2="toc" aria-label="On this page"><div class="q-container p2-toc-in"><span class="p2-toc-l">On this page</span>'
            f'<div class="p2-toc-s">{links}</div></div><span class="p2-toc-p" aria-hidden="true"></span></nav>')


def _takeaways(s, ctx):
    E = ctx["E"]
    items = "".join(f'<li style="--i:{i}"><span class="p2-ky" aria-hidden="true">{ico("check", 22, 2.600)}</span><div><b>{E(q)}</b><p>{E(a)}</p></div></li>' for i, (q, a) in enumerate(s["items"]))
    return (f'{ctx["sec_open"](s, "p2-take")} <div class="q-container p2-takegrid"><div><div class="q-eyebrow">{E(s.get("eyebrow", "Key takeaways"))}</div>'
            f'<h2 class="q-h2 p2-h2">{E(s.get("heading", "Key takeaways"))}</h2><p class="q-lead p2-intro">{E(s.get("intro", ""))}</p></div>'
            f'<ol class="p2-takelist" data-p2="reveal">{items}</ol></div></section>')


# ------------------------------------------------------------------------------------------------ renderers: audience

def _path(s, ctx):
    E, L = ctx["E"], ctx["L"]
    steps = "".join(f'<li class="p2-st" style="--i:{i}"><span class="p2-st-n">{i + 1}</span><span class="p2-st-i">{ico(st["icon"], 28)}</span>'
                    f'<h3>{E(st["title"])}</h3><p>{E(st["text"])}</p>'
                    f'{"<a class=p2-more href=" + chr(34) + E(L(st["href"])) + chr(34) + ">" + E(st["link"]) + "<span aria-hidden=true> &rarr;</span></a>" if st.get("href") else ""}</li>' for i, st in enumerate(s["steps"]))
    return (f'{ctx["sec_open"](s, "p2-path")} <div class="q-container">{_head(E, s, True)}<ol class="p2-steps" data-p2="reveal">{steps}</ol></div></section>')


def _stack(s, ctx):
    E, L = ctx["E"], ctx["L"]
    specs = "".join(f'<li><span aria-hidden="true">{ico("doc", 16, 2)}</span>{E(x)}</li>' for x in s["specs"])
    bl = "".join(f"<li>{E(b)}</li>" for b in s.get("bullets", []))
    cta = f'<a class="q-btn" href="{E(L(s["cta"]["href"]))}">{E(s["cta"]["label"])}</a>' if s.get("cta") else ""
    return (f'{ctx["sec_open"](s, "p2-stk")} <div class="q-container p2-stkgrid"><div class="p2-stkcopy">{_head(E, s)}'
            f'<p class="q-lead p2-intro">{E(s.get("body", ""))}</p><ul class="p2-stkb">{bl}</ul>{cta}</div>'
            f'<div class="p2-files" data-p2="files" aria-label="The spec pack, as a stack of files">'
            f'<div class="p2-f p2-f4" aria-hidden="true"><span>Documentation library</span><b>{E(s["library"][0])}</b><i>{E(s["library"][1])}</i></div>'
            f'<div class="p2-f p2-f3" aria-hidden="true"><span>CAD drawings</span><b>{E(s["cad"][0])}</b><i>{E(s["cad"][1])}</i></div>'
            f'<div class="p2-f p2-f2" aria-hidden="true"><span>System Surveyor</span><b>{E(s["tool"][0])}</b><i>{E(s["tool"][1])}</i></div>'
            f'<div class="p2-f p2-f1"><span class="p2-ftab">Spec pack</span><b>{len(s["specs"])} written specifications</b><ul>{specs}</ul></div></div></div></section>')


def _flip(s, ctx):
    E = ctx["E"]
    cards = []
    for i, (q, a) in enumerate(s["items"]):
        cards.append(f'<li class="p2-fl" style="--i:{i}"><button type="button" class="p2-fl-in" aria-pressed="false">'
                     f'<span class="p2-fl-f"><span class="p2-fl-n">{i + 1:02d}</span><b>{E(q)}</b><span class="p2-fl-h"><span>See the answer</span>{ico("arrow", 18, 2.200)}</span></span>'
                     f'<span class="p2-fl-b"><span class="p2-fl-n">{i + 1:02d}</span><i>What good looks like</i><span class="p2-fl-a">{E(a)}</span></span></button></li>')
    return (f'{ctx["sec_open"](s, "p2-flips")} <div class="q-container">{_head(E, s)}<ul class="p2-flgrid" data-p2="flip">{"".join(cards)}</ul>'
            f'<p class="p2-fl-hint">Tap or press a card to flip it.</p></div></section>')


def _platform(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    sat = "".join(f'<li class="p2-sat p2-sat{i}"><a href="{E(L(x["href"]))}"><span class="p2-sat-i">{ico(x["icon"], 26)}</span><b>{E(x["title"])}</b><small>{E(x["text"])}</small></a></li>' for i, x in enumerate(s["systems"]))
    return (f'{ctx["sec_open"](s, "p2-plat")} <div class="q-container">{_head(E, s, True)}<div class="p2-pl">'
            f'<div class="p2-pl-core"><span class="p2-pl-ring" aria-hidden="true"></span><img src="{E(rel(s["image"]))}" alt="{E(s.get("image_alt", ""))}" width="900" height="620" loading="lazy" decoding="async">'
            f'<div class="p2-pl-tags"><span>One panel</span><span>One app</span><span>One set of accounts</span></div></div>'
            f'<ul class="p2-sats">{sat}</ul></div></div></section>')


RENDER_POP2 = {"p2-day": _day, "p2-outcomes": _outcomes, "p2-cta": _cta, "p2-numbers": _numbers, "p2-leaders": _leaders, "p2-quote": _quote,
               "p2-router": _router, "p2-chooser": _chooser, "p2-faqgrid": _faqgrid, "p2-partners": _partners, "p2-board": _board,
               "p2-toc": _toc, "p2-takeaways": _takeaways, "p2-path": _path, "p2-stack": _stack, "p2-flip": _flip, "p2-platform": _platform}


# ------------------------------------------------------------------------------------------------ wrappers: portal sample dashboard, finder compare

_STATE = {"specs": {}, "ptype": {}}


def _tile_end(html, start):
    """Index just past the </div> that closes the <div> opening at html[start]."""
    depth = 0
    for m in re.finditer(r"<div\b|</div>", html[start:]):
        depth += 1 if m.group(0) != "</div>" else -1
        if depth == 0:
            return start + m.end()
    return -1


def _portal_sample(ctx):
    E, rel = ctx["E"], ctx["rel"]
    docs = [("XR550 spec sheet", "Product specifications", "Viewed today"), ("XR Series compliance guide", "Listings and compliance", "Viewed yesterday"),
            ("Firmware release notes", "Version 263", "Viewed this week"), ("DMP panel feature comparison guide", "Comparison guide", "Viewed this week")]
    drows = "".join(f'<li><span aria-hidden="true">{ico("doc", 18, 1.8)}</span><span><b>{E(a)}</b><small>{E(b)}</small></span><em>{E(c)}</em></li>' for a, b, c in docs)
    steps = [("Placed", True), ("Packed", True), ("Shipped", False), ("Delivered", False)]
    srows = "".join(f'<li class="{"on" if on else ""}"><i></i><span>{E(n)}</span></li>' for n, on in steps)
    courses = [("X1 Series Access Control, 1 hour", "Complete"), ("Virtual Keypad dealer course, 1 hour", "Complete"), ("XR Series Basics, 8 hours", "In progress"), ("XT75 Series Basics, 8 hours", "Not started")]
    crows = "".join(f'<li class="{"done" if c == "Complete" else "mid" if c == "In progress" else ""}"><span>{E(t)}</span><em>{E(c)}</em></li>' for t, c in courses)
    ring = ('<svg class="p2-ring" viewBox="0 0 80 80" aria-hidden="true" focusable="false"><circle cx="40" cy="40" r="32" class="t"/>'
            '<circle cx="40" cy="40" r="32" class="v" pathLength="100" stroke-dasharray="50 100" transform="rotate(-90 40 40)"/><text x="40" y="45" text-anchor="middle">50%</text></svg>')
    assets = [("Product brochure", "assets/banner-allin-600.jpg", "Your logo and contact details"), ("Custom video", "assets/phone-commercial-600.jpg", "Free to customize"), ("Branded keypad", "assets/keypad-722-600.png", "With your logo")]
    arows = "".join(f'<li><span class="p2-as-img"><img src="{E(rel(img))}" alt="" width="200" height="120" loading="lazy" decoding="async"></span><b>{E(t)}</b><small>{E(c)}</small></li>' for t, img, c in assets)
    return (f'<div class="p2-sample"><div class="p2-sample-h"><b>Your day</b><span class="p2-sd">Sample data</span><small>Illustrative only. These cards show the kind of thing the portal could surface, not real orders or accounts.</small></div>'
            f'<div class="p2-sgrid">'
            f'<section class="p2-sc" aria-label="Recently viewed documents, sample data"><h4>Recently viewed<span class="p2-sd">Sample</span></h4><ul class="p2-sdocs">{drows}</ul></section>'
            f'<section class="p2-sc" aria-label="Order status, sample data"><h4>Order status<span class="p2-sd">Sample</span></h4><p class="p2-sord"><b>Sample order 0001</b><small>XR550 control panel x 2, SR3 Bluetooth reader x 6</small></p><ol class="p2-ssteps">{srows}</ol></section>'
            f'<section class="p2-sc" aria-label="Training progress, sample data"><h4>DMP University<span class="p2-sd">Sample</span></h4><div class="p2-strain">{ring}<ul>{crows}</ul></div></section>'
            f'<section class="p2-sc" aria-label="Marketing assets, sample data"><h4>Marketing Central<span class="p2-sd">Sample</span></h4><ul class="p2-sas">{arows}</ul></section>'
            f'</div></div>')


def _portal_wrap(s, ctx):
    import preview_motion
    html = preview_motion._portal(s, ctx)
    i = html.find('<div class="mo-tiles">')
    if i < 0:
        return html
    j = _tile_end(html, i)
    return html[:j] + _portal_sample(ctx) + html[j:] if j > 0 else html


def _finder_wrap(s, ctx):
    import preview_motion
    html = preview_motion._finder(s, ctx)
    E = ctx["E"]
    bl = {x["key"]: x["label"] for x in s.get("buildings", [])}
    nl = {x["key"]: x["label"] for x in s.get("needs", [])}
    prods = s.get("products", [])
    it = iter(range(len(prods)))
    specs = {}

    def card(m):
        i = next(it, None)
        if i is None:
            return m.group(0)
        p = prods[i]
        href = p.get("href", "")
        sp = _STATE["specs"].get(href, [])
        specs[str(i)] = {"n": p["name"], "h": href, "t": [bl.get(k, k) for k in p.get("buildings", [])], "s": [nl.get(k, k) for k in p.get("needs", [])],
                         "soon": "coming soon" in p["name"].lower(), "sp": sp}
        chips = "".join(f'<span class="p2-wc" data-k="b:{E(k)}">{E(bl.get(k, k))}</span>' for k in p.get("buildings", []))
        chips += "".join(f'<span class="p2-wc" data-k="n:{E(k)}">{E(nl.get(k, k))}</span>' for k in p.get("needs", []))
        why = f'<span class="p2-why"><i>Why this</i><span class="p2-why-c">{chips}</span></span>'
        inner = m.group(2).replace('<span class="mo-go">', why + '<span class="mo-go">', 1)
        soon = '<span class="p2-soon">Coming soon, not orderable</span>' if specs[str(i)]["soon"] else ""
        btn = (f'<button type="button" class="p2-cmp" data-i="{i}" aria-pressed="false" aria-label="Compare {E(p["name"])}"><span class="p2-cmp-b" aria-hidden="true">{ico("check", 14, 3)}</span>Compare</button>')
        return m.group(1) + inner + soon + btn + m.group(3)

    html = re.sub(r'(<li class="mo-fc"[^>]*>)(.*?)(</li>)', card, html, flags=re.S)
    data = json.dumps(specs, ensure_ascii=False).replace("</", "<\\/")
    tray = ('<div class="p2-tray" data-p2="tray" hidden role="region" aria-label="Compare products">'
            '<div class="p2-tray-panel" hidden><div class="p2-tray-scroll"></div></div>'
            '<div class="p2-tray-bar"><span class="p2-tray-t"><b>Compare</b><small data-c>0 of 3 selected</small></span><ul class="p2-tray-sel"></ul>'
            '<button type="button" class="p2-tray-go" disabled>Compare specs</button><button type="button" class="p2-tray-clear" aria-label="Clear comparison">Clear</button></div></div>')
    k = html.rfind("</div></section>")
    extra = f'<script type="application/json" class="p2-fdata">{data}</script>{tray}'
    return html[:k] + extra + html[k:] if k > 0 else html + extra


RENDER_POP2["portal"] = _portal_wrap
RENDER_POP2["finder"] = _finder_wrap


# ------------------------------------------------------------------------------------------------ augment: insert or swap sections from facts already in the content

PHONE = "877-757-4367"
BUY = "https://buy.dmp.com/dmp/Shop"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def _find(secs, pred, start=0):
    for i in range(start, len(secs)):
        if pred(secs[i]):
            return i
    return -1


def _first_sentence(t):
    m = re.search(r"(?<=[a-z0-9\)\"])\.(\s|$)", t)
    return (t[:m.start() + 1] if m else t).strip()


def _ctasec(heading, body, primary, secondary, eyebrow="", note=""):
    return {"type": "p2-cta", "eyebrow": eyebrow, "heading": heading, "body": body, "primary": primary, "secondary": secondary, "note": note}


def _inside_sales():
    return {"label": f"Talk to Inside Sales {PHONE}", "href": "tel:+18777574367"}


def _industry(p, slug):
    secs = p["sections"]
    hero = secs[0]
    name = hero.get("eyebrow", slug.replace("-", " ").title())
    nm = name.lower()
    k = _find(secs, lambda s: s["type"] == "showcase3d")
    sp = _find(secs, lambda s: s["type"] == "spotlight")
    if k < 0 or sp < 0 or slug not in IND_DAY:
        return
    moments = IND_DAY[slug]
    day = {"type": "p2-day", "id": "day", "alt": True, "eyebrow": "A day in the building", "heading": IND_NOUN[slug],
           "intro": f"{len(moments)} moments, each one tied to a real DMP capability named on this page.", "moments": moments}
    items = []
    for b in secs[sp].get("needs", []):
        m = re.match(r"^([^:]{2,48}): (.+)$", b)
        cap = lambda t: t[:1].upper() + t[1:]
        items.append((m.group(1), cap(m.group(2)), "") if m else (cap(b), "", ""))
    items = items[:4]
    words = lambda t: set(re.findall(r"[a-z0-9]+", t.lower()))
    for v, lab in hero.get("stats", []):
        if len(items) >= 6:
            break
        lw = words(lab)
        if any(len(lw & words(t + " " + x)) / max(1, len(lw)) >= .5 for t, x, _g in items):
            continue
        items.append((lab, "", v))
    lineup = secs[k]["items"][0]
    out = {"type": "p2-outcomes", "id": "outcomes", "dark": True, "eyebrow": "The checklist", "heading": "What a good system does here",
           "intro": "What to look for, in DMP's own words.", "items": items, "image": lineup[1], "image_alt": lineup[0], "caption": lineup[0]}
    secs[k + 1:k + 1] = [day, out]
    cta = _ctasec(f"Talk to a DMP dealer about {IND_CTA.get(slug, nm)}", "DMP sells through authorized dealers. A dealer designs, installs and services the system, and Inside Sales supports the design.",
               {"label": "Find a dealer", "href": "find-a-dealer.html"}, _inside_sales(), "Next step", "Inside Sales, 8 a.m. to 5 p.m. Central.")
    lf = _find(secs, lambda s: s["type"] == "leadform")
    secs.insert(lf if lf >= 0 else len(secs), cta)


def _about(p):
    secs = p["sections"]
    m = _find(secs, lambda s: s.get("id") == "mission")
    t = _find(secs, lambda s: s.get("id") == "story")
    pl = _find(secs, lambda s: s.get("id") == "plant")
    ld = _find(secs, lambda s: s["type"] == "leadership")
    if ld >= 0:
        secs[ld] = {**secs[ld], "type": "p2-leaders"}
    if pl >= 0:
        secs[pl] = {**secs[pl], "image": "assets/hq-exterior-1200.jpg", "image_alt": "The DMP headquarters in Springfield, Missouri", "tag": "Our headquarters"}
    if t >= 0:
        secs.insert(t + 1, {"type": "p2-quote", "id": "quote", "image": "assets/plant-1200.jpg", "image_alt": "The DMP production floor",
                            "quote": "We provide customer-driven products through listening, anticipating needs and responding quickly with innovative solutions that work.",
                            "sub": "We insist on the integrity of our products and our people.", "cite": "DMP's mission, in our own words"})
    if m >= 0:
        secs.insert(m + 1, {"type": "p2-numbers", "id": "numbers", "dark": True, "eyebrow": "By the numbers", "heading": "What fifty years of building security adds up to",
                            "items": [["100", "%", "Of DMP products are quality tested before shipping"], ["14", "", "Product categories"], ["900", "+", "Documents in the library"],
                                      ["200", "", "Sales training videos on DMP University"], ["3", "", "Year warranty on products we manufacture"], ["12", "", "People who lead DMP"]],
                            "src": "All figures are from DMP's own pages on this site."})


def _contact(p):
    secs = p["sections"]
    cb = _find(secs, lambda s: s["type"] == "callboard")
    hours = {}
    if cb >= 0:
        for it in secs[cb].get("items", []):
            hours[it["number"]] = it["hours"]
    def tel(label, num, text):
        return {"tel": num, "label": label, "text": text, "hours": hours.get(num, "")}
    roles = [
        {"key": "dealer", "label": "I am a dealer", "hint": "Order, program, get support", "icon": "wrench", "title": "Dealers: order, install, get answers", "lead": "The fastest routes for an authorized dealer.",
         "actions": [{"href": BUY, "label": "Order at buy.DMP.com", "text": "The Buy site takes orders 24 hours a day.", "icon": "cart"},
                     tel("Technical Support", "888-436-7832", "Installation, programming and troubleshooting."),
                     tel("Customer Service", "866-266-2826", "Products and ordering, software activations, shipping."),
                     {"href": "support/documentation.html", "label": "Technical documentation", "text": "Spec sheets, installation and programming guides, quick start guides.", "icon": "doc"},
                     {"href": "support/become-a-dealer.html", "label": "Not a dealer yet? Apply", "text": "Approval should take just a few days.", "icon": "star"}]},
        {"key": "specifier", "label": "I am specifying a building", "hint": "Design, specs, quotes", "icon": "build", "title": "Specifiers: design support and documents", "lead": "System design help from a person, and the documents to write the spec.",
         "actions": [tel("Inside Sales", PHONE, "System design, architect and engineer support, pre-sales support, quotes and pricing."),
                     {"href": "support/ae-support.html", "label": "Architect and engineer support", "text": "A&E specifications and CAD drawings for panels, enclosures, modules, keypads and wireless.", "icon": "doc"},
                     {"href": "support/design-tools.html", "label": "Design tools", "text": "Design DMP systems on a digital floor plan and generate a bill of materials.", "icon": "layers"},
                     {"href": "support/get-a-quote.html", "label": "Get a quote", "text": "Tell us what you are specifying and where. A person will reply.", "icon": "quote"}]},
        {"key": "owner", "label": "I own a building", "hint": "Find a dealer, ask the right questions", "icon": "home", "title": "Building owners: start with a dealer", "lead": "DMP sells through authorized dealers and distributors, so a dealer is the first call.",
         "actions": [{"href": "find-a-dealer.html", "label": "Find an authorized dealer", "text": "Tell us where the building is and what it needs, and a person replies.", "icon": "pin"},
                     tel("Inside Sales", PHONE, "Give your city or state and Inside Sales connects you with the regional sales manager for your territory."),
                     {"href": "for-building-owners.html", "label": "Six questions to ask a dealer", "text": "What separates a good proposal from a vague one.", "icon": "check"}]},
        {"key": "customer", "label": "I already have a DMP system", "hint": "Help with a system in place", "icon": "shield", "title": "Existing systems: where to get help", "lead": "Your installing dealer knows the system. These cover the rest.",
         "actions": [{"href": "find-a-dealer.html", "label": "Need a dealer? Find one", "text": "DMP sells and supports through authorized dealers and distributors.", "icon": "pin"},
                     {"href": "support/tech-faqs/mobile-platforms.html", "label": "App answers", "text": "Help files, App Keys, EASYconnect, push notifications and Remote Link downloads.", "icon": "phone"},
                     {"href": "training/end-user-training.html", "label": "Virtual Keypad training", "text": "A one-hour live Virtual Keypad session with a DMP trainer.", "icon": "cap"},
                     tel("Technical Support", "888-436-7832", "Installation, programming, troubleshooting and diagnostic issues.")]},
    ]
    sec = {"type": "p2-router", "id": "router", "eyebrow": "Start here", "heading": "Who are you?", "intro": "Pick the one that fits and we show the exact next step.", "roles": roles,
           "note": "Hours are Central time. The Open now badge is calculated in your browser from the posted hours, on weekdays; DMP holiday closures are on the support page."}
    secs.insert(1 if secs and secs[0]["type"].startswith("hero") else 0, sec)


def _support(pages, p):
    secs = p["sections"]
    tf = pages.get("support/tech-faqs.html")
    cats = []
    if tf:
        tl = next((s for s in tf["sections"] if s["type"] == "tiles"), None)
        icons = {"access-control": "key", "cellular-network-communication": "signal", "control-panel": "layers", "keypads": "keypad", "mobile-platforms": "phone", "monitoring-center": "server", "video": "camera", "wireless": "plug"}
        for it in (tl["items"] if tl else []):
            slug = it[2].rsplit("/", 1)[-1].replace(".html", "")
            pg = pages.get(it[2])
            n = sum(len(s.get("items", [])) for s in pg["sections"] if s["type"] == "faq") if pg else 0
            cats.append({"title": it[0], "text": it[1], "href": it[2], "icon": icons.get(slug, "wrench"), "n": n})
    index = [{"t": c["title"] + " (technical FAQs)", "d": c["text"], "h": c["href"], "k": "faq answer question troubleshoot"} for c in cats]
    index += [
        {"t": "Programming and diagnostics codes", "d": "Control panel answers: codes, firmware updates, Remote Link, wireless and keypad setup by panel.", "h": "support/tech-faqs/control-panel.html", "k": "program programming code diagnostics reset lockout default user code firmware panel"},
        {"t": "Documentation library", "d": "Spec sheets, installation and programming guides, quick start guides and technical updates.", "h": "support/documentation.html", "k": "spec sheet datasheet manual guide pdf documents download"},
        {"t": "DMP University", "d": "Free on-demand courses and 200 sales training videos.", "h": "training/dmp-university.html", "k": "course learn training online video"},
        {"t": "Technical training", "d": "Technician Bootcamps and Tech Training Tours.", "h": "training/technical-training.html", "k": "bootcamp class training tour technician"},
        {"t": "SecureCom Wireless", "d": "Activation and billing for cellular service on SecureComWireless.com.", "h": "https://securecomwireless.com/", "k": "activate activation billing cellular lte sim"},
        {"t": "Call Technical Support", "d": "888-436-7832, 7 a.m. to 7 p.m. Central.", "h": "tel:+18884367832", "k": "phone call help installation programming troubleshooting"},
        {"t": "Call Inside Sales", "d": "877-757-4367, 8 a.m. to 5 p.m. Central. System design, quotes and pricing.", "h": "tel:+18777574367", "k": "phone call quote pricing design sales"},
        {"t": "Call Customer Service", "d": "866-266-2826, 8 a.m. to 6 p.m. Central. Orders, activations and shipping.", "h": "tel:+18662662826", "k": "phone call order shipping return"},
        {"t": "Get a quote", "d": "Tell us what you are specifying and where.", "h": "support/get-a-quote.html", "k": "quote price estimate"},
        {"t": "Find a regional sales manager", "d": "The directory lists titles and territories.", "h": "support/sales-directory.html", "k": "sales rep manager territory region"},
        {"t": "Architect and engineer support", "d": "A&E specifications and CAD drawings.", "h": "support/ae-support.html", "k": "cad drawing specification architect engineer"},
        {"t": "Dealer services", "d": "Dealer Admin, Dealer Account, firmware, the Customer Return Center and the warranty.", "h": "support/dealer-services.html", "k": "dealer admin return repair rma warranty firmware"},
        {"t": "Marketing support", "d": "Marketing Central assets, custom videos and print at our cost.", "h": "support/marketing.html", "k": "brochure logo video marketing print"},
    ]
    chooser = {"type": "p2-chooser", "id": "start-here", "dark": True, "eyebrow": "Start here", "heading": "Tell us what you need. We point to the exact page.",
               "intro": "Type a word, or pick one of the four things people ask for most.", "placeholder": "Try: firmware, programming code, spec sheet, activation",
               "tech": "888-436-7832, 7 a.m. to 7 p.m. Central",
               "needs": [{"label": "Fix or program a panel", "text": "Codes, firmware and wireless setup, answered by panel.", "href": "support/tech-faqs/control-panel.html", "icon": "wrench"},
                         {"label": "Find a spec sheet or guide", "text": "More than 900 documents in the library.", "href": "support/documentation.html", "icon": "doc"},
                         {"label": "Learn a product", "text": "DMP University, technical, sales and end-user training.", "href": "training.html", "icon": "cap"},
                         {"label": "Activate cellular service", "text": "Activation and billing on SecureComWireless.com.", "href": "https://securecomwireless.com/", "icon": "signal"}],
               "index": index}
    grid = {"type": "p2-faqgrid", "id": "faqs", "eyebrow": "Technical FAQs", "heading": "Eight categories of answers from Technical Support", "intro": "Pick the product family you are working on. Every question and answer is on its page.", "cats": cats}
    t = _find(secs, lambda s: s["type"] == "tiles" and s.get("eyebrow") == "Start here")
    if t >= 0:
        del secs[t]
    secs[1:1] = [chooser, grid] if cats else [chooser]


def _partners(p):
    secs = p["sections"]
    sv = _find(secs, lambda s: s["type"] == "services")
    if sv < 0:
        return
    meta = {"Evolon": ("Video verification", "camera", ["Virtual Keypad", "DMP intrusion panels", "AlarmVision"], "No special licensing or dealer certification"),
            "System Surveyor": ("System design", "layers", ["The DMP product catalog"], "A free dealer tier, no certification"),
            "SureView Systems": ("Alarm response", "alert", ["SCS-1R", "SCS-VR", "Entré"], "A Class 3 License and a Device Server or OpsLink Server"),
            "Genetec": ("Video management", "server", ["DMP intrusion panels"], "One Genetec license per intrusion panel"),
            "HavenLock": ("Door hardware", "lock", ["Platform agnostic"], "Certification recommended"),
            "ASSA ABLOY Aperio": ("Door hardware", "key", ["XR150", "XR550", "734A module"], "")}
    items = []
    for n, d, h in secs[sv]["items"]:
        c, ic, w, r = meta.get(n, ("Partner", "plug", [], ""))
        items.append({"name": n, "cat": c, "icon": ic, "works": w, "req": r, "text": _first_sentence(d), "href": h})
    secs[sv] = {"type": "p2-partners", "id": "partners", "eyebrow": "Integrates with DMP", "heading": secs[sv].get("heading", "Pick the partner that matches the job"),
                "intro": "DMP at the centre, six partners with verified integrations around it, connected through Dealer Admin.", "hub": "Panels, Dealer Admin", "items": items}
    d = _find(secs, lambda s: s.get("eyebrow") == "Build a connected solution")
    if d >= 0:
        secs.insert(d + 1, _ctasec("Make something that works with DMP", "Software providers, hardware makers and platforms can apply. We evaluate each on technical compatibility, customer value, market opportunity and long-term strategic alignment.",
                                {"label": "Apply to the Technology Partner Program", "href": "partners/become-a-partner.html#apply"}, _inside_sales(), "Become a partner"))


def _training(p):
    secs = p["sections"]
    t = _find(secs, lambda s: s["type"] == "timeline")
    if t < 0:
        return
    ses = []
    for mon, title, text, _img in secs[t]["items"]:
        m = re.match(r"(\w+) (\d+) to (\d+), (\d{4})\.\s*(.*)", text)
        if not m or m.group(1) not in MONTHS:
            continue
        mo = MONTHS.index(m.group(1)) + 1
        d1, d2, y = int(m.group(2)), int(m.group(3)), int(m.group(4))
        wd = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        dow = f"{wd[date(y, mo, d1).weekday()]} to {wd[date(y, mo, d2).weekday()]}"
        tour = "Tour" in title
        kind = "Tech Training Tour" if tour else "Advanced Bootcamp" if title.startswith("Advanced") else "Technician Bootcamp"
        clean = re.sub(r" (January|February|March|April|May|June|July|August|September|October|November|December)$", "", title).split(", ")[0]
        where = "Detroit, Michigan" if "Detroit" in title else "Springfield headquarters"
        ses.append({"month": mon, "d1": str(d1), "d2": str(d2), "dow": dow, "kind": kind, "title": clean, "where": where, "text": m.group(5), "end": f"{y:04d}-{mo:02d}-{d2:02d}"})
    if len(ses) < 3:
        return
    secs[t] = {"type": "p2-board", "id": "sessions", "alt": True, "eyebrow": secs[t].get("eyebrow", "Upcoming in-person sessions"), "heading": secs[t]["heading"],
               "intro": "Dates are from DMP's published schedule. Days of the week are worked out from the dates.", "sessions": ses,
               "cta": {"label": "See technical training", "href": "training/technical-training.html"}, "note": "Bootcamp registration includes a card payment."}


def _blog_post(pages, p):
    secs = p["sections"]
    sa = _find(secs, lambda s: s["type"] == "detail" and s.get("eyebrow") == "The short answer")
    if sa < 0:
        return
    toc = [("short-answer", "The short answer")]
    secs[sa]["id"] = "short-answer"
    take = []
    for s in secs[sa + 1:]:
        if s["type"] == "detail" and s.get("eyebrow") != "Engineer's note" and s.get("heading") and s["heading"].endswith("?") and len(take) < 4:
            take.append((s["heading"], _first_sentence(s.get("body", ""))))
        if s.get("heading") and s["type"] in ("detail", "comparison", "faq", "cards") and s.get("eyebrow") != "Engineer's note" and not s.get("stage"):
            sid = _slug(s["heading"])[:44]
            if s["type"] == "cards" and not s["heading"].endswith("?"):
                pass
            s.setdefault("id", sid)
            toc.append((s["id"], s["heading"]))
    toc = toc[:11]
    ins = []
    if take:
        ins.append({"type": "p2-takeaways", "id": "takeaways", "dark": True, "eyebrow": "Key takeaways", "heading": "Key takeaways",
                    "intro": "The short answer, then what settles it.", "items": take})
    secs[sa + 1:sa + 1] = ins
    secs.insert(1, {"type": "p2-toc", "items": toc})
    # thumbnails on the "More from the blog" cards
    hub = pages.get("blog.html")
    thumbs = {}
    if hub:
        for s in hub["sections"]:
            if s["type"] == "tiles":
                for it in s["items"]:
                    thumbs[it[2]] = it[3]
    for s in secs:
        if s["type"] == "resources" and s.get("id") == "more-posts":
            s["items"] = [list(it[:5]) + [thumbs[it[4]]] if it[4] in thumbs else it for it in s["items"]]


def _for_dealers(p):
    secs = p["sections"]
    steps = [{"icon": "doc", "title": "Apply", "text": "Approval to become an authorized DMP dealer should take just a few days.", "href": "support/become-a-dealer.html", "link": "Apply"},
             {"icon": "cap", "title": "Train", "text": "DMP University is free and on demand, with 200 sales training videos.", "href": "training/dmp-university.html", "link": "See DMP University"},
             {"icon": "megaphone", "title": "Brand", "text": "A free Marketing Central account. Most assets are free, and they carry your logo and contact details.", "href": "support/marketing.html", "link": "See Marketing Central"},
             {"icon": "cart", "title": "Order", "text": "The Buy site takes orders 24 hours a day.", "href": BUY, "link": "Open the Buy site"},
             {"icon": "wrench", "title": "Get support", "text": "Technical Support picks up from 7 a.m. to 7 p.m. Central at 888-436-7832.", "href": "support.html", "link": "See every line"}]
    secs.insert(1, {"type": "p2-path", "id": "path", "alt": True, "eyebrow": "The dealer path", "heading": "From application to first order, five steps.", "intro": "Each one has a home today.", "steps": steps})
    lf = _find(secs, lambda s: s["type"] == "leadform")
    secs.insert(lf if lf >= 0 else len(secs), _ctasec("Become an authorized DMP dealer", "Approval should take just a few days. Inside Sales can answer questions before you apply.",
                                                    {"label": "Apply to become a dealer", "href": "support/become-a-dealer.html"}, _inside_sales(), "Join", "Inside Sales, 8 a.m. to 5 p.m. Central."))


def _for_specifiers(p):
    secs = p["sections"]
    i = _find(secs, lambda s: s.get("eyebrow") == "The spec pack")
    if i >= 0:
        b = secs[i]
        names = [x.strip() for x in re.split(r",\s*| and ", b["bullets"][0].replace("Written specs for the ", "")) if x.strip()]
        secs[i] = {"type": "p2-stack", "id": "spec-pack", "stage": True, "eyebrow": b["eyebrow"], "heading": b["heading"], "body": b["body"], "bullets": b["bullets"][1:],
                   "specs": [n + " A&E specification" for n in names], "cad": ["73", "CAD drawings in six groups"], "tool": ["5 catalogs", "import into System Surveyor, with a free dealer tier"],
                   "library": ["900+", "documents in the library"], "cta": b.get("cta")}
    lf = _find(secs, lambda s: s["type"] == "leadform")
    secs.insert(lf if lf >= 0 else len(secs), _ctasec("Start your specification with a person", "Inside Sales supports system design, architect and engineer questions and pre-sales work.",
                                                   _inside_sales(), {"label": "Open the documentation library", "href": "support/documentation.html"}, "Specifiers", "Inside Sales, 8 a.m. to 5 p.m. Central."))


def _for_owners(p):
    secs = p["sections"]
    i = _find(secs, lambda s: s["type"] == "cards" and s.get("heading", "").startswith("Six questions"))
    if i >= 0:
        b = secs[i]
        secs[i] = {"type": "p2-flip", "id": "six-questions", "alt": True, "eyebrow": b.get("eyebrow", "What to ask"), "heading": b["heading"], "items": [[a, c] for a, c in b["items"]]}
    lf = _find(secs, lambda s: s["type"] == "leadform")
    secs.insert(lf if lf >= 0 else len(secs), _ctasec("Find an authorized DMP dealer", "Tell us where the building is, and Inside Sales connects you with the regional sales manager for your territory, who can point you to a dealer.",
                                                   {"label": "Find a dealer", "href": "find-a-dealer.html"}, _inside_sales(), "Building owners", "Inside Sales, 8 a.m. to 5 p.m. Central."))


def _why(p):
    secs = p["sections"]
    i = _find(secs, lambda s: s["type"] == "cards" and s.get("eyebrow") == "One platform")
    if i >= 0:
        b = secs[i]
        icons = {"Intrusion": ("shield", "services/intrusion.html"), "Access control": ("key", "services/access-control.html"), "Fire": ("alert", "services/fire.html"), "Video": ("camera", "services/video.html")}
        secs[i] = {"type": "p2-platform", "id": "platform", "alt": True, "eyebrow": b["eyebrow"], "heading": b["heading"], "image": "assets/p-xr550-1200.png", "image_alt": "The DMP XR550 control panel",
                   "systems": [{"title": t, "text": x, "icon": icons.get(t, ("shield", "services.html"))[0], "href": icons.get(t, ("shield", "services.html"))[1]} for t, x in b["items"]]}
    lf = _find(secs, lambda s: s["type"] == "leadform")
    secs.insert(lf if lf >= 0 else len(secs), _ctasec("See it on your building", "Choose a product, or tell a person what you are protecting.",
                                                   {"label": "Find a system", "href": "find-a-system.html"}, _inside_sales(), "Why DMP", "Inside Sales, 8 a.m. to 5 p.m. Central."))


def augment(content):
    pages = {pg["file"]: pg for pg in content["pages"]}
    if content.get("_pop2") or "industries/commercial.html" not in pages:
        return content   # only the DMP content file
    content["_pop2"] = True
    # product specs for the finder compare tray
    for f, pg in pages.items():
        if f.startswith("products/"):
            sp = next((s for s in pg["sections"] if s["type"] == "specs"), None)
            if sp:
                _STATE["specs"][f] = [[a, b] for a, b in sp["items"]]
    for f in list(pages):
        if f.startswith("industries/") and f != "industries.html":
            _industry(pages[f], f.split("/")[1][:-5])
    for f, fn in (("about.html", _about), ("contact.html", _contact), ("partners.html", _partners), ("training.html", _training),
                  ("for-dealers.html", _for_dealers), ("for-specifiers.html", _for_specifiers), ("for-building-owners.html", _for_owners), ("why-dmp.html", _why)):
        if f in pages:
            fn(pages[f])
    if "support.html" in pages:
        _support(pages, pages["support.html"])
    if "partners/become-a-partner.html" in pages:
        pass
    for f in list(pages):
        if f.startswith("blog/"):
            _blog_post(pages, pages[f])
    return content


# ------------------------------------------------------------------------------------------------ CSS

POP2_CSS = r"""
/* ===== pop pass 2 ===== */
.p2-head{max-width:760px;margin:0 0 44px}.p2-head.p2-center{margin-left:auto;margin-right:auto;text-align:center}
.p2-h2{margin-top:22px}.p2-intro{margin-top:18px;max-width:580px}
.p2-more{display:inline-flex;align-items:center;min-height:44px;margin-top:4px;font-weight:700;font-size:14.5px;color:var(--accent-ink);text-decoration:none}
.p2-more:hover{text-decoration:underline;text-underline-offset:3px}
html.pv-js .p2-rv{opacity:0;transform:translateY(22px)}
html.pv-js .p2-rv.in{opacity:1;transform:none;transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1);transition-delay:calc(var(--i,0)*80ms)}
.p2-day .q-container,.p2-out .q-container,.p2-nums .q-container{position:relative}
@keyframes p2-float{0%,100%{transform:translateY(0) rotate(-.6deg)}50%{transform:translateY(-14px) rotate(.8deg)}}
@keyframes p2-ping{0%{transform:scale(.9);opacity:.8}100%{transform:scale(1.5);opacity:0}}
@keyframes p2-dash{to{stroke-dashoffset:-14}}
@keyframes p2-drop{0%,100%{transform:scaleY(.4);transform-origin:top}50%{transform:scaleY(1);transform-origin:top}}
@keyframes p2-in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes p2-pop{from{opacity:0;transform:translateY(14px) scale(.96)}to{opacity:1;transform:none}}

/* ---- A day in the building ---- */
.p2-dgrid{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:clamp(32px,6vw,96px);align-items:start}
.p2-dside{position:sticky;top:110px}.p2-dside .p2-head{margin-bottom:26px}
.p2-dhint{display:flex;align-items:center;gap:12px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--fg-muted);font-weight:700}
.p2-dhint span{display:block;width:2px;height:44px;background:linear-gradient(var(--q-gold),transparent);animation:p2-drop 2.2s ease-in-out infinite}
.p2-tl{list-style:none;margin:0;padding:0;position:relative;--p:1}
.p2-tl::before{content:"";position:absolute;left:27px;top:28px;bottom:28px;width:3px;border-radius:2px;background:var(--border)}
.p2-tl::after{content:"";position:absolute;left:27px;top:28px;width:3px;border-radius:2px;background:var(--q-gold);height:calc((100% - 56px)*var(--p))}
.p2-m{position:relative;display:grid;grid-template-columns:56px minmax(0,1fr);gap:22px;padding-bottom:30px}.p2-m:last-child{padding-bottom:0}
.p2-node{position:relative;z-index:1;width:56px;height:56px;border-radius:50%;display:grid;place-items:center;background:var(--q-gold);color:#111;box-shadow:0 0 0 6px var(--bg-alt),0 16px 30px -12px rgba(255,210,61,.7);transition:background .4s,color .4s,box-shadow .4s,transform .4s}
.p2-mc{background:var(--card);border:1px solid var(--border);border-radius:calc(var(--radius) + 6px);padding:26px 28px 22px;box-shadow:0 20px 44px -30px rgba(17,24,39,.4);transition:opacity .5s,transform .5s,border-color .3s,box-shadow .3s}
.p2-mc:hover{border-color:var(--q-gold);box-shadow:0 26px 50px -28px rgba(17,24,39,.5)}
.p2-mk{display:flex;align-items:center;gap:10px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:800;color:var(--accent-ink)}
.p2-mk b{font-size:13px;padding:3px 9px;border-radius:999px;background:var(--q-gold);color:#111;letter-spacing:.06em}
.p2-mc h3{margin:12px 0 8px;font-size:clamp(21px,2vw,27px);line-height:1.15;letter-spacing:-.02em;color:var(--fg)}
.p2-mc p{margin:0;font-size:16.5px;line-height:1.6;color:var(--fg-muted)}
html.pv-js .p2-m:not(.in) .p2-node{background:var(--card);color:var(--fg-muted);box-shadow:0 0 0 6px var(--bg-alt);border:2px solid var(--border);transform:scale(.86)}
html.pv-js .p2-m:not(.in) .p2-mc{opacity:.3;transform:translateX(20px)}
@media(max-width:900px){.p2-dgrid{grid-template-columns:1fr;gap:28px}.p2-dside{position:static}.p2-dhint{display:none}.p2-m{grid-template-columns:44px minmax(0,1fr);gap:14px}.p2-node{width:44px;height:44px}.p2-node svg{width:20px;height:20px}.p2-tl::before,.p2-tl::after{left:21px}.p2-mc{padding:20px 20px 16px}}

/* ---- outcomes ---- */
.p2-ogrid{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);gap:clamp(32px,5vw,84px);align-items:center}
.p2-prod{position:relative;margin:0;display:grid;place-items:center;min-height:400px}
.p2-prod img{position:relative;z-index:2;display:block;max-width:92%;max-height:440px;width:auto;height:auto;filter:drop-shadow(0 40px 40px rgba(0,0,0,.55));animation:p2-float 7s ease-in-out infinite}
.p2-prod.p2-light img{background:#fff;padding:22px;box-sizing:border-box;border-radius:24px;filter:none;box-shadow:0 50px 90px -30px rgba(0,0,0,.75),0 0 0 1px rgba(255,255,255,.16)}
.p2-halo{position:absolute;inset:4%;border-radius:50%;background:radial-gradient(circle,rgba(255,210,61,.3),transparent 64%)}
.p2-prod::before{content:"";position:absolute;left:50%;top:50%;width:min(92%,460px);aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;border:1px dashed rgba(255,210,61,.4)}
.p2-prod figcaption{position:absolute;z-index:3;bottom:2%;left:50%;transform:translateX(-50%);padding:8px 16px;border-radius:999px;background:rgba(7,16,31,.8);border:1px solid rgba(255,255,255,.2);color:#fff;font-size:14px;font-weight:700;white-space:nowrap;max-width:92%;overflow:hidden;text-overflow:ellipsis}
.p2-oclist{list-style:none;margin:0;padding:0;display:grid;gap:12px}
.p2-oc{display:grid;grid-template-columns:56px minmax(0,1fr);gap:18px;align-items:center;padding:14px 20px 14px 14px;border:1px solid var(--border);border-radius:18px;background:var(--card);transition:border-color .3s,transform .3s}
.p2-oc:hover{border-color:var(--q-gold);transform:translateX(4px)}
.p2-chk{width:56px;height:56px;border-radius:50%;background:var(--q-gold);color:#111;display:grid;place-items:center;box-shadow:0 12px 26px -10px rgba(255,210,61,.7)}
.p2-chk svg{width:30px;height:30px}.p2-chk path{stroke-dasharray:1;stroke-dashoffset:0}
html.pv-js .p2-rv:not(.in) .p2-chk path{stroke-dashoffset:1}
html.pv-js .p2-rv.in .p2-chk path{transition:stroke-dashoffset .7s cubic-bezier(.4,0,.2,1) calc(.25s + var(--i,0)*80ms)}
.p2-oc b{display:block;font-size:18px;line-height:1.3;color:var(--fg)}
.p2-oc b em{font-style:normal;margin-left:10px;font-size:13px;padding:3px 10px;border-radius:999px;background:rgba(255,210,61,.16);color:var(--q-gold);font-weight:800;white-space:nowrap}
.p2-oc div>span{display:block;font-size:15px;line-height:1.5;color:var(--fg-muted);margin-top:4px}
@media(max-width:900px){.p2-ogrid{grid-template-columns:1fr}.p2-prod{min-height:300px;order:-1}.p2-prod img{max-height:300px}.p2-oc{grid-template-columns:44px minmax(0,1fr);gap:14px}.p2-chk{width:44px;height:44px}.p2-chk svg{width:24px;height:24px}}

/* ---- closing band ---- */
.p2-cta{position:relative;overflow:hidden;background:var(--q-gold);color:#111;padding:clamp(52px,7vw,92px) 0!important;isolation:isolate}
.p2-cbg{position:absolute;inset:0;z-index:-1;background:repeating-linear-gradient(-45deg,rgba(0,0,0,.055) 0 2px,transparent 2px 24px),radial-gradient(760px 380px at 92% 0%,rgba(255,255,255,.45),transparent 62%)}
.p2-cwrap{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,.85fr);gap:clamp(24px,4vw,56px);align-items:center}
.p2-ceb{font-size:13px;letter-spacing:.18em;text-transform:uppercase;font-weight:800;margin-bottom:16px;display:flex;align-items:center;gap:12px}.p2-ceb::before{content:"";width:34px;height:3px;background:#111}
.p2-cta h2{font-family:var(--q-sans);font-weight:800;font-size:clamp(34px,5vw,70px);line-height:1;letter-spacing:-.035em;margin:0;color:#111;text-wrap:balance}
.p2-ctxt p{margin:20px 0 0;font-size:clamp(17px,1.5vw,20px);line-height:1.55;color:rgba(17,17,17,.82);max-width:620px}
.p2-cbtns{display:grid;gap:12px;justify-items:stretch}
.p2-b{display:inline-flex;align-items:center;justify-content:center;gap:12px;min-height:60px;padding:0 28px;border-radius:8px;font-weight:800;font-size:17px;line-height:1.2;text-decoration:none;text-align:center;transition:transform .25s,box-shadow .25s,background .25s,color .25s}
.p2-b1{background:#111;color:var(--q-gold);box-shadow:0 18px 36px -16px rgba(0,0,0,.6)}.p2-b1:hover{transform:translateY(-3px);box-shadow:0 26px 40px -16px rgba(0,0,0,.65)}
.p2-b1 svg{transition:transform .25s}.p2-b1:hover svg{transform:translateX(5px)}
.p2-b2{border:2px solid #111;color:#111}.p2-b2:hover{background:#111;color:var(--q-gold)}
.p2-b:focus-visible{outline:3px solid #111;outline-offset:3px}
.p2-cnote{margin:6px 0 0;font-size:14px;font-weight:600;color:rgba(17,17,17,.75);text-align:center}
[data-dir="showcase"] .p2-b{border-radius:999px}[data-dir="press"] .p2-b{border-radius:2px}[data-dir="press"] .p2-cta h2{font-family:var(--q-serif);font-weight:500;letter-spacing:-.02em}
@media(max-width:900px){.p2-cwrap{grid-template-columns:1fr}}

/* ---- about: numbers ---- */
.p2-ngrid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid rgba(255,255,255,.16)}
.p2-nm{padding:34px 28px 32px 0;border-bottom:1px solid rgba(255,255,255,.16);position:relative}
.p2-nm:not(:nth-child(3n+1)){padding-left:28px;border-left:1px solid rgba(255,255,255,.12)}
.p2-big{display:block;font-family:var(--q-sans);font-weight:800;font-size:clamp(52px,8.6vw,128px);line-height:.95;letter-spacing:-.05em;color:var(--q-gold);font-variant-numeric:tabular-nums}
@supports ((-webkit-background-clip:text) or (background-clip:text)){.p2-big{color:transparent;background:linear-gradient(180deg,#fff 10%,#ffd23d 110%);-webkit-background-clip:text;background-clip:text}}
.p2-nm span{display:block;margin-top:14px;font-size:16px;line-height:1.45;color:var(--fg-muted);max-width:24ch}
.p2-nsrc{margin:22px 0 0;font-size:14px;color:var(--fg-muted)}
[data-dir="press"] .p2-big{font-family:var(--q-serif);font-weight:500}
@media(max-width:900px){.p2-ngrid{grid-template-columns:repeat(2,minmax(0,1fr))}.p2-nm,.p2-nm:not(:nth-child(3n+1)){padding:26px 16px 26px 0;border-left:0}.p2-nm:nth-child(2n){padding-left:20px;border-left:1px solid rgba(255,255,255,.12)}}

/* ---- about: leaders ---- */
.p2-lgroup{margin-top:40px}.p2-lgh{display:flex;align-items:center;gap:14px;margin:0 0 18px;font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--q-gold);font-weight:800}
.p2-lgh::after{content:"";flex:1;height:1px;background:var(--border)}.p2-lgh i{font-style:normal;order:2;padding:2px 10px;border-radius:999px;border:1px solid var(--border);color:var(--fg-muted)}
.p2-lgrid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.p2-lp{position:relative;overflow:hidden;min-height:236px;padding:20px 20px 20px;border:1px solid var(--border);border-radius:18px;background:var(--card);display:flex;flex-direction:column;justify-content:flex-end;gap:4px;outline:none;transition:border-color .3s,transform .3s,box-shadow .3s}
.p2-lp:hover,.p2-lp:focus-visible{border-color:var(--q-gold);transform:translateY(-4px);box-shadow:0 26px 50px -26px rgba(0,0,0,.7)}
.p2-lp:focus-visible{outline:3px solid var(--q-gold);outline-offset:3px}
.p2-lmono{position:absolute;left:0;right:0;top:0;height:128px;display:grid;place-items:center;background:linear-gradient(135deg,rgba(255,210,61,.24),rgba(255,210,61,.04));border-bottom:1px solid var(--border)}
.p2-lmono em{font-style:normal;font-family:var(--q-sans);font-weight:800;font-size:56px;letter-spacing:-.04em;color:var(--q-gold)}
.p2-lname{font-weight:800;font-size:19px;color:var(--fg)}.p2-ltitle{font-size:14.5px;line-height:1.4;color:var(--fg-muted)}
.p2-lrev{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;padding:22px;background:linear-gradient(160deg,var(--q-gold),#ffe27a);color:#111;transform:translateY(102%);transition:transform .42s cubic-bezier(.2,.7,.2,1)}
.p2-lp:hover .p2-lrev,.p2-lp:focus-visible .p2-lrev{transform:none}
.p2-lrev i{font-style:normal;font-size:13px;letter-spacing:.16em;text-transform:uppercase;font-weight:800}.p2-lrev b{font-size:24px;line-height:1.12;margin-top:6px;letter-spacing:-.02em}
@media(hover:none){.p2-lrev{position:static;transform:none;background:none;color:var(--q-gold);padding:6px 0 0;flex-direction:row;gap:8px;align-items:baseline}.p2-lrev b{font-size:14.5px;margin:0}.p2-lrev-r{display:none}}
.p2-orgs{margin-top:44px;padding-top:24px;border-top:1px solid var(--border)}.p2-orgs p{margin:0 0 14px;font-size:15px;color:var(--fg-muted)}
.p2-orgs div{display:flex;flex-wrap:wrap;gap:10px}.p2-orgs span{padding:8px 14px;border:1px solid var(--border);border-radius:999px;font-size:14px;color:var(--fg);background:var(--card)}
[data-dir="press"] .p2-lp,[data-dir="press"] .p2-mc,[data-dir="press"] .p2-oc{border-radius:2px}
@media(max-width:1024px){.p2-lgrid{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:768px){.p2-lgrid{grid-template-columns:repeat(2,minmax(0,1fr))}.p2-lp{min-height:210px}.p2-lmono{height:104px}.p2-lmono em{font-size:44px}}
@media(max-width:420px){.p2-lname{font-size:17px}}

/* ---- about: quote ---- */
.p2-quote{position:relative;padding:0!important;min-height:min(80vh,720px);display:flex;align-items:center;overflow:hidden;isolation:isolate;color:#fff}
.p2-qimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2}
.p2-qshade{position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(5,10,24,.9),rgba(5,10,24,.58) 62%,rgba(5,10,24,.32)),linear-gradient(0deg,rgba(5,10,24,.55),transparent 50%)}
.p2-qwrap{position:relative;padding-top:92px;padding-bottom:92px}
.p2-qmark{display:block;font-family:Georgia,serif;font-size:clamp(120px,15vw,210px);line-height:.7;height:.42em;color:var(--q-gold);margin-bottom:28px}
.p2-quote blockquote{margin:0;max-width:900px}
.p2-qtext{margin:0;font-family:var(--q-sans);font-weight:800;font-size:clamp(28px,4.4vw,62px);line-height:1.06;letter-spacing:-.035em;color:#fff;text-wrap:balance}
.p2-qsub{margin:22px 0 0;font-size:clamp(18px,1.8vw,24px);line-height:1.5;color:rgba(255,255,255,.88);max-width:640px}
.p2-quote footer{margin-top:30px;font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--q-gold);font-weight:800;display:flex;align-items:center;gap:14px}.p2-quote footer::before{content:"";width:40px;height:3px;background:var(--q-gold)}
[data-dir="press"] .p2-qtext{font-family:var(--q-serif);font-weight:500;letter-spacing:-.02em}

/* ---- contact: router ---- */
.p2-rt{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);gap:clamp(24px,4vw,56px);align-items:start}
.p2-rt-picks{display:none;gap:12px}html.pv-js .p2-rt-picks{display:grid}
.p2-rt-pick{display:grid;grid-template-columns:52px minmax(0,1fr) 24px;gap:16px;align-items:center;text-align:left;padding:16px 20px 16px 16px;min-height:88px;border-radius:var(--radius);border:1px solid var(--border);background:var(--card);color:var(--fg);font:inherit;cursor:pointer;transition:border-color .25s,background .25s,transform .25s,box-shadow .25s}
.p2-rt-pick:hover{border-color:var(--q-gold);transform:translateX(4px)}
.p2-rt-pick:focus-visible{outline:3px solid var(--accent-ink);outline-offset:3px}
.p2-rt-i{width:52px;height:52px;border-radius:14px;display:grid;place-items:center;background:color-mix(in srgb,var(--q-gold) 20%,var(--card));color:var(--accent-ink)}
.p2-rt-t b{display:block;font-size:18px;line-height:1.25}.p2-rt-t small{display:block;font-size:14.5px;color:var(--fg-muted);margin-top:2px}
.p2-rt-a{color:var(--accent-ink);opacity:.6;transition:transform .25s}
.p2-rt-pick[aria-selected=true]{background:var(--q-gold);border-color:var(--q-gold);color:#111;box-shadow:0 20px 40px -22px rgba(255,210,61,.9)}
.p2-rt-pick[aria-selected=true] .p2-rt-i{background:rgba(0,0,0,.12);color:#111}.p2-rt-pick[aria-selected=true] small{color:rgba(17,17,17,.78)}.p2-rt-pick[aria-selected=true] .p2-rt-a{color:#111;opacity:1;transform:translateX(4px)}
.p2-rt-stage{position:relative;min-height:420px;border-radius:calc(var(--radius) + 8px);border:1px solid var(--border);background:var(--card);box-shadow:0 30px 70px -40px rgba(17,24,39,.45);overflow:hidden}
.p2-rt-empty{display:none;position:absolute;inset:0;place-content:center;justify-items:center;text-align:center;gap:10px;padding:30px;color:var(--fg-muted)}
.p2-rt-empty span{color:var(--q-gold)}.p2-rt-empty b{font-size:22px;color:var(--fg)}.p2-rt-empty small{font-size:15px;max-width:30ch}
html.pv-js .p2-rt:not(.has) .p2-rt-empty{display:grid}
html.pv-js .p2-rt-panel{display:none}html.pv-js .p2-rt-panel.on{display:block;animation:p2-in .45s cubic-bezier(.2,.7,.2,1)}
html:not(.pv-js) .p2-rt{grid-template-columns:1fr}html:not(.pv-js) .p2-rt-stage{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border:0;box-shadow:none;background:none;gap:18px;overflow:visible}html:not(.pv-js) .p2-rt-panel{border:1px solid var(--border);border-radius:var(--radius);background:var(--card)}
.p2-rt-panel{padding:30px 30px 10px}.p2-rt-ph{position:relative;margin-bottom:12px;padding-right:64px}
.p2-rt-no{position:absolute;right:0;top:-8px;font:800 54px var(--q-sans);color:transparent;-webkit-text-stroke:1.5px color-mix(in srgb,var(--q-gold) 75%,transparent)}
.p2-rt-ph h3{margin:0 0 6px;font-size:clamp(22px,2.3vw,29px);line-height:1.15;letter-spacing:-.02em;color:var(--fg)}.p2-rt-ph p{margin:0;color:var(--fg-muted);font-size:16px}
.p2-acts{list-style:none;margin:0;padding:0}
.p2-act{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;align-items:center;border-top:1px solid var(--border)}
.p2-act>a{display:grid;grid-template-columns:44px minmax(0,1fr) 20px;gap:14px;align-items:center;padding:14px 4px;min-height:72px;text-decoration:none;color:var(--fg)}
.p2-act-tel>a{grid-template-columns:44px minmax(0,1fr)}.p2-act:not(.p2-act-tel){grid-template-columns:1fr}
.p2-act-i{width:44px;height:44px;border-radius:12px;display:grid;place-items:center;background:color-mix(in srgb,var(--q-gold) 20%,var(--card));color:var(--accent-ink)}
.p2-act-t b{display:block;font-size:17px;line-height:1.25}.p2-act-t em{display:block;font-style:normal;font-family:var(--q-sans);font-weight:800;font-size:clamp(24px,2.6vw,32px);letter-spacing:-.02em;line-height:1.15}
.p2-act-t small{display:block;font-size:14.5px;line-height:1.45;color:var(--fg-muted);margin-top:2px}
.p2-act-go{color:var(--accent-ink);transition:transform .25s}.p2-act>a:hover .p2-act-go{transform:translateX(5px)}.p2-act>a:hover b{text-decoration:underline;text-underline-offset:3px}
.p2-act>a:focus-visible{outline:3px solid var(--accent-ink);outline-offset:2px}
.p2-act-side{display:flex;flex-direction:column;align-items:flex-end;gap:6px}
.p2-hrs{font-size:13.5px;font-weight:700;padding:5px 12px;border-radius:999px;border:1px solid var(--border);white-space:nowrap;color:var(--fg)}
.p2-open{display:inline-flex;align-items:center;gap:7px;font-size:13px;font-weight:800;padding:4px 11px;border-radius:999px;background:rgba(22,163,74,.14);color:#15803d;white-space:nowrap;letter-spacing:.02em}
.p2-open[hidden]{display:none}
.p2-open::before{content:"";width:8px;height:8px;border-radius:50%;background:currentColor;animation:p2-blink 2s ease-in-out infinite}
.p2-open.is-closed{background:rgba(100,116,139,.16);color:var(--fg-muted)}.p2-open.is-closed::before{animation:none;opacity:.7}
.lf-dark .p2-open:not(.is-closed),.pv-dark .p2-open:not(.is-closed){background:rgba(74,222,128,.15);color:#4ade80}
.p2-hrow{display:flex;flex-wrap:wrap;align-items:center;gap:8px 10px;margin-top:4px}.p2-hrow .cd-hrs{margin-top:0}
@keyframes p2-blink{0%,100%{opacity:1}50%{opacity:.35}}
.p2-rt-note{margin:20px 0 0;font-size:14px;color:var(--fg-muted)}
@media(max-width:900px){.p2-rt{grid-template-columns:1fr}.p2-rt-stage{min-height:0}html:not(.pv-js) .p2-rt-stage{grid-template-columns:1fr}.p2-rt-panel{padding:24px 18px 6px}.p2-act-tel{grid-template-columns:1fr}.p2-act-side{flex-direction:row;align-items:center;padding:0 0 12px 58px;flex-wrap:wrap}}

/* ---- support: chooser and FAQ grid ---- */
.p2-search{max-width:860px;margin:0 0 38px;display:none}html.pv-js .p2-search{display:block}
.p2-slab{display:block;margin-bottom:12px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:800;color:var(--q-gold)}
.p2-sbox{display:flex;align-items:center;gap:14px;padding:0 20px;min-height:68px;border-radius:999px;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.28);color:var(--q-gold);transition:border-color .25s,box-shadow .25s,background .25s}
.p2-sbox:focus-within{border-color:var(--q-gold);box-shadow:0 0 0 4px rgba(255,210,61,.22);background:rgba(255,255,255,.12)}
.p2-sbox input{flex:1;min-width:0;min-height:60px;background:none;border:0;outline:0;color:#fff;font:600 19px var(--q-sans)}
.p2-sbox input::placeholder{color:rgba(255,255,255,.58)}.p2-sbox input::-webkit-search-cancel-button{filter:invert(1)}
.p2-sbox kbd{font:700 13px var(--q-sans);padding:5px 10px;border:1px solid rgba(255,255,255,.3);border-radius:8px;color:rgba(255,255,255,.75)}
.p2-res{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:8px}.p2-res[hidden],.p2-sempty[hidden]{display:none}
.p2-res a{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:14px;align-items:center;padding:14px 18px;min-height:64px;border-radius:14px;border:1px solid var(--border);background:var(--card);text-decoration:none;color:var(--fg);transition:border-color .2s,transform .2s}
.p2-res a:hover,.p2-res a:focus-visible,.p2-res a.sel{border-color:var(--q-gold);transform:translateX(4px)}.p2-res b{display:block;font-size:16.5px}.p2-res small{display:block;font-size:14px;color:var(--fg-muted);line-height:1.4}.p2-res mark{background:rgba(255,210,61,.3);color:inherit;border-radius:3px}
.p2-res span.g{color:var(--q-gold)}.p2-sempty{margin:14px 0 0;font-size:16px;color:var(--fg-muted)}
.p2-needs-h{display:flex;align-items:center;gap:14px;margin-bottom:16px;font-size:13px;letter-spacing:.16em;text-transform:uppercase;font-weight:800;color:var(--fg-muted)}.p2-needs-h::after{content:"";flex:1;height:1px;background:var(--border)}
.p2-needs{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.p2-need{display:flex;flex-direction:column;gap:16px;height:100%;padding:26px 24px 22px;border-radius:calc(var(--radius) + 6px);border:1px solid var(--border);background:var(--card);text-decoration:none;color:var(--fg);transition:transform .3s,border-color .3s,box-shadow .3s}
.p2-need:hover{transform:translateY(-6px);border-color:var(--q-gold);box-shadow:0 30px 50px -28px rgba(0,0,0,.7)}.p2-need:focus-visible{outline:3px solid var(--q-gold);outline-offset:3px}
.p2-need-i{width:56px;height:56px;border-radius:16px;display:grid;place-items:center;background:var(--q-gold);color:#111}
.p2-need-t b{display:block;font-size:20px;line-height:1.2;color:var(--fg)}.p2-need-t small{display:block;margin-top:8px;font-size:15px;line-height:1.5;color:var(--fg-muted)}
.p2-need-go{margin-top:auto;color:var(--q-gold);transition:transform .25s}.p2-need:hover .p2-need-go{transform:translateX(6px)}
.p2-fgrid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.p2-fc{display:flex;flex-direction:column;gap:8px;height:100%;padding:24px 22px 20px;border:1px solid var(--border);border-radius:calc(var(--radius) + 4px);background:var(--card);text-decoration:none;color:var(--fg);transition:transform .3s,border-color .3s,box-shadow .3s}
.p2-fc:hover{transform:translateY(-5px);border-color:var(--q-gold);box-shadow:0 24px 40px -26px rgba(17,24,39,.4)}.p2-fc:focus-visible{outline:3px solid var(--accent-ink);outline-offset:3px}
.p2-fc-i{width:48px;height:48px;border-radius:14px;display:grid;place-items:center;background:color-mix(in srgb,var(--q-gold) 22%,var(--card));color:var(--accent-ink);margin-bottom:6px}
.p2-fc b{font-size:18px;line-height:1.25}.p2-fc small{font-size:14.5px;line-height:1.5;color:var(--fg-muted);flex:1}
.p2-fc-n{font:800 32px/1 var(--q-sans);color:var(--accent-ink);margin-top:8px;letter-spacing:-.03em}.p2-fc-n i{font:600 14px var(--q-sans);font-style:normal;color:var(--fg-muted);letter-spacing:0}
@media(max-width:1100px){.p2-needs,.p2-fgrid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:560px){.p2-needs,.p2-fgrid{grid-template-columns:1fr}.p2-sbox kbd{display:none}.p2-sbox input{font-size:17px}}

/* ---- partners ---- */
.p2-net{position:relative;margin:0 auto 56px;max-width:1040px;aspect-ratio:16/10;border-radius:28px;background:radial-gradient(800px 380px at 50% 50%,rgba(255,210,61,.18),transparent 65%),linear-gradient(165deg,#121c30,#0b1220);border:1px solid rgba(255,255,255,.12);box-shadow:0 40px 80px -40px rgba(0,5,69,.6);color:#fff}
.p2-net::before{content:"";position:absolute;inset:0;border-radius:inherit;opacity:.5;background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:44px 44px;mask-image:radial-gradient(ellipse at 50% 50%,#000,transparent 75%);-webkit-mask-image:radial-gradient(ellipse at 50% 50%,#000,transparent 75%)}
.p2-net-l{position:absolute;inset:0;width:100%;height:100%}.p2-net-l ellipse{fill:none;stroke:rgba(255,255,255,.14);stroke-dasharray:2 5;vector-effect:non-scaling-stroke}
.p2-net-l line{stroke:rgba(255,210,61,.55);stroke-width:1.4;vector-effect:non-scaling-stroke;stroke-dasharray:4 5;animation:p2-dash 1.6s linear infinite}.p2-pulse{fill:#ffd23d}
.p2-hub{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:2;width:clamp(120px,17%,170px);aspect-ratio:1;border-radius:50%;display:grid;place-content:center;text-align:center;background:var(--q-gold);color:#111;box-shadow:0 0 0 10px rgba(255,210,61,.16),0 30px 60px -20px rgba(255,210,61,.55)}
.p2-hub b{font:800 clamp(28px,3.2vw,44px)/1 var(--q-sans);letter-spacing:-.04em}.p2-hub small{font-size:13px;font-weight:700;margin-top:4px;padding:0 10px}
.p2-hub-r{position:absolute;inset:-14px;border-radius:50%;border:1.5px solid rgba(255,210,61,.55);animation:p2-ping 3.2s ease-out infinite}.p2-hub-r.r2{animation-delay:1.6s}
.p2-pn{position:absolute;z-index:3;transform:translate(-50%,-50%);display:grid;grid-template-columns:auto 1fr;column-gap:10px;align-items:center;padding:9px 18px 9px 9px;min-height:52px;border-radius:999px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.24);color:#fff;text-decoration:none;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);white-space:nowrap;transition:background .25s,color .25s,border-color .25s,box-shadow .25s}
.p2-pn-i{grid-row:1/3;width:38px;height:38px;border-radius:50%;background:var(--q-gold);color:#111;display:grid;place-items:center}
.p2-pn b{font-size:15px;line-height:1.2;text-align:left}.p2-pn small{font-size:13px;color:rgba(255,255,255,.72);text-align:left}
.p2-pn:hover,.p2-pn:focus-visible{background:var(--q-gold);color:#111;border-color:var(--q-gold);box-shadow:0 0 0 6px rgba(255,210,61,.22)}.p2-pn:hover small,.p2-pn:focus-visible small{color:rgba(17,17,17,.75)}.p2-pn:hover .p2-pn-i,.p2-pn:focus-visible .p2-pn-i{background:#111;color:var(--q-gold)}
.p2-pn:focus-visible{outline:3px solid #fff;outline-offset:3px}
.p2-pcards{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.p2-pc{position:relative;display:flex;flex-direction:column;gap:12px;height:100%;padding:26px 24px 22px;border:1px solid var(--border);border-radius:calc(var(--radius) + 6px);background:var(--card);text-decoration:none;color:var(--fg);overflow:hidden;transition:transform .3s,border-color .3s,box-shadow .3s}
.p2-pc::before{content:"";position:absolute;left:0;top:0;height:4px;width:36%;background:linear-gradient(90deg,var(--q-gold),transparent);transition:width .5s cubic-bezier(.2,.7,.2,1)}.p2-pc:hover::before{width:100%}
.p2-pc:hover{transform:translateY(-6px);border-color:var(--q-gold);box-shadow:0 30px 50px -28px rgba(17,24,39,.4)}.p2-pc:focus-visible{outline:3px solid var(--accent-ink);outline-offset:3px}
.p2-pc-top{display:flex;align-items:center;justify-content:space-between;gap:10px}
.p2-pc-i{width:52px;height:52px;border-radius:14px;display:grid;place-items:center;background:color-mix(in srgb,var(--q-gold) 22%,var(--card));color:var(--accent-ink)}
.p2-pc-cat{font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:800;color:var(--accent-ink);text-align:right}
.p2-pc h3{margin:4px 0 0;font-size:24px;letter-spacing:-.02em;color:var(--fg)}.p2-pc p{margin:0;font-size:15.5px;line-height:1.55;color:var(--fg-muted)}
.p2-pc-w{margin-top:auto}.p2-pc-w i,.p2-pc-req i{display:block;font-style:normal;font-size:13px;letter-spacing:.1em;text-transform:uppercase;font-weight:800;color:var(--fg-muted);margin-bottom:6px}
.p2-pc-w div{display:flex;flex-wrap:wrap;gap:6px}.p2-pc-w span{font-size:13.5px;font-weight:600;padding:4px 11px;border-radius:999px;background:var(--bg-alt);border:1px solid var(--border)}
.p2-pc-req{margin:0;font-size:14.5px;line-height:1.45;color:var(--fg);padding-top:12px;border-top:1px dashed var(--border)}
.p2-pc-go{font-size:14.5px;font-weight:700;color:var(--accent-ink)}
[data-dir="press"] .p2-pc,[data-dir="press"] .p2-net,[data-dir="press"] .p2-mo,[data-dir="press"] .p2-fc,[data-dir="press"] .p2-need,[data-dir="press"] .p2-rt-stage{border-radius:2px}
@media(max-width:1024px){.p2-pcards{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:820px){.p2-net{aspect-ratio:auto;padding:28px 16px 22px;display:grid;gap:12px;border-radius:22px}.p2-net-l{display:none}.p2-hub{position:relative;left:auto;top:auto;transform:none;margin:0 auto 14px;width:132px}.p2-pn{position:static;transform:none;white-space:normal;width:100%}}
@media(max-width:640px){.p2-pcards{grid-template-columns:1fr}}

/* ---- training board ---- */
.p2-months{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;align-items:start}
.p2-mo{background:var(--card);border:1px solid var(--border);border-radius:calc(var(--radius) + 6px);overflow:hidden;box-shadow:0 20px 44px -32px rgba(17,24,39,.45)}
.p2-mo-h{display:flex;align-items:baseline;justify-content:space-between;gap:10px;padding:16px 20px;background:linear-gradient(165deg,#121c30,#0b1220);color:#fff}
.p2-mo-h b{font:800 28px/1 var(--q-sans);letter-spacing:-.03em}.p2-mo-h span{font:800 15px var(--q-sans);color:var(--q-gold);letter-spacing:.06em}
.p2-mo ul{list-style:none;margin:0;padding:14px;display:grid;gap:12px}
.p2-tk{position:relative;display:grid;grid-template-columns:1fr;gap:12px;padding:14px;border:1px solid var(--border);border-radius:14px;background:var(--bg-alt)}
.p2-tk-d{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;border-radius:12px;background:var(--q-gold);color:#111;padding:10px 14px}
.p2-tk-d b{display:inline-flex;align-items:baseline;gap:8px;font:800 30px/1.05 var(--q-sans);letter-spacing:-.03em}.p2-tk-d b em{font-style:normal;font-size:14px;font-weight:700;opacity:.7;letter-spacing:0}
.p2-tk-d i{font-style:normal;font-size:13.5px;font-weight:700;line-height:1.2}
.p2-tk-k{display:block;font-size:13px;letter-spacing:.1em;text-transform:uppercase;font-weight:800;color:var(--accent-ink)}
.p2-tk-b>b{display:block;font-size:16.5px;line-height:1.25;margin:4px 0 6px;color:var(--fg)}.p2-tk-b small{display:flex;gap:6px;align-items:center;font-size:14px;color:var(--fg-muted)}.p2-tk-b small svg{flex:none}
.p2-tk-s{display:block;font-size:14px;line-height:1.5;color:var(--fg-muted);margin-top:8px}
.p2-tk.is-past{opacity:.5}.p2-tk-next{position:absolute;right:12px;top:-11px;background:#111;color:var(--q-gold);padding:4px 12px;border-radius:999px;font-size:13px;font-weight:800}.p2-tk-next[hidden]{display:none}
.p2-tk.is-next{border-color:var(--q-gold);box-shadow:0 0 0 3px rgba(255,210,61,.3)}
.p2-board-cta{display:flex;flex-wrap:wrap;gap:16px 24px;align-items:center;margin-top:34px}.p2-board-cta p{margin:0;font-size:15px;color:var(--fg-muted)}
@media(max-width:1180px){.p2-months{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:640px){.p2-months{grid-template-columns:1fr}}

/* ---- blog: toc and takeaways ---- */
.p2-toc{position:sticky;top:var(--p2-top,0);z-index:40;background:color-mix(in srgb,var(--bg) 93%,transparent);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--border)}
.p2-toc-in{display:flex;align-items:center;gap:18px;min-height:60px}.p2-toc-l{flex:none;font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:800;color:var(--fg-muted)}
.p2-toc-s{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding:8px 2px;min-width:0;flex:1}.p2-toc-s::-webkit-scrollbar{display:none}
.p2-toc a{flex:none;display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px 0 8px;border-radius:999px;border:1px solid var(--border);text-decoration:none;color:var(--fg);font-size:14px;font-weight:600;max-width:270px;background:var(--card);transition:background .2s,border-color .2s}
.p2-toc a b{flex:none;width:28px;height:28px;border-radius:50%;display:grid;place-items:center;background:var(--bg-alt);font-size:13px}.p2-toc a span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.p2-toc a:hover{border-color:var(--q-gold)}.p2-toc a:focus-visible{outline:3px solid var(--accent-ink);outline-offset:2px}.p2-toc a.on{background:var(--q-gold);border-color:var(--q-gold);color:#111}.p2-toc a.on b{background:rgba(0,0,0,.14)}
.p2-toc-p{position:absolute;left:0;bottom:-1px;height:3px;width:100%;background:var(--q-gold);transform:scaleX(var(--p,0));transform-origin:0 50%}
.p2-toc ~ .q-section[id]{scroll-margin-top:132px}
.p2-takegrid{display:grid;grid-template-columns:minmax(0,.7fr) minmax(0,1.3fr);gap:clamp(28px,5vw,72px);align-items:start}
.p2-takelist{list-style:none;margin:0;padding:0;display:grid;gap:14px}
.p2-takelist li{display:grid;grid-template-columns:44px minmax(0,1fr);gap:16px;padding:18px 22px 18px 18px;border-left:3px solid var(--q-gold);background:rgba(255,255,255,.055);border-radius:0 14px 14px 0}
.p2-ky{width:44px;height:44px;border-radius:50%;background:var(--q-gold);color:#111;display:grid;place-items:center}
.p2-takelist b{display:block;font-size:17.5px;line-height:1.3;color:#fff}.p2-takelist p{margin:6px 0 0;color:var(--fg-muted);font-size:15.5px;line-height:1.55}
@media(max-width:900px){.p2-takegrid{grid-template-columns:1fr}.p2-toc-l{display:none}}

/* ---- audience: dealer path ---- */
.p2-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));position:relative}
.p2-steps::before{content:"";position:absolute;left:10%;right:10%;top:34px;height:3px;background:repeating-linear-gradient(90deg,var(--q-gold) 0 10px,transparent 10px 18px)}
.p2-st{position:relative;padding:0 14px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:8px}
.p2-st-i{position:relative;z-index:1;width:68px;height:68px;border-radius:50%;background:var(--q-gold);color:#111;display:grid;place-items:center;box-shadow:0 0 0 8px var(--bg-alt),0 18px 30px -14px rgba(255,210,61,.8)}
.p2-st-n{position:absolute;z-index:2;top:-8px;left:calc(50% + 16px);width:28px;height:28px;border-radius:50%;background:#111;color:var(--q-gold);font:800 14px var(--q-sans);display:grid;place-items:center}
.p2-st h3{margin:8px 0 0;font-size:21px;letter-spacing:-.02em;color:var(--fg)}.p2-st p{margin:0;font-size:15px;line-height:1.55;color:var(--fg-muted);max-width:26ch}
@media(max-width:900px){.p2-steps{grid-template-columns:1fr;gap:26px}.p2-steps::before{left:33px;right:auto;top:20px;bottom:20px;width:3px;height:auto;background:repeating-linear-gradient(180deg,var(--q-gold) 0 10px,transparent 10px 18px)}.p2-st{display:grid;grid-template-columns:68px minmax(0,1fr);column-gap:18px;text-align:left;align-items:start;padding:0}.p2-st-i{grid-row:1/4}.p2-st-n{left:50px;top:-6px}.p2-st h3{margin:0}.p2-st p{max-width:none}}
/* spec pack stack */
.p2-stkgrid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(32px,6vw,88px);align-items:center}
.p2-stkb{list-style:none;margin:22px 0 28px;padding:0;display:grid;gap:10px}.p2-stkb li{position:relative;padding-left:30px;color:var(--fg-muted);font-size:16px;line-height:1.5}.p2-stkb li::before{content:"";position:absolute;left:0;top:.35em;width:16px;height:16px;border-radius:50%;background:var(--q-gold)}
.p2-files{position:relative;height:580px;perspective:1200px}
.p2-f{position:absolute;left:50%;width:min(92%,440px);border-radius:16px;padding:16px 22px;color:#111;background:#fff;box-shadow:0 30px 60px -24px rgba(0,0,0,.6);transition:transform .55s cubic-bezier(.2,.7,.2,1)}
.p2-f:not(.p2-f1){display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:nowrap;height:58px;overflow:hidden}.p2-f:not(.p2-f1) span{font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:800}.p2-f:not(.p2-f1) b{font:800 24px var(--q-sans);letter-spacing:-.03em}.p2-f:not(.p2-f1) i{display:none}
.p2-f4{top:0;background:#e3e9fb;transform:translateX(-50%) rotate(-3deg)}.p2-f3{top:60px;background:#fff0b8;transform:translateX(-50%) rotate(2.5deg)}.p2-f2{top:120px;background:#d9f2e2;transform:translateX(-50%) rotate(-1.5deg)}
.p2-f1{top:184px;z-index:5;padding:30px 24px 22px;transform:translateX(-50%)}
.p2-ftab{position:absolute;top:-16px;left:22px;padding:6px 16px;border-radius:10px 10px 0 0;background:var(--q-gold);font-size:13px;font-weight:800;letter-spacing:.1em;text-transform:uppercase}
.p2-f1>b{display:block;font:800 21px/1.2 var(--q-sans);letter-spacing:-.02em;margin-bottom:12px}
.p2-f1 ul{list-style:none;margin:0;padding:0;display:grid;gap:0}.p2-f1 li{color:#111;display:flex;align-items:center;gap:10px;padding:8px 0;border-top:1px solid rgba(17,17,17,.12);font-size:15px;font-weight:600}.p2-f1 li span{color:#846600;display:grid;place-items:center}
.p2-files:hover .p2-f4{transform:translateX(-50%) translateY(-12px) rotate(-5deg)}.p2-files:hover .p2-f3{transform:translateX(-50%) translateY(-8px) rotate(4deg)}.p2-files:hover .p2-f2{transform:translateX(-50%) translateY(-4px) rotate(-2.5deg)}
html.pv-js .p2-files:not(.in) .p2-f{opacity:0;transform:translateX(-50%) translateY(60px)}html.pv-js .p2-files.in .p2-f{transition:opacity .6s,transform .8s cubic-bezier(.2,.7,.2,1)}
html.pv-js .p2-files.in .p2-f1{transition-delay:.0s}html.pv-js .p2-files.in .p2-f2{transition-delay:.15s}html.pv-js .p2-files.in .p2-f3{transition-delay:.3s}html.pv-js .p2-files.in .p2-f4{transition-delay:.45s}
@media(max-width:900px){.p2-stkgrid{grid-template-columns:1fr}}
/* six questions: flip cards */
.p2-flgrid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.p2-fl{perspective:1300px}
.p2-fl-in{position:relative;display:block;width:100%;min-height:290px;border:0;background:none;padding:0;cursor:pointer;font:inherit;text-align:left;color:inherit;transform-style:preserve-3d;transition:transform .75s cubic-bezier(.2,.7,.2,1)}
.p2-fl-in[aria-pressed=true]{transform:rotateY(180deg)}.p2-fl-in:focus-visible{outline:3px solid var(--accent-ink);outline-offset:4px;border-radius:20px}
.p2-fl-f,.p2-fl-b{position:absolute;inset:0;display:flex;flex-direction:column;padding:26px 26px 22px;border-radius:calc(var(--radius) + 8px);backface-visibility:hidden;-webkit-backface-visibility:hidden}
.p2-fl-f{background:var(--card);border:1px solid var(--border);box-shadow:0 20px 44px -30px rgba(17,24,39,.4)}.p2-fl-in:hover .p2-fl-f{border-color:var(--q-gold)}
.p2-fl-b{background:linear-gradient(160deg,var(--q-gold),#ffe27a);color:#111;transform:rotateY(180deg)}
.p2-fl-n{font:800 44px/1 var(--q-sans);color:transparent;-webkit-text-stroke:1.5px color-mix(in srgb,var(--q-gold) 80%,transparent);letter-spacing:-.04em}.p2-fl-b .p2-fl-n{-webkit-text-stroke:1.5px rgba(17,17,17,.4)}
.p2-fl-f>b{display:block;margin-top:14px;font-size:clamp(19px,1.7vw,22px);line-height:1.25;color:var(--fg);letter-spacing:-.01em}
.p2-fl-h{margin-top:auto;display:flex;align-items:center;gap:8px;font-size:14px;font-weight:800;color:var(--accent-ink)}
.p2-fl-b i{font-style:normal;margin-top:12px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:800;opacity:.75}.p2-fl-a{display:block;margin-top:8px;font-size:17px;line-height:1.5;font-weight:600}
.p2-fl-hint{margin:22px 0 0;font-size:14px;color:var(--fg-muted)}
html:not(.pv-js) .p2-fl-in{display:grid;gap:10px;min-height:0;transform:none}html:not(.pv-js) .p2-fl-f,html:not(.pv-js) .p2-fl-b{position:static;transform:none;backface-visibility:visible;-webkit-backface-visibility:visible}html:not(.pv-js) .p2-fl-hint,html:not(.pv-js) .p2-fl-h{display:none}
@media(max-width:1024px){.p2-flgrid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:640px){.p2-flgrid{grid-template-columns:1fr}.p2-fl-in{min-height:260px}}
@media(prefers-reduced-motion:reduce){.p2-fl-in{transition:none}}
/* one platform */
.p2-pl{display:grid;grid-template-columns:minmax(0,1fr) minmax(260px,420px) minmax(0,1fr);gap:28px 56px;align-items:center}
.p2-sats{display:contents;list-style:none}
.p2-sat{position:relative;align-self:stretch}.p2-sat a{height:100%;box-sizing:border-box}.p2-sat0{grid-column:1;grid-row:1}.p2-sat1{grid-column:3;grid-row:1}.p2-sat2{grid-column:1;grid-row:2}.p2-sat3{grid-column:3;grid-row:2}
.p2-sat a{display:block;position:relative;padding:24px 24px 22px;border:1px solid var(--border);border-radius:calc(var(--radius) + 6px);background:var(--card);text-decoration:none;color:var(--fg);transition:transform .3s,border-color .3s,box-shadow .3s}
.p2-sat a:hover{transform:translateY(-5px);border-color:var(--q-gold);box-shadow:0 26px 44px -28px rgba(17,24,39,.45)}.p2-sat a:focus-visible{outline:3px solid var(--accent-ink);outline-offset:3px}
.p2-sat a::after{content:"";position:absolute;top:50%;width:56px;border-top:2px dashed var(--q-gold)}.p2-sat0 a::after,.p2-sat2 a::after{left:100%}.p2-sat1 a::after,.p2-sat3 a::after{right:100%}
.p2-sat-i{width:48px;height:48px;border-radius:14px;display:grid;place-items:center;background:var(--q-gold);color:#111;margin-bottom:12px}.p2-sat b{display:block;font-size:21px;letter-spacing:-.02em}.p2-sat small{display:block;margin-top:6px;font-size:15px;line-height:1.5;color:var(--fg-muted)}
.p2-pl-core{grid-column:2;grid-row:1/3;position:relative;display:grid;place-items:center;align-content:center;gap:22px;min-height:420px}
.p2-pl-ring{position:absolute;left:50%;top:44%;width:min(100%,400px);aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,rgba(255,210,61,.3),transparent 65%)}
.p2-pl-ring::after{content:"";position:absolute;inset:6%;border-radius:50%;border:1px dashed color-mix(in srgb,var(--q-gold) 70%,transparent);animation:p2-ping 4s ease-out infinite}
.p2-pl-core img{position:relative;display:block;max-width:100%;max-height:340px;width:auto;height:auto;filter:drop-shadow(0 30px 30px rgba(0,5,69,.35));animation:p2-float 7s ease-in-out infinite}
.p2-pl-tags{position:relative;display:flex;flex-wrap:wrap;gap:8px;justify-content:center}.p2-pl-tags span{padding:7px 14px;border-radius:999px;background:#111;color:var(--q-gold);font-size:13px;font-weight:800;letter-spacing:.04em}
@media(max-width:1000px){.p2-pl{grid-template-columns:1fr 1fr;gap:18px}.p2-sats{display:contents}.p2-pl-core{grid-column:1/3;grid-row:1;min-height:340px}.p2-sat0{grid-column:1;grid-row:2}.p2-sat1{grid-column:2;grid-row:2}.p2-sat2{grid-column:1;grid-row:3}.p2-sat3{grid-column:2;grid-row:3}.p2-sat a::after{display:none}}
@media(max-width:560px){.p2-pl{grid-template-columns:1fr}.p2-pl-core{grid-column:1}.p2-sat0,.p2-sat1,.p2-sat2,.p2-sat3{grid-column:1}.p2-sat0{grid-row:2}.p2-sat1{grid-row:3}.p2-sat2{grid-row:4}.p2-sat3{grid-row:5}}

/* ---- portal sample dashboard ---- */
.p2-sample{margin-top:22px;padding-top:18px;border-top:1px dashed var(--border)}
.p2-sample-h{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin-bottom:14px}.p2-sample-h b{font:800 18px var(--q-sans);color:var(--fg)}.p2-sample-h small{flex-basis:100%;font-size:13.5px;line-height:1.45;color:var(--fg-muted)}
.p2-sd{display:inline-flex;align-items:center;font-size:13px;font-weight:800;padding:3px 10px;border-radius:999px;background:#111;color:var(--q-gold);letter-spacing:.06em;text-transform:uppercase}
.p2-sgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.p2-sc{padding:16px 18px 18px;border:1px solid var(--border);border-radius:var(--radius);background:var(--card);box-shadow:0 8px 20px rgba(0,5,69,.06);min-width:0}
.p2-sc h4{display:flex;justify-content:space-between;align-items:center;gap:8px;margin:0 0 12px;font-size:15.5px;color:var(--fg)}
.p2-sdocs{list-style:none;margin:0;padding:0;display:grid;gap:10px}.p2-sdocs li{display:grid;grid-template-columns:20px minmax(0,1fr) auto;gap:10px;align-items:center;font-size:14px;color:var(--fg)}.p2-sdocs svg{color:var(--accent-ink)}
.p2-sdocs b{display:block;font-weight:600;line-height:1.3}.p2-sdocs small{display:block;font-size:13px;color:var(--fg-muted)}.p2-sdocs em{font-style:normal;font-size:13px;color:var(--fg-muted);white-space:nowrap}
.p2-sord{margin:0}.p2-sord b{display:block;font-size:15px;color:var(--fg)}.p2-sord small{display:block;font-size:13.5px;color:var(--fg-muted);margin-top:2px}
.p2-ssteps{display:flex;list-style:none;margin:16px 0 0;padding:0}.p2-ssteps li{flex:1;position:relative;padding-top:24px;text-align:center;font-size:13px;color:var(--fg-muted)}
.p2-ssteps li i{position:absolute;top:0;left:50%;width:16px;height:16px;border-radius:50%;background:var(--border);transform:translateX(-50%);z-index:1}.p2-ssteps li::before{content:"";position:absolute;top:7px;left:-50%;width:100%;height:2px;background:var(--border)}.p2-ssteps li:first-child::before{display:none}
.p2-ssteps li.on{color:var(--fg);font-weight:700}.p2-ssteps li.on i,.p2-ssteps li.on::before{background:var(--q-gold)}
.p2-strain{display:grid;grid-template-columns:88px minmax(0,1fr);gap:14px;align-items:center}.p2-strain ul{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.p2-strain li{display:flex;justify-content:space-between;gap:10px;font-size:13.5px;color:var(--fg);line-height:1.35}.p2-strain em{font-style:normal;font-weight:700;color:var(--fg-muted);white-space:nowrap}.p2-strain li.done em{color:#15803d}.p2-strain li.mid em{color:var(--accent-ink)}
.p2-ring{width:88px;height:88px}.p2-ring circle{fill:none;stroke-width:8}.p2-ring .t{stroke:var(--border)}.p2-ring .v{stroke:var(--q-gold);stroke-linecap:round}.p2-ring text{font:800 18px var(--q-sans);fill:var(--fg)}
.p2-sas{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.p2-as-img{display:block;aspect-ratio:5/3;border-radius:10px;overflow:hidden;background:var(--bg-alt)}.p2-as-img img{width:100%;height:100%;object-fit:cover;display:block}
.p2-sas b{display:block;margin-top:8px;font-size:13.5px;line-height:1.25;color:var(--fg)}.p2-sas small{display:block;font-size:13px;line-height:1.3;color:var(--fg-muted);margin-top:2px}
.mo-screen.is-in .p2-sc{animation:p2-pop .55s cubic-bezier(.2,.8,.2,1) both}.mo-screen.is-in .p2-sc:nth-child(1){animation-delay:.9s}.mo-screen.is-in .p2-sc:nth-child(2){animation-delay:1s}.mo-screen.is-in .p2-sc:nth-child(3){animation-delay:1.1s}.mo-screen.is-in .p2-sc:nth-child(4){animation-delay:1.2s}
@media(max-width:1024px){.p2-sgrid{grid-template-columns:1fr}}@media(max-width:480px){.p2-sas{grid-template-columns:1fr 1fr}.p2-strain{grid-template-columns:1fr;justify-items:start}}

/* ---- finder: why this, compare ---- */
.mo-fc{position:relative}
.p2-why{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:14px 0 4px}.p2-why>i{font-style:normal;font-size:13px;font-weight:800;color:var(--accent-ink);text-transform:uppercase;letter-spacing:.1em;margin-right:2px}.p2-why-c{display:contents}
.p2-wc{font-size:13px;font-weight:600;padding:3px 10px;border-radius:999px;border:1px solid var(--border);background:var(--bg-alt);color:var(--fg-muted);line-height:1.4}
.p2-wc.on{background:var(--q-gold);border-color:var(--q-gold);color:#111;font-weight:800}.p2-wc.on::before{content:"\2713\00a0"}
.p2-soon{position:absolute;left:12px;top:12px;z-index:2;padding:5px 11px;border-radius:999px;background:#111;color:var(--q-gold);font-size:13px;font-weight:800}
.p2-cmp{display:none;position:absolute;right:12px;top:12px;z-index:3;align-items:center;gap:8px;min-height:44px;padding:0 14px 0 10px;border-radius:999px;border:1px solid var(--border);background:var(--card);color:var(--fg);font:700 14px var(--q-sans);cursor:pointer;box-shadow:0 8px 18px rgba(0,0,0,.14);transition:background .2s,color .2s,border-color .2s}
html.pv-js .p2-cmp{display:inline-flex}.p2-cmp:hover{border-color:var(--q-gold)}.p2-cmp:focus-visible{outline:3px solid var(--accent-ink);outline-offset:3px}
.p2-cmp-b{width:20px;height:20px;border-radius:6px;border:2px solid var(--border);display:grid;place-items:center;color:transparent}
.p2-cmp[aria-pressed=true]{background:#111;color:var(--q-gold);border-color:#111}.p2-cmp[aria-pressed=true] .p2-cmp-b{background:var(--q-gold);border-color:var(--q-gold);color:#111}
.p2-cmp[aria-disabled=true]{opacity:.5;cursor:not-allowed}
.p2-tray{position:fixed;left:16px;bottom:16px;z-index:95;width:min(820px,calc(100vw - 32px))}.p2-tray[hidden]{display:none}
.p2-tray-bar{display:flex;align-items:center;gap:12px;padding:10px 12px 10px 18px;background:#0b1220;color:#fff;border-radius:20px;border:1px solid rgba(255,255,255,.2);box-shadow:0 24px 60px rgba(0,0,0,.5)}
.p2-tray-t{display:flex;flex-direction:column;flex:none}.p2-tray-t b{font-size:15px}.p2-tray-t small{font-size:13px;color:rgba(255,255,255,.7)}
.p2-tray-sel{list-style:none;margin:0;padding:0;display:flex;gap:8px;flex:1;min-width:0;overflow:hidden}
.p2-tray-sel li{display:flex;align-items:center;gap:6px;min-width:0;padding:0 4px 0 12px;min-height:44px;border-radius:999px;background:rgba(255,255,255,.1);font-size:13.5px;font-weight:600}
.p2-tray-sel li span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:150px}
.p2-tray-sel li button{flex:none;width:36px;height:36px;border:0;border-radius:50%;background:none;color:#fff;font-size:20px;line-height:1;cursor:pointer}.p2-tray-sel li button:hover{background:rgba(255,255,255,.18)}
.p2-tray-go{flex:none;min-height:44px;padding:0 18px;border-radius:999px;border:0;background:var(--q-gold);color:#111;font:800 14.5px var(--q-sans);cursor:pointer}.p2-tray-go[disabled]{opacity:.4;cursor:not-allowed}
.p2-tray-clear{flex:none;min-height:44px;padding:0 10px;background:none;border:0;color:rgba(255,255,255,.75);font:600 14px var(--q-sans);cursor:pointer;text-decoration:underline}
.p2-tray button:focus-visible{outline:3px solid #fff;outline-offset:2px}
.p2-tray-panel{margin-bottom:10px;background:var(--card);color:var(--fg);border:1px solid var(--border);border-radius:20px;box-shadow:0 30px 70px rgba(0,0,0,.45);overflow:hidden}.p2-tray-panel[hidden]{display:none}
.p2-tray-scroll{max-height:min(56vh,480px);overflow:auto}
.p2-cmp-t{border-collapse:collapse;width:100%;min-width:560px;font-size:14.5px}.p2-cmp-t th,.p2-cmp-t td{padding:12px 16px;text-align:left;vertical-align:top;border-bottom:1px solid var(--border);line-height:1.4}
.p2-cmp-t thead th{position:sticky;top:0;background:var(--card);z-index:2;font-size:15.5px}.p2-cmp-t thead th a{color:var(--fg);text-decoration:none}.p2-cmp-t thead th small{display:block;font-weight:600;color:var(--accent-ink);margin-top:3px}
.p2-cmp-t tbody th{position:sticky;left:0;background:var(--bg-alt);z-index:1;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--fg-muted);width:150px}.p2-cmp-t td.na{color:var(--fg-muted);font-style:italic}
@media(min-width:1025px){.p2-tray{left:220px;width:min(720px,calc(100vw - 260px))}}
@media(max-width:767px){.p2-tray{bottom:78px;left:8px;width:calc(100vw - 16px)}.p2-tray-sel{display:none}.p2-tray-bar{justify-content:space-between}}
@media(prefers-reduced-motion:reduce){.p2-prod img,.p2-pl-core img,.p2-hub-r,.p2-pl-ring::after,.p2-net-l line,.p2-dhint span,.p2-open::before{animation:none}.p2-pulse{display:none}html.pv-js .p2-rv,html.pv-js .p2-rv.in{opacity:1;transform:none;transition:none}html.pv-js .p2-m:not(.in) .p2-mc{opacity:1;transform:none}.p2-rt-panel.on{animation:none}.mo-screen.is-in .p2-sc{animation:none}.p2-f,.p2-lrev{transition:none}html.pv-js .p2-files:not(.in) .p2-f{opacity:1;transform:translateX(-50%)}.p2-f4{transform:translateX(-50%) rotate(-3deg)!important}.p2-f3{transform:translateX(-50%) rotate(2.5deg)!important}.p2-f2{transform:translateX(-50%) rotate(-1.5deg)!important}.p2-f1{transform:translateX(-50%)!important}}
@media print{html.pv-js .p2-rv,html.pv-js .p2-m:not(.in) .p2-mc{opacity:1!important;transform:none!important}.p2-toc,.p2-tray{display:none}}
"""


# ------------------------------------------------------------------------------------------------ JS

POP2_JS = r"""(function(){
var d=document,rm=matchMedia('(prefers-reduced-motion: reduce)').matches,io='IntersectionObserver' in window;
function $(r,s){return r.querySelector(s)}function $$(r,s){return Array.prototype.slice.call(r.querySelectorAll(s))}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
/* header offset for sticky bars */
function top(){var h=$(d,'.q-header'),v=0;if(h){var p=getComputedStyle(h).position;if(p==='sticky'||p==='fixed')v=Math.round(h.getBoundingClientRect().height)}d.documentElement.style.setProperty('--p2-top',v+'px')}
top();addEventListener('resize',top);var tr=0;addEventListener('scroll',function(){if(!tr)tr=requestAnimationFrame(function(){tr=0;top()})},{passive:true});
/* reveal on scroll */
function watch(els,cb,th){if(!io||rm){els.forEach(function(e){cb(e,true)});return}var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){o.unobserve(e.target);cb(e.target,false)}})},{threshold:th||.18,rootMargin:'0px 0px -6% 0px'});els.forEach(function(e){o.observe(e)})}
$$(d,'[data-p2=reveal]').forEach(function(box){var kids=$$(box,':scope > li');kids.forEach(function(k,i){k.style.setProperty('--i',i);if(!rm&&io)k.classList.add('p2-rv')});if(rm||!io)return;watch(kids,function(k){k.classList.add('in')},.2)});
$$(d,'[data-p2=files]').forEach(function(f){if(rm||!io){f.classList.add('in');return}watch([f],function(e){e.classList.add('in')},.25)});
/* day timeline */
$$(d,'[data-p2=tl]').forEach(function(tl){var ms=$$(tl,'.p2-m');if(rm||!io){ms.forEach(function(m){m.classList.add('in')});return}
var raf=0;function upd(){raf=0;var line=innerHeight*.62,r=tl.getBoundingClientRect();ms.forEach(function(m){var b=m.getBoundingClientRect();if(b.top+30<line)m.classList.add('in')});var p=(line-r.top-28)/Math.max(1,r.height-56);tl.style.setProperty('--p',Math.max(0,Math.min(1,p)).toFixed(3))}
addEventListener('scroll',function(){if(!raf)raf=requestAnimationFrame(upd)},{passive:true});addEventListener('resize',upd);upd()});
/* count-up numerals */
$$(d,'[data-p2=nums] .p2-big').forEach(function(el){if(rm||!io)return;var to=parseFloat(el.getAttribute('data-to')),suf=el.getAttribute('data-suf')||'',final=el.textContent;el.textContent='0'+suf;watch([el],function(e){var t0=null;function st(ts){if(t0===null)t0=ts;var k=Math.min(1,(ts-t0)/1700);k=1-Math.pow(1-k,3);e.textContent=Math.round(to*k)+suf;if(k<1)requestAnimationFrame(st);else e.textContent=final}requestAnimationFrame(st)},.5)});
/* contact router */
$$(d,'[data-p2=router]').forEach(function(root){var picks=$$(root,'.p2-rt-pick'),panels=$$(root,'.p2-rt-panel'),stage=$(root,'.p2-rt-stage');
function sel(i,focus){picks.forEach(function(p,j){var on=j===i;p.setAttribute('aria-selected',on?'true':'false');p.tabIndex=on||(i<0&&j===0)?0:-1});panels.forEach(function(p,j){p.classList.toggle('on',j===i)});root.classList.add('has');if(focus)picks[i].focus();if(innerWidth<=900&&stage){setTimeout(function(){var r=stage.getBoundingClientRect();if(r.top>innerHeight*.6||r.top<0)stage.scrollIntoView({behavior:rm?'auto':'smooth',block:'start'})},60)}status()}
picks.forEach(function(p,i){p.tabIndex=i===0?0:-1;p.addEventListener('click',function(){sel(i)});p.addEventListener('keydown',function(e){var n=picks.length,k=e.key;if(k==='ArrowDown'||k==='ArrowRight'){e.preventDefault();sel((i+1)%n,true)}else if(k==='ArrowUp'||k==='ArrowLeft'){e.preventDefault();sel((i+n-1)%n,true)}else if(k==='Home'){e.preventDefault();sel(0,true)}else if(k==='End'){e.preventDefault();sel(n-1,true)}})})});
/* open now, from the posted hours, Central time */
var HOL={'2026-01-01':1,'2026-05-25':1,'2026-07-03':1,'2026-09-07':1,'2026-11-26':1,'2026-11-27':1,'2026-12-24':1,'2026-12-25':1};
function central(){try{var f=new Intl.DateTimeFormat('en-US',{timeZone:'America/Chicago',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',weekday:'short',hourCycle:'h23'}),o={};f.formatToParts(new Date()).forEach(function(p){o[p.type]=p.value});return{wd:o.weekday,date:o.year+'-'+o.month+'-'+o.day,min:(+o.hour)*60+(+o.minute)}}catch(e){return null}}
function parseH(t){var m=String(t).match(/(\d{1,2})(?::(\d{2}))?\s*a\.m\.\s*to\s*(\d{1,2})(?::(\d{2}))?\s*p\.m\./);if(!m)return null;var s=(+m[1]%12)*60+(+(m[2]||0)),e=((+m[3]%12)+12)*60+(+(m[4]||0));return{s:s,e:e,sl:m[1]+(m[2]?':'+m[2]:'')+' a.m.'}}
function state(h){var c=central(),p=parseH(h);if(!c||!p)return null;if(HOL[c.date])return{o:false,t:'Closed today (holiday)'};if(c.wd==='Sat'||c.wd==='Sun')return{o:false,t:'Closed now'};if(c.min>=p.s&&c.min<p.e)return{o:true,t:'Open now'};if(c.min<p.s)return{o:false,t:'Opens '+p.sl+' Central'};return{o:false,t:'Closed now'}}
function paint(el,st){if(!st)return;el.hidden=false;el.textContent=st.t;el.classList.toggle('is-closed',!st.o)}
var lines=[];$$(d,'.cd-line').forEach(function(l){var h=$(l,'.cd-hrs');if(!h||!parseH(h.textContent))return;var w=d.createElement('div');w.className='p2-hrow';h.parentNode.insertBefore(w,h);w.appendChild(h);var b=d.createElement('span');b.className='p2-open';b.hidden=true;b.setAttribute('role','status');w.appendChild(b);lines.push([b,h.textContent])});
function status(){$$(d,'.p2-open[data-hours]').forEach(function(el){paint(el,state(el.getAttribute('data-hours')))});lines.forEach(function(x){paint(x[0],state(x[1]))})}
status();setInterval(status,60000);
/* support chooser */
$$(d,'[data-p2=chooser]').forEach(function(root){var inp=$(root,'input'),ul=$(root,'.p2-res'),em=$(root,'.p2-sempty'),idx=[],sel=-1;try{idx=JSON.parse($(root,'.p2-idx').textContent)}catch(e){}
function hl(t,ts){var s=esc(t);ts.forEach(function(q){if(q.length>1)s=s.replace(new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig'),'<mark>$1</mark>')});return s}
function run(){var q=inp.value.trim().toLowerCase(),ts=q.split(/\s+/).filter(Boolean);sel=-1;if(!ts.length){ul.hidden=true;em.hidden=true;ul.innerHTML='';return}
var r=[];idx.forEach(function(it){var t=it.t.toLowerCase(),k=(it.k||'').toLowerCase(),dd=it.d.toLowerCase(),sc=0,ok=true;ts.forEach(function(w){var s=0;if(t.indexOf(w)>-1)s+=3;if(k.indexOf(w)>-1)s+=2;if(dd.indexOf(w)>-1)s+=1;if(!s)ok=false;sc+=s});if(ok)r.push([sc,it])});r.sort(function(a,b){return b[0]-a[0]});r=r.slice(0,6);
ul.innerHTML=r.map(function(x){var it=x[1],ext=/^https?:/.test(it.h)?' rel="noopener"':'';return '<li><a href="'+esc(it.h)+'"'+ext+'><span><b>'+hl(it.t,ts)+'</b><small>'+hl(it.d,ts)+'</small></span><span class="g" aria-hidden="true">&rarr;</span></a></li>'}).join('');ul.hidden=!r.length;em.hidden=!!r.length}
function mv(n){var a=$$(ul,'a');if(!a.length)return;a.forEach(function(x){x.classList.remove('sel')});sel=(sel+n+a.length)%a.length;a[sel].classList.add('sel');a[sel].scrollIntoView({block:'nearest'})}
inp.addEventListener('input',run);inp.addEventListener('keydown',function(e){if(e.key==='ArrowDown'){e.preventDefault();mv(1)}else if(e.key==='ArrowUp'){e.preventDefault();mv(-1)}else if(e.key==='Enter'){var a=$$(ul,'a');var t=a[sel<0?0:sel];if(t){e.preventDefault();location.href=t.href}}else if(e.key==='Escape'){inp.value='';run()}})});
/* training board */
$$(d,'[data-p2=board]').forEach(function(root){var c=central(),today=c?c.date:new Date().toISOString().slice(0,10),first=null;$$(root,'.p2-tk').forEach(function(t){var e=t.getAttribute('data-end');if(e<today)t.classList.add('is-past');else if(!first){first=t;t.classList.add('is-next');$(t,'.p2-tk-next').hidden=false}})});
/* blog toc */
$$(d,'[data-p2=toc]').forEach(function(nav){var links=$$(nav,'a'),secs=links.map(function(a){return d.getElementById(a.getAttribute('data-t'))}),strip=$(nav,'.p2-toc-s'),raf=0,cur=-1;
function upd(){raf=0;var off=(parseInt(getComputedStyle(d.documentElement).getPropertyValue('--p2-top'))||0)+nav.offsetHeight+30,a=0;secs.forEach(function(s,i){if(s&&s.getBoundingClientRect().top<=off)a=i});if(scrollY<20)a=0;if(a!==cur){cur=a;links.forEach(function(l,i){l.classList.toggle('on',i===a);if(i===a)l.setAttribute('aria-current','true');else l.removeAttribute('aria-current')});var l=links[a];strip.scrollTo?strip.scrollTo({left:Math.max(0,l.offsetLeft-strip.clientWidth/2+l.offsetWidth/2),behavior:rm?'auto':'smooth'}):0}
var m=$(d,'main'),r=m.getBoundingClientRect(),p=(-r.top+innerHeight*.3)/Math.max(1,r.height-innerHeight*.3);nav.style.setProperty('--p',Math.max(0,Math.min(1,p)).toFixed(3))}
addEventListener('scroll',function(){if(!raf)raf=requestAnimationFrame(upd)},{passive:true});addEventListener('resize',upd);upd()});
/* flip cards */
$$(d,'[data-p2=flip] .p2-fl-in').forEach(function(b){b.addEventListener('click',function(){b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true')})});
/* finder: why this and compare tray */
$$(d,'[data-mo=finder]').forEach(function(root){var dj=$(root,'.p2-fdata'),tray=$(root,'[data-p2=tray]');if(!dj||!tray)return;var data={};try{data=JSON.parse(dj.textContent)}catch(e){}
var btns=$$(root,'.p2-cmp'),pick=[],bar=tray.querySelector('.p2-tray-sel'),cnt=tray.querySelector('[data-c]'),go=tray.querySelector('.p2-tray-go'),panel=tray.querySelector('.p2-tray-panel'),scroll=tray.querySelector('.p2-tray-scroll');
function why(){var b=$(root,'.mo-fnd-row[data-kind=b] .mo-chip[aria-pressed=true]'),n=$(root,'.mo-fnd-row[data-kind=n] .mo-chip[aria-pressed=true]'),kb=b?b.getAttribute('data-k'):'all',kn=n?n.getAttribute('data-k'):'all';$$(root,'.p2-wc').forEach(function(c){var k=c.getAttribute('data-k');c.classList.toggle('on',k==='b:'+kb||k==='n:'+kn)})}
root.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.mo-chip,.mo-reset'))setTimeout(why,0)});why();
function table(){var items=pick.map(function(i){return data[i]}),labels=[],cnt={};items.forEach(function(it){it.sp.forEach(function(s){if(!cnt[s[0]]){cnt[s[0]]=0;labels.push(s[0])}cnt[s[0]]++})});labels.sort(function(a,b){return cnt[b]-cnt[a]});var shared=labels.filter(function(l){return cnt[l]>1});labels=shared.length>=4?shared.slice(0,10):labels.slice(0,8);
var h='<table class="p2-cmp-t"><thead><tr><th scope="col"><span class="mo-vh">Spec</span></th>'+items.map(function(it){return '<th scope="col"><a href="'+esc(it.h)+'">'+esc(it.n)+'</a>'+(it.soon?'<small>Coming soon, not orderable</small>':'<small>View product</small>')+'</th>'}).join('')+'</tr></thead><tbody>';
h+='<tr><th scope="row">Product type</th>'+items.map(function(it){return '<td>'+esc(it.t.join(', '))+'</td>'}).join('')+'</tr><tr><th scope="row">Systems</th>'+items.map(function(it){return '<td>'+esc(it.s.join(', '))+'</td>'}).join('')+'</tr>';
labels.forEach(function(l){h+='<tr><th scope="row">'+esc(l)+'</th>'+items.map(function(it){var v=null;it.sp.forEach(function(s){if(s[0]===l)v=s[1]});return v?'<td>'+esc(v)+'</td>':'<td class="na">Not listed</td>'}).join('')+'</tr>'});
scroll.innerHTML=h+'</tbody></table>'}
function ui(){tray.hidden=!pick.length;cnt.textContent=pick.length+' of 3 selected';go.disabled=pick.length<2;bar.innerHTML=pick.map(function(i){return '<li><span>'+esc(data[i].n)+'</span><button type="button" data-r="'+i+'" aria-label="Remove '+esc(data[i].n)+' from comparison">&times;</button></li>'}).join('');
btns.forEach(function(b){var on=pick.indexOf(b.getAttribute('data-i'))>-1;b.setAttribute('aria-pressed',on?'true':'false');b.setAttribute('aria-disabled',!on&&pick.length>=3?'true':'false')});
if(!panel.hidden){if(pick.length<2){panel.hidden=true;go.textContent='Compare specs'}else table()}}
btns.forEach(function(b){b.addEventListener('click',function(){var i=b.getAttribute('data-i'),k=pick.indexOf(i);if(k>-1)pick.splice(k,1);else if(pick.length<3)pick.push(i);else return;ui()})});
bar.addEventListener('click',function(e){var r=e.target.getAttribute&&e.target.getAttribute('data-r');if(r===null||r===undefined)return;pick.splice(pick.indexOf(r),1);ui()});
go.addEventListener('click',function(){if(panel.hidden){table();panel.hidden=false;go.textContent='Hide comparison'}else{panel.hidden=true;go.textContent='Compare specs'}});
tray.querySelector('.p2-tray-clear').addEventListener('click',function(){pick=[];panel.hidden=true;go.textContent='Compare specs';ui()});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&!panel.hidden){panel.hidden=true;go.textContent='Compare specs'}})});
})();"""
