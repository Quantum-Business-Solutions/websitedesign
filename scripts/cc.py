#!/usr/bin/env python3
"""Client Command's side of a directions build, from inside GitHub Actions.

    python3 scripts/cc.py brief    <build_id>                         fetch the brief -> brands/<slug>.brief.json; prints slug=... for $GITHUB_OUTPUT
    python3 scripts/cc.py scaffold <build_id>                         newclient.py with the brief's values (idempotent)
    python3 scripts/cc.py progress <build_id> <step> <message...>     one line in the Client Command status
    python3 scripts/cc.py upload   <build_id> <slug> <out-dir>        assets straight into the sites bucket, text files as one zip; prints the zip path
    python3 scripts/cc.py finish   <build_id> <slug> <out-dir> <zip>  Client Command unpacks the zip into the site
    python3 scripts/cc.py fail     <build_id> <message> [logfile]

Authentication is the job's GitHub OIDC token (the workflow grants `id-token: write`). Client Command checks the
token was minted for this repository's Website directions workflow, so no shared secret exists on either side.
Only the standard library is used; it runs on a bare runner before `pip install`.
"""
from __future__ import annotations

import json
import mimetypes
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENDPOINT = os.environ.get("CLIENTCOMMAND_FUNCTIONS", "https://zjtgesaiemlveuoymubo.supabase.co/functions/v1") + "/site-build"
AUDIENCE = "clientcommand"

TEXT_EXT = {".html", ".htm", ".css", ".js", ".mjs", ".json", ".xml", ".txt", ".svg", ".csv", ".md", ".webmanifest", ".map"}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}
SKIP_FILES = {"README.md", "vercel.json", ".DS_Store", ".gitignore"}
EXTRA_MIME = {".glb": "model/gltf-binary", ".webp": "image/webp", ".avif": "image/avif", ".woff2": "font/woff2", ".woff": "font/woff",
              ".mp4": "video/mp4", ".webm": "video/webm", ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}


