class PredictionError(Exception):
    pass


class FeatureValidationError(
    PredictionError
):
    pass


class ModelNotLoadedError(
    PredictionError
):
    pass