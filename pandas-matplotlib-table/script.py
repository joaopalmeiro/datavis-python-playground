import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def render_mpl_table(
    data,
    col_width=3.0,
    row_height=0.625,
    bbox=[0, 0, 1, 1],
    font_size=14,
    edge_color="w",
    header_color="#44475a",
    row_colors=["#f5f5f5", "w"],
    header_columns=0,
    **kwargs,
):
    size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array(
        [col_width, row_height]
    )
    fig, ax = plt.subplots(figsize=size)  # (width, height)
    ax.axis("off")

    mpl_table = ax.table(
        cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs,
    )

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table.get_celld().items():
        cell.set_edgecolor(edge_color)

        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight="bold", color="w")
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])

    return fig


if __name__ == "__main__":
    data = pd.DataFrame(np.random.randint(0, 100, size=(20, 5)), columns=list("ABCDE"))

    table = render_mpl_table(data)

    table.savefig("table.png", dpi=300, bbox_inches="tight")
