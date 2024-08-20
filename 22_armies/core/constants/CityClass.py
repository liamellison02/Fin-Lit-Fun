from __future__ import annotations

from enum import IntEnum, auto


class CityClass(IntEnum):
    DEFAULT = 1

    @staticmethod
    def fromName(name: str) -> CityClass:
        if name not in cityClassName2Id:
            raise ValueError(f"Invalid city class name {name}")
        return cityClassName2Id[name]

    def toName(self) -> str:
        return cityClassId2Name[self]


cityClassId2Name = {}
cityClassName2Id = {}
for property in CityClass:
    cityClassId2Name[property.value] = property.name
    cityClassName2Id[property.name] = property