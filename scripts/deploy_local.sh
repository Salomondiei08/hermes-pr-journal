#!/usr/bin/env bash
# Build the site and publish dist/ to the web root Caddy serves for
# jay.reinvent-labs.com. No sudo: the web root must belong to user:caddy
# (restored 2026-10-14; the Aug 30 rewrite had dropped the publish step,
# which froze the live site on Aug 20). podcasts/ lives only on the server.
set -euo pipefail
cd "$(dirname "$0")/.."
DEST="/srv/www/jay.reinvent-labs.com"

python3 scripts/build_site.py

if [ ! -w "$DEST" ]; then
  echo "deploy: FAILED, $DEST is not writable (run: sudo chown -R user:caddy $DEST)" >&2
  exit 1
fi
rsync -a --exclude podcasts/ dist/ "$DEST/"
echo "deploy: OK, published to $DEST"
