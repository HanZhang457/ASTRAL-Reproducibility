from __future__ import annotations

from pathlib import Path

import numpy as np


def load_ts(path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    """Load a fixed-length UCR/UEA .ts classification file.

    The parser supports timestamp-free, colon-separated multivariate rows with
    the class label in the final field. Missing values are rejected.
    """
    path = Path(path)
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    in_data = False
    cases: list[np.ndarray] = []
    labels: list[str] = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if not in_data:
            if line.lower().startswith("@data"):
                in_data = True
            continue
        fields = line.split(":")
        if len(fields) < 2:
            raise ValueError(f"invalid .ts data row in {path}")
        channels = []
        for field in fields[:-1]:
            if "?" in field:
                raise ValueError(f"missing values are not permitted: {path}")
            channels.append(np.asarray([float(v) for v in field.split(",")], dtype=float))
        lengths = {row.size for row in channels}
        if len(lengths) != 1:
            raise ValueError(f"variable-length rows are outside this release: {path}")
        cases.append(np.stack(channels))
        labels.append(fields[-1].strip())
    if not cases:
        raise ValueError(f"no data rows found in {path}")
    shapes = {x.shape for x in cases}
    if len(shapes) != 1:
        raise ValueError(f"dataset is not fixed-shape: {path}")
    return np.stack(cases), np.asarray(labels)

