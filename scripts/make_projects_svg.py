#!/usr/bin/env python3
"""Generate compact, linkable project tiles (paired two-up in the README)."""

from __future__ import annotations

import argparse
import sys
import textwrap

from common import (
    chip,
    delayed,
    esc,
    get_theme,
    premium_css,
    premium_frame,
    premium_svg_open,
    setup_logging,
    truncate,
    write_svg,
)
from config import CASE_STUDIES, PROJECTS_DIR

logger = setup_logging("make_projects")

WIDTH = 406
HEIGHT = 204
PAD = 20
MAX_STACK_CHIPS = 3
SUMMARY_WIDTH_CHARS = 48
SUMMARY_MAX_LINES = 3


def _summary_lines(summary: str) -> list[str]:
    """Wrap to a fixed line budget; never drop trailing content silently."""
    lines = textwrap.wrap(summary, width=SUMMARY_WIDTH_CHARS, break_long_words=False)
    if len(lines) <= SUMMARY_MAX_LINES:
        return lines
    kept = lines[: SUMMARY_MAX_LINES - 1]
    remainder = " ".join(lines[SUMMARY_MAX_LINES - 1 :])
    kept.append(truncate(remainder, SUMMARY_WIDTH_CHARS))
    return kept


def render(project: dict[str, object], theme_name: str) -> list[str]:
    """Render one compact project tile."""
    name = str(project["name"])
    category = str(project["category"])
    index = str(project["index"])
    summary = str(project["summary"])
    stack = list(project["stack"])[:MAX_STACK_CHIPS]

    parts: list[str] = [
        premium_svg_open(WIDTH, HEIGHT, f"{name} — {category}", summary),
        premium_css(get_theme(theme_name)),
    ]
    parts.extend(premium_frame(WIDTH, HEIGHT))

    parts.append(
        delayed(
            f'<text x="{PAD}" y="28" class="faint" font-size="9.5" letter-spacing="1">'
            f"PROJECT {esc(index)}</text>"
            f'<text x="{WIDTH - PAD}" y="28" class="green" font-size="9.5" '
            f'text-anchor="end">↗</text>'
            f'<text x="{PAD}" y="54" class="text" font-size="18" '
            f'font-weight="700">{esc(name)}</text>'
            f'<text x="{PAD}" y="74" class="cyan" font-size="10.5">'
            f"{esc(category)}</text>",
            0.08,
        )
    )

    parts.append(
        f'<line x1="{PAD}" y1="90" x2="{WIDTH - PAD}" y2="90" class="line draw" '
        'pathLength="1" stroke-width="1" style="animation-delay:.16s"/>'
    )

    summary_markup = "".join(
        f'<text x="{PAD}" y="{112 + line_index * 18}" class="muted" font-size="11">'
        f"{esc(line)}</text>"
        for line_index, line in enumerate(_summary_lines(summary))
    )
    parts.append(delayed(summary_markup, 0.2))

    chip_x = float(PAD)
    chip_y = 170.0
    row_start_x = chip_x
    for tool_index, tool in enumerate(stack):
        markup, chip_w = chip(chip_x, chip_y, tool, height=21)
        if chip_x + chip_w > WIDTH - PAD:
            chip_x = row_start_x
            chip_y += 27
            markup, chip_w = chip(chip_x, chip_y, tool, height=21)
        parts.append(delayed(markup, 0.28 + tool_index * 0.05, "fade"))
        chip_x += chip_w + 7

    parts.append("</svg>")
    return parts


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--theme",
        choices=("all", "dark", "light"),
        default="all",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    themes = ("dark", "light") if args.theme == "all" else (args.theme,)
    try:
        for project in CASE_STUDIES:
            slug = str(project["slug"])
            for theme_name in themes:
                output = PROJECTS_DIR / f"{slug}-{theme_name}.svg"
                write_svg(output, render(project, theme_name), logger)
    except Exception as exc:  # noqa: BLE001
        logger.exception("failed to generate project tiles: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
