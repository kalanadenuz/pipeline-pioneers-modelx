import unittest
import pandas as pd
from hydropulse.models.baselines import PersistenceBaseline, LinearLagBaseline
class TestBase(unittest.TestCase):
    def test_pers(self):
        df = pd.DataFrame({'current_surge_m': [0.5]})
        self.assertEqual(PersistenceBaseline().predict(df)[0], 0.5)
