from typing import Any, Union

import numpy as np
import pandas as pd
from carla.data.catalog import OnlineCatalog

def predict_negative_instances(model: Any, data: Union[pd.DataFrame, OnlineCatalog]) -> pd.DataFrame:
    """Predicts the data target and retrieves the negative instances. (H^-)

    Assumption: Positive class label is at position 1

    Parameters
    ----------
    name : Tensorflow or PyTorch Model
        Model object retrieved by :func:`load_model`
    data : pd.DataFrame
        Dataset used for predictions
    Returns
    -------
    df :  data.api Data() class with negative predicted instances
    """
    # get processed data and remove target
    df = data.df.copy()
    df["y_neg"] = predict_label(model, df)
    df = df[df["y_neg"] == 0]
    df = df.drop("y_neg", axis="columns")

    return df


def predict_label(model: Any, df: pd.DataFrame, as_prob: bool = False) -> np.ndarray:
    """Predicts the data target

    Assumption: Positive class label is at position 1

    Parameters
    ----------
    name : Tensorflow or PyTorch Model
        Model object retrieved by :func:`load_model`
    df : pd.DataFrame
        Dataset used for predictions
    Returns
    -------
    predictions :  2d numpy array with predictions
    """

    predictions = model.predict(df)

    if not as_prob:
        predictions = predictions.round()

    return predictions
