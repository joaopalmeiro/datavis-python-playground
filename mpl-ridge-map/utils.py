# from itertools import chain
from typing import Dict, List, Tuple


def generate_bboxfinder_url(g_bbox: Dict[str, List[float]]) -> str:
    # (lat, long, lat, long)
    base_url = "http://bboxfinder.com/#"

    ne = g_bbox["northeast"]
    sw = g_bbox["southwest"]

    coordinates = map(str, [*sw, *ne])
    # coordinates = map("{:.6f}".format, chain.from_iterable(g_bbox.values()))
    # coordinates = map(str, chain.from_iterable(g_bbox.values()))

    query = ",".join(coordinates)

    url = f"{base_url}{query}"

    return url


def get_ridge_map_bbox(
    g_bbox: Dict[str, List[float]]
) -> Tuple[float, float, float, float]:
    # return tuple(
    #     chain.from_iterable(coordinate[::-1] for coordinate in g_bbox.values())
    # )

    # ne = g_bbox["northeast"][::-1]
    # sw = g_bbox["southwest"][::-1]

    # -> Tuple[float, ...]
    # return (*sw, *ne)

    ne = g_bbox["northeast"]
    sw = g_bbox["southwest"]

    return (sw[1], sw[0], ne[1], ne[0])
