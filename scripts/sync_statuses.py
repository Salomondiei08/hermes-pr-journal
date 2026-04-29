#!/usr/bin/env python3
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKED = ROOT / 'data' / 'tracked_prs.json'
SITE = ROOT / 'data' / 'site.json'


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'Hermes PR Journal'})
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
            if data.get('merged_at'):
                posts[slug]['status'] = 'merged'
            else:
                posts[slug]['status'] = data.get('state', 'unknown')
    site['posts'] = sorted(posts.values(), key=lambda p: p['date'], reverse=True)
    SITE.write_text(json.dumps(site, indent=2) + '\n')
    print(f"synced {len(tracked)} tracked PR status(es)")


if __name__ == '__main__':
    main()
