from fastapi import APIRouter, HTTPException
from app.schemas import PredictRequest, PredictResponse, BatchPredictRequest, BatchPredictResponse, BatchPredictItem, ModelInfoResponse
from app.dependencies import get_inference_service
from src.core.exceptions import FeatureValidationError, PredictionError
import pandas as pd
from fastapi import Depends

router = APIRouter()

@router.get("/")
def root():
    return {
        "service": "Climate Health Risk API",
        "version": "1.0"
    }

@router.post("/predict")
def predict(request: PredictRequest, service = Depends(get_inference_service)):

    if not request.data:
        raise FeatureValidationError(
            "Input data dictionary cannot be empty"
        )
    
    df = pd.DataFrame([request.data])

    state = service.predict(df)

    if "failed" in state.status:
        raise PredictionError(state.status)

    return PredictResponse(
        request_id=state.request_id,
        risk_score=state.risk_score,
        risk_level=state.risk_level,
        confidence=state.confidence,
        explanation=state.explanation,
        alert_message=state.alert_message,
        llm_explanation=state.llm_explanation,
        recommendations=state.recommendations,
        model_version=state.model_version,
        model_used=state.model_used,
        status=state.status,
        prediction_time=state.prediction_time,
    )

@router.get("/features")
def features(service = Depends(get_inference_service)):
    return {
        "count":
            service.predictor.get_model_info()["feature_count"],
        "features":
            service.predictor.get_required_features()
    }

@router.get("/model-info", response_model=ModelInfoResponse)
def model_info(service = Depends(get_inference_service)):
    return service.predictor.get_model_info()


@router.post("/predict/batch", response_model=BatchPredictResponse)
def predict_batch(request: BatchPredictRequest, service = Depends(get_inference_service)):
    if not request.data:
        raise FeatureValidationError(
            "Input batch cannot be empty"
        )

    df = pd.DataFrame(request.data)

    states = service.predict_batch(df)

    return BatchPredictResponse(
        status="completed",
        count=len(states),
        results=[
            BatchPredictItem(
                risk_score=s.risk_score,
                risk_level=s.risk_level,
                confidence=s.confidence,
                alert=s.alert_message
            )
            for s in states
        ]
    )


















