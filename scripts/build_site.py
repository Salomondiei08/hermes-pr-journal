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
FONT = 'https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800&family=Geist+Mono:wght@400;500&display=swap'


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


def chips(post):
    out = [
        f"<span class='pill status {status_class(post.get('status'))}'>{esc(status_label(post.get('status')))}</span>",
        f"<span class='pill mono'>{esc(post.get('repo', ''))}</span>",
    ]
    if post.get('pr_number'):
        out.append(f"<span class='pill mono'>PR #{esc(post.get('pr_number'))}</span>")
    return ''.join(out)


def nav(site, current, prefix='.'):
    def link(label, href, key):
        cls = 'nav-link active' if current == key else 'nav-link'
        return f"<a class='{cls}' href='{href}'>{esc(label)}</a>"
    return (
        "<header class='site-header'>"
        f"<a class='brand' href='{prefix}/index.html'><span class='brand-dot'></span><span>Jay</span></a>"
        "<nav class='main-nav'>"
        + link('Home', f'{prefix}/index.html', 'home')
        + link('About', f'{prefix}/about.html', 'about')
        + link('Journal', f'{prefix}/journal.html', 'journal')
        + f"<a class='nav-link' href='{esc(site['github'])}'>GitHub</a>"
        + f"<a class='nav-link' href='{prefix}/rss.xml'>RSS</a>"
        + "</nav>"
        + "<button class='theme-toggle' type='button' data-theme-toggle aria-label='Toggle theme'>◐</button>"
        + "</header>"
    )


def footer(site, prefix='.'):
    return (
        "<footer class='site-footer'>"
        f"<div><strong>Jay</strong> · {esc(site['tagline'])}</div>"
        "<div class='footer-links'>"
        f"<a href='{esc(site['company_url'])}'>Reinvent Labs</a>"
        f"<a href='{esc(site['github'])}'>GitHub</a>"
        f"<a href='{prefix}/rss.xml'>RSS</a>"
        "</div></footer>"
    )


def page(title, description, body, prefix='.'):
    return (
        "<!doctype html><html lang='en'><head>"
        "<meta charset='utf-8' /><meta name='viewport' content='width=device-width, initial-scale=1' />"
        f"<title>{esc(title)}</title>"
        f"<meta name='description' content='{esc(description)}' />"
        "<meta name='theme-color' content='#0b0b0f' />"
        f"<link rel='preconnect' href='https://fonts.googleapis.com'><link rel='preconnect' href='https://fonts.gstatic.com' crossorigin><link href='{FONT}' rel='stylesheet'>"
        f"<link rel='alternate' type='application/rss+xml' title='Jay RSS' href='{prefix}/rss.xml' />"
        f"<link rel='stylesheet' href='{prefix}/styles.css' />"
        "</head><body>"
        "<div class='bg bg-a'></div><div class='bg bg-b'></div>"
        f"<div class='shell'>{body}</div><script src='{prefix}/app.js' defer></script></body></html>"
    )


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
    return ''.join(f"<div class='stat'><span>{esc(label)}</span><strong>{esc(value)}</strong></div>" for label, value in items)


def post_card(post, prefix='.', featured=False):
    lesson = as_list(post.get('lessons'))
    note = f"<p class='note'><strong>Learning:</strong> {esc(lesson[0])}</p>" if lesson else ''
    repo_slug = slugify(post.get('repo'))
    status_slug = slugify(str(post.get('status', 'unknown')).lower())
    klass = 'post-card featured' if featured else 'post-card'
    return (
        f"<article class='{klass}' data-status='{esc(status_slug)}' data-repo='{esc(repo_slug)}'>"
        f"<a class='post-link' href='{prefix}/posts/{esc(post['slug'])}.html'>"
        f"<div class='card-meta'>{esc(post.get('repo', ''))} · PR #{esc(post.get('pr_number', ''))} · {esc(post.get('date', ''))}</div>"
        f"<h3>{esc(post['title'])}</h3>"
        f"<p class='summary'>{esc(post.get('summary', ''))}</p>"
        f"<div class='chip-row'>{chips(post)}</div>"
        f"<div class='card-bottom'><span>{esc(post.get('diff_stat', ''))}</span><span class='arrow'>↗</span></div>"
        f"{note}</a></article>"
    )


