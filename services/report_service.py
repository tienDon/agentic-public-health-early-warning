class ReportService:
    def generate(self, state):
        insights = state.explanation or []
        
        return {
            "summary": {
                "risk_level": state.risk_level,
                "risk_score": round(state.risk_score, 2),
                "confidence": f"{state.confidence * 100:.1f}%" if state.confidence else "0.0%"
            },
            # Map trực tiếp qua schema phẳng một cách an toàn
            "insights": [
                {
                    "feature": e["feature"],
                    "impact": e["impact"],
                    "reason": e["reason"]
                }
                for e in insights
            ],
            "alert": state.alert_message,
            "status": state.status
        }