import pandas as pd

from services.inference_service import (
    InferenceService
)

from features.feature_builder import (
    build_feature_matrix
)

from services.report_service import ReportService

df = pd.read_csv(
    "data/processed/test_features.csv"
)

metadata_cols = [
    "date",
    "country_name",
    "region",
    "income_level",
    "vector_disease_risk_score",
    "target_log"
]

leakage_cols = [
    "temperature_celsius",
    "precipitation_mm",
    "pm25_ugm3"
]

X_test, _ = build_feature_matrix(
    df,
    metadata_cols,
    leakage_cols
)

service = InferenceService()

# for x in range(len(X_test)):
#     state = service.predict(
#         X_test.iloc[[x]]
#     )
#     if state.risk_level == "HIGH":
#         print(f"High risk detected for index {x}:")
#         print(state.explanation)
state = service.predict(
    X_test.iloc[[1637]]
)

print()
print("Risk Level:", state.risk_level)
print("Risk Score:", state.risk_score)
print("Confidence:", state.confidence)
print("Explanation:", state.explanation)
print("Alert:", state.alert_message)
print()
print(f"Prediction State: {state}")
