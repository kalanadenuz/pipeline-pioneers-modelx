import unittest
import pandas as pd
from hydropulse.features.routing import TopologicalRouter
class TestRoute(unittest.TestCase):
    def test_lags(self):
        df = pd.DataFrame({'rain_upstream_weighted_mm': range(10), 'surface_runoff_mm': range(10)})
        lags = TopologicalRouter().build_lag_features(df)
        self.assertIn('rain_upstream_lag_16h', lags.columns)
