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

    # It is necessary to use transforms, so that the facet is sorted as intended,
    # because of this bug: https://github.com/altair-viz/altair/issues/2303.
    hist = (
        base.mark_bar()
        .encode(
            x=alt.X(f"binned_{xvar}:O", axis=alt.Axis(format="~", title="Score")),
            y=alt.Y("y_count:Q", axis=alt.Axis(title="Count")),
            facet=alt.Facet(
                f"{CONFUSION_CATEGORIES_COL_NAME}:O",
                sort=CONFUSION_CATEGORIES,
                title=f"Threshold: {threshold}",
                columns=2,
            ),
        )
        .transform_bin(f"binned_{xvar}", xvar, bin=binning)
        .transform_aggregate(
            y_count="count()", groupby=[f"binned_{xvar}", CONFUSION_CATEGORIES_COL_NAME]
        )
    )

    return hist
