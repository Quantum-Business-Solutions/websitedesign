# Where client work lives

**Not a branch per client.** One shared method repo, and a client repo only when a client build
produces code. Most won't.

---

## Why a branch per client is the wrong tool

A branch is for a divergent version of the same thing that will eventually **converge**. A client
site never converges back into the methodology. Using branches that way breaks in five specific
ways:

1. **Improvements stop reaching clients.** Every fix to the process, the guardrails or the scripts
   lands on `main`. Twenty client branches means twenty stale copies, each needing a merge nobody
   will do. Six months in, the newest client has the best tooling and the oldest has none.
2. **You can only see one client at a time.** Checking out Kelly hides Revolution. Cross-client work
   becomes impossible — and cross-client work is where the value is. `verticals/office-technology.md`
   only exists because six clients' briefs were readable side by side in one working tree.
3. **History becomes unreadable.** Either `main` carries client commits or the branches diverge
   permanently. Neither gives you a usable `git log`.
4. **The scripts have no home.** If `reskin.py` improves on a client branch, which branch is
   canonical? The answer is always `main`, which means client branches can never contribute.
5. **It is the fork mistake, one level up.** `process/reskin.md` forbids forking the nine themes per
   client because nine maintainable themes become forty unmaintainable ones. A branch per client is
   the same error applied to the repo.

## The boundary that actually works

Four layers, each with one job:

| Layer | Holds | Source of truth for |
|---|---|---|
| **`websitedesign`** — `main` only | The method, the guardrails, the patterns, the scripts, **and every client brief** | How we work, and what we know about each client |
| **`<client>` repo** — *only when needed* | Custom theme source, client-specific modules, review previews, upload tooling | The client's build source |
| **HubSpot** | The live site | **The site itself.** Always |
| **BrandCommand / ClientCommand** | Project, plan, pages, assets, hours | The engagement |

The scripts here already assume this shape. They take the client as an **argument**, not as a
checkout:

```bash
python3 scripts/reskin.py plan --client "Kelly Office Solutions" …
python3 scripts/mockup.py --client "Kelly Office Solutions" --brief brands/kelly-office.md …
node scripts/verify.mjs <url> --expect-org "Kelly Office Solutions"
```

**`websitedesign` is a tool that operates on clients, not a template you copy per client.** That
distinction is the whole answer.

## The decision rule: a client gets a repo when Phase 4 happens

Phase 4 of `process/RUNBOOK.md` is *build theme, templates, modules*. If a build produces **code**,
it needs a repo. If it doesn't, a repo would be empty.

| Situation | Repo? |
|---|---|
| **Launch tier** — three-of-nine re-skinned, no custom modules | **No.** HubSpot is the artifact; the brief is the record |
| **Growth** — re-skin plus a handful of existing modules | **No**, usually |
| **Growth/Transform with custom modules** | **Yes** — Revolution needed 29 modules, 7 sections, 10 templates |
| Custom app, calculator, or an interactive preview | **Yes** |

`Quantum-Business-Solutions/revolution` is the existing precedent and it was the right call: a
Next.js preview app, the HubSpot theme as a record, and `gen-tokens.mjs` / `upload.sh` /
`build-site.mjs`. None of that would fit here, and none of it belongs on a branch.

## Briefs stay here, all of them, together

`brands/<slug>.md` lives in `websitedesign` even for clients with their own repo. This is the one
place a per-client split would do real damage:

- Reading across briefs is how the **vertical layer** got built. Six dealer briefs in one tree
  produced a measured category palette, a keyword profile and a module kit. Split across six repos,
  that never happens.
- Briefs are **tiny text files.** There is no storage argument.
- They are the **institutional memory** — the Revolution "Ink" conflict was caught weeks later only
  because a constraint was written down somewhere findable.

> ⚠️ **They also contain client-confidential material** — pricing, stated constraints, contacts,
> traffic numbers. `websitedesign` must stay **private**, and if it is ever shared or opened up, the
> `brands/` directory moves first. No credentials in briefs, ever — reference where a token lives,
> never its value.

## The drift risk, named

Revolution's repo carries tooling that does not exist here: `gen-tokens.mjs`, `gen-chrome.mjs`,
`upload.sh`, `build-site.mjs`, `tools/reg.mjs`. **The tooling has already forked once.** That is the
real cost of client repos, and the mitigation is a rule:

**Tooling that would help a second client belongs in `websitedesign`, not in a client repo.**

By that rule, at least three of Revolution's five scripts should be here:

- `upload.sh` — syncing a theme folder to a portal with HubL validation is universal
- `build-site.mjs` — building pages from a content definition is universal
- `gen-tokens.mjs` — generating tokens from one source is the principle `designsystem.py` already
  follows

Only `gen-chrome.mjs` (defaults from Revolution's own nav) and the Next.js resolve hook are
genuinely client-specific.

## Naming

| Thing | Convention |
|---|---|
| Client repo | `Quantum-Business-Solutions/<client-slug>` — lowercase, hyphenated |
| Brief | `brands/<client-slug>.md`, same slug |
| Theme clone in HubSpot | `<Company> — <ThemeName>` |
| BrandCommand project | `<Company> — <ThemeName>`, per direction |
| Semrush project | the client's name |

One slug per client, used everywhere. Chasing a client across four systems with three spellings is
a real cost at ten clients.

## Branches inside a client repo

Normal software branching — `main` is what's deployed, feature branches for work in progress. That
is branches used for what branches are for. The rule is only about **never using a branch to mean a
client.**

## What this means at ten clients

- One `websitedesign`, one `main`, ten briefs in one directory, one set of scripts everyone benefits
  from.
- Two or three client repos, for the builds that genuinely produced code.
- Ten live sites in HubSpot, ten projects in ClientCommand.
- A vertical layer that gets better every time a brief is added — which is the compounding property
  none of the alternatives have.
