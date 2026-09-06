import unittest

import numpy as np

from astral.kpca import ExactKernelPCA


class KernelPCATests(unittest.TestCase):
    def test_training_coordinates_and_oos_agree(self):
        rng = np.random.default_rng(3)
        x = rng.normal(size=(16, 5))
        kernel = np.exp(-np.linalg.norm(x[:, None] - x[None, :], axis=-1))
        model = ExactKernelPCA(max_rank=8)
        train = model.fit_transform(kernel)
        recovered = model.transform(kernel)
        self.assertTrue(np.allclose(train, recovered, atol=1.0e-8))


if __name__ == "__main__":
    unittest.main()
