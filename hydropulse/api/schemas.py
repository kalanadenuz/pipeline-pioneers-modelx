"""FastAPI Schemas."""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Tuple, Any

class TelemetryIngestRequest(BaseModel):
    basin: str = Field(default="Kelani")
    rain_upstream_weighted_mm: float
    soil_saturation_pct: float
    current_hanwella_stage_m: float
    telemetry_latency_hours: float = 2.5
    upstream_cumulative_24h_rain_mm: float = 85.0

class ForecastResponse(BaseModel):
    status: str
    target_location: str
    lead_time_hours: float
    point_predicted_surge_m: float
    conformal_bounds_90pct_m: Tuple[float, float]
    estimated_plot_inundation_m: float
    plot_inundation_bounds_m: Tuple[float, float]
    upstream_soil_saturation_pct: float
    telemetry_latency_hours: float
    safe_failure_triggered: bool
    safety_message: Optional[str]

class AlertResponse(BaseModel):
    alert_level: str
    urgency: str
    arrival_window: str
    action_deadline: str
    plain_text_sms: str
    action_checklist: List[str]
    safety_status: Dict[str, Any]
