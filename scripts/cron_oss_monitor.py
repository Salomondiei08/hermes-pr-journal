#!/usr/bin/env python3
"""
Cron monitor for Jay's OSS contribution workflow.

- Checks GitHub API state for every PR in data/tracked_prs.json.
- Compares against data/monitor_state.json (fingerprint baseline).
- Updates data/site.json with a short `updates` entry for each meaningful
  change (new comments/reviews, pushes, CI changes, state transitions).
- Rebuilds and deploys the site only when something actually changed.
- Also checks Himalaya for new GitHub notification emails; if any new IDs are
  seen they are recorded in monitor_state.json.
"""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TRACKED = DATA / "tracked_prs.json"
SITE = DATA / "site.json"
MONITOR = DATA / "monitor_state.json"
LAST_STATE = DATA / "last_checked_pr_state.json"
ENV = Path.home() / ".hermes" / ".env"

_NOW = datetime.now(timezone.utc)
_NOW_STR = _NOW.strftime("%Y-%m-%dT%H:%M:%SZ")


def github_token():
    for key in ("GITHUB_TOKEN", "GH_TOKEN"):
        v = os.environ.get(key)
        if v:
            return v.strip()
    if ENV.exists():
        for line in ENV.read_text(errors="ignore").splitlines():
            if line.startswith("GITHUB_TOKEN=") or line.startswith("COPILOT_GITHUB_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    creds = Path.home() / ".git-credentials"
    if creds.exists():
        for line in creds.read_text(errors="ignore").splitlines():
            m = re.search(r":(gh[pousr]_[a-zA-Z0-9]+)@github\.com", line)
            if m:
                return m.group(1)
    return None


TOKEN = github_token()


def fetch_json(url):
    if not TOKEN:
        raise RuntimeError("missing GitHub token")
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "jay-oss-monitor",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def get_json_list(url):
    """Fetch multiple pages and return concatenated items."""
    items = []
    page = 1
    while True:
        paged_url = f"{url}{'&' if '?' in url else '?'}page={page}&per_page=100"
        batch = fetch_json(paged_url)
        if not batch:
            break
        if not isinstance(batch, list):
            break
        items.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return items


def pr_fingerprint(pr, comments, reviews, review_comments, check_runs, commit_statuses):
    labels = sorted({l.get("name", "") for l in pr.get("labels", [])})
    comment_ids = sorted({c.get("id") for c in comments})
    review_ids_states = sorted([list(t) for t in {(r.get("id"), r.get("state")) for r in reviews}])
    review_comment_ids = sorted({c.get("id") for c in review_comments})
    checks = sorted([list(t) for t in {(r.get("name"), r.get("status"), r.get("conclusion")) for r in check_runs}])
    statuses = sorted([list(t) for t in {(s.get("context"), s.get("state"), s.get("target_url")) for s in commit_statuses}])
    return {
        "state": pr.get("state"),
        "draft": pr.get("draft"),
        "merged_at": pr.get("merged_at"),
        "closed_at": pr.get("closed_at"),
        "head_sha": pr.get("head", {}).get("sha"),
        "labels": labels,
        "comment_ids": comment_ids,
        "review_ids_states": review_ids_states,
        "review_comment_ids": review_comment_ids,
        "checks": checks,
        "statuses": statuses,
    }


def semantic_reviews(reviews, review_comments):
    sem = []
    for r in reviews:
        body = (r.get("body") or "").strip()
        if not body and r.get("state") == "APPROVED":
            body = "approved this PR"
        sem.append({
            "id": r.get("id"),
            "state": r.get("state"),
            "user": (r.get("user") or {}).get("login"),
            "body": body[:500],
        })
    return sem


def fetch_pr_bundle(owner, repo, num):
    pr = fetch_json(f"https://api.github.com/repos/{owner}/{repo}/pulls/{num}")
    sha = pr.get("head", {}).get("sha")
    comments = get_json_list(f"https://api.github.com/repos/{owner}/{repo}/issues/{num}/comments?per_page=100")
    reviews = get_json_list(f"https://api.github.com/repos/{owner}/{repo}/pulls/{num}/reviews?per_page=100")
    review_comments = get_json_list(f"https://api.github.com/repos/{owner}/{repo}/pulls/{num}/comments?per_page=100")
    commit_statuses = fetch_json(f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}/status")
    checks = fetch_json(f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}/check-runs?per_page=100")
    return pr, comments, reviews, review_comments, commit_statuses, checks


def diff_fingerprint(prev, cur):
    """Return human-readable reasons for fingerprint change."""
    reasons = []
    if prev.get("state") != cur.get("state"):
        reasons.append(f"state {prev.get('state')} -> {cur.get('state')}")
    if prev.get("draft") != cur.get("draft"):
        reasons.append(f"draft {prev.get('draft')} -> {cur.get('draft')}")
    if prev.get("merged_at") != cur.get("merged_at"):
        changed = "merged now" if cur.get("merged_at") else "un-merged"
        reasons.append(changed)
    if prev.get("closed_at") != cur.get("closed_at"):
        changed = "closed now" if cur.get("closed_at") else "reopened"
        reasons.append(changed)
    if prev.get("head_sha") != cur.get("head_sha"):
        reasons.append("new push")
    if prev.get("labels") != cur.get("labels"):
        reasons.append(f"labels {prev.get('labels')} -> {cur.get('labels')}")
    if prev.get("comment_ids") != cur.get("comment_ids"):
        added = set(cur.get("comment_ids", [])) - set(prev.get("comment_ids", []))
        reasons.append(f"{len(added)} new comment(s)")
    if prev.get("review_ids_states") != cur.get("review_ids_states"):
        prev_by_id = {r[0]: r[1] for r in prev.get("review_ids_states", [])}
        cur_by_id = {r[0]: r[1] for r in cur.get("review_ids_states", [])}
        added = [cur_by_id[i] for i in set(cur_by_id) - set(prev_by_id)]
        changed = [cur_by_id[i] for i in set(cur_by_id) & set(prev_by_id) if prev_by_id[i] != cur_by_id[i]]
        labels = []
        if added:
            labels.append(f"{len(added)} new review(s): {', '.join(sorted(set(added)))}")
        if changed:
            labels.append(f"{len(changed)} review state change(s)")
        reasons.extend(labels)
    if prev.get("review_comment_ids") != cur.get("review_comment_ids"):
        added = set(cur.get("review_comment_ids", [])) - set(prev.get("review_comment_ids", []))
        reasons.append(f"{len(added)} new review comment(s)")
    if prev.get("checks") != cur.get("checks"):
        reasons.append("check runs changed")

    prev_statuses = sorted({(s[0], s[1]) for s in prev.get("statuses", []) if len(s) >= 2})
    cur_statuses = sorted({(s[0], s[1]) for s in cur.get("statuses", []) if len(s) >= 2})
    if prev_statuses != cur_statuses:
        reasons.append("commit statuses changed")
    return reasons


def state_from_pr(pr):
    if pr.get("merged_at"):
        return "merged"
    return pr.get("state", "unknown")


def update_site_post(site, slug, repo, pr_num, current_state, reasons):
    for post in site.get("posts", []):
        if post.get("slug") == slug or (post.get("repo") == repo and post.get("pr_number") == pr_num):
            post["status"] = current_state
            post["last_updated"] = _NOW_STR
            existing = post.get("updates")
            if not isinstance(existing, list):
                post["updates"] = []
            summary = "; ".join(reasons)
            if "review" in summary.lower() or "approved" in summary.lower() or "comment" in summary.lower():
                category = "Discussion/review activity"
            elif "merged" in summary.lower() or "closed" in summary.lower() or "state" in summary.lower():
                category = "State transition"
            elif "check" in summary.lower() or "status" in summary.lower() or "ci" in summary.lower():
                category = "CI update"
            elif "push" in summary.lower():
                category = "New commits"
            else:
                category = "PR update"
            post["updates"].append({
                "date": _NOW_STR,
                "summary": f"{category}: {summary}.",
            })
            return True
    return False


def run_himalaya_and_find_new_email_ids(previously_processed):
    """Return new GitHub notification IDs not in previously_processed."""
    import subprocess
    new_ids = []
    try:
        with open("/tmp/inbox_monitor.json", "w") as out, open("/tmp/inbox_monitor.err", "w") as err:
            subprocess.run(
                ["himalaya", "envelope", "list", "--page-size", "100", "--output", "json"],
                stdout=out,
                stderr=err,
                timeout=60,
            )
        data = json.loads(Path("/tmp/inbox_monitor.json").read_text())
    except Exception:
        return []
    proc_set = {str(x) for x in previously_processed}
    for m in data:
        sender = (m.get("from") or {}).get("addr", "")
        if sender == "notifications@github.com":
            mid = str(m.get("id"))
            if mid and mid not in proc_set:
                new_ids.append(mid)
    return sorted(new_ids, key=int)


def main():
    if not TOKEN:
        print("ERROR: missing GitHub token", file=sys.stderr)
        sys.exit(1)

    tracked = json.loads(TRACKED.read_text())["tracked_prs"]
    site = json.loads(SITE.read_text()) if SITE.exists() else {"posts": []}
    monitor = json.loads(MONITOR.read_text()) if MONITOR.exists() else {"prs": {}}
    previous_prs = monitor.get("prs", {})

    new_prs_state = {}
    meaningful_changes = []

    for item in tracked:
        slug = item["slug"]
        owner = item["owner"]
        repo = item["repo"]
        num = item["pr_number"]
        repo_key = f"{owner}/{repo}"
        pr_full_slug = f"{repo_key}#{num}"

        pr, comments, reviews, review_comments, commit_statuses, checks = fetch_pr_bundle(owner, repo, num)
        fp = pr_fingerprint(pr, comments, reviews, review_comments, checks.get("check_runs", []), commit_statuses.get("statuses", []))

        new_prs_state[slug] = {
            "state": fp["state"],
            "merged": bool(pr.get("merged_at")),
            "head_sha": pr.get("head", {}).get("sha"),
            "comments_count": len(comments),
            "review_comments_count": len(review_comments),
            "labels": fp["labels"],
            "locked": pr.get("locked"),
            "draft": pr.get("draft"),
            "fingerprint": fp,
            "_reviews_semantic": semantic_reviews(reviews, review_comments),
            "merge_commit_sha": pr.get("merge_commit_sha"),
        }

        prev = previous_prs.get(slug)
        if prev is None:
            # First time we're tracking this PR in this snapshot style.
            # Don't treat backfilling as a meaningful change.
            continue

        reasons = diff_fingerprint(prev.get("fingerprint", {}), fp)
        if reasons:
            current_state = state_from_pr(pr)
            updated = update_site_post(site, slug, f"{owner}/{repo}", num, current_state, reasons)
            meaningful_changes.append({
                "slug": slug,
                "pr": pr_full_slug,
                "state": current_state,
                "reasons": reasons,
                "site_updated": updated,
            })

    # Himalaya email check (record only new GitHub notification IDs).
    previously_processed = monitor.get("processed_email_ids", [])
    new_email_ids = run_himalaya_and_find_new_email_ids(previously_processed)
    if new_email_ids:
        monitor["processed_email_ids"] = sorted(
            {str(x) for x in previously_processed} | set(new_email_ids),
        )
        meaningful_changes.append({
            "event": "new_github_emails",
            "ids": new_email_ids,
        })

    # Always refresh monitor state with current data.
    monitor["prs"] = new_prs_state
    monitor["generated_at"] = _NOW_STR
    MONITOR.write_text(json.dumps(monitor, indent=2) + "\n")

    # Keep last_checked_pr_state.json consistent with a smaller snapshot.
    last_state = {"_meta": {"last_checked": _NOW_STR}}
    for slug, state in new_prs_state.items():
        fp = state.get("fingerprint", {})
        last_state[slug] = {
            "state": state["state"],
            "merged": state["merged"],
            "closed_at": fp.get("closed_at"),
            "merged_at": fp.get("merged_at"),
            "head_sha": state["head_sha"],
            "comments": state["comments_count"],
            "review_comments": state["review_comments_count"],
            "labels": fp.get("labels", []),
            "locked": state["locked"],
            "draft": state["draft"],
            "checks": fp.get("checks", []),
            "statuses": fp.get("statuses", []),
        }
    LAST_STATE.write_text(json.dumps(last_state, indent=2) + "\n")

    # If any meaningful changes, persist site.json and rebuild/deploy.
    if meaningful_changes:
        SITE.write_text(json.dumps(site, indent=2) + "\n")

    msg = {
        "email_new_ids": new_email_ids,
        "meaningful_changes": meaningful_changes,
        "generated_at": _NOW_STR,
    }
    print(json.dumps(msg, indent=2))

    # Exit non-zero to make a shell wrapper skip rebuild?  We'll return data instead.
    return msg


if __name__ == "__main__":
    main()
