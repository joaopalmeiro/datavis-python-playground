import pandas as pd


def get_nullity_matrix_data(data):
    nm_data = data.copy()

    null_percentage = (
        nm_data.isnull()
        .mean()
        .to_frame(name="percentage_null_values_per_column")
        .rename_axis("column")
        .reset_index()
    )
    n_rows = nm_data.shape[0]

    nm_data = nm_data.isnull()
    nm_data["row"] = nm_data.index
    nm_data = nm_data.melt(id_vars=["row"], var_name="column", value_name="isnull")

    final_data = pd.merge(nm_data, null_percentage, on="column")

    return final_data, n_rows - 1
