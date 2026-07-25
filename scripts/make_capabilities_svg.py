#!/usr/bin/env python3
"""Generate capability and research maps in paired theme variants."""

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


def _section_header(kicker: str, title: str, subtitle: str) -> str:
    return (
        f'<text x="32" y="36" class="green" font-size="10">'
        f"{esc(kicker)}</text>"
        f'<text x="32" y="68" class="text" font-size="22" '
        f'font-weight="700">{esc(title)}</text>'
        f'<text x="32" y="92" class="muted" font-size="12">{esc(subtitle)}</text>'
        '<line x1="32" y1="112" x2="828" y2="112" class="line draw" '
        'pathLength="1" stroke-width="1" style="animation-delay:.1s"/>'
    )


def render_capabilities(theme_name: str) -> list[str]:
    """Render the three-domain capability matrix."""
    height = 400
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
    parts.append(
        _section_header(
            "Focus",
            "Where the work sits.",
            "Vision, spatial interfaces, and AI systems shipping as products.",
        )
    )

    card_y = 136
    card_w = 252
    card_h = 232
    gap = 20
    for index, group in enumerate(CAPABILITY_GROUPS):
        x = 32 + index * (card_w + gap)
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
            f'<text x="{x + 18}" y="{card_y + 170}" class="faint" '
            'font-size="9">Stack</text>'
        )
        for tool_index, tool in enumerate(tools):
            col = tool_index % 2
            row = tool_index // 2
            tool_x = x + 18 + col * 110
            tool_y = card_y + 194 + row * 22
            card.append(
                f'<text x="{tool_x}" y="{tool_y}" class="muted" '
                f'font-size="10.5">{esc(tool)}</text>'
            )

        parts.append(delayed("".join(card), 0.16 + index * 0.1))

    parts.append("</svg>")
    return parts


def render_research(theme_name: str) -> list[str]:
    """Render the research-to-product pipeline."""
    height = 250
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
    parts.append(
        _section_header(
            "Research",
            "From pixels to presence.",
            "The same loop shows up in retail XR, holography, and product AI.",
        )
    )

    start_x = 32
    node_y = 132
    node_w = 184
    gap = 20
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
