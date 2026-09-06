from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import yaml


@dataclass(frozen=True)
class AstralConfig:
    windows: Tuple[int, ...] = (5, 11, 25)
    pool_length: int = 24
    acf_lags: int = 12
    component_weights: Tuple[float, float, float] = (0.4, 0.3, 0.3)
    calibration_pairs: int = 1024
    epsilon: float = 1.0e-6
    kernel_rank: int = 96
    probe_c: float = 1.0
    probe_max_iter: int = 3000
    random_state: int = 0

    def __post_init__(self) -> None:
        if not self.windows or any(w <= 0 or w % 2 == 0 for w in self.windows):
            raise ValueError("windows must be positive odd integers")
        if self.pool_length <= 0 or self.acf_lags < 0:
            raise ValueError("invalid descriptor dimensions")
        if len(self.component_weights) != 3:
            raise ValueError("exactly three component weights are required")
        if any(a < 0 for a in self.component_weights):
            raise ValueError("component weights must be nonnegative")
        if abs(sum(self.component_weights) - 1.0) > 1.0e-12:
            raise ValueError("component weights must sum to one")
        if self.epsilon <= 0 or self.kernel_rank <= 0:
            raise ValueError("epsilon and kernel_rank must be positive")

    @classmethod
    def from_yaml(cls, path: str | Path) -> "AstralConfig":
        raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        method = raw["method"]
        probe = raw["probe"]
        random = raw["random"]
        return cls(
            windows=tuple(method["windows"]),
            pool_length=int(method["pool_length"]),
            acf_lags=int(method["acf_lags"]),
            component_weights=tuple(float(x) for x in method["component_weights"]),
            calibration_pairs=int(method["calibration_pairs"]),
            epsilon=float(method["descriptor_epsilon"]),
            kernel_rank=int(method["kernel_rank"]),
            probe_c=float(probe["C"]),
            probe_max_iter=int(probe["max_iter"]),
            random_state=int(random["calibration_seed"]),
        )

