import altair as alt
import pandas as pd


def score_dist_chart(
    data: pd.DataFrame,
    xvar: str,
    target_var: str,
    main: int,
    silhouette: int,
    bin_width: float = 0.1,
) -> alt.LayerChart:
    bin_prop = alt.Bin(extent=[0.0, 1.0], step=bin_width)

    base = alt.Chart(data)

    dist = base.encode(x=alt.X(f"{xvar}:Q", bin=bin_prop, title="Score"), y="count()")

    main_dist = dist.mark_bar(tooltip=True, cursor="context-menu").transform_filter(
        f"datum.{target_var} === {main}"
    )
    silhouette_dist = dist.mark_line(
        tooltip=False, interpolate="step", stroke="black", strokeWidth=1, xOffset=0.5
    ).transform_filter(f"datum.{target_var} === {silhouette}")

    return alt.layer(main_dist, silhouette_dist)
