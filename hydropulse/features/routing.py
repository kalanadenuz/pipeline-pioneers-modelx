"""Topological Flow Routing and Catchment Lag Engine."""
import pandas as pd
from typing import List
from hydropulse.config import CatchmentConfig

class TopologicalRouter:
    def __init__(self):
        self.config = CatchmentConfig()

    def compute_weighted_upstream_rain(self, df: pd.DataFrame) -> pd.Series:
        weights = {"rain_norton_mm": 0.30, "rain_castlereigh_mm": 0.25, "rain_kitulgala_mm": 0.25, "rain_deraniyagala_mm": 0.20}
        weighted = sum(df[col] * weight for col, weight in weights.items() if col in df.columns)
        return weighted.rename("rain_upstream_weighted_mm")

    def build_lag_features(self, df: pd.DataFrame, lags_steps: List[int] = [1, 2, 3, 4, 5, 6]) -> pd.DataFrame:
        feat_df = pd.DataFrame(index=df.index)
        for l in lags_steps:
            feat_df[f"rain_upstream_lag_{l*4}h"] = df["rain_upstream_weighted_mm"].shift(l)
            feat_df[f"runoff_lag_{l*4}h"] = df["surface_runoff_mm"].shift(l) if "surface_runoff_mm" in df.columns else 0.0
        feat_df["rain_cumulative_12h"] = df["rain_upstream_weighted_mm"].rolling(window=3).sum()
        feat_df["rain_cumulative_24h"] = df["rain_upstream_weighted_mm"].rolling(window=6).sum()
        feat_df["rain_cumulative_48h"] = df["rain_upstream_weighted_mm"].rolling(window=12).sum()
        return feat_df


    # Lag features capture hydrodynamic wave travel mechanics down river channel


    def compute_cumulative_windows(self, df):
        return df['rain_upstream_weighted_mm'].rolling(6).sum()
