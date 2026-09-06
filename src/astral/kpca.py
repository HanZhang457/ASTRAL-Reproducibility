from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class ExactKernelPCA:
    max_rank: int = 96
    eigen_floor: float = 1.0e-10
    eigenvalues_: np.ndarray | None = None
    eigenvectors_: np.ndarray | None = None
    train_column_mean_: np.ndarray | None = None
    train_grand_mean_: float | None = None

    def fit_transform(self, kernel: np.ndarray) -> np.ndarray:
        kernel = np.asarray(kernel, dtype=np.float64)
        if kernel.ndim != 2 or kernel.shape[0] != kernel.shape[1]:
            raise ValueError("training kernel must be square")
        if not np.allclose(kernel, kernel.T, atol=1.0e-10):
            raise ValueError("training kernel must be symmetric")
        self.train_column_mean_ = kernel.mean(axis=0)
        self.train_grand_mean_ = float(kernel.mean())
        centered = (
            kernel
            - kernel.mean(axis=0, keepdims=True)
            - kernel.mean(axis=1, keepdims=True)
            + self.train_grand_mean_
        )
        values, vectors = np.linalg.eigh((centered + centered.T) / 2)
        order = np.argsort(values)[::-1]
        values, vectors = values[order], vectors[:, order]
        positive = values > self.eigen_floor
        rank = min(self.max_rank, kernel.shape[0] - 1, int(positive.sum()))
        self.eigenvalues_ = values[:rank]
        self.eigenvectors_ = vectors[:, :rank]
        return self.eigenvectors_ * np.sqrt(self.eigenvalues_)

    def transform(self, cross_kernel: np.ndarray) -> np.ndarray:
        if (
            self.eigenvalues_ is None
            or self.eigenvectors_ is None
            or self.train_column_mean_ is None
            or self.train_grand_mean_ is None
        ):
            raise RuntimeError("kernel PCA has not been fitted")
        cross = np.asarray(cross_kernel, dtype=np.float64)
        if cross.ndim != 2 or cross.shape[1] != self.train_column_mean_.size:
            raise ValueError("cross kernel must have one column per training case")
        centered = (
            cross
            - self.train_column_mean_[None, :]
            - cross.mean(axis=1, keepdims=True)
            + self.train_grand_mean_
        )
        return (centered @ self.eigenvectors_) / np.sqrt(self.eigenvalues_)

