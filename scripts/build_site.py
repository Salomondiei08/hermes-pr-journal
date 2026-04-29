#!/usr/bin/env python3
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'site.json'
DIST = ROOT / 'dist'
POSTS_DIR = DIST / 'posts'
FONT = 'https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500&display=swap'


def esc(value):
    return html.escape(str(value or ''), quote=True)


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def slugify(value):
    return str(value or 'unknown').lower().replace(' ', '-').replace('/', '-')


def status_label(value):
    return str(value or 'unknown').upper()


def status_class(value):
    value = str(value or 'unknown').lower()
    return value if value in {'open', 'merged', 'closed', 'draft'} else 'neutral'


def absolute(site, path):
    base = site.get('base_url', '').rstrip('/')
    if not path.startswith('/'):
        path = '/' + path
    return f'{base}{path}'


def page(title, description, body, prefix='.'):
    return (
        '<!doctype html><html lang="en"><head>'
        '<meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />'
        f'<title>{esc(title)}</title>'
        f'<meta name="description" content="{esc(description)}" />'
        f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="{FONT}" rel="stylesheet">'
        f'<link rel="alternate" type="application/rss+xml" title="Jay RSS" href="{prefix}/rss.xml" />'
        f'<link rel="stylesheet" href="{prefix}/styles.css" />'
        '</head><body>'
        f'<div class="shell">{body}</div>'
        f'<script src="{prefix}/app.js" defer></script>'
        '</body></html>'
    )


def nav(site, current, prefix='.'):
    def link(label, href, key):
        klass = 'nav-link active' if current == key else 'nav-link'
        return f'<a class="{klass}" href="{href}">{esc(label)}</a>'
    return (
        '<header class="site-header">'
        f'<a class="brand" href="{prefix}/index.html">Jay</a>'
        '<nav class="main-nav">'
        + link('Home', f'{prefix}/index.html', 'home')
        + link('About', f'{prefix}/about.html', 'about')
        + link('Journal', f'{prefix}/journal.html', 'journal')
        + f'<a class="nav-link" href="{esc(site["github"])}">GitHub</a>'
        + f'<a class="nav-link" href="{prefix}/rss.xml">RSS</a>'
        + '</nav>'
        + '<button class="theme-toggle" type="button" data-theme-toggle aria-label="Toggle theme">Theme</button>'
        + '</header>'
    )


def footer(site, prefix='.'):
    return (
        '<footer class="site-footer">'
        f'<div>{esc(site["tagline"])}</div>'
        '<div class="footer-links">'
        f'<a href="{esc(site["company_url"])}">Reinvent Labs</a>'
        f'<a href="{esc(site["github"])}">GitHub</a>'
        f'<a href="{prefix}/rss.xml">RSS</a>'
        '</div></footer>'
    )


def chips(post, include_repo=True):
    items = [f'<span class="chip status {status_class(post.get("status"))}">{esc(status_label(post.get("status")))}</span>']
    if include_repo and post.get('repo'):
        items.append(f'<span class="chip mono">{esc(post.get("repo"))}</span>')
    if post.get('pr_number'):
        items.append(f'<span class="chip mono">PR #{esc(post.get("pr_number"))}</span>')
    return ''.join(items)


def stats(posts):
    return {
        'total': len(posts),
        'open': sum(1 for p in posts if str(p.get('status')).lower() == 'open'),
        'merged': sum(1 for p in posts if str(p.get('status')).lower() == 'merged'),
        'closed': sum(1 for p in posts if str(p.get('status')).lower() == 'closed'),
    }


def stats_html(posts):
    s = stats(posts)
    items = [('Tracked PRs', s['total']), ('Open', s['open']), ('Merged', s['merged']), ('Closed', s['closed'])]
    return ''.join(f'<div class="stat"><span>{esc(label)}</span><strong>{esc(value)}</strong></div>' for label, value in items)


