#!/usr/bin/env python3
"""Build the 80-question Technology Strength Assessment from VAF's original questions plus a DRAFT answer key.

    python3 scripts/vaf_assessment_build.py                 # write brands/vanausdall.assessment-bank.json and refresh the fallback list in themes/vaf/js/vaf-assess.js
    CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_assessment_build.py --hubdb    # also load the rows into the HubDB table (draft, then publish)

Questions are VAF's own wording (brands/vanausdall.assessment-original-questions.json, read from the live site).
The answer key (good answer, Eliminate/Optimize/Leverage bucket, recommendation line) is a DRAFT for VAF to confirm.
good = yes (a Yes is the strong answer), no (a No is the strong answer, e.g. software at end of life), none (profile question, not scored).
"""
import json, os, re, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(ROOT, "brands/vanausdall.assessment-original-questions.json")
OUT = os.path.join(ROOT, "brands/vanausdall.assessment-bank.json")
JS = os.path.join(ROOT, "themes/vaf/js/vaf-assess.js")
TABLE = "451332876"
PORTAL = "50498425"

# (good, bucket, recommendation) per question number, per area. good "none" = profile question, not scored.
KEY = {
"Information": {
 1: ("yes", "optimize", "Put recurring vulnerability scans on the calendar and track every finding to closure."),
 2: ("yes", "eliminate", "Turn on multi-factor authentication for every administrator and user account, including email, line-of-business apps and VPN. It closes the most common way accounts are taken over."),
 3: ("yes", "eliminate", "Manage passwords and password changes centrally, with a policy strong enough that a stolen password is not the way in."),
 4: ("yes", "eliminate", "Back up server data every night and keep more than one copy, with at least one off site or in the cloud, so one failure cannot take your data with it."),
 5: ("yes", "optimize", "Patch servers and computers at least once a month, and name the person responsible."),
 6: ("yes", "optimize", "Review corporate firewall updates on a schedule so a known weakness is not left open."),
 7: ("yes", "eliminate", "Put one centrally managed anti-virus on every computer, so every machine gets current signature files."),
 8: ("yes", "optimize", "Schedule restore tests for your backups. A backup nobody has restored is a hope, not a plan."),
 9: ("yes", "leverage", "Write the disaster recovery plan down, include your IT systems, name an owner and revise it once or twice a year."),
 10: ("yes", "optimize", "Use device monitoring software so system problems are caught and fixed before users notice."),
 11: ("yes", "optimize", "Add a battery backup that keeps your router, firewall and servers running for at least 30 minutes in a power outage."),
 12: ("yes", "optimize", "Train every user to spot email and web-based hacking attempts, and repeat the training on a schedule."),
 13: ("no", "eliminate", "Replace software and operating systems that have reached end of life. They no longer receive security fixes."),
 14: ("yes", "leverage", "Look at server virtualization for fault tolerance and faster disaster recovery."),
 15: ("yes", "optimize", "Add the ability to send encrypted email when you share sensitive information."),
 16: ("yes", "optimize", "Assess your technology vendors every year to confirm they extend your security standards."),
 17: ("yes", "optimize", "Share written Internet usage and corporate email policies with every user."),
 18: ("yes", "optimize", "Write an IT onboarding and offboarding policy so access is granted and removed on time."),
 19: ("yes", "leverage", "Plan a multi-cloud strategy so the same authentication, security and policies apply everywhere."),
 20: ("no", "optimize", "Replace computers older than five years on a schedule, so aging machines do not slow people down or add risk."),
},
"Print": {
 1: ("yes", "leverage", "Define a print strategy: which devices you need, who owns them and what the goals are."),
 2: ("yes", "optimize", "Put every printer on the network so it can be monitored, secured and managed."),
 3: ("yes", "optimize", "Put supplies, service and device costs in one annual report so you know what printing really costs."),
 4: ("yes", "leverage", "Have a strategic print assessment done to find the cost, risk and waste in your fleet."),
 5: ("yes", "eliminate", "Learn the current security risks of printers and multifunction devices, and close the gaps."),
 6: ("none", "optimize", ""),
 7: ("none", "optimize", ""),
 8: ("yes", "eliminate", "Track the printing of sensitive information so you can see who printed what."),
 9: ("yes", "eliminate", "Require users to authenticate at the multifunction device so documents are released only to the right person."),
 10: ("yes", "leverage", "Move scanning onto your multifunction devices to cut hand-offs and speed up document workflows."),
 11: ("no", "optimize", "Set up automatic supply replenishment so you never run out of toner or other print supplies."),
 12: ("yes", "optimize", "Agree a replacement plan for when a printer breaks, so work does not stop."),
 13: ("none", "optimize", ""),
 14: ("yes", "optimize", "Match your high-volume printers to your critical print needs, so peaks do not stall the office."),
 15: ("no", "eliminate", "Turn on secure print release so jobs are not left unclaimed in the output tray."),
 16: ("none", "optimize", ""),
 17: ("yes", "optimize", "Hold your device supplier to the service you expect, and change supplier if they cannot meet it."),
 18: ("yes", "optimize", "Keep enough backup printers in storage so a failure is a swap, not a delay."),
 19: ("none", "optimize", ""),
 20: ("yes", "optimize", "Send management regular print and copy activity reports with job detail and costs."),
},
"Process": {
 1: ("yes", "eliminate", "Adopt a formal records retention schedule and follow it."),
 2: ("yes", "optimize", "Keep business records in one centralized, searchable repository."),
 3: ("no", "eliminate", "Move paper-based processes to electronic workflows to cut handling time and errors."),
 4: ("yes", "eliminate", "Write a continuity strategy so the business keeps operating at full capacity if the building or the paper records are not accessible."),
 5: ("no", "eliminate", "Convert paper department files to searchable electronic records."),
 6: ("no", "optimize", "Take routine office services off your administrative staff so they can focus on higher-value work."),
 7: ("none", "optimize", ""),
 8: ("none", "optimize", ""),
 9: ("yes", "leverage", "Automate accounts payable processing to cut manual entry and speed approvals."),
 10: ("yes", "leverage", "Automate HR and onboarding paperwork."),
 11: ("yes", "leverage", "Automate legal and contract documentation."),
 12: ("no", "optimize", "Add a managed office-services option so staff turnover does not disrupt daily work."),
 13: ("yes", "optimize", "Set up a centralized resource center for office services."),
 14: ("yes", "optimize", "Put a coverage plan in place for when an employee is out sick or on vacation."),
 15: ("no", "optimize", "Replace the paper visitor log with an electronic visitor management system."),
 16: ("yes", "leverage", "Use an electronic conference room management system for scheduling."),
 17: ("yes", "optimize", "Track inbound packages from the dock to the desktop."),
 18: ("yes", "optimize", "Take full advantage of carrier and USPS discounts on outgoing mail and overnight shipping."),
 19: ("yes", "leverage", "Use an electronic forms management or print submission tool."),
 20: ("no", "optimize", "Bring print work in house or onto one managed service instead of outsourcing most of it to local printers."),
},
"Communication": {
 1: ("yes", "optimize", "Use Power over Ethernet compliant switching so phones, access points and cameras can be powered from the network."),
 2: ("yes", "optimize", "Review your internet service against what the business needs now, and fix the gaps."),
 3: ("yes", "eliminate", "Subscribe to more than one internet service for traffic steering, shaping and failover."),
 4: ("yes", "eliminate", "Write a disaster recovery plan for your business phone system."),
 5: ("yes", "leverage", "Fully integrate remote users with your phone system."),
 6: ("yes", "optimize", "Move to an IP-based phone system."),
 7: ("yes", "leverage", "Look at a cloud-based phone system."),
 8: ("yes", "leverage", "Connect smart phones to your corporate phone system for extension dialing and real-time presence."),
 9: ("yes", "optimize", "Add call recording."),
 10: ("yes", "leverage", "Give users a desktop client to manage call activity, real-time presence and call routing."),
 11: ("yes", "leverage", "Use Microsoft Teams for video conferencing and collaboration, connected to your phone system."),
 12: ("yes", "leverage", "Let people use a desktop or laptop as their phone."),
 13: ("yes", "optimize", "Fix Wi-Fi coverage gaps so every work area is covered."),
 14: ("no", "optimize", "Fix the technology behind late or ineffective meetings."),
 15: ("yes", "leverage", "Add contact center functionality that queues calls, emails and chat requests in high call volume groups."),
 16: ("yes", "optimize", "Use call reports to see employee productivity."),
 17: ("yes", "optimize", "Give conference room technology a dedicated owner or team."),
 18: ("yes", "optimize", "Improve the conference room technology that is not working well for you."),
 19: ("none", "optimize", ""),
 20: ("none", "optimize", ""),
},
}


