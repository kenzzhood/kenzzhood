#!/usr/bin/env python3
"""Generate the Spatial Command Center hero in dark and light variants."""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from common import (
    delayed,
    esc,
    get_theme,
    premium_css,
    premium_frame,
    premium_svg_open,
    setup_logging,
    write_svg,
)
from config import (
    CANVAS_WIDTH,
    COMPANY,
    HERO_DARK_SVG,
    HERO_LIGHT_SVG,
    NAME,
    POSITIONING,
    PROFILE_PREPPED,
    PROOF_POINTS,
    ROLE,
)

logger = setup_logging("make_hero")

WIDTH = CANVAS_WIDTH
HEIGHT = 420


def portrait_rows(path: Path, cols: int = 44, rows: int = 31) -> list[str]:
    """Convert the preprocessed portrait to a compact ASCII field."""
    if not path.is_file():
        raise FileNotFoundError(
            f"missing portrait source {path}; run scripts/prep_photo.py first"
        )
    try:
        image = Image.open(path).convert("L")
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError(f"invalid portrait source: {path}") from exc

    image = image.resize((cols, rows), Image.Resampling.LANCZOS)
    pixels = image.load()
    ramp = " .:-=+*#%@"
    result: list[str] = []
    for y in range(rows):
        chars: list[str] = []
        for x in range(cols):
            luminance = pixels[x, y] / 255.0
            if luminance > 0.86:
                chars.append(" ")
                continue
            index = round((1.0 - luminance) * (len(ramp) - 1))
            chars.append(ramp[max(0, min(index, len(ramp) - 1))])
        result.append("".join(chars))
    return result


def _point_field() -> str:
    """Deterministic spatial point cloud behind the portrait."""
    rng = random.Random(19)
    parts: list[str] = []
    for index in range(42):
        x = rng.uniform(575, 826)
        y = rng.uniform(58, 362)
        radius = rng.choice((0.8, 1.0, 1.3, 1.6))
        color_class = rng.choice(("cyan", "green", "faint"))
        delay = 0.35 + (index % 9) * 0.07
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" '
            f'class="{color_class} fade" opacity=".65" '
            f'style="animation-delay:{delay:.2f}s"/>'
        )
    return "".join(parts)


