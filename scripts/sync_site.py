#!/usr/bin/env python3
"""Fetch latest PR data and sync the blog site content."""
import json, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TRACKED = BASE / "data" / "tracked_prs.json"
SITE = BASE / "docs" / "_data" / "prs.json"

def main():
    if not TRACKED.exists():
        print("ERROR: tracked_prs.json not found")
        sys.exit(1)
    with open(TRACKED) as f:
        prs = json.load(f)
    SITE.parent.mkdir(parents=True, exist_ok=True)
    with open(SITE, "w") as f:
        json.dump(prs, f, indent=2)
    print(f"sync: OK — copied {len(prs)} PR records to site data")

if __name__ == "__main__":
    main()