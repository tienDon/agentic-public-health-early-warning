from typing import Optional, List

class AlertService:
    def generate_alert(self, risk_level: str, confidence: float) -> Optional[str]:
        alerts: List[str] = []

        if risk_level == "LOW":
            alerts.append("No immediate outbreak risk detected.")
        elif risk_level == "MEDIUM":
            alerts.append("Moderate outbreak risk detected. Increased surveillance recommended.")
        elif risk_level == "HIGH":
            alerts.append("High outbreak risk detected. Immediate monitoring recommended.")
        else:
            alerts.append("Unknown risk level detected.")

        if confidence < 0.5:
            alerts.append("Prediction confidence is low. Manual review recommended.")

        return " ".join(alerts) if alerts else "No alert messages."