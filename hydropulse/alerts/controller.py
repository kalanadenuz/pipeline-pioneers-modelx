"""Operational Alert Controller."""
from datetime import datetime, timedelta
from typing import Dict, Any
from hydropulse.config import AlertConfig, CatchmentConfig

class AlertController:
    def __init__(self):
        self.config = AlertConfig()
        self.catchment = CatchmentConfig()

    def evaluate_alert(self, predicted_surge_m: float, conformal_low_m: float, conformal_high_m: float, soil_saturation_pct: float, lead_time_hours: float = 16.0, current_time: datetime = None, safety_status: Dict[str, Any] = None) -> Dict[str, Any]:
        if current_time is None:
            current_time = datetime.now()
        arrival_start = current_time + timedelta(hours=lead_time_hours - 1.0)
        arrival_end = current_time + timedelta(hours=lead_time_hours + 1.0)
        action_deadline = arrival_start - timedelta(hours=self.config.lead_time_buffer_hours)

        inundation_depth = max(0.0, predicted_surge_m - 0.45)
        inundation_low = max(0.0, conformal_low_m - 0.45)
        inundation_high = max(0.0, conformal_high_m - 0.45)

        if predicted_surge_m >= self.config.alert_major_flood_surge_m:
            alert_level = "CRITICAL_MAJOR_FLOOD"
            urgency = "HIGH"
        elif predicted_surge_m >= self.config.low_lying_warning_surge_m:
            alert_level = "HIGH_RISK_INUNDATION"
            urgency = "HIGH"
        elif predicted_surge_m >= 0.30:
            alert_level = "ADVISORY_MONITORING"
            urgency = "MEDIUM"
        else:
            alert_level = "NORMAL_BASEFLOW"
            urgency = "LOW"

        checklist = []
        if alert_level in ["HIGH_RISK_INUNDATION", "CRITICAL_MAJOR_FLOOD"]:
            checklist = [
                "Dismantle and elevate field electric water pumps to high scaffolding",
                "Move two-wheel tractors and tillers to elevated road embankments",
                "Relocate bagged fertilizer, seed reserves, and harvested grain to dry storage sheds",
                "Clear perimeter drainage trenches and block lower farm plot canal ingress points",
            ]
        elif alert_level == "ADVISORY_MONITORING":
            checklist = [
                "Monitor upstream mountain rainfall updates",
                "Prepare pump uncoupling wrenches and equipment transport paths",
            ]
        else:
            checklist = ["Normal operations; soil moisture within seasonal absorption capacity"]

        return {
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "alert_level": alert_level,
            "urgency": urgency,
            "target_location": "Kelani Basin: Hanwella / Biyagama Lower Floodplain",
            "upstream_saturation_pct": round(soil_saturation_pct, 1),
            "predicted_surge_m": round(predicted_surge_m, 2),
            "conformal_bounds_m": (round(conformal_low_m, 2), round(conformal_high_m, 2)),
            "estimated_plot_inundation_m": round(inundation_depth, 2),
            "plot_inundation_bounds_m": (round(inundation_low, 2), round(inundation_high, 2)),
            "lead_time_hours": lead_time_hours,
            "arrival_window": f"{arrival_start.strftime('%I:%M %p')} – {arrival_end.strftime('%I:%M %p')} tomorrow",
            "action_deadline": f"Before {action_deadline.strftime('%I:%M %p')}",
            "action_checklist": checklist,
            "safety_status": safety_status or {},
        }


        # Buffer: 3.5 hours for farmers to uncouple pumps and move tractors
