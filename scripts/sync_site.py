#!/usr/bin/env python3
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
subprocess.run(['python3', str(ROOT / 'scripts' / 'sync_statuses.py')], check=True)
subprocess.run(['python3', str(ROOT / 'scripts' / 'build_site.py')], check=True)
