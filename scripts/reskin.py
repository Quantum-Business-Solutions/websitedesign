#!/usr/bin/env python3
"""
Clone a Quantum theme and re-skin it to a client's brand.

Roadmap item 1. Replaces the by-hand operation in process/reskin.md, and carries the
item-5 Organization schema fix in the same pass so it can never be forgotten.

SAFETY
  Read-only by default. Every mutating run requires --apply AND --approved-by "<name>".
  Without both, the script prints the exact change table and exits without touching
  the portal. That table IS the propose-then-confirm proposal required by the
  qbs-hubspot-private-app skill.

  The nine themes are never modified. The script refuses to write to a path that
  matches a known Quantum theme name.

AUTH
  Token from $QBS_HUBSPOT_TOKEN, or --token. Never written to disk, never logged.

USAGE
  # what is the current state of a theme?
  reskin.py inspect --theme "Quantum Press"

  # what would a re-skin change? (read-only -- prints the proposal table)
  reskin.py plan --theme "Quantum Press" --client "Meridian Dental" \
      --accent "#1E6B8C" --ground light \
      --org-name "Meridian Dental Group" --org-url "https://meridiandental.com"

  # execute it
  reskin.py plan ... --apply --approved-by "Shawn"
"""
from __future__ import annotations

import argparse
import colorsys
import json
import os
import re
import sys
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
import urllib.parse
import uuid

API = "https://api.hubapi.com"
EXPECTED_PORTAL = "20682069"

NINE = [
    "Quantum Flagship", "Quantum Void", "Quantum Signal", "Quantum Converter",
    "Quantum Clean", "Quantum Press", "Quantum Paper", "Quantum Journal",
    "Quantum Showcase",
]

# ground -> which themes are light. From themes/catalogue.md.
LIGHT_THEMES = {"Quantum Clean", "Quantum Press", "Quantum Paper",
                "Quantum Journal", "Quantum Showcase"}

# The re-skin surface is NOT fields.json.
#
# QA, 2026-09-03: `theme.colors` is referenced in ZERO files across all nine themes --
# not in quantum.css (which contains no HubL at all), not in base.html, not in any of
# the 57 module.html files. The five colour fields in fields.json are dead: setting them
# changes nothing on the rendered page. `appearance.mode` is the only live field, and it
# only drives the .only-dark/.only-light logo visibility rules.
#
# The REAL surface is css/quantum.css, which has this architecture in every theme:
#
#   :root                                    base --q-* tokens (identical in all nine)
#   [data-theme="dark"] / ["light"]          the mode palettes
#   [data-qdir="clean"] ... ["void"]         ALL NINE directions, in every theme's CSS
#   /* NATIVE DIRECTION: <Theme> */          pins this theme's direction over BOTH modes
#     :root, [data-theme="dark"], [data-theme="light"] { ... }
#
# The native-direction block is last and equal-specificity, so it wins -- which is why
# `appearance.mode` has no effect on the palette, and why the light themes render light
# despite defaulting to `dark`.
#
# Re-skinning therefore means rewriting the native-direction block. Twelve custom
# properties, one contiguous block, one file. Typefaces are in it too, so type IS
# re-skinnable -- contrary to what themes/catalogue.md used to say.

NATIVE_RE = re.compile(
    r"(/\*\s*=+\s*NATIVE DIRECTION:[^*]*\*/\s*"
    r":root\s*,\s*\[data-theme=\"dark\"\]\s*,\s*\[data-theme=\"light\"\]\s*\{)(.*?)(\})",
    re.S)

# custom property -> what it does. Order is the order they get written.
SURFACE = [
    ("--q-gold",        "primary accent FILL: buttons, chips, rules, icons"),
    ("--q-gold-bright", "accent hover/active"),
    ("--q-gold-dim",    "accent, de-emphasised"),
    ("--accent-ink",    "accent TEXT on a light ground -- darkened until it clears AA"),
    ("--accent-lift",   "accent TEXT on a dark band"),
    ("--q-serif",       "heading face (theme identity)"),
    ("--q-sans",        "body face"),
    ("--bg",            "page ground"),
    ("--bg-alt",        "alternating band / raised surface"),
    ("--fg",            "body text"),
    ("--fg-muted",      "secondary text"),
    ("--border",        "hairlines"),
    ("--card",          "card surface"),
    ("--cta-fg",        "text ON the accent -- contrast-critical"),
]

MODE_FIELD = "appearance.mode"


# --------------------------------------------------------------------------- http

class HubSpotError(RuntimeError):
    pass


