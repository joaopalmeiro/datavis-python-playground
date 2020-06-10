import pandas as pd

HABITAT = {
    "g": "grasses",
    "l": "leaves",
    "m": "meadows",
    "p": "paths",
    "u": "urban",
    "w": "waste",
    "d": "woods",
}

CLASS = {"e": "edible", "p": "poisonous"}

COLUMN_MAPS = {"class": CLASS, "habitat": HABITAT}


def load_mushroom_dataset(cols=[]):
    data = pd.read_csv("./raw_data/mushrooms.csv", usecols=cols if cols else None)

    for col in cols:
        if col in COLUMN_MAPS.keys():
            data[col] = data[col].map(COLUMN_MAPS[col])

    return data


def get_marimekko_data(data, xvar, yvar):
    x_data = (
        data[xvar]
        .value_counts(normalize=True)
        .to_frame(name=f"{xvar}_percentage")
        .rename_axis(xvar)
        .reset_index()
    )

    x_data["x2"] = x_data[f"{xvar}_percentage"].cumsum()
    x_data["x1"] = x_data["x2"].shift(fill_value=0)

    x_data[f"{xvar}_tooltip"] = (
        x_data[xvar] + " (" + x_data[f"{xvar}_percentage"].map("{:.2%}".format) + ")"
    )

    y_data = (
        data.groupby(xvar)[yvar]
        .value_counts(normalize=True)
        .to_frame(name=f"{yvar}_percentage")
        .reset_index()
    )

    y_data["y2"] = y_data.groupby(xvar)[f"{yvar}_percentage"].cumsum()
    y_data["y1"] = y_data.groupby(xvar)["y2"].shift(fill_value=0)

    y_data[f"{yvar}_tooltip"] = (
        y_data[yvar] + " (" + y_data[f"{yvar}_percentage"].map("{:.2%}".format) + ")"
    )

    marimekko_data = pd.merge(y_data, x_data, on=xvar)

    marimekko_data = marimekko_data[
        [
            xvar,
            yvar,
            f"{xvar}_percentage",
            f"{yvar}_percentage",
            f"{xvar}_tooltip",
            f"{yvar}_tooltip",
            "x1",
            "x2",
            "y1",
            "y2",
        ]
    ]

    return marimekko_data
