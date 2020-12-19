from functools import partial

SPARKBAR_CHARS = "▁▂▃▅▆▇"


def get_sparkbar_char(datum, mn, incr, empty_zero, none_value):
    """Source: fastcore (https://fastcore.fast.ai/).

    >>> not 0
    True
    >>> not 1
    False
    """
    if datum is None:
        return none_value
    elif empty_zero and not datum:
        return " "
    else:
        bar_idx = int((datum - mn) / incr - 0.5)

        return SPARKBAR_CHARS[bar_idx]


def sparkbars(data, empty_zero=True, none_value=" "):
    """Source: fastcore (https://fastcore.fast.ai/)."""
    valid = [datum for datum in data if datum is not None]

    mn = min(valid)
    mx = max(valid)
    n = len(SPARKBAR_CHARS)  # Number of bars available

    extent = mx - mn
    bar_incr = extent / n  # "Uniform"

    res = [
        get_sparkbar_char(datum, mn, bar_incr, empty_zero, none_value) for datum in data
    ]

    return "".join(res)


if __name__ == "__main__":
    print = partial(print, end="\n\n")

    print(sparkbars([9, 6, None, 1, 4, 0, 8, 15, 10]))
    print(sparkbars([9, 6, None, 1, 4, 0, 8, 15, 10], empty_zero=False))
    print(
        sparkbars([9, 6, None, 1, 4, 0, 8, 15, 10], none_value="�")
    )  # Replacement character

    print(sparkbars([1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2, 1]))
    print(sparkbars([0, 1, 19, 20]))
