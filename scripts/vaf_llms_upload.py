#!/usr/bin/env python3
"""Upload brands/vanausdall.llms.txt to HubSpot Files as /vanausdall/launch/llms.txt (access PUBLIC_NOT_INDEXABLE), overwriting any copy.

    CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_llms_upload.py
Staging only: this adds no redirect and does not serve the file at /llms.txt (that waits for go-live). Checks the portal first."""
import json, os, subprocess, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = os.environ["CLIENT_HUBSPOT_TOKEN"]
PORTAL = "50498425"

acct = json.load(urllib.request.urlopen(urllib.request.Request("https://api.hubapi.com/account-info/v3/details", headers={"Authorization": "Bearer " + TOKEN}), timeout=30))
if str(acct["portalId"]) != PORTAL:
    raise SystemExit(f"token is for portal {acct['portalId']}, not {PORTAL}")
out = subprocess.run(["curl", "-s", "-X", "POST", "-H", "@-", "-F", f"file=@{os.path.join(ROOT, 'brands/vanausdall.llms.txt')};filename=llms.txt;type=text/plain",
                      "-F", "folderPath=/vanausdall/launch", "-F", 'options={"access":"PUBLIC_NOT_INDEXABLE","overwrite":true}', "https://api.hubapi.com/files/v3/files"],
                     input=f"Authorization: Bearer {TOKEN}\n".encode(), capture_output=True, timeout=120).stdout
d = json.loads(out or b"{}")
if "id" not in d:
    raise SystemExit("upload failed: " + str(d)[:300])
print("uploaded", d.get("path"), d.get("access"), d.get("size"), "bytes, file id", d["id"])