def _req(method: str, path: str, token: str, body: bytes | None = None, ctype=None):
    """Transport is curl, not urllib.

    This environment routes outbound HTTPS through an agent proxy that urllib
    cannot negotiate (it returns 405 on CONNECT). curl inherits the proxy and CA
    configuration from the environment, so shelling out is both simpler and more
    portable than reimplementing that here.

    The token is passed via a header file on stdin, never as an argv element, so
    it cannot leak into `ps` output or shell history.
    """
    url = path if path.startswith("http") else API + path
    cmd = ["curl", "-sS", "--fail-with-body", "-X", method,
           "-H", "@-",                     # read headers from stdin
           "-w", "\n__HTTP_STATUS__%{http_code}", url]
    headers = f"Authorization: Bearer {token}\n"
    if ctype:
        headers += f"Content-Type: {ctype}\n"

    if body is not None:
        with tempfile.NamedTemporaryFile(delete=False) as fh:
            fh.write(body)
            tmp = fh.name
        cmd[-1:-1] = ["--data-binary", f"@{tmp}"]
    else:
        tmp = None

    try:
        proc = subprocess.run(cmd, input=headers.encode(), capture_output=True, timeout=120)
    finally:
        if tmp:
            os.unlink(tmp)

    out = proc.stdout
    marker = b"\n__HTTP_STATUS__"
    status = None
    if marker in out:
        out, _, tail = out.rpartition(marker)
        status = tail.decode().strip()

    if proc.returncode != 0 and status not in ("200", "201", "204"):
        err = (proc.stderr.decode("utf-8", "replace") or out.decode("utf-8", "replace"))[:400]
        raise HubSpotError(f"{method} {url} -> {status or 'transport error'}: {err}")
    if status and not status.startswith("2"):
        raise HubSpotError(f"{method} {url} -> {status}: {out.decode('utf-8', 'replace')[:400]}")
    return out


def get_json(path, token):
    return json.loads(_req("GET", path, token))


def get_text(path, token):
    return _req("GET", path, token).decode("utf-8")


def read_source(theme_path: str, token: str) -> str:
    """Read one file out of a theme. `theme_path` is portal-relative and NOT
    pre-encoded, e.g. 'Quantum Press/fields.json'."""
    return get_text(
        "/cms/v3/source-code/published/content/" + urllib.parse.quote(theme_path), token)


def put_file(path: str, token: str, content: str):
    """Create or update a file in the DRAFT environment via multipart upload."""
    boundary = f"----qbs{uuid.uuid4().hex}"
    payload = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(path)}"\r\n'
        "Content-Type: application/octet-stream\r\n\r\n"
    ).encode() + content.encode("utf-8") + f"\r\n--{boundary}--\r\n".encode()
    enc = urllib.parse.quote(path)
    return _req("PUT", f"/cms/v3/source-code/draft/content/{enc}", token,
                body=payload, ctype=f"multipart/form-data; boundary={boundary}")


def verify_portal(token: str, expected: str | None = None) -> dict:
    """Confirm the token belongs to the portal the caller NAMED.

    The guard used to be "must be 20682069", which made this script unusable for the
    case it exists to serve: a client's site lives in the client's portal, with
    CLIENT_HUBSPOT_TOKEN. Revolution's theme is in 47019673. The real risk is not
    "wrong portal" in the abstract -- it is acting on a portal you did not mean to,
    so the check is now "the portal you named must equal the token's portal."

    Touching one of the nine is prevented separately, by a PATH check on the target,
    which is correct in any portal."""
    info = get_json("/account-info/v3/details", token)
    pid = str(info.get("portalId"))
    want = str(expected or EXPECTED_PORTAL)
    if pid != want:
        raise SystemExit(
            f"REFUSING TO PROCEED. You named portal {want}; this token belongs to {pid}.\n"
            f"  - QBS portal {EXPECTED_PORTAL}: use $QBS_HUBSPOT_TOKEN\n"
            f"  - a client portal: pass --portal <id> and use that client's token\n"
            "Never use the QBS token against a client portal, or the OAuth MCP for either."
        )
    if pid != EXPECTED_PORTAL:
        print(f"note: operating on CLIENT portal {pid} "
              f"({info.get('companyName') or 'unnamed'}), not QBS {EXPECTED_PORTAL}.",
              file=sys.stderr)
    return info


# ------------------------------------------------------------------- theme reading

def children(path: str, token: str):
    enc = urllib.parse.quote(path)
    meta = get_json(f"/cms/v3/source-code/published/metadata/{enc}?properties=children", token)
    out = []
    for c in meta.get("children") or []:
        out.append(c if isinstance(c, str) else c.get("name", ""))
    return [c for c in out if c]


def walk(path: str, token: str, depth=0):
    """Yield every file path under a theme. Folders are anything without a dot,
    plus HubSpot's *.module directories."""
    if depth > 6:
        return
    for name in children(path, token):
        child = f"{path}/{name}"
        is_dir = name.endswith(".module") or "." not in name
        if is_dir:
            yield from walk(child, token, depth + 1)
        else:
            yield child


def read_fields(theme: str, token: str):
    return json.loads(read_source(f"{theme}/fields.json", token))


def current_mode(fields) -> str | None:
    """The only live field. colors.* is dead -- see the note at the top of this file."""
    for group in fields:
        if group.get("name") != "appearance":
            continue
        for child in group.get("children") or []:
            if child.get("name") == "mode":
                return child.get("default")
    return None


ORG_RE = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>\s*(\{.*?"@type"\s*:\s*"Organization".*?\})\s*</script>',
    re.S,
)


def parse_native(css: str) -> dict:
    """Pull the twelve custom properties out of the native-direction block."""
    m = NATIVE_RE.search(css)
    if not m:
        return {}
    body = m.group(2)
    out = {}
    for decl in body.split(";"):
        if ":" not in decl:
            continue
        k, _, v = decl.partition(":")
        k, v = k.strip(), v.strip()
        if k.startswith("--"):
            out[k] = v
    return out


