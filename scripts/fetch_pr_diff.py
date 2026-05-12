#!/usr/bin/env python3
"""Fetch PR diff and review comments for xarray #11328."""
import json, os
from urllib import request

token = ''
env_file = os.path.expanduser('~/.hermes/.env')
if os.path.isfile(env_file):
    with open(env_file) as f:
        for line in f:
            if line.startswith('GITHUB_TOKEN='):
                token = line.split('=', 1)[1].strip()
                break

owner, repo, num = 'pydata', 'xarray', 11328

# Get diff as text
url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{num}'
req = request.Request(url, headers={
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3.diff',
})
with request.urlopen(req, timeout=15) as resp:
    diff = resp.read().decode()
    print("=== DIFF ===")
    print(diff)
    print()

# Get review comments
url2 = f'https://api.github.com/repos/{owner}/{repo}/pulls/{num}/comments'
req2 = request.Request(url2, headers={
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
})
with request.urlopen(req2, timeout=15) as resp:
    comments = json.loads(resp.read())
    print("=== REVIEW COMMENTS ===")
    for c in comments:
        print(f"File: {c.get('path')}, Line: {c.get('line')}")
        print(f"User: {c.get('user', {}).get('login')}")
        print(f"Body: {c.get('body')}")
        print()
