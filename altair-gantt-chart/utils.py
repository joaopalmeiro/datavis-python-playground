from typing import Optional

import pandas as pd


def compute_size_with_aspect_ratio(
    value: int, get_width: bool = False, aspect_ratio: float = 16 / 9
) -> float:
    return value * aspect_ratio if get_width else value / aspect_ratio


def split_rows_with_marker(
    data: pd.DataFrame, xstart_var: str, xend_var: str, marker: Optional[pd.DataFrame]
) -> pd.DataFrame:
    if marker is None:
        return data

    data = data.copy()
    marker_date = marker["date"].item()

    mask = (data[xstart_var] < marker_date) & (data[xend_var] > marker_date)

    data_aux = data.copy()[mask]
    data_aux[xstart_var] = marker_date

    data.loc[mask, xend_var] = marker_date

    return pd.concat([data, data_aux], ignore_index=True)