def patch_native(css: str, new_vals: dict) -> str:
    """Rewrite the native-direction block, preserving any property we don't manage."""
    m = NATIVE_RE.search(css)
    if not m:
        raise HubSpotError("no NATIVE DIRECTION block in this stylesheet -- "
                           "the theme's CSS architecture is not what this script expects")
    current = parse_native(css)
    merged = dict(current)
    merged.update({k: v for k, v in new_vals.items() if v is not None})
    managed = [k for k, _ in SURFACE]
    ordered = [k for k in managed if k in merged] + [k for k in merged if k not in managed]
    body = "\n  " + "\n  ".join(f"{k}:{merged[k]};" for k in ordered) + "\n"
    return css[:m.start(2)] + body + css[m.end(2):]


def find_org_block(base_html: str):
    m = ORG_RE.search(base_html)
    return m.group(0) if m else None


# ------------------------------------------------------------------------- colours

def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(*(max(0, min(255, round(v * 255))) for v in (r, g, b)))


def lighten(hex_color: str, amount=0.12) -> str:
    """gold_bright is DERIVED, not extracted -- same hue, lifted lightness.
    process/reskin.md rule 2."""
    h, l, s = colorsys.rgb_to_hls(*hex_to_rgb(hex_color))
    return rgb_to_hex(*colorsys.hls_to_rgb(h, min(1.0, l + amount), s))


def tinted_neutral(hue_source: str, lightness: float, sat: float) -> str:
    """Bias neutrals toward a hue -- a pure mid-grey reads as inherited, a neutral
    with a slight hue cast reads as chosen. House guardrail, survives re-skinning.
    process/reskin.md rule 3.

    Saturation has to RISE at the extremes. At lightness 0.05 a saturation of 0.10
    is arithmetically invisible -- it rounds to pure grey and silently fails the
    guardrail it was written to satisfy. These values were checked by eye against
    the rendered hex, not assumed."""
    h, _l, _s = colorsys.rgb_to_hls(*hex_to_rgb(hue_source))
    return rgb_to_hex(*colorsys.hls_to_rgb(h, lightness, sat))


# lightness / saturation per ground role. Derived from the QBS originals: with
# accent #c4a44a the paper role reproduces #fbfaf6 exactly, which is the real
# QBS value -- so these are calibrated, not invented.
NEUTRAL_ROLES = {
    "colors.void":  (0.050, 0.30),
    "colors.navy":  (0.120, 0.22),
    "colors.paper": (0.975, 0.40),
}


def derive_native(accent: str, ground: str, neutral_hue: str | None = None,
                  serif: str | None = None, sans: str | None = None) -> dict:
    """Build the twelve native-direction values from an accent and a ground.

    neutral_hue defaults to the accent, per the guardrail. Pass a different hex for a
    complementary scheme -- which is what the QBS originals actually do: gold accent
    (#c4a44a) against blue-cast neutrals (#080b12 / #101725). Both are legitimate, so
    the choice is explicit rather than assumed."""
    accent = accent if accent.startswith("#") else "#" + accent
    src = neutral_hue or accent
    light = ground == "light"

    out = {
        "--q-gold": accent.lower(),
        "--q-gold-bright": lighten(accent, 0.10 if light else 0.12) if not light
                           else lighten(accent, -0.10),
        "--q-gold-dim": lighten(accent, -0.06),
        "--bg":       tinted_neutral(src, 0.965 if light else 0.050, 0.40 if light else 0.30),
        "--bg-alt":   tinted_neutral(src, 0.992 if light else 0.115, 0.45 if light else 0.22),
        "--fg":       tinted_neutral(src, 0.130 if light else 0.900, 0.10),
        "--fg-muted": tinted_neutral(src, 0.360 if light else 0.640, 0.08),
        "--card":     tinted_neutral(src, 0.992 if light else 0.075, 0.30),
        "--border":   rgba_from(accent, 0.22 if light else 0.14),
        # Text ON the accent. Chosen for contrast against the accent, not for looks.
        "--cta-fg":   best_on(accent),
    }
    # If neither near-black nor near-white clears AA on the accent, the accent itself is
    # in the awkward mid band. Nudge the FILL until its own text colour clears -- the
    # brand hue is preserved, and a button nobody can read is not a button.
    if contrast_ratio(out["--q-gold"], out["--cta-fg"]) < 4.5:
        out["--q-gold"] = darken_until(out["--q-gold"], out["--cta-fg"], 4.5)
        out["--q-gold-bright"] = lighten(out["--q-gold"], 0.10 if light else -0.10)
        out["--q-gold-dim"] = lighten(out["--q-gold"], -0.06)
    # Accent text, on both grounds. Derived, never picked.
    out["--accent-ink"] = darken_until(accent, out["--bg"], 4.5)
    dark_band = out["--bg"] if not light else tinted_neutral(src, 0.10, 0.28)
    out["--accent-lift"] = darken_until(accent, dark_band, 4.5)

    if serif:
        out["--q-serif"] = serif
    if sans:
        out["--q-sans"] = sans
    return out


