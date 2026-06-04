# Data Schema

## Core Features

| Column Name    | Type   | Description                                       |
| -------------- | ------ | ------------------------------------------------- |
| `record_id`    | String | Unique identifier for each record                 |
| `country_name` | String | Name of the country                               |
| `date`         | Date   | Start date of the weekly observation (YYYY-MM-DD) |
| `latitude`     | Float  | Country centroid latitude                         |
| `longitude`    | Float  | Country centroid longitude                        |

## Climate Indicators

| Column Name           | Unit  | Logical Range |
| --------------------- | ----- | ------------- |
| `temperature_celsius` | °C    | (-50, 60)     |
| `precipitation_mm`    | mm    | (0, 1000)     |
| `heat_wave_days`      | Days  | (0, 7)        |
| `air_quality_index`   | Index | (0, 500)      |
| `pm25_ugm3`           | µg/m³ | (0, 500)      |

## Health Outcomes

| Column Name                 | Unit      | Logical Range |
| --------------------------- | --------- | ------------- |
| `vector_disease_risk_score` | Index     | (0, 100)      |
| `respiratory_disease_rate`  | Case/100k | (0, 200)      |
| `heat_related_admissions`   | Case/100k | (0, 50)       |

## Socioeconomic Context

| Column Name               | Description                                    |
| ------------------------- | ---------------------------------------------- |
| `income_level`            | Categorical (High, Upper-Middle, Lower-Middle) |
| `healthcare_access_index` | Index (0-1) measuring medical infrastructure   |
