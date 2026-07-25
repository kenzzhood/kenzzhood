#!/usr/bin/env python3
"""
Prepare a portrait photo for clean ASCII conversion.

Pipeline
--------
1. Remove the background (rembg) so the subject is isolated.
2. Boost local contrast with OpenCV CLAHE.
3. Composite onto pure white so the background maps to blank ASCII spaces.
4. Write a grayscale PNG consumed by ``make_ascii_svg.py``.

Usage
-----
    python scripts/prep_photo.py [input.jpg] [output.png]

Defaults come from ``config.py`` (assets/profile.jpg → assets/profile-prepped.png).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError

from common import setup_logging

# config import via common's sys.path bootstrap
from config import ASCII, PROFILE_PHOTO, PROFILE_PREPPED  # noqa: E402

logger = setup_logging("prep_photo")


def prepare_photo(inp: Path, out: Path) -> Path:
    """Run the full prep pipeline and return the output path."""
    if not inp.is_file():
        raise FileNotFoundError(f"input image not found: {inp}")

    try:
        source = Image.open(inp).convert("RGBA")
    except UnidentifiedImageError as exc:
        raise ValueError(f"invalid or unsupported image: {inp}") from exc
    except OSError as exc:
        raise ValueError(f"failed to open image: {inp}") from exc

    logger.info("removing background from %s (%dx%d)", inp.name, source.width, source.height)

    try:
        from rembg import remove
    except ImportError as exc:
        raise RuntimeError(
            "rembg is required for background removal. "
            "Install with: pip install rembg"
        ) from exc

    cut = remove(source)
    rgb = np.array(cut.convert("RGB"))
    alpha = np.array(cut.split()[-1])

    # Local contrast (CLAHE) on luminance
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    tile = int(ASCII["clahe_tile"])
    clahe = cv2.createCLAHE(
        clipLimit=float(ASCII["clahe_clip"]),
        tileGridSize=(tile, tile),
    )
    gray = clahe.apply(gray)
    gray = cv2.convertScaleAbs(
        gray,
        alpha=float(ASCII["global_alpha"]),
        beta=int(ASCII["global_beta"]),
    )

    # Feathered composite onto white
    mask = alpha.astype(np.float32) / 255.0
    mask = cv2.GaussianBlur(mask, (0, 0), 1.0)
    composed = gray.astype(np.float32) * mask + 255.0 * (1.0 - mask)
    composed = np.clip(composed, 0, 255).astype(np.uint8)

    # Tight crop to the subject so ASCII isn't mostly empty space
    composed = _crop_to_content(composed, pad_frac=0.06)

    out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(composed, mode="L").save(out)
    logger.info("wrote %s %s", out, composed.shape)
    return out


def _crop_to_content(gray: np.ndarray, pad_frac: float = 0.06) -> np.ndarray:
    """Crop near-white margins; keep a small pad around the subject."""
    content = gray < 248
    if not content.any():
        return gray
    rows = np.any(content, axis=1)
    cols = np.any(content, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    h, w = gray.shape
    pad_y = int((rmax - rmin + 1) * pad_frac)
    pad_x = int((cmax - cmin + 1) * pad_frac)
    rmin = max(0, rmin - pad_y)
    rmax = min(h - 1, rmax + pad_y)
    cmin = max(0, cmin - pad_x)
    cmax = min(w - 1, cmax + pad_x)
    return gray[rmin : rmax + 1, cmin : cmax + 1]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=PROFILE_PHOTO,
        help=f"source photo (default: {PROFILE_PHOTO})",
    )
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=PROFILE_PREPPED,
        help=f"prepped grayscale PNG (default: {PROFILE_PREPPED})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        prepare_photo(args.input, args.output)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        logger.error("%s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001 — exit gracefully
        logger.exception("unexpected failure: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
