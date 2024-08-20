from __future__ import annotations
from enum import IntEnum


class Resource(IntEnum):
    FOOD = 1
    GOLD = 2
    STONE = 3
    WOOD = 4

    @staticmethod
    def fromName(name: str) -> Resource:
        if name not in resourceName2Id:
            raise ValueError(f"Invalid resource name {name}")
        return resourceName2Id[name]

    def toName(self) -> str:
        return resourceId2Name[self]

    def formatName(self) -> str:
        return resourceId2Name[self].lower()

Resources = {
    Resource.FOOD,
    Resource.GOLD,
    Resource.STONE,
    Resource.WOOD
}

resourceId2Name = {
    Resource.FOOD: "FOOD",
    Resource.GOLD: "GOLD",
    Resource.STONE: "STONE",
    Resource.WOOD: "WOOD"
}

resourceName2Id = {
    "FOOD": Resource.FOOD,
    "GOLD": Resource.GOLD,
    "STONE": Resource.STONE,
    "WOOD": Resource.WOOD
}
