#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import os
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, f1_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astral import AstralConfig, AstralExactClassifier
from astral.io import load_ts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset")
    parser.add_argument("--data-root", default="data/raw")
    parser.add_argument("--config", default="configs/paper.yaml")
    parser.add_argument("--output", default="results/rebuilt_exact.csv")
    args = parser.parse_args()
    dataset = Path(args.data_root) / args.dataset
    train_path = next(dataset.rglob(f"{args.dataset}_TRAIN.ts"))
    test_path = next(dataset.rglob(f"{args.dataset}_TEST.ts"))
    X_train, y_train = load_ts(train_path)
    X_test, y_test = load_ts(test_path)
    config = AstralConfig.from_yaml(args.config)
    start = time.perf_counter()
    classifier = AstralExactClassifier(config).fit(X_train, y_train)
    prediction = classifier.predict(X_test)
    elapsed = time.perf_counter() - start
    correct = int(np.sum(prediction == y_test))
    row = {
        "dataset": args.dataset,
        "method": "ASTRAL-K",
        "seed": str(config.random_state),
        "correct": str(correct),
        "test_count": str(len(y_test)),
        "accuracy": f"{accuracy_score(y_test, prediction):.17g}",
        "macro_f1": f"{f1_score(y_test, prediction, average='macro'):.17g}",
        "elapsed_seconds": f"{elapsed:.6f}",
        "evidence_status": "REBUILT",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    if output.exists():
        with output.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    key = (row["dataset"], row["method"], row["seed"])
    duplicate = [
        old for old in rows
        if (old["dataset"], old["method"], old["seed"]) == key
    ]
    if duplicate:
        scientific = ("correct", "test_count", "accuracy", "macro_f1")
        if all(duplicate[0][field] == row[field] for field in scientific):
            print({**row, "write_status": "SKIP_IDENTICAL_KEY"})
            return 0
        raise RuntimeError(f"duplicate key with conflicting values: {key}")
    rows.append(row)
    with tempfile.NamedTemporaryFile(
        "w", newline="", encoding="utf-8", dir=output.parent, delete=False
    ) as handle:
        temporary = Path(handle.name)
        writer = csv.DictWriter(handle, fieldnames=row)
        writer.writeheader()
        writer.writerows(rows)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, output)
    print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
