import logging
from src.schemas.graph_state import PredictionState

logger = logging.getLogger(__name__)

class ExplanationNode:
    def __init__(self, agent):
        self.agent = agent

    def __call__(self, state: PredictionState) -> dict:
        if state.get("status") == "failed":
            return {}

        logger.info("Kích hoạt ExplanationNode gọi LLM sinh tóm tắt phân tích.")
        # Chạy Agent và nhận lại State mới (Agent đã tự bắt try-except và ghi log)
        updated_state = self.agent.run(state)
        
        # Trả về các trường mà Agent đã cập nhật vào state
        return {
            "llm_explanation": updated_state.get("llm_explanation"),
        }