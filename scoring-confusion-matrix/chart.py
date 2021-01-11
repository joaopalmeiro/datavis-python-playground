import altair as alt
import pandas as pd


def confusion_category_histogram(data: pd.DataFrame, xvar: str, full_domain):
    binning = alt.Bin(step=0.1, extent=[0, 1]) if full_domain else alt.Bin(step=0.1)

    base = alt.Chart(data)

    hist = base.mark_bar().encode(alt.X(f"{xvar}:Q", bin=binning), y="count()",)

    return hist


def scoring_confusion_matrix(
    data: pd.DataFrame,
    xvar: str,
    target_var: str,
    threshold: float = 0.5,
    full_domain: bool = True,
):

    data_to_plot = data.query(f"{target_var} == 1 and {xvar} >= {threshold}")
    tp = confusion_category_histogram(data_to_plot, xvar, full_domain)

    return tp