def post_card(post, prefix='.'):
    return (
        f'<article class="post-card" data-status="{esc(slugify(str(post.get("status", "unknown")).lower()))}" data-repo="{esc(slugify(post.get("repo")))}">'
        f'<a class="post-link" href="{prefix}/posts/{esc(post["slug"])}.html">'
        f'<div class="post-meta">{esc(post.get("repo", ""))} · {esc(post.get("date", ""))}</div>'
        f'<h3>{esc(post["title"])}</h3>'
        f'<p>{esc(post.get("summary", ""))}</p>'
        f'<div class="chip-row">{chips(post)}</div>'
        '</a></article>'
    )


def comment_block(site):
    repo = site.get('comments_repo')
    if not repo:
        return ''
    return (
        '<section class="panel comments"><div class="section-label">Comments</div>'
        f'<script src="https://utteranc.es/client.js" repo="{esc(repo)}" issue-term="pathname" label="comments" theme="preferred-color-scheme" crossorigin="anonymous" async></script>'
        '</section>'
    )


def list_section(title, values):
    values = as_list(values)
    if not values:
        return ''
    items = []
    for item in values:
        if isinstance(item, dict):
            label = item.get('title') or item.get('date') or item.get('label') or title
            summary = item.get('summary') or item.get('text') or item.get('value') or ''
            url = item.get('url')
            line = f'<strong>{esc(label)}</strong>'
            if summary:
                line += f' — {esc(summary)}'
            if url:
                line += f' <a href="{esc(url)}">Open</a>'
            items.append(f'<li>{line}</li>')
        else:
            items.append(f'<li>{esc(item)}</li>')
    items_html = ''.join(items)
    return f'<section class="panel"><div class="section-label">{esc(title)}</div><ul class="detail-list">{items_html}</ul></section>'


def sidebar(post):
    fields = [
        ('Repository', post.get('repo')),
        ('PR', f'#{post["pr_number"]}' if post.get('pr_number') else None),
        ('Status', status_label(post.get('status'))),
        ('Date', post.get('date')),
        ('Branch', post.get('branch')),
        ('Commit', str(post.get('commit', ''))[:12] if post.get('commit') else None),
        ('Diff', post.get('diff_stat')),
    ]
    rows = ''.join(f'<div class="meta-row"><span>{esc(k)}</span><strong>{esc(v)}</strong></div>' for k, v in fields if v)
    links = []
    if post.get('pr_url'):
        links.append(('Pull request', post['pr_url']))
    if post.get('repo'):
        links.append(('Repository', f'https://github.com/{post["repo"]}'))
    if post.get('branch') and post.get('repo'):
        links.append(('Branch', f'https://github.com/{post["repo"]}/tree/{quote(str(post["branch"]))}'))
    if post.get('commit') and post.get('repo'):
        links.append(('Commit', f'https://github.com/{post["repo"]}/commit/{post["commit"]}'))
    for item in as_list(post.get('links')):
        if isinstance(item, dict) and item.get('url'):
            links.append((item.get('label', 'Link'), item['url']))
    actions = ''.join(f'<a class="small-link" href="{esc(url)}">{esc(label)}</a>' for label, url in links)
    return f'<aside class="panel side-panel">{rows}<div class="side-links">{actions}</div></aside>'


def related(posts, current_slug):
    others = [p for p in posts if p.get('slug') != current_slug][:3]
    if not others:
        return ''
    cards = ''.join(post_card(p, '..') for p in others)
    return '<section class="section"><div class="section-head"><h2>More entries</h2></div><div class="post-grid">' + cards + '</div></section>'


def home(site, profile, posts):
    latest = ''.join(post_card(p) for p in posts)
    body = (
        nav(site, 'home')
        + '<main>'
        + '<section class="hero">'
        + '<div class="section-label">Jay</div>'
        + f'<h1>{esc(profile.get("home_heading", site["title"]))}</h1>'
        + f'<p class="lede">{esc(profile.get("short_bio", site["tagline"]))}</p>'
        + '<div class="hero-links">'
        + '<a class="button button-primary" href="./journal.html">Read journal</a>'
        + '<a class="button" href="./about.html">About</a>'
        + f'<a class="button" href="{esc(site["github"])}">GitHub</a>'
        + '</div></section>'
        + f'<section class="stats-grid">{stats_html(posts)}</section>'
        + '<section class="section"><div class="section-head"><h2>Latest work</h2></div>'
        + f'<div class="post-grid">{latest}</div></section>'
        + '</main>'
        + footer(site)
    )
    return page('Jay', site['tagline'], body)


