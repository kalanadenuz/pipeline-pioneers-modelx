"""Physical Catchment Hydrodynamics Simulator and Dataset Generator."""
import numpy as np
import pandas as pd
from hydropulse.config import CatchmentConfig, PhysicsConfig

class KelaniDataGenerator:
    def __init__(self, seed: int = 42):
        self.seed = seed
        self.catchment = CatchmentConfig()
        self.physics = PhysicsConfig()
        np.random.seed(seed)

    def generate_time_series(self, start_date: str = "2020-01-01", end_date: str = "2024-12-31", freq_hours: int = 4) -> pd.DataFrame:
        timestamps = pd.date_range(start=start_date, end=end_date, freq=f"{freq_hours}h")
        n = len(timestamps)

        day_of_year = timestamps.dayofyear.values
        sw_monsoon = np.exp(-0.5 * ((day_of_year - 150) / 30) ** 2) * 1.5
        sim_monsoon = np.exp(-0.5 * ((day_of_year - 305) / 25) ** 2) * 1.8
        seasonal_intensity = 0.2 + sw_monsoon + sim_monsoon

        rain_prob = 0.15 * seasonal_intensity
        rain_events = (np.random.rand(n) < rain_prob).astype(float)

        rain_norton = rain_events * np.random.gamma(shape=2.5, scale=12.0 * seasonal_intensity, size=n)
        rain_castlereigh = rain_events * np.random.gamma(shape=2.3, scale=11.0 * seasonal_intensity, size=n)
        rain_kitulgala = rain_events * np.random.gamma(shape=2.0, scale=9.5 * seasonal_intensity, size=n)
        rain_deraniyagala = rain_events * np.random.gamma(shape=1.8, scale=8.0 * seasonal_intensity, size=n)
        rain_hanwella_local = (np.random.rand(n) < (rain_prob * 0.4)).astype(float) * np.random.gamma(shape=1.5, scale=5.0 * seasonal_intensity, size=n)

        rain_upstream_weighted = 0.30 * rain_norton + 0.25 * rain_castlereigh + 0.25 * rain_kitulgala + 0.20 * rain_deraniyagala

        soil_water_l1 = np.zeros(n)
        soil_water_l2 = np.zeros(n)
        asmi_index = np.zeros(n)

        sw1 = 0.22
        sw2 = 0.26
        asmi = 25.0
        decay = np.exp(-(freq_hours / 24.0) * (1.0 - self.physics.asmi_decay_factor))

        for t in range(n):
            p = rain_upstream_weighted[t]
            sw1 = sw1 * decay + (p / 250.0) * (0.48 - sw1)
            sw1 = np.clip(sw1, 0.14, 0.46)
            sw2 = sw2 * (decay ** 0.5) + (sw1 * 0.05)
            sw2 = np.clip(sw2, 0.18, 0.48)
            asmi = asmi * decay + p
            soil_water_l1[t] = sw1
            soil_water_l2[t] = sw2
            asmi_index[t] = asmi

        soil_saturation_pct = np.clip((asmi_index / self.physics.soil_saturation_threshold_mm) * 100.0, 5.0, 99.5)
        effective_runoff_coeff = self.physics.runoff_coefficient_dry + ((self.physics.runoff_coefficient_saturated - self.physics.runoff_coefficient_dry) * (soil_saturation_pct / 100.0) ** 2.2)
        surface_runoff = rain_upstream_weighted * effective_runoff_coeff

        routing_kernel = np.array([0.00, 0.00, 0.05, 0.20, 0.45, 0.20, 0.10])
        full_conv = np.convolve(surface_runoff, routing_kernel, mode="full")
        routed_runoff = full_conv[:n]

        baseflow = 1.80 + 0.20 * np.sin(2 * np.pi * day_of_year / 365.25)
        stage_surge = (routed_runoff / 14.0) ** 1.15 + (rain_hanwella_local / 80.0)
        stage_height = baseflow + stage_surge + np.random.normal(0, 0.03, size=n)

        srai = (stage_surge - np.mean(stage_surge)) / (np.std(stage_surge) + 1e-6)
        inundation_depth = np.maximum(0.0, stage_surge - 0.45)

        return pd.DataFrame({
            "timestamp": timestamps,
            "rain_norton_mm": np.round(rain_norton, 2),
            "rain_castlereigh_mm": np.round(rain_castlereigh, 2),
            "rain_kitulgala_mm": np.round(rain_kitulgala, 2),
            "rain_deraniyagala_mm": np.round(rain_deraniyagala, 2),
            "rain_hanwella_local_mm": np.round(rain_hanwella_local, 2),
            "rain_upstream_weighted_mm": np.round(rain_upstream_weighted, 2),
            "era5_soil_water_l1": np.round(soil_water_l1, 4),
            "era5_soil_water_l2": np.round(soil_water_l2, 4),
            "asmi_mm": np.round(asmi_index, 2),
            "soil_saturation_pct": np.round(soil_saturation_pct, 1),
            "surface_runoff_mm": np.round(surface_runoff, 2),
            "hanwella_stage_m": np.round(stage_height, 2),
            "stage_surge_m": np.round(stage_surge, 2),
            "srai": np.round(srai, 2),
            "plot_inundation_depth_m": np.round(inundation_depth, 2),
        })

    def inject_extreme_storm_event(self, df: pd.DataFrame, storm_date: str = "2024-05-18") -> pd.DataFrame:
        df = df.copy()
        idx = df[df["timestamp"] >= storm_date].index
        if len(idx) < 18:
            return df
        start_idx = idx[0]
        for i in range(max(0, start_idx - 18), start_idx):
            df.loc[i, "rain_upstream_weighted_mm"] += 25.0
            df.loc[i, "soil_saturation_pct"] = min(94.0, 75.0 + (i - start_idx + 18) * 1.1)
            df.loc[i, "asmi_mm"] = 172.0

        df.loc[start_idx, "rain_norton_mm"] = 110.0
        df.loc[start_idx, "rain_castlereigh_mm"] = 95.0
        df.loc[start_idx, "rain_kitulgala_mm"] = 70.0
        df.loc[start_idx, "rain_upstream_weighted_mm"] = 92.0
        df.loc[start_idx, "rain_hanwella_local_mm"] = 0.0
        df.loc[start_idx, "soil_saturation_pct"] = 92.4

        df.loc[start_idx + 1, "rain_norton_mm"] = 75.0
        df.loc[start_idx + 1, "rain_castlereigh_mm"] = 68.0
        df.loc[start_idx + 1, "rain_kitulgala_mm"] = 45.0
        df.loc[start_idx + 1, "rain_upstream_weighted_mm"] = 68.0
        df.loc[start_idx + 1, "rain_hanwella_local_mm"] = 2.0
        df.loc[start_idx + 1, "soil_saturation_pct"] = 95.8

        peak_idx = start_idx + 4
        df.loc[peak_idx, "stage_surge_m"] = 1.10
        df.loc[peak_idx, "hanwella_stage_m"] = 3.10
        df.loc[peak_idx, "plot_inundation_depth_m"] = 0.65

        df.loc[peak_idx + 1, "stage_surge_m"] = 1.05
        df.loc[peak_idx + 1, "hanwella_stage_m"] = 3.05
        df.loc[peak_idx + 1, "plot_inundation_depth_m"] = 0.60
        return df


# Monsoonal seasonal intensity factors tuned to Kelani wet-zone
