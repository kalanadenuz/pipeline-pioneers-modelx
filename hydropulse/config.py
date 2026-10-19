"""Configuration settings for Kelani Basin."""
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class CatchmentConfig:
    basin_name: str = "Kelani River Basin"
    bounding_box: Tuple[float, float, float, float] = (6.70, 7.25, 79.85, 80.60)
    total_area_km2: float = 2292.0


@dataclass(frozen=True)
class AlertConfig:
    low_lying_warning_surge_m: float = 0.50


    sub_catchments = {
        "Norton_Bridge_Upper": {"elevation_m": 1250.0, "lag_hours": 24.0, "weight": 0.22},
        "Castlereigh_Catchment": {"elevation_m": 1100.0, "lag_hours": 22.0, "weight": 0.20},
        "Kitulgala_Mid": {"elevation_m": 420.0, "lag_hours": 16.0, "weight": 0.25},
        "Deraniyagala_Seethawaka": {"elevation_m": 350.0, "lag_hours": 14.0, "weight": 0.18},
        "Hanwella_Lower_Floodplain": {"elevation_m": 12.0, "lag_hours": 0.0, "weight": 0.15},
    }


@dataclass(frozen=True)
class PhysicsConfig:
    asmi_decay_factor: float = 0.90
    soil_saturation_threshold_mm: float = 180.0
    runoff_coefficient_dry: float = 0.25
    runoff_coefficient_saturated: float = 0.92


    # Downstream staff gauge baseline datums
    hanwella_baseflow_datum_m: float = 1.80


@dataclass(frozen=True)
class ModelConfig:
    forecast_horizons_hours: Tuple[int, ...] = (14, 18, 20, 24)
    target_lead_time_hours: int = 18
    conformal_coverage: float = 0.90
    significance_level_alpha: float = 0.10
    max_telemetry_latency_hours: float = 6.0
    safe_failure_uncertainty_expansion: float = 0.40
    dam_spill_threshold_rainfall_mm: float = 150.0
