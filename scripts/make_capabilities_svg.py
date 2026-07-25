#!/usr/bin/env python3
"""Generate a flat three-column skills panel (no nested cards)."""

from __future__ import annotations

import argparse
import sys
import textwrap

from common import (
    PAD,
    chip,
    delayed,
    esc,
    get_theme,
    premium_css,
    premium_frame,
    premium_svg_open,
    section_header,
    setup_logging,
    write_svg,
)
from config import (
    CANVAS_WIDTH,
    CAPABILITIES_DARK_SVG,
    CAPABILITIES_LIGHT_SVG,
    CAPABILITY_GROUPS,
    RESEARCH_DARK_SVG,
    RESEARCH_LIGHT_SVG,
    RESEARCH_PIPELINE,
)

logger = setup_logging("make_capabilities")

WIDTH = CANVAS_WIDTH


def render_capabilities(theme_name: str) -> list[str]:
    """Render three flat skill columns — title, statement, chips. No nested boxes."""
    header, divider_y = section_header(
        WIDTH,
        "What I build with",
        "Vision, spatial interfaces, and AI systems shipped as products.",
    )
    col_top = divider_y + 28
    col_w = 248
    gap = 26
    # statement (2 lines) + chips (2 rows) + breathing room
    col_h = 148
    height = col_top + col_h + PAD

    parts: list[str] = [
        premium_svg_open(
            WIDTH,
            height,
            "What I build",
            "Vision and 3D, spatial XR, and AI product systems.",
        ),
        premium_css(get_theme(theme_name)),
    ]
    parts.extend(premium_frame(WIDTH, height))
    parts.append(header)

    for index, group in enumerate(CAPABILITY_GROUPS):
        x = PAD + index * (col_w + gap)
        accent = ("green", "cyan", "violet")[index]
        tools = list(group["tools"])
        statement_lines = textwrap.wrap(
            str(group["statement"]),
            width=34,
            break_long_words=False,
        )[:2]

        # Soft column separator (not a card border)
        if index > 0:
            parts.append(
                f'<line x1="{x - gap / 2:.1f}" y1="{col_top}" '
                f'x2="{x - gap / 2:.1f}" y2="{col_top + col_h - 8}" '
                'class="lineSoft" stroke-width="1"/>'
            )

        column = [
            f'<text x="{x}" y="{col_top + 14}" class="{accent}" font-size="10" '
            f'letter-spacing="1">{esc(group["index"])}</text>',
            f'<text x="{x + 28}" y="{col_top + 14}" class="text" font-size="13" '
            f'font-weight="700">{esc(group["name"])}</text>',
        ]
        for line_i, line in enumerate(statement_lines):
            column.append(
                f'<text x="{x}" y="{col_top + 44 + line_i * 18}" class="muted" '
                f'font-size="11.5">{esc(line)}</text>'
            )

        # Fixed chip baseline so all three columns align regardless of copy length.
        chip_x = float(x)
        chip_y = float(col_top + 92)
        row_start = chip_x
        for tool in tools:
            markup, chip_w = chip(chip_x, chip_y, tool, height=22)
            if chip_x + chip_w > x + col_w:
                chip_x = row_start
                chip_y += 28
                markup, chip_w = chip(chip_x, chip_y, tool, height=22)
            column.append(markup)
            chip_x += chip_w + 7

        parts.append(delayed("".join(column), 0.14 + index * 0.08))

    parts.append("</svg>")
    return parts


def render_research(theme_name: str) -> list[str]:
    """Keep a light research strip available for optional use."""
    header, divider_y = section_header(
        WIDTH,
        "From pixels to presence",
        "The same loop shows up in retail XR, holography, and product AI.",
        accent="cyan",
    )
    node_y = divider_y + 28
    node_w = 184
    gap = 20
    height = node_y + 86 + PAD

    parts: list[str] = [
        premium_svg_open(
            WIDTH,
            height,
            "Research path",
            "From perception and 3D reconstruction to multimodal AI and spatial UX.",
        ),
        premium_css(get_theme(theme_name)),
    ]
    parts.extend(premium_frame(WIDTH, height))
    parts.append(header)

    for index, item in enumerate(RESEARCH_PIPELINE):
        x = PAD + index * (node_w + gap)
        accent = ("green", "cyan", "violet", "green")[index]
        inner = (
            f'<rect x="{x}" y="{node_y}" width="{node_w}" height="86" rx="12" '
            'class="surface" stroke="var(--line)" stroke-width="1"/>'
            f'<text x="{x + 15}" y="{node_y + 24}" class="{accent}" '
            f'font-size="10">{esc(item["step"])}</text>'
            f'<text x="{x + 15}" y="{node_y + 48}" class="text" '
            f'font-size="13" font-weight="700">{esc(item["title"])}</text>'
            f'<text x="{x + 15}" y="{node_y + 70}" class="muted" '
            f'font-size="10">{esc(item["detail"])}</text>'
        )
        parts.append(delayed(inner, 0.16 + index * 0.08))
        if index < len(RESEARCH_PIPELINE) - 1:
            arrow_x = x + node_w
            parts.append(
                f'<path d="M{arrow_x + 3} {node_y + 43}h14l-4-4m4 4-4 4" '
                'fill="none" class="line draw" pathLength="1" stroke-width="1" '
                f'style="animation-delay:{0.3 + index * 0.08:.2f}s"/>'
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
    targets = {
        "dark": (CAPABILITIES_DARK_SVG, RESEARCH_DARK_SVG),
        "light": (CAPABILITIES_LIGHT_SVG, RESEARCH_LIGHT_SVG),
    }
    selected = targets if args.theme == "all" else {args.theme: targets[args.theme]}
    try:
        for theme_name, (cap_path, research_path) in selected.items():
            write_svg(cap_path, render_capabilities(theme_name), logger)
            write_svg(research_path, render_research(theme_name), logger)
    except Exception as exc:  # noqa: BLE001
        logger.exception("failed to generate capability maps: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
