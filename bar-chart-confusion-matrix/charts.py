import altair as alt
import pandas as pd

from utils import (
    CONFUSION_CATEGORIES,
    CONFUSION_CATEGORIES_COL_NAME,
    COUNT_COL_NAME,
    compute_confusion_categories,
    humanize_title,
    millify,
)


def bar_chart(
    data: pd.DataFrame,
    xvar: str,
    yvar: str,
    excluded_category: str,
    w: int = 300,
    h: int = 300,
) -> alt.Chart:
    return (
        alt.Chart(data, width=w, height=h)
        .mark_bar()
        .encode(
            x=alt.X(f"{xvar}:N", axis=alt.Axis(labelAngle=0, title=None), sort="-y"),
            y=alt.Y(f"{yvar}:Q", axis=alt.Axis(title=humanize_title(yvar))),
            tooltip=[
                alt.Tooltip(f"{xvar}:N", title=humanize_title(xvar)),
                alt.Tooltip(f"{yvar}:Q", title=humanize_title(yvar)),
            ],
        )
        .transform_filter(alt.datum[xvar] != excluded_category)
    )


def stacked_bar(
    data: pd.DataFrame, xvar: str, yvar: str, main_category: str, w: int = 300
) -> alt.Chart:
    main_value = data.query(f"{xvar} == '{main_category}'")[yvar].item()
    others_value = data.query(f"{xvar} != '{main_category}'")[yvar].sum()

    df = pd.DataFrame(
        {
            "Confusion Category": [
                " + ".join(CONFUSION_CATEGORIES[:-1]),
                main_category,
            ],
            "Count": [others_value, main_value],
        }
    )

    base = alt.Chart(df, width=300)

    stacked_bar = base.mark_bar(
        size=5, strokeWidth=0.5, stroke="black", strokeOpacity=1, tooltip=True
    ).encode(
        x=alt.X("Count:Q", axis=None),
        color=alt.Color("Confusion Category:N", legend=None, sort=None),
    )

    return stacked_bar


def confusion_matrix(
    data: pd.DataFrame,
    score_var: str,
    target_var: str,
    threshold: float,
    subtitle_sep: str = " • ",
) -> alt.VConcatChart:
    data = compute_confusion_categories(data, score_var, target_var, threshold)
    tn_name = CONFUSION_CATEGORIES[-1]
    total = millify(data[COUNT_COL_NAME].sum())

    # print(data)

    bar = bar_chart(data, CONFUSION_CATEGORIES_COL_NAME, COUNT_COL_NAME, tn_name)
    aux_bar = stacked_bar(data, CONFUSION_CATEGORIES_COL_NAME, COUNT_COL_NAME, tn_name)

    return (
        alt.vconcat(bar, aux_bar, spacing=0)
        .properties(
            title={
                "text": "Confusion Matrix",
                "subtitle": [
                    f"{total} instances{subtitle_sep}Threshold: {threshold}",
                    "",
                ],
            }
        )
        .configure_title(anchor="start")
        .configure_view(strokeOpacity=0)
    )
