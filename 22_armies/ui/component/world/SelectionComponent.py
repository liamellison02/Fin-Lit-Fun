from typing import Optional, Tuple, cast

from pygame.surface import Surface

from core.logic import DistanceMap
from core.state import Layer, GameState
from tools.vector import vectorSubI
from ui.layer.SelectionValue import SelectionValue
from .LayerComponent import LayerComponent
from .LayerRenderer import LayerRenderer
from ..text.token import TextStyle
from ...layer import SelectionItem
from ...theme.Theme import Theme


class SelectionComponent(LayerComponent):
    def __init__(self, theme: Theme, state: GameState, layer: Layer):
        super().__init__(theme, layer, "selection")
        self.__state = state
        self.__selectionLayer = layer
        self.__resourcesTileset = theme.getTileset("resources")
        self.__damageCell: Optional[Tuple[int, int]] = None
        self.__damage = 0
        self.__damageShift = 0
        self.__showAssignedTiles = True

        # Debug / Illustrate
        self.__textStyle = TextStyle("small", "white")
        self.__distanceMap: Optional[DistanceMap] = None
        self.__movePoints: Optional[int] = None
        self.__showMode = 0

    def addDamage(self, cell: Tuple[int, int], damage: int):
        self.__damage = damage
        self.__damageCell = cell
        self.__damageShift = 0

    def render(self, surface: Surface):
        super().render(surface)
        tileset = self.tileset.surface
        tileSize = self.tileset.tileSize
        tilesRects = self.tileset.getTilesRects()
        resourcesTileset = self.__resourcesTileset.surface
        resourcesTileSize = self.__resourcesTileset.tileSize
        resourcesTileRects = self.__resourcesTileset.getTilesRects()

        renderer = self.createRenderer(surface)
        cellsSlice = renderer.cellsSlice
        layer = self.__selectionLayer
        cells = layer.cells[cellsSlice]

        valid = cells == SelectionValue.SELECTED
        valid |= cells == SelectionValue.SELECTED2
        currentPlayerId = self.__state.playerId
        for dest, value, _ in renderer.cells(valid):
            rect = tilesRects[value][currentPlayerId]
            dest = vectorSubI(dest, tileSize)
            surface.blit(tileset, dest, rect)

        valid = cells != SelectionValue.NONE
        valid &= cells != SelectionValue.SELECTED
        valid &= cells != SelectionValue.SELECTED2
        for dest, value, cell in renderer.cells(valid):
            rects = tilesRects[value]
            if len(rects) == 1:
                rect = rects[0]
            else:
                rect = rects[currentPlayerId]
            surface.blit(tileset, dest, rect)

            item = layer.getItem(cell)
            if item is None:
                continue
            selectionItem = cast(SelectionItem, item)
            resources = selectionItem.resources
            if value == SelectionValue.ASSIGNED2:
                shiftX = tileSize[0] // 2
                shiftY = tileSize[1] // 2
                x, y = 1, 2 * tileSize[1] - shiftY
                for resource in resources:
                    rect = resourcesTileRects[resource][0]
                    surface.blit(resourcesTileset, (dest[0] + x, dest[1] + y), rect)
                    x += shiftX
                    if (x + resourcesTileSize[0]) >= 2 * tileSize[0]:
                        x = 1
                        y -= shiftY
            else:
                if len(resources) < 5:
                    shiftX = tileSize[0] // 2
                    shiftY = tileSize[1] // 2
                else:
                    shiftX = tileSize[0] // 3
                    shiftY = tileSize[1] // 3

                x, y = 1, tileSize[1] - shiftY
                for resource in resources:
                    rect = resourcesTileRects[resource][0]
                    surface.blit(resourcesTileset, (dest[0] + x, dest[1] + y), rect)
                    x += shiftX
                    if (x + resourcesTileSize[0]) >= tileSize[0]:
                        x = 1
                        y -= shiftY

        # Debug / Illustrate
        if self.__distanceMap is None:
            return
        if self.__showMode == 1:
            self.__showEdges(surface, renderer)
        elif self.__showMode == 2:
            self.__showMap(surface, renderer)

    # Debug / Illustrate

    def setDistanceMap(self, distanceMap: Optional[DistanceMap], movePoints: Optional[int] = None):
        self.__distanceMap = distanceMap
        self.__movePoints = movePoints

    def rollShowMode(self):
        self.__showMode += 1
        if self.__showMode > 2:
            self.__showMode = 0
        self._needRefresh = True

    def __showMap(self, surface: Surface, renderer: LayerRenderer):
        if self.__distanceMap is None:
            return
        map = self.__distanceMap.map
        ax1, ay1, ax2, ay2 = self.__distanceMap.area
        cellMinX, cellMinY = renderer.topLeft
        print(ax1, ay1, "=>", cellMinX, cellMinY)

        textStyle = TextStyle("small", "white")
        tileWidth, tileHeight = self.theme.getTileset("ground").tileSize
        for dest, value, cell in renderer.cells():
            x, y = cell
            if x < ax1 or y < ay1 or x >= ax2 or y >= ay2:
                continue
            mapX, mapY = x - ax1, y - ay1
            x, y = dest
            value = map[mapX, mapY]
            if value < 100:
                textSurface = textStyle.render(self.theme, value)
                textSurface.set_colorkey((0, 0, 0))
                surface.blit(textSurface, (
                    x + (tileWidth - textSurface.get_width()) // 2,
                    y + (tileHeight - textSurface.get_height()) // 2
                ))

    def __showEdges(self, surface: Surface, renderer: LayerRenderer):
        if self.__distanceMap is None:
            return

        edges = self.__distanceMap.edges
        ax1, ay1, ax2, ay2 = self.__distanceMap.area
        cellMinX, cellMinY = renderer.topLeft

        textStyle = TextStyle("small", "white")
        tileWidth, tileHeight = self.theme.getTileset("ground").tileSize
        for dest, value, cell in renderer.cells():
            x, y = cell
            if x < ax1 or y < ay1 or x >= ax2 or y >= ay2:
                continue
            mapX, mapY = x - ax1, y - ay1
            x, y = dest
            # Top Left
            value = edges[mapX, mapY, 0]
            if value < 10:
                textSurface = textStyle.render(self.theme, value)
                textSurface.set_colorkey((0, 0, 0))
                surface.blit(textSurface, (
                    x - 1,
                    y
                ))
            # Left
            value = edges[mapX, mapY, 1]
            if value < 10:
                textSurface = textStyle.render(self.theme, value)
                textSurface.set_colorkey((0, 0, 0))
                surface.blit(textSurface, (
                    x - 1,
                    y + (tileHeight - textSurface.get_height()) // 2
                ))
            # Bottom Left
            value = edges[mapX, mapY, 2]
            if value < 10:
                textSurface = textStyle.render(self.theme, value)
                textSurface.set_colorkey((0, 0, 0))
                surface.blit(textSurface, (
                    x - 1,
                    y + tileHeight - textSurface.get_height()
                ))
            # Top
            value = edges[mapX, mapY, 3]
            if value < 10:
                textSurface = textStyle.render(self.theme, value)
                textSurface.set_colorkey((0, 0, 0))
                surface.blit(textSurface, (
                    x + (tileWidth - textSurface.get_width()) // 2,
                    y
                ))
            # Bottom
            value = edges[mapX, mapY, 4]
            if value < 10:
                textSurface = textStyle.render(self.theme, value)
                textSurface.set_colorkey((0, 0, 0))
                surface.blit(textSurface, (
                    x + (tileWidth - textSurface.get_width()) // 2,
                    y + tileHeight - textSurface.get_height()
                ))
            # Top Right
            value = edges[mapX, mapY, 5]
            if value < 10:
                textSurface = textStyle.render(self.theme, value)
                textSurface.set_colorkey((0, 0, 0))
                surface.blit(textSurface, (
                    x + tileWidth - textSurface.get_width(),
                    y
                ))
            # Right
            value = edges[mapX, mapY, 6]
            if value < 10:
                textSurface = textStyle.render(self.theme, value)
                textSurface.set_colorkey((0, 0, 0))
                surface.blit(textSurface, (
                    x + tileWidth - textSurface.get_width(),
                    y + (tileHeight - textSurface.get_height()) // 2
                ))
            # Bottom Right
            value = edges[mapX, mapY, 7]
            if value < 10:
                textSurface = textStyle.render(self.theme, value)
                textSurface.set_colorkey((0, 0, 0))
                surface.blit(textSurface, (
                    x + tileWidth - textSurface.get_width(),
                    y + tileHeight - textSurface.get_height()
                ))


