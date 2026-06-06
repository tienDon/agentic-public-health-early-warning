import logging
from src.schemas.graph_state import PredictionState

logger = logging.getLogger(__name__)

class RecommendationNode:
    def __init__(self, agent):
        self.agent = agent

    def __call__(self, state: PredictionState) -> dict:
        if state.get("status") == "failed":
            return {}

        logger.info("Kích hoạt RecommendationNode gọi LLM sinh khuyến nghị y tế.")
        updated_state = self.agent.run(state)
        
        return {
            "recommendations": updated_state.get("recommendations"),
            "status": "prediction_completed"  # Đánh dấu Graph hoàn thành trọn vẹn
        }