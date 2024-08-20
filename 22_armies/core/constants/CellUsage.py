from __future__ import annotations

from enum import IntEnum


class CellUsage(IntEnum):
    NONE = 0

    HOUSE = 1
    WORKER = 2
    PRODUCTION_BUILDING = 3
    TRAINING_CAMP = 4
