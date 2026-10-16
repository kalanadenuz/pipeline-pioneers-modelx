import unittest
from hydropulse.data.synthetic_generator import KelaniDataGenerator
class TestGen(unittest.TestCase):
    def test_len(self):
        df = KelaniDataGenerator().generate_time_series('2024-01-01', '2024-01-05')
        self.assertGreater(len(df), 20)
