#!/usr/bin/env python3
"""
One-command generator for all README assets.

Runs (in order):
  1. prep_photo          (optional — skip with --skip-photo)
  2. make_ascii_svg
  3. make_neofetch
  4. make_banner
  5. fetch_contributions
  6. render_heatmap_svg
  7. fetch_repos         (optional — skip with --skip-repos)

Usage
-----
    python scripts/generate_all.py
    python scripts/generate_all.py --skip-photo   # reuse existing prepped PNG
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from common import setup_logging
from config import PROFILE_PREPPED, ROOT

logger = setup_logging("generate_all")

SCRIPTS = ROOT / "scripts"


def run_script(name: str, *extra: str) -> None:
    """Execute a sibling script; raise on non-zero exit."""
    path = SCRIPTS / name
    cmd = [sys.executable, str(path), *extra]
    logger.info("$ %s", " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"{name} failed with exit code {result.returncode}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-photo",
        action="store_true",
        help="skip rembg / CLAHE prep (reuse profile-prepped.png)",
    )
    parser.add_argument(
        "--skip-repos",
        action="store_true",
        help="skip GitHub API repo listing",
    )
    parser.add_argument(
        "--heatmap-only",
        action="store_true",
        help="only refresh contributions + heatmap (CI path)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.heatmap_only:
            run_script("fetch_contributions.py")
            run_script("render_heatmap_svg.py")
            return 0

        if not args.skip_photo:
            run_script("prep_photo.py")
        elif not PROFILE_PREPPED.is_file():
            logger.error("%s missing — run without --skip-photo", PROFILE_PREPPED)
            return 1

        run_script("make_ascii_svg.py")
        run_script("make_neofetch.py")
        run_script("make_banner.py")
        run_script("fetch_contributions.py")
        run_script("render_heatmap_svg.py")

        if not args.skip_repos:
            try:
                run_script("fetch_repos.py")
            except RuntimeError as exc:
                logger.warning("repo fetch skipped: %s", exc)

        logger.info("all assets generated successfully")
    except RuntimeError as exc:
        logger.error("%s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        logger.exception("unexpected failure: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
