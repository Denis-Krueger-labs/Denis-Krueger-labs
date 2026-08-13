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

MONO = (
    "ui-monospace, SFMono-Regular, "
    "Menlo, Consolas, monospace"
)


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
            result = json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.HTTPError as exc:
        body = exc.read().decode(
            "utf-8",
            errors="replace",
        )

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
    start = berlin_day_start(
        start_day
    ).astimezone(timezone.utc)

    end = berlin_day_end(
        end_day
    ).astimezone(timezone.utc)

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

    calendar = user[
        "contributionsCollection"
    ][
        "contributionCalendar"
    ]

    contributions: dict[date, int] = {}

    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            contribution_day = date.fromisoformat(
                day["date"]
            )

            contributions[contribution_day] = int(
                day["contributionCount"]
            )

    return contributions


def fetch_contribution_history(
    token: str,
    username: str,
    start_day: date,
    end_day: date,
) -> dict[date, int]:
    """
    Fetch contribution history in bounded chunks.

    Each request stays comfortably below one year while still
    allowing MORI to calculate multi-year streaks.
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

        current_start = (
            current_end + timedelta(days=1)
        )

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

    return (
        longest_count,
        longest_start,
        longest_end,
    )


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
        return (
            f"{format_day(start)} - "
            f"{format_day(end)}"
        )

    return (
        f"{start.strftime('%d/%m/%Y')} - "
        f"{end.strftime('%d/%m/%Y')}"
    )


# ---------------------------------------------------------------------------
# Animated counter
# ---------------------------------------------------------------------------

def counter_values(
    target: int,
    max_frames: int = 40,
) -> list[int]:
    """
    Small streaks display every number.

    Large streaks sample the range so a five-year streak does not
    create thousands of SVG text elements.
    """

    if target <= max_frames:
        return list(range(target + 1))

    values = [
        round(
            target * index / max_frames
        )
        for index in range(max_frames + 1)
    ]

    return list(
        dict.fromkeys(values)
    )


def render_number_reel(
    *,
    x: int,
    baseline_y: int,
    target: int,
    font_size: int,
    color: str,
    reel_id: str,
    duration: float,
    width: int = 120,
) -> list[str]:
    """
    Render a flip-style number reel with a static fallback.

    If SVG animation is unsupported, the final target number remains
    visible instead of leaving the counter stuck at zero.
    """

    values = counter_values(target)

    if target == 0:
        return [
            f'<text x="{x}" y="{baseline_y}" '
            f'fill="{color}" '
            f'font-family="{MONO}" '
            f'font-size="{font_size}" '
            f'font-weight="700">'
            f'0'
            f'</text>'
        ]

    row_height = font_size + 14

    clip_y = (
        baseline_y - font_size
    )

    clip_height = (
        font_size + 12
    )

    offsets = [
        -(index * row_height)
        for index in range(len(values))
    ]

    transform_values = ";".join(
        f"0 {offset}"
        for offset in offsets
    )

    parts = [
        "<defs>",

        (
            f'<clipPath id="{reel_id}-clip">'
            f'<rect '
            f'x="{x}" '
            f'y="{clip_y}" '
            f'width="{width}" '
            f'height="{clip_height}"'
            f'/>'
            f'</clipPath>'
        ),

        "</defs>",

        # Static final value.
        #
        # If SMIL animation is unsupported, this remains visible.
        (
            f'<text '
            f'x="{x}" '
            f'y="{baseline_y}" '
            f'fill="{color}" '
            f'font-family="{MONO}" '
            f'font-size="{font_size}" '
            f'font-weight="700">'
            f'{target}'
            f'<set '
            f'attributeName="opacity" '
            f'to="0" '
            f'begin="0s" '
            f'fill="freeze"'
            f'/>'
            f'</text>'
        ),

        # Animated reel starts hidden.
        #
        # Browsers supporting SVG animation reveal it immediately.
        (
            f'<g '
            f'clip-path="url(#{reel_id}-clip)" '
            f'opacity="0">'
            f'<set '
            f'attributeName="opacity" '
            f'to="1" '
            f'begin="0s" '
            f'fill="freeze"'
            f'/>'
        ),

        "<g>",

        (
            f'<animateTransform '
            f'attributeName="transform" '
            f'type="translate" '
            f'values="{transform_values}" '
            f'dur="{duration}s" '
            f'calcMode="discrete" '
            f'fill="freeze"'
            f'/>'
        ),
    ]

    for index, value in enumerate(values):
        y = (
            baseline_y
            + index * row_height
        )

        parts.append(
            f'<text '
            f'x="{x}" '
            f'y="{y}" '
            f'fill="{color}" '
            f'font-family="{MONO}" '
            f'font-size="{font_size}" '
            f'font-weight="700">'
            f'{value}'
            f'</text>'
        )

    parts.extend(
        [
            "</g>",
            "</g>",
        ]
    )

    return parts


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

    tier = streak_tier(
        current_streak
    )

    rank = escape(
        str(tier["rank"])
    )

    verdict = escape(
        str(tier["verdict"])
    )

    current_range = escape(
        format_range(
            current_start,
            current_end,
        )
    )

    longest_range = escape(
        format_range(
            longest_start,
            longest_end,
        )
    )

    progress = escape(
        progress_message(
            current_streak
        )
    )

    parts = [
        f'<svg '
        f'xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" '
        f'height="{height}" '
        f'viewBox="0 0 {width} {height}" '
        f'role="img" '
        f'aria-labelledby="title desc">',

        '<title id="title">'
        'MORI streak card'
        '</title>',

        (
            f'<desc id="desc">'
            f'Current streak: '
            f'{current_streak} days. '
            f'Longest streak: '
            f'{longest_streak} days. '
            f'MORI classification: '
            f'{rank}.'
            f'</desc>'
        ),

        # Background
        f'<rect '
        f'width="{width}" '
        f'height="{height}" '
        f'rx="14" '
        f'fill="{BACKGROUND}"'
        f'/>',

        # Outer border
        f'<rect '
        f'x="1" '
        f'y="1" '
        f'width="{width - 2}" '
        f'height="{height - 2}" '
        f'rx="13" '
        f'fill="none" '
        f'stroke="{BORDER}"'
        f'/>',

        # Header
        f'<text '
        f'x="28" '
        f'y="31" '
        f'fill="{ACCENT}" '
        f'font-family="{MONO}" '
        f'font-size="14" '
        f'font-weight="700">'
        f'MORI // OPERATOR CONTINUITY'
        f'</text>',

        f'<text '
        f'x="{width - 28}" '
        f'y="31" '
        f'text-anchor="end" '
        f'fill="{MUTED}" '
        f'font-family="{MONO}" '
        f'font-size="10">'
        f'field persistence monitor'
        f'</text>',

        # Current streak panel
        f'<rect '
        f'x="28" '
        f'y="48" '
        f'width="390" '
        f'height="92" '
        f'rx="10" '
        f'fill="{PANEL}" '
        f'stroke="{BORDER}"'
        f'/>',

        f'<text '
        f'x="48" '
        f'y="72" '
        f'fill="{MUTED}" '
        f'font-family="{MONO}" '
        f'font-size="10" '
        f'font-weight="700">'
        f'CURRENT STREAK'
        f'</text>',
    ]

    # Animated current streak counter
    parts.extend(
        render_number_reel(
            x=48,
            baseline_y=118,
            target=current_streak,
            font_size=44,
            color=TEXT,
            reel_id="current-streak",
            duration=1.25,
            width=120,
        )
    )

    parts.extend(
        [
            f'<text '
            f'x="128" '
            f'y="108" '
            f'fill="{ACCENT_BRIGHT}" '
            f'font-family="{MONO}" '
            f'font-size="12" '
            f'font-weight="700">'
            f'DAYS'
            f'</text>',

            f'<text '
            f'x="128" '
            f'y="126" '
            f'fill="{MUTED}" '
            f'font-family="{MONO}" '
            f'font-size="10">'
            f'{current_range}'
            f'</text>',

            # Longest streak panel
            f'<rect '
            f'x="432" '
            f'y="48" '
            f'width="230" '
            f'height="92" '
            f'rx="10" '
            f'fill="{PANEL}" '
            f'stroke="{BORDER}"'
            f'/>',

            f'<text '
            f'x="452" '
            f'y="72" '
            f'fill="{MUTED}" '
            f'font-family="{MONO}" '
            f'font-size="10" '
            f'font-weight="700">'
            f'LONGEST STREAK'
            f'</text>',
        ]
    )

    # Animated longest streak counter
    parts.extend(
        render_number_reel(
            x=452,
            baseline_y=108,
            target=longest_streak,
            font_size=27,
            color=TEXT,
            reel_id="longest-streak",
            duration=1.45,
            width=100,
        )
    )

    parts.extend(
        [
            f'<text '
            f'x="452" '
            f'y="126" '
            f'fill="{MUTED}" '
            f'font-family="{MONO}" '
            f'font-size="10">'
            f'{longest_range}'
            f'</text>',

            # Rank + next level
            f'<text '
            f'x="28" '
            f'y="166" '
            f'fill="{ACCENT_BRIGHT}" '
            f'font-family="{MONO}" '
            f'font-size="12" '
            f'font-weight="700">'
            f'{rank}'
            f'</text>',

            f'<text '
            f'x="{width - 28}" '
            f'y="166" '
            f'text-anchor="end" '
            f'fill="{MUTED}" '
            f'font-family="{MONO}" '
            f'font-size="10">'
            f'{progress}'
            f'</text>',

            # Divider
            f'<line '
            f'x1="28" '
            f'y1="181" '
            f'x2="{width - 28}" '
            f'y2="181" '
            f'stroke="{BORDER}" '
            f'stroke-width="1"'
            f'/>',

            # The beast
            f'<text '
            f'x="28" '
            f'y="207" '
            f'fill="{ACCENT}" '
            f'font-family="{MONO}" '
            f'font-size="12" '
            f'font-weight="700">'
            f'{escape(MORI)}'
            f'</text>',

            f'<text '
            f'x="110" '
            f'y="207" '
            f'fill="{TEXT}" '
            f'font-family="{MONO}" '
            f'font-size="11">'
            f'{verdict}'
            f'</text>',

            f'<text '
            f'x="{width - 28}" '
            f'y="222" '
            f'text-anchor="end" '
            f'fill="{MUTED}" '
            f'font-family="{MONO}" '
            f'font-size="9">'
            f'mori familiar classification // berlin'
            f'</text>',

            "</svg>",
        ]
    )

    return "\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    token = os.getenv(
        "GITHUB_TOKEN"
    )

    username = os.getenv(
        "GITHUB_USERNAME",
        "Denis-Krueger-labs",
    )

    if not token:
        print(
            "GITHUB_TOKEN is required.",
            file=sys.stderr,
        )
        return 1

    try:
        today = datetime.now(
            BERLIN
        ).date()

        created_at = (
            get_account_created_at(
                token,
                username,
            )
        )

        created_day = (
            created_at
            .astimezone(BERLIN)
            .date()
        )

        contributions = (
            fetch_contribution_history(
                token,
                username,
                created_day,
                today,
            )
        )

        (
            current_streak,
            current_start,
            current_end,
        ) = calculate_current_streak(
            contributions,
            today,
        )

        (
            longest_streak,
            longest_start,
            longest_end,
        ) = calculate_longest_streak(
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
            "Failed to generate "
            f"MORI streak card: {exc}",
            file=sys.stderr,
        )

        return 1

    tier = streak_tier(
        current_streak
    )

    print(
        f"Generated: "
        f"{OUTPUT_PATH.relative_to(ROOT)}"
    )

    print(
        f"Current streak: "
        f"{current_streak} days"
    )

    print(
        f"Longest streak: "
        f"{longest_streak} days"
    )

    print(
        "MORI classification: "
        f"{tier['rank']}"
    )

    print(
        "MORI verdict: "
        f"{tier['verdict']}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
