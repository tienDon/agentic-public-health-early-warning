from src.schemas.graph_state import create_initial_state
from src.graphs.graph_dependencies import get_prediction_graph
import pandas as pd

from src.features.feature_builder import (
    build_feature_matrix
)

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

sample = X_test.iloc[1637].to_dict()

state = create_initial_state(
    input_data=sample
)

graph = get_prediction_graph()

result = graph.invoke(state)

print(result)