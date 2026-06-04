from fastapi import FastAPI
import pandas as pd
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.schemas import PredictRequest
from app.dependencies import get_inference_service
from services.inference_service import InferenceService
app = FastAPI(title="Climate Health Risk API", version="1.0")

service = get_inference_service()


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "climate-risk-api"
    }


# =========================
# PREDICT ENDPOINT
# =========================
@app.post("/predict")
def predict(request: PredictRequest):

    # convert input → DataFrame
    df = pd.DataFrame([request.data])

    # call inference pipeline
    state = service.predict(df)

    # nếu lỗi
    if "failed" in state.status:
        return {
            "status": "error",
            "message": state.status
        }

    # response chuẩn
    return {
        "risk_score": state.risk_score,
        "risk_level": state.risk_level,
        "confidence": state.confidence,
        "explanation": state.explanation,
        "alert_message": state.alert_message,
        "model_version": state.model_version,
        "status": state.status
    }