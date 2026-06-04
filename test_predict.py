import pandas as pd

from models.predictor import RiskPredictor
from features.feature_builder import build_feature_matrix
from utils.metrics import evaluate


# ==================================================
# LOAD DATA
# ==================================================

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

# ==================================================
# LOAD MODEL
# ==================================================

predictor = RiskPredictor(
    "models/ensemble_bundle.joblib"
)

# ==================================================
# FULL TEST SET EVALUATION
# ==================================================

preds = predictor.predict(X_test)

y_true = df[
    "vector_disease_risk_score"
]

print("Evaluation Metrics")
print(
    evaluate(
        y_true,
        preds
    )
)

# ==================================================
# SINGLE SAMPLE TEST
# ==================================================

print("\nPrediction Example")

result = predictor.predict_with_metadata(
    X_test.iloc[[0]]
)

print(result)

print("\n========== FEATURE SCHEMA ==========\n")

for col, dtype in X_test.dtypes.items():
    print(
        f"{col}: {dtype}"
    )

schema = {
    col: str(dtype)
    for col, dtype
    in X_test.dtypes.items()
}

print(schema)