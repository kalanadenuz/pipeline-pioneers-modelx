import unittest
import numpy as np
from hydropulse.models.regressor import FastRegressionTree
class TestTree(unittest.TestCase):
    def test_fit(self):
        t = FastRegressionTree(max_depth=3)
        t.fit(np.random.randn(30, 4), np.random.randn(30))
        p = t.predict(np.random.randn(5, 4))
        self.assertEqual(len(p), 5)
