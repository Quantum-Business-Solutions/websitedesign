# Website assets without Shawn: who does what, and where

A "website asset" is one of two things the conveyor produces for a client or prospect:

- **Three directions**: the preview hub with three complete websites, the design system and the search package, deployed to a Vercel project (kelly-office-solutions.vercel.app).
- **Analysis**: the search and AI-answer report alone, every page scored, with the Excel workbook, served from the `qbs-analyses` Vercel project (analyses/<slug>/).

Either one is attached to the client's portal in Client Command so the client and the team find it there. This page says which teammate can do each step today, with what, and what Client Command still has to add so the whole path is a button.

## Today: three steps, three tools, no terminal required for two of them

| Step | Who | Where | How |
|---|---|---|---|
| 1. Intake and first build | Any teammate with Claude Code and access to this repo | Claude Code on `websitedesign` | Say "new client <name>, <domain>, <cities>" and follow INTAKE.md. `scripts/newclient.py` scaffolds the content, search and build files; the fifteen-minute path in RUNBOOK.md does the rest. Locations come from the client's own site and the client, never from a guess. |
| 2. Rebuild or re-render | Any teammate with access to this repo | GitHub, Actions tab, "Client site" | Run workflow, type the slug, choose build or analysis. The client repo is pushed and Vercel deploys, or `analyses/<slug>/` is committed and `qbs-analyses` serves it. Needs the `CLIENT_REPOS_TOKEN` secret set once by an admin. |
| 3. Attach to the portal | Any teammate with a read_write Client Command token, or anyone in the app | Client Command | In the app: the portal's Files, add a link. By agent: `attach_portal_file` with `portal_id`, `link_url`, `name`. Kelly's hub and report are attached this way (9 September 2026). |

One-time admin work per client: create the Vercel project from the client repo (Vercel dashboard, Import). The `qbs-analyses` project is one import for every prospect analysis, root directory `analyses`.

## Tomorrow: what Client Command adds so step 3 is native and step 1 is a form

Client Command already has the pieces for a site to live inside it rather than on Vercel: `publish_site`, `publish_site_pages`, `put_site_asset`, `list_sites`, `get_site`, the `sites` and `site_pages` tables and the `sites` storage bucket. Any teammate with a read_write token can call them; nothing is admin-only. What stops them being the path is transport: a built site is tens of megabytes and the tools take file contents inline, which no agent should type. Four additions close the gap, for the Client Command session:

1. **`import_site_from_url`**: slug, title, portal_id, visibility, and a source, either a deployed address (https://kelly-office-solutions.vercel.app) or a GitHub repository. The function fetches the files server-side, walks the HTML for same-origin links and assets, writes text files to `site_pages` and binaries to the `sites` bucket, and returns `link_url`. One call per site. Re-running replaces.
2. **A Websites tab on the portal**, reading `sites` where `portal_id` matches (the `client_portal_sites` table exists for this): title, visibility, link, last updated, open and share buttons. Client-visible when visibility is link or public.
3. **"New website asset" on the portal**: a form with the intake fields from INTAKE.md (client, domain, headquarters and locations, services, people, colours, photographs). Submitting it creates an agent task that runs the conveyor. Until the conveyor runs inside Client Command, the task triggers this repo's "Client site" workflow through GitHub's API (the `github` internal service is registered but has no token yet) and the task closes with the link attached.
4. **Permission**: read_write scope, not admin, for all of the above. The audit log already records who did what.

When 1 and 2 land, step 3 above becomes `import_site_from_url` once, and the Vercel project becomes optional. When 3 lands, step 1 no longer needs Claude Code for the intake; it still needs the conveyor's judgement for the content and the findings, which is why the agent task runs the same scripts and process this repo holds.

## Where each thing is written down

- INTAKE.md: what to collect, the search baseline, one command per client, analysis before a build.
- RUNBOOK.md: the eight phases, the fifteen-minute path, robustness rules.
- repos.md: repositories, Vercel projects, knowledge base ids, the file table.
- qa-findings.md: everything that went wrong once and the rule that came out of it.
- `.github/workflows/client.yml`: the rebuild and re-render workflow.
