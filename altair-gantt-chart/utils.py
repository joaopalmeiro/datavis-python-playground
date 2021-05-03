def compute_size_with_aspect_ratio(
    value: int, get_width: bool = False, aspect_ratio: float = 16 / 9
) -> float:
    return value * aspect_ratio if get_width else value / aspect_ratio
