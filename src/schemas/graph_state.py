# src/schemas/graph_state.py
from typing import TypedDict, Optional, Dict, Any, List, Annotated
import uuid
from datetime import datetime, timezone

# Hàm reducer mặc định nếu bạn muốn ghi đè dữ liệu (Overwrite)
# Hoặc bạn có thể dùng operator.add để cộng dồn List
def merge_dict(old: Optional[Dict], new: Optional[Dict]) -> Optional[Dict]:
    if old is None: return new
    if new is None: return old
    return {**old, **new}

class PredictionState(TypedDict, total=False):

    request_id: str

    request_time: str
    prediction_time: str

    input_data: Dict[str, Any]

    risk_score: float
    risk_level: str
    confidence: float

    explanation: List[Dict[str, Any]]

    alert_message: str

    llm_explanation: str
    recommendations: List[Dict[str, Any]]

    external_context: Dict[str, Any]

    model_version: str
    model_used: str

    status: str
    error: Optional[str]

    agent_trace: List[str]

    current_node: Optional[str]

    graph_version: str

def create_initial_state(
    input_data: Optional[Dict[str, Any]] = None
) -> PredictionState:

    now = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    return {
        "request_id": str(uuid.uuid4()),

        "request_time": now,
        "prediction_time": None,

        "input_data": input_data,

        "risk_score": None,
        "risk_level": None,
        "confidence": None,

        "explanation": [],
        "recommendations": [],

        "alert_message": None,
        "llm_explanation": None,

        "external_context": {},

        "model_version": None,
        "model_used": None,

        "status": "created",
        "error": None,

        "agent_trace": [],

        "current_node": "start",
        "graph_version": "1.0"
    }

