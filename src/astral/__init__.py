"""Reference implementation of the deterministic ASTRAL teacher."""

from .config import AstralConfig
from .descriptors import DescriptorBundle, extract_descriptors
from .kernels import StructuralTeacher
from .kpca import ExactKernelPCA
from .pipeline import AstralExactClassifier

__all__ = [
    "AstralConfig",
    "DescriptorBundle",
    "extract_descriptors",
    "StructuralTeacher",
    "ExactKernelPCA",
    "AstralExactClassifier",
]

