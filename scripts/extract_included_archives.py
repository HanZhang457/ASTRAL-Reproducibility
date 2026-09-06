#!/usr/bin/env python3
from __future__ import annotations

import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVES = ROOT / "data" / "archives"
RAW = ROOT / "data" / "raw"


def safe_extract(archive: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive) as zipped:
        if zipped.testzip() is not None:
            raise RuntimeError(f"CRC failure: {archive}")
        root = destination.resolve()
        for member in zipped.infolist():
            target = (destination / member.filename).resolve()
            if root != target and root not in target.parents:
                raise RuntimeError(f"unsafe member in {archive}: {member.filename}")
        zipped.extractall(destination)


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    names = sorted({path.name.split(".zip.part", 1)[0] for path in ARCHIVES.glob("*.zip.part*")})
    for name in names:
        parts = sorted(ARCHIVES.glob(f"{name}.zip.part*"))
        archive = RAW / f"{name}.zip"
        with archive.open("wb") as output:
            for part in parts:
                with part.open("rb") as source:
                    shutil.copyfileobj(source, output)
        destination = RAW / name
        destination.mkdir(exist_ok=True)
        safe_extract(archive, destination)
        print(f"extracted {name} from {len(parts)} part(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
