from src.models.predictor import RiskPredictor
from src.core.prediction_state import PredictionState
from src.services.alert_service import AlertService
from src.services.shap_explanation_service import ShapExplanationService
from src.services.report_service import ReportService
from src.features.feature_validator import FeatureValidator
from src.services.risk_service import RiskService
class InferenceService:

    def __init__(
            self,
        predictor,
        validator,
        shap_service,
        alert_service
    ):

        self.predictor = predictor
        self.validator = validator
        self.shap_service = shap_service
        self.alert_service = alert_service

    def predict(self, X):

        # 1. Pipeline Tiền xử lý (Validation)
        self.validator.validate(X)
        X_clean = self.predictor.reorder_features(X)
        
        # 2. Pipeline Dự báo (Prediction)
        pred_result = self.predictor.predict(X_clean)
        
        # 3. Phân loại Rủi ro & Tính Độ tin cậy (Risk Service)
        score = pred_result["score"]
        risk_level = RiskService.classify_risk(score)
        confidence = RiskService.calculate_confidence(
            pred_lgb=pred_result["pred_lgb_raw"],
            pred_xgb=pred_result["pred_xgb_raw"]
        )

        # 4. Pipeline XAI (SHAP)
        shap_insights = self.shap_service.explain_prediction(X_clean)

        state = PredictionState(
            input_data=X.to_dict("records")[0],
            risk_score=round(score, 2),
            risk_level=risk_level,
            confidence=confidence,
            model_version=self.predictor.version,
            explanation=shap_insights, 
            status="completed"
        )

        state.alert_message = self.alert_service.generate_alert(
            risk_level=state.risk_level,
            confidence=state.confidence
        )

        return state

