import unittest
import pandas as pd
from hydropulse.features.asmi import ASMICalculator
class TestASMI(unittest.TestCase):
    def test_decay(self):
        s = ASMICalculator().compute_asmi(pd.Series([50, 0, 0]))
        self.assertLess(s.iloc[2], s.iloc[0])
