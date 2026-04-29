#!/usr/bin/env python3
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "site.json"
DIST = ROOT / "dist"
POSTS = DIST / "posts"
STYLE = "styles.css"
FONT_LINK = "https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500&display=swap"


def esc(value):
    return html.escape(str(value))


def as_list(value):
    if not value:
        return []
    if isinstance(value, list):
        return value
    return [value]


def count_status(posts, name):
    return sum(1 for post in posts if str(post.get("status", "")).lower() == name)


def status_class(status):
    status = str(status or "unknown").lower()
    return {
        "merged": "is-merged",
        "open": "is-open",
        "closed": "is-closed",
        "draft": "is-draft",
    }.get(status, "is-neutral")


def status_label(status):
    return str(status or "unknown").upper()


def derive_repo_url(post):
    repo = post.get("repo")
    return f"https://github.com/{repo}" if repo else None


def derive_commit_url(post):
    repo = post.get("repo")
    commit = post.get("commit")
    if repo and commit:
        return f"https://github.com/{repo}/commit/{commit}"
    return None


def derive_branch_url(post):
    repo = post.get("repo")
    branch = post.get("branch")
    if repo and branch:
        return f"https://github.com/{repo}/tree/{branch}"
    return None


def normalize_links(post):
    links = []
    seen = set()

    def add(label, url):
        if not url:
            return
        key = (label, url)
        if key in seen:
            return
        seen.add(key)
        links.append({"label": label, "url": url})

    add("Pull request", post.get("pr_url"))
    add("Repository", derive_repo_url(post))
    add("Commit", derive_commit_url(post))
    add("Branch", derive_branch_url(post))

    for item in as_list(post.get("links")):
        if isinstance(item, dict):
            add(item.get("label", "Link"), item.get("url"))
        elif isinstance(item, str):
            add("Link", item)

    return links


def render_chip(text, class_name=""):
    extra = f" {class_name}" if class_name else ""
    return f"<span class='chip{extra}'>{esc(text)}</span>"


def render_meta_row(post):
    chips = [
        render_chip(status_label(post.get("status")), f"status-chip {status_class(post.get('status'))}"),
    ]
    if post.get("repo"):
        chips.append(render_chip(post["repo"], "mono-chip"))
    if post.get("pr_number"):
        chips.append(render_chip(f"PR #{post['pr_number']}", "mono-chip"))
    if post.get("date"):
        chips.append(render_chip(post["date"]))
    return "".join(chips)


def render_bullet_list(values):
    parts = []
    for item in as_list(values):
        if isinstance(item, dict):
            label = item.get("title") or item.get("label") or item.get("date") or "Update"
            body = item.get("summary") or item.get("text") or item.get("value") or ""
            url = item.get("url")
            line = f"<strong>{esc(label)}</strong>"
            if body:
                line += f" — {esc(body)}"
            if url:
                line += f" <a href='{esc(url)}'>Open</a>"
            parts.append(f"<li>{line}</li>")
        else:
            parts.append(f"<li>{esc(item)}</li>")
    return "".join(parts)


def render_section(title, values, section_class=""):
    values = as_list(values)
    if not values:
        return ""
    klass = f"section-card {section_class}".strip()
    return f"""
    <section class='{klass}'>
      <div class='section-heading'>{esc(title)}</div>
      <ul class='detail-list'>{render_bullet_list(values)}</ul>
    </section>
    """


def render_links(links):
    if not links:
        return ""
    items = "".join(
        f"<a class='action-link' href='{esc(item['url'])}'>{esc(item['label'])}</a>" for item in links
    )
    return f"<div class='action-group'>{items}</div>"


def render_sidebar(post):
    rows = []
    fields = [
        ("Repository", post.get("repo")),
        ("PR", f"#{post['pr_number']}" if post.get("pr_number") else None),
        ("Status", status_label(post.get("status"))),
        ("Published", post.get("date")),
        ("Branch", post.get("branch")),
        ("Commit", (post.get("commit") or "")[:12] if post.get("commit") else None),
        ("Diff", post.get("diff_stat")),
    ]
    for label, value in fields:
        if value:
            rows.append(f"<div class='meta-pair'><span>{esc(label)}</span><strong>{esc(value)}</strong></div>")
    return f"<aside class='sidebar-card'>{''.join(rows)}</aside>" if rows else ""


