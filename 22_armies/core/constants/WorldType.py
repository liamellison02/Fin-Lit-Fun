from __future__ import annotations

from enum import IntEnum, auto


class WorldType(IntEnum):
    STRATEGIC=auto()
    TACTIC=auto()

    @staticmethod
    def fromName(name: str) -> WorldType:
        if name not in worldTypeName2Id:
            raise ValueError(f"Invalid world type name {name}")
        return worldTypeName2Id[name]

    def toName(self) -> str:
        return worldTypeId2Name[self]


worldTypeId2Name = {}
worldTypeName2Id = {}
for property in WorldType:
    worldTypeId2Name[property.value] = property.name
    worldTypeName2Id[property.name] = property
    