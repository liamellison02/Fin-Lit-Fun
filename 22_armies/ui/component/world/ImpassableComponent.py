import numpy as np
from pygame.surface import Surface

from core.constants import CellValue, directions4, Direction
from core.state import Layer, World
from tools.tilecodes import code4np
from .LayerComponent import LayerComponent
from ...theme.Theme import Theme


class ImpassableComponent(LayerComponent):
    def __init__(self, theme: Theme, world: World):
        super().__init__(theme, world.impassable, "impassable")
        self.__ground = world.ground
        self.__impassable = world.impassable
        self.__river_code2rect = self.tileset.getCode4Rects(0, 1)
        self.__riverMouth = {
            Direction.LEFT: self.tileset.getTileRect("riverMouthLeft"),
            Direction.RIGHT: self.tileset.getTileRect("riverMouthRight"),
            Direction.TOP: self.tileset.getTileRect("riverMouthTop"),
            Direction.BOTTOM: self.tileset.getTileRect("riverMouthBottom"),
        }

    def render(self, surface: Surface):
        super().render(surface)
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()

        renderer = self.createRenderer(surface)
        cellsSlice = renderer.cellsSlice
        cellsBox = renderer.cellsBox
        cells = self.__impassable.cells[cellsSlice]

        # Default
        valid = cells != CellValue.NONE
        valid &= cells != CellValue.IMPASSABLE_RIVER
        noise = self.noise[cellsSlice]
        for dest, value, cell in renderer.cellsRel(valid):
            rects = tilesRects[value]
            rectIndex = int(noise[cell]) % len(rects)
            surface.blit(tileset, dest, rects[rectIndex])

        # Rivers
        neighbors = self.__impassable.getAreaNeighbors4(cellsBox)
        masks = neighbors == CellValue.IMPASSABLE_RIVER
        masks |= neighbors == CellValue.IMPASSABLE_MOUNTAIN
        groundNeighbors = self.__ground.getAreaNeighbors4(cellsBox)
        masks |= groundNeighbors == CellValue.GROUND_SEA
        codes = code4np(masks)

        valid = cells == CellValue.IMPASSABLE_RIVER
        for dest, _, cell in renderer.cellsRel(valid):
            rect = self.__river_code2rect[codes[cell]]
            surface.blit(tileset, dest, rect)

        # River mouths
        groundCells = self.__ground.cells[cellsSlice]
        valid = cells == CellValue.NONE
        valid &= groundCells == CellValue.GROUND_SEA
        codes = code4np(neighbors == CellValue.IMPASSABLE_RIVER)
        valid &= codes != 0
        cellMinX, cellMinY, _, _ = renderer.cellsBox
        for dest, _, cell in renderer.cells(valid):
            for direction in directions4:
                value = self.__impassable.getValue(cell, direction)
                if value == CellValue.IMPASSABLE_RIVER:
                    rect = self.__riverMouth[direction]
                    surface.blit(tileset, dest, rect)
