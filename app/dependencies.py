from src.models.predictor import RiskPredictor
from src.features.feature_validator import FeatureValidator
from src.services.alert_service import AlertService
from src.services.shap_explanation_service import ShapExplanationService
from src.services.inference_service import InferenceService


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