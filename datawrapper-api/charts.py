import os

import pandas as pd
from datawrapper import Datawrapper
from dotenv import load_dotenv

PIE_CHART = "d3-pies"

PURPLE = "#8624F5"
GREEN = "#1FC3AA"


def prepare_column(df, col):
    return df[col].value_counts().rename_axis(col).reset_index(name="count")


if __name__ == "__main__":
    load_dotenv()
    dw_api_token = os.getenv("DATAWRAPPER_API_TOKEN")

    dw = Datawrapper(access_token=dw_api_token)

    data = pd.read_csv("data/maja_horst_paper_table.csv")

    # Gender
    chart_info = dw.create_chart(
        title="Gender of the interviewed scientists",
        chart_type=PIE_CHART,
        data=prepare_column(data, "Gender"),
    )
    dw.update_description(
        chart_info["id"],
        source_name="Horst, 2013",
        source_url="https://doi.org/10.1177/1075547013487513",
    )
    properties = {
        "visualize": {
            "custom-colors": {"Male": GREEN, "Female": PURPLE},
            "inside_labels": {"enabled": False},
            "color_key": {
                "stack": False,
                "enabled": False,
                "position": "top",
                "label_values": True,
            },
            "pie_size": {"inside_labels": 50, "outside_labels": 25},
            "outside_labels": {"edge": False, "color": True, "enabled": True},
        }
    }
    dw.update_metadata(chart_info["id"], properties)
    dw.publish_chart(chart_info["id"], display=False)
    dw.export_chart(
        chart_info["id"],
        output="png",
        filepath="img/gender.png",
        display=False,
        border_width=0,
        scale=4,
    )
