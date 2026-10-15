import unittest
from hydropulse.api.schemas import TelemetryIngestRequest
class TestSchemas(unittest.TestCase):
    def test_schema(self):
        req = TelemetryIngestRequest(rain_upstream_weighted_mm=50, soil_saturation_pct=80, current_hanwella_stage_m=2.0)
        self.assertEqual(req.basin, 'Kelani')
