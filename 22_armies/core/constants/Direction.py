from enum import Enum, auto

from typing import Tuple


class Direction(Enum):
    NONE = 0
    LEFT = auto()
    TOP = auto()
    BOTTOM = auto()
    RIGHT = auto()
    TOPLEFT = auto(),
    TOPRIGHT = auto(),
    BOTTOMLEFT = auto(),
    BOTTOMRIGHT = auto()


directions4 = (
    Direction.LEFT,
    Direction.TOP,
    Direction.BOTTOM,
    Direction.RIGHT
)

directions8 = (
    Direction.TOPLEFT,
    Direction.LEFT,
    Direction.BOTTOMLEFT,
    Direction.TOP,
    Direction.BOTTOM,
    Direction.TOPRIGHT,
    Direction.RIGHT,
    Direction.BOTTOMRIGHT
)


def transformCoords(cell: Tuple[int, int], direction: Direction) -> Tuple[int, int]:
    if direction == Direction.NONE:
        return cell
    x, y = cell
    if direction == Direction.LEFT:
        return x - 1, y
    if direction == Direction.RIGHT:
        return x + 1, y
    if direction == Direction.TOP:
        return x, y - 1
    if direction == Direction.BOTTOM:
        return x, y + 1
    if direction == Direction.TOPLEFT:
        return x - 1, y - 1
    if direction == Direction.BOTTOMLEFT:
        return x - 1, y + 1
    if direction == Direction.TOPRIGHT:
        return x + 1, y - 1
    if direction == Direction.BOTTOMRIGHT:
        return x + 1, y + 1
    raise ValueError("Invalid direction")
