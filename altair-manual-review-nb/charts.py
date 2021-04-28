import altair as alt
import pandas as pd


def bar_chart(data: pd.DataFrame, xvar: str, yvar: str) -> alt.Chart:
    base = alt.Chart(data)

    bar = base.mark_bar(tooltip=True, cursor="context-menu").encode(
        x=alt.X(xvar, axis=alt.Axis(labelAngle=0)), y=alt.Y(yvar)
    )

    return bar
