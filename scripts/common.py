"""
Shared helpers for profile SVG generators.

Provides logging setup, SVG chrome (titlebar / frame), and path utilities.
"""

from __future__ import annotations

import html
import logging
import sys
from pathlib import Path
from typing import Iterable, Mapping

# Allow `python scripts/foo.py` to import top-level config.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import COLORS, FONT_FAMILY, THEMES  # noqa: E402


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


# ---------------------------------------------------------------------------
# Spatial Command Center primitives
# ---------------------------------------------------------------------------


def get_theme(name: str) -> Mapping[str, str]:
    """Return a named profile theme or fail with a useful error."""
    try:
        return THEMES[name]
    except KeyError as exc:
        valid = ", ".join(sorted(THEMES))
        raise ValueError(f"unknown theme {name!r}; expected one of: {valid}") from exc


def premium_svg_open(
    width: int,
    height: int,
    title: str,
    description: str,
) -> str:
    """Open an accessible, responsive SVG document."""
    safe_title = html.escape(title)
    safe_description = html.escape(description)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc" '
        f'font-family="{FONT_FAMILY}">'
        f'<title id="title">{safe_title}</title>'
        f'<desc id="desc">{safe_description}</desc>'
    )


def premium_css(theme: Mapping[str, str]) -> str:
    """Shared visual tokens and restrained one-shot motion."""
    tokens = ";".join(f"--{key}:{value}" for key, value in theme.items())
    return (
        f"<style>:root{{{tokens}}}"
        ".bg{fill:var(--bg)}.surface{fill:var(--surface)}"
        ".surface2{fill:var(--surface_2)}.line{stroke:var(--line)}"
        ".lineSoft{stroke:var(--line_soft)}.text{fill:var(--text)}"
        ".muted{fill:var(--muted)}.faint{fill:var(--faint)}"
        ".green{fill:var(--green)}.cyan{fill:var(--cyan)}"
        ".violet{fill:var(--violet)}"
        "@keyframes rise{from{opacity:0;transform:translateY(8px)}"
        "to{opacity:1;transform:translateY(0)}}"
        "@keyframes fade{from{opacity:0}to{opacity:1}}"
        "@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}"
        "@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}"
        ".rise{opacity:0;animation:rise .7s cubic-bezier(.2,.8,.2,1) forwards}"
        ".fade{opacity:0;animation:fade .6s ease forwards}"
        ".draw{stroke-dasharray:1;stroke-dashoffset:1;"
        "animation:draw 1.2s cubic-bezier(.2,.8,.2,1) forwards}"
        ".pulse{animation:pulse 2.4s ease-in-out infinite}"
        "@media(prefers-reduced-motion:reduce){"
        ".rise,.fade,.draw,.pulse{animation:none!important;opacity:1!important;"
        "transform:none!important;stroke-dashoffset:0!important}}</style>"
    )


def premium_frame(
    width: int,
    height: int,
    *,
    radius: int = 18,
    grid: bool = True,
) -> list[str]:
    """Return the flat premium background, border, and optional spatial grid."""
    parts = [
        f'<rect class="bg" width="{width}" height="{height}" rx="{radius}"/>',
        f'<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" '
        f'rx="{radius}" fill="none" class="line" stroke-width="1"/>',
    ]
    if grid:
        for x in range(32, width, 48):
            parts.append(
                f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" '
                'class="lineSoft" stroke-width=".6" opacity=".28"/>'
            )
        for y in range(32, height, 48):
            parts.append(
                f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" '
                'class="lineSoft" stroke-width=".6" opacity=".28"/>'
            )
    return parts


def delayed(inner: str, delay: float, css_class: str = "rise") -> str:
    """Wrap SVG markup in a delayed animation group."""
    return f'<g class="{css_class}" style="animation-delay:{delay:.2f}s">{inner}</g>'


def truncate(text: str, max_chars: int) -> str:
    """Clip display text without splitting the final word when possible."""
    if len(text) <= max_chars:
        return text
    clipped = text[: max_chars - 1].rstrip()
    if " " in clipped:
        clipped = clipped.rsplit(" ", 1)[0]
    return clipped + "…"


def esc(text: object) -> str:
    """Escape arbitrary content for safe SVG text nodes."""
    return html.escape(str(text), quote=True)
