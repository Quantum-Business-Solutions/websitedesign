#!/usr/bin/env python3
"""reskin.py, reading the source theme from themes/source/ instead of from the portal.

Why: reskin.py clones a theme INSIDE one portal (it reads the source theme with the same
token it writes with). The nine Quantum themes live in the QBS portal, so a brand-new
client portal has nothing to clone from. themes/source/ is a complete mirror of the nine,
so this wrapper swaps the two read functions for local-disk reads and leaves every other
rule in reskin.py untouched: the contrast gate, the refusal to write to one of the nine,
the Organization schema fix, and the propose-then-confirm step (--apply --approved-by).

Usage (identical to reskin.py plan; the token is the CLIENT's, never ours):

  CLIENT_HUBSPOT_TOKEN=... python3 scripts/reskin_from_source.py --portal 50498425 plan \
      --theme "Quantum Showcase" --client "Van Ausdall and Farrar" \
      --accent "#2A71AF" --ground light \
      --org-name "Van Ausdall & Farrar, Inc." --org-url "https://www.vanausdall.com"
  ... add  --apply --approved-by "<name>"  to write to the portal's DRAFT environment.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reskin  # noqa: E402

SRC = os.path.join(os.path.dirname(HERE), "themes", "source")


def _repair_fields(raw):
    """HubSpot rejects a repeating field (one with `occurrence`) whose default is not an
    array: MODULE_DATA_VALIDATION_INVALID_FORMAT_FOR_FIELD_WITH_OCCURRENCE. The shared
    themes carry one such field (quantum-org-schema: org_sameas). We repair it on the way
    OUT to the client portal and leave the mirror in themes/source/ untouched."""
    import json
    try:
        data = json.loads(raw)
    except ValueError:
        return raw
    changed = []

    def fix(fields):
        for x in fields if isinstance(fields, list) else []:
            if not isinstance(x, dict):
                continue
            if "occurrence" in x and not isinstance(x.get("default"), list):
                x["default"] = [] if x.get("default") in ("", None) else [x["default"]]
                changed.append(x.get("name"))
            fix(x.get("children"))

    fix(data)
    return json.dumps(data, indent=2, ensure_ascii=False) if changed else raw


def _local_read(theme_path, token=None):
    with open(os.path.join(SRC, theme_path), encoding="utf-8") as fh:
        raw = fh.read()
    if theme_path.endswith("fields.json") and "/modules/" in theme_path:
        raw = _repair_fields(raw)
    return raw


def _local_walk(path, token=None, depth=0):
    base = os.path.join(SRC, path)
    for root, _dirs, files in os.walk(base):
        for f in sorted(files):
            full = os.path.join(root, f)
            yield os.path.relpath(full, SRC).replace(os.sep, "/")


reskin.read_source = _local_read
reskin.walk = _local_walk

# RESKIN_ENV=published writes the clone to the portal's PUBLISHED environment (default is
# draft). Pages can only use published templates, so a clone that will carry pages needs it.
_ENV = os.environ.get("RESKIN_ENV", "draft")
_orig_put = reskin.put_file


def _put(path, token, content, env="draft"):
    return _orig_put(path, token, content, _ENV)


reskin.put_file = _put

if __name__ == "__main__":
    sys.exit(reskin.main())
