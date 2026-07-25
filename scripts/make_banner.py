#!/usr/bin/env python3
"""
Generate an animated terminal startup banner SVG.

Includes a typing prompt, blinking cursor, and animated separator dashes.
One-shot typewriter on the banner line; cursor blinks indefinitely.

Usage
-----
    python scripts/make_banner.py
"""

from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

from common import setup_logging, svg_background, svg_open, svg_titlebar, write_svg
from config import ABOUT, BANNER_SVG, COLORS, NAME, PROMPT_HOST, ROLE, SEPARATOR_SVG

logger = setup_logging("make_banner")


def build_banner_svg() -> list[str]:
    """Build the startup banner SVG parts."""
    w, h = 860, 96
    pad = 22
    titlebar_h = 30
    ink = COLORS["ink"]
    muted = COLORS["muted"]
    accent = COLORS["accent"]
    frame = COLORS["frame"]

    line1 = f"{PROMPT_HOST}:~$ boot --profile"
    line2 = f"{NAME} · {ROLE}"
    line3 = ABOUT if len(ABOUT) < 90 else ABOUT[:87] + "…"

    parts: list[str] = [svg_open(w, h)]
    parts.extend(svg_background(w, h))
    parts.extend(svg_titlebar(w, f"{PROMPT_HOST}: ~$ ./boot.sh", titlebar_h, pad))

    y1 = titlebar_h + 22
    # Prompt types in
    parts.append(
        f'<text x="{pad}" y="{y1}" fill="{muted}" font-size="12" opacity="0">'
        f"{html.escape(line1)}"
        f'<animate attributeName="opacity" from="0" to="1" begin="0.1s" '
        f'dur="0.3s" fill="freeze"/></text>'
    )
    # Name line slides in
    parts.append(
        f'<text x="{pad}" y="{y1 + 22}" fill="{accent}" font-size="16" font-weight="700" '
        f'opacity="0" transform="translate(0,4)">{html.escape(line2)}'
        f'<animate attributeName="opacity" from="0" to="1" begin="0.4s" '
        f'dur="0.4s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 4" to="0 0" begin="0.4s" dur="0.4s" fill="freeze"/></text>'
    )
    parts.append(
        f'<text x="{pad}" y="{y1 + 42}" fill="{ink}" font-size="12" opacity="0">'
        f"{html.escape(line3)}"
        f'<animate attributeName="opacity" from="0" to="1" begin="0.7s" '
        f'dur="0.4s" fill="freeze"/></text>'
    )
    # Blinking cursor
    parts.append(
        f'<rect x="{pad + len(line3) * 7.1:.1f}" y="{y1 + 30}" width="7" height="12" '
        f'fill="{ink}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
        f'dur="1s" repeatCount="indefinite"/></rect>'
    )
    # Subtle bottom rule
    parts.append(
        f'<line x1="{pad}" y1="{h - 10}" x2="{w - pad}" y2="{h - 10}" '
        f'stroke="{frame}" stroke-opacity="0.5">'
        f'<animate attributeName="stroke-dasharray" from="0 {w}" to="{w} 0" '
        f'begin="0.2s" dur="0.8s" fill="freeze"/></line>'
    )
    parts.append("</svg>")
    return parts


def build_separator_svg() -> list[str]:
    """Animated dashed separator line."""
    w, h = 860, 24
    frame = COLORS["frame"]
    accent = COLORS["accent"]
    parts: list[str] = [svg_open(w, h)]
    parts.append(f'<rect width="{w}" height="{h}" fill="none"/>')
    mid = h / 2
    parts.append(
        f'<line x1="40" y1="{mid}" x2="{w - 40}" y2="{mid}" '
        f'stroke="{frame}" stroke-width="1" stroke-dasharray="4 6">'
        f'<animate attributeName="stroke-dashoffset" from="60" to="0" '
        f'dur="1.2s" fill="freeze"/></line>'
    )
    parts.append(
        f'<circle cx="{w / 2}" cy="{mid}" r="2.5" fill="{accent}" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" begin="0.6s" '
        f'dur="0.3s" fill="freeze"/></circle>'
    )
    parts.append("</svg>")
    return parts


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--banner", type=Path, default=BANNER_SVG)
    parser.add_argument("--separator", type=Path, default=SEPARATOR_SVG)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        write_svg(args.banner, build_banner_svg(), logger)
        write_svg(args.separator, build_separator_svg(), logger)
    except Exception as exc:  # noqa: BLE001
        logger.exception("failed: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