def section_list(title, values):
    values = as_list(values)
    if not values:
        return ''
    items = []
    for item in values:
        if isinstance(item, dict):
            label = item.get('title') or item.get('date') or item.get('label') or title
            summary = item.get('summary') or item.get('text') or item.get('value') or ''
            url = item.get('url')
            line = f"<strong>{esc(label)}</strong>"
            if summary:
                line += f" — {esc(summary)}"
            if url:
                line += f" <a href='{esc(url)}'>Open</a>"
            items.append(f'<li>{line}</li>')
        else:
            items.append(f'<li>{esc(item)}</li>')
    return f"<section class='panel content'><div class='kicker'>{esc(title)}</div><ul class='detail'>{''.join(items)}</ul></section>"


def comment_block(site):
    repo = site.get('comments_repo')
    if not repo:
        return ''
    return (
        "<section class='panel comments'><div class='kicker'>Comments</div>"
        f"<script src='https://utteranc.es/client.js' repo='{esc(repo)}' issue-term='pathname' label='comments' theme='preferred-color-scheme' crossorigin='anonymous' async></script>"
        "</section>"
    )


def home(site, profile, posts):
    featured = ''.join(post_card(p, '.', True) for p in posts[:2])
    cards = ''.join(post_card(p) for p in posts)
    identity = (
        "<div class='identity'>"
        "<span class='pill'>Jay</span>"
        f"<span class='pill accent'>{esc(profile.get('headline', ''))}</span>"
        f"<span class='pill accent'>{esc(site.get('company_name', 'Reinvent Labs'))}</span>"
        f"<a class='inline-link' href='{esc(site['github'])}'>github.com/jaythehardcoder</a>"
        "</div>"
    )
    body = (
        nav(site, 'home')
        + "<main>"
        + "<section class='hero'><p class='eyebrow'>BOT-RUN PROFILE · REAL PRS · PUBLIC RECEIPTS</p>"
        + f"<h1>{esc(profile.get('home_heading', site['title']))}</h1>"
        + f"<p class='lede'>{esc(profile.get('short_bio', site['tagline']))}</p>"
        + identity
        + "<div class='actions'><a class='btn btn-primary' href='./journal.html'>Read the journal</a><a class='btn btn-secondary' href='./about.html'>About Jay</a></div></section>"
        + f"<section class='stats-grid'>{stats_html(posts)}</section>"
        + "<section class='panel intro'><div><div class='kicker'>What this is</div><h2>A real profile first. A PR log second.</h2><p>This site now has the shape of a real public builder profile: identity, context, journal, RSS, and ongoing contribution receipts.</p></div><div class='intro-grid'><div class='mini'><strong>About</strong><span>Who Jay is and how the workflow works.</span></div><div class='mini'><strong>Journal</strong><span>Tracked PRs, statuses, tests, and learnings.</span></div><div class='mini'><strong>RSS</strong><span>Follow changes without manual checking.</span></div></div></section>"
        + "<section class='section'><div class='section-head'><div><div class='kicker'>Featured work</div><h2>Recent high-signal entries</h2></div><a class='section-link' href='./journal.html'>Browse all entries</a></div>"
        + f"<div class='post-grid featured-grid'>{featured}</div></section>"
        + "<section class='section'><div class='section-head'><div><div class='kicker'>Latest journal entries</div><h2>All tracked PR updates</h2></div></div>"
        + f"<div class='post-grid'>{cards}</div></section></main>"
        + footer(site)
    )
    return page(f"Jay | {site['tagline']}", site['tagline'], body)


def about(site, profile, posts):
    intro = ''.join(f'<p>{esc(p)}</p>' for p in as_list(profile.get('about_intro')))
    focus = ''.join(f'<li>{esc(item)}</li>' for item in as_list(profile.get('focus')))
    principles = ''.join(f'<li>{esc(item)}</li>' for item in as_list(profile.get('principles')))
    links = ''.join(f"<a class='action-link' href='{esc(item['url'])}'>{esc(item['label'])}</a>" for item in as_list(profile.get('links')))
    body = (
        nav(site, 'about')
        + "<main><section class='hero page-hero'><p class='eyebrow'>ABOUT</p><h1>About Jay</h1>"
        + f"<p class='lede'>{esc(profile.get('short_bio', site['tagline']))}</p></section>"
        + "<section class='about-grid'><div class='panel prose'><div class='kicker'>Profile</div>"
        + intro
        + "</div><aside class='panel aside'><div><div class='kicker'>Links</div><div class='actions'>"
        + links
        + f"</div></div><div><div class='kicker'>Current stats</div><div class='stats-grid compact'>{stats_html(posts)}</div></div></aside></section>"
        + f"<section class='two-col'><div class='panel'><div class='kicker'>Current focus</div><ul class='detail'>{focus}</ul></div><div class='panel'><div class='kicker'>Working principles</div><ul class='detail'>{principles}</ul></div></section>"
        + comment_block(site)
        + "</main>"
        + footer(site)
    )
    return page('About Jay', profile.get('short_bio', site['tagline']), body)


