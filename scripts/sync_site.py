#!/usr/bin/env python3
"""Skeleton sync script."""
import json, sys, os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)

tracked = DATA / "tracked_prs.json"
if tracked.exists():
    prs = json.loads(tracked.read_text())
else:
    prs = []
    tracked.write_text(json.dumps(prs, indent=2))

print(f"Sync complete. {len(prs)} PRs tracked.")
sys.exit(0 if len(prs) > 0 else 1)