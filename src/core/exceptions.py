class PredictionError(Exception):
    """Lớp ngoại lệ cơ sở cho phần lõi AI"""
    def __init__(self, message: str = "Prediction failed"):
        self.message = message
        super().__init__(self.message)

class FeatureValidationError(PredictionError):
    """Lỗi khi dữ liệu đầu vào không đúng định dạng mong muốn"""
    pass

class ModelNotLoadedError(PredictionError):
    """Lỗi khi file mô hình (.joblib/.pkl) chưa được nạp thành công"""
    pass