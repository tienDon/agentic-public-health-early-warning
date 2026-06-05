from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import uuid
from datetime import datetime, timezone

@dataclass
class PredictionState:

    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # INPUT
    input_data: Optional[Dict[str, Any]] = None

    # MODEL OUTPUT
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    confidence: Optional[float] = None

    # EXPLAINABILITY
    explanation: Optional[List[Dict[str, Any]]] = None

    # ALERT
    alert_message: Optional[str] = None

    # LLM LAYER
    llm_explanation: Optional[str] = None

    recommendations: Optional[List[Dict[str, str]]] = None

    # AGENT DATA
    external_context: Optional[Dict[str, Any]] = None

    # METADATA
    model_version: Optional[str] = None
    model_used: Optional[str] = None

    status: str = "created"
    prediction_time: str = field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))