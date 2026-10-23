from hydropulse.data.connectors import TelemetryConnector
print(TelemetryConnector().fetch_nasa_gpm_precipitation(None, None, force_mock_latency_hours=7.0))
