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


# More info: https://numpy.org/devdocs/reference/typing.html
# import numpy.typing as npt
# npt.ArrayLike
def trunc(values: pd.Series, decs: int = 0) -> pd.Series:
    return np.trunc(values * 10 ** decs) / (10 ** decs)


def get_order_of_magnitude(number: int) -> int:
    return int(math.log10(number))


def compute_bins(
    data: pd.DataFrame, xvar: str, target_var: str, nbins: int = 10
) -> pd.DataFrame:
    decimal_places = get_order_of_magnitude(nbins)

    nbins += 1
    bins = np.linspace(0.0, 1.0, nbins)

    # binned = data.groupby(
    #     [target_var, pd.cut(data[xvar], bins=bins, right=False)]
    # ).count()

    binned = data.copy()
    binned["trunc_score_count"] = trunc(binned[xvar], decs=decimal_places)

    binned = binned.groupby([target_var, "trunc_score_count"])[
        ["trunc_score_count"]
    ].count()

    binned = (
        binned.reset_index(level=target_var)
        .rename_axis("bin_min")
        .reset_index(drop=False)
    )

    full_binned = pd.DataFrame(
        {
            target_var: np.repeat(binned[target_var].unique(), nbins - 1),
            "bin_min": np.tile(bins[:-1], 2),
        }
    )

    binned["bin_min"] = binned["bin_min"].round(decimal_places)
    full_binned["bin_min"] = full_binned["bin_min"].round(decimal_places)

    full_binned = full_binned.merge(
        binned, how="left", on=[target_var, "bin_min"]
    ).fillna(0)

    full_binned["trunc_score_count"] = full_binned["trunc_score_count"].astype("int32")

    full_binned["bin_max"] = np.tile(bins[1:], 2)

    return full_binned


def prepara_bin_edges_for_silhouette_line(
    data: pd.DataFrame, target_var: str, value: int
) -> pd.DataFrame:
    # shifted_data = data.copy()
    # shifted_data["bin_min"] = shifted_data["bin_min"] + 0.1

    # return (
    #     pd.concat([data, shifted_data], ignore_index=True)
    #     .rename(columns={"bin_min": "bin"})
    #     .drop(columns=["bin_max"])
    # )

    silhouette_data = data.query(f"{target_var} == {value}")

    last_row = (
        silhouette_data.tail(1)
        .rename(columns={"bin_max": "bin"})
        .drop(columns=["bin_min"])
    )

    silhouette_data = silhouette_data.rename(columns={"bin_min": "bin"}).drop(
        columns=["bin_max"]
    )

    return pd.concat([silhouette_data, last_row], ignore_index=True)
