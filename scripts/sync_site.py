#!/usr/bin/env python3
"""Rebuild the static site from data/site.json.

Future PRs can be appended to data/site.json and this script will regenerate the site.
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
subprocess.run(['python3', str(ROOT / 'scripts' / 'build_site.py')], check=True)
