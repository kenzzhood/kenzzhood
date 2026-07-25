#!/usr/bin/env python3
"""
Generate an animated neofetch-style info card SVG.

Lines fade in and slide up sequentially (one-shot SMIL). Content is driven by
``config.py`` — name, role, company, research, languages, frameworks, focus.

Usage
-----
    python scripts/make_neofetch.py [output.svg]

Set STATIC=1 for a frozen preview frame.
"""

from __future__ import annotations

import argparse
import html
import os
import sys
from pathlib import Path
from typing import Any

from common import setup_logging, svg_background, svg_open, svg_titlebar, write_svg
from config import (
    COLORS,
    COMPANY,
    CURRENTLY_BUILDING,
    FRAMEWORKS,
    GITHUB_USERNAME,
    LANGUAGES,
    NAME,
    NEOFETCH,
    NEOFETCH_SVG,
    OPEN_SOURCE,
    PROMPT_HOST,
    RESEARCH_INTERESTS,
    ROLE,
    STARTUP,
)

logger = setup_logging("make_neofetch")


def esc(text: str) -> str:
    return html.escape(text)


def rise(inner: str, index: int, static: bool) -> str:
    """Wrap *inner* in a fade + slight upward slide, staggered by index."""
    if static:
        return f"<g>{inner}</g>"
    delay = float(NEOFETCH["initial_delay"]) + index * float(NEOFETCH["stagger"])
    dur = float(NEOFETCH["fade_dur"])
    return (
        f'<g opacity="0" transform="translate(0,5)">{inner}'
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{delay:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 5" to="0 0" begin="{delay:.2f}s" dur="{dur:.2f}s" '
        f'fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>'
    )


def _clip(text: str, limit: int) -> str:
    """Hard-clip a value so it fits the neofetch column width."""
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "…"


def content_rows() -> list[tuple[Any, ...]]:
    """Build the neofetch content model from config."""
    research = _clip(", ".join(RESEARCH_INTERESTS[:3]), 42)
    langs = _clip(", ".join(LANGUAGES), 42)
    frameworks = _clip(", ".join(FRAMEWORKS[:5]), 42)
    building = _clip(CURRENTLY_BUILDING[0] if CURRENTLY_BUILDING else "—", 48)
    oss = _clip(OPEN_SOURCE[0] if OPEN_SOURCE else "—", 48)
    startup = _clip(STARTUP, 48)

    return [
        ("host",),
        ("kv", "Name", NAME),
        ("kv", "Role", ROLE),
        ("kv", "Company", COMPANY),
        ("kv", "Shell", "AI × XR × Vision"),
        ("gap",),
        ("sec", "Research"),
        ("kv", "Focus", research),
        ("gap",),
        ("sec", "Stack"),
        ("kv", "Languages", langs),
        ("kv", "Frameworks", frameworks),
        ("gap",),
        ("sec", "Now"),
        ("bul", building),
        ("bul", oss),
        ("bul", startup),
    ]


def build_neofetch_svg(static: bool = False) -> list[str]:
    """Assemble the animated neofetch card."""
    w = int(NEOFETCH["width"])
    h = int(NEOFETCH["height"])
    pad = int(NEOFETCH["pad"])
    titlebar_h = int(NEOFETCH["titlebar_h"])
    line_h = float(NEOFETCH["line_h"])
    key_x = pad
    val_x = pad + int(NEOFETCH["key_width"])

    muted = COLORS["muted"]
    ink = COLORS["ink"]
    accent = COLORS["accent"]
    frame = COLORS["frame"]
    bright = COLORS["bright"]

    parts: list[str] = [svg_open(w, h)]
    parts.extend(svg_background(w, h))
    parts.extend(svg_titlebar(w, f"{PROMPT_HOST}: ~$ neofetch", titlebar_h, pad))

    y = titlebar_h + 28.0
    for i, row in enumerate(content_rows()):
        kind = row[0]
        if kind == "gap":
            y += line_h * 0.45
            continue

        if kind == "host":
            inner = (
                f'<text x="{key_x}" y="{y:.1f}" font-size="14" font-weight="700">'
                f'<tspan fill="{accent}">{esc(GITHUB_USERNAME)}</tspan>'
                f'<tspan fill="{muted}">@</tspan>'
                f'<tspan fill="{bright}">github</tspan></text>'
                f'<line x1="{key_x + 120}" y1="{y - 4:.1f}" x2="{w - pad}" '
                f'y2="{y - 4:.1f}" stroke="{frame}" stroke-opacity="0.8"/>'
            )
        elif kind == "sec":
            title = esc(str(row[1]))
            rule_x = key_x + 14 + len(str(row[1])) * 8
            inner = (
                f'<text x="{key_x}" y="{y:.1f}" fill="{accent}" font-size="12.5" '
                f'font-weight="700">— {title}</text>'
                f'<line x1="{rule_x}" y1="{y - 4:.1f}" x2="{w - pad}" '
                f'y2="{y - 4:.1f}" stroke="{frame}" stroke-opacity="0.8"/>'
            )
        elif kind == "kv":
            key, val = esc(str(row[1])), esc(str(row[2]))
            inner = (
                f'<text x="{key_x}" y="{y:.1f}" fill="{muted}" font-size="12.5" '
                f'font-weight="700">{key}</text>'
                f'<text x="{val_x}" y="{y:.1f}" fill="{ink}" font-size="12.5">{val}</text>'
            )
        elif kind == "bul":
            txt = esc(str(row[1]))
            inner = (
                f'<circle cx="{key_x + 3}" cy="{y - 4:.1f}" r="2.5" fill="{accent}"/>'
                f'<text x="{key_x + 14}" y="{y:.1f}" fill="{ink}" font-size="12.5">{txt}</text>'
            )
        else:
            continue

        parts.append(rise(inner, i, static))
        y += line_h

    # Grow height if content overflowed configured height
    needed = int(y + pad)
    if needed > h:
        logger.warning("content taller than config height (%d > %d); clipping", needed, h)

    parts.append("</svg>")
    return parts


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", nargs="?", type=Path, default=NEOFETCH_SVG)
    parser.add_argument(
        "--static",
        action="store_true",
        default=bool(os.environ.get("STATIC")),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        parts = build_neofetch_svg(static=args.static)
        write_svg(args.output, parts, logger)
    except Exception as exc:  # noqa: BLE001
        logger.exception("failed to build neofetch card: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
