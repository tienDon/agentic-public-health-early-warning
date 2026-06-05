from src.services.llm_explanation_service import LLMService


class ExplanationAgent:

    def __init__(self):

        self.llm = LLMService()

    def run(self, state):

        factors = []

        for item in state.explanation:

            factors.append(
                f"- {item['reason']}"
            )

        prompt = f"""
You are a public health analyst.

Risk Level:
{state.risk_level}

Risk Score:
{state.risk_score}

Key Factors:
{chr(10).join(factors)}

Explain the outbreak risk in plain English.
Keep it under 100 words.
"""

        state.llm_explanation = (
            self.llm.generate(prompt)
        )

        return state