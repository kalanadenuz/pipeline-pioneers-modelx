"""Automated Data Preprocessor and Quality Assurance Engine."""
import pandas as pd
from typing import Dict, Any, Tuple
from hydropulse.config import CatchmentConfig, ModelConfig

class DataPreprocessor:
    def __init__(self):
        self.catchment = CatchmentConfig()
        self.model_cfg = ModelConfig()

    def clip_catchment_bounds(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.copy()

    def clean_and_impute(self, df: pd.DataFrame, telemetry_latency_hours: float = 2.0) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        cleaned = df.copy()
        qa_report = {
            "telemetry_latency_hours": telemetry_latency_hours,
            "latency_acceptable": telemetry_latency_hours <= self.model_cfg.max_telemetry_latency_hours,
            "missing_values_imputed": 0,
            "status": "VALID",
        }
        if telemetry_latency_hours > self.model_cfg.max_telemetry_latency_hours:
            qa_report["status"] = "TELEMETRY_COMPROMISED"
            qa_report["action"] = "HALT_DETERMINISTIC_PREDICTION"
            return cleaned, qa_report

        missing_count = cleaned.isna().sum().sum()
        if missing_count > 0:
            cleaned = cleaned.ffill().bfill()
            qa_report["missing_values_imputed"] = int(missing_count)

        return cleaned, qa_report

    def verify_physical_conservation(self, df: pd.DataFrame) -> bool:
        total_precip = df["rain_upstream_weighted_mm"].sum()
        total_runoff = df["surface_runoff_mm"].sum()
        return total_runoff <= (total_precip * 1.05)
