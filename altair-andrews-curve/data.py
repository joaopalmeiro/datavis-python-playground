import numpy as np
import pandas as pd


def get_andrews_curve_dataset(
    data: pd.DataFrame, target_col: str, samples: int = 200
) -> pd.DataFrame:
    t = np.linspace(-np.pi, np.pi, samples)

    one_dimension_per_row = data.drop(target_col, axis=1).values.T

    curves = np.outer(one_dimension_per_row[0] / np.sqrt(2), np.ones_like(t))

    for i in range(1, len(one_dimension_per_row)):
        trig_t = ((i + 1) // 2) * t
        curves += np.outer(
            one_dimension_per_row[i], np.sin(trig_t) if i % 2 else np.cos(trig_t)
        )

    df = pd.DataFrame(
        {
            "t": np.tile(t, curves.shape[0]),
            "sample": np.repeat(np.arange(curves.shape[0]), curves.shape[1]),
            "curve_value": curves.ravel(),
            "target": np.repeat(data[target_col], samples),
        }
    ).reset_index(drop=True)

    return df
