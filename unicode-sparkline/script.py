SPARK_CHARS = "▁▂▃▅▆▇"


def sparkbars(data, empty_zero=True):
    valid = [datum for datum in data if datum is not None]

    mn = min(valid)
    mx = max(valid)
    n = len(SPARK_CHARS)

    incr = (mx - mn) / n

    res = None

    return incr


if __name__ == "__main__":
    data = [9, 6, None, 1, 4, 0, 8, 15, 10]

    print(sparkbars(data))

