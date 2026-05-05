#!/usr/bin/env python3
import json
import os
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKED = ROOT / "data" / "tracked_prs.json"
SITE = ROOT / "data" / "site.json"
HERMES_ENV = Path('/home/user/.hermes/.env')


def load_github_token():
    token = os.environ.get('GITHUB_TOKEN', '').strip()
    if token:
        return token
    if HERMES_ENV.exists():
        for line in HERMES_ENV.read_text(errors='ignore').splitlines():
            if line.startswith('GITHUB_TOKEN='):
                return line.split('=', 1)[1].strip().strip('"').strip("'")
    return None


def fetch_json(url: str):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Hermes PR Journal'}
    token = load_github_token()
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def main():
    tracked = json.loads(TRACKED.read_text())['tracked_prs']
    site = json.loads(SITE.read_text())
    posts = {post['slug']: post for post in site['posts']}

    for item in tracked:
        slug = item['slug']
        url = f"https://api.github.com/repos/{item['owner']}/{item['repo']}/pulls/{item['pr_number']}"
        data = fetch_json(url)
        if slug in posts:
            posts[slug]['status'] = 'merged' if data.get('merged_at') else data.get('state', 'unknown')
    site['posts'] = sorted(posts.values(), key=lambda p: (p.get('date', ''), p.get('last_updated', '')), reverse=True)
    SITE.write_text(json.dumps(site, indent=2) + "\n")
    print(f"synced {len(tracked)} tracked PR status(es)")


if __name__ == '__main__':
    main()
