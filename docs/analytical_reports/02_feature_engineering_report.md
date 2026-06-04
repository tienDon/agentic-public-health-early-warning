# Feature Engineering Report

## 1. Data Integrity & Leakage Control

- **AQI anomaly repair:** 374 invalid negative `air_quality_index` values were corrected using a region-month median computed from the pre-2023 training period.
- **Fallback handling:** Missing region-month medians were replaced with the global training median.
- **Boundary clipping:** `vector_disease_risk_score`, `respiratory_disease_rate`, and `waterborne_disease_incidents` were constrained to the $[0, 100]$ interval.

## 2. Feature Construction

- **Temporal lags:** 1-week and 2-week lag features were created for `temperature_celsius`, `precipitation_mm`, `pm25_ugm3`, `respiratory_disease_rate`, and `waterborne_disease_incidents`.
- **Rolling statistics:** 4-week rolling mean, sum, and standard deviation features were generated for precipitation, temperature, and PM2.5.
- **Seasonality encoding:** `month` was converted into `month_sin` and `month_cos`.
- **Socioeconomic interaction:** `income_level` was ordinally encoded and combined with precipitation to create `precip_vulnerability_interact`.
- **Feature reduction:** Raw `air_quality_index`, `respiratory_disease_rate`, and `waterborne_disease_incidents` columns were dropped after the derived features were created.

## 3. Scaling & Export

- **Training-only scaling:** `RobustScaler` was fit on the 2015-2022 training subset and applied to the 2023-2025 test subset.
- **Target transform:** `target_log = log1p(vector_disease_risk_score)` was added to both splits.
- **Memory optimization:** Numeric columns were cast to `float32` before export.
- **Artifacts generated:** `data/processed/train_features.csv`, `data/processed/test_features.csv`, and `models/robust_scaler.joblib` were successfully saved.

## 4. Final Verification

- **Training samples:** 10,350 records.
- **Test samples:** 3,675 records.
- **Boundary integrity:** 2023 boundary records were preserved after lag generation and filtering.
- **Pipeline status:** Feature engineering and preprocessing completed successfully and are ready for modeling.