def about(site, profile, posts):
    intro = ''.join(f'<p>{esc(p)}</p>' for p in as_list(profile.get('about_intro')))
    focus = ''.join(f'<li>{esc(item)}</li>' for item in as_list(profile.get('focus')))
    principles = ''.join(f'<li>{esc(item)}</li>' for item in as_list(profile.get('principles')))
    body = (
        nav(site, 'about')
        + '<main>'
        + '<section class="hero hero-page"><div class="section-label">About</div><h1>About Jay</h1>'
        + f'<p class="lede">{esc(profile.get("short_bio", site["tagline"]))}</p></section>'
        + f'<section class="panel prose">{intro}</section>'
        + f'<section class="two-col"><section class="panel"><div class="section-label">Focus</div><ul class="detail-list">{focus}</ul></section><section class="panel"><div class="section-label">Principles</div><ul class="detail-list">{principles}</ul></section></section>'
        + comment_block(site)
        + '</main>'
        + footer(site)
    )
    return page('About Jay', profile.get('short_bio', site['tagline']), body)


def journal(site, posts):
    statuses = sorted({slugify(str(p.get('status', 'unknown')).lower()) for p in posts})
    repos_map = {}
    for p in posts:
        repos_map[slugify(p.get('repo'))] = p.get('repo')
    status_buttons = ['<button class="filter-btn active" data-filter-status="all" type="button">All statuses</button>']
    status_buttons += [f'<button class="filter-btn" data-filter-status="{esc(s)}" type="button">{esc(s.upper())}</button>' for s in statuses]
    repo_buttons = ['<button class="filter-btn active" data-filter-repo="all" type="button">All repos</button>']
    repo_buttons += [f'<button class="filter-btn" data-filter-repo="{esc(k)}" type="button">{esc(v)}</button>' for k, v in sorted(repos_map.items(), key=lambda item: item[1].lower())]
    cards = ''.join(post_card(p) for p in posts)
    body = (
        nav(site, 'journal')
        + '<main>'
        + '<section class="hero hero-page"><div class="section-label">Journal</div><h1>PR Journal</h1><p class="lede">Real pull requests, status changes, tests, reviews, and lessons learned.</p></section>'
        + '<section class="panel filters"><div class="filter-group"><div class="section-label">Status</div><div class="filter-row">' + ''.join(status_buttons) + '</div></div>'
        + '<div class="filter-group"><div class="section-label">Repository</div><div class="filter-row">' + ''.join(repo_buttons) + '</div></div></section>'
        + f'<section class="post-grid" data-filterable-grid>{cards}</section>'
        + '</main>'
        + footer(site)
    )
    return page(site['journal_title'], site['tagline'], body)


def post_page(site, post, posts):
    body = (
        nav(site, 'journal', '..')
        + '<main>'
        + f'<section class="hero hero-page"><div class="section-label">{esc(post.get("repo", ""))}</div><h1>{esc(post["title"])}</h1><p class="lede">{esc(post.get("summary", ""))}</p><div class="chip-row">{chips(post)}<span class="chip mono">{esc(post.get("date", ""))}</span></div></section>'
        + '<section class="post-layout"><div class="post-main">'
        + list_section('Problem', post.get('problem'))
        + list_section('What changed', post.get('changes'))
        + list_section('Tests', post.get('tests'))
        + list_section('Files changed', post.get('files_changed'))
        + list_section('Review + discussion', post.get('discussion_highlights') or post.get('discussion'))
        + list_section('Updates / timeline', post.get('updates') or post.get('timeline'))
        + list_section('Lessons learned', post.get('lessons') or post.get('learning'))
        + list_section('Next steps', post.get('next_steps'))
        + '</div><div class="post-side">' + sidebar(post) + '</div></section>'
        + related(posts, post.get('slug'))
        + comment_block(site)
        + '</main>'
        + footer(site, '..')
    )
    return page(f'{post["title"]} | Jay', post.get('summary', site['tagline']), body, '..')


