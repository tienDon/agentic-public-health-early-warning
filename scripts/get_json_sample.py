import pandas as pd
import json

# Load file data đã xử lý
df = pd.read_csv("data/processed/test_features.csv")

# Bỏ các cột metadata/leakage như trong code test của cậu
metadata_cols = ['record_id', 'date', 'country_name', 'region', 'income_level', 'vector_disease_risk_score', 'target_log', 'country_code']
synthetic_leakage_cols = ['temperature_celsius', 'precipitation_mm', 'pm25_ugm3']
drop_cols = metadata_cols + synthetic_leakage_cols
X = df.drop(columns=[c for c in drop_cols if c in df.columns])

# Lấy dòng đầu tiên và chuyển thành dict
sample_dict = X.iloc[0].to_dict()

# In ra màn hình dạng JSON
print(json.dumps(sample_dict, indent=4))
print("length of sample_dict:", len(sample_dict))
print(sample_dict.describe())