#!/usr/bin/env python3
"""Validate profile assets, README references, and contribution data."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import setup_logging
from config import (
    CAPABILITIES_DARK_SVG,
    CAPABILITIES_LIGHT_SVG,
    CASE_STUDIES,
    CONTRIBUTION_DARK_SVG,
    CONTRIBUTION_LIGHT_SVG,
    CONTRIBUTIONS_JSON,
    HERO_DARK_SVG,
    HERO_LIGHT_SVG,
    PROJECTS_DIR,
    RESEARCH_DARK_SVG,
    RESEARCH_LIGHT_SVG,
    ROOT,
)

logger = setup_logging("validate_profile")


def expected_svgs() -> list[Path]:
    """Return every asset required by the generated README."""
    paths = [
        HERO_DARK_SVG,
        HERO_LIGHT_SVG,
        CAPABILITIES_DARK_SVG,
        CAPABILITIES_LIGHT_SVG,
        RESEARCH_DARK_SVG,
        RESEARCH_LIGHT_SVG,
        CONTRIBUTION_DARK_SVG,
        CONTRIBUTION_LIGHT_SVG,
    ]
    for project in CASE_STUDIES:
        slug = str(project["slug"])
        paths.extend(
            [
                PROJECTS_DIR / f"{slug}-dark.svg",
                PROJECTS_DIR / f"{slug}-light.svg",
            ]
        )
    return paths


def validate_svg(path: Path) -> list[str]:
    """Validate XML, accessibility metadata, and self-containment."""
    errors: list[str] = []
    if not path.is_file():
        return [f"missing SVG: {path.relative_to(ROOT)}"]

    text = path.read_text(encoding="utf-8")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        return [f"invalid XML in {path.relative_to(ROOT)}: {exc}"]

    local_name = root.tag.rsplit("}", 1)[-1]
    if local_name != "svg":
        errors.append(f"{path.name}: root element is not svg")
    if not root.get("viewBox"):
        errors.append(f"{path.name}: missing viewBox")
    if "<title" not in text or "<desc" not in text:
        errors.append(f"{path.name}: missing accessible title/description")
    if re.search(r"<\s*script\b", text, re.IGNORECASE):
        errors.append(f"{path.name}: script tags are forbidden")

    for element in root.iter():
        for attribute, value in element.attrib.items():
            if attribute.endswith("href") and value.startswith(("http://", "https://")):
                errors.append(f"{path.name}: external SVG dependency {value}")
    return errors


def validate_readme(path: Path) -> list[str]:
    """Ensure README artwork is local, present, and semantically described."""
    if not path.is_file():
        return ["README.md is missing"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if re.search(r'(?:src|srcset)="https?://', text, re.IGNORECASE):
        errors.append("README contains externally hosted visual assets")
    if "<script" in text.lower():
        errors.append("README contains a script tag")

    references = re.findall(r'(?:src|srcset)="([^"]+)"', text)
    for reference in references:
        clean = reference.split("#", 1)[0].split("?", 1)[0]
        if not clean.startswith("./"):
            continue
        target = ROOT / clean[2:]
        if not target.is_file():
            errors.append(f"README references missing asset: {clean}")

    images = re.findall(r"<img\b[^>]*>", text, re.IGNORECASE)
    for image in images:
        if not re.search(r'\balt="[^"]+"', image):
            errors.append("README image is missing non-empty alt text")
    return errors


def validate_contributions(path: Path) -> list[str]:
    """Sanity-check the scraped contribution payload."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid contribution data: {exc}"]

    errors: list[str] = []
    days = data.get("days", [])
    if len(days) < 350:
        errors.append(f"contribution data contains only {len(days)} days")
    if data.get("total_contributions", -1) < 0:
        errors.append("total_contributions must be non-negative")
    dates = [day.get("date") for day in days]
    if dates != sorted(dates):
        errors.append("contribution days are not chronological")
    return errors


def main() -> int:
    errors: list[str] = []
    for path in expected_svgs():
        errors.extend(validate_svg(path))
    errors.extend(validate_readme(ROOT / "README.md"))
    errors.extend(validate_contributions(CONTRIBUTIONS_JSON))

    if errors:
        for error in errors:
            logger.error("%s", error)
        logger.error("validation failed with %d issue(s)", len(errors))
        return 1

    logger.info(
        "profile valid: %d SVGs, README references, contribution data",
        len(expected_svgs()),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
