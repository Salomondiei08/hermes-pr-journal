#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
ROOT = Path('/home/user/.hermes/hermes-agent/work/hermes-pr-blog')

try:
    subprocess.run(['python3', str(ROOT / 'scripts' / 'sync_statuses.py')], check=True, cwd=str(ROOT))
    print("sync_statuses OK")
except subprocess.CalledProcessError as e:
    print(f"sync_statuses FAILED (exit {e.returncode})")
    sys.exit(1)

try:
    subprocess.run(['python3', str(ROOT / 'scripts' / 'build_site.py')], check=True, cwd=str(ROOT))
    print("build_site OK")
except subprocess.CalledProcessError as e:
    print(f"build_site FAILED (exit {e.returncode})")
    sys.exit(1)
