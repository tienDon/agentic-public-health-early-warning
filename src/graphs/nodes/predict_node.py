import logging
from src.services.risk_service import RiskService
from src.schemas.graph_state import PredictionState
import pandas as pd
from datetime import datetime
logger = logging.getLogger(__name__)

class PredictNode:
    def __init__(self, predictor, validator):
        self.predictor = predictor
        self.validator = validator

    def __call__(self, state: PredictionState) -> dict:
        logger.info(f"Kích hoạt PredictNode cho Request: {state.get('request_id')}")
        try:
            raw_dict = state["input_data"]

            df = pd.DataFrame([raw_dict])

            self.validator.validate(df)

            # X_clean = self.predictor.reorder_features(df)

            pred_result = self.predictor.predict(df)
            score = pred_result["score"]
            
            current_time_iso = datetime.utcnow().isoformat() + "Z"

            # 3. Chỉ trả về những trường thay đổi để LangGraph cập nhật State
            return {
                "risk_score": round(score, 2),
                "risk_level": RiskService.classify_risk(score),
                "confidence": RiskService.calculate_confidence(
                    pred_result["pred_lgb_raw"],
                    pred_result["pred_xgb_raw"]
                ),
                "model_version": self.predictor.model_version,
                "model_used": pred_result["model_used"],
                "prediction_time": current_time_iso,
                "status": "predicted"
            }
        except Exception as e:
            logger.error("Lỗi xảy ra tại PredictNode", exc_info=True)
            return {
                "status": "failed",
                "error": str(e)
            }