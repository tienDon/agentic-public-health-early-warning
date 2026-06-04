# EDA Findings Report

## 1. Data Quality & Integrity

- **Missing Values:** 0% missing values across all columns (14,100 records).
- **Duplicates:** No duplicated records found based on `record_id`.
- **Logical Issues:** Detected **374 invalid AQI records** with negative values (min: -52.0).
- **Continuity:**
  - **Temporal:** Each country has exactly 564 weekly observations (2015-2025).
  - **Spatial:** Geographic coordinates (Lat/Long) are 100% consistent per country.

## 2. Key Insights & Trends

- **Seasonality:** Strong annual cycle in both temperature and vector disease risk. Peak disease risk closely follows peak summer temperatures.
- **Correlation Strengths:**
  - `temperature_celsius` vs `vector_disease_risk_score`: **0.65** (Strong positive).
  - `pm25_ugm3` vs `respiratory_disease_rate`: **0.76** (Very strong positive).
  - `air_quality_index` vs `pm25_ugm3`: **0.97** (Redundant features).
- **Precipitation:** Shows a weaker immediate correlation (0.27) with disease risk, suggesting a potential time-lag effect.

## 3. Socioeconomic Impact

- **Inequality:** `Lower-Middle` income countries suffer from significantly higher `respiratory_disease_rate` (>80 vs ~63 in High income).
- **Vulnerability:** Vector disease risk is nearly 4x higher in `Lower-Middle` income countries compared to `High` income.
- **Universal Risk:** `Heat-related admissions` are relatively consistent across all income levels (~7 admissions per 100k), highlighting a universal vulnerability to extreme heat.
- **Healthcare Shield:** Strong negative correlation between `healthcare_access_index` and disease rates, confirming that medical infrastructure mitigates climate-health risks.

## 4. Modeling Implications

- **Target Features:** `vector_disease_risk_score` and `respiratory_disease_rate` are highly predictable using climate drivers.
- **Feature Selection:** One of `air_quality_index` or `pm25_ugm3` should be dropped to avoid multicollinearity.
- **Outlier Focus:** The model must be trained to handle the long tail of outbreaks (risk scores jumping from 0 to 100) instead of just predicting averages.