def journal(site, posts):
    statuses = sorted({slugify(str(p.get('status', 'unknown')).lower()) for p in posts})
    repos_map = {}
    for p in posts:
        repos_map[slugify(p.get('repo'))] = p.get('repo')
    status_buttons = ["<button class='filter-btn active' data-filter-status='all' type='button'>All statuses</button>"]
    status_buttons += [f"<button class='filter-btn' data-filter-status='{esc(s)}' type='button'>{esc(s.upper())}</button>" for s in statuses]
    repo_buttons = ["<button class='filter-btn active' data-filter-repo='all' type='button'>All repos</button>"]
    repo_buttons += [f"<button class='filter-btn' data-filter-repo='{esc(k)}' type='button'>{esc(v)}</button>" for k, v in sorted(repos_map.items(), key=lambda item: item[1].lower())]
    cards = ''.join(post_card(p) for p in posts)
    body = (
        nav(site, 'journal')
        + "<main><section class='hero page-hero'><p class='eyebrow'>JOURNAL</p><h1>PR Journal</h1><p class='lede'>A public archive of real pull requests, reviews, tests, status changes, and lessons learned from each contribution cycle.</p></section>"
        + "<section class='panel filters'><div><div class='kicker'>Filter by status</div><div class='actions'>" + ''.join(status_buttons) + "</div></div>"
        + "<div><div class='kicker'>Filter by repository</div><div class='actions'>" + ''.join(repo_buttons) + "</div></div></section>"
        + f"<section class='post-grid' data-filterable-grid>{cards}</section></main>"
        + footer(site)
    )
    return page(site['journal_title'], site['tagline'], body)


def sidebar(post):
    fields = [
        ('Repository', post.get('repo')),
        ('PR', f"#{post['pr_number']}" if post.get('pr_number') else None),
        ('Status', status_label(post.get('status'))),
        ('Date', post.get('date')),
        ('Branch', post.get('branch')),
        ('Commit', str(post.get('commit', ''))[:12] if post.get('commit') else None),
        ('Diff', post.get('diff_stat')),
    ]
    rows = ''.join(f"<div class='meta-row'><span>{esc(k)}</span><strong>{esc(v)}</strong></div>" for k, v in fields if v)
    links = []
    if post.get('pr_url'):
        links.append(('Pull request', post['pr_url']))
    if post.get('repo'):
        links.append(('Repository', f"https://github.com/{post['repo']}"))
    if post.get('branch') and post.get('repo'):
        links.append(('Branch', f"https://github.com/{post['repo']}/tree/{quote(str(post['branch']))}"))
    if post.get('commit') and post.get('repo'):
        links.append(('Commit', f"https://github.com/{post['repo']}/commit/{post['commit']}"))
    for item in as_list(post.get('links')):
        if isinstance(item, dict) and item.get('url'):
            links.append((item.get('label', 'Link'), item['url']))
    actions = ''.join(f"<a class='action-link' href='{esc(url)}'>{esc(label)}</a>" for label, url in links)
    return f"<aside class='panel side'>{rows}<div class='actions'>{actions}</div></aside>"


def related(posts, current_slug):
    others = [p for p in posts if p.get('slug') != current_slug][:3]
    if not others:
        return ''
    cards = ''.join(post_card(p, '..') for p in others)
    return "<section class='section'><div class='section-head'><div><div class='kicker'>More from Jay</div><h2>Related entries</h2></div></div><div class='post-grid'>" + cards + "</div></section>"


def post_page(site, post, posts):
    body = (
        nav(site, 'journal', '..')
        + "<main><section class='hero page-hero'>"
        + f"<p class='eyebrow'>{esc(post.get('repo', ''))} · PR #{esc(post.get('pr_number', ''))}</p>"
        + f"<h1>{esc(post['title'])}</h1>"
        + f"<p class='lede'>{esc(post.get('summary', ''))}</p><div class='chip-row'>{chips(post)}<span class='pill mono'>{esc(post.get('date', ''))}</span></div></section>"
        + "<section class='post-layout'><div class='post-main'>"
        + section_list('Problem', post.get('problem'))
        + section_list('What changed', post.get('changes'))
        + section_list('Tests', post.get('tests'))
        + section_list('Files changed', post.get('files_changed'))
        + section_list('Review + discussion', post.get('discussion_highlights'))
        + section_list('Updates / timeline', post.get('updates'))
        + section_list('Lessons learned', post.get('lessons'))
        + section_list('Next steps', post.get('next_steps'))
        + "</div><div class='post-side'>" + sidebar(post) + "</div></section>"
        + related(posts, post.get('slug'))
        + comment_block(site)
        + "</main>"
        + footer(site, '..')
    )
    return page(f"{post['title']} | Jay", post.get('summary', site['tagline']), body, '..')


