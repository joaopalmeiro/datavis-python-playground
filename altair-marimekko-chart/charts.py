import altair as alt

ANTIQUE = [
    "#855C75",
    "#D9AF6B",
    "#AF6458",
    "#736F4C",
    "#526A83",
    "#625377",
    "#68855C",
    "#9C9C5E",
    "#A06177",
    "#8C785D",
    "#467378",
    "#7C7C7C",
]


def count_bar_chart(data, xvar, w=300, h=300, bar_color=ANTIQUE[2]):
    return (
        alt.Chart(data, width=w, height=h)
        .mark_bar(color=bar_color)
        .encode(
            x=alt.X(f"{xvar}:N"),
            y=alt.Y("count(*):Q", axis=alt.Axis(format="s", title="Count")),
            tooltip=[f"{xvar}:N", alt.Tooltip("count(*):Q", format=",", title="Count")],
        )
    )


def marimekko_chart(data, xvar, yvar, w=400, h=400):
    STROKE = 1

    selection = alt.selection_single(fields=[yvar], bind="legend")

    base = alt.Chart(data, width=w, height=h)

    rect = (
        base.mark_rect(
            strokeWidth=STROKE,
            stroke="white",
            xOffset=STROKE / 2,
            x2Offset=STROKE / 2,
            yOffset=STROKE / 2,
            y2Offset=STROKE / 2,
        )
        .encode(
            x=alt.X(
                "x1:Q",
                axis=alt.Axis(
                    zindex=1, format="%", title=f"{xvar} (% of total)", grid=False
                ),
            ),
            x2="x2:Q",
            y=alt.Y(
                "y1:Q",
                axis=alt.Axis(
                    zindex=1, format="%", title=f"{yvar} (% of total)", grid=False
                ),
            ),
            y2="y2:Q",
            color=alt.Color(
                f"{yvar}:N",
                legend=alt.Legend(title=f"{yvar} (press to highlight)"),
                scale=alt.Scale(range=ANTIQUE),
            ),
            tooltip=[
                alt.Tooltip(f"{xvar}_tooltip:N", title=xvar),
                alt.Tooltip(f"{yvar}_tooltip:N", title=yvar),
            ],
            opacity=alt.condition(selection, alt.value(1), alt.value(0.3)),
        )
        .add_selection(selection)
    )

    return rect.configure_view(strokeWidth=0)
