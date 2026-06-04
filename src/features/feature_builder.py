import numpy as np


def build_feature_matrix(
    df,
    metadata_cols,
    leakage_cols
):

    drop_cols = (
        metadata_cols
        + leakage_cols
    )

    X = df.drop(
        columns=[
            c
            for c in df.columns
            if c in drop_cols
        ],
        errors="ignore"
    ).copy()

    X = X.select_dtypes(
        include=[np.number]
    )

    features = list(X.columns)

    return X, features