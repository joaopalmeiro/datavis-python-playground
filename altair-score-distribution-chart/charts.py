import altair as alt
import pandas as pd

from utils import prepara_bin_edges_for_silhouette_line


def score_dist_chart(
    data: pd.DataFrame,
    yvar: str,
    target_var: str,
    main: int,
    silhouette: int,
    width: int = 400,
) -> alt.LayerChart:
    # bin_prop = alt.Bin(extent=[0.0, 1.0], step=bin_width)
    bin_prop = alt.Bin(binned=True)

    # n_bins = (1.0 - 0.0) / bin_width
    # single_bar_width = width / n_bins

    main_dist = (
        alt.Chart(data, width=width)
        .encode(
            x=alt.X(f"bin_min:Q", bin=bin_prop, title="Score"),
            x2=alt.X2("bin_max:Q"),
            y=alt.Y(f"{yvar}:Q", title="Count"),
        )
        .mark_bar(tooltip=True, cursor="context-menu")
        .transform_filter(f"datum.{target_var} === {main}")
    )

    silhouette_data = prepara_bin_edges_for_silhouette_line(
        data, target_var, silhouette
    )

    silhouette_dist = (
        alt.Chart(silhouette_data)
        .encode(x=alt.X(f"bin:Q"), y=alt.Y(f"{yvar}:Q"))
        .mark_line(
            point=False,
            tooltip=False,
            interpolate="step-after",
            stroke="black",
            strokeWidth=1,
            xOffset=0.5,
        )
    )

    # debug = (
    #     alt.Chart(data, width=width)
    #     .encode(
    #         x=alt.X(f"bin_min:Q", bin=bin_prop, title="Score"),
    #         x2=alt.X2("bin_max:Q"),
    #         y=alt.Y(f"{yvar}:Q", title="Count"),
    #     )
    #     .mark_bar(tooltip=True, cursor="context-menu", color="red")
    #     .transform_filter(f"datum.{target_var} === {silhouette}")
    # )

    return alt.layer(main_dist, silhouette_dist)
