#!/usr/bin/env python3
"""Stamp the Python SDK version from the SINGLE source of truth: the repo-root
VERSION file.

Keeps ``pyproject.toml``'s ``version`` and ``scalix_sdk/_version.py`` in lockstep
with the gateway spec + TypeScript SDK, so the version strings can never drift.
Run automatically by ``scripts/generate.sh``; also safe to run standalone:
``python3 scripts/sync_version.py``.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent.parent
VERSION_FILE = PKG_DIR.parent.parent / "VERSION"


def main() -> int:
    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    if not re.match(r"^\d+\.\d+\.\d+", version):
        print(f"sync_version: VERSION file has an unexpected value: {version!r}", file=sys.stderr)
        return 1

    # pyproject.toml — replace only the first top-level `version = "..."`.
    pyproject = PKG_DIR / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")
    new_text, n = re.subn(
        r'(?m)^version = "[^"]*"', f'version = "{version}"', text, count=1
    )
    if n != 1:
        print("sync_version: could not find the version field in pyproject.toml", file=sys.stderr)
        return 1
    if new_text != text:
        pyproject.write_text(new_text, encoding="utf-8")
        print(f"sync_version: pyproject.toml -> {version}")

    # scalix_sdk/_version.py — the runtime __version__ (used for the User-Agent).
    version_py = PKG_DIR / "scalix_sdk" / "_version.py"
    version_py.write_text(f'__version__ = "{version}"\n', encoding="utf-8")
    print(f"sync_version: scalix_sdk/_version.py -> {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
