from typing import Tuple, Optional, List

import numpy as np

from core.constants import CellValue
from core.state import Layer


class LayerRenderer:

    def __init__(self,
                 layer: Layer,
                 cellMinX: int, cellMinY: int, cellMaxX: int, cellMaxY: int,
                 view: Tuple[int, int], tileSize: Tuple[int, int]):
        self.layer = layer
        self.view = view
        self.tileSize = tileSize
        self.cellsBox = (cellMinX, cellMinY, cellMaxX, cellMaxY)
        self.cellsSlice = np.s_[cellMinX:cellMaxX, cellMinY:cellMaxY]

    @property
    def topLeft(self) -> Tuple[int, int]:
        return self.cellsBox[0], self.cellsBox[1]

    def computeDest(self, cell: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        x, y = cell
        cellMinX, cellMinY, cellMaxX, cellMaxY = self.cellsBox
        if x < cellMinX or x >= cellMaxX or y < cellMinY or y >= cellMaxY:
            return None
        tileWidth, tileHeight = self.tileSize
        viewX, viewY = self.view
        return (
            (x - cellMinX) * tileWidth - viewX % tileWidth,
            (y - cellMinY) * tileHeight - viewY % tileHeight
        )

    def cells(self, validCells: Optional[np.ndarray] = None):
        tileWidth, tileHeight = self.tileSize
        viewX, viewY = self.view
        cellMinX, cellMinY, cellMaxX, cellMaxY = self.cellsBox
        if validCells is None:
            cells = self.layer.cells
            shiftX = cellMinX * tileWidth + viewX % tileWidth
            shiftY = cellMinY * tileHeight + viewY % tileHeight
            for cellY in range(cellMinY, cellMaxY):
                for cellX in range(cellMinX, cellMaxX):
                    value = int(cells[cellX, cellY])
                    destX = cellX * tileWidth - shiftX
                    destY = cellY * tileHeight - shiftY
                    yield (destX, destY), value, (cellX, cellY)
        else:
            cells = self.layer.cells[self.cellsSlice]
            cellCoords = np.transpose(np.nonzero(validCells))
            for cell in cellCoords:
                cellRelX = int(cell[0])
                cellRelY = int(cell[1])
                value = int(cells[cellRelX, cellRelY])
                destX = cellRelX * tileWidth - viewX % tileWidth
                destY = cellRelY * tileHeight - viewY % tileHeight
                yield (destX, destY), value, (cellRelX + cellMinX, cellRelY + cellMinY)

    def cellsRel(self, validCells: Optional[np.ndarray] = None):
        tileWidth, tileHeight = self.tileSize
        viewX, viewY = self.view
        if validCells is None:
            cells = self.layer.cells
            cellMinX, cellMinY, cellMaxX, cellMaxY = self.cellsBox
            shiftX = cellMinX * tileWidth + viewX % tileWidth
            shiftY = cellMinY * tileHeight + viewY % tileHeight
            for cellY in range(cellMinY, cellMaxY):
                for cellX in range(cellMinX, cellMaxX):
                    value = int(cells[cellX, cellY])
                    destX = cellX * tileWidth - shiftX
                    destY = cellY * tileHeight - shiftY
                    yield (destX, destY), value, (cellX - cellMinX, cellY - cellMinY)
        else:
            cells = self.layer.cells[self.cellsSlice]
            cellCoords = np.transpose(np.nonzero(validCells))
            for cell in cellCoords:
                cellRelX = int(cell[0])
                cellRelY = int(cell[1])
                value = int(cells[cellRelX, cellRelY])
                destX = cellRelX * tileWidth - viewX % tileWidth
                destY = cellRelY * tileHeight - viewY % tileHeight
                yield (destX, destY), value, (cellRelX, cellRelY)

    def items(self, validCells: Optional[np.ndarray] = None):
        tileWidth, tileHeight = self.tileSize
        viewX, viewY = self.view
        if validCells is None:
            cells = self.layer.cells
            cellMinX, cellMinY, cellMaxX, cellMaxY = self.cellsBox
            shiftX = cellMinX * tileWidth + viewX % tileWidth
            shiftY = cellMinY * tileHeight + viewY % tileHeight
            for cellY in range(cellMinY, cellMaxY):
                for cellX in range(cellMinX, cellMaxX):
                    cell = (cellX, cellY)
                    item = self.layer.getItem(cell)
                    if item is None:
                        continue
                    value = int(cells[cellX, cellY])
                    destX = cellX * tileWidth - shiftX
                    destY = cellY * tileHeight - shiftY
                    yield (destX, destY), value, item, cell
        else:
            cells = self.layer.cells[self.cellsSlice]
            cellCoords = np.transpose(np.nonzero(validCells))
            cellMinX, cellMinY, cellMaxX, cellMaxY = self.cellsBox
            for cell in cellCoords:
                cellRelX = int(cell[0])
                cellRelY = int(cell[1])
                cellX = cellMinX + cellRelX
                cellY = cellMinY + cellRelY
                item = self.layer.getItem((cellX, cellY))
                if item is None:
                    continue
                value = int(cells[cellRelX, cellRelY])
                destX = cellRelX * tileWidth - viewX % tileWidth
                destY = cellRelY * tileHeight - viewY % tileHeight
                yield (destX, destY), value, item, (cellX, cellY)
