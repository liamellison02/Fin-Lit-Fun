from typing import Optional, Tuple, cast

import numpy as np
import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from core.constants import cellValueRanges, CellValue
from core.state import World, ILayerListener, Layer, Unit
from tools.vector import vectorSubI, vectorAddI, vectorMulI, vectorClampI, vectorSubHalfI
from .FrameComponent import FrameComponent
from ...Mouse import Mouse
from ...theme.Theme import Theme


class MinimapFrame(FrameComponent, ILayerListener):

    def __init__(self, theme: Theme, world: World):
        super().__init__(theme, (64, 48))
        self.__world = world
        self.__view = (0, 0)
        self.__minimapCoords = (0, 0)
        self.__tileSize = theme.getTileset("ground").tileSize
        self.__minimapSurface: Optional[Surface] = None
        self.__viewShift = (0, 0)

        self.__colors = {}
        for name in ["ground", "impassable", "objects"]:
            tileset = theme.getTileset(name)
            valueRange = cellValueRanges[name]
            self.__colors[name] = tileset.getTilesColor(valueRange)

        # Layers listener
        for layer in self.__world.layers:
            layer.registerListener(self)

    def dispose(self):
        super().dispose()
        for layer in self.__world.layers:
            layer.removeListener(self)

    def __renderMinimap(self, cellsBox: Optional[Tuple[int, int, int, int]] = None):
        layers = zip(
            reversed(self.__world.layerNames),
            reversed(self.__world.layers)
        )

        if self.__minimapSurface is None or cellsBox is None:
            cellMinX, cellMaxX = 0, self.__world.width
            cellMinY, cellMaxY = 0, self.__world.height
        else:
            cellMinX, cellMaxX, cellMinY, cellMaxY = cellsBox
        cellsSlice = np.s_[cellMinX:cellMaxX, cellMinY:cellMaxY]
        minimapArray = np.zeros(
            [cellMaxX - cellMinX, cellMaxY - cellMinY, 4],
            dtype=np.int32
        )

        for name, layer in layers:
            cells = layer.cells[cellsSlice]
            if name == "units":
                playerColors = self.theme.playerColors
                validCells = cells == CellValue.UNITS_UNIT
                cellCoords = np.transpose(np.nonzero(validCells))
                for cell in cellCoords:
                    cellX = int(cellMinX + cell[0])
                    cellY = int(cellMinY + cell[1])
                    item = layer.getItem((cellX, cellY))
                    if item is not None:
                        unit = cast(Unit, item)
                        color = playerColors[unit.playerId]
                        minimapArray[cell[0], cell[1], :] = color
            else:
                colorMap = self.__colors[name]
                colors = colorMap[cells]
                transparent = minimapArray[..., 3] == 0
                minimapArray[transparent] = colors[transparent]

        minimapArea = pygame.surfarray.make_surface(minimapArray[..., 0:3]).convert()
        if self.__minimapSurface is None:
            self.__minimapSurface = minimapArea
        else:
            self.__minimapSurface.blit(minimapArea, (cellMinX, cellMinY))

    def update(self):
        view = vectorAddI(self.__view, self.__viewShift)
        worldSize = vectorMulI(self.__world.size, self.theme.defaulTileSize)
        maxView = vectorSubI(worldSize, self.theme.viewSize)
        view = vectorClampI(view, 0, maxView)
        if view != self.__view:
            self.notifyViewChanged(view)

    def render(self, surface: Surface):
        super().render(surface)

        # Compute the whole minimap
        if self.__minimapSurface is None:
            self.__renderMinimap()

        # Create a temporary surface to draw the minimap and rectangle
        innerArea = self.innerArea
        tempSurface = Surface(innerArea.size)
        tempSurface.set_colorkey((0, 0, 0))

        # Compute the location of the minimap and the view rectangle in the temporary surface
        def computeCoord(areaSize, worldSize, viewCoord, viewSize):
            if areaSize >= worldSize:  # Enough space to draw the whole map
                minimap = (areaSize - worldSize) // 2
                rect = minimap + viewCoord
            else:  # Not enough space
                rect = (areaSize - viewSize) // 2
                minimap = rect - viewCoord
                if minimap > 0:
                    rect -= minimap
                    minimap = 0
                minimapMin = areaSize - worldSize
                if minimap < minimapMin:
                    rect += minimapMin - minimap
                    minimap = minimapMin
            return minimap, rect

        tileWidth, tileHeight = self.__tileSize
        worldWidth, worldHeight = self.__world.size
        viewX = self.__view[0] // tileWidth
        viewY = self.__view[1] // tileHeight
        viewWidth = self.theme.viewSize[0] // tileWidth
        viewHeight = self.theme.viewSize[1] // tileHeight
        minimapX, rectX = computeCoord(innerArea.width, worldWidth, viewX, viewWidth)
        minimapY, rectY = computeCoord(innerArea.height, worldHeight, viewY, viewHeight)
        self.__minimapCoords = (minimapX, minimapY)

        # Draw minimap & view rectangle in the temporary surface
        if self.__minimapSurface is not None:
            tempSurface.blit(self.__minimapSurface, self.__minimapCoords)
        viewRect = Rect(rectX, rectY, viewWidth, viewHeight)
        pygame.draw.rect(tempSurface, (255, 255, 255), viewRect, width=1)

        # Draw the temporary surface (contains clipped minimap + view rectangle)
        surface.blit(tempSurface, innerArea.topleft)

    # UI Event handler

    def __updateViewShift(self, mouse: Mouse) -> bool:
        if not mouse.button1:
            return True
        innerArea = self.innerArea
        if not innerArea.collidepoint(mouse.pixel):
            return True
        self.__viewShift = vectorSubI(mouse.pixel, innerArea.center)
        return True

    def mouseButtonDown(self, mouse: Mouse) -> bool:
        if not mouse.button1:
            return True
        innerArea = self.innerArea
        if not innerArea.collidepoint(mouse.pixel):
            return True
        # Convert mouse pixel coordinates to pixel relative to minimap top left corner
        # Since one minimap pixel = cell, these coordinates are world cell coordinates
        cell = vectorSubI(mouse.pixel, innerArea.topleft)
        cell = vectorSubI(cell, self.__minimapCoords)
        if not self.__world.contains(cell):
            return True
        # Convert cell coordinates into pixel coordinates
        view = vectorMulI(cell, self.__tileSize)
        # Center so the cursor in the middle of the view
        view = vectorSubHalfI(view, self.theme.viewSize)
        worldSize = vectorMulI(self.__world.size, self.__tileSize)
        maxView = vectorSubI(worldSize, self.theme.viewSize)
        view = vectorClampI(view, 0, maxView)
        if view != self.__view:
            self.notifyViewChanged(view)
        return self.__updateViewShift(mouse)

    def mouseMove(self, mouse: Mouse) -> bool:
        return self.__updateViewShift(mouse)

    def mouseButtonUp(self, mouse: Mouse, speed: float=1.0) -> bool:
        self.__viewShift = (0, 0)
        return True

    def mouseLeave(self) -> bool:
        super().mouseLeave()
        self.__viewShift = (0, 0)
        return True

    # Component listener

    def viewChanged(self, view: Tuple[int, int]):
        if view != self.__view:
            self.__view = view

    # Layer listener

    def cellChanged(self, layer: Layer, cell: Tuple[int, int]):
        cellX, cellY = cell
        cellMinX, cellMaxX = max(cellX, 0), min(cellX + 1, layer.width)
        cellMinY, cellMaxY = max(cellY, 0), min(cellY + 1, layer.height)
        self.__renderMinimap((cellMinX, cellMaxX, cellMinY, cellMaxY))
