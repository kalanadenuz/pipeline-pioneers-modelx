"""Comprehensive Feature Pipeline for HydroPulse."""
import pandas as pd
from typing import Tuple, List
from hydropulse.features.asmi import ASMICalculator
from hydropulse.features.routing import TopologicalRouter

class HydrologicalFeaturePipeline:
    def __init__(self):
        self.asmi_calc = ASMICalculator()
        self.router = TopologicalRouter()

    def build_feature_matrix(self, df: pd.DataFrame, target_horizon_steps: int = 4) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
        df = df.copy()
        if "rain_upstream_weighted_mm" not in df.columns:
            df["rain_upstream_weighted_mm"] = self.router.compute_weighted_upstream_rain(df)
        if "asmi_mm" not in df.columns:
            df["asmi_mm"] = self.asmi_calc.compute_asmi(df["rain_upstream_weighted_mm"])
            df["soil_saturation_pct"] = self.asmi_calc.estimate_saturation_percentage(df["asmi_mm"])

        lag_df = self.router.build_lag_features(df, lags_steps=[1, 2, 3, 4, 5, 6])
        features = pd.DataFrame(index=df.index)
        features["asmi_mm"] = df["asmi_mm"]
        features["soil_saturation_pct"] = df["soil_saturation_pct"]
        features["era5_soil_water_l1"] = df["era5_soil_water_l1"]
        features["era5_soil_water_l2"] = df["era5_soil_water_l2"]
        features["rain_upstream_current"] = df["rain_upstream_weighted_mm"]
        features["rain_local_hanwella"] = df["rain_hanwella_local_mm"]
        features["current_hanwella_stage"] = df["hanwella_stage_m"]
        features["current_surge_m"] = df["stage_surge_m"]
        features = pd.concat([features, lag_df], axis=1)

        features["rain_x_saturation"] = features["rain_upstream_current"] * (features["soil_saturation_pct"] / 100.0)
        features["rain_cumulative_24h_x_saturation"] = features["rain_cumulative_24h"] * (features["soil_saturation_pct"] / 100.0)
        features["kinematic_wave_prior"] = (lag_df["runoff_lag_16h"] / 14.0) ** 1.15

        target = df["stage_surge_m"].shift(-target_horizon_steps).rename(f"target_surge_{target_horizon_steps*4}h")
        valid_idx = features.dropna().index.intersection(target.dropna().index)
        X = features.loc[valid_idx]
        y = target.loc[valid_idx]
        return X, y, list(X.columns)


        # Non-linear interaction: rain * saturation coupling
