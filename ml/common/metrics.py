from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)


def classification_metrics(
    y_true,
    y_pred,
    y_probability,
) -> dict[str, Any]:
    return {
        "accuracy": float(
            accuracy_score(y_true, y_pred)
        ),
        "precision": float(
            precision_score(
                y_true,
                y_pred,
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                y_true,
                y_pred,
                zero_division=0,
            )
        ),
        "f1_score": float(
            f1_score(
                y_true,
                y_pred,
                zero_division=0,
            )
        ),
        "roc_auc": float(
            roc_auc_score(
                y_true,
                y_probability,
            )
        ),
        "confusion_matrix": confusion_matrix(
            y_true,
            y_pred,
        ).tolist(),
    }


def regression_metrics(
    y_true,
    y_pred,
) -> dict[str, float]:
    y_true_array = np.asarray(y_true)
    y_pred_array = np.asarray(y_pred)

    mae = mean_absolute_error(
        y_true_array,
        y_pred_array,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_true_array,
            y_pred_array,
        )
    )

    non_zero_mask = y_true_array != 0

    if non_zero_mask.any():
        mape = (
            np.mean(
                np.abs(
                    (
                        y_true_array[non_zero_mask]
                        - y_pred_array[non_zero_mask]
                    )
                    / y_true_array[non_zero_mask]
                )
            )
            * 100
        )
    else:
        mape = 0.0

    return {
        "mae": float(mae),
        "rmse": float(rmse),
        "mape": float(mape),
        "r2": float(
            r2_score(
                y_true_array,
                y_pred_array,
            )
        ),
    }