def render(theme_name: str, portrait: list[str]) -> list[str]:
    """Build one theme variant."""
    theme = get_theme(theme_name)
    parts: list[str] = [
        premium_svg_open(
            WIDTH,
            HEIGHT,
            f"{NAME} — {ROLE} at {COMPANY}",
            (
                "Founder, engineer, and researcher building spatial intelligence "
                "with computer vision, XR, real-time 3D, and agentic AI."
            ),
        ),
        premium_css(theme),
    ]
    parts.extend(premium_frame(WIDTH, HEIGHT, grid=True))

    # Header rail and identity
    parts.append(
        '<g class="fade" style="animation-delay:.05s">'
        '<circle cx="37" cy="35" r="4" class="green"/>'
        '<text x="50" y="39" class="muted" font-size="10.5" '
        'letter-spacing="2.1">INNOXR // SPATIAL INTELLIGENCE LAB</text>'
        '<text x="527" y="39" class="faint" font-size="9.5" '
        'text-anchor="end">PROFILE_NODE 01</text>'
        "</g>"
    )

    parts.append(
        delayed(
            f'<text x="36" y="91" class="text" font-size="32" '
            f'font-weight="700" letter-spacing="-.8">{esc(NAME)}</text>'
            f'<text x="37" y="119" class="cyan" font-size="12.5" '
            f'font-weight="700" letter-spacing="1.2">{esc(ROLE.upper())} '
            f'· {esc(COMPANY.upper())}</text>',
            0.12,
        )
    )

    # Deliberately hand-wrapped for stable rendering across SVG engines.
    position_lines = [
        "Building spatial intelligence systems where AI can see,",
        "understand, and interact with the physical world.",
    ]
    parts.append(
        delayed(
            "".join(
                f'<text x="37" y="{165 + i * 23}" class="text" font-size="14">'
                f"{esc(line)}</text>"
                for i, line in enumerate(position_lines)
            ),
            0.22,
        )
    )

    parts.append(
        '<line x1="37" y1="218" x2="527" y2="218" class="line draw" '
        'pathLength="1" stroke-width="1" style="animation-delay:.28s"/>'
    )

    y = 252
    for index, proof in enumerate(PROOF_POINTS):
        inner = (
            f'<text x="37" y="{y}" class="faint" font-size="9.5" '
            f'letter-spacing="1.3">{esc(proof["label"])}</text>'
            f'<text x="175" y="{y}" class="text" font-size="11.5">'
            f'{esc(proof["value"])}</text>'
        )
        parts.append(delayed(inner, 0.34 + index * 0.09))
        y += 34

    parts.append(
        delayed(
            '<rect x="36" y="365" width="491" height="30" rx="8" '
            'class="surface2" stroke="var(--line)" stroke-width="1"/>'
            '<text x="52" y="384" class="green" font-size="9.5" '
            'letter-spacing="1.3">BUILD SIGNAL</text>'
            '<text x="158" y="384" class="muted" font-size="10.5">'
            "research → prototype → product → iterate</text>",
            0.62,
        )
    )

    # Portrait stage
    parts.append(
        '<rect x="552" y="20" width="288" height="380" rx="16" '
        'class="surface" stroke="var(--line)" stroke-width="1"/>'
        '<path d="M570 72V42H600 M792 42H822V72 M570 347V378H600 '
        'M792 378H822V347" fill="none" class="line draw" '
        'pathLength="1" stroke-width="1.2" style="animation-delay:.2s"/>'
        '<ellipse cx="696" cy="201" rx="112" ry="151" fill="none" '
        'class="lineSoft draw" pathLength="1" stroke-width=".8" '
        'style="animation-delay:.25s"/>'
        '<ellipse cx="696" cy="201" rx="87" ry="135" fill="none" '
        'class="lineSoft draw" pathLength="1" stroke-width=".7" '
        'stroke-dasharray="3 6" style="animation-delay:.35s"/>'
        + _point_field()
    )

    art_x = 572
    art_y = 76
    line_height = 8.8
    for index, line in enumerate(portrait):
        parts.append(
            f'<text xml:space="preserve" x="{art_x}" '
            f'y="{art_y + index * line_height:.1f}" class="text fade" '
            f'font-size="7.2" opacity=".92" textLength="248" '
            f'lengthAdjust="spacing" style="animation-delay:{0.28 + index * 0.025:.3f}s">'
            f"{esc(line)}</text>"
        )

    parts.append(
        '<g class="fade" style="animation-delay:1.05s">'
        '<rect x="577" y="351" width="238" height="28" rx="7" '
        'class="surface2" stroke="var(--line)" stroke-width="1"/>'
        '<circle cx="593" cy="365" r="3" class="green pulse"/>'
        '<text x="605" y="369" class="muted" font-size="9.5" '
        'letter-spacing=".7">SYSTEM ONLINE · BENGALURU, IN</text>'
        "</g>"
    )

    parts.append("</svg>")
    return parts


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--theme",
        choices=("all", "dark", "light"),
        default="all",
        help="theme variant to generate",
    )
    parser.add_argument("--portrait", type=Path, default=PROFILE_PREPPED)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        portrait = portrait_rows(args.portrait)
        targets = {
            "dark": HERO_DARK_SVG,
            "light": HERO_LIGHT_SVG,
        }
        themes = targets if args.theme == "all" else {args.theme: targets[args.theme]}
        for theme_name, output in themes.items():
            write_svg(output, render(theme_name, portrait), logger)
    except (FileNotFoundError, ValueError) as exc:
        logger.error("%s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        logger.exception("failed to generate hero: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
