import os
from dotenv import load_dotenv
from src.agents.base_llm_agent import BaseLLMAgent
from src.prompts.explanation_prompt import ExplanationPrompt    
from src.schemas.explanation_schema import ExplanationResponse
import logging
load_dotenv()
logger = logging.getLogger(__name__)

class ExplanationAgent(BaseLLMAgent):

    def __init__(self):
        super().__init__()
        # Ép cấu trúc model ngay từ khi khởi tạo Agent
        self.structured_model = self.model.with_structured_output(ExplanationResponse)

    def run(self, state):
        try:
            # 1. Gọi Prompt Builder tách biệt
            prompt = ExplanationPrompt.build(state)
            
            # 2. Invoke qua structured_model (ĐÃ SỬA: Thay vì gọi self.model thô)
            response: ExplanationResponse = self.structured_model.invoke(prompt)
            
            # 3. Cập nhật State trực tiếp từ thuộc tính của Pydantic Object
            if response and response.summary:
                state["llm_explanation"] = response.summary
            else:
                logger.warning("Explanation Agent received empty summary from LLM.")
                state["llm_explanation"] = "No explanation summary provided by AI."
                
        except Exception as e:
            # ĐỒNG NHẤT: Tránh làm sập luồng LangGraph, gán fallback khi có lỗi
            logger.error(f"[Error] Explanation Agent Error: {e}")
            state["llm_explanation"] = "Unable to generate AI explanation due to an error."
            
        # 4. Luôn trả về State object đúng chuẩn LangGraph
        return state