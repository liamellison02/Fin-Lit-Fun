from typing import Tuple

import numpy as np


def mask4(a: Tuple[int, int, int, int],
          value: int) -> Tuple[int, int, int, int]:
    return (a[0] == value, a[1] == value,
            a[2] == value, a[3] == value)


def combine4(
        a: Tuple[int, int, int, int],
        b: Tuple[int, int, int, int]) \
        -> Tuple[int, int, int, int]:
    return (
        a[0] or b[0],
        a[1] or b[1],
        a[2] or b[2],
        a[3] or b[3]
    )


def code4(a: Tuple[int, int, int, int]) -> int:
    return a[0] + 2 * a[1] + 4 * a[2] + 8 * a[3]


weights4 = np.array((1, 2, 4, 8))


def code4np(a: np.ndarray) -> np.ndarray:
    return a.dot(weights4)
