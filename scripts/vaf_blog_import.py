#!/usr/bin/env python3
"""Import brands/vanausdall.blog.json into the HubSpot blog of portal 50498425 (CMS Blog Posts API).

    CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_blog_import.py prep      # author + tags (needs no blog)
    CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_blog_import.py import    # create/publish every post (needs the blog)
    CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_blog_import.py retry     # re-run only the posts logged as failed
    CLIENT_HUBSPOT_TOKEN=... python3 scripts/vaf_blog_import.py report    # rewrite brands/vanausdall.blog-import.md

The blog itself ('VAF Blog', slug blog) cannot be created through the public API; create it once in the UI
(Settings > Website > Blog) and this script finds it (env VAF_BLOG_ID overrides). Idempotent: posts whose slug already
exists in the blog are skipped. Every post is staging-noindexed through headHtml; removing that is a launch gate.
"""
import datetime, json, os, re, sys, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = os.environ["CLIENT_HUBSPOT_TOKEN"]
API = "https://api.hubapi.com"
DATA = os.path.join(ROOT, "brands/vanausdall.blog.json")
STATE = os.path.join(ROOT, "brands/vanausdall.blog-import.state.json")     # tag/author ids, created post ids
FAILS = os.path.join(ROOT, "brands/vanausdall.blog-import-failures.jsonl")
REPORT = os.path.join(ROOT, "brands/vanausdall.blog-import.md")
NOINDEX = '<meta name="robots" content="noindex, nofollow">'
POST_TEMPLATE = "Van Ausdall and Farrar - Showcase/templates/vaf-blog-post.html"
AUTHOR = "Van Ausdall & Farrar"
CAT_SLUGS = {"ai-consulting", "business-phone-systems", "business-process-solutions", "cloud-solutions", "cybersecurity",
             "document-conversion", "document-management", "managed-it", "managed-print-services", "news", "physical-security"}


def call(method, path, body=None, retries=6):
    """Transport is curl: this environment's proxy defeats urllib (RemoteDisconnected), see scripts/reskin.py."""
    import subprocess
    for attempt in range(retries):
        cmd = ["curl", "-s", "-X", method, "-H", "@-", "-H", "Content-Type: application/json", "--max-time", "90",
               "-w", "\n__HTTP__%{http_code}", API + path]
        if body is not None:
            cmd[-1:-1] = ["--data-binary", "@-"]
        # header file goes on stdin first, body second would collide, so pass the body from a temp file
        import tempfile
        tmp = None
        if body is not None:
            tmp = tempfile.NamedTemporaryFile(delete=False); tmp.write(json.dumps(body).encode()); tmp.close()
            cmd[cmd.index("--data-binary") + 1] = "@" + tmp.name
        try:
            r = subprocess.run(cmd, input=f"Authorization: Bearer {TOKEN}\n".encode(), capture_output=True, timeout=120)
        except subprocess.TimeoutExpired:
            time.sleep(2 ** attempt); continue
        finally:
            if tmp: os.unlink(tmp.name)
        out, _, code = r.stdout.rpartition(b"\n__HTTP__")
        code = int(code or 0)
        try:
            j = json.loads(out) if out.strip() else {}
        except ValueError:
            j = {"raw": out[:300].decode("utf-8", "replace")}
        if code in (0, 429, 500, 502, 503, 504) and attempt < retries - 1:
            time.sleep(min(30, 2 ** attempt * (3 if code == 429 else 1))); continue
        return code, j
    return 0, {"message": "network failure"}


def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {"tags": {}, "created": {}}


def save_state(st):
    json.dump(st, open(STATE, "w"), indent=1, sort_keys=True)


def listall(path):
    out, after = [], None
    while True:
        s, r = call("GET", path + ("&" if "?" in path else "?") + "limit=100" + (f"&after={after}" if after else ""))
        if s != 200:
            raise SystemExit(f"GET {path} -> {s} {r}")
        out += r.get("results", [])
        after = (r.get("paging") or {}).get("next", {}).get("after")
        if not after:
            return out


