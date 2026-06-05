import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

class LLMExplanationService:
    def __init__(self):
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
        self.model = init_chat_model("google_genai:gemini-2.5-flash")

    def explain(self, state):
        # BÓC TÁCH CẢ IMPACT VÀ REASON ĐỂ ÉP LLM HIỂU HƯỚNG TÁC ĐỘNG
        factors = []
        for item in state.explanation:
            feature = item.get("feature", "Unknown")
            impact = item.get("impact", 0.0)
            reason = item.get("reason", "")
            
            # Gắn nhãn rõ ràng cho LLM biết tác động là Tích cực hay Tiêu cực
            direction_text = "INCREASES risk (Bad)" if impact > 0 else "DECREASES risk (Good/Protective)"
            factors.append(f"- {feature}: {reason} -> This factor {direction_text} with an impact score of {impact}")

        prompt = f"""
            You are a public health risk analyst.

            Risk Level: {state.risk_level}
            Risk Score: {state.risk_score}
            Confidence: {state.confidence}

            Top Factors:
            {chr(10).join(factors)}

            Explain the risk in plain English.

            Requirements:
            - Maximum 100 words
            - Non-technical language
            - Accurately reflect whether a factor is increasing or decreasing the risk based on the provided direction.
            - Mention the most important drivers
            - Mention the overall risk level
            """

        response = self.model.invoke(prompt)
        return response.content