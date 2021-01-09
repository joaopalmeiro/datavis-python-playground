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


def stellar_chart(data, cat_var, ymax, dpi=100):
    categories = data.columns.tolist()
    categories.remove(cat_var)

    N = len(categories)
    angle_midpoint = pi / N

    # It is necessary to repeat the first value to close the circular chart.
    values = data.loc[0].drop(cat_var).to_list()
    values += values[:1]

    angles = [n / N * 2 * pi for n in range(N)]
    angles += angles[:1]

    fig = plt.figure(dpi=dpi)
    ax = fig.add_subplot(111, polar=True)

    plt.xticks(angles[:-1], categories, color="grey", size=8)

    ax.set_rlabel_position(0)

    plt.yticks(range(10, ymax, 10), color="grey", size=7)
    plt.ylim(0, ymax)

    stellar_angles = [angle + angle_midpoint for angle in angles[:-1]]
    stellar_values = [0.05 * ymax] * N

    all_angles = list(even_odd_merge(angles, stellar_angles))
    all_values = list(even_odd_merge(values, stellar_values))

    ax.plot(
        all_angles, all_values, linewidth=1, linestyle="solid", solid_joinstyle="round",
    )

    ax.fill(all_angles, all_values, "b", alpha=0.1)
