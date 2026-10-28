#!/usr/bin/env python3
"""Offline checks for a VAF module + its mapper, before anything is uploaded.

    python3 scripts/vaf_check.py themes/vaf/modules/vaf-hero.module [more modules...]
    python3 scripts/vaf_check.py --mapper scripts/vaf_map_a.py     # every REGISTRY entry against every page that uses it

Fails on: invalid JSON, forbidden/duplicate field ids, repeater defaults that are not arrays or violate min,
module.html reading a field that does not exist, mapper params that are not fields (or group children that are not
children), and mapper output that is not JSON-serialisable.
"""
import importlib.util, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
FORBIDDEN = {"body", "label", "value", "name", "type", "id", "default", "content"}
HOST_OK = {"PAGE", "BLOG_POST", "BLOG_LISTING"}


def walk(fields, seen, errs, where):
    for f in fields:
        n = f.get("name")
        if n in FORBIDDEN:
            errs.append(f"{where}: forbidden field id {n!r}")
        if n in seen:
            errs.append(f"{where}: duplicate field id {n!r} (ids must be unique module-wide, including nested)")
        seen.add(n)
        if f.get("occurrence"):
            occ, d = f["occurrence"], f.get("default")
            if not isinstance(d, list):
                errs.append(f"{where}: repeater {n!r} default must be an array")
            elif len(d) < occ.get("min", 0):
                errs.append(f"{where}: repeater {n!r} default has {len(d)} items, min is {occ.get('min')}")
            if occ.get("default", 0) < occ.get("min", 0):
                errs.append(f"{where}: repeater {n!r} occurrence.default < min")
        if f.get("children"):
            walk(f["children"], seen, errs, where)


def names(fields):
    return {f["name"]: f for f in fields}


def check_module(path):
    errs = []
    try:
        fields = json.load(open(os.path.join(path, "fields.json")))
        meta = json.load(open(os.path.join(path, "meta.json")))
    except Exception as e:
        return [f"{path}: {e}"], None
    walk(fields, set(), errs, path)
    for t in meta.get("host_template_types", []):
        if t not in HOST_OK:
            errs.append(f"{path}: host_template_types {t!r} not allowed")
    if os.path.exists(os.path.join(path, "module.js")) and "ANY" in meta.get("host_template_types", []):
        errs.append(f"{path}: module.js not allowed with ANY")
    allf = set()
    def collect(fs):
        for f in fs:
            allf.add(f["name"]); collect(f.get("children", []))
    collect(fields)
    html = open(os.path.join(path, "module.html")).read()
    for m in set(re.findall(r"\bmodule\.([A-Za-z_][A-Za-z0-9_]*)", html)):
        if m not in allf and m not in {"css_class", "id", "name", "module_id", "widget_name", "path", "label"}:
            errs.append(f"{path}/module.html reads module.{m} which is not a field")
    return errs, fields


def check_params(params, fields, where, errs):
    fm = names(fields)
    for k, v in params.items():
        if k not in fm:
            errs.append(f"{where}: param {k!r} is not a field"); continue
        f = fm[k]
        if f.get("children") and isinstance(v, list):
            cm = names(f["children"])
            for item in v:
                for ck, cv in item.items():
                    if ck not in cm:
                        errs.append(f"{where}: {k}[].{ck} is not a child field")
                    elif cm[ck].get("children") and isinstance(cv, list):
                        check_params_list(cv, cm[ck], f"{where}.{k}.{ck}", errs)
        elif f.get("children") and not isinstance(v, list):
            errs.append(f"{where}: repeater {k!r} must be given a list")
    json.dumps(params)


def check_params_list(items, f, where, errs):
    cm = names(f["children"])
    for item in items:
        for ck in item:
            if ck not in cm:
                errs.append(f"{where}: .{ck} is not a child field")


def check_mapper(pyfile):
    spec = importlib.util.spec_from_file_location("m", pyfile); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    content = json.load(open(os.path.join(ROOT, "brands/vanausdall.content.json"), encoding="utf-8"))
    errs, used = [], {}
    for t, (mod, fn) in m.REGISTRY.items():
        mp = os.path.join(ROOT, "themes/vaf/modules", mod + ".module")
        e, fields = check_module(mp); errs += e
        if fields is None:
            continue
        n = 0
        for p in content["pages"]:
            for s in p["sections"]:
                if s["type"] == t:
                    n += 1
                    out = fn(s)
                    out = out if isinstance(out, list) else [out]
                    for o in out:
                        check_params(o[1] if isinstance(o, tuple) else o, fields, f"{t} on {p['file']}", errs)
        used[t] = n
    print("sections checked per type:", used)
    return errs


if __name__ == "__main__":
    a = sys.argv[1:]
    errs = []
    if a and a[0] == "--mapper":
        errs = check_mapper(a[1])
    else:
        for p in a:
            e, _ = check_module(p); errs += e
    print("\n".join(sorted(set(errs))[:60]) or "OK")
    sys.exit(1 if errs else 0)
