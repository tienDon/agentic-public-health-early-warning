from features.missing_feature_checker import (
    MissingFeatureChecker
)

required = [
    "year",
    "month",
    "latitude"
]

input_cols = [
    "year",
    "month"
]

result = (
    MissingFeatureChecker.check(
        input_cols,
        required
    )
)

print(result)