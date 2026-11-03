"""Epistemic Humility and Safe-Failure Guardrails."""
from typing import Dict, Any
from hydropulse.config import ModelConfig

class EpistemicGuardrail:
    def __init__(self):
        self.config = ModelConfig()

    def evaluate_telemetry_safety(self, telemetry_latency_hours: float, upstream_cumulative_24h_rain_mm: float) -> Dict[str, Any]:
        is_compromised = telemetry_latency_hours > self.config.max_telemetry_latency_hours
        is_dam_spill_risk = upstream_cumulative_24h_rain_mm >= self.config.dam_spill_threshold_rainfall_mm
        safety_status = {
            "telemetry_latency_hours": telemetry_latency_hours,
            "max_allowed_latency_hours": self.config.max_telemetry_latency_hours,
            "telemetry_compromised": is_compromised,
            "dam_spill_risk": is_dam_spill_risk,
            "state": "OPERATIONAL_NOMINAL",
            "uncertainty_expansion_factor": 1.0,
            "user_banner": None,
        }
        if is_compromised:
            safety_status["state"] = "SAFE_FAILURE_STATE"
            safety_status["uncertainty_expansion_factor"] = 1.0 + self.config.safe_failure_uncertainty_expansion
            safety_status["user_banner"] = (
                "⚠️ TELEMETRY COMPROMISED: Satellite data stream latency exceeds 6 hours. "
                "Deterministic point predictions halted. Uncertainty interval widened by ±40% based on seasonal persistence."
            )
        if is_dam_spill_risk:
            dam_notice = (
                "🚨 DAM SPILLWAY ADVISORY: Extreme high-altitude rainfall (>150mm/24h) approaches "
                "upstream reservoir thresholds (Castlereigh / Maussakelle). Artificial gate releases "
                "cannot be tracked via spaceborne precipitation alone. Cross-reference Irrigation Dept sirens."
            )
            safety_status["user_banner"] = (safety_status["user_banner"] + "\n" + dam_notice) if safety_status["user_banner"] else dam_notice
        return safety_status
