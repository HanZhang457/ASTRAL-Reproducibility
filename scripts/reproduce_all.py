#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASETS = [
    "ItalyPowerDemand",
    "GunPoint",
    "ArrowHead",
    "ECG200",
    "Coffee",
    "BasicMotions",
    "Epilepsy",
    "AtrialFibrillation",
    "StandWalkJump",
]


def run(*command: str) -> None:
    environment = os.environ.copy()
    source = str(ROOT / "src")
    environment["PYTHONPATH"] = (
        source
        if not environment.get("PYTHONPATH")
        else source + os.pathsep + environment["PYTHONPATH"]
    )
    subprocess.run(command, cwd=ROOT, env=environment, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch-data", action="store_true")
    parser.add_argument("--strict-integrity", action="store_true")
    args = parser.parse_args()
    run(sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v")
    run(sys.executable, "scripts/smoke_test.py")
    if args.fetch_data:
        run(sys.executable, "scripts/fetch_datasets.py")
    if (ROOT / "data" / "raw").exists():
        for dataset in DATASETS:
            run(sys.executable, "scripts/run_exact_astral.py", dataset)
    run(sys.executable, "scripts/generate_figures.py")
    command = [sys.executable, "scripts/verify_integrity.py"]
    if args.strict_integrity:
        command.append("--strict")
    run(*command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
