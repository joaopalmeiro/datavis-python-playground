import os


def sow(seed=0):
    random.seed(seed)

    # More info: https://python.readthedocs.io/en/latest/using/cmdline.html#envvar-PYTHONHASHSEED
    os.environ["PYTHONHASHSEED"] = str(seed)


def prepare_titanic_data(data):
    data["sibsp_parch"] = data["SibSp"] + data["Parch"]
    data["is_female"] = (data["Sex"] != "male").astype(int)

    median_age = data["Age"].dropna().median()
    data["age_imputed"] = data["Age"].fillna(median_age)

    return data

