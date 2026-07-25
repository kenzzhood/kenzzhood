#!/usr/bin/env python3
"""Generate locally hosted, linkable proof-of-work project cards."""

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
HEIGHT = 230


def _summary_lines(summary: str) -> list[str]:
    return textwrap.wrap(summary, width=67, break_long_words=False)[:2]


def render(project: dict[str, object], theme_name: str) -> list[str]:
    """Render one flagship-project proof card."""
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
            f"{summary} Architecture: {' to '.join(map(str, pipeline))}.",
        ),
        premium_css(get_theme(theme_name)),
    ]
    parts.extend(premium_frame(WIDTH, HEIGHT, grid=False))

    # Project identity and outcome statement
    parts.append(
        delayed(
            f'<text x="32" y="35" class="green" font-size="9.5" '
            f'letter-spacing="1.6">SELECTED SYSTEM // {esc(index)}</text>'
            f'<text x="32" y="72" class="text" font-size="24" '
            f'font-weight="700">{esc(name)}</text>'
            f'<text x="32" y="94" class="cyan" font-size="9.5" '
            f'letter-spacing="1.3">{esc(category)}</text>',
            0.08,
        )
    )

    summary_markup = "".join(
        f'<text x="228" y="{48 + line_index * 21}" class="text" font-size="12">'
        f"{esc(line)}</text>"
        for line_index, line in enumerate(_summary_lines(summary))
    )
    parts.append(delayed(summary_markup, 0.16))

    parts.append(
        '<line x1="32" y1="118" x2="828" y2="118" class="line draw" '
        'pathLength="1" stroke-width="1" style="animation-delay:.24s"/>'
    )

    # Architecture pipeline
    node_y = 151
    node_w = 126
    node_gap = 18
    pipeline_x = 32
    for pipe_index, item in enumerate(pipeline):
        x = pipeline_x + pipe_index * (node_w + node_gap)
        accent_class = ("green", "cyan", "violet", "green")[pipe_index % 4]
        parts.append(
            delayed(
                f'<rect x="{x}" y="{node_y - 17}" width="{node_w}" height="32" '
                'rx="7" class="surface2" stroke="var(--line)" stroke-width=".8"/>'
                f'<circle cx="{x + 13}" cy="{node_y - 1}" r="2.5" '
                f'class="{accent_class}"/>'
                f'<text x="{x + 23}" y="{node_y + 3}" class="text" '
                f'font-size="9">{esc(truncate(item, 16))}</text>',
                0.3 + pipe_index * 0.07,
            )
        )
        if pipe_index < len(pipeline) - 1:
            arrow_x = x + node_w + 4
            parts.append(
                f'<path d="M{arrow_x} {node_y - 1}h8l-3-3m3 3-3 3" '
                'fill="none" class="line draw" pathLength="1" stroke-width="1" '
                f'style="animation-delay:{0.34 + pipe_index * 0.07:.2f}s"/>'
            )

    # Technical stack rail
    stack_x = 32
    stack_y = 195
    parts.append(
        '<text x="32" y="203" class="faint" font-size="8.5" '
        'letter-spacing="1.2">STACK</text>'
    )
    stack_x += 52
    for stack_index, item in enumerate(stack):
        item_width = max(48, len(str(item)) * 6.1 + 18)
        parts.append(
            f'<rect x="{stack_x:.1f}" y="{stack_y - 13}" width="{item_width:.1f}" '
            'height="24" rx="6" class="surface" stroke="var(--line)" stroke-width=".8"/>'
            f'<text x="{stack_x + item_width / 2:.1f}" y="{stack_y + 3}" '
            f'class="muted" font-size="8.5" text-anchor="middle">{esc(item)}</text>'
        )
        stack_x += item_width + 8

    parts.append(
        delayed(
            '<text x="828" y="203" class="faint" font-size="8.5" '
            'letter-spacing="1.1" text-anchor="end">TECHNICAL SIGNAL</text>'
            f'<text x="828" y="219" class="muted" font-size="9.2" '
            f'text-anchor="end">{esc(truncate(signal, 58))}</text>',
            0.62,
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
