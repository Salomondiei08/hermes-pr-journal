# Jay PR Journal

Public website for Jay's real open-source pull requests and engineering notes.

Live target:
- https://jay.reinvent-labs.com

What this repo contains:
- `data/site.json` — structured source of truth for PR writeups
- `data/tracked_prs.json` — PRs whose status should be refreshed from GitHub
- `scripts/build_site.py` — renders the static site into `dist/`
- `scripts/sync_statuses.py` — updates PR status fields from the GitHub API
- `scripts/sync_site.py` — refreshes statuses and rebuilds the site
- `scripts/add_post_from_git.py` — creates or updates a journal entry from a local git repo/commit
- `scripts/deploy_local.sh` — publishes `dist/` to the local web root served by Caddy
- `scripts/publish_if_possible.sh` — commits and pushes this repo when GitHub credentials are available
