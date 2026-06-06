class RecommendationPrompt:

    @staticmethod
    def build(state) -> str:
        bad_drivers = []
        for item in state["explanation"]:
            if item.get("impact", 0) > 0:
                bad_drivers.append(f"- {item.get('feature')}: {item.get('reason')}")

        return f"""
            You are an expert Public Health Action & Recommendation Agent.
            Your task is to provide exactly 2 to 3 highly actionable public health recommendations based on the current climate risk assessment.

            Current Risk Level: {state["risk_level"]}
            Current Risk Score: {state["risk_score"]}

            Top Climate/Environmental Drivers Increasing the Risk:
            {chr(10).join(bad_drivers) if bad_drivers else "- Baseline environmental conditions."}

            Instructions:
            - Generate 2 to 3 recommendations tailored to the drivers above.
            - Ensure actions are direct, concrete, and under 15 words.
            - Provide a proper priority level (HIGH, MEDIUM, or LOW) for each action based on urgency.
            - Fill the data directly into the requested JSON schema structure.
            """