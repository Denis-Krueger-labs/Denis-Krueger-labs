from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path

GRAPHQL_URL = "https://api.github.com/graphql"
OUTPUT_PATH = Path("assets/activity.svg")

BACKGROUND = "#0b0d10"
BORDER = "#3b2b4f"
TEXT = "#e8dfcf"
MUTED = "#877c91"
ACCENT = "#9b6fd3"
EMPTY = "#161a20"

LEVELS = {
    "NONE": EMPTY,
    "FIRST_QUARTILE": "#2c2340",
    "SECOND_QUARTILE": "#523775",
    "THIRD_QUARTILE": "#7650a6",
    "FOURTH_QUARTILE": "#a878e3",
}

MORI_VERDICTS = (
    "commits inspected. acceptable.",
    "activity detected. suspicious.",
    "documentation debt contained.",
    "several commits passed inspection.",
    "the logs have been consulted.",
    "metadata quality: reluctantly acceptable.",
    "branch integrity appears stable.",
    "no catastrophic merge conflicts detected.",
    "repository activity acknowledged.",
    "the familiar remains unconvinced.",
    "tests observed. confidence cautiously increased.",
    "source history reviewed. judgement pending.",
)

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
            weekday
          }
        }
      }
    }
  }
}
"""


def github_graphql(token: str, username: str) -> dict:
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=364)
    payload = json.dumps({
        "query": QUERY,
        "variables": {
            "login": username,
            "from": start.isoformat(),
            "to": now.isoformat(),
        },
    }).encode("utf-8")

    request = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-activity-generator",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API returned HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach GitHub API: {exc.reason}") from exc

    if result.get("errors"):
        raise RuntimeError(f"GitHub GraphQL error: {result['errors']}")

    user = result.get("data", {}).get("user")
    if not user:
        raise RuntimeError(f"GitHub user not found: {username}")

    return user["contributionsCollection"]["contributionCalendar"]


def daily_mori_verdict(now: datetime | None = None) -> str:
    current = now or datetime.now(timezone.utc)
    digest = hashlib.sha256(current.date().isoformat().encode("utf-8")).digest()
    index = int.from_bytes(digest[:4], "big") % len(MORI_VERDICTS)
    return MORI_VERDICTS[index]


def render_svg(calendar: dict, username: str, verdict: str) -> str:
    weeks = calendar["weeks"]
    total = calendar["totalContributions"]
    cell, gap, left, top = 11, 4, 48, 58
    grid_width = len(weeks) * (cell + gap)
    width = max(900, left + grid_width + 34)
    height = 235

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(username)} GitHub activity</title>',
        f'<desc id="desc">{total} contributions during the last year. Mori says: {escape(verdict)}</desc>',
        f'<rect width="{width}" height="{height}" rx="14" fill="{BACKGROUND}"/>',
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="13" fill="none" stroke="{BORDER}"/>',
        f'<text x="28" y="31" fill="{ACCENT}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="14" font-weight="700">FIELD ACTIVITY // LAST 365 DAYS</text>',
        f'<text x="{width - 28}" y="31" text-anchor="end" fill="{TEXT}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="13">{total} contributions</text>',
    ]

    for weekday, label in {1: "Mon", 3: "Wed", 5: "Fri"}.items():
        y = top + weekday * (cell + gap) + cell - 1
        parts.append(f'<text x="12" y="{y}" fill="{MUTED}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10">{label}</text>')

    for week_index, week in enumerate(weeks):
        x = left + week_index * (cell + gap)
        for day in week["contributionDays"]:
            y = top + day["weekday"] * (cell + gap)
            fill = LEVELS.get(day.get("contributionLevel", "NONE"), EMPTY)
            date = escape(day["date"])
            count = int(day["contributionCount"])
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{fill}"><title>{date}: {count} contributions</title></rect>')

    legend_y = 174
    legend_x = width - 205
    parts.append(f'<text x="{legend_x - 38}" y="{legend_y + 9}" fill="{MUTED}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10">less</text>')
    legend_colors = [EMPTY, LEVELS["FIRST_QUARTILE"], LEVELS["SECOND_QUARTILE"], LEVELS["THIRD_QUARTILE"], LEVELS["FOURTH_QUARTILE"]]
    for index, color in enumerate(legend_colors):
        x = legend_x + index * (cell + gap)
        parts.append(f'<rect x="{x}" y="{legend_y}" width="{cell}" height="{cell}" rx="2" fill="{color}"/>')
    parts.append(f'<text x="{legend_x + 5 * (cell + gap) + 2}" y="{legend_y + 9}" fill="{MUTED}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10">more</text>')

    parts.extend([
        f'<line x1="28" y1="200" x2="{width - 28}" y2="200" stroke="{BORDER}" stroke-width="1"/>',
        f'<text x="28" y="220" fill="{ACCENT}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12" font-weight="700">/•᷅‎‎•᷄\\੭</text>',
        f'<text x="112" y="220" fill="{TEXT}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12">{escape(verdict)}</text>',
        f'<text x="{width - 28}" y="220" text-anchor="end" fill="{MUTED}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10">daily familiar verdict</text>',
        '</svg>',
    ])
    return "\n".join(parts)


def main() -> int:
    token = os.getenv("GITHUB_TOKEN")
    username = os.getenv("GITHUB_USERNAME", "Denis-Krueger-labs")
    if not token:
        print("GITHUB_TOKEN is required.", file=sys.stderr)
        return 1

    try:
        calendar = github_graphql(token, username)
        verdict = daily_mori_verdict()
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(render_svg(calendar, username, verdict), encoding="utf-8")
    except Exception as exc:
        print(f"Failed to generate activity graph: {exc}", file=sys.stderr)
        return 1

    print(f"Updated {OUTPUT_PATH} with Mori verdict: {verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())