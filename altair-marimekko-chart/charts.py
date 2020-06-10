import altair as alt


def count_bar_chart(data, xvar, w=300, h=300, bar_color="#cda279"):
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

    base = alt.Chart(data, width=w, height=h)

    rect = base.mark_rect(
        strokeWidth=STROKE,
        stroke="white",
        xOffset=STROKE / 2,
        x2Offset=STROKE / 2,
        yOffset=STROKE / 2,
        y2Offset=STROKE / 2,
    ).encode(
        x=alt.X("x1:Q", axis=alt.Axis(zindex=1, format="%", title=xvar, grid=False)),
        x2="x2:Q",
        y=alt.Y("y1:Q", axis=alt.Axis(zindex=1, format="%", title=yvar, grid=False)),
        y2="y2:Q",
        color=alt.Color(f"{yvar}:N"),
        tooltip=[alt.Tooltip(f"{xvar}:N"), alt.Tooltip(f"{yvar}:N")],
    )

    return rect.configure_view(strokeWidth=0)
