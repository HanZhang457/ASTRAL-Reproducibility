from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class FrozenStandardizer:
    epsilon: float = 1.0e-12
    mean_: np.ndarray | None = None
    scale_: np.ndarray | None = None

    def fit(self, x: np.ndarray) -> "FrozenStandardizer":
        x = np.asarray(x, dtype=np.float64)
        self.mean_ = x.mean(axis=0)
        scale = x.std(axis=0)
        self.scale_ = np.where(scale > self.epsilon, scale, 1.0)
        return self

    def transform(self, x: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.scale_ is None:
            raise RuntimeError("standardizer has not been fitted")
        return (np.asarray(x, dtype=np.float64) - self.mean_) / self.scale_

    def fit_transform(self, x: np.ndarray) -> np.ndarray:
        return self.fit(x).transform(x)


def energy_balanced_fusion(neural: np.ndarray, analytic: np.ndarray) -> np.ndarray:
    neural = np.asarray(neural, dtype=np.float64)
    analytic = np.asarray(analytic, dtype=np.float64)
    if neural.shape[0] != analytic.shape[0]:
        raise ValueError("blocks must contain the same cases")
    if neural.ndim != 2 or analytic.ndim != 2:
        raise ValueError("blocks must be matrices")
    factor = np.sqrt(neural.shape[1] / analytic.shape[1])
    return np.concatenate([neural, factor * analytic], axis=1)

