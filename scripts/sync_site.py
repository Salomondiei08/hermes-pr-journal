#!/usr/bin/env python3
"""Refresh PR statuses from GitHub, then copy them into the site data."""
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TRACKED = BASE / "data" / "tracked_prs.json"
SITE = BASE / "docs" / "_data" / "prs.json"


def main():
    # Statuses (open / merged / closed, reviews) come from the GitHub API.
    status = subprocess.run([sys.executable, str(BASE / "scripts" / "sync_statuses.py")], capture_output=True, text=True)
    if status.returncode != 0:
        print(f"sync: status refresh FAILED: {(status.stderr or status.stdout).strip()[-300:]}")
        sys.exit(1)
    if not TRACKED.exists():
        print("sync: FAILED, tracked_prs.json not found")
        sys.exit(1)
    prs = json.loads(TRACKED.read_text())
    SITE.parent.mkdir(parents=True, exist_ok=True)
    SITE.write_text(json.dumps(prs, indent=2))
    count = len(prs.get("tracked_prs", prs)) if isinstance(prs, dict) else len(prs)
    print(f"sync: OK, {count} PRs refreshed from GitHub")


if __name__ == "__main__":
    main()
