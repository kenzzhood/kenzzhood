#!/usr/bin/env python3
"""Generate capability and research maps in paired theme variants."""

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
    truncate,
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
    """Render the three-domain capability matrix."""
    header, divider_y = section_header(
        WIDTH,
        "What I build with",
        "Vision, spatial interfaces, and AI systems shipped as real products.",
    )
    card_y = divider_y + 28
    card_w = 252
    card_h = 232
    gap = 20
    height = card_y + card_h + PAD

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
        x = PAD + index * (card_w + gap)
        accent_class = ("green", "cyan", "violet")[index]
        tools = group["tools"]
        pipeline = group["pipeline"]
        statement_lines = textwrap.wrap(
            str(group["statement"]),
            width=34,
            break_long_words=False,
        )[:2]

        card = [
            f'<rect x="{x}" y="{card_y}" width="{card_w}" height="{card_h}" '
            'rx="12" class="surface" stroke="var(--line)" stroke-width="1"/>',
            f'<text x="{x + 18}" y="{card_y + 28}" class="{accent_class}" '
            f'font-size="10">{esc(group["index"])}  {esc(group["name"])}</text>',
            f'<text x="{x + 18}" y="{card_y + 58}" class="text" '
            f'font-size="12" font-weight="700">{esc(statement_lines[0])}</text>',
            f'<text x="{x + 18}" y="{card_y + 78}" class="muted" font-size="11">'
            f'{esc(statement_lines[1] if len(statement_lines) > 1 else "")}</text>',
            f'<line x1="{x + 18}" y1="{card_y + 96}" x2="{x + card_w - 18}" '
            f'y2="{card_y + 96}" class="lineSoft" stroke-width="1"/>',
        ]

        pipe_y = card_y + 126
        node_w = 62
        for pipe_index, item in enumerate(pipeline):
            node_x = x + 18 + pipe_index * 72
            card.append(
                f'<rect x="{node_x}" y="{pipe_y - 16}" width="{node_w}" height="28" '
                'rx="6" class="surface2" stroke="var(--line)" stroke-width=".8"/>'
                f'<text x="{node_x + node_w / 2}" y="{pipe_y + 2}" class="text" '
                f'font-size="9" text-anchor="middle">{esc(item)}</text>'
            )
            if pipe_index < len(pipeline) - 1:
                card.append(
                    f'<path d="M{node_x + node_w + 3} {pipe_y - 2}h7" '
                    'class="line" stroke-width="1" fill="none"/>'
                )

        card.append(
            f'<text x="{x + 18}" y="{card_y + 172}" class="faint" '
            'font-size="9">Stack</text>'
        )
        chip_x = x + 18.0
        chip_y = card_y + 182.0
        row_start_x = chip_x
        for tool in tools:
            markup, chip_w = chip(chip_x, chip_y, tool, height=21)
            if chip_x + chip_w > x + card_w - 14:
                chip_x = row_start_x
                chip_y += 27
                markup, chip_w = chip(chip_x, chip_y, tool, height=21)
            card.append(markup)
            chip_x += chip_w + 7

        parts.append(delayed("".join(card), 0.16 + index * 0.1))

    parts.append("</svg>")
    return parts


def render_research(theme_name: str) -> list[str]:
    """Render the research-to-product pipeline."""
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

    start_x = PAD
    for index, item in enumerate(RESEARCH_PIPELINE):
        x = start_x + index * (node_w + gap)
        accent_class = ("green", "cyan", "violet", "green")[index]
        inner = (
            f'<rect x="{x}" y="{node_y}" width="{node_w}" height="86" rx="12" '
            'class="surface" stroke="var(--line)" stroke-width="1"/>'
            f'<text x="{x + 15}" y="{node_y + 24}" class="{accent_class}" '
            f'font-size="10">{esc(item["step"])}</text>'
            f'<text x="{x + 15}" y="{node_y + 48}" class="text" '
            f'font-size="13" font-weight="700">{esc(item["title"])}</text>'
            f'<text x="{x + 15}" y="{node_y + 70}" class="muted" '
            f'font-size="10">{esc(truncate(item["detail"], 28))}</text>'
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
