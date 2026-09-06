import unittest

import numpy as np

from astral import AstralConfig
from astral.descriptors import extract_dataset
from astral.kernels import StructuralTeacher


class KernelTests(unittest.TestCase):
    def test_kernel_psd_and_fingerprint_conservation(self):
        rng = np.random.default_rng(2)
        X = rng.normal(size=(12, 1, 48))
        cfg = AstralConfig(calibration_pairs=40)
        descriptors = extract_dataset(X, cfg)
        teacher = StructuralTeacher(cfg).fit(descriptors)
        kernel = teacher.kernel(descriptors)
        fingerprint = teacher.fingerprints(descriptors)
        self.assertTrue(np.allclose(kernel, kernel.T))
        self.assertGreater(np.linalg.eigvalsh(kernel).min(), -1.0e-8)
        self.assertTrue(np.all(fingerprint >= 0))
        self.assertTrue(np.allclose(fingerprint.sum(axis=-1), 1.0))


if __name__ == "__main__":
    unittest.main()
