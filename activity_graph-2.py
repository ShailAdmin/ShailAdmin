"""Draw a 31-day contribution activity graph as SVG (light and dark).

Reads public contribution counts from the GitHub GraphQL API, so the graph
is generated inside this repo and never depends on a third-party image host.

Usage: GH_TOKEN=... python activity_graph.py <username> <output_dir>
"""
import datetime as dt
import json
import os
import re
import sys
import urllib.request

DAYS = 31
W, H = 900, 300
PAD_L, PAD_R, PAD_T, PAD_B = 56, 24, 56, 44

THEMES = {
    "activity-graph.svg": dict(bg="#ffffff", fg="#1f2328", muted="#656d76", grid="#d0d7de", line="#0969da", area="#0969da", dot="#0969da"),
    "activity-graph-dark.svg": dict(bg="#1a1b27", fg="#c0caf5", muted="#787c99", grid="#2a2e45", line="#7aa2f7", area="#7aa2f7", dot="#bb9af7"),
}


def fetch_graphql(user, token):
    """Contribution counts from the GraphQL API (needs a token)."""
    to = dt.datetime.now(dt.timezone.utc).replace(hour=23, minute=59, second=59, microsecond=0)
    frm = (to - dt.timedelta(days=DAYS - 1)).replace(hour=0, minute=0, second=0)
    query = """query($u:String!,$f:DateTime!,$t:DateTime!){user(login:$u){
      contributionsCollection(from:$f,to:$t){contributionCalendar{
        weeks{contributionDays{date contributionCount}}}}}}"""
    body = json.dumps({"query": query, "variables": {"u": user, "f": frm.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                                     "t": to.strftime("%Y-%m-%dT%H:%M:%SZ")}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "activity-graph"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("errors") or not (data.get("data") or {}).get("user"):
        raise RuntimeError(f"GraphQL returned no data: {data.get('errors')}")
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [(d["date"], d["contributionCount"]) for w in weeks for d in w["contributionDays"]]


def parse_contributions_html(html):
    """Parse GitHub's public contributions calendar HTML into [(date, count)]."""
    id_to_date = {}
    for cell in re.findall(r"<td\b[^>]*\bdata-date=[^>]*>", html):  # one calendar day per cell
        date = re.search(r'data-date="(\d{4}-\d{2}-\d{2})"', cell)
        cid = re.search(r'\bid="([^"]+)"', cell)
        if date and cid:
            id_to_date[cid.group(1)] = date.group(1)
    days = {}
    for tip_for, text in re.findall(r'<tool-tip[^>]*\bfor="([^"]+)"[^>]*>([^<]*)</tool-tip>', html):
        if tip_for in id_to_date:
            m = re.match(r"\s*([\d,]+)\s+contribution", text)
            days[id_to_date[tip_for]] = int(m.group(1).replace(",", "")) if m else 0
    for d in id_to_date.values():  # days without a tooltip count as zero
        days.setdefault(d, 0)
    return sorted(days.items())


def fetch_public_page(user):
    """Contribution counts from the public profile calendar (no token needed)."""
    req = urllib.request.Request(f"https://github.com/users/{user}/contributions",
                                 headers={"User-Agent": "Mozilla/5.0 activity-graph"})
    with urllib.request.urlopen(req, timeout=30) as r:
        days = parse_contributions_html(r.read().decode("utf-8", "replace"))
    if not days:
        raise RuntimeError("contributions page had no calendar data")
    return days


def fetch(user, token):
    """Try the API first, then the public page. Returns the last DAYS days ending today."""
    errors = []
    sources = [("public contributions page", lambda: fetch_public_page(user))]
    if token:
        sources.insert(0, ("GraphQL API", lambda: fetch_graphql(user, token)))
    for name, fn in sources:
        try:
            days = fn()
            print(f"Fetched {len(days)} days from the {name}")
            break
        except Exception as e:  # noqa: BLE001 - report and try the next source
            errors.append(f"{name}: {e}")
            print(f"::warning::Could not read contributions from the {name}: {e}")
    else:
        raise RuntimeError("; ".join(errors))
    today = dt.datetime.now(dt.timezone.utc).date()
    by_date = dict(days)
    return [((today - dt.timedelta(days=i)).isoformat(),
             by_date.get((today - dt.timedelta(days=i)).isoformat(), 0)) for i in range(DAYS - 1, -1, -1)]


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


def render_unavailable(t, user, reason):
    """Placeholder card so the README shows a clear message instead of a broken image."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
            f'aria-label="{user} contribution activity unavailable">'
            f'<rect width="{W}" height="{H}" rx="8" fill="{t["bg"]}"/>'
            '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}</style>'
            f'<text x="{W/2}" y="{H/2 - 8}" text-anchor="middle" font-size="18" font-weight="600" fill="{t["fg"]}">'
            f'{user}\'s contribution graph</text>'
            f'<text x="{W/2}" y="{H/2 + 20}" text-anchor="middle" font-size="13" fill="{t["muted"]}">'
            f'{reason} · retrying at the next daily run</text></svg>')


def main():
    user, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    try:
        if os.environ.get("SAMPLE"):  # local testing with saved data
            days = [tuple(d) for d in json.load(open(os.environ["SAMPLE"]))]
        else:
            days = fetch(user, os.environ.get("GH_TOKEN"))
        pages = {name: render(days, theme, user) for name, theme in THEMES.items()}
        summary = f"{sum(c for _, c in days)} contributions over {len(days)} days"
    except Exception as e:  # noqa: BLE001 - never fail the job; the snake must still publish
        print(f"::warning::Activity graph data unavailable, writing placeholder: {e}")
        pages = {name: render_unavailable(theme, user, "Data temporarily unavailable") for name, theme in THEMES.items()}
        summary = "placeholder"
    for name, svg in pages.items():
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write(svg)
    print(f"Wrote {len(pages)} graphs for {user}: {summary}")


if __name__ == "__main__":
    main()
