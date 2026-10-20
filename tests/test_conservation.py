import unittest
import pandas as pd
from hydropulse.data.preprocessor import DataPreprocessor
class TestCons(unittest.TestCase):
    def test_cons(self):
        df = pd.DataFrame({'rain_upstream_weighted_mm': [100], 'surface_runoff_mm': [80]})
        self.assertTrue(DataPreprocessor().verify_physical_conservation(df))
