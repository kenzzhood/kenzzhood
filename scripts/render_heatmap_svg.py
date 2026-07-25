#!/usr/bin/env python3
"""Render public contribution data as a premium build-telemetry SVG."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

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
    CONTRIBUTION_DARK_SVG,
    CONTRIBUTION_LIGHT_SVG,
    CONTRIBUTIONS_JSON,
)

logger = setup_logging("render_heatmap")

WIDTH = CANVAS_WIDTH
HEIGHT = 318
CELL = 10
GAP = 3
STEP = CELL + GAP
GRID_LEFT = 55
GRID_TOP = 104

PALETTES: dict[str, list[str]] = {
    "dark": ["#141b24", "#103a2b", "#155c3e", "#1f8a57", "#48d17a", "#8bf0b3"],
    "light": ["#e7edf2", "#d2f4df", "#98e6b5", "#4fc77e", "#20985a", "#126b3f"],
}

Cell = tuple[str, int, int] | None


def level_for(count: int) -> int:
    """Map a count to a stable six-step intensity."""
    if count <= 0:
        return 0
    if count <= 2:
        return 1
    if count <= 5:
        return 2
    if count <= 10:
        return 3
    if count <= 20:
        return 4
    return 5


def build_grid(days: list[dict[str, Any]]) -> list[list[Cell]]:
    """Pack chronological days into Sunday-first week columns."""
    if not days:
        raise ValueError("contribution payload contains no days")

    first = dt.date.fromisoformat(days[0]["date"])
    lead = (first.weekday() + 1) % 7
    columns: list[list[Cell]] = []
    column: list[Cell] = [None] * lead

    for day in days:
        date = dt.date.fromisoformat(day["date"])
        weekday = (date.weekday() + 1) % 7
        while len(column) < weekday:
            column.append(None)
        count = int(day["count"])
        column.append((day["date"], count, level_for(count)))
        if len(column) == 7:
            columns.append(column)
            column = []

    if column:
        column.extend([None] * (7 - len(column)))
        columns.append(column)
    return columns[-54:]


def _month_labels(grid: list[list[Cell]]) -> list[tuple[int, str]]:
    labels: list[tuple[int, str]] = []
    seen: set[tuple[int, int]] = set()
    for column_index, column in enumerate(grid):
        for cell in column:
            if cell is None:
                continue
            date = dt.date.fromisoformat(cell[0])
            key = (date.year, date.month)
            if key not in seen and date.day <= 7:
                seen.add(key)
                labels.append((column_index, date.strftime("%b").upper()))
            break
    return labels


def _stat_card(
    x: int,
    label: str,
    value: str,
    detail: str,
    accent_class: str,
    delay: float,
) -> str:
    return delayed(
        f'<rect x="{x}" y="229" width="185" height="65" rx="11" '
        'class="surface" stroke="var(--line)" stroke-width="1"/>'
        f'<text x="{x + 14}" y="249" class="faint" font-size="8" '
        f'letter-spacing="1.1">{esc(label)}</text>'
        f'<text x="{x + 14}" y="273" class="{accent_class}" '
        f'font-size="17" font-weight="700">{esc(value)}</text>'
        f'<text x="{x + 14}" y="286" class="muted" font-size="7.8">'
        f"{esc(detail)}</text>",
        delay,
    )


def render(data: dict[str, Any], theme_name: str) -> list[str]:
    """Build one themed telemetry panel."""
    theme = get_theme(theme_name)
    palette = PALETTES[theme_name]
    grid = build_grid(data["days"])
    current_length = int(data["current_streak"]["length"])
    longest_length = int(data["longest_streak"]["length"])
    current_unit = "day" if current_length == 1 else "days"
    longest_unit = "day" if longest_length == 1 else "days"

    cell_css = (
        "<style>@keyframes cellIn{from{opacity:0;transform:translateY(-5px)}"
        "to{opacity:1;transform:translateY(0)}}"
        ".cell{opacity:0;animation:cellIn .42s cubic-bezier(.2,.8,.2,1) forwards}"
        "@media(prefers-reduced-motion:reduce){.cell{animation:none!important;"
        "opacity:1!important;transform:none!important}}</style>"
    )

    parts: list[str] = [
        premium_svg_open(
            WIDTH,
            HEIGHT,
            "GitHub contributions",
            (
                f"{data['total_contributions']} contributions; current streak "
                f"{current_length} {current_unit}; longest streak "
                f"{longest_length} {longest_unit}."
            ),
        ),
        premium_css(theme),
        cell_css,
    ]
    parts.extend(premium_frame(WIDTH, HEIGHT, grid=False))

    parts.append(
        '<text x="32" y="35" class="green" font-size="10">Activity</text>'
        '<text x="32" y="68" class="text" font-size="22" font-weight="700">'
        "Public contribution graph</text>"
        f'<text x="828" y="35" class="faint" font-size="10" text-anchor="end">'
        f'{esc(data["range"]["start"])} → {esc(data["range"]["end"])}</text>'
        '<line x1="32" y1="84" x2="828" y2="84" class="line draw" '
        'pathLength="1" stroke-width="1" style="animation-delay:.1s"/>'
    )

    for column_index, label in _month_labels(grid):
        x = GRID_LEFT + column_index * STEP
        parts.append(
            f'<text x="{x}" y="98" class="faint" font-size="7.5">{label}</text>'
        )

    for row, name in ((1, "M"), (3, "W"), (5, "F")):
        y = GRID_TOP + row * STEP + 8
        parts.append(
            f'<text x="34" y="{y}" class="faint" font-size="7.5">{name}</text>'
        )

    for column_index, column in enumerate(grid):
        x = GRID_LEFT + column_index * STEP
        for row_index, cell in enumerate(column):
            if cell is None:
                continue
            date, count, level = cell
            y = GRID_TOP + row_index * STEP
            delay = 0.16 + column_index * 0.012 + row_index * 0.025
            plural = "" if count == 1 else "s"
            parts.append(
                f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" '
                f'height="{CELL}" rx="2.2" fill="{palette[level]}" '
                f'style="animation-delay:{delay:.3f}s">'
                f"<title>{esc(date)}: {count} contribution{plural}</title></rect>"
            )

    legend_x = 774
    legend_y = 199
    parts.append(
        f'<text x="{legend_x - 10}" y="{legend_y + 8}" class="faint" '
        'font-size="7.5" text-anchor="end">LESS</text>'
    )
    for index, color in enumerate(palette):
        parts.append(
            f'<rect x="{legend_x + index * 12}" y="{legend_y}" width="9" '
            f'height="9" rx="2" fill="{color}"/>'
        )
    parts.append(
        f'<text x="{legend_x + 79}" y="{legend_y + 8}" class="faint" '
        'font-size="7.5">MORE</text>'
    )

    total = int(data["total_contributions"])
    active = int(data["active_days"])
    current = current_length
    longest = longest_length
    average = data["avg_per_active_day"]

    parts.extend(
        [
            _stat_card(32, "CONTRIBUTIONS", f"{total:,}", "last 12 months", "green", 0.38),
            _stat_card(231, "ACTIVE DAYS", str(active), f"{average} avg / active day", "cyan", 0.46),
            _stat_card(430, "CURRENT STREAK", f"{current}d", "ongoing", "violet", 0.54),
            _stat_card(629, "LONGEST STREAK", f"{longest}d", "best stretch", "green", 0.62),
        ]
    )

    parts.append("</svg>")
    return parts


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=CONTRIBUTIONS_JSON)
    parser.add_argument(
        "--theme",
        choices=("all", "dark", "light"),
        default="all",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        targets = {
            "dark": CONTRIBUTION_DARK_SVG,
            "light": CONTRIBUTION_LIGHT_SVG,
        }
        selected = targets if args.theme == "all" else {args.theme: targets[args.theme]}
        for theme_name, output in selected.items():
            write_svg(output, render(data, theme_name), logger)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        logger.error("%s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        logger.exception("failed to render telemetry: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
