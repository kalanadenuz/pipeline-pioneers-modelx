import unittest
import pandas as pd
import numpy as np
from hydropulse.data.preprocessor import DataPreprocessor
class TestPrep(unittest.TestCase):
    def test_impute(self):
        df = pd.DataFrame({'a': [1, np.nan, 3]})
        c, r = DataPreprocessor().clean_and_impute(df)
        self.assertEqual(c['a'].isna().sum(), 0)
