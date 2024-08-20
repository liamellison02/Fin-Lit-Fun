import random
from typing import Tuple, Dict, cast, Optional, Any

import numpy as np

from core.state.item.Item import Item
from core.state.item.City import City


class Assignments:

    def __init__(self, size: Tuple[int, int]):
        super().__init__()
        self.__size = size
        self.__cities: Dict[Tuple[int, int], City] = {}
        self.__citiesMask = np.zeros([size[0], size[1]], dtype=bool)

    @property
    def size(self) -> Tuple[int, int]:
        return self.__size

    @property
    def width(self) -> int:
        return self.__size[0]

    @property
    def height(self) -> int:
        return self.__size[1]

    def __eq__(self, other) -> bool:
        if not isinstance(other, Assignments):
            return False
        layer = cast(Assignments, other)
        if self.__size != layer.__size:
            return False
        if len(self.__cities) != len(layer.__cities):
            return False
        for cell, item in self.__cities.items():
            if cell not in layer.__cities:
                return False
            if item != layer.__cities[cell]:
                return False
        return True

    def hasAssignment(self, cell: Tuple[int, int]) -> bool:
        if cell not in self.__cities:
            return False
        return self.__cities[cell] is not None

    def getAssignment(self, cell: Tuple[int, int]) -> City:
        assert cell in self.__cities
        return self.__cities[cell]

    def setAssignment(self, cell: Tuple[int, int], city: Optional[City] = None):
        x, y = cell[0], cell[1]
        assert 0 <= x < self.__size[0], f"Invalid x={x}"
        assert 0 <= y < self.__size[1], f"Invalid y={y}"
        if city is None:
            if cell in self.__cities:
                del self.__cities[cell]
                self.__citiesMask[cell] = False
        else:
            self.__cities[cell] = city
            self.__citiesMask[cell] = True

    # Data transfer

    def gatherData(self, items: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:

        for item in self.__cities.values():
            itemId = str(id(item))
            if itemId not in items:
                items[itemId] = item.gatherData()

        citiesCell = []
        for cell, item in self.__cities.items():
            citiesCell.append([
                cell[0], cell[1], id(item)
            ])

        return {
            "width": self.width,
            "height": self.height,
            "cities": citiesCell
        }

    def takeData(self, data: Dict[str, Any], itemsData: Dict[int, Item]):
        self.__size = (int(data["width"]), int(data["height"]))

        self.__cities = {}
        for itemData in data["cities"]:
            if type(itemData) == dict:
                x = int(itemData["x"])
                y = int(itemData["y"])
                itemId = int(itemData["id"])
            elif type(itemData) == list:
                x = int(itemData[0])
                y = int(itemData[1])
                itemId = int(itemData[2])
            else:
                raise ValueError(f"Invalid item data type {type(itemData)}")
            item = itemsData[itemId]
            assert isinstance(item, City)
            self.__cities[(x, y)] = cast(City, item)