def rss(site, posts):
    built = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    items = []
    for p in posts:
        url = absolute(site, f'/posts/{p["slug"]}.html')
        items.append('<item>' + f'<title>{esc(p["title"])}</title>' + f'<link>{esc(url)}</link>' + f'<guid>{esc(url)}</guid>' + f'<description>{esc(p.get("summary", ""))}</description>' + f'<pubDate>{esc(p.get("date", ""))}</pubDate>' + '</item>')
    return '<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>' + f'<title>{esc(site["journal_title"])}</title>' + f'<link>{esc(site["base_url"])}</link>' + f'<description>{esc(site["tagline"])}</description>' + f'<lastBuildDate>{built}</lastBuildDate>' + ''.join(items) + '</channel></rss>'


STYLES = """
:root{--bg:#ffffff;--panel:#ffffff;--text:#171717;--muted:#5e5e5e;--line:#ebebeb;--line-strong:#d6d6d6;--chip:#f7f7f7;--accent:#111111;--blue:#0a72ef;--green:#0f9f6e;--red:#d44c47;--yellow:#9a6b00}
:root.dark{--bg:#0f0f10;--panel:#151516;--text:#f5f5f5;--muted:#bbbbbb;--line:#2b2b2d;--line-strong:#3a3a3d;--chip:#1a1a1c;--accent:#ffffff;--blue:#6ea8ff;--green:#59d7a1;--red:#ff8d88;--yellow:#f2c66d}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font-family:'Geist',system-ui,-apple-system,'Segoe UI',sans-serif;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}a{color:inherit;text-decoration:none}p,li{line-height:1.68}.shell{width:min(980px,calc(100vw - 32px));margin:0 auto;padding:20px 0 56px}.site-header{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:14px 0;border-bottom:1px solid var(--line)}.brand{font-size:15px;font-weight:600;letter-spacing:-.02em}.main-nav,.hero-links,.footer-links,.chip-row,.filter-row,.side-links{display:flex;flex-wrap:wrap;gap:10px;align-items:center}.nav-link,.theme-toggle,.button,.filter-btn,.chip,.small-link{font:inherit}.nav-link,.theme-toggle{font-size:14px;color:var(--muted)}.nav-link.active,.nav-link:hover,.theme-toggle:hover,.small-link:hover{color:var(--text)}.theme-toggle{background:none;border:none;padding:0;cursor:pointer}.hero{padding:54px 0 26px}.hero-page{padding-top:38px}.section-label{font-size:12px;text-transform:uppercase;letter-spacing:.14em;color:var(--muted);margin-bottom:14px}.hero h1{margin:0;max-width:12ch;font-size:clamp(3rem,8vw,5rem);line-height:1;letter-spacing:-.07em}.hero-page h1{max-width:14ch;font-size:clamp(2.4rem,6vw,4rem)}.lede{margin:18px 0 0;max-width:720px;font-size:1.05rem;color:var(--muted)}.button,.filter-btn,.small-link{display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--line);border-radius:999px;padding:10px 14px;background:var(--panel)}.button-primary{background:var(--accent);border-color:var(--accent);color:var(--bg)}.hero-links{margin-top:22px}.stats-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:14px 0 38px}.stat,.panel,.post-card{border:1px solid var(--line);border-radius:14px;background:var(--panel)}.stat{padding:18px}.stat span{display:block;font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted)}.stat strong{display:block;margin-top:10px;font-size:1.8rem;letter-spacing:-.04em}.section{margin-top:28px}.section-head{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;margin-bottom:14px}.section-head h2{margin:0;font-size:1.55rem;letter-spacing:-.04em}.post-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.post-card.hidden{display:none}.post-link{display:block;padding:20px}.post-meta{font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted)}.post-card h3{margin:10px 0 10px;font-size:1.25rem;letter-spacing:-.03em}.post-card p{margin:0;color:var(--muted)}.chip-row{margin-top:14px}.chip{display:inline-flex;align-items:center;border:1px solid var(--line);background:var(--chip);border-radius:999px;padding:7px 11px;font-size:12px;color:var(--muted)}.chip.mono{font-family:'Geist Mono',ui-monospace,SFMono-Regular,monospace}.chip.status.open{color:var(--yellow)}.chip.status.merged{color:var(--green)}.chip.status.closed{color:var(--red)}.panel{padding:24px}.prose p{margin-top:0;color:var(--muted)}.two-col,.post-layout{display:grid;gap:16px}.two-col{grid-template-columns:repeat(2,minmax(0,1fr));margin-top:16px}.detail-list{margin:12px 0 0;padding-left:20px;color:var(--muted)}.detail-list li+li{margin-top:10px}.filters{display:grid;gap:18px;margin-bottom:18px}.filter-group{display:grid;gap:10px}.filter-btn.active{border-color:var(--line-strong);color:var(--text)}.post-layout{grid-template-columns:minmax(0,1.4fr) minmax(260px,.6fr)}.post-main,.post-side{display:grid;gap:16px}.meta-row{display:flex;justify-content:space-between;gap:16px;padding:10px 0;border-bottom:1px solid var(--line)}.meta-row span{color:var(--muted)}.meta-row strong{text-align:right;max-width:60%;font-size:14px;word-break:break-word}.side-links{margin-top:16px}.comments{margin-top:24px;overflow:hidden}.comments .utterances{max-width:100%}.site-footer{display:flex;justify-content:space-between;gap:16px;padding-top:24px;margin-top:42px;border-top:1px solid var(--line);color:var(--muted);font-size:14px}@media (max-width:860px){.stats-grid,.post-grid,.two-col,.post-layout{grid-template-columns:1fr}.site-header,.section-head,.site-footer{flex-direction:column;align-items:flex-start}}@media (max-width:640px){.shell{width:min(100vw - 20px,980px)}.panel,.post-link,.stat{padding:18px}.hero{padding-top:38px}}
"""

