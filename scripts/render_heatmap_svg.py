#!/usr/bin/env python3
"""
Render ``data/contributions.json`` as an animated contribution heatmap SVG.

Features
--------
- Rounded boxes with the GitHub green palette
- Diagonal reveal animation (CSS keyframes, one-shot)
- Less → More legend
- Stats footer: total, current streak, longest streak, best day
- Monthly labels

Usage
-----
    python scripts/render_heatmap_svg.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

from common import setup_logging, svg_background, svg_open, svg_titlebar, write_svg
from config import (
    COLORS,
    CONTRIB_PALETTE,
    CONTRIBUTION_SVG,
    CONTRIBUTIONS_JSON,
    HEATMAP,
    PROMPT_HOST,
)

logger = setup_logging("render_heatmap")

Cell = tuple[str, int, int] | None  # (date, count, level) or empty


def level_for(count: int) -> int:
    """Map a contribution count to a palette index (0–5)."""
    if count == 0:
        return 0
    if count <= 5:
        return 1
    if count <= 15:
        return 2
    if count <= 30:
        return 3
    if count <= 50:
        return 4
    return 5


def build_grid(days: list[dict[str, Any]]) -> list[list[Cell]]:
    """Pack days into a Sunday-first week-column grid."""
    first = dt.date.fromisoformat(days[0]["date"])
    lead_pad = (first.weekday() + 1) % 7  # Sunday = 0
    grid: list[list[Cell]] = []
    col: list[Cell] = [None] * lead_pad

    for day in days:
        date = dt.date.fromisoformat(day["date"])
        weekday = (date.weekday() + 1) % 7
        while len(col) < weekday:
            col.append(None)
        col.append((day["date"], day["count"], level_for(day["count"])))
        if len(col) == 7:
            grid.append(col)
            col = []

    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)
    return grid


def render(data: dict[str, Any]) -> list[str]:
    """Build SVG parts for the contribution heatmap."""
    days = data["days"]
    if not days:
        raise ValueError("contributions.json contains no days")

    grid = build_grid(days)
    n_cols = len(grid)

    cell = int(HEATMAP["cell"])
    gap = int(HEATMAP["gap"])
    step = cell + gap
    pad = int(HEATMAP["pad"])
    left_label_w = int(HEATMAP["left_label_w"])
    top_label_h = int(HEATMAP["top_label_h"])
    titlebar_h = int(HEATMAP["titlebar_h"])
    stats_h = int(HEATMAP["stats_h"])
    col_t = float(HEATMAP["col_t"])
    row_t = float(HEATMAP["row_t"])
    cell_dur = float(HEATMAP["cell_dur"])

    art_w = n_cols * step
    art_h = 7 * step
    canvas_w = pad + left_label_w + art_w + pad
    canvas_h = titlebar_h + top_label_h + art_h + stats_h + pad

    muted = COLORS["muted"]
    accent = COLORS["accent"]
    bright = COLORS["bright"]
    gold = COLORS["gold"]
    frame = COLORS["frame"]

    # Month labels
    month_labels: list[tuple[int, str]] = []
    seen_months: set[tuple[int, int]] = set()
    for ci, column in enumerate(grid):
        for c in column:
            if c is None:
                continue
            date = dt.date.fromisoformat(c[0])
            key = (date.year, date.month)
            if key not in seen_months and date.day <= 7:
                seen_months.add(key)
                month_labels.append((ci, date.strftime("%b")))
            break

    css = (
        "@keyframes cell {"
        "0%{opacity:0;transform:translateY(-6px)}"
        "100%{opacity:1;transform:translateY(0)}"
        "}"
        f".c{{opacity:0;animation:cell {cell_dur:.2f}s cubic-bezier(.2,.8,.2,1) both}}"
    )

    parts: list[str] = [svg_open(canvas_w, canvas_h)]
    parts.append(f"<style>{css}</style>")
    parts.extend(svg_background(canvas_w, canvas_h))
    parts.extend(
        svg_titlebar(
            canvas_w,
            f"{PROMPT_HOST}: ~/contributions --graph",
            titlebar_h,
            pad,
        )
    )

    grid_top = titlebar_h + top_label_h
    grid_left = pad + left_label_w

    for ci, label in month_labels:
        x = grid_left + ci * step
        parts.append(
            f'<text x="{x}" y="{titlebar_h + 14}" fill="{muted}" font-size="10">{label}</text>'
        )

    for wi, wname in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = grid_top + wi * step + cell * 0.78
        parts.append(
            f'<text x="{pad}" y="{y:.1f}" fill="{muted}" font-size="9">{wname}</text>'
        )

    for ci, column in enumerate(grid):
        gx = grid_left + ci * step
        for ri, c in enumerate(column):
            if c is None:
                continue
            date_s, count, lvl = c
            gy = grid_top + ri * step
            delay = ci * col_t + ri * row_t
            plural = "s" if count != 1 else ""
            parts.append(
                f'<rect class="c" x="{gx}" y="{gy}" width="{cell}" height="{cell}" '
                f'rx="2.5" fill="{CONTRIB_PALETTE[lvl]}" '
                f'style="animation-delay:{delay:.3f}s">'
                f"<title>{date_s}: {count} contribution{plural}</title></rect>"
            )

    # Legend
    leg_y = grid_top + art_h + 6
    leg_x = canvas_w - pad - (len(CONTRIB_PALETTE) * (cell - 1) + 70)
    parts.append(
        f'<text x="{leg_x}" y="{leg_y + cell * 0.8:.1f}" fill="{muted}" '
        f'font-size="10" text-anchor="end">Less</text>'
    )
    lx = leg_x + 8
    for color in CONTRIB_PALETTE:
        parts.append(
            f'<rect x="{lx}" y="{leg_y}" width="{cell - 1}" height="{cell - 1}" '
            f'rx="2.2" fill="{color}"/>'
        )
        lx += cell
    parts.append(
        f'<text x="{lx + 4}" y="{leg_y + cell * 0.8:.1f}" fill="{muted}" '
        f'font-size="10">More</text>'
    )

    sep_y = leg_y + cell + 14
    parts.append(
        f'<line x1="0" y1="{sep_y}" x2="{canvas_w}" y2="{sep_y}" '
        f'stroke="{frame}" stroke-opacity="0.25"/>'
    )

    cs = data["current_streak"]["length"]
    ls = data["longest_streak"]["length"]
    total = data["total_contributions"]
    best = data["best_day"]
    rng = data["range"]

    ly = sep_y + 24
    parts.append(
        f'<text x="{pad}" y="{ly}" font-size="13" fill="{accent}">'
        f'<tspan font-weight="700">{total:,}</tspan>'
        f'<tspan fill="{muted}"> contributions in the last year</tspan></text>'
    )
    parts.append(
        f'<text x="{canvas_w - pad}" y="{ly}" font-size="12" fill="{muted}" '
        f'text-anchor="end">{rng["start"]} → {rng["end"]}</text>'
    )
    ly += 24
    parts.append(
        f'<text x="{pad}" y="{ly}" font-size="13" fill="{muted}">current streak '
        f'<tspan fill="{bright}" font-weight="700">{cs} days</tspan>'
        f'<tspan fill="{muted}">   ·   longest </tspan>'
        f'<tspan fill="{bright}" font-weight="700">{ls} days</tspan></text>'
    )
    parts.append(
        f'<text x="{canvas_w - pad}" y="{ly}" font-size="12" fill="{muted}" '
        f'text-anchor="end">best day '
        f'<tspan fill="{gold}" font-weight="700">{best["count"]}</tspan> '
        f'on {best["date"]}</text>'
    )

    parts.append("</svg>")
    return parts


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=CONTRIBUTIONS_JSON)
    parser.add_argument("--output", type=Path, default=CONTRIBUTION_SVG)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if not args.input.is_file():
            raise FileNotFoundError(
                f"missing {args.input} — run fetch_contributions.py first"
            )
        data = json.loads(args.input.read_text(encoding="utf-8"))
        parts = render(data)
        write_svg(args.output, parts, logger)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        logger.error("%s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        logger.exception("unexpected failure: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
