import pandas as pd

from services.inference_service import InferenceService
from services.report_service import ReportService
from features.feature_builder import build_feature_matrix


# ==================================================
# 1. LOAD TEST DATA
# ==================================================
print("\n[1] Loading test data...")

df = pd.read_csv("data/processed/test_features.csv")

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

print(f"✔ Test samples: {len(X_test)} features: {X_test.shape[1]}")


# ==================================================
# 2. INIT SERVICES
# ==================================================
print("\n[2] Initializing AI services...")

inference_service = InferenceService()
report_service = ReportService()


# ==================================================
# 3. RUN PREDICTION (SINGLE SAMPLE DEMO)
# ==================================================
sample_index = 1637

print(f"\n[3] Running prediction for sample #{sample_index}...")

state = inference_service.predict(
    X_test.iloc[[sample_index]]
)


# ==================================================
# 4. CHECK RESULT STATUS
# ==================================================
if "failed" in state.status:
    print("\n❌ Prediction failed:")
    print(state.status)
    exit()


# ==================================================
# 5. GENERATE REPORT
# ==================================================
print("\n[4] Generating report...")

report = report_service.generate(state)


# ==================================================
# 6. DISPLAY RESULT (MVP DEMO FORMAT)
# ==================================================
print("\n" + "="*50)
print("            CLIMATE HEALTH AI REPORT")
print("="*50)

# Summary
summary = report["summary"]

print("\n📊 RISK SUMMARY")
print("-" * 50)
print(f"Risk Level : {summary['risk_level']}")
print(f"Risk Score : {summary['risk_score']}")
print(f"Confidence : {summary['confidence']}")

# SHAP Insights
print("\n🧠 KEY DRIVERS (SHAP EXPLANATION)")
print("-" * 50)

for i, insight in enumerate(report["insights"], 1):
    print(f"{i}. {insight['reason']}")
    print(f"   Impact: {insight['impact']}")

# Alert
print("\n🚨 ALERT")
print("-" * 50)
print(report["alert"] or "No alert generated")

print("\n" + "="*50)
print("END OF REPORT")
print("="*50)