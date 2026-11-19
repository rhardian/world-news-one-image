#!/usr/bin/env python3
"""make.fun news-image-20261118 entry point (Python 3.13, standard library only).

The graded program copies the pre-rendered front page of 18 November 2026
world news (assets/entry.png) to the output directory. The image is rendered
offline by render_news_image.py; copying keeps both graded runs byte-identical
and needs no network, no dependencies and no randomness.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SOURCE_IMAGE = REPO_ROOT / "assets" / "entry.png"


def output_dir() -> Path:
    """The grader writes to /output; locally MAKEFUN_OUTPUT_DIR stands in."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> int:
    if not SOURCE_IMAGE.is_file():
        print(f"entry image missing: {SOURCE_IMAGE}", file=sys.stderr)
        return 1
    head = SOURCE_IMAGE.read_bytes()[:8]
    if head != b"\x89PNG\r\n\x1a\n":
        print("entry image is not a PNG", file=sys.stderr)
        return 1
    if SOURCE_IMAGE.stat().st_size > 1048576:
        print("entry image exceeds the 1 MiB gate limit", file=sys.stderr)
        return 1
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(SOURCE_IMAGE, target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()[:16]
    print(f"wrote {target} ({target.stat().st_size} bytes, sha256:{digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
