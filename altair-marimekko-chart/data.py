import pandas as pd


def load_mushroom_dataset(cols=[]):
    data = pd.read_csv("./raw_data/mushrooms.csv", usecols=cols if cols else None)

    return data
