#!/usr/bin/env python3
"""Validate the editorial README's structure and factual links."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from common import setup_logging
from config import ROOT

logger = setup_logging("validate_profile")

REQUIRED_SECTIONS = (
    "## Experience",
    "## Selected work",
    "## Publication",
    "## Recognition",
    "## Technical skills",
    "## Education",
    "## Leadership",
)

REQUIRED_LINKS = (
    "https://innoxrlabs.com",
    "https://github.com/kenzzhood/AuraFit",
    "https://github.com/kenzzhood/AutoOps",
    "https://github.com/kenzzhood/Wander_Lens",
    "https://github.com/kenzzhood/MILES",
    "https://doi.org/10.1109/RMKMATE69073.2026.11518707",
    "https://www.linkedin.com/in/goutham-srinath-380446288",
)


def validate(path: Path) -> list[str]:
    if not path.is_file():
        return ["README.md is missing"]

    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"missing section: {section}")
    for link in REQUIRED_LINKS:
        if link not in text:
            errors.append(f"missing verified link: {link}")

    if "<img" in text.lower() or "<picture" in text.lower():
        errors.append("editorial profile must not depend on decorative artwork")
    if re.search(r"<\s*script\b", text, re.IGNORECASE):
        errors.append("README contains a forbidden script tag")
    if len(text) > 12_000:
        errors.append("README is too long for a concise public profile")

    return errors


def main() -> int:
    errors = validate(ROOT / "README.md")
    if errors:
        for error in errors:
            logger.error("%s", error)
        return 1
    logger.info("editorial profile README is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