def oidc() -> str:
    url, tok = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_URL"), os.environ.get("ACTIONS_ID_TOKEN_REQUEST_TOKEN")
    if not url or not tok:
        sys.exit("No OIDC token available: the job needs `permissions: id-token: write`.")
    req = urllib.request.Request(f"{url}&audience={AUDIENCE}", headers={"Authorization": f"bearer {tok}", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["value"]


def call(action: str, payload: dict) -> dict:
    body = json.dumps({"action": action, **payload}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                 headers={"Authorization": f"Bearer {oidc()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "ignore")[:600]
        sys.exit(f"Client Command answered {e.code} to {action}: {detail}")


def run_context() -> dict:
    rid = os.environ.get("GITHUB_RUN_ID", "")
    server, repo = os.environ.get("GITHUB_SERVER_URL", "https://github.com"), os.environ.get("GITHUB_REPOSITORY", "")
    return {"run_id": rid, "run_url": f"{server}/{repo}/actions/runs/{rid}" if rid and repo else None, "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", "")}


def brief_path(slug: str) -> str:
    return os.path.join(ROOT, "brands", f"{slug}.brief.json")


def cmd_brief(build_id: str) -> None:
    b = call("brief", {"build_id": build_id, **run_context()})
    slug = b["slug"]
    with open(brief_path(slug), "w", encoding="utf-8") as f:
        json.dump(b, f, indent=1, ensure_ascii=False)
    # For $GITHUB_OUTPUT. Values are single-line by construction (Client Command trims them).
    for k in ("slug", "client", "short", "domain", "base_url"):
        print(f"{k}={str(b.get(k) or '').splitlines()[0] if b.get(k) else ''}")
    print(f"wrote brands/{slug}.brief.json", file=sys.stderr)


def cmd_scaffold(build_id: str) -> None:
    slugs = [f[:-len(".brief.json")] for f in os.listdir(os.path.join(ROOT, "brands")) if f.endswith(".brief.json")]
    briefs = [json.load(open(brief_path(s), encoding="utf-8")) for s in slugs]
    b = next((x for x in briefs if x.get("build_id") == build_id), None)
    if not b:
        sys.exit("Run `cc.py brief` first.")
    cities = b.get("cities") or []
    args = [sys.executable, os.path.join(HERE, "newclient.py"), "--slug", b["slug"], "--client", b["client"], "--short", b.get("short") or b["client"].split(" ")[0],
            "--domain", b["domain"], "--repo", f"../out-{b['slug']}", "--base-url", b["base_url"],
            "--city-tag", b.get("city_tag") or (cities[0] if cities else ""), "--cities", ",".join(cities)]
    print("$", " ".join(args), file=sys.stderr)
    subprocess.run(args, cwd=ROOT, check=True)
    # A client built before has a build.json pointing at a Vercel project. This build serves from Client Command.
    bj = os.path.join(ROOT, "brands", f"{b['slug']}.build.json")
    cfg = json.load(open(bj, encoding="utf-8"))
    cfg["base_url"], cfg["out"] = b["base_url"], f"../out-{b['slug']}"
    json.dump(cfg, open(bj, "w", encoding="utf-8"), indent=1)


def cmd_progress(build_id: str, step: str, message: str) -> None:
    call("progress", {"build_id": build_id, "step": step, "message": message[:400], **run_context()})


def mime_of(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    return EXTRA_MIME.get(ext) or mimetypes.guess_type(path)[0] or "application/octet-stream"


def put_signed(url: str, data: bytes, content_type: str) -> None:
    req = urllib.request.Request(url, data=data, method="PUT", headers={"Content-Type": content_type, "x-upsert": "true"})
    with urllib.request.urlopen(req, timeout=300) as r:
        r.read()


def walk(out_dir: str):
    for dirpath, dirnames, filenames in os.walk(out_dir):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn in SKIP_FILES:
                continue
            full = os.path.join(dirpath, fn)
            yield full, os.path.relpath(full, out_dir).replace(os.sep, "/")


def cmd_upload(build_id: str, slug: str, out_dir: str) -> None:
    out_dir = os.path.normpath(os.path.join(ROOT, out_dir)) if not os.path.isabs(out_dir) else out_dir
    text, binary = [], []
    for full, rel in walk(out_dir):
        (text if os.path.splitext(rel)[1].lower() in TEXT_EXT else binary).append((full, rel))
    print(f"{len(text)} text files, {len(binary)} assets", file=sys.stderr)

    def one(item):
        full, rel = item
        ct = mime_of(rel)
        target = call("upload_url", {"build_id": build_id, "path": f"{slug}/{rel}", "content_type": ct})
        with open(full, "rb") as f:
            put_signed(target["url"], f.read(), ct)
        return os.path.getsize(full)

    total = 0
    with ThreadPoolExecutor(max_workers=4) as ex:
        for n in ex.map(one, binary):
            total += n
    print(f"assets uploaded: {total / 1048576:.1f} MB", file=sys.stderr)

    zpath = os.path.join(ROOT, f"{slug}.site.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for full, rel in text:
            z.write(full, rel)
    key = f"_builds/{build_id}/site.zip"
    target = call("upload_url", {"build_id": build_id, "path": key, "content_type": "application/zip"})
    with open(zpath, "rb") as f:
        put_signed(target["url"], f.read(), "application/zip")
    print(f"zip uploaded: {os.path.getsize(zpath) / 1048576:.1f} MB as {key}", file=sys.stderr)
    print(key)


def cmd_finish(build_id: str, slug: str, out_dir: str, zip_path: str) -> None:
    out_dir = os.path.normpath(os.path.join(ROOT, out_dir)) if not os.path.isabs(out_dir) else out_dir
    summary: dict = {"pages": 0, "assets": 0, "bytes": 0}
    for full, rel in walk(out_dir):
        summary["bytes"] += os.path.getsize(full)
        summary["pages" if os.path.splitext(rel)[1].lower() in {".html", ".htm"} else "assets"] += 1
    try:
        cfg = json.load(open(os.path.join(ROOT, "brands", f"{slug}.build.json"), encoding="utf-8"))
        summary["themes"], summary["recommend"], summary["roles"] = cfg.get("themes"), cfg.get("recommend"), cfg.get("roles")
    except Exception:  # noqa: BLE001
        pass
    try:
        sc = json.load(open(os.path.join(out_dir, "seo-build-scores.first.json"), encoding="utf-8"))
        summary["score"] = {"avg": sc.get("avg_score"), "grade_a": sc.get("grade_a"), "count": sc.get("count")}
    except Exception:  # noqa: BLE001
        pass
    try:
        content = json.load(open(os.path.join(ROOT, "brands", f"{slug}.content.json"), encoding="utf-8"))
        summary["confirm"] = (content.get("pitch") or {}).get("confirm", [])[:20]
        summary["site_pages"] = len(content.get("pages", []))
    except Exception:  # noqa: BLE001
        pass
    r = call("finish", {"build_id": build_id, "zip_path": zip_path, "summary": summary, **run_context()})
    print(json.dumps(r))


def cmd_fail(build_id: str, message: str, logfile: str | None) -> None:
    log = ""
    if logfile and os.path.exists(logfile):
        log = open(logfile, encoding="utf-8", errors="ignore").read()[-4000:]
    call("fail", {"build_id": build_id, "error": message[:800], "log": log, **run_context()})


def main(argv: list[str]) -> None:
    if len(argv) < 2:
        sys.exit(__doc__)
    cmd, args = argv[0], argv[1:]
    if cmd == "brief":
        cmd_brief(args[0])
    elif cmd == "scaffold":
        cmd_scaffold(args[0])
    elif cmd == "progress":
        cmd_progress(args[0], args[1], " ".join(args[2:]))
    elif cmd == "upload":
        cmd_upload(args[0], args[1], args[2])
    elif cmd == "finish":
        cmd_finish(args[0], args[1], args[2], args[3])
    elif cmd == "fail":
        cmd_fail(args[0], args[1], args[2] if len(args) > 2 else None)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
