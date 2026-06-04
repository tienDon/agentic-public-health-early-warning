import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def evaluate(
    y_true,
    y_pred
):

    return {

        "MAE":
            round(
                mean_absolute_error(
                    y_true,
                    y_pred
                ),
                4
            ),

        "RMSE":
            round(
                np.sqrt(
                    mean_squared_error(
                        y_true,
                        y_pred
                    )
                ),
                4
            ),

        "R2":
            round(
                r2_score(
                    y_true,
                    y_pred
                ),
                4
            )
    }