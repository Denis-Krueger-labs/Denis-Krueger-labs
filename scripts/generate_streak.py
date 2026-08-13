from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

from datetime import date, datetime, time, timedelta, timezone
from html import escape
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "assets" / "streak.svg"

BERLIN = ZoneInfo("Europe/Berlin")
GRAPHQL_URL = "https://api.github.com/graphql"


# ---------------------------------------------------------------------------
# MORI palette
# ---------------------------------------------------------------------------

BACKGROUND = "#0b0d10"
BORDER = "#3b2b4f"
TEXT = "#e8dfcf"
MUTED = "#877c91"
ACCENT = "#9b6fd3"
ACCENT_BRIGHT = "#a878e3"
PANEL = "#161a20"


# The creature.
MORI = "/•᷅‎‎•᷄\\੭"


# ---------------------------------------------------------------------------
# MORI streak progression
# ---------------------------------------------------------------------------

STREAK_TIERS = (
    {
        "min": 0,
        "rank": "COLD BOOT",
        "verdict": "No worthy field activity has presented itself.",
    },
    {
        "min": 1,
        "rank": "SIGNAL FOUND",
        "verdict": "I have noticed you. Do not become excited.",
    },
    {
        "min": 7,
        "rank": "PATTERN FORMING",
        "verdict": "Your persistence is becoming difficult to ignore.",
    },
    {
        "min": 14,
        "rank": "RELIABLE OPERATOR",
        "verdict": "You may, in fact, know what you are doing.",
    },
    {
        "min": 30,
        "rank": "TOLERATED OPERATOR",
        "verdict": "Your presence is now expected. Do not ruin this.",
    },
    {
        "min": 100,
        "rank": "TRUSTED ENTITY",
        "verdict": "You have earned a rare thing: my trust.",
    },
    {
        "min": 365,
        "rank": "YEARBOUND",
        "verdict": "A full cycle. I admit this is becoming impressive.",
    },
    {
        "min": 730,
        "rank": "LEGEND-CLASS FAMILIAR",
        "verdict": "Years have passed. The archive knows your name now.",
    },
    {
        "min": 1825,
        "rank": "MYTHIC ARCHIVE",
        "verdict": "Five years. Fine. I am impressed. Do not quote me.",
    },
)


# ---------------------------------------------------------------------------
# GraphQL queries
# ---------------------------------------------------------------------------