def render_related(post, posts):
    related = [p for p in posts if p.get('slug') != post.get('slug') and p.get('repo') == post.get('repo')][:3]
    if not related:
        related = [p for p in posts if p.get('slug') != post.get('slug')][:2]
    if not related:
        return ''
    cards = []
    for item in related:
        cards.append(f"""
        <a class='related-card' href='../posts/{esc(item['slug'])}.html'>
          <div class='mini-meta'>{esc(item.get('repo',''))} · PR #{esc(item.get('pr_number',''))}</div>
          <h3>{esc(item['title'])}</h3>
          <p>{esc(item.get('summary',''))}</p>
        </a>
        """)
    return f"""
    <section class='related-shell'>
      <div class='section-heading'>Related entries</div>
      <div class='related-grid'>{''.join(cards)}</div>
    </section>
    """


def layout(title: str, body: str, site_title: str, root_prefix: str) -> str:
    page_title = esc(site_title if title == site_title else f"{title} · {site_title}")
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{page_title}</title>
  <meta name=\"theme-color\" content=\"#fafafa\" />
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
  <link href=\"{FONT_LINK}\" rel=\"stylesheet\">
  <link rel=\"stylesheet\" href=\"{root_prefix}/{STYLE}\" />
</head>
<body>
  <div class=\"page-bg\"></div>
  <div class=\"shell\">{body}</div>
</body>
</html>
"""


def render_post(post, site, posts):
    links = normalize_links(post)
    body = f"""
    <header class='topbar'>
      <a class='brand' href='../index.html'>
        <span class='brand-mark'></span>
        <span>{esc(site['title'])}</span>
      </a>
      <a class='toplink' href='{esc(post['pr_url'])}'>View on GitHub</a>
    </header>

    <main class='post-layout'>
      <section class='post-hero'>
        <p class='eyebrow'>REAL OPEN SOURCE WORK</p>
        <h1>{esc(post['title'])}</h1>
        <p class='lede'>{esc(post.get('summary', ''))}</p>
        <div class='chip-row'>{render_meta_row(post)}</div>
        {render_links(links)}
      </section>

      <div class='post-grid'>
        <div class='post-main'>
          {render_section('Problem', post.get('problem'))}
          {render_section('What changed', post.get('changes'))}
          {render_section('Tests', post.get('tests'))}
          {render_section('Files changed', post.get('files_changed'))}
          {render_section('Review + discussion', post.get('discussion_highlights'))}
          {render_section('Updates / timeline', post.get('updates'))}
          {render_section('Lessons learned', post.get('lessons'))}
          {render_section('Next steps', post.get('next_steps'))}
          {render_related(post, posts)}
        </div>
        <div class='post-side'>
          {render_sidebar(post)}
        </div>
      </div>
    </main>
    """
    return layout(post['title'], body, site['title'], '..')


def render_featured(posts):
    if not posts:
        return ''
    featured = posts[:2]
    cards = []
    for post in featured:
        cards.append(f"""
        <a class='featured-card' href='posts/{esc(post['slug'])}.html'>
          <div class='mini-meta'>{esc(post.get('repo',''))} · PR #{esc(post.get('pr_number',''))}</div>
          <h3>{esc(post['title'])}</h3>
          <p>{esc(post.get('summary', ''))}</p>
          <div class='chip-row'>{render_meta_row(post)}</div>
        </a>
        """)
    return f"<section class='featured-grid'>{''.join(cards)}</section>"


def render_card(post):
    lesson = as_list(post.get('lessons'))
    lesson_html = f"<p class='micro-note'>Lesson: {esc(lesson[0])}</p>" if lesson else ''
    return f"""
    <article class='feed-card'>
      <a class='card-link' href='posts/{esc(post['slug'])}.html'>
        <div class='card-head'>
          <div>
            <div class='mini-meta'>{esc(post.get('repo',''))} · PR #{esc(post.get('pr_number',''))} · {esc(post.get('date',''))}</div>
            <h2>{esc(post['title'])}</h2>
          </div>
          <span class='arrow'>↗</span>
        </div>
        <p class='card-summary'>{esc(post.get('summary', ''))}</p>
        <div class='card-footer'>
          <div class='chip-row'>{render_meta_row(post)}</div>
          <div class='statline'>{esc(post.get('diff_stat', ''))}</div>
        </div>
        {lesson_html}
      </a>
    </article>
    """


def build_styles():
    return """