def rgba_from(hex_color: str, alpha: float) -> str:
    r, g, b = (round(v * 255) for v in hex_to_rgb(hex_color))
    return f"rgba({r},{g},{b},{alpha})"


def relative_luminance(hex_color: str) -> float:
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in hex_to_rgb(hex_color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a: str, b: str) -> float:
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def darken_until(fg: str, bg: str, target: float = 4.5, step: float = 0.02) -> str:
    """Walk lightness down (or up, on a dark ground) until fg clears `target` on bg.

    This is the two-token accent fix from themes/architecture.md, and it is the reason
    a saturated brand colour can be both a working button and readable text. A single
    accent cannot do both: Revolution's amber is ~2:1 on white, so as text it fails on
    exactly the numbers a buyer most wants to read -- while darkening it far enough to
    read would kill the button.

    Hue and saturation are preserved, so it still looks like the brand."""
    h, l, sat = colorsys.rgb_to_hls(*hex_to_rgb(fg))
    going_darker = relative_luminance(bg) > 0.18
    for _ in range(50):
        cand = rgb_to_hex(*colorsys.hls_to_rgb(h, max(0.0, min(1.0, l)), sat))
        if contrast_ratio(cand, bg) >= target:
            return cand
        l = l - step if going_darker else l + step
        if l <= 0 or l >= 1:
            break
    return rgb_to_hex(*colorsys.hls_to_rgb(h, 0.02 if going_darker else 0.98, sat))


def best_on(bg: str) -> str:
    """Pick near-black or near-white for text on `bg`, whichever has more contrast.
    Never composite text with opacity -- guardrail. This is a real colour."""
    dark, light_ = "#0b0d10", "#fffdf9"
    return dark if contrast_ratio(bg, dark) >= contrast_ratio(bg, light_) else light_


# --------------------------------------------------------------------------- schema

QBS_PROFILES = ("quantum-business-solutions", "thequantumleap", "shawn-peterson")


def check_sameas(sameas):
    """Advisories for the Organization's sameAs. sameAs is the entity-resolution
    signal: it is how an answer engine confirms *this* Organization is *that*
    LinkedIn company page, and not a namesake. The LinkedIn company URL is the
    one that matters most, because it is the profile with the most corroborating
    third-party data (headcount, location, employees) that engines already trust."""
    notes = []
    urls = list(sameas or [])
    if not urls:
        notes.append("ADVISORY sameAs is empty. Add at least the LinkedIn company URL "
                     "(brands/<client>.md -> Entity facts). Without it the entity stands alone.")
        return notes
    if not any("linkedin.com/company/" in u for u in urls):
        notes.append("ADVISORY sameAs has no linkedin.com/company/ URL - the single most useful "
                     "one for entity resolution. Personal profiles (linkedin.com/in/) do not count.")
    for u in urls:
        if not u.startswith("https://"):
            notes.append(f"ADVISORY sameAs entry is not an absolute https URL: {u}")
        if any(q in u.lower() for q in QBS_PROFILES):
            notes.append(f"BLOCKING sameAs points at a QBS profile on a client site: {u}")
    return notes


def build_org_schema(name, url, description=None, logo=None, sameas=None) -> str:
    """Fail-safe: with no name we emit NOTHING. Absent markup is safe -- an engine
    infers the entity from the page. Wrong markup is a false statement in the one
    format engines are built to trust. process/structured-data.md."""
    if not name:
        return ""
    org = {"@context": "https://schema.org", "@type": "Organization", "name": name}
    if url:
        org["url"] = url
    if description:
        org["description"] = description
    if logo:
        org["logo"] = logo
    if sameas:
        # An empty sameAs asserts nothing and reads as a template left unfilled. Omit it.
        org["sameAs"] = list(sameas)
    return ('<script type="application/ld+json">'
            + json.dumps(org, separators=(",", ":"), ensure_ascii=False)
            + "</script>")


# ----------------------------------------------------------------------- reporting

def table(rows, headers):
    widths = [max(len(str(r[i])) for r in [headers] + rows) for i in range(len(headers))]
    line = "  ".join("-" * w for w in widths)
    print("  ".join(str(h).ljust(w) for h, w in zip(headers, widths)))
    print(line)
    for r in rows:
        print("  ".join(str(c).ljust(w) for c, w in zip(r, widths)))


# ------------------------------------------------------------------------ commands