USER_QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
  }
}
"""

CONTRIBUTIONS_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""


# ---------------------------------------------------------------------------
# Tier helpers
# ---------------------------------------------------------------------------

def streak_tier(streak: int) -> dict[str, object]:
    active = STREAK_TIERS[0]

    for tier in STREAK_TIERS:
        if streak < int(tier["min"]):
            break

        active = tier

    return active


def next_streak_tier(streak: int) -> dict[str, object] | None:
    for tier in STREAK_TIERS:
        if int(tier["min"]) > streak:
            return tier

    return None


def progress_message(streak: int) -> str:
    next_tier = next_streak_tier(streak)

    if next_tier is None:
        return "highest archive classification reached"

    target = int(next_tier["min"])
    remaining = target - streak
    unit = "day" if remaining == 1 else "days"

    return f"{remaining} {unit} until {next_tier['rank']}"


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

def graphql_request(
    token: str,
    query: str,
    variables: dict[str, Any],
) -> dict[str, Any]:
    payload = json.dumps(
        {
            "query": query,
            "variables": variables,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "mori-profile-streak-generator",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"GitHub API returned HTTP {exc.code}: {body}"
        ) from exc

    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Could not reach GitHub API: {exc.reason}"
        ) from exc

    if result.get("errors"):
        raise RuntimeError(
            f"GitHub GraphQL error: {result['errors']}"
        )

    return result


def get_account_created_at(
    token: str,
    username: str,
) -> datetime:
    result = graphql_request(
        token,
        USER_QUERY,
        {
            "login": username,
        },
    )

    user = result.get("data", {}).get("user")

    if not user:
        raise RuntimeError(
            f"GitHub user not found: {username}"
        )

    created_at = user.get("createdAt")

    if not created_at:
        raise RuntimeError(
            "GitHub did not return account creation time."
        )

    return datetime.fromisoformat(
        created_at.replace("Z", "+00:00")
    )


def berlin_day_start(day: date) -> datetime:
    return datetime.combine(
        day,
        time.min,
        tzinfo=BERLIN,
    )


def berlin_day_end(day: date) -> datetime:
    return (
        datetime.combine(
            day + timedelta(days=1),
            time.min,
            tzinfo=BERLIN,
        )
        - timedelta(microseconds=1)
    )


def fetch_contribution_range(
    token: str,
    username: str,
    start_day: date,
    end_day: date,
) -> dict[date, int]:
    start = berlin_day_start(start_day).astimezone(timezone.utc)
    end = berlin_day_end(end_day).astimezone(timezone.utc)

    result = graphql_request(
        token,
        CONTRIBUTIONS_QUERY,
        {
            "login": username,
            "from": start.isoformat(),
            "to": end.isoformat(),
        },
    )

    user = result.get("data", {}).get("user")

    if not user:
        raise RuntimeError(
            f"GitHub user not found: {username}"
        )

    calendar = user["contributionsCollection"]["contributionCalendar"]
    contributions: dict[date, int] = {}

    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            contribution_day = date.fromisoformat(day["date"])
            contributions[contribution_day] = int(day["contributionCount"])

    return contributions


def fetch_contribution_history(
    token: str,
    username: str,
    start_day: date,
    end_day: date,
) -> dict[date, int]:
    """
    Fetch contribution history in bounded chunks.

    This keeps each GitHub contribution query comfortably below
    the one-year range while still allowing multi-year streaks.
    """

    history: dict[date, int] = {}
    current_start = start_day

    while current_start <= end_day:
        current_end = min(
            current_start + timedelta(days=359),
            end_day,
        )

        print(
            "Fetching contribution history: "
            f"{current_start.isoformat()} -> "
            f"{current_end.isoformat()}"
        )

        chunk = fetch_contribution_range(
            token,
            username,
            current_start,
            current_end,
        )

        history.update(chunk)
        current_start = current_end + timedelta(days=1)

    return history


# ---------------------------------------------------------------------------
# Streak calculation
# ---------------------------------------------------------------------------

def calculate_current_streak(
    contributions: dict[date, int],
    today: date,
) -> tuple[int, date | None, date | None]:
    if contributions.get(today, 0) > 0:
        cursor = today
    else:
        cursor = today - timedelta(days=1)

    streak_end = cursor
    count = 0

    while contributions.get(cursor, 0) > 0:
        count += 1
        cursor -= timedelta(days=1)

    if count == 0:
        return 0, None, None

    streak_start = cursor + timedelta(days=1)

    return count, streak_start, streak_end


def calculate_longest_streak(
    contributions: dict[date, int],
    start_day: date,
    end_day: date,
) -> tuple[int, date | None, date | None]:
    longest_count = 0
    longest_start: date | None = None
    longest_end: date | None = None

    current_count = 0
    current_start: date | None = None
    cursor = start_day

    while cursor <= end_day:
        if contributions.get(cursor, 0) > 0:
            if current_count == 0:
                current_start = cursor

            current_count += 1

            if current_count > longest_count:
                longest_count = current_count
                longest_start = current_start
                longest_end = cursor
        else:
            current_count = 0
            current_start = None

        cursor += timedelta(days=1)

    return longest_count, longest_start, longest_end


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_day(day: date | None) -> str:
    if day is None:
        return "--/--"

    return day.strftime("%d/%m")


def format_range(
    start: date | None,
    end: date | None,
) -> str:
    if start is None or end is None:
        return "no active sequence"

    if start.year == end.year:
        return f"{format_day(start)} - {format_day(end)}"

    return (
        f"{start.strftime('%d/%m/%Y')} - "
        f"{end.strftime('%d/%m/%Y')}"
    )


# ---------------------------------------------------------------------------
# SVG rendering
# ---------------------------------------------------------------------------

def render_svg(
    current_streak: int,
    current_start: date | None,
    current_end: date | None,
    longest_streak: int,
    longest_start: date | None,
    longest_end: date | None,
) -> str:
    width = 690
    height = 245

    mono = (
        "ui-monospace, SFMono-Regular, "
        "Menlo, Consolas, monospace"
    )

    tier = streak_tier(current_streak)

    rank = escape(str(tier["rank"]))
    verdict = escape(str(tier["verdict"]))

    current_range = escape(format_range(current_start, current_end))
    longest_range = escape(format_range(longest_start, longest_end))
    progress = escape(progress_message(current_streak))

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" '
        f'role="img" aria-labelledby="title desc">',

        '<title id="title">MORI streak card</title>',
        '<desc id="desc">A MORI-themed GitHub streak card.</desc>',

        f'<rect width="{width}" height="{height}" rx="14" fill="{BACKGROUND}"/>',
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" '
        f'rx="13" fill="none" stroke="{BORDER}"/>',

        f'<text x="28" y="31" fill="{ACCENT}" '
        f'font-family="{mono}" font-size="14" font-weight="700">'
        f'MORI // OPERATOR CONTINUITY'
        f'</text>',

        f'<text x="{width - 28}" y="31" text-anchor="end" '
        f'fill="{MUTED}" font-family="{mono}" font-size="10">'
        f'field persistence monitor'
        f'</text>',

        f'<rect x="28" y="48" width="390" height="92" '
        f'rx="10" fill="{PANEL}" stroke="{BORDER}"/>',

        f'<text x="48" y="72" fill="{MUTED}" '
        f'font-family="{mono}" font-size="10" font-weight="700">'
        f'CURRENT STREAK'
        f'</text>',

        f'<text x="48" y="118" fill="{TEXT}" '
        f'font-family="{mono}" font-size="44" font-weight="700">'
        f'{current_streak}'
        f'</text>',

        f'<text x="128" y="108" fill="{ACCENT_BRIGHT}" '
        f'font-family="{mono}" font-size="12" font-weight="700">'
        f'DAYS'
        f'</text>',

        f'<text x="128" y="126" fill="{MUTED}" '
        f'font-family="{mono}" font-size="10">'
        f'{current_range}'
        f'</text>',

        f'<rect x="432" y="48" width="230" height="92" '
        f'rx="10" fill="{PANEL}" stroke="{BORDER}"/>',

        f'<text x="452" y="72" fill="{MUTED}" '
        f'font-family="{mono}" font-size="10" font-weight="700">'
        f'LONGEST STREAK'
        f'</text>',

        f'<text x="452" y="108" fill="{TEXT}" '
        f'font-family="{mono}" font-size="27" font-weight="700">'
        f'{longest_streak}'
        f'</text>',

        f'<text x="452" y="126" fill="{MUTED}" '
        f'font-family="{mono}" font-size="10">'
        f'{longest_range}'
        f'</text>',

        f'<text x="28" y="166" fill="{ACCENT_BRIGHT}" '
        f'font-family="{mono}" font-size="12" font-weight="700">'
        f'{rank}'
        f'</text>',

        f'<text x="{width - 28}" y="166" text-anchor="end" '
        f'fill="{MUTED}" font-family="{mono}" font-size="10">'
        f'{progress}'
        f'</text>',

        f'<line x1="28" y1="181" x2="{width - 28}" y2="181" '
        f'stroke="{BORDER}" stroke-width="1"/>',

        f'<text x="28" y="207" fill="{ACCENT}" '
        f'font-family="{mono}" font-size="12" font-weight="700">'
        f'{escape(MORI)}'
        f'</text>',

        f'<text x="110" y="207" fill="{TEXT}" '
        f'font-family="{mono}" font-size="11">'
        f'{verdict}'
        f'</text>',

        f'<text x="{width - 28}" y="228" text-anchor="end" '
        f'fill="{MUTED}" font-family="{mono}" font-size="9">'
        f'mori familiar classification // berlin'
        f'</text>',

        "</svg>",
    ]

    return "\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    token = os.getenv("GITHUB_TOKEN")
    username = os.getenv(
        "GITHUB_USERNAME",
        "Denis-Krueger-labs",
    )

    if not token:
        print("GITHUB_TOKEN is required.", file=sys.stderr)
        return 1

    try:
        today = datetime.now(BERLIN).date()

        created_at = get_account_created_at(
            token,
            username,
        )

        created_day = created_at.astimezone(BERLIN).date()

        contributions = fetch_contribution_history(
            token,
            username,
            created_day,
            today,
        )

        current_streak, current_start, current_end = calculate_current_streak(
            contributions,
            today,
        )

        longest_streak, longest_start, longest_end = calculate_longest_streak(
            contributions,
            created_day,
            today,
        )

        svg = render_svg(
            current_streak=current_streak,
            current_start=current_start,
            current_end=current_end,
            longest_streak=longest_streak,
            longest_start=longest_start,
            longest_end=longest_end,
        )

        OUTPUT_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        OUTPUT_PATH.write_text(
            svg,
            encoding="utf-8",
        )

    except Exception as exc:
        print(
            f"Failed to generate MORI streak card: {exc}",
            file=sys.stderr,
        )
        return 1

    tier = streak_tier(current_streak)

    print(f"Generated: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Current streak: {current_streak} days")
    print(f"Longest streak: {longest_streak} days")
    print(f"MORI classification: {tier['rank']}")
    print(f"MORI verdict: {tier['verdict']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
