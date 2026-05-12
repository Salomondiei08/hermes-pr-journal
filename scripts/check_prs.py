#!/usr/bin/env python3
"""Check PR statuses via GitHub API."""
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

prs = [
    ('pydata', 'xarray', 11328),
    ('pydata', 'xarray', 11326),
    ('jupyter', 'nbconvert', 2283),
    ('jupyter', 'nbconvert', 2282),
    ('jupyter', 'nbconvert', 2280),
    ('jupyter', 'nbconvert', 2279),
]

for owner, repo, num in prs:
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{num}'
    req = request.Request(url, headers={
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github+json',
    })
    try:
        with request.urlopen(req, timeout=15) as resp:
            d = json.loads(resp.read())
            state = d.get('state', '?')
            merged = 'Yes' if d.get('merged_at') else 'No'
            comments = d.get('comments', 0)
            reviews = d.get('review_comments', 0)
            head = d.get('head', {}).get('sha', '?')[:8]
            title = d.get('title', '?')
            print(f'{owner}/{repo}#{num}: state={state} merged={merged} '
                  f'comments={comments} reviews={reviews} sha={head}')
            print(f'  Title: {title}')
    except Exception as e:
        print(f'{owner}/{repo}#{num}: ERROR - {e}')