def cmd_inspect(a, token):
    verify_portal(token, a.portal)
    theme = a.theme
    print(f"\n=== {theme} ===\n")

    css = read_source(f"{theme}/css/quantum.css", token)
    native = parse_native(css)
    if not native:
        print("  no NATIVE DIRECTION block found -- unexpected CSS architecture")
    else:
        print("Live re-skin surface (css/quantum.css, NATIVE DIRECTION block):\n")
        rows = [[k, native.get(k, "(absent)"), role] for k, role in SURFACE]
        table(rows, ["custom property", "value", "role"])
        cta, accent = native.get("--cta-fg", ""), native.get("--q-gold", "")
        if cta.startswith("#") and accent.startswith("#"):
            cr = contrast_ratio(accent, cta)
            print(f"\n  --cta-fg on --q-gold: {cr:.2f}:1 "
                  f"({'PASS' if cr >= 4.5 else 'FAIL'} WCAG AA normal text, needs 4.5)")

    fields = read_fields(theme, token)
    mode = current_mode(fields)
    ground = "light" if theme in LIGHT_THEMES else "dark"
    print(f"\nfields.json: {', '.join(f'{g.get(chr(110)+chr(97)+chr(109)+chr(101))}' for g in fields)}")
    print(f"  appearance.mode default = {mode}   (theme's true ground: {ground})")
    print("  colors.* -- DEAD. `theme.colors` is referenced in no file in this theme.")

    base = read_source(f"{theme}/templates/layouts/base.html", token)
    print("\nJSON-LD in templates/layouts/base.html:")
    blocks = re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', base, re.S)
    if not blocks:
        print("  none")
    for b in blocks:
        try:
            d = json.loads(b)
            t, nm = d.get("@type"), d.get("name") or d.get("url") or ""
        except Exception:
            t, nm = "(unparseable)", ""
        flag = ""
        if isinstance(nm, str) and "Quantum Business Solutions" in nm:
            flag = "   <-- WRONG ENTITY for a client build"
        print(f"  {t}: {nm}{flag}")

    # QBS identity leaks beyond the schema
    print("\nQBS identity elsewhere in the theme:")
    for rel in ("templates/partials/header.html", "templates/partials/footer.html"):
        try:
            txt = read_source(f"{theme}/{rel}", token)
        except HubSpotError:
            print(f"  {rel}: not found")
            continue
        leaks = []
        for pat, label in ((r"thequantumleap\.business", "QBS domain"),
                           (r"quantum-business-solutions", "QBS LinkedIn"),
                           (r"Quantum Business Solutions", "QBS name"),
                           (r"Quantum Academy", "Quantum Academy link")):
            n = len(re.findall(pat, txt, re.I))
            if n:
                leaks.append(f"{label} x{n}")
        print(f"  {rel}: {', '.join(leaks) if leaks else 'clean'}")
    print("  NOTE: partials are templateType global_partial -- portal-scoped singletons.\n"
          "        Per-client overrides need care. See process/reskin.md.")

    print("\nPerformance primitives:")
    print(f"  fonts via CSS @import : {'@import' in css}")
    print(f"  preconnect in base    : {'preconnect' in base}")
    print(f"  preload in base       : {'preload' in base}")


