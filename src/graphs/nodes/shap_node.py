# src/graphs/nodes/shap_node.py
import logging
import pandas as pd
from src.schemas.graph_state import PredictionState

logger = logging.getLogger(__name__)

class ShapNode:
    def __init__(self, shap_service, predictor):
        """
        Dependency Injection: Nhận cả shap_service và predictor 
        để tái sử dụng logic căn chỉnh cột dữ liệu.
        """
        self.shap_service = shap_service
        self.predictor = predictor

    def __call__(self, state: PredictionState) -> dict:
        # Nếu node trước đó (PredictNode) thất bại, không chạy tiếp
        if state.get("status") == "failed":
            return {}
            
        logger.info("Kích hoạt ShapNode tính toán giải thích mô hình (XAI).")
        try:
            # 1. Chuyển đổi dữ liệu từ Graph State (dict) thành DataFrame 1 dòng
            raw_dict = state["input_data"]
            df_raw = pd.DataFrame([raw_dict])
            
            # 2. SỬA LỖI TIỀM ẨN: Ép đúng thứ tự cột mà Model yêu cầu
            df_clean = self.predictor.reorder_features(df_raw)
            
            # 3. Gọi Service tính toán raw SHAP và định dạng danh sách
            shap_insights = self.shap_service.explain_prediction(df_clean)
            
            # 4. BỔ SUNG LOGIC CŨ: Bổ sung trường 'rank' cho từng nhân tố tác động
            for idx, item in enumerate(shap_insights):
                item["rank"] = idx + 1
            
            # 5. Trả về kết quả để LangGraph tự động cập nhật State
            return {
                "explanation": shap_insights,
            }
            
        except Exception as e:
            logger.warning(
                "Không thể tính toán SHAP values do lệch cấu trúc dữ liệu hoặc lỗi thư viện. "
                "Bỏ qua bước giải thích chi tiết.", 
                exc_info=True
            )
            # Trả về mảng trống để Node LLM phía sau biết đường xử lý fallback
            return {
                "explanation": [],
            }