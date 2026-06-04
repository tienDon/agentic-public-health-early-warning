import shap
import pandas as pd

FEATURE_DESCRIPTIONS = {
    "temp_rolling_4wk_mean": "Sustained high temperature trend",
    "temperature_celsius_lag_1": "Recent temperature anomaly",
    "temperature_celsius_lag_2": "Persistent temperature anomaly",
    "pm25_rolling_4wk_mean": "Elevated air pollution levels",
    "healthcare_access_index": "Healthcare access below average",
    "precip_vulnerability_interact": "Climate vulnerability interaction",
    "heat_related_admissions": "Heat-related health burden elevated"
}

class ShapExplanationService:
    def __init__(self, model, feature_names):
        self.explainer = shap.TreeExplainer(model)
        self.feature_names = feature_names

    def explain(self, X):
        """Tính toán raw SHAP values."""
        shap_values = self.explainer.shap_values(X)
        if isinstance(X, pd.DataFrame):
            return pd.DataFrame(shap_values, columns=self.feature_names)
        return shap_values

    def explain_prediction(self, X, index=0, top_n=3):
        """
        FIX 1 & 4: Khớp Contract và chuẩn hóa Schema thành một List[Dict] duy nhất.
        """
        shap_df = self.explain(X)
        actual_shap = shap_df.iloc[index]
        abs_shap = actual_shap.abs()
        
        top_feature_names = abs_shap.nlargest(top_n).index
        
        explanations = []
        for feat in top_feature_names:
            reason = FEATURE_DESCRIPTIONS.get(
                feat, 
                feat.replace("_", " ").capitalize()
            )
            explanations.append({
                "feature": feat,
                "impact": round(float(actual_shap[feat]), 4),
                "reason": reason
            })
        return explanations