def cmd_plan(a, token):
    info = verify_portal(token, a.portal)
    src, client = a.theme, a.client
    target = a.target or f"{client} - {src.replace('Quantum ', '')}"

    if target in NINE or target.strip() in NINE:
        raise SystemExit(f"REFUSING: target '{target}' is one of the nine themes. "
                         "The nine are the product line, shared across every client. "
                         "Clone to a client-specific child instead.")
    if src not in NINE:
        print(f"warning: source '{src}' is not one of the nine themes", file=sys.stderr)

    ground = a.ground or ("light" if src in LIGHT_THEMES else "dark")
    css = read_source(f"{src}/css/quantum.css", token)
    old_native = parse_native(css)
    new_native = (derive_native(a.accent, ground, a.neutral_hue, a.serif, a.sans)
                  if a.accent else {})
    for k, v in (a.set or {}).items():
        new_native[k if k.startswith("--") else "--" + k] = v

    base = read_source(f"{src}/templates/layouts/base.html", token)
    # Only the Organization block is ours to replace. Matching every ld+json block meant
    # a Void clone got three identical Organization nodes and lost its WebSite (which
    # still controls the site name in results) and its BreadcrumbList.
    all_ld = re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', base, re.S)
    all_blocks = re.findall(r'<script[^>]*application/ld\+json[^>]*>.*?</script>', base, re.S)
    old_orgs, kept_types = [], []
    for blk, body in zip(all_blocks, all_ld):
        try:
            t = json.loads(body).get("@type")
        except Exception:
            t = None
        if t == "Organization" or (isinstance(t, list) and "Organization" in t):
            old_orgs.append(blk)
        elif t:
            kept_types.append(t)
    new_org = build_org_schema(a.org_name, a.org_url, a.org_description,
                               a.org_logo, a.org_sameas)
    sameas_notes = check_sameas(a.org_sameas) if a.org_name else []

    files = sorted(walk(src, token))

    print(f"\n{'=' * 78}")
    print(f"PROPOSED CHANGE - portal {info.get('portalId')} ({info.get('accountType')})")
    print(f"{'=' * 78}\n")
    print(f"  clone   {src}")
    print(f"     ->   {target}")
    print(f"  files   {len(files)} copied into the DRAFT environment")
    print(f"  source  UNTOUCHED (the nine are never edited in place)")
    print(f"  ground  {ground}\n")

    print("css/quantum.css - NATIVE DIRECTION block (this is the real re-skin surface):\n")
    rows = []
    for k, role in SURFACE:
        o = old_native.get(k, "(absent)")
        n = new_native.get(k, o)
        rows.append([k, o, n, "changed" if str(o) != str(n) else "-"])
    table(rows, ["custom property", "current", "new", ""])

    # Contrast gate. A direction that fails this does not go to a client.
    accent = new_native.get("--q-gold", old_native.get("--q-gold", ""))
    problems, advisories = [], []
    CHECKS = (
        ("--cta-fg", "--q-gold", 4.5, "CTA text on accent", True),
        ("--fg", "--bg", 4.5, "body text on ground", True),
        ("--fg-muted", "--bg", 4.5, "secondary text on ground", True),
        ("--accent-ink", "--bg", 4.5, "accent TEXT on ground", True),
        # WCAG 1.4.11: a control's boundary needs 3:1 against what's behind it. A
        # saturated brand colour on a light ground rarely clears that, and the fix is a
        # border on the control -- not a different brand colour. Advisory, not blocking.
        ("--q-gold", "--bg", 3.0, "accent FILL on ground (control edge)", False),
    )
    for fg_key, bg_key, need, what, blocking in CHECKS:
        fg = new_native.get(fg_key, old_native.get(fg_key, ""))
        bg = new_native.get(bg_key, old_native.get(bg_key, ""))
        if not (fg.startswith("#") and bg.startswith("#")):
            continue
        cr = contrast_ratio(fg, bg)
        ok = cr >= need
        mark = "PASS" if ok else ("FAIL" if blocking else "WARN")
        if not ok:
            (problems if blocking else advisories).append(f"{what}: {cr:.2f}:1 (needs {need})")
        print(f"  {mark}  {what:38} {cr:5.2f}:1  (needs {need})")
    if advisories:
        print("\n  ADVISORY (does not block):")
        for ad in advisories:
            print(f"    - {ad}")
        print("    A brand accent this saturated needs a 1px border or an outline on")
        print("    accent-filled controls so the control's edge is discernible.")
    if problems:
        print("\n  CONTRAST FAILURES:")
        for pr in problems:
            print(f"    - {pr}")
        print("  Fix with e.g. --set bg=#ffffff before applying. Never solve contrast")
        print("  with opacity; use a real colour. See design/guardrails.md.")

    print("\nfields.json:")
    print(f"  appearance.mode -> {ground}   (only live field; drives .only-dark/.only-light)")
    print("  colors.*        -> left alone. Dead fields; `theme.colors` is referenced nowhere.")

    print("\ntemplates/layouts/base.html - JSON-LD:\n")
    for b in old_orgs:
        print(f"  REMOVE  {b[:130]}")
    print(f"  INSERT  {new_org[:130] or '(nothing - no --org-name given, omitted by design)'}")
    if kept_types:
        print(f"  KEEP    {', '.join(kept_types)} (left untouched)")
    for n in sameas_notes:
        print(f"  {n}")
        if n.startswith("BLOCKING"):
            problems.append(n)
    if not a.org_name:
        print("\n  NOTE: with no --org-name the block is omitted entirely. That is the")
        print("        fail-safe: absent markup is safe, wrong markup is not.")
    print("\n  Google recommends Organization on the home page or a single about page,")
    print("  not site-wide. This clone puts it in base.html because that is where the")
    print("  themes put it; narrowing it is a theme fix at source.")

    print("\nSTILL LEAKS QBS, and this script does NOT fix it:")
    for rel in ("templates/partials/header.html", "templates/partials/footer.html"):
        print(f"  {rel} - QBS logo, nav, social links, copyright line.")
    print("  These are global_partials (portal-scoped singletons). Handle them per")
    print("  process/reskin.md before anything goes in front of a client.")

    if not (a.apply and a.approved_by):
        print(f"\n{'-' * 78}")
        print("DRY RUN - nothing was written.")
        print('To execute, re-run with:  --apply --approved-by "<your name>"')
        print(f"{'-' * 78}\n")
        return 0

    if problems and not a.force:
        raise SystemExit("\nREFUSING to apply: contrast gate failed (above). "
                         "Fix with --set, or pass --force if you have a specific reason.")

    print(f"\n{'-' * 78}")
    print(f"APPLYING - approved by {a.approved_by}")
    if problems and a.force:
        print(f"CONTRAST GATE OVERRIDDEN. Reason given: {a.force_reason}")
    print(f"{'-' * 78}\n")

    written = 0
    for f in files:
        rel = f[len(src) + 1:]
        content = read_source(f, token)
        if rel == "css/quantum.css" and new_native:
            content = patch_native(content, new_native)
        elif rel == "fields.json":
            content = patch_fields_json(content, {MODE_FIELD: ground})
        elif rel == "templates/layouts/base.html":
            for i, b in enumerate(old_orgs):
                # first one becomes the client's; any duplicates are removed
                content = content.replace(b, new_org if i == 0 else "", 1)
        put_file(f"{target}/{rel}", token, content)
        written += 1
        if written % 40 == 0:
            print(f"  ... {written}/{len(files)}")
    print(f"\n  wrote {written} files to draft: {target}")
    print("  Next: publish in Design Manager, then gate it:")
    print(f'    node scripts/verify.mjs <staging-url> --env staging '
          f'--expect-org "{a.org_name or client}"')
    return 0


