class ExplanationPrompt:

    @staticmethod
    def build(state) -> str:
        factors = []
        for item in state["explanation"]:
            feature = item.get("feature", "Unknown")
            impact = item.get("impact", 0.0)
            reason = item.get("reason", "")
            
            direction_text = "INCREASES risk (Bad)" if impact > 0 else "DECREASES risk (Good/Protective)"
            factors.append(f"- {feature}: {reason} -> This factor {direction_text} with an impact score of {impact}")

        return f"""
            You are an expert public health risk analyst. Your task is to synthesize environmental and climate data into a clear, non-technical explanation for the public.

            [INPUT DATA]
            - Overall Risk Level: {state["risk_level"]}
            - Risk Score: {state["risk_score"]}
            - Confidence Level: {state["confidence"]}

            [TOP FACTORS ANALYZED]
            {chr(10).join(factors) if factors else "- No specific climate drivers detected."}

            [INSTRUCTIONS]
            - Synthesize the input data and top factors into a coherent summary.
            - Clearly mention the overall risk level and highlight the primary drivers that are increasing or decreasing the risk based on the provided direction.
            - Keep the explanation non-technical, professional, and accessible to general public health officials.
            - The explanation must be accurate, concise, and strictly under 100 words.
            
            [OUTPUT FORMAT]
            - Populate your final synthesized text directly into the 'summary' field of the requested JSON schema.
            """