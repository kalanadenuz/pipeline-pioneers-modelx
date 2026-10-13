# Test GPM query
from hydropulse.data.connectors import TelemetryConnector
c = TelemetryConnector()
print(c.fetch_nasa_gpm_precipitation(None, None))
