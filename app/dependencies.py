# app/dependencies.py
from src.models.predictor import RiskPredictor
from src.features.feature_validator import FeatureValidator
from src.services.alert_service import AlertService
from src.services.shap_explanation_service import ShapExplanationService
from src.services.inference_service import InferenceService
from src.services.graph_inference_service import GraphInferenceService
_graph_service = GraphInferenceService()

def get_graph_service() -> GraphInferenceService:
    """Dependency Provider duy nhất cung cấp Graph Service cho toàn bộ Route API"""
    return _graph_service

def get_inference_service():

    predictor = RiskPredictor(
        "artifacts/ensemble_bundle.joblib"
    )

    validator = FeatureValidator(
        expected_features=predictor.features,
        feature_schema=predictor.feature_schema
    )

    shap_service = ShapExplanationService(
        model=predictor.get_primary_model(),
        feature_names=predictor.features
    )

    alert_service = AlertService()

    return InferenceService(
        predictor=predictor,
        validator=validator,
        shap_service=shap_service,
        alert_service=alert_service
    )
