from pydantic import BaseModel
from typing import Dict, Any

class PredictRequest(BaseModel):
    data: Dict[str, float]

class PredictResponse(BaseModel):
    risk_score: float
    risk_level: str
    confidence: float
    explanation: list
    alert_message: str
    model_version: str