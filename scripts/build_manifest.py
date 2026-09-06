#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDE = {"MANIFEST_SHA256.json", "ASTRAL_PAA_submission_package_FULL_GATES.zip"}
EXCLUDE_SUFFIXES = {".aux", ".blg", ".log", ".out", ".pyc"}


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def main() -> int:
    files = {}
    for path in sorted(ROOT.rglob("*")):
        if (
            path.is_file()
            and path.name not in EXCLUDE
            and path.suffix not in EXCLUDE_SUFFIXES
            and "__pycache__" not in path.parts
        ):
            files[str(path.relative_to(ROOT))] = {
                "bytes": path.stat().st_size,
                "sha256": digest(path),
            }
    output = ROOT / "MANIFEST_SHA256.json"
    output.write_text(json.dumps(files, indent=2, sort_keys=True) + "\n")
    print(f"wrote {output} with {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
