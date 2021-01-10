from itertools import chain, tee, zip_longest
from math import pi

import matplotlib.pyplot as plt


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)

    return zip(a, b)


def midpoint(pair):
    return (pair[0] + pair[1]) / 2


def even_odd_merge(even, odd, filter_none=True):
    if filter_none:
        return filter(None.__ne__, chain.from_iterable(zip_longest(even, odd)))

    return chain.from_iterable(zip_longest(even, odd))


def prepare_data(data, cat_var):
    categories = data.columns.tolist()
    categories.remove(cat_var)

    # It is necessary to repeat the first value to close the circular chart.
    values = data.loc[0].drop(cat_var).to_list()
    values += values[:1]

    return categories, values


def prepare_angles(N):
    angles = [n / N * 2 * pi for n in range(N)]
    angles += angles[:1]

    return angles


def prepare_stellar_aux_data(angles, ymax, N):
    angle_midpoint = pi / N

    stellar_angles = [angle + angle_midpoint for angle in angles[:-1]]
    stellar_values = [0.05 * ymax] * N

    return stellar_angles, stellar_values


def draw_peripherals(
    ax, categories, angles, ymax, outer_color="slategrey", inner_color="lightgrey"
):
    plt.xticks(angles[:-1], categories, color=outer_color, size=8)
    ax.set_rlabel_position(0)

    plt.yticks(range(10, ymax, 10), color=inner_color, size=7)
    plt.ylim(0, ymax)

    ax.spines["polar"].set_color(outer_color)

    ax.set_axisbelow(True)
    ax.xaxis.grid(True, color=inner_color, linestyle="-")
    ax.yaxis.grid(True, color=inner_color, linestyle="-")


def stellar_chart(data, cat_var, ymax, dpi=100, color="tab:blue", save_fig=False):
    categories, values = prepare_data(data, cat_var)
    N = len(categories)

    angles = prepare_angles(N)

    fig = plt.figure(dpi=dpi)
    ax = fig.add_subplot(111, polar=True)
    draw_peripherals(ax, categories, angles, ymax)

    stellar_angles, stellar_values = prepare_stellar_aux_data(angles, ymax, N)

    all_angles = list(even_odd_merge(angles, stellar_angles))
    all_values = list(even_odd_merge(values, stellar_values))

    ax.plot(
        all_angles,
        all_values,
        linewidth=1,
        linestyle="solid",
        solid_joinstyle="round",
        color=color,
    )

    ax.fill(all_angles, all_values, color)

    # Decorative dot in the center of the chart.
    ax.plot(0, 0, marker="o", color="white", markersize=3)

    if save_fig:
        plt.savefig(
            "stellar_chart.png", dpi=300, bbox_inches="tight", facecolor="white"
        )
