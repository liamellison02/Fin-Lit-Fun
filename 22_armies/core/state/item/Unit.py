from typing import Dict, Any, cast

from core.constants import UnitClass
from .Item import Item


class Unit(Item):

    __slots__ = [
        "__unitClass"
    ]

    def __init__(self, unitClass: UnitClass = UnitClass.WORKER, playerId: int = 0):
        super().__init__(playerId)
        self.__unitClass = unitClass

    def __eq__(self, other) -> bool:
        if not isinstance(other, Unit):
            return False
        unit = cast(Unit, other)
        if self.__unitClass != unit.__unitClass:
            return False
        return super().__eq__(other)

    def __repr__(self) -> str:
        return self.__unitClass.toName() + str(id(self))

    @property
    def unitClass(self) -> UnitClass:
        return self.__unitClass

    # Data transfer

    def gatherData(self) -> Dict[str, Any]:
        data = super().gatherData()
        data["type"] = "unit"
        data["unitClass"] = self.__unitClass.toName()
        return data

    def takeData(self, data: Dict[str, Any]):
        self.__unitClass = UnitClass.fromName(data['unitClass'])
        super().takeData(data)
