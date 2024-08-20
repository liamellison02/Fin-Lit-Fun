from typing import Tuple

from pygame.surface import Surface

from core.constants import CellValue, ItemProperty
from core.logic import Rules
from .LayerComponent import LayerComponent
from ...theme.Theme import Theme


class ResourcesComponent(LayerComponent):
    def __init__(self, theme: Theme, rules: Rules, cityPos: Tuple[int, int]):
        super().__init__(theme, rules.state.world.objects, "selection")
        self.__rules = rules
        self.__cityCell = rules.getCityTopLeft(cityPos)
        self.__city = rules.getCity(cityPos)
        self.__resourcesTileset = theme.getTileset("resources")

    def render(self, surface: Surface):
        super().render(surface)
        mainTileSize = self.tileset.tileSize
        tileset = self.__resourcesTileset.surface
        tileSize = self.__resourcesTileset.tileSize
        tilesRects = self.__resourcesTileset.getTilesRects()

        renderer = self.createRenderer(surface)
        cellsSlice = renderer.cellsSlice
        cellMinX, cellMinY, _, _ = renderer.cellsBox
        cells = self.layer.cells[cellsSlice]

        rules = self.__rules
        city = self.__city
        valid = cells == CellValue.OBJECTS_CITY
        for dest, _, item, cell in renderer.items(valid):
            if item != city:
                continue
            resources = rules.computeCellResources(city, cell)

            if len(resources) < 5:
                shiftX = mainTileSize[0] // 2
                shiftY = mainTileSize[1] // 2
            else:
                shiftX = mainTileSize[0] // 3
                shiftY = mainTileSize[1] // 3

            x, y = 1, mainTileSize[1] - shiftY
            for resource in resources:
                rect = tilesRects[resource][0]
                surface.blit(tileset, (dest[0] + x, dest[1] + y), rect)
                x += shiftX
                if (x + tileSize[0]) >= mainTileSize[0]:
                    x = 1
                    y -= shiftY

        cityCell = self.__cityCell
        valid = cells == CellValue.OBJECTS_CITY
        for dest, _, item, cell in renderer.items(valid):
            if item != city or cell != cityCell:
                continue
            resources = city.getResourcesListProperty(ItemProperty.BASE_PRODUCTION, [])
            shiftX = mainTileSize[0] // 2
            shiftY = mainTileSize[1] // 2
            x, y = 1, 2 * mainTileSize[1] - shiftY
            for resource in resources:
                rect = tilesRects[resource][0]
                surface.blit(tileset, (dest[0] + x, dest[1] + y), rect)
                x += shiftX
                if (x + tileSize[0]) >= 2*mainTileSize[0]:
                    x = 1
                    y -= shiftY


