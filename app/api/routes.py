# app/api/routes.py
from fastapi import APIRouter, HTTPException
from app.schemas import PredictRequest, PredictResponse, BatchPredictRequest, BatchPredictResponse, BatchPredictItem, ModelInfoResponse
from app.dependencies import get_inference_service
from src.core.exceptions import FeatureValidationError, PredictionError
import pandas as pd
from fastapi import Depends
from src.services.graph_inference_service import GraphInferenceService
from app.dependencies import get_graph_service
router = APIRouter()

@router.get("/")
def root():
    return {
        "service": "Climate Health Risk API",
        "version": "1.0",
        "engine": "LangGraph"
    }

@router.post("/predict")
def predict(request: PredictRequest, service: GraphInferenceService = Depends(get_graph_service)):

    if not request.data:
        raise FeatureValidationError(
            "Input data dictionary cannot be empty"
        )
    
    # df = pd.DataFrame([request.data])

    # state = service.predict(df)

    state_dict = service.predict(request.data)

    # if "failed" in state.status:
    #     raise PredictionError(state.status)

    current_status = state_dict.get("status", "failed")
    if current_status.endswith("failed"):
        raise PredictionError(current_status)

    return PredictResponse(
        request_id=state_dict.get("request_id"),
        risk_score=state_dict.get("risk_score"),
        risk_level=state_dict.get("risk_level"),
        confidence=state_dict.get("confidence"),
        explanation=state_dict.get("explanation"),
        alert_message=state_dict.get("alert_message"),
        llm_explanation=state_dict.get("llm_explanation"),
        recommendations=state_dict.get("recommendations"),
        model_version=state_dict.get("model_version"),
        model_used=state_dict.get("model_used"),
        status=state_dict.get("status"),
        prediction_time=state_dict.get("prediction_time"),
    )

@router.get("/features")
def features(service: GraphInferenceService = Depends(get_graph_service)):
    # Lấy trực tiếp từ thuộc tính self.predictor cực kỳ an toàn
    predictor = service.predictor 
    return {
        "count": predictor.get_model_info()["feature_count"],
        "features": predictor.get_required_features()
    }

@router.get("/model-info", response_model=ModelInfoResponse)
def model_info(service: GraphInferenceService = Depends(get_graph_service)):
    return service.predictor.get_model_info()


@router.post("/predict/batch", response_model=BatchPredictResponse)
async def predict_batch(request: BatchPredictRequest, service: GraphInferenceService = Depends(get_graph_service)):
    if not request.data:
        raise FeatureValidationError(
            "Input batch cannot be empty"
        )

    # df = pd.DataFrame(request.data)

    # states = service.predict_batch(df)

    raw_batch_list = request.data
    states = await service.predict_batch(raw_batch_list)

    formatted_results = []
    for s in states:
        # 4. Bảo vệ mảng recommendations an toàn tuyệt đối tránh gãy chuỗi dữ liệu rỗng
        recommendations = s.get("recommendations") or []
        top_recommendation = (
            recommendations[0]["action"] if recommendations and "action" in recommendations[0]
            else "No immediate action required."
        )
        
        formatted_results.append(
            BatchPredictItem(
                risk_score=s.get("risk_score"),
                risk_level=s.get("risk_level"),
                confidence=s.get("confidence"),
                alert=s.get("alert_message"),
                ai_summary=s.get("llm_explanation"),  # Nếu schema cũ của bạn là ai_summary
                top_recommendation=top_recommendation
            )
        )

    return BatchPredictResponse(
        status="completed",
        count=len(states),
        results=formatted_results
    )
    


















