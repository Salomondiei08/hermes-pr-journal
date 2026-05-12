#!/usr/bin/env python3
"""Get review comments for a specific PR."""
import json
import os
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

# Get review comments
url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{num}/comments'
req = request.Request(url, headers={
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github+json',
})
try:
    with request.urlopen(req, timeout=15) as resp:
        comments = json.loads(resp.read())
        for c in comments:
            print(f"--- Comment on {c.get('path', '?')}:{c.get('line', '?')} ---")
            print(f"User: {c.get('user', {}).get('login', '?')}")
            print(f"Body: {c.get('body', '')}")
            print()
except Exception as e:
    print(f'Error: {e}')

# Get timeline events
url2 = f'https://api.github.com/repos/{owner}/{repo}/issues/{num}/timeline?per_page=20'
req2 = request.Request(url2, headers={
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github+json',
})
try:
    with request.urlopen(req2, timeout=15) as resp:
        events = json.loads(resp.read())
        for e in events:
            etype = e.get('event', '?')
            if etype in ('review_requested', 'ready_for_review', 'labeled', 'assigned'):
                print(f"Event: {etype} at {e.get('created_at', '?')}")
except Exception as e:
    print(f'Error: {e}')
