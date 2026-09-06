from __future__ import annotations

import csv
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Iterable

import numpy as np


def sha256_file(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_zip_crc(path: str | Path) -> None:
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad is not None:
            raise ValueError(f"CRC failure in {path}: {bad}")


def verify_npz_crc(path: str | Path) -> None:
    verify_zip_crc(path)
    with np.load(path, allow_pickle=False) as data:
        for name in data.files:
            value = data[name]
            if np.issubdtype(value.dtype, np.number) and not np.isfinite(value).all():
                raise ValueError(f"nonfinite values in NPZ array {name}")


def load_expected_hashes(path: str | Path) -> dict[str, str]:
    expected: dict[str, str] = {}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        digest, name = line.split(maxsplit=1)
        expected[name.strip()] = digest.lower()
    return expected


def validate_result_rows(
    rows: Iterable[dict[str, str]],
    key_fields: tuple[str, ...] = ("dataset", "method", "seed"),
) -> list[dict[str, str]]:
    materialized = list(rows)
    seen: set[tuple[str, ...]] = set()
    for index, row in enumerate(materialized, start=1):
        key = tuple(row[field] for field in key_fields)
        if key in seen:
            raise ValueError(f"duplicate experimental key at row {index}: {key}")
        seen.add(key)
        correct = int(row["correct"])
        test_count = int(row["test_count"])
        accuracy = float(row["accuracy"])
        macro_f1 = float(row["macro_f1"])
        if test_count <= 0 or not (0 <= correct <= test_count):
            raise ValueError(f"invalid counts at row {index}")
        if not np.isfinite([accuracy, macro_f1]).all():
            raise ValueError(f"nonfinite metric at row {index}")
        if abs(accuracy - correct / test_count) > 5.0e-12:
            raise ValueError(f"accuracy/count mismatch at row {index}")
    return materialized


def validate_result_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return validate_result_rows(csv.DictReader(handle))


def write_json_atomic(path: str | Path, payload: object) -> None:
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)

