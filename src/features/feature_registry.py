# features/feature_registry.py

from features.feature_schema import (
    FeatureSchema
)


class FeatureRegistry:

    def __init__(self):

        self.schema = FeatureSchema()

    def get_features(self):

        return self.schema.get_feature_names()

    def get_feature_count(self):

        return len(
            self.get_features()
        )

    def has_feature(
        self,
        feature_name
    ):

        return (
            feature_name
            in self.get_features()
        )