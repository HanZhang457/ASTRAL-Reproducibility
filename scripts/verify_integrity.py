#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astral.audit import (
    load_expected_hashes,
    sha256_file,
    validate_result_csv,
    verify_npz_crc,
    verify_zip_crc,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="validation/EXPECTED_SHA256SUMS.txt")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--output", default="validation/integrity_receipt.json")
    args = parser.parse_args()
    expected = load_expected_hashes(args.manifest)
    receipt = {"files": {}, "result_files": {}, "strict": args.strict}
    failed = False
    for relative, digest in expected.items():
        path = ROOT / relative
        status = {"expected_sha256": digest, "exists": path.exists()}
        if path.exists():
            actual = sha256_file(path)
            status["actual_sha256"] = actual
            status["sha256_match"] = actual == digest
            if path.suffix.lower() == ".zip":
                verify_zip_crc(path)
                status["crc"] = "PASS"
            elif path.suffix.lower() == ".npz":
                verify_npz_crc(path)
                status["crc"] = "PASS"
            failed |= actual != digest
        else:
            status["sha256_match"] = False
            failed |= args.strict
        receipt["files"][relative] = status
    for path in sorted((ROOT / "results").glob("*.csv")):
        if "snapshot" in path.name:
            receipt["result_files"][str(path.relative_to(ROOT))] = {
                "status": "UNVERIFIED_SNAPSHOT_NOT_VALIDATED",
                "reason": (
                    "Manuscript transcription retained for traceability; "
                    "this file is not registered row-level evidence."
                ),
            }
            continue
        try:
            rows = validate_result_csv(path)
            receipt["result_files"][str(path.relative_to(ROOT))] = {
                "status": "PASS",
                "rows": len(rows),
            }
        except (ValueError, KeyError) as exc:
            receipt["result_files"][str(path.relative_to(ROOT))] = {
                "status": "FAIL",
                "reason": str(exc),
            }
            failed = True
    destination = ROOT / args.output
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
