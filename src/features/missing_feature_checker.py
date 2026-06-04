# features/missing_feature_checker.py

class MissingFeatureChecker:

    @staticmethod
    def check(
        input_columns,
        required_features
    ):

        input_set = set(
            input_columns
        )

        required_set = set(
            required_features
        )

        missing = list(
            required_set
            - input_set
        )

        extra = list(
            input_set
            - required_set
        )

        return {
            "missing": missing,
            "extra": extra,
            "valid":
                len(missing) == 0
        }