import joblib


class FeatureSchema:

    def __init__(
        self,
        schema_path="artifacts/feature_schema.joblib"
    ):
        self.schema = joblib.load(
            schema_path
        )

    def get_feature_names(self):
        return list(
            self.schema.keys()
        )

    def get_dtype(
        self,
        feature_name
    ):
        return self.schema.get(
            feature_name
        )

    def validate(
        self,
        df
    ):
        missing = []

        for feature in self.schema:

            if feature not in df.columns:
                missing.append(
                    feature
                )

        return {
            "valid": len(missing) == 0,
            "missing": missing
        }