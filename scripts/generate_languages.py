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
        with urllib.request.urlopen(
            request,
            timeout=30,
        ) as response:
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

        page_data = github_request(
            token,
            url,
        )

        if not isinstance(
            page_data,
            list,
        ):
            raise RuntimeError(
                "GitHub did not return a repository list."
            )

        if not page_data:
            break

        for repo in page_data:
            # Forks do not count as operator work.
            if repo.get("fork"):
                continue

            repos.append(repo)

        page += 1

    return repos


# ---------------------------------------------------------------------------
# Repository-weighted language analysis
# ---------------------------------------------------------------------------

def calculate_repo_weighted_languages(
    token: str,
    repos: list[dict[str, Any]],
) -> tuple[dict[str, float], int]:
    """
    Give every repository equal influence.

    Example:

        Repo A:
            C      90%
            Python 10%

        Repo B:
            C#     100%

    Repo A and Repo B each contribute exactly one repository worth
    of weight, regardless of how many source bytes they contain.

    This prevents one giant repository from dominating the entire
    profile language distribution.
    """

    scores: dict[str, float] = {}
    counted_repositories = 0

    for repo in repos:
        repo_name = str(
            repo.get(
                "name",
                "unknown",
            )
        )

        languages_url = repo.get(
            "languages_url"
        )

        if not languages_url:
            continue

        print(
            f"Fetching languages: {repo_name}"
        )

        language_map = github_request(
            token,
            languages_url,
        )

        if not isinstance(
            language_map,
            dict,
        ):
            continue

        language_bytes: dict[str, int] = {}

        for language, byte_count in language_map.items():
            byte_count_int = int(
                byte_count
            )

            if byte_count_int <= 0:
                continue

            language_bytes[
                str(language)
            ] = byte_count_int

        repo_total = sum(
            language_bytes.values()
        )

        # Empty / documentation-only repositories have no useful
        # language vote.
        if repo_total <= 0:
            print(
                f"Skipping language-empty repository: "
                f"{repo_name}"
            )
            continue

        counted_repositories += 1

        print(
            f"  repository weight: 1/{counted_repositories}"
        )

        for language, byte_count in language_bytes.items():
            repo_share = (
                byte_count / repo_total
            )

            scores[language] = (
                scores.get(
                    language,
                    0.0,
                )
                + repo_share
            )

    return (
        scores,
        counted_repositories,
    )


def top_languages(
    scores: dict[str, float],
    repository_count: int,
    limit: int = 5,
) -> list[dict[str, float | str]]:
    """
    Convert accumulated per-repository shares into percentages.

    Since every counted repository contributes a total weight of 1,
    dividing each language score by the number of repositories gives
    its average repository-weighted presence.
    """

    if repository_count <= 0:
        return []

    ranked = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    result: list[
        dict[str, float | str]
    ] = []

    for language, score in ranked[:limit]:
        percentage = (
            score / repository_count
        ) * 100

        result.append(
            {
                "name": language,
                "percentage": percentage,
            }
        )

    return result


# ---------------------------------------------------------------------------
# MORI opinions
# ---------------------------------------------------------------------------