def tag_plan(posts):
    """name -> slug. Category tags first (original slugs so /blog/tag/managed-it mirrors the old /blog/managed-it/), then topic tags."""
    plan, by_lower = {}, {}
    for p in posts:
        for c in p["categories"]:
            plan[c["name"]] = c["slug"]; by_lower[c["name"].lower()] = c["name"]
    for p in posts:
        for t in p["tags"]:
            if t.lower() not in by_lower:
                plan[t] = None; by_lower[t.lower()] = t
    return plan, by_lower


def post_tag_names(p, by_lower):
    names = [c["name"] for c in p["categories"]] + [by_lower[t.lower()] for t in p["tags"]]
    seen = []
    for n in names:
        if n not in seen:
            seen.append(n)
    return seen


def cmd_prep():
    posts = json.load(open(DATA, encoding="utf-8"))
    st = load_state()
    if "author" not in st:
        have = [a for a in listall("/cms/v3/blogs/authors") if a.get("fullName") == AUTHOR]
        if have:
            st["author"] = have[0]["id"]
        else:
            s, r = call("POST", "/cms/v3/blogs/authors", {"fullName": AUTHOR, "displayName": AUTHOR, "slug": "van-ausdall-and-farrar", "language": "en"})
            if s not in (200, 201):
                raise SystemExit(f"author create failed {s} {r}")
            st["author"] = r["id"]
        save_state(st)
    print("author", st["author"])
    existing = {t["name"].lower(): t for t in listall("/cms/v3/blogs/tags")}
    plan, _ = tag_plan(posts)
    made = 0
    for name, slug in plan.items():
        if name in st["tags"]:
            continue
        t = existing.get(name.lower())
        if not t:
            body = {"name": name, "language": "en"}
            if slug:
                body["slug"] = slug
            s, t = call("POST", "/cms/v3/blogs/tags", body)
            if s not in (200, 201):
                print("  tag FAIL", name, s, t); continue
            made += 1
            time.sleep(0.15)
        st["tags"][name] = t["id"]
    save_state(st)
    print(f"{len(st['tags'])} of {len(plan)} tags ready ({made} created)")


def find_blog():
    if os.environ.get("VAF_BLOG_ID"):
        return os.environ["VAF_BLOG_ID"], "blog"
    s, r = call("GET", "/blogs/v3/blogs")
    blogs = r.get("objects", []) if s == 200 else []
    if not blogs:
        raise SystemExit("BLOCKED: portal 50498425 has no blog yet. The public API cannot create one: create 'VAF Blog' "
                         "(slug blog) in Settings > Website > Blog, then re-run.")
    pick = next((b for b in blogs if b.get("name") == "VAF Blog" or b.get("slug") == "blog"), blogs[0])
    return str(pick["id"]), pick.get("slug") or "blog"


def payload(p, st, blog_id, blog_slug, by_lower, with_template):
    d = datetime.date.fromisoformat(p["date"])
    pub = datetime.datetime(d.year, d.month, d.day, 16, 0, tzinfo=datetime.timezone.utc)    # noon US Eastern
    body = {"name": p["title"], "slug": f"{blog_slug}/{p['slug']}", "contentGroupId": blog_id, "language": "en",
            "htmlTitle": p["htmlTitle"], "metaDescription": p["metaDescription"], "postSummary": p["teaser"],
            "postBody": p["bodyHtml"], "blogAuthorId": st["author"], "headHtml": NOINDEX,
            "tagIds": [st["tags"][n] for n in post_tag_names(p, by_lower) if n in st["tags"]],
            "publishDate": pub.strftime("%Y-%m-%dT%H:%M:%SZ"), "publishImmediately": False}
    if p["featuredImage"]:
        body.update({"featuredImage": p["featuredImage"], "featuredImageAltText": p["featuredImageAlt"], "useFeaturedImage": True})
    else:
        body["useFeaturedImage"] = False
    if with_template:
        body["templatePath"] = POST_TEMPLATE
    return body, pub


