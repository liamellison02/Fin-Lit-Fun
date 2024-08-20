from __future__ import annotations

from enum import IntEnum


class UnitClass(IntEnum):
    NONE = 0
    WORKER = 1
    FARMER = 2
    BOWMAN = 3
    PIKEMAN = 4
    SWORDSMAN = 5
    KNIGHT = 6
    CATAPULT = 7

    @staticmethod
    def fromName(name: str) -> UnitClass:
        try:
            return UnitClass[name]
        except KeyError:
            raise ValueError(f"Invalid cell unit class {name}")

    def toName(self) -> str:
        return self.name

    def formatName(self) -> str:
        return unitClassStr[self]


unitClassStr = {
    UnitClass.WORKER: "Worker",
    UnitClass.FARMER: "Farmer",
    UnitClass.BOWMAN: "Bowman",
    UnitClass.PIKEMAN: "Pikeman",
    UnitClass.SWORDSMAN: "Swordsman",
    UnitClass.KNIGHT: "Knight",
    UnitClass.CATAPULT: "Catapult"
}

