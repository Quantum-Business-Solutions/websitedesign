#!/usr/bin/env python3
"""Upload themes/vaf/{css,js,modules,templates} into the VAF theme in portal 50498425 (published).

    CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_upload.py [path-prefix ...]   # e.g. modules/vaf-hero.module
Unchanged files (by content hash, kept in .vaf-upload-cache.json) are skipped. HubL is validated before each write;
the validator's two known false alarms (dnd areas 'unmapped', deprecated favicon_src in the stock base) are ignored.
"""
import hashlib, json, os, subprocess, sys, urllib.parse, uuid
sys.path.insert(0, os.path.dirname(__file__))
import reskin

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "themes/vaf")
THEME = "Van Ausdall and Farrar - Showcase"
TOKEN = os.environ["CLIENT_HUBSPOT_TOKEN"]
CACHE = os.path.join(ROOT, "themes/vaf/.upload-cache.json")
NOISE = ("Unmapped templates cannot contain drag and drop areas", "favicon_src has been deprecated")
TOP = ("css", "js", "modules", "templates")


def body(path, data):
    b = f"----qbs{uuid.uuid4().hex}"
    return (f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{os.path.basename(path)}\"\r\n"
            "Content-Type: application/octet-stream\r\n\r\n").encode() + data + f"\r\n--{b}--\r\n".encode(), b


def validate(path, data):
    if not path.endswith((".html", ".json")):
        return
    p = f"{THEME}/{path}"
    with __import__("tempfile").NamedTemporaryFile(suffix=os.path.splitext(path)[1], delete=False) as fh:
        fh.write(data)
    try:
        out = subprocess.run(["curl", "-s", "-X", "POST", "-H", "@-", "-F", f"file=@{fh.name};filename={os.path.basename(path)}",
                              f"{reskin.API}/cms/v3/source-code/published/validate/" + urllib.parse.quote(p)],
                             input=f"Authorization: Bearer {TOKEN}\n".encode(), capture_output=True, timeout=120).stdout
    finally:
        os.unlink(fh.name)
    d = json.loads(out or b"{}")
    real = [e["message"] for e in d.get("errors", []) if not any(k in e["message"] for k in NOISE)]
    if real:
        raise SystemExit(f"VALIDATION FAILED {path}\n  " + "\n  ".join(m[:400] for m in real))


def main(prefixes):
    reskin.verify_portal(TOKEN, "50498425")
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    n = 0
    for top in TOP:
        for dp, _, fs in os.walk(os.path.join(SRC, top)):
            for fn in sorted(fs):
                full = os.path.join(dp, fn)
                rel = os.path.relpath(full, SRC)
                if prefixes and not any(rel.startswith(p) for p in prefixes):
                    continue
                data = open(full, "rb").read()
                h = hashlib.sha1(data).hexdigest()
                if cache.get(rel) == h:
                    continue
                validate(rel, data)
                bd, b = body(rel, data)
                reskin._req("PUT", "/cms/v3/source-code/published/content/" + urllib.parse.quote(f"{THEME}/{rel}"), TOKEN, bd,
                            f"multipart/form-data; boundary={b}")
                cache[rel] = h
                n += 1
                print("  put", rel)
                json.dump(cache, open(CACHE, "w"), indent=1)
    print(n, "files uploaded")


if __name__ == "__main__":
    main(sys.argv[1:])
