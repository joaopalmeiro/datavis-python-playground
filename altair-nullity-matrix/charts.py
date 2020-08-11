import altair as alt

from data import get_nullity_matrix_data


def nullity_matrix_chart(
    data, keep_original_col_order=True, show_tooltip=False, threshold=0.5, h=400
):
    nm_data, n_rows = get_nullity_matrix_data(data)
    text_font_size = 10

    base = alt.Chart(nm_data, height=h)

    chart = base.mark_rect(cursor="context-menu" if show_tooltip else "default").encode(
        x=alt.X(
            "column:N",
            sort=None if keep_original_col_order else "ascending",
            axis=alt.Axis(
                orient="top",
                labelAngle=-90,
                labelColor="#44475A",
                domain=False,
                tickColor="transparent",
                title=None,
            ),
        ),
        y=alt.Y(
            "row:Q",
            axis=alt.Axis(
                grid=False,
                domain=False,
                tickColor="transparent",
                labelColor="#44475A",
                title=None,
                values=[0, n_rows],
            ),
            scale=alt.Scale(nice=False, domain=[n_rows, 0]),
        ),
        color=alt.Color(
            "isnull:N",
            legend=None,
            scale=alt.Scale(domain=[True, False], range=["white", "#44475A"]),
        ),
    )

    if show_tooltip:
        chart = chart.encode(
            tooltip=[
                alt.Tooltip("row:Q", title="Row"),
                alt.Tooltip("isnull:N", title="Null value?"),
                alt.Tooltip("column:N", title="Column"),
                alt.Tooltip(
                    "percentage_null_values_per_column:Q",
                    format=".2~%",
                    title="% of null values in this column",
                ),
            ]
        )

    # Altair/Vega-Lite:
    # Default `labelFontSize` = 10
    # Default `tickSize` = 5
    # Default `labelPadding` = 2
    # Default `translate` = 0.5

    text = base.mark_text(
        baseline="middle", align="right", fontSize=text_font_size, angle=270
    ).encode(
        x=alt.X("column:N"),
        y=alt.value(h + (text_font_size / 2) + 5 + 2 + 0.5),
        text=alt.Text("percentage_null_values_per_column:Q", format=".2~%"),
        color=alt.condition(
            f"datum.percentage_null_values_per_column > {threshold}",
            alt.value("#E84A5F"),
            alt.value("#44475A"),
        ),
    )

    return (
        alt.layer(chart, text)
        .configure_view(strokeWidth=0)
        .configure_scale(bandPaddingInner=0.1)
    )
