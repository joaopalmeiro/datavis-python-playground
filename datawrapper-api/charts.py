import os
from pathlib import Path

import pandas as pd
import requests as r
from datawrapper import Datawrapper
from dotenv import load_dotenv

PIE_CHART = "d3-pies"
VBAR_CHART = "column-chart"

PURPLE = "#8624F5"
GREEN = "#1FC3AA"
GRAY = "#A6A6A6"


def export_chart_patched(
    self,
    chart_id,
    unit="px",
    mode="rgb",
    width=None,
    plain=False,
    scale=1,
    border_width=20,
    zoom=2,
    output="png",
    filepath="./image.png",
    display=False,
):
    _export_url = f"{self._CHARTS_URL}/{chart_id}/export/{output}"
    _filepath = Path(filepath)
    _filepath = _filepath.with_suffix(f".{output}")

    plain = "true" if plain else "false"
    querystring = {
        "unit": unit,
        "mode": mode,
        "width": width,
        "plain": plain,
        "scale": scale,
        "borderWidth": border_width,
        "zoom": zoom,
    }

    _header = self._auth_header
    _header["accept"] = "*/*"

    export_chart_response = r.get(url=_export_url, headers=_header, params=querystring)

    if export_chart_response.status_code == 200:
        with open(_filepath, "wb") as response:
            response.write(export_chart_response.content)
        if display:
            return Image(_filepath)
        else:
            print(f"File exported at {_filepath}")
    elif export_chart_response.status_code == 403:
        print("You don't have access to the requested code.")
    elif export_chart_response.status_code == 401:
        print("You couldn't be authenticated.")
    else:
        print("Couldn't export at this time.")


Datawrapper.export_chart = export_chart_patched


def prepare_column(df, col, sort=True):
    if sort:
        return df[col].value_counts().rename_axis(col).reset_index(name="count")

    return (
        df[col]
        .value_counts(sort=sort)
        .reindex(df[col].unique())
        .rename_axis(col)
        .reset_index(name="count")
    )


if __name__ == "__main__":
    load_dotenv()
    dw_api_token = os.getenv("DATAWRAPPER_API_TOKEN")

    dw = Datawrapper(access_token=dw_api_token)

    data = pd.read_csv("data/maja_horst_paper_table.csv")

    # Gender
    # chart_info = dw.create_chart(
    #     title="Gender of the interviewed scientists",
    #     chart_type=PIE_CHART,
    #     data=prepare_column(data, "Gender"),
    # )
    # dw.update_description(
    #     chart_info["id"],
    #     source_name="Horst, 2013",
    #     source_url="https://doi.org/10.1177/1075547013487513",
    # )
    # properties = {
    #     "visualize": {
    #         "custom-colors": {"Male": GREEN, "Female": PURPLE},
    #         "inside_labels": {"enabled": False},
    #         "color_key": {
    #             "stack": False,
    #             "enabled": False,
    #             "position": "top",
    #             "label_values": True,
    #         },
    #         "pie_size": {"inside_labels": 50, "outside_labels": 25},
    #         "outside_labels": {"edge": False, "color": True, "enabled": True},
    #     }
    # }
    # dw.update_metadata(chart_info["id"], properties)
    # dw.publish_chart(chart_info["id"], display=False)
    # dw.export_chart(
    #     chart_info["id"],
    #     output="png",
    #     filepath="img/gender.png",
    #     display=False,
    #     border_width=0,
    #     zoom=10,
    # )

    # Age group
    # chart_info = dw.create_chart(
    #     title="Age group of the interviewed scientists",
    #     chart_type=VBAR_CHART,
    #     data=prepare_column(data, "Age, years", sort=False),
    # )
    # dw.update_description(
    #     chart_info["id"],
    #     source_name="Horst, 2013",
    #     source_url="https://doi.org/10.1177/1075547013487513",
    # )
    # properties = {
    #     "visualize": {"rotate-labels": "off", "custom-colors": {"Undisclosed": GRAY},}
    # }
    # dw.update_metadata(chart_info["id"], properties)
    # dw.publish_chart(chart_info["id"], display=False)
    # dw.export_chart(
    #     chart_info["id"],
    #     output="png",
    #     filepath="img/age_group.png",
    #     display=False,
    #     border_width=0,
    #     zoom=8,
    # )
