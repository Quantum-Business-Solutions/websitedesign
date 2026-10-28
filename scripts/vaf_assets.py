#!/usr/bin/env python3
"""Copy VAF's images into the HubSpot Files tool (portal 50498425) and record the public URLs.

Sources:  preview assets (https://van-ausdall.vercel.app/assets/...), partner logos and the SOC 2 mark
          scraped from vanausdall.com (their own site, their own partners).
Output:   brands/vanausdall.asset-map.json   {"assets/x.jpg": "https://...hubspotusercontent.../vaf/assets/x.jpg", "partners/canon": "..."}

    CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_assets.py
"""
import json, os, re, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = os.environ["CLIENT_HUBSPOT_TOKEN"]
PREVIEW = "https://van-ausdall.vercel.app"
SITE = "https://www.vanausdall.com"
MAP = os.path.join(ROOT, "brands/vanausdall.asset-map.json")
PARTNERS = ("8x8.png artic-wolf-logo.png autotask.jpg appdirect.png brother.png canon.png datto.jpg agent.png fujitsu.png "
            "fortinet.png fortinet-voice.png hp.png hevlet.png elevate.png juniper.png knowbe4.png kyocera.png n-able.png "
            "microsoft-patner.png mitel-logo.png opex.png onbase.png ringcentral.png rapid.png ricoh.jpg square9.png "
            "scalegray.png sophos-logo.png tenable.png zebra.png vmware.png acronis.png").split()


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, **kw)


def upload(local, folder, name):
    out = sh(["curl", "-s", "-X", "POST", "-H", "@-", "-F", f"file=@{local};filename={name}",
              "-F", 'options={"access":"PUBLIC_NOT_INDEXABLE","overwrite":true}', "-F", f"folderPath={folder}",
              "https://api.hubapi.com/files/v3/files"], input=f"Authorization: Bearer {TOKEN}\n".encode()).stdout
    d = json.loads(out)
    if "defaultHostingUrl" not in d:
        raise SystemExit(f"upload failed for {name}: {out[:300]!r}")
    return d["defaultHostingUrl"]


def fetch(url, dest):
    r = sh(["curl", "-s", "-f", "-o", dest, url])
    return r.returncode == 0 and os.path.getsize(dest) > 200


def main():
    amap = json.load(open(MAP)) if os.path.exists(MAP) else {}
    content = open(os.path.join(ROOT, "brands/vanausdall.content.json"), encoding="utf-8").read()
    paths = sorted(set(re.findall(r'(?:\.\./)*(assets/[A-Za-z0-9_./-]+\.(?:jpg|jpeg|png|webp|svg))', content)))
    tmp = tempfile.mkdtemp()
    jobs = [(p, f"{PREVIEW}/{p}", "/vaf/" + os.path.dirname(p)) for p in paths]
    for f in PARTNERS:
        jobs.append((f"partners/{os.path.splitext(f)[0]}", f"{SITE}/images/partners/{f}", "/vaf/partners"))
    jobs.append(("badges/soc2", f"{SITE}/images/soc-logo.png", "/vaf/badges"))
    for key, url, folder in jobs:
        if key in amap:
            continue
        ext = os.path.splitext(url)[1]
        local = os.path.join(tmp, re.sub(r"\W", "_", key) + ext)
        if not fetch(url, local):
            print("  SKIP (fetch failed)", url); continue
        name = (os.path.basename(key) if key.startswith("assets/") else os.path.basename(key)) + (ext if not key.startswith("assets/") else "")
        amap[key] = upload(local, folder, os.path.basename(url) if not key.startswith("assets/") else os.path.basename(key))
        print("  ok", key, "->", amap[key].split("/")[-1])
        json.dump(amap, open(MAP, "w"), indent=1, sort_keys=True)
    json.dump(amap, open(MAP, "w"), indent=1, sort_keys=True)
    print(len(amap), "assets mapped")


main()
