"""Configuration settings for Kelani Basin."""
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class CatchmentConfig:
    basin_name: str = "Kelani River Basin"
    bounding_box: Tuple[float, float, float, float] = (6.70, 7.25, 79.85, 80.60)
    total_area_km2: float = 2292.0
