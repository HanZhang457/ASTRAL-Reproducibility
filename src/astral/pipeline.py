from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from sklearn.linear_model import LogisticRegression

from .config import AstralConfig
from .descriptors import DescriptorBundle, extract_dataset
from .kernels import StructuralTeacher
from .kpca import ExactKernelPCA


@dataclass
class AstralExactClassifier:
    """Leakage-safe ASTRAL-K reference pipeline."""

    config: AstralConfig = field(default_factory=AstralConfig)
    teacher_: StructuralTeacher | None = None
    kpca_: ExactKernelPCA | None = None
    classifier_: LogisticRegression | None = None
    train_descriptors_: DescriptorBundle | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "AstralExactClassifier":
        descriptors = extract_dataset(X, self.config)
        teacher = StructuralTeacher(self.config).fit(descriptors)
        kernel = teacher.kernel(descriptors)
        kpca = ExactKernelPCA(self.config.kernel_rank)
        coordinates = kpca.fit_transform(kernel)
        classifier = LogisticRegression(
            C=self.config.probe_c,
            max_iter=self.config.probe_max_iter,
            random_state=self.config.random_state,
        )
        classifier.fit(coordinates, y)
        self.train_descriptors_ = descriptors
        self.teacher_, self.kpca_, self.classifier_ = teacher, kpca, classifier
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if (
            self.teacher_ is None
            or self.kpca_ is None
            or self.train_descriptors_ is None
        ):
            raise RuntimeError("pipeline has not been fitted")
        descriptors = extract_dataset(X, self.config)
        cross = self.teacher_.kernel(descriptors, self.train_descriptors_)
        return self.kpca_.transform(cross)

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.classifier_ is None:
            raise RuntimeError("pipeline has not been fitted")
        return self.classifier_.predict(self.transform(X))

