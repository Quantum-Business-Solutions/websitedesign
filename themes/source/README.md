# The nine themes, in source control

This is a **read-only mirror** of the nine Quantum themes as published in HubSpot portal
**20682069**, exported by `python3 scripts/reskin.py export --all`. 2,835 files.

**It exists so the portal cannot drift silently.** `python3 scripts/reskin.py drift` diffs the
live portal against this directory and exits 1 if they differ.

## Rules

- **Do not edit here to change a theme.** Nothing pushes from this directory to the portal. Theme
  fixes go through the propose-then-confirm process in `themes/architecture.md`, get made in the
  portal, then `reskin.py export` records them here in the same commit.
- **A drift is either committed or reverted the same week** (`process/SCHEDULE.md`, weekly numbers).
  A live edit nobody recorded is the failure this directory prevents.
- **Client themes are not mirrored here.** They live in the client's portal, and in a client repo
  only when Phase 4 produced code (`process/repos.md`).

## Refresh

```bash
python3 scripts/reskin.py export --all      # all nine, 8 threads, ~2 minutes
python3 scripts/reskin.py export --theme "Quantum Press"
python3 scripts/reskin.py drift             # exit 0 clean, 1 drifted
```

Requires `$QBS_HUBSPOT_TOKEN`. The script refuses any other portal.
