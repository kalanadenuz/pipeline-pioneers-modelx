import unittest
from hydropulse.models.trainer import ModelTrainer
class TestTrainer(unittest.TestCase):
    def test_init(self): self.assertIsNotNone(ModelTrainer())