:root {
  --bg: #fafafa;
  --surface: rgba(255,255,255,0.88);
  --surface-strong: #ffffff;
  --text: #171717;
  --muted: #5e5e5e;
  --line: rgba(0,0,0,0.08);
  --line-strong: #e9e9e9;
  --blue: #0a72ef;
  --pink: #de1d8d;
  --red: #ff5b4f;
  --green: #0f9f6e;
  --shadow-card: rgba(0,0,0,0.08) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 8px 30px -12px, #fafafa 0px 0px 0px 1px inset;
  --radius: 20px;
  --radius-sm: 14px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: 'Geist', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
a { color: inherit; text-decoration: none; }
a:hover { text-decoration: none; }
.page-bg {
  position: fixed;
  inset: 0;
  background:
    radial-gradient(circle at top left, rgba(10,114,239,0.07), transparent 28%),
    radial-gradient(circle at top right, rgba(222,29,141,0.06), transparent 28%),
    linear-gradient(180deg, #ffffff 0%, #fafafa 60%, #f6f6f6 100%);
  pointer-events: none;
}
.shell {
  position: relative;
  width: min(1100px, calc(100vw - 32px));
  margin: 0 auto;
  padding: 20px 0 72px;
}
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 10px 0 20px;
}
.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: -0.2px;
}
.brand-mark {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: linear-gradient(135deg, var(--text), var(--blue));
  box-shadow: 0 0 0 4px rgba(10,114,239,0.08);
}
.toplink {
  color: var(--muted);
  font-size: 14px;
}
.toplink:hover, .action-link:hover, .card-link:hover h2, .featured-card:hover h3, .related-card:hover h3 {
  color: var(--blue);
}
.hero {
  padding: 36px 0 26px;
}
.eyebrow {
  margin: 0 0 14px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.12em;
}
.hero h1, .post-hero h1 {
  margin: 0;
  max-width: 12ch;
  font-size: clamp(2.8rem, 6vw, 5rem);
  line-height: 0.95;
  letter-spacing: -0.06em;
}
.hero .lede, .post-hero .lede {
  margin: 20px 0 0;
  max-width: 760px;
  font-size: 1.1rem;
  line-height: 1.8;
  color: var(--muted);
}
.metrics {
  display: grid;
  grid-template-columns: repeat(4, minmax(0,1fr));
  gap: 14px;
  margin-top: 28px;
}
.metric {
  background: rgba(255,255,255,0.8);
  border-radius: 18px;
  padding: 18px;
  box-shadow: var(--shadow-card);
}
.metric .label {
  color: var(--muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.metric strong {
  display: block;
  margin-top: 12px;
  font-size: 2rem;
  letter-spacing: -0.05em;
}
.featured-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0,1fr));
  gap: 18px;
  margin: 22px 0 28px;
}
.featured-card,
.feed-card,
.sidebar-card,
.section-card,
.related-card {
  background: var(--surface);
  border-radius: var(--radius);
  box-shadow: var(--shadow-card);
  backdrop-filter: blur(10px);
}
.featured-card {
  padding: 24px;
  min-height: 230px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.featured-card h3, .related-card h3 {
  margin: 10px 0 10px;
  font-size: 1.55rem;
  line-height: 1.06;
  letter-spacing: -0.04em;
}
.featured-card p, .related-card p, .card-summary, .micro-note, .statline {
  color: var(--muted);
}
.section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 24px 0 14px;
}
.section-title h2 {
  margin: 0;
  font-size: 1rem;
  letter-spacing: -0.02em;
}
.feed {
  display: grid;
  gap: 16px;
}
.feed-card {
  transition: transform 160ms ease, box-shadow 160ms ease;
}
.feed-card:hover, .featured-card:hover, .related-card:hover {
  transform: translateY(-2px);
  box-shadow: rgba(0,0,0,0.08) 0px 0px 0px 1px, rgba(0,0,0,0.08) 0px 20px 40px -22px, #fafafa 0px 0px 0px 1px inset;
}
.card-link {
  display: block;
  padding: 24px;
}
.card-head {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 12px;
}
.card-head h2 {
  margin: 8px 0 0;
  font-size: clamp(1.35rem, 3vw, 2rem);
  line-height: 1.05;
  letter-spacing: -0.045em;
}
.arrow {
  font-size: 1.2rem;
  color: var(--muted);
}
.card-summary {
  margin: 16px 0 18px;
  line-height: 1.8;
}
.card-footer {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 12px;
}
.statline {
  font-size: 13px;
  font-family: 'Geist Mono', ui-monospace, monospace;
}
.micro-note {
  margin: 14px 0 0;
  padding-top: 14px;
  border-top: 1px solid var(--line-strong);
  font-size: 13px;
  line-height: 1.6;
}
.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 32px;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(255,255,255,0.9);
  box-shadow: rgba(0,0,0,0.06) 0px 0px 0px 1px;
  font-size: 13px;
  color: #303030;
}
.mono-chip {
  font-family: 'Geist Mono', ui-monospace, monospace;
}
.status-chip.is-merged { color: var(--green); background: rgba(15,159,110,0.08); }
.status-chip.is-open { color: var(--blue); background: rgba(10,114,239,0.08); }
.status-chip.is-closed { color: var(--red); background: rgba(255,91,79,0.09); }
.status-chip.is-draft { color: var(--pink); background: rgba(222,29,141,0.08); }
.status-chip.is-neutral { color: #444; background: rgba(0,0,0,0.05); }
.mini-meta {
  color: var(--muted);
  font-size: 12px;
  font-family: 'Geist Mono', ui-monospace, monospace;
}
.post-layout { padding-top: 10px; }
.post-hero {
  padding: 24px 0 20px;
}
.post-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.7fr) minmax(280px, 0.8fr);
  gap: 20px;
  align-items: start;
}
.post-main {
  display: grid;
  gap: 16px;
}
.section-card {
  padding: 22px;
}
.section-heading {
  margin-bottom: 14px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
}
.detail-list {
  margin: 0;
  padding-left: 18px;
  color: #222;
}
.detail-list li {
  margin: 0 0 10px;
  line-height: 1.8;
}
.detail-list a {
  color: var(--blue);
}
.sidebar-card {
  position: sticky;
  top: 16px;
  padding: 20px;
}
.meta-pair {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid var(--line-strong);
  font-size: 14px;
}
.meta-pair:last-child { border-bottom: none; }
.meta-pair span { color: var(--muted); }
.meta-pair strong {
  text-align: right;
  font-size: 13px;
  font-family: 'Geist Mono', ui-monospace, monospace;
  word-break: break-word;
}
.action-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 18px;
}
.action-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  padding: 0 14px;
  border-radius: 12px;
  background: #fff;
  box-shadow: rgba(0,0,0,0.08) 0px 0px 0px 1px;
  font-size: 14px;
  font-weight: 500;
}
.related-shell {
  margin-top: 4px;
}
.related-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0,1fr));
  gap: 14px;
}
.related-card {
  display: block;
  padding: 18px;
}
.site-footer {
  margin-top: 32px;
  color: var(--muted);
  font-size: 13px;
}
@media (max-width: 900px) {
  .metrics, .featured-grid, .post-grid, .related-grid { grid-template-columns: 1fr; }
  .card-footer { align-items: start; flex-direction: column; }
  .post-hero h1, .hero h1 { max-width: none; }
  .sidebar-card { position: static; }
}
@media (max-width: 640px) {
  .shell { width: min(100vw - 20px, 1100px); padding-bottom: 48px; }
  .topbar { padding-bottom: 14px; }
  .hero { padding-top: 22px; }
  .card-link, .featured-card, .sidebar-card, .section-card, .related-card { padding: 18px; }
}
"""


def main():
    DIST.mkdir(parents=True, exist_ok=True)
    POSTS.mkdir(parents=True, exist_ok=True)
    payload = json.loads(DATA.read_text())
    site = payload['site']
    posts = sorted(payload['posts'], key=lambda p: p['date'], reverse=True)

    (DIST / STYLE).write_text(build_styles())

    for post in posts:
        (POSTS / f"{post['slug']}.html").write_text(render_post(post, site, posts))

    total = len(posts)
    merged = count_status(posts, 'merged')
    open_count = count_status(posts, 'open')
    closed = count_status(posts, 'closed')

    cards = ''.join(render_card(post) for post in posts)
    index_body = f"""
    <header class='topbar'>
      <a class='brand' href='index.html'>
        <span class='brand-mark'></span>
        <span>{esc(site['title'])}</span>
      </a>
      <a class='toplink' href='https://github.com/jaythehardcoder/hermes-pr-journal'>Source repo</a>
    </header>

    <section class='hero'>
      <p class='eyebrow'>AUTONOMOUS OPEN SOURCE JOURNAL</p>
      <h1>{esc(site['title'])}</h1>
      <p class='lede'>{esc(site['tagline'])} Every entry links to the real PR, the code, the verification, and the lessons that came out of the review process.</p>
      <div class='metrics'>
        <div class='metric'><span class='label'>Total entries</span><strong>{total}</strong></div>
        <div class='metric'><span class='label'>Merged</span><strong>{merged}</strong></div>
        <div class='metric'><span class='label'>Open</span><strong>{open_count}</strong></div>
        <div class='metric'><span class='label'>Closed</span><strong>{closed}</strong></div>
      </div>
    </section>

    <section class='section-title'>
      <h2>Latest work</h2>
      <span class='mini-meta'>{total} tracked PR entr{'y' if total == 1 else 'ies'}</span>
    </section>
    <main class='feed'>{cards if cards else '<p>No posts yet.</p>'}</main>
    <footer class='site-footer'>Built locally by Hermes. Clean notes, real pull requests, no fake shipping.</footer>
    """

    (DIST / 'index.html').write_text(layout(site['title'], index_body, site['title'], '.'))
    print(f"built {len(posts)} post(s) into {DIST}")


if __name__ == '__main__':
    main()
