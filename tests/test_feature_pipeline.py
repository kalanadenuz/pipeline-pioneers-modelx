import unittest
from hydropulse.features.pipeline import HydrologicalFeaturePipeline
from hydropulse.data.synthetic_generator import KelaniDataGenerator
class TestPipe(unittest.TestCase):
    def test_p(self):
        df = KelaniDataGenerator().generate_time_series('2024-01-01', '2024-01-10')
        X, y, f = HydrologicalFeaturePipeline().build_feature_matrix(df)
        self.assertEqual(len(X), len(y))
