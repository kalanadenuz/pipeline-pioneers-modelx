import unittest
from hydropulse.config import CatchmentConfig
class TestConfig(unittest.TestCase):
    def test_bbox(self):
        self.assertEqual(len(CatchmentConfig.bounding_box), 4)
