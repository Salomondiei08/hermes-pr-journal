#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

git add -A
if ! git diff --cached --quiet; then
  git commit -m "chore: update PR journal"
fi

if git remote get-url origin >/dev/null 2>&1; then
  if git push origin HEAD >/dev/null 2>&1; then
    echo "pushed"
    exit 0
  fi
fi

echo "push-skipped-no-auth-or-remote"
