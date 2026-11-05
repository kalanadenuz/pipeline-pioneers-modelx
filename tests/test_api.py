import unittest
from hydropulse.api.main import app
class TestAPI(unittest.TestCase):
    def test_title(self): self.assertEqual(app.title, 'HydroPulse Early-Warning API')
