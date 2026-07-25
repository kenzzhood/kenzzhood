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
    section_header,
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
CELL = 10
GAP = 3
STEP = CELL + GAP
GRID_LEFT = 55

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


def render(data: dict[str, Any], theme_name: str) -> list[str]:
    """Build one themed contribution panel with an inline stats strip."""
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

    header, divider_y = section_header(
        WIDTH,
        "Public contribution graph",
        corner=f'{data["range"]["start"]} \u2192 {data["range"]["end"]}',
    )
    grid_top = divider_y + 20
    month_label_y = divider_y + 14
    legend_y = grid_top + 95
    stats_y = legend_y + 28
    height = stats_y + 28

    total = int(data["total_contributions"])
    active = int(data["active_days"])
    average = data["avg_per_active_day"]

    parts: list[str] = [
        premium_svg_open(
            WIDTH,
            height,
            "GitHub contributions",
            (
                f"{total} contributions; current streak "
                f"{current_length} {current_unit}; longest streak "
                f"{longest_length} {longest_unit}."
            ),
        ),
        premium_css(theme),
        cell_css,
    ]
    parts.extend(premium_frame(WIDTH, height, grid=False))
    parts.append(header)

    for column_index, label in _month_labels(grid):
        x = GRID_LEFT + column_index * STEP
        parts.append(
            f'<text x="{x}" y="{month_label_y}" class="faint" font-size="7.5">{label}</text>'
        )

    for row, name in ((1, "M"), (3, "W"), (5, "F")):
        y = grid_top + row * STEP + 8
        parts.append(
            f'<text x="34" y="{y}" class="faint" font-size="7.5">{name}</text>'
        )

    for column_index, column in enumerate(grid):
        x = GRID_LEFT + column_index * STEP
        for row_index, cell in enumerate(column):
            if cell is None:
                continue
            date, count, level = cell
            y = grid_top + row_index * STEP
            delay = 0.16 + column_index * 0.012 + row_index * 0.025
            plural = "" if count == 1 else "s"
            parts.append(
                f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" '
                f'height="{CELL}" rx="2.2" fill="{palette[level]}" '
                f'style="animation-delay:{delay:.3f}s">'
                f"<title>{esc(date)}: {count} contribution{plural}</title></rect>"
            )

    legend_x = 700
    parts.append(
        f'<text x="{legend_x - 10}" y="{legend_y + 8}" class="faint" '
        'font-size="7.5" text-anchor="end">Less</text>'
    )
    for index, color in enumerate(palette):
        parts.append(
            f'<rect x="{legend_x + index * 12}" y="{legend_y}" width="9" '
            f'height="9" rx="2" fill="{color}"/>'
        )
    parts.append(
        f'<text x="{legend_x + 79}" y="{legend_y + 8}" class="faint" '
        'font-size="7.5">More</text>'
    )

    # Single quiet stats strip — one accent, no nested dashboard cards.
    parts.append(
        delayed(
            f'<text x="32" y="{stats_y}" class="text" font-size="12">'
            f'<tspan class="green" font-weight="700">{total:,}</tspan>'
            f'<tspan class="muted"> contributions</tspan>'
            f'<tspan class="faint">  ·  </tspan>'
            f'<tspan class="text" font-weight="700">{active}</tspan>'
            f'<tspan class="muted"> active days</tspan>'
            f'<tspan class="faint">  ·  </tspan>'
            f'<tspan class="text" font-weight="700">{current_length}d</tspan>'
            f'<tspan class="muted"> current</tspan>'
            f'<tspan class="faint">  ·  </tspan>'
            f'<tspan class="text" font-weight="700">{longest_length}d</tspan>'
            f'<tspan class="muted"> longest</tspan>'
            f'<tspan class="faint">  ·  </tspan>'
            f'<tspan class="muted">{average} avg / day</tspan>'
            "</text>",
            0.4,
            "fade",
        )
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
