#!/usr/bin/env python3
"""Continuous category monitoring — the plan, and the check.

We scrape competitors once at brief time and never again. For a vertical where six of
ten clients are office technology, watching the category is cheap and it compounds:
a competitor relaunch is the worst moment to pitch a prospect, and a stale site is the
best. Worth more in outbound than in delivery.

This script is READ-ONLY by default. It builds the monitoring plan for a vertical and
shows exactly what it would register. `--apply` is the only thing that creates anything,
and it prints what it created. Monitor creation is an outward-facing action with cost,
so it goes through the same propose-then-confirm as everything else here.

  python3 scripts/monitor.py plan --vertical office-technology
  python3 scripts/monitor.py plan --vertical office-technology --apply --approved-by "Shawn"

What gets watched, per competitor:
  - homepage change (a relaunch, a rebrand, a new offer) -> Firecrawl monitor
  - ranking movement on the category head terms       -> Semrush position tracking
  - new content cadence                                -> Firecrawl monitor on /blog

Firecrawl monitors are created through the Firecrawl MCP (firecrawl_monitor_create),
not from this script, so --apply emits the exact calls for the agent to make and a
human to approve. Same for Semrush projects. The script owns the PLAN and the RECORD;
it does not hold API keys.
"""
from __future__ import annotations
import argparse, json, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(ROOT, "verticals", "monitors.json")

# Category head terms per vertical. From the Semrush pulls in verticals/*.md.
HEAD_TERMS = {
    "office-technology": [
        "copier lease", "printer lease", "managed print services", "copier dealer",
        "office equipment leasing", "cost per page", "multifunction printer lease",
        "managed IT services",
    ],
}


def competitors_for(vertical: str) -> list[dict]:
    """Read the competitor set out of the vertical file, so one source governs."""
    path = os.path.join(ROOT, "verticals", f"{vertical}.md")
    if not os.path.exists(path):
        raise SystemExit(f"no vertical file at {path}")
    txt = open(path, encoding="utf-8").read()
    out = []
    # the client table carries domains; treat every client site as a category watch too
    for m in re.finditer(r"\|\s*([^|]+?)\s*\|\s*([a-z0-9.-]+\.(?:com|net|org|business))\s*\|", txt):
        name, dom = m.group(1).strip().strip("*"), m.group(2).strip()
        if name.lower() in ("client", "site", "competitor"):
            continue
        out.append({"name": name, "domain": dom, "kind": "client-or-peer"})
    return out


def build_plan(vertical: str, extra: list[str]) -> dict:
    comps = competitors_for(vertical)
    for d in extra:
        comps.append({"name": d, "domain": d, "kind": "competitor"})
    monitors = []
    for c in comps:
        monitors.append({"target": f"https://{c['domain']}", "type": "page-change",
                         "cadence": "weekly", "why": "relaunch / rebrand / new offer"})
        monitors.append({"target": f"https://{c['domain']}/blog", "type": "page-change",
                         "cadence": "weekly", "why": "content cadence"})
    return {
        "vertical": vertical,
        "generated": datetime.date.today().isoformat(),
        "competitors": comps,
        "firecrawl_monitors": monitors,
        "semrush_tracking": {"terms": HEAD_TERMS.get(vertical, []),
                             "domains": [c["domain"] for c in comps]},
        "digest": {"cadence": "monthly",
                   "trigger": "any homepage change on a PROSPECT -> process/outbound-mockups.md"},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    pl = sub.add_parser("plan")
    pl.add_argument("--vertical", required=True)
    pl.add_argument("--competitor", action="append", default=[], help="extra domain to watch")
    pl.add_argument("--apply", action="store_true", help="record the plan and emit the calls")
    pl.add_argument("--approved-by")
    a = ap.parse_args()

    plan = build_plan(a.vertical, a.competitor)
    print(f"\nMonitoring plan — {a.vertical}\n")
    print(f"  {len(plan['competitors'])} domains · {len(plan['firecrawl_monitors'])} Firecrawl "
          f"monitors · {len(plan['semrush_tracking']['terms'])} head terms tracked\n")
    for c in plan["competitors"]:
        print(f"  watch  {c['domain']:36} {c['kind']}")
    print(f"\n  terms  {', '.join(plan['semrush_tracking']['terms'])}")
    print(f"\n  digest monthly; a homepage change on a prospect triggers an outbound mockup.")

    if not a.apply:
        print("\nDRY RUN. Nothing registered. Re-run with --apply --approved-by \"<name>\".\n")
        return 0
    if not a.approved_by:
        raise SystemExit("--apply requires --approved-by. Monitors cost money.")

    os.makedirs(os.path.dirname(REGISTRY), exist_ok=True)
    reg = json.load(open(REGISTRY)) if os.path.exists(REGISTRY) else {}
    plan["approved_by"] = a.approved_by
    reg[a.vertical] = plan
    json.dump(reg, open(REGISTRY, "w"), indent=2)
    print(f"\nRecorded to {os.path.relpath(REGISTRY, ROOT)}. Now make these calls:\n")
    for m in plan["firecrawl_monitors"]:
        print(f"  firecrawl_monitor_create url={m['target']} schedule={m['cadence']}  # {m['why']}")
    print(f"\n  Semrush: add {len(plan['semrush_tracking']['terms'])} terms to position tracking "
          f"for each of {len(plan['semrush_tracking']['domains'])} domains.")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