def create(p, st, blog_id, blog_slug, by_lower, with_template=True):
    body, pub = payload(p, st, blog_id, blog_slug, by_lower, with_template)
    future = pub > datetime.datetime.now(datetime.timezone.utc)
    body["state"] = "DRAFT" if future else "PUBLISHED"
    s, r = call("POST", "/cms/v3/blogs/posts", body)
    if s in (200, 201) and future:
        s2, r2 = call("POST", "/cms/v3/blogs/posts/schedule", {"id": r["id"], "publishDate": body["publishDate"]})
        if s2 not in (200, 204):
            return s2, r2
    return s, r


def cmd_import(only_failed=False):
    posts = json.load(open(DATA, encoding="utf-8"))
    st = load_state()
    if "author" not in st or len(st["tags"]) == 0:
        cmd_prep(); st = load_state()
    blog_id, blog_slug = find_blog()
    _, by_lower = tag_plan(posts)
    have = {x["slug"].split("/")[-1] for x in listall(f"/cms/v3/blogs/posts?contentGroupId={blog_id}")}
    todo = [p for p in posts if p["slug"] not in have]
    if only_failed and os.path.exists(FAILS):
        failed = {json.loads(l)["slug"] for l in open(FAILS)}
        todo = [p for p in todo if p["slug"] in failed]
    open(FAILS, "w").close()
    print(f"blog {blog_id} ({blog_slug}): {len(have)} already there, {len(todo)} to create")
    with_template, ok, bad = True, 0, 0
    for i, p in enumerate(todo, 1):
        s, r = create(p, st, blog_id, blog_slug, by_lower, with_template)
        if s not in (200, 201) and with_template and ("templatePath" in json.dumps(r) or "TEMPLATE_PATH_NOT_SETTABLE" in json.dumps(r)):
            with_template = False                          # the API refuses a per-post template: the blog's own setting applies
            print("  per-post templatePath refused, relying on the blog's post template setting")
            s, r = create(p, st, blog_id, blog_slug, by_lower, False)
        if s in (200, 201):
            st["created"][p["slug"]] = {"id": r["id"], "url": r.get("url"), "slug": r.get("slug"), "state": r.get("state")}
            ok += 1
            if r.get("slug", "").split("/")[-1] != p["slug"]:
                print("  slug changed by HubSpot:", p["slug"], "->", r.get("slug"))
        else:
            bad += 1
            open(FAILS, "a").write(json.dumps({"slug": p["slug"], "status": s, "error": r}) + "\n")
            print("  FAIL", p["slug"], s, str(r)[:200])
        if i % 25 == 0:
            save_state(st); print(f"  {i}/{len(todo)}")
        time.sleep(0.4)                                    # ~2.5 req/s, far under the 190 per 10 s private-app limit
    save_state(st)
    print(f"created {ok}, failed {bad}")
    cmd_report()


def cmd_report():
    posts = json.load(open(DATA, encoding="utf-8"))
    st = load_state()
    fails = [json.loads(l) for l in open(FAILS)] if os.path.exists(FAILS) else []
    future = [p["slug"] for p in posts if p["date"] > datetime.date.today().isoformat()]
    lines = ["# VAF blog import report", "", f"Generated {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC. Portal 50498425.", "",
             f"- Posts found on vanausdall.com/blog: {len(posts)} (the live listing; the plan estimated 324)",
             f"- Posts retrieved and normalised: {len(posts)} (0 unretrievable)",
             f"- Posts created in HubSpot: {len(st['created'])}", f"- Failures logged: {len(fails)}",
             f"- Future-dated posts (kept with their original date, so HubSpot schedules them): {len(future)}"]
    if fails:
        lines += ["", "## Failures", ""] + [f"- `{f['slug']}`: {f['status']} {str(f['error'])[:160]}" for f in fails]
    open(REPORT, "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    {"prep": cmd_prep, "import": cmd_import, "retry": lambda: cmd_import(True), "report": cmd_report}[sys.argv[1]]()
