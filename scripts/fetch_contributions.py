#!/usr/bin/env python3
"""
Scrape public GitHub contribution calendar HTML (no token, no GraphQL).

Fetches ``https://github.com/users/<USERNAME>/contributions``, parses day cells
with BeautifulSoup, and writes ``data/contributions.json`` with raw days plus
derived stats (current streak, longest streak, best day, monthly totals).

Usage
-----
    python scripts/fetch_contributions.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup

from common import ensure_parent, setup_logging
from config import (
    CONTRIBUTIONS_JSON,
    CONTRIBUTIONS_URL,
    GITHUB_USERNAME,
    REQUEST_TIMEOUT,
    USER_AGENT,
)

logger = setup_logging("fetch_contributions")


def fetch_html(url: str) -> str:
    """GET the contributions page; raise on network / HTTP errors."""
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
    except requests.Timeout as exc:
        raise RuntimeError(f"request timed out after {REQUEST_TIMEOUT}s: {url}") from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"network failure fetching {url}: {exc}") from exc
    return resp.text


def parse_days(html: str) -> list[dict[str, Any]]:
    """Extract ``{date, count}`` entries from contribution calendar HTML."""
    soup = BeautifulSoup(html, "html.parser")
    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        # Fallback: older / alternate markup
        cells = soup.select("[data-date]")

    days: list[dict[str, Any]] = []
    for td in cells:
        date = td.get("data-date")
        if not date:
            continue

        # Prefer tooltip text; fall back to data-level / data-count attrs
        count = 0
        td_id = td.get("id")
        tooltip_el = soup.find("tool-tip", attrs={"for": td_id}) if td_id else None
        text = tooltip_el.get_text(strip=True) if tooltip_el else ""

        if text:
            if re.search(r"no contributions", text, re.I):
                count = 0
            else:
                match = re.match(r"(\d+)", text)
                count = int(match.group(1)) if match else 0
        else:
            raw = td.get("data-count")
            if raw is not None:
                count = int(raw)
            else:
                level = td.get("data-level")
                count = int(level) if level and level.isdigit() else 0

        days.append({"date": date, "count": count})

    if not days:
        raise RuntimeError(
            "no calendar cells found — GitHub markup may have changed"
        )

    days.sort(key=lambda d: d["date"])
    return days


def compute_current_streak(days: list[dict[str, Any]]) -> tuple[int, str | None, str | None]:
    """Return (length, start, end) for the active streak ending today/yesterday."""
    idx = len(days) - 1
    if days[idx]["count"] == 0:
        idx -= 1  # today may still be empty
    streak = 0
    end_idx = idx
    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1
    if streak == 0:
        return 0, None, None
    start_idx = idx + 1
    return streak, days[start_idx]["date"], days[end_idx]["date"]


def compute_longest_streak(
    days: list[dict[str, Any]],
) -> tuple[int, str | None, str | None]:
    """Return (length, start, end) for the longest contiguous active run."""
    longest = run = 0
    longest_start = longest_end = None
    run_start_idx: int | None = None
    for i, day in enumerate(days):
        if day["count"] > 0:
            if run == 0:
                run_start_idx = i
            run += 1
            if run > longest and run_start_idx is not None:
                longest = run
                longest_start = days[run_start_idx]["date"]
                longest_end = days[i]["date"]
        else:
            run = 0
    return longest, longest_start, longest_end


def build_data(days: list[dict[str, Any]], username: str) -> dict[str, Any]:
    """Derive summary stats and package the contributions payload."""
    total = sum(d["count"] for d in days)
    active_days = sum(1 for d in days if d["count"] > 0)
    best = max(days, key=lambda d: d["count"])
    cur_len, cur_start, cur_end = compute_current_streak(days)
    long_len, long_start, long_end = compute_longest_streak(days)

    monthly: dict[str, int] = {}
    for day in days:
        key = day["date"][:7]
        monthly[key] = monthly.get(key, 0) + day["count"]
    monthly_list = [{"month": k, "total": v} for k, v in sorted(monthly.items())]

    return {
        "username": username,
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active_days,
        "avg_per_active_day": round(total / active_days, 1) if active_days else 0,
        "current_streak": {"length": cur_len, "start": cur_start, "end": cur_end},
        "longest_streak": {"length": long_len, "start": long_start, "end": long_end},
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": monthly_list,
        "days": days,
    }


def fetch_and_save(
    url: str = CONTRIBUTIONS_URL,
    out: Path = CONTRIBUTIONS_JSON,
    username: str = GITHUB_USERNAME,
) -> dict[str, Any]:
    """Fetch, parse, write JSON, and return the data dict."""
    logger.info("fetching %s", url)
    html = fetch_html(url)
    days = parse_days(html)
    data = build_data(days, username)
    ensure_parent(out)
    out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    logger.info(
        "wrote %s: %s contributions, current streak %s, longest %s",
        out,
        data["total_contributions"],
        data["current_streak"]["length"],
        data["longest_streak"]["length"],
    )
    return data


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default=GITHUB_USERNAME)
    parser.add_argument("--output", type=Path, default=CONTRIBUTIONS_JSON)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    url = f"https://github.com/users/{args.username}/contributions"
    try:
        fetch_and_save(url=url, out=args.output, username=args.username)
    except RuntimeError as exc:
        logger.error("%s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        logger.exception("unexpected failure: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
