from fastapi import FastAPI
from app.api import routes, health
from app.api.errors import global_exception_handler, app_exception_handler
from src.core.exceptions import PredictionError

app = FastAPI(title="Climate Health Risk API", version="1.0")

# Đăng ký bộ xử lý lỗi toàn cục
app.add_exception_handler(PredictionError, app_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Nạp các router
app.include_router(health.router)
app.include_router(routes.router)