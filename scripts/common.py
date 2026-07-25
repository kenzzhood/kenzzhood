"""
Shared helpers for profile SVG generators.

Provides logging setup, SVG chrome (titlebar / frame), and path utilities.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Iterable

# Allow `python scripts/foo.py` to import top-level config.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import COLORS, FONT_FAMILY  # noqa: E402


def setup_logging(name: str, level: int = logging.INFO) -> logging.Logger:
    """Configure a concise stderr logger for a script."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", "%H:%M:%S")
        )
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def ensure_parent(path: Path) -> None:
    """Create parent directories for *path* if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)


def svg_open(width: int | float, height: int | float) -> str:
    """Opening <svg> tag with JetBrains Mono stack."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT_FAMILY}">'
    )


def svg_background(width: int | float, height: int | float, radius: int = 12) -> list[str]:
    """Rounded terminal panel background + border."""
    bg = COLORS["bg"]
    bg2 = COLORS["bg2"]
    frame = COLORS["frame"]
    return [
        "<defs>"
        f'<linearGradient id="panel-bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{bg2}"/>'
        f'<stop offset="1" stop-color="{bg}"/>'
        "</linearGradient></defs>",
        f'<rect width="{width}" height="{height}" rx="{radius}" fill="url(#panel-bg)"/>',
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" '
        f'rx="{radius}" fill="none" stroke="{frame}" stroke-width="1"/>',
    ]


def svg_titlebar(
    width: int | float,
    title: str,
    titlebar_h: int = 30,
    pad: int = 20,
) -> list[str]:
    """macOS-style traffic lights + centered prompt title."""
    frame = COLORS["frame"]
    muted = COLORS["muted"]
    parts = [
        f'<line x1="0" y1="{titlebar_h}" x2="{width}" y2="{titlebar_h}" stroke="{frame}"/>',
    ]
    for i, key in enumerate(("dot_red", "dot_yellow", "dot_green")):
        parts.append(
            f'<circle cx="{pad + i * 16}" cy="{titlebar_h / 2}" r="5" fill="{COLORS[key]}"/>'
        )
    parts.append(
        f'<text x="{width / 2}" y="{titlebar_h / 2 + 4}" fill="{muted}" '
        f'font-size="12" text-anchor="middle">{title}</text>'
    )
    return parts


def write_svg(path: Path, parts: Iterable[str], logger: logging.Logger | None = None) -> int:
    """Join SVG parts, write to disk, return byte length."""
    ensure_parent(path)
    svg = "".join(parts)
    path.write_text(svg, encoding="utf-8")
    if logger:
        logger.info("wrote %s (%d bytes)", path, len(svg))
    return len(svg)
