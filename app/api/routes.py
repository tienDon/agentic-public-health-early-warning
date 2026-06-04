from fastapi import APIRouter, HTTPException
from app.schemas import PredictRequest
from app.dependencies import get_inference_service
from src.core.exceptions import FeatureValidationError
import pandas as pd

router = APIRouter()
service = get_inference_service()

@router.get("/")
def root():
    return {
        "service": "Climate Health Risk API",
        "version": "1.0"
    }

@router.post("/predict")
def predict(request: PredictRequest):

    if not request.data:
        raise FeatureValidationError(
            "Input data dictionary cannot be empty"
        )

    df = pd.DataFrame([request.data])

    state = service.predict(df)

    if "failed" in state.status:
        raise HTTPException(
            status_code=500,
            detail=state.status
        )

    return {
        "risk_score": state.risk_score,
        "risk_level": state.risk_level,
        "confidence": state.confidence,
        "explanation": state.explanation,
        "alert_message": state.alert_message,
        "model_version": state.model_version,
        "status": state.status
    }

@router.get("/features")
def features():

    return {
        "count":
            service.predictor.get_model_info()["feature_count"],
        "features":
            service.predictor.get_required_features()
    }

@router.get("/model-info")
def model_info():

    return service.predictor.get_model_info()











