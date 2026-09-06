#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astral.io import load_ts


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    manifest = yaml.safe_load((ROOT / "data" / "datasets.yaml").read_text())
    receipt = {}
    failed = False
    for item in manifest["datasets"]:
        name = item["name"]
        directory = ROOT / "data" / "raw" / name
        train = list(directory.rglob(f"{name}_TRAIN.ts"))
        test = list(directory.rglob(f"{name}_TEST.ts"))
        state = {"train_files": len(train), "test_files": len(test)}
        if len(train) != 1 or len(test) != 1:
            state["status"] = "BLOCKED_MISSING_OR_AMBIGUOUS"
            failed = True
        else:
            X_train, y_train = load_ts(train[0])
            X_test, y_test = load_ts(test[0])
            observed = {
                "train": int(len(y_train)),
                "test": int(len(y_test)),
                "length": int(X_train.shape[-1]),
                "channels": int(X_train.shape[-2]),
                "classes": int(len(set(y_train) | set(y_test))),
            }
            expected = {key: int(item[key]) for key in observed}
            state.update({"observed": observed, "expected": expected})
            state["train_file"] = {
                "path": str(train[0].relative_to(ROOT)),
                "bytes": train[0].stat().st_size,
                "sha256": sha256(train[0]),
            }
            state["test_file"] = {
                "path": str(test[0].relative_to(ROOT)),
                "bytes": test[0].stat().st_size,
                "sha256": sha256(test[0]),
            }
            state["status"] = "PASS" if observed == expected else "FAIL"
            failed |= observed != expected
        receipt[name] = state
    output = ROOT / "validation" / "dataset_receipt.json"
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
