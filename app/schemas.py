# app/schemas.py
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from src.schemas.recommendation_schema import RecommendationItem
from src.schemas.explanation_schema import ExplanationItem
class PredictRequest(BaseModel):
    data: Dict[str, float]

class PredictResponse(BaseModel):
    request_id: str
    risk_score: float
    risk_level: str
    confidence: float
    explanation: Optional[List[ExplanationItem]] = None
    alert_message: str
    llm_explanation: Optional[str] = None
    recommendations: Optional[List[RecommendationItem]] = None
    model_version: str
    model_used: str
    prediction_time: Optional[str] = None

class BatchPredictRequest(BaseModel):
    data: List[Dict[str, float]]

class BatchPredictItem(BaseModel):
    risk_score: float
    risk_level: str
    confidence: float
    alert: str
    llm_explanation: Optional[str] = None          # Trích từ state["llm_explanation"]
    top_recommendation: Optional[str] = None


class BatchPredictResponse(BaseModel):
    status: str
    count: int
    results: list[BatchPredictItem]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_version: str
    feature_count: int

class ModelInfoResponse(BaseModel):
    version: str
    target: str | None
    feature_count: int
    ensemble: bool







