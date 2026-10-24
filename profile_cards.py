"""Generate the profile's stats, streak and repository cards as SVG (light and dark).

Replaces third-party card services (github-readme-stats, streak-stats, trophies)
that often time out with "upstream" errors. Everything is drawn here from the
GitHub GraphQL API and published to the "output" branch by the workflow.

Usage: GH_TOKEN=... python profile_cards.py <username> <output_dir> [repo ...]
"""
import datetime as dt
import json
import os
import sys
import textwrap
import urllib.request
from xml.sax.saxutils import escape

THEMES = {
    "": dict(bg="#ffffff", border="#d0d7de", title="#0969da", fg="#1f2328", muted="#656d76", accent="#8250df", icon="#0969da"),
    "-dark": dict(bg="#1a1b27", border="#2a2e45", title="#7aa2f7", fg="#c0caf5", muted="#787c99", accent="#bb9af7", icon="#7dcfff"),
}
FONT = '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}</style>'

QUERY = """query($u:String!){user(login:$u){
  name login followers{totalCount}
  repositories(ownerAffiliations:OWNER, privacy:PUBLIC, isFork:false, first:100){
    totalCount nodes{name description stargazerCount forkCount primaryLanguage{name color}}}
  contributionsCollection{
    totalCommitContributions totalPullRequestContributions totalIssueContributions
    contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""


def fetch(user, token):
    body = json.dumps({"query": QUERY, "variables": {"u": user}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-cards"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("errors") or not (data.get("data") or {}).get("user"):
        raise RuntimeError(f"GraphQL returned no data: {data.get('errors')}")
    return data["data"]["user"]


def streaks(days, today):
    """(current, current_start, longest, longest_start, longest_end) from [(date, count)]."""
    days = sorted((dt.date.fromisoformat(d), c) for d, c in days if dt.date.fromisoformat(d) <= today)
    longest = (0, None, None)
    run, start = 0, None
    for d, c in days:
        if c > 0:
            run, start = run + 1, start or d
            if run > longest[0]:
                longest = (run, start, d)
        else:
            run, start = 0, None
    # current streak: ends today, or yesterday if nothing yet today
    current, cur_start = 0, None
    seq = list(reversed(days))
    if seq and seq[0][0] == today and seq[0][1] == 0:
        seq = seq[1:]
    for d, c in seq:
        if c == 0:
            break
        current, cur_start = current + 1, d
    return current, cur_start, longest[0], longest[1], longest[2]


def icon(kind, x, y, color):
    """Small drawn icons (no font glyphs, so they render the same everywhere)."""
    c, s = color, f'stroke="{color}" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    shapes = {
        "star": f'<path d="M7 1l1.8 3.8 4.2.5-3.1 2.9.8 4.1L7 10.3 3.3 12.3l.8-4.1L1 5.3l4.2-.5z" fill="{c}"/>',
        "commit": f'<circle cx="7" cy="7" r="3" {s}/><path d="M0 7h4M10 7h4" {s}/>',
        "pr": f'<circle cx="3" cy="3" r="2" {s}/><circle cx="3" cy="11" r="2" {s}/><circle cx="11" cy="11" r="2" {s}/>'
              f'<path d="M3 5v4M11 9V5.5Q11 3 8.5 3H7" {s}/>',
        "issue": f'<circle cx="7" cy="7" r="6" {s}/><circle cx="7" cy="7" r="1.6" fill="{c}"/>',
        "repo": f'<path d="M3 1.5h8.5v11H3.5A1.5 1.5 0 0 1 2 11V3a1.5 1.5 0 0 1 1-1.5zM2 11a1.5 1.5 0 0 1 1.5-1.5h8" {s}/>',
        "people": f'<circle cx="7" cy="4.5" r="3" {s}/><path d="M1.5 13a5.5 5.5 0 0 1 11 0" {s}/>',
        "fork": f'<circle cx="3" cy="2.5" r="1.8" {s}/><circle cx="11" cy="2.5" r="1.8" {s}/><circle cx="7" cy="11.5" r="1.8" {s}/>'
                f'<path d="M3 4.3v1.2Q3 7 4.5 7h5Q11 7 11 5.5V4.3M7 7v2.7" {s}/>',
        "flame": f'<path d="M7 0.5C8 3 11.5 5 11.5 8.8A4.5 4.5 0 0 1 2.5 8.8C2.5 6.5 4 5.5 4.5 3.5 5.5 5 6 5.5 6.6 5.8 6.8 4 6.5 2 7 0.5z" fill="{c}"/>',
    }
    return f'<g transform="translate({x} {y})">{shapes[kind]}</g>'


def fmt_date(d):
    return f"{d.day} {d.strftime('%b')}" if d else ""


def frame(w, h, t, label, inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-label="{escape(label)}">{FONT}'
            f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="8" fill="{t["bg"]}" stroke="{t["border"]}"/>'
            f'{inner}</svg>')


def stats_card(u, t):
    cc = u["contributionsCollection"]
    stars = sum(r["stargazerCount"] for r in u["repositories"]["nodes"])
    rows = [("star", "Total stars", stars),
            ("commit", "Commits (last 12 months)", cc["totalCommitContributions"]),
            ("pr", "Pull requests", cc["totalPullRequestContributions"]),
            ("issue", "Issues", cc["totalIssueContributions"]),
            ("repo", "Public repositories", u["repositories"]["totalCount"]),
            ("people", "Followers", u["followers"]["totalCount"])]
    name = u.get("name") or u["login"]
    out = [f'<text x="25" y="35" font-size="18" font-weight="600" fill="{t["title"]}">{escape(name)}\'s GitHub stats</text>']
    for i, (kind, label, value) in enumerate(rows):
        y = 68 + i * 22
        out.append(icon(kind, 25, y - 12, t["icon"]) +
                   f'<text x="48" y="{y}" font-size="14" fill="{t["fg"]}">{label}</text>'
                   f'<text x="300" y="{y}" font-size="14" font-weight="700" fill="{t["fg"]}" text-anchor="end">{value:,}</text>')
    total = cc["contributionCalendar"]["totalContributions"]
    out.append(f'<circle cx="405" cy="105" r="48" fill="none" stroke="{t["border"]}" stroke-width="6"/>'
               f'<circle cx="405" cy="105" r="48" fill="none" stroke="{t["accent"]}" stroke-width="6" stroke-linecap="round" '
               f'stroke-dasharray="{min(total, 365) / 365 * 301.6:.1f} 301.6" transform="rotate(-90 405 105)"/>'
               f'<text x="405" y="108" font-size="22" font-weight="700" fill="{t["fg"]}" text-anchor="middle">{total:,}</text>'
               f'<text x="405" y="126" font-size="11" fill="{t["muted"]}" text-anchor="middle">contributions</text>'
               f'<text x="405" y="174" font-size="11" fill="{t["muted"]}" text-anchor="middle">last 12 months</text>')
    return frame(495, 200, t, f"{name} GitHub stats", "".join(out))


def streak_card(u, t, today):
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
    cur, cur_start, best, best_start, best_end = streaks(days, today)
    cols = [(82, f'{cal["totalContributions"]:,}', "Total contributions", "last 12 months"),
            (247, str(cur), "Current streak", f"{fmt_date(cur_start)} – {fmt_date(today)}" if cur else "start one today"),
            (412, str(best), "Longest streak", f"{fmt_date(best_start)} – {fmt_date(best_end)}" if best else "—")]
    out = []
    for i, (x, big, label, sub) in enumerate(cols):
        hi = i == 1
        if hi:
            out.append(f'<circle cx="{x}" cy="78" r="40" fill="none" stroke="{t["accent"]}" stroke-width="5"/>'
                       + icon("flame", x - 7, 17, t["accent"]))
        out.append(f'<text x="{x}" y="{88 if hi else 86}" font-size="28" font-weight="700" fill="{t["accent"] if hi else t["fg"]}" text-anchor="middle">{big}</text>'
                   f'<text x="{x}" y="145" font-size="14" font-weight="600" fill="{t["fg"]}" text-anchor="middle">{label}</text>'
                   f'<text x="{x}" y="166" font-size="12" fill="{t["muted"]}" text-anchor="middle">{sub}</text>')
    out.append(f'<line x1="165" x2="165" y1="30" y2="170" stroke="{t["border"]}"/><line x1="330" x2="330" y1="30" y2="170" stroke="{t["border"]}"/>')
    return frame(495, 200, t, "GitHub contribution streak", "".join(out))


def wrap(text, width, lines):
    return textwrap.wrap(text or "No description provided", width, max_lines=lines, placeholder="…")


def repo_card(r, t, user):
    desc = wrap(r.get("description"), 52, 2)
    out = [icon("repo", 25, 23, t["icon"]) +
           f'<text x="45" y="35" font-size="16" font-weight="600" fill="{t["title"]}">{escape(r["name"])}</text>']
    for i, line in enumerate(desc):
        out.append(f'<text x="25" y="{62 + i * 18}" font-size="13" fill="{t["muted"]}">{escape(line)}</text>')
    x = 25
    lang = r.get("primaryLanguage")
    if lang:
        out.append(f'<circle cx="{x + 6}" cy="104" r="6" fill="{lang.get("color") or t["muted"]}"/>'
                   f'<text x="{x + 18}" y="109" font-size="13" fill="{t["fg"]}">{escape(lang["name"])}</text>')
        x += 30 + 8 * len(lang["name"])
    out.append(icon("star", x, 97, t["fg"]) + f'<text x="{x + 19}" y="109" font-size="13" fill="{t["fg"]}">{r["stargazerCount"]}</text>'
               + icon("fork", x + 55, 97, t["fg"]) + f'<text x="{x + 74}" y="109" font-size="13" fill="{t["fg"]}">{r["forkCount"]}</text>')
    return frame(400, 125, t, f"{user}/{r['name']} repository", "".join(out))


def placeholder(w, h, t, label):
    return frame(w, h, t, label, f'<text x="{w/2}" y="{h/2 - 4}" font-size="15" font-weight="600" fill="{t["fg"]}" text-anchor="middle">{escape(label)}</text>'
                                 f'<text x="{w/2}" y="{h/2 + 18}" font-size="12" fill="{t["muted"]}" text-anchor="middle">Data temporarily unavailable · retrying at the next daily run</text>')


def main():
    user, out_dir, repos = sys.argv[1], sys.argv[2], sys.argv[3:]
    os.makedirs(out_dir, exist_ok=True)
    today = dt.datetime.now(dt.timezone.utc).date()
    files = {}
    try:
        u = json.load(open(os.environ["SAMPLE"])) if os.environ.get("SAMPLE") else fetch(user, os.environ.get("GH_TOKEN", ""))
        by_name = {r["name"].lower(): r for r in u["repositories"]["nodes"]}
        for sfx, t in THEMES.items():
            files[f"stats{sfx}.svg"] = stats_card(u, t)
            files[f"streak{sfx}.svg"] = streak_card(u, t, today)
            for name in repos:
                r = by_name.get(name.lower())
                files[f"repo-{name}{sfx}.svg"] = repo_card(r, t, user) if r else placeholder(400, 125, t, name)
        summary = "from live data"
    except Exception as e:  # noqa: BLE001 - never fail the job
        print(f"::warning::Profile card data unavailable, writing placeholders: {e}")
        for sfx, t in THEMES.items():
            files[f"stats{sfx}.svg"] = placeholder(495, 200, t, "GitHub stats")
            files[f"streak{sfx}.svg"] = placeholder(495, 200, t, "Contribution streak")
            for name in repos:
                files[f"repo-{name}{sfx}.svg"] = placeholder(400, 125, t, name)
        summary = "as placeholders"
    for name, svg in files.items():
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write(svg)
    print(f"Wrote {len(files)} cards {summary}: {', '.join(sorted(files))}")


if __name__ == "__main__":
    main()
