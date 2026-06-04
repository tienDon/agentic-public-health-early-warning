class ExplanationService:

    def explain(self, record):

        reasons = []

        if record["temp_rolling_4wk_mean"] > 1:
            reasons.append(
                "Sustained high temperature trend detected"
            )

        if record["temperature_celsius_lag_1"] > 1:
            reasons.append(
                "Recent temperature spike detected"
            )

        if record["pm25_rolling_4wk_mean"] > 1:
            reasons.append(
                "Air pollution elevated"
            )

        if record["healthcare_access_index"] < -0.5:
            reasons.append(
                "Healthcare access below average"
            )

        if record["precip_vulnerability_interact"] > 1:
            reasons.append(
                "Climate vulnerability interaction elevated"
            )

        if not reasons:
            reasons.append(
                "No dominant risk factor identified"
            )

        return reasons