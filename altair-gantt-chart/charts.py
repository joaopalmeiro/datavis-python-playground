from typing import Optional, Union

import altair as alt
import pandas as pd

from utils import compute_size_with_aspect_ratio, split_rows_with_marker

# Colors:
# - https://colors.eva.design/
# - https://akveo.github.io/nebular/docs/design-system/dark-theme
BLACK_COLOR: str = "#222b45"  # color-basic-800


def gantt_chart(
    data: pd.DataFrame,
    xstart_var: str,
    xend_var: str,
    yvar: str,
    width: int = 500,
    marker: Optional[pd.DataFrame] = None,
    color: str = "#3366ff",  # color-primary-500
    deemphasis_color: str = "#a6c1ff",  # color-primary-300
) -> Union[alt.Chart, alt.LayerChart]:
    height = compute_size_with_aspect_ratio(width)

    data = split_rows_with_marker(data, xstart_var, xend_var, marker)

    gantt = (
        alt.Chart(data, width=width, height=height)
        .mark_bar(color=color, tooltip=False)
        .encode(
            x=alt.X(
                f"{xstart_var}:T",
                axis=alt.Axis(
                    grid=False,
                    title=None,
                    tickColor=BLACK_COLOR,
                    labelColor=BLACK_COLOR,
                    domainColor=BLACK_COLOR,
                ),
                # More info: https://altair-viz.github.io/user_guide/generated/core/altair.Scale.html
                scale=alt.Scale(nice={"interval": "week", "step": 2}),
                # scale=alt.Scale(nice="month"),
            ),
            x2=alt.X2(f"{xend_var}:T"),
            y=alt.Y(
                f"{yvar}:O",
                sort=None,
                axis=alt.Axis(
                    grid=True,
                    domain=False,
                    ticks=True,
                    title=None,
                    labelColor=BLACK_COLOR,
                    gridColor="#e4e9f2",  # color-basic-400
                ),
            ),
        )
    )

    if marker is not None:
        gantt = gantt.encode(
            color=alt.condition(
                alt.datum[xend_var] <= alt.expr.time(marker["date"].item()),
                alt.value(color),
                alt.value(deemphasis_color),
            )
        )

        base_marker = alt.Chart(marker).encode(x="date:T")

        vrule = base_marker.mark_rule(
            strokeDash=[5, 1], tooltip=False, color=color
        ).encode(size=alt.value(1.0))

        text = base_marker.mark_text(
            align="center",
            baseline="bottom",
            dy=-height / 2 - 3,
            tooltip=False,
            color=BLACK_COLOR,
        ).encode(text="message:N")

        gantt = alt.layer(gantt, vrule, text)

    return (
        gantt.properties(
            usermeta={
                "embedOptions": {"downloadFileName": "gantt_chart", "scaleFactor": 5}
            }
        )
        .configure_view(strokeWidth=0)
        .configure_axisY(tickColor="transparent")
    )
