from enum import IntEnum


class MoveCost(IntEnum):
    ROAD_STONE = 1,
    ROAD_DIRT = 2,
    GROUND = 3,
    OBJECTS = 4,
    INFINITE = 10000
