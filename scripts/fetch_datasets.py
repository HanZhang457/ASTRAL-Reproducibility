#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import urllib.request
import zipfile
from pathlib import Path

import yaml


BASE = "https://www.timeseriesclassification.com/aeon-toolkit/{name}.zip"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_extract(zipped: zipfile.ZipFile, destination: Path) -> None:
    root = destination.resolve()
    for member in zipped.infolist():
        target = (destination / member.filename).resolve()
        if root != target and root not in target.parents:
            raise RuntimeError(f"unsafe archive member: {member.filename}")
    zipped.extractall(destination)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="data/datasets.yaml")
    parser.add_argument("--output", default="data/raw")
    parser.add_argument("--keep-archives", action="store_true")
    args = parser.parse_args()
    root = Path(args.output)
    root.mkdir(parents=True, exist_ok=True)
    manifest = yaml.safe_load(Path(args.manifest).read_text(encoding="utf-8"))
    receipt = {}
    for item in manifest["datasets"]:
        name = item["name"]
        archive = root / f"{name}.zip"
        url = item.get("url", BASE.format(name=name))
        print(f"downloading {name} from {url}")
        with urllib.request.urlopen(url) as source, archive.open("wb") as target:
            shutil.copyfileobj(source, target)
        with zipfile.ZipFile(archive) as zipped:
            bad = zipped.testzip()
            if bad is not None:
                raise RuntimeError(f"CRC failure in {name}: {bad}")
            destination = root / name
            destination.mkdir(exist_ok=True)
            safe_extract(zipped, destination)
        receipt[name] = {
            "archive_sha256": sha256(archive),
            "train": item["train"],
            "test": item["test"],
            "length": item["length"],
            "channels": item["channels"],
            "classes": item["classes"],
            "url": url,
        }
        if not args.keep_archives:
            archive.unlink()
    (root / "DOWNLOAD_RECEIPT.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