def patch_fields_json(raw: str, new_six: dict) -> str:
    fields = json.loads(raw)
    for group in fields:
        for child in group.get("children") or []:
            key = f"{group.get('name')}.{child.get('name')}"
            if key not in new_six:
                continue
            val = new_six[key]
            if isinstance(child.get("default"), dict):
                child["default"] = dict(child["default"], color=val)
            else:
                child["default"] = val
    return json.dumps(fields, indent=2, ensure_ascii=False)


def cmd_audit(a, token):
    """Sweep all nine themes for the known defects. Read-only."""
    verify_portal(token, getattr(a, "portal", None))
    rows = []
    for t in NINE:
        try:
            css = read_source(f"{t}/css/quantum.css", token)
            base = read_source(f"{t}/templates/layouts/base.html", token)
            nat = parse_native(css)
            mode = current_mode(read_fields(t, token))
            mods = [c for c in children(f"{t}/modules", token) if c.endswith(".module")]
            tpl = [c for c in children(f"{t}/templates", token) if c.endswith(".html")]
            names = re.findall(r'"name"\s*:\s*"([^"]+)"', base)
            who = "QBS" if any("Quantum Business Solutions" in n for n in names) else (
                  names[0][:14] if names else "none")
            cta, acc = nat.get("--cta-fg", ""), nat.get("--q-gold", "")
            cr = (f"{contrast_ratio(acc, cta):.1f}" if cta.startswith("#") and acc.startswith("#")
                  else "?")
            rows.append([t.replace("Quantum ", ""), mode,
                         "light" if t in LIGHT_THEMES else "dark",
                         nat.get("--bg", "?"), acc or "?", cr,
                         len(mods), len(tpl), who,
                         "yes" if "@import" in css else "no",
                         "yes" if "preconnect" in base else "no"])
        except HubSpotError as e:
            rows.append([t.replace("Quantum ", ""), "ERR", "", str(e)[:16],
                         "", "", "", "", "", "", ""])
    print("\nNine-theme defect sweep\n")
    table(rows, ["theme", "mode", "ground", "--bg", "accent", "cta:acc",
                 "mods", "tpls", "schema", "@import", "precon"])
    print("""
Reading this:
  mode      fields.json default. All nine say 'dark' -- but see --bg: the native-direction
            block in quantum.css overrides both modes, so the light themes DO render light.
            `mode` only drives the .only-dark/.only-light logo visibility rules.
  --bg      what the theme actually renders. This is the real ground.
  cta:acc   contrast of --cta-fg on --q-gold. Below 4.5 fails WCAG AA for normal text.
  schema    'QBS' = a client site cloned from this theme declares itself to be Quantum
            Business Solutions. Void's block is richer and also leaks a founder name
            and email address.
  @import   fonts loaded through a CSS @import -- one extra serial hop, and invisible to
            the preload scanner.
""")
    return 0


# ---------------------------------------------------------------------- export/drift

SOURCE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "themes", "source")


def _fetch_one(args):
    path, token = args
    try:
        return path, read_source(path, token), None
    except HubSpotError as e:
        return path, None, str(e)[:120]


