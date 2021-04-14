import math
import re
from typing import Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification

CONFUSION_CATEGORIES: Tuple[str, str, str, str] = ("TP", "FP", "FN", "TN")
CONFUSION_CATEGORIES_COL_NAME: str = "confusion_category"
COUNT_COL_NAME: str = "count"


def make_classification_df(
    seed: int,
    n_samples: int = 10_000,
    n_features: int = 25,
    n_informative: int = 10,
    n_redundant: int = 10,
    n_repeated: int = 5,
    class_sep: float = 0.2,
    flip_y: float = 0.1,
    target_col: str = "target",
    target_dist: Optional[Sequence[float]] = None,
) -> pd.DataFrame:
    """Source of default values: https://queirozf.com/entries/scikit-learn-examples-making-dummy-dataset."""
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_redundant=n_redundant,
        n_repeated=n_repeated,
        class_sep=class_sep,
        flip_y=flip_y,
        random_state=seed,
        weights=target_dist,
    )
    df = pd.DataFrame(np.c_[X, y])

    df[df.columns[-1]] = df[df.columns[-1]].astype(int)
    df = df.rename(columns={df.columns[-1]: target_col})

    return df


def compute_confusion_categories(
    data: pd.DataFrame,
    score_var: str,
    target_var: str,
    threshold: float,
    add_counts: bool = True,
) -> pd.DataFrame:
    conditions = [
        data[target_var].eq(1) & data[score_var].ge(threshold),
        data[target_var].eq(0) & data[score_var].ge(threshold),
        data[target_var].eq(1) & data[score_var].lt(threshold),
        data[target_var].eq(0) & data[score_var].lt(threshold),
    ]

    data[CONFUSION_CATEGORIES_COL_NAME] = np.select(conditions, CONFUSION_CATEGORIES)

    agg_data = (
        data[CONFUSION_CATEGORIES_COL_NAME]
        .value_counts()
        .rename_axis(CONFUSION_CATEGORIES_COL_NAME)
        .reset_index(name=COUNT_COL_NAME)
    )

    return agg_data
