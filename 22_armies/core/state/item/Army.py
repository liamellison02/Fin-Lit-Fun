from itertools import compress
from typing import Dict, Any, cast, List, Optional

from .Item import Item
from .Unit import Unit
from ...constants import ItemProperty


class Army(Item):
    __slots__ = [
        "__units"
    ]

    def __init__(self, playerId: int = 0):
        super().__init__(playerId)
        self.__units: List[Unit] = []

    def __eq__(self, other) -> bool:
        if not isinstance(other, Army):
            return False
        army = cast(Army, other)
        if self.__units != army.__units:
            return False
        return super().__eq__(other)

    def __repr__(self) -> str:
        return "Army"

    def __len__(self) -> int:
        return len(self.__units)

    @property
    def units(self) -> List[Unit]:
        return self.__units

    def addUnit(self, unit: Unit):
        self.__units.append(unit)

    def removeUnits(self, selection: List[bool]):
        self.__units = list(compress(self.__units, selection))

    def findRepresentativeUnit(self) -> Optional[Unit]:
        counts = {}
        bestCount = 0
        bestUnit = None
        for unit in self.__units:
            unitClass = unit.unitClass
            if unitClass not in counts:
                counts[unitClass] = 1
            else:
                counts[unitClass] += 1
            if counts[unitClass] > bestCount:
                bestCount = counts[unitClass]
                bestUnit = unit
            elif counts[unitClass] == bestCount:
                if bestUnit is None or unitClass > bestUnit.unitClass:
                    bestUnit = unit
        return bestUnit

    def getLowestIntProperty(self, prop: ItemProperty, defaultValue: Optional[int] = None,
                             selection: List[Unit] = None) -> Optional[int]:
        lowest = None
        for index, unit in enumerate(self.__units):
            if selection and unit not in selection:
                continue
            value = unit.getIntProperty(prop, defaultValue)
            if lowest is None:
                lowest = value
            else:
                lowest = min(lowest, value)
        return lowest

    # Data transfer

    def gatherData(self) -> Dict[str, Any]:
        data = super().gatherData()
        data["type"] = "army"
        data["units"] = [unit.gatherData() for unit in self.__units]
        return data

    def takeData(self, data: Dict[str, Any]):
        self.__units.clear()
        for unitData in data["units"]:
            unit = Unit()
            unit.takeData(unitData)
            self.__units.append(unit)
        super().takeData(data)
