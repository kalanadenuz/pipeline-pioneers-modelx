"""Telemetry data connectors."""


class TelemetryConnector:
    def __init__(self, cache_dir='data/raw'):
        self.cache_dir = cache_dir
    def fetch_nasa_gpm_precipitation(self, start_time, end_time):
        return {'source': 'NASA_GPM_IMERG_V06', 'resolution': '0.1_deg'}