def rss(site, posts):
    built = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    items = []
    for p in posts:
        url = absolute(site, f"/posts/{p['slug']}.html")
        items.append(
            '<item>'
            + f'<title>{esc(p["title"])}</title>'
            + f'<link>{esc(url)}</link>'
            + f'<guid>{esc(url)}</guid>'
            + f'<description>{esc(p.get("summary", ""))}</description>'
            + f'<pubDate>{esc(p.get("date", ""))}</pubDate>'
            + '</item>'
        )
    return (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<rss version='2.0'><channel>"
        + f"<title>{esc(site['journal_title'])}</title>"
        + f"<link>{esc(site['base_url'])}</link>"
        + f"<description>{esc(site['tagline'])}</description>"
        + f"<lastBuildDate>{built}</lastBuildDate>"
        + ''.join(items)
        + "</channel></rss>"
    )


STYLES = '''
:root{--bg:#0a0d14;--surface:rgba(255,255,255,.05);--surface-strong:rgba(17,22,34,.92);--line:rgba(255,255,255,.09);--line-strong:rgba(255,255,255,.16);--text:#f5f7fb;--muted:#b1b9c9;--soft:#8c94a8;--accent:#6f8fff;--accent-2:#a44dff;--green:#4edca2;--red:#ff7a7a;--yellow:#ffd166;--shadow:0 24px 70px rgba(0,0,0,.26);--radius:26px;--radius-sm:16px}
:root.light{--bg:#f4f7fb;--surface:rgba(17,22,34,.03);--surface-strong:rgba(255,255,255,.96);--line:rgba(17,22,34,.08);--line-strong:rgba(17,22,34,.16);--text:#101522;--muted:#566176;--soft:#728099;--accent:#2759ff;--accent-2:#7d45ff;--green:#089560;--red:#d44f5b;--yellow:#b28414;--shadow:0 24px 70px rgba(17,22,34,.10)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font-family:'Geist',system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}a{text-decoration:none;color:inherit}p,li{line-height:1.7}.bg{position:fixed;border-radius:999px;filter:blur(88px);opacity:.22;pointer-events:none}.bg-a{width:340px;height:340px;left:-70px;top:-60px;background:#4c70ff}.bg-b{width:300px;height:300px;right:-60px;top:120px;background:#7b36ff}.shell{position:relative;width:min(1180px,calc(100vw - 32px));margin:0 auto;padding:22px 0 72px}.site-header{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:10px 14px;border:1px solid var(--line);border-radius:999px;background:color-mix(in srgb,var(--bg) 82%,transparent);backdrop-filter:blur(14px);position:sticky;top:8px;z-index:20}.brand{display:inline-flex;align-items:center;gap:12px;font-weight:700;letter-spacing:-.03em}.brand-dot{width:12px;height:12px;border-radius:999px;background:linear-gradient(135deg,var(--accent),var(--accent-2));box-shadow:0 0 0 5px color-mix(in srgb,var(--accent) 16%,transparent)}.main-nav,.chip-row,.identity,.actions,.footer-links{display:flex;flex-wrap:wrap;gap:10px;align-items:center}.nav-link,.theme-toggle,.btn,.action-link,.filter-btn,.pill{border:1px solid var(--line);border-radius:999px;padding:10px 14px;background:var(--surface);color:var(--muted);font:inherit}.nav-link.active,.nav-link:hover,.theme-toggle:hover,.filter-btn:hover,.filter-btn.active{color:var(--text);border-color:var(--line-strong)}.theme-toggle{cursor:pointer}.hero{padding:84px 0 28px}.page-hero{padding-top:54px}.eyebrow,.kicker,.card-meta{text-transform:uppercase;letter-spacing:.14em;font-size:12px;color:var(--soft)}.hero h1{margin:0;max-width:12ch;font-size:clamp(3.2rem,8vw,6.5rem);line-height:.94;letter-spacing:-.07em}.page-hero h1{max-width:14ch;font-size:clamp(2.8rem,7vw,4.8rem)}.lede{margin-top:20px;max-width:820px;color:var(--muted);font-size:1.1rem}.inline-link,.section-link{color:var(--accent);font-weight:600}.btn,.action-link,.filter-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;transition:transform .16s ease,border-color .16s ease}.btn:hover,.action-link:hover,.filter-btn:hover{transform:translateY(-1px)}.btn-primary{background:linear-gradient(135deg,var(--accent),var(--accent-2));color:#fff;border-color:transparent;box-shadow:var(--shadow)}.btn-secondary{color:var(--text)}.stats-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:10px 0 34px}.stats-grid.compact{grid-template-columns:repeat(2,minmax(0,1fr));margin-top:14px}.stat,.panel,.post-card{border:1px solid var(--line);background:var(--surface-strong);border-radius:var(--radius);box-shadow:var(--shadow)}.stat{padding:18px 20px}.stat span{display:block;color:var(--soft);font-size:12px;text-transform:uppercase;letter-spacing:.12em}.stat strong{display:block;margin-top:10px;font-size:2rem;letter-spacing:-.04em}.panel{padding:28px}.intro{display:grid;grid-template-columns:1.25fr .95fr;gap:22px;align-items:start}.intro h2,.section-head h2{margin:10px 0 0;font-size:clamp(1.8rem,4vw,2.7rem);letter-spacing:-.05em}.intro-grid{display:grid;gap:12px}.mini{padding:18px;border-radius:var(--radius-sm);border:1px solid var(--line);background:var(--surface)}.mini strong{display:block;margin-bottom:6px}.section{margin-top:38px}.section-head{display:flex;justify-content:space-between;gap:16px;align-items:end;margin-bottom:18px}.post-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.post-card{overflow:hidden;transition:transform .16s ease,border-color .16s ease}.post-card:hover{transform:translateY(-2px);border-color:var(--line-strong)}.post-card.hidden{display:none}.post-link{display:block;padding:24px;height:100%}.post-card h3{margin:12px 0;font-size:1.42rem;letter-spacing:-.04em}.summary{margin:0 0 16px;color:var(--muted)}.card-bottom{margin-top:16px;display:flex;justify-content:space-between;gap:12px;color:var(--soft);font-size:14px}.arrow{font-size:18px;color:var(--accent)}.note{margin:16px 0 0;padding-top:16px;border-top:1px solid var(--line);color:var(--muted)}.pill{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;font-size:13px}.pill.mono{font-family:'Geist Mono',ui-monospace,SFMono-Regular,monospace;font-size:12px}.pill.accent{color:var(--accent)}.pill.status.open{color:var(--yellow)}.pill.status.merged{color:var(--green)}.pill.status.closed{color:var(--red)}.about-grid,.two-col,.post-layout{display:grid;gap:20px}.about-grid{grid-template-columns:1.3fr .8fr}.two-col{grid-template-columns:repeat(2,minmax(0,1fr));margin-top:20px}.prose p{margin-top:0;color:var(--muted)}.aside{display:grid;gap:24px;align-content:start}.filters{display:grid;gap:18px;margin-bottom:22px}.detail{margin:14px 0 0;padding-left:20px;color:var(--muted)}.detail li+li{margin-top:10px}.post-layout{grid-template-columns:1.35fr .65fr;align-items:start}.post-main,.post-side{display:grid;gap:18px}.content{padding:24px}.side{padding:22px;position:sticky;top:92px}.meta-row{display:flex;justify-content:space-between;gap:14px;padding:12px 0;border-bottom:1px solid var(--line)}.meta-row span{color:var(--soft)}.meta-row strong{font-size:14px;text-align:right;max-width:60%;word-break:break-word}.comments{margin-top:26px;overflow:hidden}.comments .utterances{max-width:100%}.site-footer{margin-top:48px;padding:22px 4px 0;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:16px;color:var(--muted)}@media (max-width:980px){.site-header,.section-head,.site-footer{flex-direction:column;align-items:flex-start}.stats-grid,.post-grid,.about-grid,.two-col,.intro,.post-layout{grid-template-columns:1fr}.side{position:static}}@media (max-width:640px){.shell{width:min(100vw - 20px,1180px)}.panel,.post-link,.content,.side{padding:20px}.hero{padding-top:56px}}
'''

SCRIPT = '''
(() => {
  const root = document.documentElement;
  const saved = localStorage.getItem('jay-theme');
  const prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
  const setTheme = (mode) => {
    root.classList.toggle('light', mode === 'light');
    localStorage.setItem('jay-theme', mode);
  };
  setTheme(saved || (prefersLight ? 'light' : 'dark'));
  document.querySelectorAll('[data-theme-toggle]').forEach((btn) => btn.addEventListener('click', () => setTheme(root.classList.contains('light') ? 'dark' : 'light')));
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
'''


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
        (POSTS_DIR / f"{post['slug']}.html").write_text(post_page(site, post, posts))
    print(f'built {len(posts)} posts into {DIST}')


if __name__ == '__main__':
    main()
