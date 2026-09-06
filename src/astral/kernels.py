from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.spatial.distance import cdist

from .config import AstralConfig
from .descriptors import DescriptorBundle


def _positive_median_distance(
    x: np.ndarray, pair_count: int, rng: np.random.Generator, floor: float
) -> float:
    n = x.shape[0]
    if n < 2:
        return floor
    total = min(pair_count, n * (n - 1))
    pairs: set[tuple[int, int]] = set()
    while len(pairs) < total:
        i = int(rng.integers(n))
        j = int(rng.integers(n - 1))
        if j >= i:
            j += 1
        pairs.add((i, j))
    distances = np.fromiter(
        (np.linalg.norm(x[i] - x[j]) for i, j in sorted(pairs)),
        dtype=np.float64,
    )
    positive = distances[distances > 0]
    return max(float(np.median(positive)) if positive.size else floor, floor)


@dataclass
class StructuralTeacher:
    config: AstralConfig = AstralConfig()
    taus_: tuple[float, float, float] | None = None

    def fit(self, descriptors: DescriptorBundle) -> "StructuralTeacher":
        rng = np.random.default_rng(self.config.random_state)
        arrays = (descriptors.trend, descriptors.residual, descriptors.frequency)
        self.taus_ = tuple(
            _positive_median_distance(
                array,
                self.config.calibration_pairs,
                rng,
                self.config.epsilon,
            )
            for array in arrays
        )
        return self

    def _check(self) -> tuple[float, float, float]:
        if self.taus_ is None:
            raise RuntimeError("teacher has not been fitted")
        return self.taus_

    def component_kernels(
        self, left: DescriptorBundle, right: DescriptorBundle | None = None
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        taus = self._check()
        right = right or left
        pairs = (
            (left.trend, right.trend),
            (left.residual, right.residual),
            (left.frequency, right.frequency),
        )
        return tuple(
            np.exp(-cdist(a, b, metric="euclidean") / tau)
            for (a, b), tau in zip(pairs, taus)
        )

    def kernel(
        self, left: DescriptorBundle, right: DescriptorBundle | None = None
    ) -> np.ndarray:
        components = self.component_kernels(left, right)
        out = sum(
            weight * component
            for weight, component in zip(self.config.component_weights, components)
        )
        if not np.isfinite(out).all():
            raise FloatingPointError("joint kernel contains nonfinite values")
        return out

    def fingerprints(
        self, left: DescriptorBundle, right: DescriptorBundle | None = None
    ) -> np.ndarray:
        components = self.component_kernels(left, right)
        weighted = np.stack(
            [
                weight * component
                for weight, component in zip(
                    self.config.component_weights, components
                )
            ],
            axis=-1,
        )
        joint = weighted.sum(axis=-1, keepdims=True)
        return weighted / np.maximum(joint, self.config.epsilon)

