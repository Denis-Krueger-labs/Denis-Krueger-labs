from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

from html import escape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "assets" / "languages.svg"

REST_API_URL = "https://api.github.com"


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
RAIL = "#222831"

MONO = (
    "ui-monospace, SFMono-Regular, "
    "Menlo, Consolas, monospace"
)


# The creature.
MORI = "/•᷅‎‎•᷄\\੭"


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

def github_request(
    token: str,
    url: str,
) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "mori-profile-language-generator",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(
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


def fetch_owned_repositories(
    token: str,
    username: str,
) -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    page = 1

    while True:
        url = (
            f"{REST_API_URL}/users/{username}/repos"
            f"?per_page=100"
            f"&page={page}"
            f"&type=owner"
            f"&sort=updated"
        )

        page_data = github_request(token, url)

        if not isinstance(page_data, list):
            raise RuntimeError(
                "GitHub did not return a repository list."
            )

        if not page_data:
            break

        for repo in page_data:
            if repo.get("fork"):
                continue

            repos.append(repo)

        page += 1

    return repos


def aggregate_language_totals(
    token: str,
    repos: list[dict[str, Any]],
) -> dict[str, int]:
    totals: dict[str, int] = {}

    for repo in repos:
        repo_name = repo.get("name", "unknown")
        languages_url = repo.get("languages_url")

        if not languages_url:
            continue

        print(
            f"Fetching languages: {repo_name}"
        )

        language_map = github_request(
            token,
            languages_url,
        )

        if not isinstance(language_map, dict):
            continue

        for language, byte_count in language_map.items():
            totals[language] = (
                totals.get(language, 0)
                + int(byte_count)
            )

    return totals


def top_languages(
    totals: dict[str, int],
    limit: int = 4,
) -> list[dict[str, float | int | str]]:
    total_bytes = sum(totals.values())

    if total_bytes <= 0:
        return []

    ranked = sorted(
        totals.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    result: list[dict[str, float | int | str]] = []

    for language, byte_count in ranked[:limit]:
        percentage = (
            byte_count / total_bytes
        ) * 100

        result.append(
            {
                "name": language,
                "bytes": byte_count,
                "percentage": percentage,
            }
        )

    return result


# ---------------------------------------------------------------------------
# MORI opinions
# ---------------------------------------------------------------------------

def mori_language_verdict(
    languages: list[dict[str, float | int | str]],
) -> str:
    if not languages:
        return (
            "No discernible operator dialects were detected. "
            "Suspicious."
        )

    names = [
        str(item["name"])
        for item in languages
    ]

    top = names[0]

    if {"C#", "TypeScript"}.issubset(set(names[:4])):
        return (
            "Full-stack tendencies detected. "
            "Regrettably competent."
        )

    if {"Python", "Shell"}.issubset(set(names[:4])):
        return (
            "Automation has consumed the operator. "
            "I approve, cautiously."
        )

    if {"C", "C++"}.issubset(set(names[:4])):
        return (
            "Pointers and consequences. "
            "A personality trait, apparently."
        )

    if {"HTML", "CSS"}.issubset(set(names[:4])):
        return (
            "You have been moving boxes again. "
            "Remarkable."
        )

    verdicts = {
        "C": (
            "You were offered abstractions. "
            "You declined."
        ),
        "C++": (
            "C, but with enough features to qualify as weather."
        ),
        "C#": (
            "Enterprise sorcery. "
            "At least you type your variables."
        ),
        "Python": (
            "Readable, efficient, and one indentation error "
            "from mutiny."
        ),
        "JavaScript": (
            "You have selected chaos. "
            "Bold, if questionable."
        ),
        "TypeScript": (
            "JavaScript, but supervised. "
            "Sensible."
        ),
        "Rust": (
            "The borrow checker supervises you "
            "so I do not have to."
        ),
        "Go": (
            "Simple, practical, suspiciously reasonable."
        ),
        "Java": (
            "Another factory for your factory, I presume."
        ),
        "Shell": (
            "This was supposed to be six commands, was it not?"
        ),
        "PowerShell": (
            "A shell command should not resemble legal paperwork."
        ),
        "HTML": (
            "This is not a programming language. "
            "I will permit it anyway."
        ),
        "CSS": (
            "You moved the box three pixels. "
            "How triumphant."
        ),
        "Nix": (
            "You configured one package. "
            "The universe is now declarative."
        ),
        "SQL": (
            "You asked the database nicely. "
            "Unexpectedly civil."
        ),
        "Assembly": (
            "You descended beneath abstraction. "
            "I shall fetch a lantern."
        ),
    }

    return verdicts.get(
        top,
        "A curious dialect mix. "
        "You remain difficult to classify.",
    )


# ---------------------------------------------------------------------------
# Animated expanding bars
# ---------------------------------------------------------------------------

def render_expanding_bar(
    *,
    x: int,
    y: int,
    fill_width: int,
    height: int,
    delay: float,
    duration: float,
    bar_id: str,
    color: str,
) -> list[str]:
    """
    Render an expanding bar with a static fallback.

    If SVG animation is unsupported, the static final bar remains visible.
    If animation is supported, the fallback is hidden immediately and the
    animated bar expands at the configured delay.
    """

    if fill_width <= 0:
        return []

    radius = height / 2

    return [
        # Static fallback
        (
            f'<rect '
            f'x="{x}" '
            f'y="{y}" '
            f'width="{fill_width}" '
            f'height="{height}" '
            f'rx="{radius}" '
            f'fill="{color}">'
            f'<set '
            f'attributeName="opacity" '
            f'to="0" '
            f'begin="0s" '
            f'fill="freeze"'
            f'/>'
            f'</rect>'
        ),

        # Animated bar
        (
            f'<rect '
            f'x="{x}" '
            f'y="{y}" '
            f'width="0" '
            f'height="{height}" '
            f'rx="{radius}" '
            f'fill="{color}" '
            f'opacity="0">'
            f'<set '
            f'attributeName="opacity" '
            f'to="1" '
            f'begin="{delay}s" '
            f'fill="freeze"'
            f'/>'
            f'<animate '
            f'attributeName="width" '
            f'from="0" '
            f'to="{fill_width}" '
            f'begin="{delay}s" '
            f'dur="{duration}s" '
            f'fill="freeze" '
            f'calcMode="spline" '
            f'keyTimes="0;1" '
            f'keySplines="0.2 0.8 0.2 1"'
            f'/>'
            f'</rect>'
        ),
    ]


# ---------------------------------------------------------------------------
# SVG rendering
# ---------------------------------------------------------------------------

def render_svg(
    username: str,
    languages: list[dict[str, float | int | str]],
) -> str:
    width = 690
    height = 245

    verdict = escape(
        mori_language_verdict(languages)
    )

    parts = [
        f'<svg '
        f'xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" '
        f'height="{height}" '
        f'viewBox="0 0 {width} {height}" '
        f'role="img" '
        f'aria-labelledby="title desc">',

        (
            f'<title id="title">'
            f'{escape(username)} language distribution'
            f'</title>'
        ),

        (
            f'<desc id="desc">'
            f'MORI language analysis card showing the most used '
            f'languages for {escape(username)}.'
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
        f'MORI // OPERATOR DIALECTS'
        f'</text>',

        f'<text '
        f'x="{width - 28}" '
        f'y="31" '
        f'text-anchor="end" '
        f'fill="{MUTED}" '
        f'font-family="{MONO}" '
        f'font-size="10">'
        f'language distribution audit'
        f'</text>',

        # Main panel
        f'<rect '
        f'x="28" '
        f'y="48" '
        f'width="634" '
        f'height="118" '
        f'rx="10" '
        f'fill="{PANEL}" '
        f'stroke="{BORDER}"'
        f'/>',
    ]

    if not languages:
        parts.extend(
            [
                f'<text '
                f'x="48" '
                f'y="98" '
                f'fill="{TEXT}" '
                f'font-family="{MONO}" '
                f'font-size="12">'
                f'No language data available.'
                f'</text>',
            ]
        )
    else:
        label_x = 48
        rail_x = 190
        rail_width = 320
        percent_x = 632

        for index, language in enumerate(languages):
            name = escape(str(language["name"]))
            percentage = float(language["percentage"])

            label_y = 78 + index * 24
            rail_y = 84 + index * 24
            fill_width = round(
                rail_width * (percentage / 100)
            )

            delay = index * 0.12
            duration = 0.55

            parts.extend(
                [
                    f'<text '
                    f'x="{label_x}" '
                    f'y="{label_y}" '
                    f'fill="{TEXT}" '
                    f'font-family="{MONO}" '
                    f'font-size="11" '
                    f'font-weight="700">'
                    f'{name}'
                    f'</text>',

                    f'<rect '
                    f'x="{rail_x}" '
                    f'y="{rail_y}" '
                    f'width="{rail_width}" '
                    f'height="10" '
                    f'rx="5" '
                    f'fill="{RAIL}"'
                    f'/>',

                    f'<text '
                    f'x="{percent_x}" '
                    f'y="{label_y}" '
                    f'text-anchor="end" '
                    f'fill="{MUTED}" '
                    f'font-family="{MONO}" '
                    f'font-size="10">'
                    f'{percentage:.1f}%'
                    f'</text>',
                ]
            )

            parts.extend(
                render_expanding_bar(
                    x=rail_x,
                    y=rail_y,
                    fill_width=fill_width,
                    height=10,
                    delay=delay,
                    duration=duration,
                    bar_id=f"lang-bar-{index}",
                    color=ACCENT_BRIGHT,
                )
            )

    parts.extend(
        [
            # Divider
            f'<line '
            f'x1="28" '
            f'y1="181" '
            f'x2="{width - 28}" '
            f'y2="181" '
            f'stroke="{BORDER}" '
            f'stroke-width="1"'
            f'/>',

            # Verdict
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
            f'mori language assessment // berlin'
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
        repos = fetch_owned_repositories(
            token,
            username,
        )

        totals = aggregate_language_totals(
            token,
            repos,
        )

        languages = top_languages(
            totals,
            limit=4,
        )

        svg = render_svg(
            username=username,
            languages=languages,
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
            "Failed to generate MORI language card: "
            f"{exc}",
            file=sys.stderr,
        )
        return 1

    print(
        f"Generated: {OUTPUT_PATH.relative_to(ROOT)}"
    )

    if languages:
        print("Top languages:")
        for item in languages:
            print(
                f"  - {item['name']}: "
                f"{float(item['percentage']):.1f}%"
            )
    else:
        print("No language data available.")

    print(
        "MORI verdict: "
        f"{mori_language_verdict(languages)}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
