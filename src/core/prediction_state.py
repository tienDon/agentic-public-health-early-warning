from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class PredictionState:

    input_data: Optional[Dict[str, Any]] = None

    risk_score: Optional[float] = None

    risk_level: Optional[str] = None

    confidence: Optional[float] = None

    model_version: Optional[str] = None

    explanation: Optional[List[Dict[str, Any]]] = None

    alert_message: Optional[str] = None

    # shap_service: Optional[Dict[str, Any]] = None

    status: str = "created"