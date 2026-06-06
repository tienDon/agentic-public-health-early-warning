import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from src.agents.base_agent import BaseAgent
from src.prompts.recommendation_prompt import RecommendationPrompt
from src.parsers.recommendation_parser import RecommendationParser
from src.agents.base_llm_agent import BaseLLMAgent
from src.schemas.recommendation_schema import RecommendationResponse, RecommendationItem
import logging
load_dotenv()
logger = logging.getLogger(__name__)
class RecommendationAgent(BaseLLMAgent):

    def __init__(self):
        super().__init__()
        self.structured_model = self.model.with_structured_output(RecommendationResponse)

    def _get_fallback_recommendations(self, risk_level: str) -> list[dict]:
        """
        Trả về dữ liệu fallback cố định dưới dạng list[dict] 
        để đồng nhất với cấu trúc sau khi model_dump().
        """
        if risk_level == "LOW":
            return [{"priority": "LOW", "action": "Continue routine monitoring"}]
        elif risk_level == "MEDIUM":
            return [    
                {"priority": "HIGH", "action": "Increase disease surveillance"}, 
                {"priority": "MEDIUM", "action": "Review hospital readiness"}
            ]
        else: # HIGH
            return [
                {"priority": "HIGH", "action": "Activate emergency monitoring"}, 
                {"priority": "HIGH", "action": "Prepare healthcare resources"},
                {"priority": "MEDIUM", "action": "Issue public health advisory"}
            ]

    def run(self, state):
        try:
            # Kiểm tra nhanh điều kiện tối ưu token (Early return với fallback tĩnh)
            bad_drivers = [item for item in state["explanation"] if item.get("impact", 0) > 0]
            if not bad_drivers and state["risk_level"] == "LOW":
                state["recommendations"] = self._get_fallback_recommendations(state["risk_level"])
                return state

            # 1. Gọi Prompt Builder tách biệt
            prompt = RecommendationPrompt.build(state)

            # 2. Invoke qua structured_model -> Trả về thẳng RecommendationResponse object
            response: RecommendationResponse = self.structured_model.invoke(prompt)
            
            # 3. Cập nhật State trực tiếp bằng cách dump data từ object sang dict
            if response and response.recommendations:
                state["recommendations"] = response.model_dump()["recommendations"]
            else:
                # Log cảnh báo nếu LLM trả về rỗng một cách bất thường trước khi dùng fallback
                logger.warning("Recommendation Agent received empty response from LLM. Using fallback.")
                state["recommendations"] = self._get_fallback_recommendations(state["risk_level"])

        except Exception as e:
            logger.error(f"[Error] Recommendation Agent Error: {e}. Using fallback.")
            state["recommendations"] = self._get_fallback_recommendations(state["risk_level"])

        # 4. Luôn trả về State object
        return state