from fastapi import APIRouter
from app.dependencies import get_inference_service

router = APIRouter()

@router.get("/health")
def health():

    service = get_inference_service()

    return {
        "status": "healthy",
        "model_loaded": True,
        "model_version":
            service.predictor.version,
        "feature_count":
            len(service.predictor.features)
    }