import altair as alt


def count_bar_chart(data, xvar):
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X(f"{xvar}:N"),
            y=alt.Y("count(*):Q", axis=alt.Axis(format="s", title="Count")),
            tooltip=[f"{xvar}:N", alt.Tooltip("count(*):Q", title="Count")],
        )
    )
