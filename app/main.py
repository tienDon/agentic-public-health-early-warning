# main.py
import logging
from fastapi import FastAPI
from app.api import routes, health
from app.api.errors import global_exception_handler, app_exception_handler
from src.core.exceptions import PredictionError
from src.core.logging_config import setup_logging  # Import cấu hình JSON logger

# 1. Kích hoạt cấu hình JSON Logging ngay từ đầu
setup_logging()
logger = logging.getLogger(__name__)

# 2. Khởi tạo FastAPI app
app = FastAPI(title="Climate Health Risk API", version="1.0")

# Đăng ký bộ xử lý lỗi toàn cục
app.add_exception_handler(PredictionError, app_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Nạp các router
app.include_router(health.router)
app.include_router(routes.router)

# 3. Log thông báo hệ thống đã sẵn sàng bằng JSON định dạng
@app.on_event("startup")
async def on_startup():
    logger.info("Climate Health Risk API has been successfully started.")