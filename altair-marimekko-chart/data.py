import pandas as pd


def load_mushroom_dataset(cols=[]):
    data = pd.read_csv("./raw_data/mushrooms.csv", usecols=cols if cols else None)

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

    y_data = (
        data.groupby(xvar)[yvar]
        .value_counts(normalize=True)
        .to_frame(name=f"{yvar}_percentage")
        .reset_index()
    )

    y_data["y2"] = y_data.groupby(xvar)[f"{yvar}_percentage"].cumsum()
    y_data["y1"] = y_data.groupby(xvar)["y2"].shift(fill_value=0)

    marimekko_data = pd.merge(y_data, x_data, on=xvar)

    return marimekko_data
