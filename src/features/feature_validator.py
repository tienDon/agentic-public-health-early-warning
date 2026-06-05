import pandas as pd
import numpy as np
from src.core.exceptions import FeatureValidationError

class FeatureValidator:

    def __init__(self, expected_features, feature_schema=None):
        """
        expected_features: list feature từ model
        feature_schema: dict {feature: dtype} (optional)
        """
        self.expected_features = expected_features
        self.feature_schema = feature_schema

    # 1. Check missing columns
    def validate_features(self, X: pd.DataFrame):
        missing = [f for f in self.expected_features if f not in X.columns]
        if missing:
            raise FeatureValidationError(f"Missing features: {missing}")
        return True

    # 2. Check NaN values
    def validate_missing_values(self, X: pd.DataFrame):
        if X.isnull().sum().sum() > 0:
            raise FeatureValidationError("Input contains missing values (NaN)")
        return True

    # 3. Check numeric type
    def validate_dtypes(self, X: pd.DataFrame):
        non_numeric = [
            col for col in self.expected_features
            if not np.issubdtype(X[col].dtype, np.number)
        ]

        if non_numeric:
            raise FeatureValidationError(f"Non-numeric features detected: {non_numeric}")

        return True

    # 4. Validate schema (optional strict mode)
    def validate_schema(self, X: pd.DataFrame):
        if not self.feature_schema:
            return True

        mismatched = []

        for col, expected_dtype in self.feature_schema.items():
            actual_dtype = str(X[col].dtype)
            if col in X.columns and actual_dtype != expected_dtype:
                mismatched.append((col, expected_dtype, actual_dtype))

        if mismatched:
            raise FeatureValidationError(f"Schema mismatch: {mismatched}")

        return True

    # 5. Full pipeline
    def validate(self, X: pd.DataFrame):
        self.validate_features(X)
        self.validate_missing_values(X)
        self.validate_dtypes(X)
        self.validate_schema(X)
        return True

    # 6. Reorder features (VERY IMPORTANT)
    def reorder(self, X: pd.DataFrame):
        return X[self.expected_features]