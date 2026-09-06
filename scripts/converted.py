#!/usr/bin/env python3
"""Close the loop from shipped to converted.

Everything else in this repo optimises for passing a gate. Nothing measures whether the
thing WORKED. So taste is still opinion with good hygiene.

This joins three things that already exist separately:
  - the page record (which module order shipped)        -> data/pages.jsonl
  - the page's conversion numbers from HubSpot           -> pulled here
  - the critic score it shipped with                     -> verify-out/scores.jsonl
and writes a learning ONLY when the sample is big enough. That last clause is not
optional: BrandCommand currently holds a learning asserting the best variant is the one
with a 0% reply rate, at maximum confidence, reinforced four times. A learning from
zero signal is worse than none.

Read-only against HubSpot. Writes only to data/performance.jsonl.

  python3 scripts/converted.py pull --client kelly-office --since 2026-10-01
  python3 scripts/converted.py learn --min-pages 6 --min-visits 200

data/pages.jsonl -- one line per shipped page, written at RUNBOOK step 27:
  {"client":"kelly-office","url":"https://.../home","template":"home",
   "sections":["hero","pain-bridge","stats-band","services-list","faq","cta-band"],
   "vertical":"office-technology","shipped":"2026-10-14"}
"""
from __future__ import annotations
import argparse, json, os, sys, subprocess, urllib.parse, datetime
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(ROOT, "data", "pages.jsonl")
PERF = os.path.join(ROOT, "data", "performance.jsonl")
LEARN = os.path.join(ROOT, "data", "learnings.jsonl")


def jsonl(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def hs_get(path, token):
    """curl, for the same proxy reason as reskin.py."""
    r = subprocess.run(["curl", "-sS", "-H", "@-", "https://api.hubapi.com" + path],
                       input=f"Authorization: Bearer {token}\n".encode(), capture_output=True)
    if r.returncode:
        raise SystemExit(r.stderr.decode()[:300])
    return json.loads(r.stdout or b"{}")


def cmd_pull(a):
    """Per-page views and conversions since a date.

    HubSpot exposes page analytics at /analytics/v2/reports/pages/total and form
    submissions via the forms API. Both need the CLIENT token. This pull records
    visits and submissions per URL; it does not attribute revenue -- that is a later
    join to deals, and it is worth doing once this much is stable.
    """
    token = os.environ.get("CLIENT_HUBSPOT_TOKEN")
    if not token:
        raise SystemExit("Set CLIENT_HUBSPOT_TOKEN -- the client's portal, never ours.")
    pages = [p for p in jsonl(PAGES) if p.get("client") == a.client]
    if not pages:
        raise SystemExit(f"no shipped pages for {a.client} in data/pages.jsonl")

    q = urllib.parse.urlencode({"start": a.since.replace("-", ""),
                                "end": datetime.date.today().strftime("%Y%m%d"),
                                "limit": 200})
    data = hs_get(f"/analytics/v2/reports/pages/total?{q}", token)
    by_url = {}
    for row in data.get("breakdowns", []) or []:
        by_url[row.get("breakdown", "")] = row

    written = 0
    with open(PERF, "a", encoding="utf-8") as out:
        for p in pages:
            key = p["url"].rstrip("/")
            row = by_url.get(key) or by_url.get(key + "/") or {}
            rec = {
                "at": datetime.date.today().isoformat(), "client": a.client,
                "url": p["url"], "template": p.get("template"),
                "sections": p.get("sections", []), "vertical": p.get("vertical"),
                "visits": row.get("visits", 0), "submissions": row.get("submissions", 0),
                "since": a.since,
            }
            rec["conversion"] = (rec["submissions"] / rec["visits"]) if rec["visits"] else None
            out.write(json.dumps(rec) + "\n")
            written += 1
    print(f"wrote {written} page rows to data/performance.jsonl")
    return 0


def cmd_learn(a):
    """Which section orders convert, by vertical and template -- with a sample floor.

    A learning is written only when it rests on at least --min-pages pages AND
    --min-visits total visits. Below that it is noise with a confidence score, which
    is exactly the failure mode already sitting in BrandCommand's agent_learnings.
    """
    perf = [r for r in jsonl(PERF) if r.get("visits")]
    groups = defaultdict(list)
    for r in perf:
        # the first three sections are the above-the-fold argument
        key = (r.get("vertical"), r.get("template"), tuple(r.get("sections", [])[:3]))
        groups[key].append(r)

    learnings, skipped = [], 0
    for (vert, tpl, top3), rows in groups.items():
        visits = sum(r["visits"] for r in rows)
        subs = sum(r["submissions"] for r in rows)
        if len(rows) < a.min_pages or visits < a.min_visits:
            skipped += 1
            continue
        conf = min(0.95, 0.4 + 0.05 * len(rows) + visits / 20000)   # scales with sample
        learnings.append({
            "at": datetime.date.today().isoformat(), "vertical": vert, "template": tpl,
            "above_fold": list(top3), "pages": len(rows), "visits": visits,
            "submissions": subs, "conversion": round(subs / visits, 4),
            "confidence": round(conf, 2),
        })

    learnings.sort(key=lambda l: -l["conversion"])
    with open(LEARN, "a", encoding="utf-8") as out:
        for l in learnings:
            out.write(json.dumps(l) + "\n")

    print(f"{len(learnings)} learning(s) written, {skipped} group(s) below the sample floor "
          f"(min {a.min_pages} pages, {a.min_visits} visits)\n")
    for l in learnings[:10]:
        print(f"  {l['vertical']}/{l['template']}: {' > '.join(l['above_fold'])}"
              f"  -> {l['conversion']*100:.1f}%  (n={l['pages']} pages, {l['visits']} visits, "
              f"conf {l['confidence']})")
    if not learnings:
        print("  Nothing clears the floor yet. That is the correct output until it does.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    pu = sub.add_parser("pull"); pu.add_argument("--client", required=True)
    pu.add_argument("--since", required=True, help="YYYY-MM-DD")
    le = sub.add_parser("learn"); le.add_argument("--min-pages", type=int, default=6)
    le.add_argument("--min-visits", type=int, default=200)
    a = ap.parse_args()
    return {"pull": cmd_pull, "learn": cmd_learn}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main() or 0)
