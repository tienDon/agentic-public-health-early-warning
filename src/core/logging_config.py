# src/core/logging_config.py
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    # 1. Định nghĩa các thuộc tính chuẩn của Python Logger muốn chuyển sang JSON
    # Bạn có thể thêm các trường tùy biến tùy theo nhu cầu hệ thống
    log_fields = (
        "asctime",
        "levelname",
        "name",
        "filename",
        "lineno",
        "message",
        "exc_info"
    )
    
    # Tạo chuỗi định dạng cho json-logger hiểu
    formatter_str = " ".join([f"%({field})s" for field in log_fields])
    
    # 2. Khởi tạo JsonFormatter
    json_formatter = jsonlogger.JsonFormatter(formatter_str)
    
    # 3. Cấu hình StreamHandler để đẩy log ra stdout (màn hình console/Docker log)
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(json_formatter)
    
    # 4. Cấu hình Root Logger của toàn bộ ứng dụng
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # Ghi nhận log từ mức INFO trở lên
    
    # Xóa các handler cũ nếu có để tránh bị lặp log (bảo vệ khi reload code)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    root_logger.addHandler(log_handler)
    
    # 5. Ép các log hệ thống của Uvicorn/FastAPI đi qua cấu hình JSON này
    # Điều này đảm bảo log request từ client cũng biến thành JSON
    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"):
        libs_logger = logging.getLogger(logger_name)
        libs_logger.handlers = [log_handler]
        libs_logger.propagate = False