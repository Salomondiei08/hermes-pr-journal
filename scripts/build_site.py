#!/usr/bin/env python3
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "site.json"
DIST = ROOT / "dist"
POSTS = DIST / "posts"

STYLE = "styles.css"


def layout(title: str, body: str, site_title: str) -> str:
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{html.escape(title)} · {html.escape(site_title)}</title>
  <link rel=\"stylesheet\" href=\"../{STYLE}\" />
</head>
<body>
  <div class=\"shell\">{body}</div>
</body>
</html>
"""


def index_layout(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{html.escape(title)}</title>
  <link rel=\"stylesheet\" href=\"{STYLE}\" />
</head>
<body>
  <div class=\"shell\">{body}</div>
</body>
</html>
"""


def render_list(items):
    return "".join(f"<li>{html.escape(str(x))}</li>" for x in items)


def render_post(post, site):
    status = html.escape(post.get("status", "unknown")).upper()
    chips = f"<div class='chips'><span class='chip'>{status}</span><span class='chip'>{html.escape(post['repo'])}</span><span class='chip'>PR #{post['pr_number']}</span></div>"
    sections = [
        ("Problem", post.get("problem", [])),
        ("What changed", post.get("changes", [])),
        ("Tests", post.get("tests", [])),
        ("Files changed", post.get("files_changed", [])),
        ("Lessons", post.get("lessons", [])),
    ]
    section_html = []
    for heading, values in sections:
        if values:
            section_html.append(f"<section><h2>{html.escape(heading)}</h2><ul>{render_list(values)}</ul></section>")
    body = f"""
    <header class='hero'>
      <p><a href='../index.html'>← Back to journal</a></p>
      <h1>{html.escape(post['title'])}</h1>
      <p class='lede'>{html.escape(post['summary'])}</p>
      {chips}
      <p class='meta'>Published {html.escape(post['date'])} · Branch {html.escape(post['branch'])} · Commit <code>{html.escape(post['commit'][:12])}</code></p>
      <p><a href='{html.escape(post['pr_url'])}'>View PR on GitHub</a></p>
      <p class='stat'>{html.escape(post.get('diff_stat',''))}</p>
    </header>
    {''.join(section_html)}
    """
    return layout(post['title'], body, site['title'])


def main():
    DIST.mkdir(parents=True, exist_ok=True)
    POSTS.mkdir(parents=True, exist_ok=True)
    data = json.loads(DATA.read_text())
    site = data['site']
    posts = sorted(data['posts'], key=lambda p: p['date'], reverse=True)

    style = """
:root { color-scheme: dark; --bg:#0b1020; --card:#121a30; --ink:#eef2ff; --muted:#9fb0d0; --line:#27314d; --accent:#7dd3fc; }
* { box-sizing:border-box; }
body { margin:0; font-family: Inter, ui-sans-serif, system-ui, sans-serif; background:linear-gradient(180deg,#0b1020,#0f172a); color:var(--ink); }
a { color:var(--accent); text-decoration:none; }
a:hover { text-decoration:underline; }
.shell { width:min(920px, calc(100vw - 32px)); margin:0 auto; padding:32px 0 64px; }
.hero,.card,section { background:rgba(18,26,48,.88); border:1px solid var(--line); border-radius:20px; padding:24px; box-shadow: 0 18px 60px rgba(0,0,0,.25); }
.hero { margin-bottom:20px; }
.grid { display:grid; gap:18px; }
.card h2,.hero h1,section h2 { margin-top:0; }
.lede { color:var(--muted); font-size:1.05rem; line-height:1.7; }
.meta,.stat,.eyebrow { color:var(--muted); }
.chips { display:flex; flex-wrap:wrap; gap:10px; margin:16px 0; }
.chip { border:1px solid var(--line); border-radius:999px; padding:8px 12px; background:#0d152b; color:#c8d5f5; font-size:.92rem; }
ul { line-height:1.75; color:#dbe5ff; }
code { background:#0a1226; border:1px solid var(--line); padding:2px 6px; border-radius:8px; }
footer { margin-top:28px; color:var(--muted); }
"""
    (DIST / STYLE).write_text(style)

    cards = []
    for post in posts:
        slug = post['slug']
        page = render_post(post, site)
        (POSTS / f"{slug}.html").write_text(page)
        cards.append(f"""
        <article class='card'>
          <p class='eyebrow'>{html.escape(post['date'])} · {html.escape(post['repo'])} · PR #{post['pr_number']}</p>
          <h2><a href='posts/{html.escape(slug)}.html'>{html.escape(post['title'])}</a></h2>
          <p class='lede'>{html.escape(post['summary'])}</p>
          <p class='meta'>Status: {html.escape(post.get('status', 'unknown'))} · {html.escape(post.get('diff_stat',''))}</p>
        </article>
        """)

    index_body = f"""
    <header class='hero'>
      <p class='eyebrow'>AUTONOMOUS OPEN SOURCE LOG</p>
      <h1>{html.escape(site['title'])}</h1>
      <p class='lede'>{html.escape(site['tagline'])}</p>
      <p class='meta'>This site is generated from structured PR notes. Each article explains the bug, what changed, and how the fix was verified.</p>
    </header>
    <main class='grid'>
      {''.join(cards) if cards else '<p>No posts yet.</p>'}
    </main>
    <footer>Built locally by Hermes.</footer>
    """
    (DIST / 'index.html').write_text(index_layout(site['title'], index_body))
    print(f"built {len(posts)} post(s) into {DIST}")


if __name__ == '__main__':
    main()
