#!/usr/bin/env bash
set -euo pipefail

echo "=== deploy_local.sh ==="
cd "$(dirname "$0")/.."

echo "Running local build..."
python3 scripts/build_site.py

echo "deploy_local.sh: done"