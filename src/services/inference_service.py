from src.models.predictor import RiskPredictor
from src.core.prediction_state import PredictionState
from src.services.explanation_service import ExplanationService
from src.services.alert_service import AlertService
from src.services.shap_explanation_service import ShapExplanationService
from src.services.report_service import ReportService
from src.features.feature_validator import FeatureValidator

class InferenceService:

    def __init__(self):

        self.predictor = RiskPredictor(
            "artifacts/ensemble_bundle.joblib"
        )
        # self.explainer = ExplanationService()
        self.alert_service = AlertService()
        self.report_service = ReportService()
        self.shap_service = ShapExplanationService(
            model=self.predictor.lgb_model,
            feature_names=self.predictor.features
        )
        self.validator = FeatureValidator(
            expected_features=self.predictor.features,
            feature_schema=self.predictor.feature_schema
        )

    def predict(self, X):

        self.validator.validate(X)
        
        result = self.predictor.predict_with_metadata(X)
        X_clean = self.predictor.reorder_features(X)
        shap_insights = self.shap_service.explain_prediction(X_clean)

        state = PredictionState(
            input_data=X.to_dict("records")[0],
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            confidence=result["confidence"],
            model_version=result["model_version"],
            explanation=shap_insights, 
            status="completed"
        )

        state.alert_message = self.alert_service.generate_alert(
            risk_level=state.risk_level,
            confidence=state.confidence
        )

        return state

