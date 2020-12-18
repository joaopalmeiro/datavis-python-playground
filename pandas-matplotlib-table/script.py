import numpy as np
import pandas as pd


def render_mpl_table():
    pass


if __name__ == "__main__":
    table = pd.DataFrame(np.random.randint(0, 100, size=(10, 5)), columns=list("ABCDE"))