def build():
    d = json.load(open(ORIG, encoding="utf-8"))["areas"]
    rows, sort = [], 0
    for area, qs in d.items():
        assert len(qs) == 20 and set(KEY[area]) == set(range(1, 21)), area
        for q in qs:
            good, bucket, fix = KEY[area][q["n"]]
            sort += 1
            rows.append({"sort": sort, "area": area, "part": q["part"], "n": q["n"], "question": q["question"],
                         "good": good, "bucket": bucket, "fix": fix, "weight": 1 if good != "none" else 0})
    json.dump({"status": "DRAFT answer key for VAF to confirm. Questions are VAF's own wording.", "rows": rows},
              open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return rows


def js_str(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def patch_js(rows):
    s = open(JS, encoding="utf-8").read()
    i = s.index("  var BANK = [")
    mp = s.index("].map(function (r)", i)
    j = s.index("\n", mp) + 1
    lines = ["  var BANK = [  // area, question, bucket, recommendation, good answer (yes, no, or none = profile question, not scored). 80 questions, 10 per step. Mirrors the HubDB table.\n"]
    for r in rows:
        lines.append("    [%s, %s, %s, %s, %s],\n" % (js_str(r["area"]), js_str(r["question"]), js_str(r["bucket"]), js_str(r["fix"]), js_str(r["good"])))
    lines.append("  ].map(function (r) { return { area: r[0], q: r[1], bucket: r[2], fix: r[3], good: r[4] || 'yes', w: r[4] === 'none' ? 0 : 1 }; });\n")
    open(JS, "w", encoding="utf-8").write(s[:i] + "".join(lines) + s[j:])


def api(method, path, body=None, tries=5):
    tok = os.environ["CLIENT_HUBSPOT_TOKEN"]
    for k in range(tries):
        req = urllib.request.Request("https://api.hubapi.com" + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                     headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                t = r.read(); return json.loads(t) if t else {}
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and k < tries - 1:
                time.sleep(2 ** (k + 1)); continue
            raise RuntimeError(f"{method} {path} -> {e.code} {e.read()[:400]!r}")


def load_hubdb(rows):
    acct = api("GET", "/account-info/v3/details")
    if str(acct["portalId"]) != PORTAL:
        raise SystemExit(f"token is for portal {acct['portalId']}, not {PORTAL}")
    t = api("GET", f"/cms/v3/hubdb/tables/{TABLE}/draft")
    cols = t["columns"]
    if not any(c["name"] == "good" for c in cols):
        cols = [{k: c[k] for k in ("name", "label", "type") if k in c} | ({"id": c["id"]} if "id" in c else {}) for c in cols]
        cols.append({"name": "good", "label": "Good answer (yes, no or none)", "type": "TEXT"})
        api("PATCH", f"/cms/v3/hubdb/tables/{TABLE}/draft", {"columns": cols})
        print("added column: good")
    old = api("GET", f"/cms/v3/hubdb/tables/{TABLE}/rows/draft?limit=500")["results"]
    if old:
        api("POST", f"/cms/v3/hubdb/tables/{TABLE}/rows/draft/batch/purge", {"inputs": [r["id"] for r in old]})
        print("removed", len(old), "draft rows")
    inputs = [{"values": {"sort": r["sort"], "area": r["area"], "question": r["question"], "bucket": r["bucket"], "fix": r["fix"], "weight": r["weight"], "good": r["good"]}} for r in rows]
    for k in range(0, len(inputs), 50):
        api("POST", f"/cms/v3/hubdb/tables/{TABLE}/rows/draft/batch/create", {"inputs": inputs[k:k + 50]})
    api("POST", f"/cms/v3/hubdb/tables/{TABLE}/draft/publish")
    n = api("GET", f"/cms/v3/hubdb/tables/{TABLE}")["rowCount"]
    print("published table rows:", n)


if __name__ == "__main__":
    rows = build()
    patch_js(rows)
    print("wrote bank:", len(rows), "questions;", sum(1 for r in rows if r["good"] == "none"), "profile (unscored);", sum(1 for r in rows if r["good"] == "no"), "reversed")
    if "--hubdb" in sys.argv:
        load_hubdb(rows)