def export_theme(theme: str, token: str, out_root: str = SOURCE_DIR):
    """Write every file of a theme to disk so it can be diffed and reviewed.

    The nine exist only in the portal: no diff, no review, no rollback, and no way
    to notice that someone edited one in Design Manager -- which is the repo's
    loudest 'never', one accidental save from changing every client's site."""
    files = sorted(walk(theme, token))
    dest_root = os.path.join(out_root, theme)
    written, failed = 0, []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for path, body, err in pool.map(_fetch_one, [(f, token) for f in files]):
            if err:
                failed.append((path, err))
                continue
            rel = path[len(theme) + 1:]
            dest = os.path.join(dest_root, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(body)
            written += 1
    return written, len(files), failed


def cmd_export(a, token):
    verify_portal(token, a.portal)
    targets = NINE if a.all else [a.theme]
    if not targets or targets == [None]:
        raise SystemExit("Pass --theme <name> or --all.")
    total = 0
    for t in targets:
        w, n, failed = export_theme(t, token)
        total += w
        flag = f"  ({len(failed)} failed)" if failed else ""
        print(f"  {t:22} {w}/{n} files{flag}")
        for path, err in failed[:3]:
            print(f"      ! {path}: {err}")
    print(f"\nwrote {total} files to themes/source/")
    print("Commit it. From here on, `reskin.py drift` tells you if the portal moved.")
    return 0


def cmd_drift(a, token):
    """Diff the live portal against what's committed. Read-only."""
    verify_portal(token, a.portal)
    targets = NINE if a.all else [a.theme]
    if not targets or targets == [None]:
        raise SystemExit("Pass --theme <name> or --all.")
    if not os.path.isdir(SOURCE_DIR):
        raise SystemExit(f"{SOURCE_DIR} does not exist. Run `reskin.py export --all` first.")

    any_drift = False
    for t in targets:
        base = os.path.join(SOURCE_DIR, t)
        if not os.path.isdir(base):
            print(f"  {t:22} NOT EXPORTED - run export first")
            any_drift = True
            continue
        committed = {}
        for root, _dirs, names in os.walk(base):
            for n in names:
                fp = os.path.join(root, n)
                committed[os.path.relpath(fp, base).replace(os.sep, "/")] = fp

        live_paths = sorted(walk(t, token))
        live_rel = {p[len(t) + 1:] for p in live_paths}
        changed, added, removed = [], sorted(live_rel - set(committed)), sorted(set(committed) - live_rel)

        with ThreadPoolExecutor(max_workers=8) as pool:
            for path, body, err in pool.map(_fetch_one, [(p, token) for p in live_paths]):
                rel = path[len(t) + 1:]
                if err or rel not in committed:
                    continue
                with open(committed[rel], encoding="utf-8") as fh:
                    if fh.read() != body:
                        changed.append(rel)

        if changed or added or removed:
            any_drift = True
            print(f"\n  {t}  DRIFT")
            for rel in changed[:12]:
                print(f"      modified  {rel}")
            for rel in added[:6]:
                print(f"      added     {rel}")
            for rel in removed[:6]:
                print(f"      removed   {rel}")
            extra = len(changed) + len(added) + len(removed) - min(len(changed), 12) \
                - min(len(added), 6) - min(len(removed), 6)
            if extra > 0:
                print(f"      ... and {extra} more")
        else:
            print(f"  {t:22} clean")

    if any_drift:
        print("\nThe portal and the repo disagree. Either someone edited a theme in Design")
        print("Manager -- which changes every client on it -- or a source fix was applied and")
        print("never exported. Reconcile before any client build.")
        return 1
    print("\nNo drift. The product line matches the repo.")
    return 0


# ------------------------------------------------------------------------------ cli

class KV(argparse.Action):
    def __call__(self, parser, ns, values, option_string=None):
        d = getattr(ns, self.dest) or {}
        for v in values:
            k, _, val = v.partition("=")
            d[k] = val
        setattr(ns, self.dest, d)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--token", default=os.environ.get("QBS_HUBSPOT_TOKEN")
                   or os.environ.get("CLIENT_HUBSPOT_TOKEN"))
    p.add_argument("--portal", help="portal id you intend to act on. Defaults to QBS "
                                    f"({EXPECTED_PORTAL}). Pass a client's id to build in "
                                    "their portal, with their token.")
    sub = p.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("inspect", help="report a theme's current re-skin surface")
    i.add_argument("--theme", required=True)

    au = sub.add_parser("audit", help="sweep all nine themes for known defects")

    ex = sub.add_parser("export", help="write a theme's source to themes/source/ for review")
    ex.add_argument("--theme")
    ex.add_argument("--all", action="store_true", help="all nine")

    dr = sub.add_parser("drift", help="diff the live portal against what's committed")
    dr.add_argument("--theme")
    dr.add_argument("--all", action="store_true", help="all nine")

    pl = sub.add_parser("plan", help="show (and optionally apply) a clone + re-skin")
    pl.add_argument("--theme", required=True, help="source theme, one of the nine")
    pl.add_argument("--client", required=True)
    pl.add_argument("--target", help="clone name (default '<Client> - <Theme>')")
    pl.add_argument("--accent", help="client accent hex; the other colours derive from it")
    pl.add_argument("--ground", choices=["light", "dark"],
                    help="light or dark. Defaults to the theme's true ground.")
    pl.add_argument("--serif", help="heading face, e.g. \"'Fraunces',Georgia,serif\"")
    pl.add_argument("--sans", help="body face")
    pl.add_argument("--force", action="store_true",
                    help="apply despite a failed contrast gate. Requires --force-reason.")
    pl.add_argument("--force-reason", metavar="TEXT",
                    help="why an accessibility gate is being overridden. Recorded in the "
                         "output. Required with --force.")
    pl.add_argument("--neutral-hue", metavar="HEX",
                    help="hue for void/navy/paper. Defaults to the accent (house "
                         "guardrail). Pass a hex for a complementary scheme, which "
                         "is what the QBS originals actually use.")
    pl.add_argument("--set", nargs="+", action=KV, metavar="field=value",
                    help="override a derived value, e.g. --set bg=#ffffff (leading -- optional)")
    pl.add_argument("--org-name")
    pl.add_argument("--org-url")
    pl.add_argument("--org-description")
    pl.add_argument("--org-logo")
    pl.add_argument("--org-sameas", nargs="*", default=[])
    pl.add_argument("--apply", action="store_true",
                    help="execute. Requires --approved-by.")
    pl.add_argument("--approved-by", help="who approved this write")

    a = p.parse_args(argv)
    if not a.token:
        raise SystemExit("No token. Set $QBS_HUBSPOT_TOKEN or pass --token.")
    if getattr(a, "force", False) and not getattr(a, "force_reason", None):
        raise SystemExit('--force requires --force-reason "<why>". Overriding an '
                         "accessibility gate is never unattributed.")
    if getattr(a, "apply", False) and not a.approved_by:
        raise SystemExit("--apply requires --approved-by \"<name>\". "
                         "Writes to a live portal are never unattributed.")
    handlers = {"inspect": cmd_inspect, "plan": cmd_plan, "audit": cmd_audit,
                "export": cmd_export, "drift": cmd_drift}
    return handlers[a.cmd](a, a.token) or 0


if __name__ == "__main__":
    try:
        main()
    except HubSpotError as e:
        raise SystemExit(f"HubSpot API error:\n{e}")
