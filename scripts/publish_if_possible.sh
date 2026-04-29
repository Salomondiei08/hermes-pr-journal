#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

"$ROOT/scripts/bootstrap_public_repo.py" >/tmp/hermes-pr-blog-bootstrap.txt 2>&1 || true

git add -A
if ! git diff --cached --quiet; then
  git commit -m "chore: update PR journal"
fi

load_token() {
  if [ -n "${GITHUB_TOKEN:-}" ]; then
    printf '%s' "$GITHUB_TOKEN"
    return 0
  fi
  if [ -f /home/user/.hermes/.env ]; then
    python3 - <<'PY'
from pathlib import Path
for line in Path('/home/user/.hermes/.env').read_text(errors='ignore').splitlines():
    if line.startswith('GITHUB_TOKEN='):
        print(line.split('=',1)[1].strip())
        break
PY
    return 0
  fi
  return 1
}

if git remote get-url origin >/dev/null 2>&1; then
  TOKEN="$(load_token || true)"
  REMOTE="$(git remote get-url origin)"
  if [ -n "$TOKEN" ] && [[ "$REMOTE" == https://github.com/* ]]; then
    PUSH_URL="https://jaythehardcoder:${TOKEN}@${REMOTE#https://}"
    if git push -u "$PUSH_URL" HEAD >/tmp/hermes-pr-blog-push.txt 2>&1; then
      git branch --set-upstream-to=origin/main main >/dev/null 2>&1 || true
      echo "pushed"
      exit 0
    fi
  fi
  if git push -u origin HEAD >/tmp/hermes-pr-blog-push.txt 2>&1; then
    echo "pushed"
    exit 0
  fi
fi

echo "push-skipped-no-auth-or-remote"
