#!/usr/bin/env python3
"""Preview images for the chooser hub: one hero crop and one tall crop of each direction's home page.

    python3 scripts/hub_shots.py OUT_DIR [--dirs showcase,clean,press] [--save brands/<slug>.assets/hub]

Serves OUT_DIR on a local port, opens <dir>/index.html in Chromium (Playwright, through scripts/_hub_shots.mjs) with the
preview notice and consent banner switched off, scrolls the page so reveals have fired, and writes into OUT_DIR/assets/hub/:

    <dir>-hero-960.jpg  <dir>-hero-640.jpg     the first screen, 16:10
    <dir>-tall-960.jpg  <dir>-tall-640.jpg     the top 4,200 px of the page (less when the page is shorter)
    <dir>-type.jpg                              the home page headline exactly as that direction sets it
    shots.json                                  image sizes, plus the measured look of each direction (headline face,
                                                grounds, accent) that the hub's chips and swatches are drawn from

then rewrites the hub cards in OUT_DIR/index.html to use them (preview_hub2.apply_shots). With --save the same files are
copied into the brand's assets folder, which is committed, so a build on a machine without Playwright still has images.

Nothing here is fatal: with no node, no Playwright, no Chromium or no Pillow it prints a warning and leaves whatever
images are already in OUT_DIR/assets/hub (the committed fallback, copied there by build.py) in place. Exit code is 0.
"""
import argparse
import functools
import http.server
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
WIDTHS = (960, 640)
SRC_W, TALL_H = 1440, 4200


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):  # noqa: D401
        pass


def _serve(root):
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(_Quiet, directory=root))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def find_dirs(out):
    skip = {"assets", "launch-package", "screenshots", "node_modules"}
    return [d for d in sorted(os.listdir(out)) if d not in skip and not d.startswith((".", "_"))
            and os.path.exists(os.path.join(out, d, "index.html"))]


def warn(msg):
    print(f"hub_shots: WARNING: {msg}; keeping the images already in assets/hub")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("out")
    p.add_argument("--dirs", default="", help="comma separated direction folders; default: every folder with an index.html")
    p.add_argument("--save", default="", help="also copy the images here (the brand's committed assets/hub folder)")
    a = p.parse_args(argv)
    out = os.path.abspath(a.out)
    dirs = [d for d in a.dirs.split(",") if d] or find_dirs(out)
    dirs = [d for d in dirs if os.path.exists(os.path.join(out, d, "index.html"))]
    if not dirs:
        return warn("no built direction found")
    try:
        from PIL import Image
    except Exception:  # noqa: BLE001
        return warn("Pillow is not installed (pip install pillow)")
    if not shutil.which("node"):
        return warn("node is not installed")
    dest = os.path.join(out, "assets", "hub")
    tmp = tempfile.mkdtemp(prefix="hubshots-")
    srv = None
    try:
        try:
            srv = _serve(out)
        except OSError as e:
            return warn(f"could not start a local server ({e})")
        base = f"http://127.0.0.1:{srv.server_address[1]}"
        try:
            r = subprocess.run(["node", os.path.join(HERE, "_hub_shots.mjs"), base, tmp, ",".join(dirs), str(SRC_W), str(TALL_H)],
                               cwd=HERE, text=True, capture_output=True, timeout=300)
        except Exception as e:  # noqa: BLE001
            return warn(f"the screenshot run did not finish ({e})")
        if r.stdout.strip():
            print("  " + r.stdout.strip().replace("\n", "\n  "))
        if r.returncode != 0:
            return warn("Playwright could not take the screenshots: " + (r.stderr.strip().splitlines() or ["unknown error"])[-1][:200])
        # every direction or none: three cards with mixed old and new images would misrepresent the build
        if not all(os.path.exists(os.path.join(tmp, f"{d}-{k}.png")) for d in dirs for k in ("hero", "tall")):
            return warn("a screenshot is missing")
        os.makedirs(dest, exist_ok=True)
        man_path = os.path.join(dest, "shots.json")
        manifest = {}
        if os.path.exists(man_path):
            try:
                manifest = json.load(open(man_path, encoding="utf-8"))
            except Exception:  # noqa: BLE001
                manifest = {}
        written = []
        for d in dirs:
            entry = {}
            for kind in ("hero", "tall"):
                im = Image.open(os.path.join(tmp, f"{d}-{kind}.png")).convert("RGB")
                for w in WIDTHS:
                    h = round(im.height * w / im.width)
                    name = f"{d}-{kind}-{w}.jpg"
                    im.resize((w, h), Image.LANCZOS).save(os.path.join(dest, name), "JPEG", quality=72 if kind == "hero" else 62,
                                                          optimize=True, progressive=True)
                    entry[f"{kind}-{w}"] = [w, h]
                    written.append(name)
            # the headline as it is really set, and the measured colours and faces (see _hub_shots.mjs)
            tp = os.path.join(tmp, f"{d}-type.png")
            if os.path.exists(tp):
                im = Image.open(tp).convert("RGB")
                w = min(im.width, 720)
                h = round(im.height * w / im.width)
                im.resize((w, h), Image.LANCZOS).save(os.path.join(dest, f"{d}-type.jpg"), "JPEG", quality=78, optimize=True, progressive=True)
                entry["type"] = [w, h]
                written.append(f"{d}-type.jpg")
            lp = os.path.join(tmp, f"{d}-look.json")
            if os.path.exists(lp):
                entry["look"] = json.load(open(lp, encoding="utf-8"))
            manifest[d] = entry
        json.dump(manifest, open(man_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
        written.append("shots.json")
        kb = sum(os.path.getsize(os.path.join(dest, n)) for n in written) / 1024
        print(f"hub_shots: {len(written) - 1} images for {', '.join(dirs)} in {os.path.relpath(dest, out)} ({kb:.0f} KB)")
        if a.save:
            save = os.path.abspath(a.save)
            if os.path.realpath(save) != os.path.realpath(dest):
                os.makedirs(save, exist_ok=True)
                for n in written:
                    shutil.copy2(os.path.join(dest, n), os.path.join(save, n))
                print(f"hub_shots: saved to {os.path.relpath(save)}")
        # the hub was written before the images existed (or with older sizes): point its cards at the new files
        hub = os.path.join(out, "index.html")
        if os.path.exists(hub):
            try:
                sys.path.insert(0, HERE)
                import preview_hub2
                html = open(hub, encoding="utf-8").read()
                new = preview_hub2.apply_shots(html, out)
                if new != html:
                    open(hub, "w", encoding="utf-8").write(new)
                    print("hub_shots: hub cards updated")
            except Exception as e:  # noqa: BLE001
                warn(f"could not update the hub cards ({e})")
        return 0
    finally:
        if srv:
            srv.shutdown()
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
