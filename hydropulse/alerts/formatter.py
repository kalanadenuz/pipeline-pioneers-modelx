"""Operational Alert Formatter."""
from typing import Dict, Any
import json

class AlertFormatter:
    @staticmethod
    def format_sms_alert(alert_data: Dict[str, Any]) -> str:
        level = alert_data["alert_level"]
        loc = alert_data["target_location"]
        arrival = alert_data["arrival_window"]
        inundation = alert_data["estimated_plot_inundation_m"]
        low, high = alert_data["plot_inundation_bounds_m"]
        sat = alert_data["upstream_saturation_pct"]
        deadline = alert_data["action_deadline"]
        checklist = alert_data["action_checklist"]

        lines = [
            "🚨 *CRITICAL FLOOD WARNING (Hanwella / Biyagama)*",
            "අවවාදයයි: හංවැල්ල/බියගම පහත් බිම්වල හදිසි ගංවතුර අනතුරක්.",
            "",
            f"• *Expected Arrival:* {arrival}",
            f"• *Predicted Peak Water Level:* {inundation:.2f}m (90% Conf: {low:.2f}m – {high:.2f}m)",
            f"• *Root Cause:* Upstream soil saturation at {sat}% with extreme mountain rainfall.",
            "",
            f"⚠️ *REQUIRED ACTIONS ({deadline}):*",
        ]
        for i, item in enumerate(checklist, 1):
            lines.append(f"{i}. {item}")

        safety = alert_data.get("safety_status", {})
        if safety.get("user_banner"):
            lines.append("")
            lines.append(safety["user_banner"])

        return "\n".join(lines)

    @staticmethod
    def format_json_webhook(alert_data: Dict[str, Any]) -> str:
        return json.dumps(alert_data, indent=2)
