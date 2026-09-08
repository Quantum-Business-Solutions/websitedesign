#!/usr/bin/env python3
"""One command per client: content file to live hub.

    python3 scripts/build.py <slug> [--push] [--shots] [--no-content]

Reads brands/<slug>.build.json:
    {"content": "brands/<slug>.content.py",          # optional; run first to regenerate the JSON
     "themes": ["Quantum Showcase", "Quantum Clean", "Quantum Press"],
     "recommend": null | "Quantum Showcase",
     "roles": {"Showcase": "...", "Clean": "...", "Press": "..."},
     "base_url": "https://<project>.vercel.app",
     "out": "../<client-repo>"}                        # relative to websitedesign/

Then runs preview.py (pages, hub, design system, the search package when brands/<slug>.seo.json and
.audit.json exist), removes stale pages the content no longer names, scores the first direction with
seo_audit.py, optionally screenshots the hub, and with --push commits and pushes the client repo, which
Vercel deploys. The exact command is never retyped, so a rebuild is one line and a new client is a
copied build.json.
"""
import argparse
import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def sh(cmd, cwd=ROOT, check=True):
    print("$", " ".join(cmd) if isinstance(cmd, list) else cmd)
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=False)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("slug")
    p.add_argument("--push", action="store_true", help="commit and push the client repo")
    p.add_argument("--shots", action="store_true", help="hub screenshots at 1280 and 390 into <out>/screenshots")
    p.add_argument("--no-content", action="store_true", help="skip running the content .py")
    p.add_argument("--message", default="Rebuild from websitedesign")
    a = p.parse_args(argv)

    cfg_path = os.path.join(ROOT, "brands", f"{a.slug}.build.json")
    if not os.path.exists(cfg_path):
        sys.exit(f"no {cfg_path}. Copy brands/_starter.build.json and fill it, or run scripts/newclient.py.")
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    out = os.path.normpath(os.path.join(ROOT, cfg["out"]))
    content_json = os.path.join(ROOT, "brands", f"{a.slug}.content.json")

    if cfg.get("content") and not a.no_content:
        sh([sys.executable, os.path.join(ROOT, cfg["content"])])
    if not os.path.exists(content_json):
        sys.exit(f"no {content_json}")

    # stale pages: anything in a direction folder the content no longer names
    content = json.load(open(content_json, encoding="utf-8"))
    keep = {pg["file"] for pg in content["pages"]}
    for t in cfg["themes"]:
        d = os.path.join(out, t.replace("Quantum ", "").lower())
        for f in glob.glob(os.path.join(d, "**", "*.html"), recursive=True):
            rel = os.path.relpath(f, d).replace(os.sep, "/")
            if rel not in keep:
                os.remove(f)
                print("removed stale", rel)

    roles = "|".join(f"{k}: {v}" for k, v in cfg["roles"].items())
    cmd = [sys.executable, os.path.join(HERE, "preview.py"), "--content", content_json, "--themes", ",".join(cfg["themes"]),
           "--roles", roles, "--base-url", cfg["base_url"], "--out", out]
    if cfg.get("recommend"):
        cmd += ["--recommend", cfg["recommend"]]
    sh(cmd)

    # score the first direction with the same checks the hub uses
    first = os.path.join(out, cfg["themes"][0].replace("Quantum ", "").lower())
    cities = ",".join((content.get("schema") or {}).get("cities", []))
    r = subprocess.run([sys.executable, os.path.join(HERE, "seo_audit.py"), "build", "--dir", first, "--cities", cities,
                        "--out", os.path.join(out, "seo-build-scores.first.json")], cwd=ROOT, text=True, capture_output=True)
    try:
        summ = json.loads(r.stdout)
        print(f"  build {cfg['themes'][0]}: {summ['avg_score']} average, {summ['grade_a']} of {summ['count']} A")
    except Exception:  # noqa: BLE001
        print(r.stdout[-400:], r.stderr[-400:])

    if a.shots:
        os.makedirs(os.path.join(out, "screenshots"), exist_ok=True)
        for w, name in ((1280, "hub-1280"), (390, "hub-390")):
            subprocess.run(["node", os.path.join(HERE, "_clip.mjs"), os.path.join(out, "index.html"), str(w), "main", "0", "2600",
                            os.path.join(out, "screenshots", f"{name}.jpg")], cwd=HERE, text=True)

    if a.push:
        sh(["git", "add", "-A"], cwd=out)
        msg = f"{a.message}\n\nCo-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01FeWbztza33MhFGyQMY13SN"
        r = subprocess.run(["git", "commit", "-q", "-m", msg], cwd=out, text=True, capture_output=True)
        if r.returncode == 0:
            sh(["git", "push", "-q", "origin", "HEAD"], cwd=out)
            print(f"  pushed; Vercel deploys {cfg['base_url']}")
        else:
            print("  nothing to commit")
    print(f"hub: {os.path.join(out, 'index.html')}  live: {cfg['base_url']}")


if __name__ == "__main__":
    main()
