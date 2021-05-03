from typing import Optional, Union

import altair as alt
import pandas as pd

from utils import compute_size_with_aspect_ratio, split_rows_with_marker


def gantt_chart(
    data: pd.DataFrame,
    xstart_var: str,
    xend_var: str,
    yvar: str,
    width: int = 500,
    marker: Optional[pd.DataFrame] = None,
) -> Union[alt.Chart, alt.LayerChart]:
    height = compute_size_with_aspect_ratio(width)

    data = split_rows_with_marker(data, xstart_var, xend_var, marker)

    gantt = (
        alt.Chart(data, width=width, height=height)
        .mark_bar(tooltip=False)
        .encode(
            x=alt.X(f"{xstart_var}:T", axis=alt.Axis(grid=False, title=None)),
            x2=alt.X2(f"{xend_var}:T"),
            y=alt.Y(
                f"{yvar}:O",
                sort=None,
                axis=alt.Axis(grid=True, domain=False, ticks=True, title=None),
            ),
        )
    )

    if marker is not None:
        gantt = gantt.encode(
            color=alt.condition(
                alt.datum[xend_var] <= alt.expr.time(marker["date"].item()),
                alt.value("blue"),
                alt.value("gray"),
            )
        )

        base_marker = alt.Chart(marker).encode(x="date:T")

        vrule = base_marker.mark_rule(
            xOffset=0.5, strokeDash=[5, 1], tooltip=False
        ).encode(size=alt.value(1.0))

        text = base_marker.mark_text(
            align="center", baseline="bottom", dy=-height / 2 - 3, tooltip=False,
        ).encode(text="message:N")

        gantt = alt.layer(gantt, vrule, text)

    return gantt.configure_view(strokeWidth=0).configure_axisY(tickColor="transparent")
