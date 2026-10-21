import unittest
from hydropulse.data.connectors import TelemetryConnector
class TestConn(unittest.TestCase):
    def test_gpm(self):
        res = TelemetryConnector().fetch_nasa_gpm_precipitation(None, None)
        self.assertEqual(res['source'], 'NASA_GPM_IMERG_V06')
