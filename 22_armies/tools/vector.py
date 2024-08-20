import math
from typing import Tuple, Union


def vectorAddI(v1: Tuple[int, int], v2: Tuple[int, int]) -> Tuple[int, int]:
    return v1[0] + v2[0], v1[1] + v2[1]


def vectorSubI(v1: Tuple[int, int], v2: Tuple[int, int]) -> Tuple[int, int]:
    return v1[0] - v2[0], v1[1] - v2[1]


def vectorSubHalfI(v1: Tuple[int, int], v2: Tuple[int, int]) -> Tuple[int, int]:
    return v1[0] - v2[0] // 2, v1[1] - v2[1] // 2


def vectorSubDiv2I(v1: Tuple[int, int], v2: Tuple[int, int]) -> Tuple[int, int]:
    return (v1[0] - v2[0]) // 2, (v1[1] - v2[1]) // 2


def vectorMulI(v1: Tuple[int, int], v2: Tuple[int, int]) -> Tuple[int, int]:
    return v1[0] * v2[0], v1[1] * v2[1]


def vectorDivI(v1: Tuple[int, int], v2: Tuple[int, int]) -> Tuple[int, int]:
    return v1[0] // v2[0], v1[1] // v2[1]


def vectorMaxI(v1: Tuple[int, int], v2: Union[int, Tuple[int, int]]) -> Tuple[int, int]:
    if type(v2) == int:
        return max(v1[0], v2), max(v1[1], v2)
    elif type(v2) == tuple:
        return max(v1[0], v2[0]), max(v1[1], v2[1])
    else:
        raise ValueError("Invalid value type")


def vectorMinI(v1: Tuple[int, int], v2: Union[int, Tuple[int, int]]) -> Tuple[int, int]:
    if type(v2) == int:
        return min(v1[0], v2), min(v1[1], v2)
    elif type(v2) == tuple:
        return min(v1[0], v2[0]), min(v1[1], v2[1])
    else:
        raise ValueError("Invalid value type")


def vectorClampI(v1: Tuple[int, int],
                 minv: Union[int, Tuple[int, int]],
                 maxv: Union[int, Tuple[int, int]]) -> Tuple[int, int]:
    if type(minv) == int:
        if type(maxv) == int:
            return min(max(v1[0], minv), maxv), \
                min(max(v1[1], minv), maxv)
        elif type(maxv) == tuple:
            return min(max(v1[0], minv), maxv[0]), \
                min(max(v1[1], minv), maxv[1])
        else:
            raise ValueError("Invalid value type")
    elif type(minv) == tuple:
        if type(maxv) == int:
            return min(max(v1[0], minv[0]), maxv), \
                min(max(v1[1], minv[1]), maxv)
        elif type(maxv) == tuple:
            return min(max(v1[0], minv[0]), maxv[0]), \
                min(max(v1[1], minv[1]), maxv[1])
        else:
            raise ValueError("Invalid value type")
    else:
        raise ValueError("Invalid value type")


def vectorMixI(v1: Tuple[int, int], v2: Tuple[int, int], w: float) -> Tuple[int, int]:
    return (
        int(w * v1[0] + (1.0 - w) * v2[0]),
        int(w * v1[1] + (1.0 - w) * v2[1])
    )


def vectorDistI(v1: Tuple[int, int], v2: Tuple[int, int]) -> int:
    return int(round(math.sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2)))


def vectorInfDistI(v1: Tuple[int, int], v2: Tuple[int, int]) -> int:
    return max(abs(v1[0] - v2[0]), abs(v1[1] - v2[1]))


def vectorFtoI(v: Tuple[float, float]) -> Tuple[int, int]:
    return int(v[0]), int(v[1])


def vectorAddF(v1: Tuple[float, float], v2: Tuple[float, float]) -> Tuple[float, float]:
    return v1[0] + v2[0], v1[1] + v2[1]


def vectorSubF(v1: Tuple[float, float], v2: Tuple[float, float]) -> Tuple[float, float]:
    return v1[0] - v2[0], v1[1] - v2[1]


def vectorMulF(v1: Tuple[float, float], v2: Tuple[float, float]) -> Tuple[float, float]:
    return v1[0] * v2[0], v1[1] * v2[1]


def vectorDivF(v1: Tuple[float, float], v2: Tuple[float, float]) -> Tuple[float, float]:
    return v1[0] / v2[0], v1[1] / v2[1]
