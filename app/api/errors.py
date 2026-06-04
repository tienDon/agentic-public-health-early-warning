from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.core.exceptions import PredictionError, FeatureValidationError, ModelNotLoadedError

async def global_exception_handler(request: Request, exc: Exception):
    """Bắt toàn bộ các lỗi không xác định (Lỗi code bug, hệ thống...)"""
    # Bạn có thể print(exc) ở đây để debug nếu cần
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error", 
            "type": "InternalServerError",
            "message": "An unexpected error occurred on the server."
        }
    )

async def app_exception_handler(request: Request, exc: PredictionError):
    """Bắt toàn bộ các lỗi nghiệp vụ AI từ thư mục core/ vứt lên"""
    
    # Tự động phân loại mã HTTP dựa trên loại lỗi
    if isinstance(exc, FeatureValidationError):
        status_code = status.HTTP_400_BAD_REQUEST
        error_type = "ValidationError"
    elif isinstance(exc, ModelNotLoadedError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        error_type = "ModelAvailabilityError"
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_type = "PredictionError"

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "type": error_type,
            "message": exc.message
        }
    )