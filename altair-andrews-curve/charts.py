import altair as alt
import pandas as pd

from configs import COLORS


def andrews_curve(
    data: pd.DataFrame,
    xvar: str = "t",
    yvar: str = "curve_value",
    targetvar: str = "target",
    samplevar: str = "sample",
    w: int = 450,
    h: int = 300,
) -> alt.LayerChart:
    selection = alt.selection_single(fields=[targetvar], bind="legend")

    base = alt.Chart(data).properties(width=w, height=h).mark_line()

    background_chart = base.encode(
        x=alt.X(f"{xvar}:Q", axis=alt.Axis(title=None), scale=alt.Scale(nice=False)),
        y=alt.Y(f"{yvar}:Q", axis=alt.Axis(title=None)),
        detail=alt.Detail(f"{samplevar}:N"),
        color=alt.value(COLORS["light_gray"]),
    )

    chart = background_chart.encode(
        color=alt.condition(
            selection,
            f"{targetvar}:N",
            alt.value("transparent"),
            legend=alt.Legend(title=f"{targetvar.title()} (click to highlight)"),
        ),
    ).add_selection(selection)

    return background_chart + chart

