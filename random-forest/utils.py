import os

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification


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
) -> pd.DataFrame:
    """Default values: https://queirozf.com/entries/scikit-learn-examples-making-dummy-dataset."""
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_redundant=n_redundant,
        n_repeated=n_repeated,
        class_sep=class_sep,
        flip_y=flip_y,
        random_state=seed,
    )
    df = pd.DataFrame(np.c_[X, y])

    df[df.columns[-1]] = df[df.columns[-1]].astype(int)
    df = df.rename(columns={df.columns[-1]: target_col})

    return df
