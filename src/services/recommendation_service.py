import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

class RecommendationService:
    
    def __init__(self):
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
        self.model = init_chat_model("google_genai:gemini-2.5-flash")

    def _get_fallback_recommendations(self, risk_level: str):
        """Hàm dự phòng cấu trúc chuẩn JSON phục vụ Dashboard khi LLM sập mạng"""
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

    def recommend(self, state):
        try:
            bad_drivers = []
            for item in state.explanation:
                if item.get("impact", 0) > 0:
                    bad_drivers.append(f"- {item.get('feature')}: {item.get('reason')}")

            if not bad_drivers and state.risk_level == "LOW":
                return self._get_fallback_recommendations(state.risk_level)

            prompt = f"""
                You are an expert Public Health Action & Recommendation Agent.
                Your task is to provide exactly 2 to 3 highly actionable public health recommendations based on the current climate risk assessment.

                Current Risk Level: {state.risk_level}
                Current Risk Score: {state.risk_score}

                Top Climate/Environmental Drivers Increasing the Risk:
                {chr(10).join(bad_drivers) if bad_drivers else "- Baseline environmental conditions."}

                Instructions for Format:
                - Output ONLY a plain text list where each recommendation is on a new line starting with a hyphen (-) using this exact format: - PRIORITY: ACTION
                - PRIORITY must be exactly one of these words: HIGH, MEDIUM, or LOW based on how urgent that specific action is.
                - Action should be direct, actionable, tailored to the drivers and under 15 words.
                - Example: - HIGH: Activate public cooling centers immediately.
                - Example: - MEDIUM: Distribute educational material on hydration.
                - Strictly no conversational filler, no markdown code blocks.
                """

            response = self.model.invoke(prompt)
            
            lines = response.content.strip().split('\n')
            recommendations = []
            for line in lines:
                line = line.strip()
                if line.startswith('-'):
                    content = line.lstrip('- ').strip()
                    if ':' in content:
                        priority, action = content.split(':', 1)
                        priority_clean = priority.strip().upper()
                        action_clean = action.strip()
                        
                        # Validate đầu ra của AI trước khi nạp vào hệ thống
                        if priority_clean in ["HIGH", "MEDIUM", "LOW"] and action_clean:
                            recommendations.append({
                                "priority": priority_clean,
                                "action": action_clean
                            })
            
            if not recommendations:
                return self._get_fallback_recommendations(state.risk_level)
                
            return recommendations

        except Exception as e:
            print(f"[Warning] Recommendation Agent Error: {e}. Using fallback.")
            return self._get_fallback_recommendations(state.risk_level)