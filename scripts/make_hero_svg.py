#!/usr/bin/env python3
"""Generate the profile hero with ASCII portrait in dark and light variants."""

from __future__ import annotations

import argparse
import sys
import textwrap
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
    CERTIFICATION,
    COMPANY,
    HERO_DARK_SVG,
    HERO_LIGHT_SVG,
    INCUBATED_AT,
    LOCATION,
    NAME,
    POSITIONING,
    PROFILE_PREPPED,
    PROOF_POINTS,
    ROLE,
    SLOGANS,
)

logger = setup_logging("make_hero")

WIDTH = CANVAS_WIDTH
HEIGHT = 400


def portrait_rows(path: Path, cols: int = 44, rows: int = 30) -> list[str]:
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


def render(theme_name: str, portrait: list[str]) -> list[str]:
    """Build one theme variant."""
    get_theme(theme_name)
    position_lines = textwrap.wrap(POSITIONING, width=48, break_long_words=False)[:2]
    slogan = f"{SLOGANS[0]}  ·  {SLOGANS[1]}"

    parts: list[str] = [
        premium_svg_open(
            WIDTH,
            HEIGHT,
            f"{NAME} — {ROLE}",
            (
                "AI / XR engineer building computer vision, spatial computing, "
                "and multimodal AI systems. Founder of InnoXR Labs."
            ),
        ),
        premium_css(get_theme(theme_name)),
    ]
    parts.extend(premium_frame(WIDTH, HEIGHT, grid=False))

    parts.append(
        '<g class="fade" style="animation-delay:.05s">'
        f'<text x="36" y="38" class="muted" font-size="11">'
        f"{esc(ROLE)}</text>"
        f'<text x="520" y="38" class="faint" font-size="10.5" '
        f'text-anchor="end">{esc(LOCATION)}</text>'
        "</g>"
    )

    parts.append(
        delayed(
            f'<text x="36" y="84" class="text" font-size="30" '
            f'font-weight="700" letter-spacing="-.6">{esc(NAME)}</text>'
            f'<text x="37" y="112" class="cyan" font-size="12.5">'
            f"{esc(slogan)}</text>",
            0.1,
        )
    )

    parts.append(
        delayed(
            "".join(
                f'<text x="37" y="{148 + i * 22}" class="text" font-size="13.5">'
                f"{esc(line)}</text>"
                for i, line in enumerate(position_lines)
            ),
            0.18,
        )
    )

    parts.append(
        '<line x1="37" y1="204" x2="520" y2="204" class="line draw" '
        'pathLength="1" stroke-width="1" style="animation-delay:.24s"/>'
    )

    y = 236
    for index, proof in enumerate(PROOF_POINTS):
        parts.append(
            delayed(
                f'<text x="37" y="{y}" class="faint" font-size="10">'
                f'{esc(proof["label"])}</text>'
                f'<text x="122" y="{y}" class="text" font-size="12">'
                f'{esc(proof["value"])}</text>',
                0.3 + index * 0.08,
            )
        )
        y += 30

    parts.append(
        delayed(
            f'<text x="37" y="348" class="muted" font-size="11">'
            f"Founder, {esc(COMPANY)}</text>"
            f'<text x="37" y="370" class="faint" font-size="10.5">'
            f"Incubated at {esc(INCUBATED_AT)}</text>",
            0.58,
            "fade",
        )
    )

    parts.append(
        '<rect x="548" y="28" width="284" height="344" rx="14" '
        'class="surface" stroke="var(--line)" stroke-width="1"/>'
    )

    art_x = 566
    art_y = 58
    line_height = 9.0
    for index, line in enumerate(portrait):
        parts.append(
            f'<text xml:space="preserve" x="{art_x}" '
            f'y="{art_y + index * line_height:.1f}" class="text fade" '
            f'font-size="7.4" opacity=".9" textLength="248" '
            f'lengthAdjust="spacing" style="animation-delay:{0.22 + index * 0.02:.3f}s">'
            f"{esc(line)}</text>"
        )

    parts.append(
        '<g class="fade" style="animation-delay:.95s">'
        '<circle cx="580" cy="348" r="3" class="green pulse"/>'
        f'<text x="592" y="352" class="muted" font-size="9.5">'
        f"{esc(CERTIFICATION.split(' — ')[0])}</text>"
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
