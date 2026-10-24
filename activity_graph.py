"""Draw a 31-day contribution activity graph as SVG (light and dark).

Reads public contribution counts from the GitHub GraphQL API, so the graph
is generated inside this repo and never depends on a third-party image host.

Usage: GH_TOKEN=... python activity_graph.py <username> <output_dir>
"""
import datetime as dt
import json
import os
import sys
import urllib.request

DAYS = 31
W, H = 900, 300
PAD_L, PAD_R, PAD_T, PAD_B = 56, 24, 56, 44

THEMES = {
    "activity-graph.svg": dict(bg="#ffffff", fg="#1f2328", muted="#656d76", grid="#d0d7de", line="#0969da", area="#0969da", dot="#0969da"),
    "activity-graph-dark.svg": dict(bg="#1a1b27", fg="#c0caf5", muted="#787c99", grid="#2a2e45", line="#7aa2f7", area="#7aa2f7", dot="#bb9af7"),
}


def fetch(user, token):
    to = dt.datetime.now(dt.timezone.utc).replace(hour=23, minute=59, second=59, microsecond=0)
    frm = (to - dt.timedelta(days=DAYS - 1)).replace(hour=0, minute=0, second=0)
    query = """query($u:String!,$f:DateTime!,$t:DateTime!){user(login:$u){
      contributionsCollection(from:$f,to:$t){contributionCalendar{
        weeks{contributionDays{date contributionCount}}}}}}"""
    body = json.dumps({"query": query, "variables": {"u": user, "f": frm.isoformat(), "t": to.isoformat()}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body,
                                 headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GraphQL error: {data['errors']}")
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = [(d["date"], d["contributionCount"]) for w in weeks for d in w["contributionDays"]]
    return days[-DAYS:]


def nice_max(v):
    """Smallest round axis top (4 gridline steps of 1, 2, 5, 10, 20, 50, ...) that fits v."""
    mag = 1
    while True:
        for m in (1, 2, 5):
            if 4 * m * mag >= v:
                return 4 * m * mag
        mag *= 10


def render(days, t, user):
    counts = [c for _, c in days]
    top = nice_max(max(counts) if counts else 0)
    pw, ph = W - PAD_L - PAD_R, H - PAD_T - PAD_B
    n = len(days)
    xs = [PAD_L + (pw * i / (n - 1) if n > 1 else pw / 2) for i in range(n)]
    ys = [PAD_T + ph - (c / top) * ph for c in counts]
    base = PAD_T + ph

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
           f'aria-label="{user} contribution activity, last {DAYS} days">',
           f'<rect width="{W}" height="{H}" rx="8" fill="{t["bg"]}"/>',
           '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}</style>',
           f'<text x="{W/2}" y="32" text-anchor="middle" font-size="18" font-weight="600" fill="{t["fg"]}">'
           f'{user}\'s contribution graph — last {DAYS} days ({sum(counts)} contributions)</text>']

    for i in range(5):  # gridlines + y labels
        v = top * i / 4
        y = base - ph * i / 4
        out.append(f'<line x1="{PAD_L}" x2="{W-PAD_R}" y1="{y:.1f}" y2="{y:.1f}" stroke="{t["grid"]}" stroke-width="1"/>')
        out.append(f'<text x="{PAD_L-10}" y="{y+4:.1f}" text-anchor="end" font-size="12" fill="{t["muted"]}">{v:g}</text>')

    for i, (date, _) in enumerate(days):  # x labels every 5 days
        if i % 5 == 0 or i == n - 1:
            d = dt.date.fromisoformat(date)
            out.append(f'<text x="{xs[i]:.1f}" y="{H-18}" text-anchor="middle" font-size="12" fill="{t["muted"]}">{d.day} {d.strftime("%b")}</text>')

    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    out.append(f'<polygon points="{xs[0]:.1f},{base} {pts} {xs[-1]:.1f},{base}" fill="{t["area"]}" fill-opacity="0.18"/>')
    out.append(f'<polyline points="{pts}" fill="none" stroke="{t["line"]}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')
    for (date, c), x, y in zip(days, xs, ys):
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{t["dot"]}"><title>{date}: {c}</title></circle>')
    out.append(f'<text x="{PAD_L}" y="{H-2}" font-size="11" fill="{t["muted"]}">Contributions per day · updated {dt.date.today().isoformat()}</text>')
    out.append("</svg>")
    return "\n".join(out)


def main():
    user, out_dir = sys.argv[1], sys.argv[2]
    days = fetch(user, os.environ["GH_TOKEN"]) if os.environ.get("GH_TOKEN") else json.load(open(os.environ["SAMPLE"]))
    os.makedirs(out_dir, exist_ok=True)
    for name, theme in THEMES.items():
        with open(os.path.join(out_dir, name), "w") as f:
            f.write(render(days, theme, user))
    print(f"Wrote {len(THEMES)} graphs for {user}: {sum(c for _, c in days)} contributions over {len(days)} days")


if __name__ == "__main__":
    main()
