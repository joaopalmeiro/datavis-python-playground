from typing import Tuple

import altair as alt
import numpy as np
import pandas as pd

CONFUSION_CATEGORIES: Tuple[str, str, str, str] = ("TP", "FP", "FN", "TN")
CONFUSION_CATEGORIES_COL_NAME: str = "confusion_category"


def compute_confusion_categories(
    data: pd.DataFrame, xvar: str, target_var: str, threshold: float
) -> pd.DataFrame:
    conditions = [
        data[target_var].eq(1) & data[xvar].ge(threshold),
        data[target_var].eq(0) & data[xvar].ge(threshold),
        data[target_var].eq(1) & data[xvar].lt(threshold),
        data[target_var].eq(0) & data[xvar].lt(threshold),
    ]

    data[CONFUSION_CATEGORIES_COL_NAME] = np.select(conditions, CONFUSION_CATEGORIES)

    return data


def scoring_confusion_matrix(
    data: pd.DataFrame,
    xvar: str,
    target_var: str,
    threshold: float = 0.5,
    width: int = 200,
    height: int = 200,
) -> alt.Chart:
    data = compute_confusion_categories(data, xvar, target_var, threshold)

    binning = alt.Bin(step=0.1)
    base = alt.Chart(data, width=width, height=height)

    hist = base.mark_bar().encode(
        x=alt.X(f"{xvar}:Q", bin=binning, axis=alt.Axis(format="~", title="Score")),
        y=alt.Y("count():Q", axis=alt.Axis(title="Count")),
        facet=alt.Facet(
            f"{CONFUSION_CATEGORIES_COL_NAME}:O",
            sort=CONFUSION_CATEGORIES,
            title=f"Threshold: {threshold}",
            columns=2,
        ),
    )

    return hist
