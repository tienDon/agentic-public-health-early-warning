# src/services/risk_service.py
from src.core.risk_levels import RiskLevel

class RiskService:
    @staticmethod
    def classify_risk(score: float) -> str:
        if score < 30: return RiskLevel.LOW
        elif score < 60: return RiskLevel.MEDIUM
        return RiskLevel.HIGH

    @staticmethod
    def calculate_confidence(pred_lgb: float, pred_xgb: float = None) -> float:
        if pred_xgb is None: 
            return 1.0
        # Tính chênh lệch giữa 2 mô hình (Ensemble disagreement)
        diff = abs(pred_lgb - pred_xgb)
        return round(float(max(0, 1 - (diff / 100))), 3)