import altair as alt
from configs import COLORS


def andrews_curve(
    data,
    xvar="t",
    yvar="curve_value",
    targetvar="target",
    samplevar="sample",
    w=450,
    h=300,
):
    selection = alt.selection_single(fields=[targetvar], bind="legend")

    base = alt.Chart(data).properties(width=w, height=h).mark_line()

    background_chart = base.encode(
        x=alt.X(f"{xvar}:Q", axis=alt.Axis(title=None)),
        y=alt.Y(f"{yvar}:Q", axis=alt.Axis(title=None)),
        detail=alt.Detail(f"{samplevar}:N"),
        color=alt.value(COLORS["light_gray"]),
    )

    chart = background_chart.encode(
        color=alt.condition(
            selection,
            f"{targetvar}:N",
            alt.value("transparent"),
            legend=alt.Legend(title=targetvar.title()),
        ),
    ).add_selection(selection)

    return background_chart + chart

