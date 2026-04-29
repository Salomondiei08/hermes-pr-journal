#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="/srv/www/jay.reinvent-labs.com"
sudo mkdir -p "$DEST"
sudo rsync -a --delete "$ROOT/dist/" "$DEST/"
sudo chown -R caddy:caddy "$DEST"
echo "deployed to $DEST"
