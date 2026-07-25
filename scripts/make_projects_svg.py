#!/usr/bin/env python3
"""Generate locally hosted, linkable project cards."""

from __future__ import annotations

import argparse
import sys
import textwrap

from common import (
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
from config import CANVAS_WIDTH, CASE_STUDIES, PROJECTS_DIR

logger = setup_logging("make_projects")

WIDTH = CANVAS_WIDTH
HEIGHT = 210


def _summary_lines(summary: str) -> list[str]:
    return textwrap.wrap(summary, width=68, break_long_words=False)[:2]


def render(project: dict[str, object], theme_name: str) -> list[str]:
    """Render one project card."""
    name = str(project["name"])
    category = str(project["category"])
    index = str(project["index"])
    summary = str(project["summary"])
    pipeline = list(project["pipeline"])
    stack = list(project["stack"])
    signal = str(project["signal"])

    parts: list[str] = [
        premium_svg_open(
            WIDTH,
            HEIGHT,
            f"{name} — {category}",
            f"{summary} Flow: {' → '.join(map(str, pipeline))}.",
        ),
        premium_css(get_theme(theme_name)),
    ]
    parts.extend(premium_frame(WIDTH, HEIGHT))

    parts.append(
        delayed(
            f'<text x="32" y="34" class="faint" font-size="10">'
            f"Project {esc(index)}</text>"
            f'<text x="32" y="66" class="text" font-size="22" '
            f'font-weight="700">{esc(name)}</text>'
            f'<text x="32" y="88" class="cyan" font-size="11">'
            f"{esc(category)}</text>",
            0.08,
        )
    )

    summary_markup = "".join(
        f'<text x="210" y="{44 + line_index * 20}" class="text" font-size="12">'
        f"{esc(line)}</text>"
        for line_index, line in enumerate(_summary_lines(summary))
    )
    parts.append(delayed(summary_markup, 0.14))

    parts.append(
        '<line x1="32" y1="108" x2="828" y2="108" class="line draw" '
        'pathLength="1" stroke-width="1" style="animation-delay:.2s"/>'
    )

    node_y = 140
    node_w = 130
    node_gap = 16
    for pipe_index, item in enumerate(pipeline):
        x = 32 + pipe_index * (node_w + node_gap)
        accent_class = ("green", "cyan", "violet", "green")[pipe_index % 4]
        parts.append(
            delayed(
                f'<rect x="{x}" y="{node_y - 16}" width="{node_w}" height="30" '
                'rx="7" class="surface2" stroke="var(--line)" stroke-width=".8"/>'
                f'<circle cx="{x + 12}" cy="{node_y - 1}" r="2.4" '
                f'class="{accent_class}"/>'
                f'<text x="{x + 22}" y="{node_y + 3}" class="text" '
                f'font-size="9.5">{esc(truncate(item, 16))}</text>',
                0.26 + pipe_index * 0.06,
            )
        )
        if pipe_index < len(pipeline) - 1:
            arrow_x = x + node_w + 3
            parts.append(
                f'<path d="M{arrow_x} {node_y - 1}h8l-3-3m3 3-3 3" '
                'fill="none" class="line draw" pathLength="1" stroke-width="1" '
                f'style="animation-delay:{0.3 + pipe_index * 0.06:.2f}s"/>'
            )

    stack_x = 32.0
    parts.append(
        '<text x="32" y="186" class="faint" font-size="9">Stack</text>'
    )
    stack_x = 78.0
    for item in stack:
        item_width = max(46, len(str(item)) * 6.0 + 16)
        parts.append(
            f'<rect x="{stack_x:.1f}" y="170" width="{item_width:.1f}" '
            'height="22" rx="6" class="surface" stroke="var(--line)" stroke-width=".8"/>'
            f'<text x="{stack_x + item_width / 2:.1f}" y="185" '
            f'class="muted" font-size="9" text-anchor="middle">{esc(item)}</text>'
        )
        stack_x += item_width + 7

    parts.append(
        delayed(
            f'<text x="828" y="186" class="muted" font-size="10" '
            f'text-anchor="end">{esc(truncate(signal, 52))}</text>',
            0.55,
            "fade",
        )
    )

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
        logger.exception("failed to generate project cards: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
