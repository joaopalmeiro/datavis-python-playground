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

    # Sort the DataFrame according to the confusion categories.
    # Source: https://stackoverflow.com/questions/13838405/custom-sorting-in-pandas-dataframe.
    confusion_category_order = {k: v for v, k in enumerate(CONFUSION_CATEGORIES)}
    data = data.sort_values(
        by=CONFUSION_CATEGORIES_COL_NAME, key=lambda x: x.map(confusion_category_order)
    )

    n_instances = (
        data[CONFUSION_CATEGORIES_COL_NAME]
        .value_counts()
        .rename_axis(CONFUSION_CATEGORIES_COL_NAME)
        .reset_index(name="count")
    )

    data = pd.merge(data, n_instances, on=CONFUSION_CATEGORIES_COL_NAME)
    data[CONFUSION_CATEGORIES_COL_NAME] = (
        data[CONFUSION_CATEGORIES_COL_NAME] + " (" + data["count"].astype(str) + ")"
    )

    data = data.drop("count", axis=1)

    return data


def scoring_confusion_matrix(
    data: pd.DataFrame,
    xvar: str,
    target_var: str,
    threshold: float = 0.5,
    bin_width: float = 0.1,
    width: int = 200,
    height: int = 200,
) -> alt.Chart:
    data = compute_confusion_categories(data, xvar, target_var, threshold)
    confusion_categories_with_counts = data[CONFUSION_CATEGORIES_COL_NAME].unique()

    binning = alt.Bin(step=bin_width)
    base = alt.Chart(
        data,
        width=width,
        height=height,
        usermeta={
            "embedOptions": {
                "scaleFactor": 5,
                "downloadFileName": "scoring_confusion_matrix",
            }
        },
    )

    # It is necessary to use transforms, so that the faceted chart is sorted as intended.
    # More info: https://github.com/altair-viz/altair/issues/2303.
    hist = (
        base.mark_bar(tooltip=True)
        .encode(
            x=alt.X(
                f"binned_{xvar}:Q",
                bin="binned",
                axis=alt.Axis(format="~", title="Score"),
            ),
            x2=f"binned_{xvar}_end:Q",
            y=alt.Y("y_count:Q", axis=alt.Axis(title="Count")),
            facet=alt.Facet(
                f"{CONFUSION_CATEGORIES_COL_NAME}:O",
                sort=confusion_categories_with_counts,
                title=None,
                columns=2,
            ),
        )
        .transform_bin(f"binned_{xvar}", xvar, bin=binning)
        .transform_joinaggregate(
            y_count=f"count()",
            groupby=[
                f"binned_{xvar}",
                f"binned_{xvar}_end",
                CONFUSION_CATEGORIES_COL_NAME,
            ],
        )
    )

    return hist.properties(
        title={
            "text": "Scoring confusion matrix",
            "subtitle": f"Threshold: {threshold}",
        }
    )
