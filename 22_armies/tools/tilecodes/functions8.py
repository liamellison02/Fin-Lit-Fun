from typing import Tuple

import numpy as np


def mask8(
        a: Tuple[int, int, int, int, int, int, int, int],
        value: int) -> Tuple[int, int, int, int, int, int, int, int]:
    return (
        a[0] == value,
        a[1] == value,
        a[2] == value,
        a[3] == value,
        a[4] == value,
        a[5] == value,
        a[6] == value,
        a[7] == value
    )


def combine8(
        a: Tuple[int, int, int, int, int, int, int, int],
        b: Tuple[int, int, int, int, int, int, int, int]) \
        -> Tuple[int, int, int, int, int, int, int, int]:
    return (
        a[0] or b[0],
        a[1] or b[1],
        a[2] or b[2],
        a[3] or b[3],
        a[4] or b[4],
        a[5] or b[5],
        a[6] or b[6],
        a[7] or b[7]
    )


def simplify8(a: Tuple[int, int, int, int, int, int, int, int]) \
        -> Tuple[int, int, int, int, int, int, int, int]:
    return (
        0 if a[0] and (not a[1] or not a[3]) else a[0],
        a[1],
        0 if a[2] and (not a[1] or not a[4]) else a[2],
        a[3],
        a[4],
        0 if a[5] and (not a[6] or not a[3]) else a[5],
        a[6],
        0 if a[7] and (not a[6] or not a[4]) else a[7]
    )


def code8(a: Tuple[int, int, int, int, int, int, int, int]) -> int:
    return a[0] + 2 * a[1] + 4 * a[2] + 8 * a[3] \
           + 16 * a[4] + 32 * a[5] + 64 * a[6] + 128 * a[7]


def decode8(code: int) -> Tuple[int, int, int, int, int, int, int, int]:
    return (
        code & 1,
        (code & 2) // 2,
        (code & 4) // 4,
        (code & 8) // 8,
        (code & 16) // 16,
        (code & 32) // 32,
        (code & 64) // 64,
        (code & 128) // 128
    )


weights8 = np.array((1, 2, 4, 8, 16, 32, 64, 128))


def code8np(a: np.ndarray) -> np.ndarray:
    return a.dot(weights8)
