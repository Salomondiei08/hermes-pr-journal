#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_NAME = os.environ.get('HERMES_PR_BLOG_REPO', 'hermes-pr-journal')
OWNER = os.environ.get('HERMES_PR_BLOG_OWNER', 'jaythehardcoder')
DESCRIPTION = 'Autonomous blog of real open-source pull requests and code changes shipped by Hermes.'


def load_token():
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        return token.strip()
    env_file = Path.home() / '.hermes' / '.env'
    if env_file.exists():
        for line in env_file.read_text(errors='ignore').splitlines():
            if line.startswith('GITHUB_TOKEN='):
                return line.split('=', 1)[1].strip()
    return None


def request(method, url, payload, token):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Authorization', f'token {token}')
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('User-Agent', 'Hermes PR Journal')
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def main():
    try:
        subprocess.check_call(['git', 'remote', 'get-url', 'origin'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print('origin-exists')
        return
    except subprocess.CalledProcessError:
        pass

    token = load_token()
    if not token:
        print('no-github-token')
        return

    payload = {
        'name': REPO_NAME,
        'description': DESCRIPTION,
        'private': False,
        'has_issues': True,
        'auto_init': False,
        'homepage': 'https://jay.reinvent-labs.com'
    }
    try:
        request('POST', 'https://api.github.com/user/repos', payload, token)
    except Exception as e:
        if 'name already exists on this account' not in str(e):
            print(f'repo-create-failed: {e}')
            return

    remote = f'https://github.com/{OWNER}/{REPO_NAME}.git'
    subprocess.check_call(['git', 'remote', 'add', 'origin', remote], cwd=ROOT)
    print(remote)


if __name__ == '__main__':
    main()
