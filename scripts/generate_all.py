#!/usr/bin/env python3
"""Generate and validate the editorial profile README."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from common import setup_logging

logger = setup_logging("generate_all")
SCRIPTS_DIR = Path(__file__).resolve().parent


def run(script: str) -> None:
    command = [sys.executable, str(SCRIPTS_DIR / script)]
    logger.info("$ %s", " ".join(command))
    subprocess.run(command, check=True)


def main() -> int:
    try:
        run("render_readme.py")
        run("validate_profile.py")
    except subprocess.CalledProcessError as exc:
        logger.error("profile generation failed with exit code %s", exc.returncode)
        return exc.returncode
    logger.info("profile generated successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
