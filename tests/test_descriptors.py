import unittest

import numpy as np

from astral import AstralConfig
from astral.descriptors import extract_descriptors, moving_average


class DescriptorTests(unittest.TestCase):
    def test_descriptor_dimensions_and_finiteness(self):
        x = np.arange(2 * 31, dtype=float).reshape(2, 31)
        bundle = extract_descriptors(x, AstralConfig())
        self.assertEqual(bundle.trend.shape, (2 * 3 * 2 * 24,))
        self.assertEqual(bundle.residual.shape, (2 * 15,))
        self.assertEqual(bundle.frequency.shape, (2 * 24,))
        self.assertEqual(bundle.shape.shape, (2 * 24,))
        self.assertEqual(bundle.analytic.shape, (2 * 207,))
        self.assertTrue(np.isfinite(bundle.analytic).all())

    def test_decomposition_reconstructs_input(self):
        rng = np.random.default_rng(0)
        x = rng.normal(size=(3, 17))
        trend = moving_average(x, 25)
        residual = x - trend
        self.assertTrue(np.allclose(trend + residual, x, rtol=0.0, atol=1.0e-15))


if __name__ == "__main__":
    unittest.main()
