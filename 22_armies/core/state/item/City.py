from typing import Dict, Any, cast, Tuple, Set

from core.constants import CityClass, ItemProperty
from .Item import Item


class City(Item):
    __slots__ = [
        "__cityClass", "__cells"
    ]

    def __init__(self, cityClass: CityClass = CityClass.DEFAULT, playerId: int = 0):
        super().__init__(playerId)
        self.__cells: Set[Tuple[int, int]] = set()
        self.__cityClass = cityClass

    def __eq__(self, other) -> bool:
        if not isinstance(other, City):
            return False
        city = cast(City, other)
        if self.__cells != city.__cells:
            return False
        if self.__cityClass != city.__cityClass:
            return False
        return super().__eq__(other)

    def __repr__(self) -> str:
        return f"City {self.getStringProperty(ItemProperty.NAME, 'NoName')}"

    @property
    def name(self) -> str:
        return self.getStringProperty(ItemProperty.NAME, 'NoName')

    @property
    def cells(self) -> Set[Tuple[int, int]]:
        return self.__cells

    def getCitizenCount(self) -> int:
        return self.getIntProperty(ItemProperty.CITIZEN_COUNT, 0)

    def getWorkerCount(self) -> int:
        return self.getIntProperty(ItemProperty.WORKER_COUNT, 0)

    def getMerchantCount(self) -> int:
        return self.getCitizenCount() - self.getWorkerCount()

    def isAssigned(self, cell: Tuple[int, int]) -> bool:
        return cell in self.__cells

    def assign(self, cell: Tuple[int, int]):
        if cell not in self.__cells:
            self.__cells.add(cell)

    def unassign(self, cell: Tuple[int, int]):
        if cell in self.__cells:
            self.__cells.remove(cell)

    # Data transfer

    def gatherData(self) -> Dict[str, Any]:
        data = super().gatherData()
        data["type"] = "city"
        data["cityClass"] = self.__cityClass.toName()
        data["cells"] = [cell for cell in self.__cells]
        return data

    def takeData(self, data: Dict[str, Any]):
        super().takeData(data)
        self.__cityClass = CityClass.fromName(data['cityClass'])
        self.__cells.clear()
        for cell in data["cells"]:
            self.__cells.add((int(cell[0]), int(cell[1])))
