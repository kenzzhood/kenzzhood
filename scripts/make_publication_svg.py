#!/usr/bin/env python3
"""Generate a single publication panel matching the profile design system."""

from __future__ import annotations

import argparse
import sys
import textwrap

from common import (
    PAD,
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
    PUBLICATION,
    PUBLICATION_DARK_SVG,
    PUBLICATION_LIGHT_SVG,
)

logger = setup_logging("make_publication")

WIDTH = CANVAS_WIDTH
HEIGHT = 148


def render(theme_name: str) -> list[str]:
    """One quiet IEEE publication card."""
    title = PUBLICATION["title"]
    venue = PUBLICATION["venue"]
    title_lines = textwrap.wrap(title, width=78, break_long_words=False)[:2]

    header, divider_y = section_header(
        WIDTH,
        "IEEE publication",
        corner=venue,
        accent="cyan",
    )

    parts: list[str] = [
        premium_svg_open(
            WIDTH,
            HEIGHT,
            f"Publication — {venue}",
            title,
        ),
        premium_css(get_theme(theme_name)),
    ]
    parts.extend(premium_frame(WIDTH, HEIGHT))
    parts.append(header)

    y = divider_y + 32
    title_markup = "".join(
        f'<text x="{PAD}" y="{y + i * 22}" class="text" font-size="13.5" '
        f'font-weight="600">{esc(line)}</text>'
        for i, line in enumerate(title_lines)
    )
    parts.append(delayed(title_markup, 0.14))

    parts.append(
        delayed(
            f'<text x="{PAD}" y="{HEIGHT - 28}" class="muted" font-size="11">'
            "Voice + gesture holographic interaction · "
            f'<tspan class="cyan">{esc(venue)}</tspan>'
            " · open code</text>",
            0.28,
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
    targets = {
        "dark": PUBLICATION_DARK_SVG,
        "light": PUBLICATION_LIGHT_SVG,
    }
    selected = targets if args.theme == "all" else {args.theme: targets[args.theme]}
    try:
        for theme_name, output in selected.items():
            write_svg(output, render(theme_name), logger)
    except Exception as exc:  # noqa: BLE001
        logger.exception("failed to generate publication panel: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
