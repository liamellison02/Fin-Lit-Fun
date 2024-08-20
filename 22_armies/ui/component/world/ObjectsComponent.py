from typing import cast

from pygame.surface import Surface

from core.constants import CellValue, Direction
from core.state import World, City
from tools.tilecodes import code4np
from tools.vector import vectorDivI, vectorAddI, vectorSubI
from .LayerComponent import LayerComponent
from ...theme.Theme import Theme


class ObjectsComponent(LayerComponent):
    def __init__(self, theme: Theme, world: World):
        super().__init__(theme, world.objects, "objects")
        self.__objects = world.objects
        self.__impassableLayer = world.impassable
        bridgeDirtRects = self.tileset.getTileRects("bridgeDirt")
        bridgeStoneRects = self.tileset.getTileRects("bridgeStone")
        self.__horizontalBrigdes = {
            CellValue.OBJECTS_ROAD_DIRT: bridgeDirtRects[0],
            CellValue.OBJECTS_ROAD_STONE: bridgeStoneRects[0],
        }
        self.__verticalBrigdes = {
            CellValue.OBJECTS_ROAD_DIRT: bridgeDirtRects[1],
            CellValue.OBJECTS_ROAD_STONE: bridgeStoneRects[1],
        }
        self.__roadDirt_code2rect = self.tileset.getCode4Rects(0, 3)
        self.__roadStone_code2rect = self.tileset.getCode4Rects(4, 3)
        self.debug = False

    def render(self, surface: Surface):
        super().render(surface)
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()

        renderer = self.createRenderer(surface)
        cellsSlice = renderer.cellsSlice
        cellsBox = renderer.cellsBox
        cells = self.__objects.cells[cellsSlice]
        impassableCells = self.__impassableLayer.cells[cellsSlice]

        # Default
        valid = cells != CellValue.NONE
        valid &= cells != CellValue.OBJECTS_ROAD_DIRT
        valid &= cells != CellValue.OBJECTS_ROAD_STONE
        valid &= cells != CellValue.OBJECTS_CITY
        noise = self.noise[cellsSlice]
        for dest, value, cell in renderer.cellsRel(valid):
            rects = tilesRects[value]
            rectIndex = int(noise[cell]) % len(rects)
            surface.blit(tileset, dest, rects[rectIndex])

        # Road border codes
        neighbors = self.__objects.getAreaNeighbors4(cellsBox)
        masks = neighbors == CellValue.OBJECTS_ROAD_DIRT
        masks |= neighbors == CellValue.OBJECTS_ROAD_STONE
        codes = code4np(masks)

        # Dirt roads (without bridges)
        valid = cells == CellValue.OBJECTS_ROAD_DIRT
        valid &= impassableCells != CellValue.IMPASSABLE_RIVER
        for dest, value, cell in renderer.cellsRel(valid):
            rect = self.__roadDirt_code2rect[codes[cell]]
            surface.blit(tileset, dest, rect)

        # Stone roads (without bridges)
        valid = cells == CellValue.OBJECTS_ROAD_STONE
        valid &= impassableCells != CellValue.IMPASSABLE_RIVER
        for dest, value, cell in renderer.cellsRel(valid):
            rect = self.__roadStone_code2rect[codes[cell]]
            surface.blit(tileset, dest, rect)

        # River codes
        neighbors = self.__impassableLayer.getAreaNeighbors4(cellsBox)
        codes = code4np(neighbors == CellValue.IMPASSABLE_RIVER)

        # Cells with a road and a river
        valid = cells == CellValue.OBJECTS_ROAD_DIRT
        valid |= cells == CellValue.OBJECTS_ROAD_STONE
        valid &= impassableCells == CellValue.IMPASSABLE_RIVER

        # Horizontal bridges
        horizontal = valid & (codes == 6)
        for dest, value, _ in renderer.cells(horizontal):
            rect = self.__horizontalBrigdes[value]
            surface.blit(tileset, dest, rect)

        # Vertical bridges
        vertical = valid & (codes == 9)
        for dest, value, _ in renderer.cells(vertical):
            rect = self.__verticalBrigdes[value]
            surface.blit(tileset, dest, rect)

        # Cities
        objects = self.__objects
        valid = cells == CellValue.OBJECTS_CITY
        for dest, value, cell in renderer.cells(valid):
            rects = tilesRects[value]
            item = objects.getItem(cell)
            if not isinstance(item, City):
                continue
            city = cast(City, item)
            rectIndex = city.playerId * 12
            leftValue = objects.getValue(cell, Direction.LEFT)
            topValue = objects.getValue(cell, Direction.TOP)
            if leftValue != CellValue.OBJECTS_CITY:
                if topValue != CellValue.OBJECTS_CITY:
                    surface.blit(tileset, dest, rects[rectIndex + 0])
                else:
                    surface.blit(tileset, dest, rects[rectIndex + 2])
            else:
                if topValue != CellValue.OBJECTS_CITY:
                    surface.blit(tileset, dest, rects[rectIndex + 1])
                else:
                    surface.blit(tileset, dest, rects[rectIndex + 3])

        if self.debug:  # Print codes to debug/illustrate
            from ..text.token.TextStyle import TextStyle
            textStyle = TextStyle("small", "white")
            tileSize = self.theme.getTileset("objects").tileSize
            tileSize2 = vectorDivI(tileSize, (2, 2))
            for dest, value, cell in renderer.cells():
                textSurface = textStyle.render(self.theme, codes[cell])
                textSurface.set_colorkey((0, 0, 0))
                dest = vectorAddI(dest, tileSize2)
                dest = vectorSubI(dest, vectorDivI(textSurface.get_size(), (2, 2)))
                surface.blit(textSurface, dest)