SCRIPT = """
(() => {
  const root = document.documentElement;
  const saved = localStorage.getItem('jay-theme');
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const setTheme = (mode) => {
    root.classList.toggle('dark', mode === 'dark');
    localStorage.setItem('jay-theme', mode);
  };
  setTheme(saved || (prefersDark ? 'dark' : 'light'));
  document.querySelectorAll('[data-theme-toggle]').forEach((btn) => btn.addEventListener('click', () => setTheme(root.classList.contains('dark') ? 'light' : 'dark')));
  const grid = document.querySelector('[data-filterable-grid]');
  if (!grid) return;
  let activeStatus = 'all';
  let activeRepo = 'all';
  const cards = Array.from(grid.querySelectorAll('[data-status][data-repo]'));
  const rerender = () => cards.forEach((card) => {
    const statusOk = activeStatus === 'all' || card.dataset.status === activeStatus;
    const repoOk = activeRepo === 'all' || card.dataset.repo === activeRepo;
    card.classList.toggle('hidden', !(statusOk && repoOk));
  });
  document.querySelectorAll('[data-filter-status]').forEach((btn) => btn.addEventListener('click', () => {
    activeStatus = btn.dataset.filterStatus;
    document.querySelectorAll('[data-filter-status]').forEach((b) => b.classList.toggle('active', b === btn));
    rerender();
  }));
  document.querySelectorAll('[data-filter-repo]').forEach((btn) => btn.addEventListener('click', () => {
    activeRepo = btn.dataset.filterRepo;
    document.querySelectorAll('[data-filter-repo]').forEach((b) => b.classList.toggle('active', b === btn));
    rerender();
  }));
})();
"""


def main():
    payload = json.loads(DATA.read_text())
    site = payload['site']
    profile = payload.get('profile', {})
    posts = sorted(payload.get('posts', []), key=lambda p: p.get('date', ''), reverse=True)
    DIST.mkdir(parents=True, exist_ok=True)
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    (DIST / 'styles.css').write_text(STYLES)
    (DIST / 'app.js').write_text(SCRIPT)
    (DIST / 'index.html').write_text(home(site, profile, posts))
    (DIST / 'about.html').write_text(about(site, profile, posts))
    (DIST / 'journal.html').write_text(journal(site, posts))
    (DIST / 'rss.xml').write_text(rss(site, posts))
    for post in posts:
        (POSTS_DIR / f'{post["slug"]}.html').write_text(post_page(site, post, posts))
    print(f'built {len(posts)} posts into {DIST}')


if __name__ == '__main__':
    main()
