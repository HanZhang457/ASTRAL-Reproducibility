#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from astral import AstralConfig, AstralExactClassifier, StructuralTeacher
from astral.descriptors import extract_dataset


def main() -> int:
    rng = np.random.default_rng(7)
    length = 96
    t = np.linspace(0, 2 * np.pi, length)
    X = []
    y = []
    for label, phase in enumerate((0.0, 0.9)):
        for _ in range(12):
            X.append((np.sin(t + phase) + 0.08 * rng.normal(size=length))[None, :])
            y.append(str(label))
    X = np.stack(X)
    y = np.asarray(y)
    cfg = AstralConfig(kernel_rank=8)
    descriptors = extract_dataset(X, cfg)
    teacher = StructuralTeacher(cfg).fit(descriptors)
    K = teacher.kernel(descriptors)
    pi = teacher.fingerprints(descriptors)
    assert np.allclose(K, K.T)
    assert np.linalg.eigvalsh(K).min() > -1.0e-8
    assert np.allclose(pi.sum(axis=-1), 1.0)
    model = AstralExactClassifier(cfg).fit(X, y)
    prediction = model.predict(X)
    assert prediction.shape == y.shape
    print("ASTRAL deterministic smoke test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

