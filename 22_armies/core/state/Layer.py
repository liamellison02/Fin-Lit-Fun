import random
from typing import Tuple, Optional, Dict, Any, cast, List, Union

import numpy as np

from .ILayerListener import ILayerListener
from .item.Item import Item
from ..Listenable import Listenable
from ..constants import Direction, CellValue


class ItemCells:
    __slots__ = ["item", "cells"]

    def __init__(self, item: Item):
        self.item = item
        self.cells: List[Tuple[int, int]] = []


class Layer(Listenable[ILayerListener]):
    def __init__(self, size: Tuple[int, int], defaultValue: int = 0):
        super().__init__()
        self.__size = size
        self.__defaultValue = int(defaultValue)
        self.__cells = np.full([size[0] + 2, size[1] + 2], defaultValue, dtype=np.int32)
        self.__items: Dict[Tuple[int, int], Item] = {}
        self.__itemsMask = np.zeros([size[0], size[1]], dtype=bool)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Layer):
            return False
        layer = cast(Layer, other)
        if self.__size != layer.__size:
            return False
        if self.__defaultValue != layer.__defaultValue:
            return False
        if not np.array_equal(self.__cells, layer.__cells):
            return False
        if len(self.__items) != len(layer.__items):
            return False
        for coords, item in self.__items.items():
            if coords not in layer.__items:
                return False
            if item != layer.__items[coords]:
                return False
        return True

    @property
    def size(self) -> Tuple[int, int]:
        return self.__size

    @property
    def width(self) -> int:
        return self.__size[0]

    @property
    def height(self) -> int:
        return self.__size[1]

    @property
    def cells(self) -> np.ndarray:
        return self.__cells[1:-1, 1:-1]

    def contains(self, coords: Tuple[int, int]) -> bool:
        return 0 <= coords[0] < self.__size[0] and 0 <= coords[1] < self.__size[1]

    def __getitem__(self, coords: Tuple[int, int]) -> int:
        return self.getValue(coords)

    def getValue(self, coords: Tuple[int, int], direction: Optional[Direction] = None) -> int:
        x, y = coords[0], coords[1]
        w, h = self.__size
        assert 0 <= x < w, f"Invalid x={x}"
        assert 0 <= y < h, f"Invalid y={y}"
        if direction and direction != Direction.NONE:
            if direction == Direction.LEFT:
                return int(self.__cells[x, y + 1])
            if direction == Direction.RIGHT:
                return int(self.__cells[x + 2, y + 1])
            if direction == Direction.TOP:
                return int(self.__cells[x + 1, y])
            if direction == Direction.BOTTOM:
                return int(self.__cells[x + 1, y + 2])
            if direction == Direction.TOPLEFT:
                return int(self.__cells[x, y])
            if direction == Direction.BOTTOMLEFT:
                return int(self.__cells[x, y + 2])
            if direction == Direction.TOPRIGHT:
                return int(self.__cells[x + 2, y])
            if direction == Direction.BOTTOMRIGHT:
                return int(self.__cells[x + 2, y + 2])
        return int(self.__cells[x + 1, y + 1])

    def __setitem__(self, coords: Tuple[int, int], value: int):
        self.setValue(coords, value)

    def setValue(self, coords: Tuple[int, int], value: int):
        x, y = coords[0], coords[1]
        assert 0 <= x < self.__size[0], f"Invalid x={x}"
        assert 0 <= y < self.__size[1], f"Invalid y={y}"
        self.__cells[x + 1, y + 1] = value
        if value == CellValue.NONE:
            if coords in self.__items:
                del self.__items[coords]
                self.__itemsMask[coords] = False

    def fill(self, value: int):
        self.__cells[1:-1, 1:-1] = value

    def findValues(self, valueOrList: Union[int, List[int]]) -> List[Tuple[int, int]]:
        if type(valueOrList) == int or type(valueOrList) == CellValue:
            value = int(valueOrList)
            cells = np.argwhere(self.__cells == value) - 1
            result = [(cell[0], cell[1]) for cell in list(cells)]
        elif type(valueOrList) == list:
            valueList = cast(list, valueOrList)
            result = []
            for value in valueList:
                cells = np.argwhere(self.__cells == value) - 1
                result.extend([(cell[0], cell[1]) for cell in list(cells)])
        else:
            raise ValueError(f"Invalid value type {type(valueOrList)}")
        return result

    def getNeighbors4(self, cell: Tuple[int, int]) -> Tuple[int, int, int, int]:
        x, y = cell
        return int(self.__cells[x, y + 1]), \
            int(self.__cells[x + 1, y]), \
            int(self.__cells[x + 1, y + 2]), \
            int(self.__cells[x + 2, y + 1])

    def getArea(self, area: Tuple[int, int, int, int]) -> np.ndarray:
        minX, minY, maxX, maxY = area
        return self.__cells[minX + 1:maxX + 1, minY + 1:maxY + 1]

    def __computeAreaIntersection(self, pos: Tuple[int, int], array: np.ndarray) -> \
            Optional[Tuple[int, int, int, int, int, int, int, int]]:
        destWidth = int(self.__cells.shape[0])
        destHeight = int(self.__cells.shape[1])
        sourceWidth = int(array.shape[0])
        sourceHeight = int(array.shape[1])

        destMinX = int(pos[0]) + 1
        destMinY = int(pos[1]) + 1
        destMaxX = destMinX + sourceWidth
        destMaxY = destMinY + sourceHeight

        sourceMinX = 0
        sourceMinY = 0
        sourceMaxX = sourceWidth
        sourceMaxY = sourceHeight

        if destMinX >= destWidth or destMaxX <= 0 \
                or destMinY >= destHeight or destMaxY <= 0:
            return None

        if destMinX < 0:
            sourceMinX -= destMinX
            destMinX = 0

        if destMinY < 0:
            sourceMinY -= destMinY
            destMinY = 0

        if destMaxX > destWidth:
            sourceMaxX -= destMaxX - destWidth
            destMaxX = destWidth

        if destMaxY > destHeight:
            sourceMaxY -= destMaxY - destHeight
            destMaxY = destHeight
        return sourceMinX, sourceMaxX, sourceMinY, sourceMaxY, \
            destMinX, destMaxX, destMinY, destMaxY

    def computeAreaIntersection(self, pos: Tuple[int, int], array: np.ndarray) -> \
            Optional[Tuple[int, int, int, int, int, int]]:
        intersection = self.__computeAreaIntersection(pos, array)
        if intersection is None:
            return None
        sourceMinX, sourceMaxX, sourceMinY, sourceMaxY, \
            destMinX, destMaxX, destMinY, destMaxY = intersection
        return sourceMinX, sourceMinY, destMinX - 1, destMinY - 1, sourceMaxX - sourceMinX, sourceMaxY -sourceMinY

    def blit(self, pos: Tuple[int, int], array: np.ndarray):
        intersection = self.__computeAreaIntersection(pos, array)
        if intersection is None:
            return
        sourceMinX, sourceMaxX, sourceMinY, sourceMaxY, \
            destMinX, destMaxX, destMinY, destMaxY = intersection
        self.__cells[destMinX:destMaxX, destMinY:destMaxY] = \
            array[sourceMinX:sourceMaxX, sourceMinY:sourceMaxY]

    def compare(self, pos: Tuple[int, int], value: int, mask: np.ndarray) -> Tuple[Tuple[int, int], np.ndarray]:
        intersection = self.__computeAreaIntersection(pos, mask)
        if intersection is None:
            return pos, np.array([])
        sourceMinX, sourceMaxX, sourceMinY, sourceMaxY, \
            destMinX, destMaxX, destMinY, destMaxY = intersection
        result = self.__cells[destMinX:destMaxX, destMinY:destMaxY] == value
        return (destMinX, destMaxX), result & (mask[sourceMinX:sourceMaxX, sourceMinY:sourceMaxY] != 0)

    def getAllNeighbors4(self) -> np.ndarray:
        w, h = self.__size
        top = self.__cells[1:w + 1, 0:h]
        left = self.__cells[0:w, 1:h + 1]
        right = self.__cells[2:w + 2, 1:h + 1]
        bottom = self.__cells[1:w + 1, 2:h + 2]
        return np.stack((left, top, bottom, right), axis=2)

    def getAreaNeighbors4(self, cellsBox: Tuple[int, int, int, int]) -> np.ndarray:
        minX, minY, maxX, maxY = cellsBox
        top = self.__cells[minX + 1:maxX + 1, minY:maxY]
        left = self.__cells[minX:maxX, minY + 1:maxY + 1]
        right = self.__cells[minX + 2:maxX + 2, minY + 1:maxY + 1]
        bottom = self.__cells[minX + 1:maxX + 1, minY + 2:maxY + 2]
        return np.stack((left, top, bottom, right), axis=2)

    def getNeighbors8(self, cell: Tuple[int, int]) -> Tuple[int, int, int, int, int, int, int, int]:
        x, y = cell
        n = np.delete(self.__cells[x:x + 3, y:y + 3].flatten(), 4)
        return int(n[0]), int(n[1]), int(n[2]), int(n[3]), \
            int(n[4]), int(n[5]), int(n[6]), int(n[7])

    def getAreaNeighbors8(self, cellsBox: Tuple[int, int, int, int]) -> np.ndarray:
        minX, minY, maxX, maxY = cellsBox
        topLeft = self.__cells[minX:maxX, minY:maxY]
        top = self.__cells[minX + 1:maxX + 1, minY:maxY]
        topRight = self.__cells[minX + 2:maxX + 2, minY:maxY]
        left = self.__cells[minX:maxX, minY + 1:maxY + 1]
        right = self.__cells[minX + 2:maxX + 2, minY + 1:maxY + 1]
        bottomLeft = self.__cells[minX:maxX, minY + 2:maxY + 2]
        bottom = self.__cells[minX + 1:maxX + 1, minY + 2:maxY + 2]
        bottomRight = self.__cells[minX + 2:maxX + 2, minY + 2:maxY + 2]
        return np.stack((topLeft, left, bottomLeft, top,
                         bottom, topRight, right, bottomRight), axis=2)

    def getAllNeighbors8(self) -> np.ndarray:
        w, h = self.__size
        topLeft = self.__cells[0:w, 0:h]
        top = self.__cells[1:w + 1, 0:h]
        topRight = self.__cells[2:w + 2, 0:h]
        left = self.__cells[0:w, 1:h + 1]
        right = self.__cells[2:w + 2, 1:h + 1]
        bottomLeft = self.__cells[0:w, 2:h + 2]
        bottom = self.__cells[1:w + 1, 2:h + 2]
        bottomRight = self.__cells[2:w + 2, 2:h + 2]
        return np.stack((topLeft, left, bottomLeft, top,
                         bottom, topRight, right, bottomRight), axis=2)

    # Items

    def hasItem(self, coords: Tuple[int, int]) -> bool:
        if coords not in self.__items:
            return False
        return self.__items[coords] is not None

    def getItem(self, coords: Tuple[int, int]) -> Optional[Item]:
        if coords not in self.__items:
            return None
        return self.__items[coords]

    def setItem(self, coords: Tuple[int, int], item: Optional[Item] = None):
        x, y = coords[0], coords[1]
        assert 0 <= x < self.__size[0], f"Invalid x={x}"
        assert 0 <= y < self.__size[1], f"Invalid y={y}"
        if item is None:
            if coords in self.__items:
                del self.__items[coords]
                self.__itemsMask[coords] = False
        else:
            self.__items[coords] = item
            self.__itemsMask[coords] = True

    def getItems(self) -> List[ItemCells]:
        items: List[ItemCells] = []
        found: Dict[int, int] = {}
        for cell, item in self.__items.items():
            id_ = id(item)
            if id_ not in found:
                found[id_] = len(items)
                items.append(ItemCells(item))
            items[found[id_]].cells.append(cell)
        return items

    def getItemsArea(self, area: Tuple[int, int, int, int]) -> List[ItemCells]:
        minX, minY, maxX, maxY = area
        cells = self.__cells[minX + 1:maxX + 1, minY + 1:maxY + 1]
        cells = np.argwhere(cells != CellValue.NONE).tolist()
        items: List[ItemCells] = []
        found: Dict[int, int] = {}
        for cell in cells:
            cell = (cell[0] + minX, cell[1] + minY)
            if cell not in self.__items:
                continue
            item = self.__items[cell]
            id_ = id(item)
            if id_ not in found:
                found[id_] = len(items)
                items.append(ItemCells(item))
            items[found[id_]].cells.append(cell)
        return items

    def getItemsByValue(self, value: int) -> List[ItemCells]:
        cells = np.argwhere(self.__cells == value).tolist()
        items: List[ItemCells] = []
        found: Dict[int, int] = {}
        for cell in cells:
            cell = (cell[0] - 1, cell[1] - 1)
            if cell not in self.__items:
                continue
            item = self.__items[cell]
            id_ = id(item)
            if id_ not in found:
                found[id_] = len(items)
                items.append(ItemCells(item))
            items[found[id_]].cells.append(cell)
        return items

    def getItemsByPlayers(self, playerId: int) -> List[ItemCells]:
        items: List[ItemCells] = []
        found: Dict[int, int] = {}
        for cell, item in self.__items.items():
            if item.playerId == playerId:
                id_ = id(item)
                if id_ not in found:
                    found[id_] = len(items)
                    items.append(ItemCells(item))
                items[found[id_]].cells.append(cell)
        return items

    # Layer listener

    def notifyContentChanged(self):
        for listener in self.listeners:
            listener.contentChanged(self)

    def notifyCellChanged(self, cell: Tuple[int, int]):
        for listener in self.listeners:
            listener.cellChanged(self, cell)

    # Data transfer

    def gatherData(self, items: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        randomShift = random.randint(0, 100)  # This is only for checking
        cellsValues = {
            str(self.__defaultValue + randomShift): CellValue(self.__defaultValue).toName()
        }
        for value in np.unique(self.__cells):
            cellsValues[str(value + randomShift)] = CellValue(value).toName()

        nonzeroX, nonzeroY = np.nonzero(self.__cells != self.__defaultValue)
        if len(nonzeroX) >= 0.1 * self.__cells.size:
            cellsData = {
                "format": "dense",
                "data": (self.__cells + randomShift).tolist(),
                "values": cellsValues
            }
        else:
            data = []
            for x, y in zip(nonzeroX, nonzeroY):
                value = self.__cells[x, y] + randomShift
                data.append([int(x), int(y), int(value)])
            cellsData = {
                "format": "sparse",
                "data": data,
                "values": cellsValues
            }

        for item in self.__items.values():
            itemId = str(id(item))
            if itemId not in items:
                items[itemId] = item.gatherData()

        itemsCell = []
        for coords, item in self.__items.items():
            itemsCell.append([
                coords[0], coords[1], id(item)
            ])

        return {
            "width": self.width,
            "height": self.height,
            "defaultValue": int(self.__defaultValue),
            "cells": cellsData,
            "items": itemsCell,
        }

    def takeData(self, data: Dict[str, Any], itemsData: Dict[int, Item]):
        cellsData = data["cells"]
        self.__size = (int(data["width"]), int(data["height"]))
        self.__defaultValue = int(data["defaultValue"])
        if cellsData["format"] == "dense":
            denseData = cellsData["data"]
            assert len(denseData) == self.width + 2
            assert len(denseData[0]) == self.height + 2
            self.__cells = np.array(denseData, dtype=np.int32)
        elif cellsData["format"] == "sparse":
            self.__cells = np.full([self.width + 2, self.height + 2], self.__defaultValue, dtype=np.int32)
            for sparseData in cellsData["data"]:
                x = int(sparseData[0])
                y = int(sparseData[1])
                value = int(sparseData[2])
                self.__cells[x, y] = value

        cellsValues = cellsData["values"]
        for serialKey, serialValue in cellsValues.items():
            serialId = int(serialKey)
            value = CellValue.fromName(serialValue)
            self.__cells[self.__cells == serialId] = value

        self.__items = {}
        for itemData in data["items"]:
            if type(itemData) == dict:
                x = int(itemData["x"])
                y = int(itemData["y"])
                itemId = itemData["id"]
            elif type(itemData) == list:
                x = int(itemData[0])
                y = int(itemData[1])
                itemId = itemData[2]
            else:
                raise ValueError(f"Invalid item data type {type(itemData)}")
            if itemId not in itemsData:
                raise ValueError(f"Invalid item id {itemId}")
            self.__items[(x, y)] = itemsData[itemId]


