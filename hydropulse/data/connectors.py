"""Telemetry data connectors."""


class TelemetryConnector:
    def __init__(self, cache_dir='data/raw'):
        self.cache_dir = cache_dir
    def fetch_nasa_gpm_precipitation(self, start_time, end_time):
        return {'source': 'NASA_GPM_IMERG_V06', 'resolution': '0.1_deg'}


    def fetch_kelani_gauge_telemetry(self, station='Hanwella'):
        return {'source': 'Sri_Lanka_Irrigation_Department', 'station': station, 'baseline_m': 1.80}


    def fetch_copernicus_era5_soil_moisture(self, start_time, end_time):
        return {'source': 'ECMWF_ERA5_LAND_CDS', 'variables': ['volumetric_soil_water_layer_1', 'volumetric_soil_water_layer_2', 'surface_runoff']}
