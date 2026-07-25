#!/usr/bin/env python3
"""
Convert a prepped grayscale portrait into a monochrome ASCII SVG.

Animation (SMIL, GitHub-compatible)
-----------------------------------
Each row is revealed with a left-to-right clip wipe. A block cursor rides the
wipe edge. Rows are staggered top → bottom so the portrait types once and
freezes. No infinite loops on the art itself; only the status-bar cursor blinks.

Usage
-----
    python scripts/make_ascii_svg.py [prepped.png] [output.svg]

Set STATIC=1 to emit a frozen frame (useful for local Quick Look).
"""

from __future__ import annotations

import argparse
import html
import os
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, UnidentifiedImageError

from common import setup_logging, svg_background, svg_open, svg_titlebar, write_svg
from config import (
    ASCII,
    ASCII_SVG,
    COLORS,
    NAME,
    PROFILE_PREPPED,
    PROMPT_HOST,
)

logger = setup_logging("make_ascii_svg")


def luminance_to_char(lum: float, ramp: str, white_floor: float, gamma: float) -> str:
    """Map a 0–1 luminance sample to a density-ramp glyph."""
    lum = pow(lum, gamma)
    if lum >= white_floor:
        return " "
    idx = int((1.0 - lum) * (len(ramp) - 1) + 0.5)
    idx = max(0, min(len(ramp) - 1, idx))
    return ramp[idx]


def image_to_ascii_rows(path: Path) -> list[str]:
    """Downsample *path* into a character grid."""
    if not path.is_file():
        raise FileNotFoundError(f"prepped image not found: {path}")

    cols = int(ASCII["cols"])
    rows = int(ASCII["rows"])
    ramp = str(ASCII["ramp"])
    white_floor = float(ASCII["white_floor"])
    gamma = float(ASCII["gamma"])

    try:
        im = Image.open(path).convert("L")
    except UnidentifiedImageError as exc:
        raise ValueError(f"invalid image: {path}") from exc

    im = ImageEnhance.Brightness(im).enhance(float(ASCII["brightness"]))
    im = ImageEnhance.Contrast(im).enhance(float(ASCII["contrast"]))
    im = im.resize((cols, rows), Image.Resampling.LANCZOS)
    px = im.load()

    lines: list[str] = []
    for y in range(rows):
        chars = [
            luminance_to_char(px[x, y] / 255.0, ramp, white_floor, gamma)
            for x in range(cols)
        ]
        lines.append("".join(chars))
    return lines


def build_ascii_svg(rows_txt: list[str], static: bool = False) -> list[str]:
    """Assemble the animated (or static) ASCII portrait SVG parts."""
    cols = int(ASCII["cols"])
    rows = int(ASCII["rows"])
    cell_w = int(ASCII["cell_w"])
    cell_h = int(ASCII["cell_h"])
    pad = int(ASCII["pad"])
    titlebar_h = int(ASCII["titlebar_h"])
    status_h = int(ASCII["status_h"])
    row_dur = float(ASCII["row_dur"])
    stagger = float(ASCII["stagger"])

    art_w = cols * cell_w
    art_h = rows * cell_h
    canvas_w = art_w + pad * 2
    canvas_h = titlebar_h + art_h + status_h + pad
    art_top = titlebar_h + pad * 0.35
    font_size = cell_h * 0.86

    ink = COLORS["ink"]
    cursor = COLORS["cursor"]
    muted = COLORS["muted"]
    frame = COLORS["frame"]

    parts: list[str] = [svg_open(canvas_w, canvas_h)]
    parts.extend(svg_background(canvas_w, canvas_h))
    parts.extend(svg_titlebar(canvas_w, f"{PROMPT_HOST}: ~$ ./portrait.sh", titlebar_h, pad))

    for ry, line in enumerate(rows_txt):
        y = art_top + ry * cell_h + cell_h * 0.74
        row_y = art_top + ry * cell_h
        delay = ry * stagger
        safe = html.escape(line)
        text = (
            f'<text xml:space="preserve" x="{pad}" y="{y:.1f}" fill="{ink}" '
            f'font-size="{font_size:.1f}" textLength="{art_w}" '
            f'lengthAdjust="spacing">{safe}</text>'
        )

        if static:
            parts.append(text)
            continue

        parts.append(
            f'<clipPath id="r{ry}">'
            f'<rect x="{pad}" y="{row_y:.1f}" height="{cell_h}" width="0">'
            f'<animate attributeName="width" from="0" to="{art_w}" '
            f'begin="{delay:.3f}s" dur="{row_dur:.2f}s" fill="freeze"/>'
            f"</rect></clipPath>"
        )
        parts.append(f'<g clip-path="url(#r{ry})">{text}</g>')
        parts.append(
            f'<rect y="{row_y + 1:.1f}" width="{cell_w}" height="{cell_h - 2}" '
            f'fill="{cursor}" opacity="0">'
            f'<animate attributeName="x" from="{pad}" to="{pad + art_w}" '
            f'begin="{delay:.3f}s" dur="{row_dur:.2f}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0.85" begin="{delay:.3f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{delay + row_dur:.3f}s"/>'
            f"</rect>"
        )

    status_line_y = titlebar_h + art_h + pad * 0.35
    status_y = status_line_y + 19
    parts.append(
        f'<line x1="0" y1="{status_line_y:.1f}" x2="{canvas_w}" '
        f'y2="{status_line_y:.1f}" stroke="{frame}"/>'
    )
    parts.append(
        f'<text x="{pad}" y="{status_y:.1f}" fill="{muted}" font-size="13">'
        f'{PROMPT_HOST}:~$ whoami <tspan fill="{ink}">{html.escape(NAME)}</tspan></text>'
    )
    # Blinking cursor after the name (indefinite — status chrome only)
    cursor_x = pad + 14 * 8 + len(NAME) * 7.4
    parts.append(
        f'<rect x="{cursor_x:.1f}" y="{status_y - 12:.1f}" width="8" height="14" fill="{ink}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
        f'dur="1s" repeatCount="indefinite"/></rect>'
    )
    parts.append("</svg>")
    return parts


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, default=PROFILE_PREPPED)
    parser.add_argument("output", nargs="?", type=Path, default=ASCII_SVG)
    parser.add_argument(
        "--static",
        action="store_true",
        default=bool(os.environ.get("STATIC")),
        help="emit frozen frame (no typing animation)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        rows = image_to_ascii_rows(args.input)
        parts = build_ascii_svg(rows, static=args.static)
        write_svg(args.output, parts, logger)
    except (FileNotFoundError, ValueError) as exc:
        logger.error("%s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        logger.exception("unexpected failure: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
