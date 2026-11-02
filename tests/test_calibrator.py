import unittest
import numpy as np
from hydropulse.conformal.calibrator import ConformalHydrologicalCalibrator
class TestCalib(unittest.TestCase):
    def test_c(self):
        c = ConformalHydrologicalCalibrator()
        q = c.calibrate(np.array([1, 2, 3]), np.array([1, 2, 3]))
        self.assertEqual(q, 0.0)