def mori_language_verdict(
    languages: list[
        dict[str, float | str]
    ],
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

    top_percentage = float(
        languages[0]["percentage"]
    )

    # A genuinely dominant repository-weighted language still
    # deserves special judgement.
    if top_percentage >= 60:
        dominant_verdicts = {
            "C": (
                "You were offered abstractions. "
                "You declined."
            ),
            "C++": (
                "Memory management has become recreational."
            ),
            "C#": (
                "Enterprise sorcery has consumed the operator."
            ),
            "Python": (
                "Indentation appears to have become a lifestyle."
            ),
            "JavaScript": (
                "Chaos has achieved majority control."
            ),
            "TypeScript": (
                "JavaScript has been placed under supervision. "
                "Good."
            ),
            "Rust": (
                "The borrow checker now appears to be your guardian."
            ),
            "Go": (
                "Suspiciously practical. "
                "I expected more drama."
            ),
            "Java": (
                "The factories have achieved self-governance."
            ),
            "Shell": (
                "The shell script is no longer a script. "
                "It is infrastructure."
            ),
            "PowerShell": (
                "The command line has become contractual paperwork."
            ),
            "HTML": (
                "You have apparently committed to moving boxes."
            ),
            "CSS": (
                "The boxes have won."
            ),
            "Nix": (
                "Oh dear. "
                "It has become ideological."
            ),
            "SQL": (
                "The database has become the primary "
                "conversational partner."
            ),
            "Assembly": (
                "You descended beneath abstraction "
                "and chose to remain there."
            ),
        }

        return dominant_verdicts.get(
            top,
            f"{top} has consumed the operator. "
            "I assume this was intentional.",
        )

    top_names = set(
        names[:5]
    )

    if {
        "C#",
        "TypeScript",
    }.issubset(top_names):
        return (
            "Full-stack tendencies detected. "
            "Regrettably competent."
        )

    if {
        "Python",
        "Shell",
    }.issubset(top_names):
        return (
            "Automation has consumed the operator. "
            "I approve, cautiously."
        )

    if {
        "C",
        "C++",
    }.issubset(top_names):
        return (
            "Pointers and consequences. "
            "A personality trait, apparently."
        )

    if {
        "HTML",
        "CSS",
    }.issubset(top_names):
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
# ASCII bar helpers
# ---------------------------------------------------------------------------

def ascii_bar_counts(
    percentage: float,
    width: int = 40,
) -> tuple[int, int]:
    filled_count = round(
        (percentage / 100)
        * width
    )

    filled_count = max(
        0,
        min(
            width,
            filled_count,
        ),
    )

    empty_count = (
        width - filled_count
    )

    return (
        filled_count,
        empty_count,
    )


def render_ascii_bar(
    *,
    x: int,
    y: int,
    percentage: float,
    width_chars: int,
    index: int,
) -> list[str]:
    """
    Draw an animated terminal-style ASCII progress bar.

    The empty rail is always visible.

    The purple block section is revealed from left to right through
    an animated clipping rectangle.
    """

    char_width = 6.6
    bracket_width = 8

    filled_count, _ = ascii_bar_counts(
        percentage,
        width=width_chars,
    )

    rail_text = (
        "░" * width_chars
    )

    fill_text = (
        "█" * filled_count
    )

    content_x = (
        x + bracket_width
    )

    bar_pixel_width = (
        width_chars
        * char_width
    )

    final_fill_width = (
        filled_count
        * char_width
    )

    closing_x = (
        content_x
        + bar_pixel_width
    )

    clip_id = (
        f"language-fill-{index}"
    )

    # Each language starts slightly after the previous one.
    delay = (
        index * 0.14
    )

    duration = 0.65

    parts = [
        "<defs>",

        (
            f'<clipPath '
            f'id="{clip_id}">'
            f'<rect '
            f'x="{content_x}" '
            f'y="{y - 13}" '
            f'width="{final_fill_width:.1f}" '
            f'height="18">'
            f'<animate '
            f'attributeName="width" '
            f'from="0" '
            f'to="{final_fill_width:.1f}" '
            f'begin="{delay}s" '
            f'dur="{duration}s" '
            f'fill="freeze" '
            f'calcMode="spline" '
            f'keyTimes="0;1" '
            f'keySplines="0.2 0.8 0.2 1"'
            f'/>'
            f'</rect>'
            f'</clipPath>'
        ),

        "</defs>",

        # [
        (
            f'<text '
            f'x="{x}" '
            f'y="{y}" '
            f'fill="{MUTED}" '
            f'font-family="{MONO}" '
            f'font-size="11">'
            f'['
            f'</text>'
        ),

        # ░░░░░░░░░░░░░░░░░░░░
        (
            f'<text '
            f'x="{content_x}" '
            f'y="{y}" '
            f'fill="{MUTED}" '
            f'font-family="{MONO}" '
            f'font-size="11">'
            f'{rail_text}'
            f'</text>'
        ),

        # ███████...
        (
            f'<text '
            f'x="{content_x}" '
            f'y="{y}" '
            f'fill="{ACCENT_BRIGHT}" '
            f'font-family="{MONO}" '
            f'font-size="11" '
            f'clip-path="url(#{clip_id})">'
            f'{fill_text}'
            f'</text>'
        ),

        # ]
        (
            f'<text '
            f'x="{closing_x:.1f}" '
            f'y="{y}" '
            f'fill="{MUTED}" '
            f'font-family="{MONO}" '
            f'font-size="11">'
            f']'
            f'</text>'
        ),
    ]

    return parts


# ---------------------------------------------------------------------------
# SVG rendering
# ---------------------------------------------------------------------------

def render_svg(
    username: str,
    languages: list[
        dict[str, float | str]
    ],
    repository_count: int,
) -> str:
    width = 690
    height = 245

    verdict = escape(
        mori_language_verdict(
            languages
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

        (
            f'<title id="title">'
            f'{escape(username)} '
            f'repository-weighted language distribution'
            f'</title>'
        ),

        (
            f'<desc id="desc">'
            f'MORI repository-weighted language analysis '
            f'across {repository_count} repositories for '
            f'{escape(username)}.'
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
        f'repository-weighted audit'
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
        parts.append(
            f'<text '
            f'x="48" '
            f'y="108" '
            f'fill="{TEXT}" '
            f'font-family="{MONO}" '
            f'font-size="12">'
            f'No language data available.'
            f'</text>'
        )

    else:
        label_x = 48
        bar_x = 170
        percent_x = 632

        # Nice long terminal bars.
        bar_chars = 40

        # Five rows fit neatly into the existing panel.
        row_start = 72
        row_gap = 20

        for index, language in enumerate(
            languages
        ):
            name = escape(
                str(
                    language["name"]
                )
            )

            percentage = float(
                language["percentage"]
            )

            row_y = (
                row_start
                + index * row_gap
            )

            # Language name
            parts.append(
                f'<text '
                f'x="{label_x}" '
                f'y="{row_y}" '
                f'fill="{TEXT}" '
                f'font-family="{MONO}" '
                f'font-size="11" '
                f'font-weight="700">'
                f'{name}'
                f'</text>'
            )

            # Animated ASCII bar
            parts.extend(
                render_ascii_bar(
                    x=bar_x,
                    y=row_y,
                    percentage=percentage,
                    width_chars=bar_chars,
                    index=index,
                )
            )

            # Percentage
            parts.append(
                f'<text '
                f'x="{percent_x}" '
                f'y="{row_y}" '
                f'text-anchor="end" '
                f'fill="{MUTED}" '
                f'font-family="{MONO}" '
                f'font-size="10">'
                f'{percentage:.1f}%'
                f'</text>'
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

            # Mori
            f'<text '
            f'x="28" '
            f'y="207" '
            f'fill="{ACCENT}" '
            f'font-family="{MONO}" '
            f'font-size="12" '
            f'font-weight="700">'
            f'{escape(MORI)}'
            f'</text>',

            # Verdict
            f'<text '
            f'x="110" '
            f'y="207" '
            f'fill="{TEXT}" '
            f'font-family="{MONO}" '
            f'font-size="11">'
            f'{verdict}'
            f'</text>',

            # Footer
            f'<text '
            f'x="{width - 28}" '
            f'y="222" '
            f'text-anchor="end" '
            f'fill="{MUTED}" '
            f'font-family="{MONO}" '
            f'font-size="9">'
            f'mori dialect assessment // '
            f'{repository_count} repositories'
            f'</text>',

            "</svg>",
        ]
    )

    return (
        "\n".join(parts)
        + "\n"
    )


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
        repos = (
            fetch_owned_repositories(
                token,
                username,
            )
        )

        (
            language_scores,
            repository_count,
        ) = calculate_repo_weighted_languages(
            token,
            repos,
        )

        languages = top_languages(
            language_scores,
            repository_count,
            limit=5,
        )

        svg = render_svg(
            username=username,
            languages=languages,
            repository_count=repository_count,
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
            f"MORI language card: {exc}",
            file=sys.stderr,
        )

        return 1

    print(
        f"Generated: "
        f"{OUTPUT_PATH.relative_to(ROOT)}"
    )

    print(
        f"Repositories included: "
        f"{repository_count}"
    )

    if languages:
        print(
            "Repository-weighted languages:"
        )

        for item in languages:
            print(
                f"  - {item['name']}: "
                f"{float(item['percentage']):.1f}%"
            )

    else:
        print(
            "No language data available."
        )

    print(
        "MORI verdict: "
        f"{mori_language_verdict(languages)}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
