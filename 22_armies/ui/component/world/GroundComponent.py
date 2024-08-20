from pygame.surface import Surface

from core.constants import CellValue
from core.state import Layer, World
from tools.tilecodes import code8np
from .LayerComponent import LayerComponent
from ...theme.Theme import Theme


class GroundComponent(LayerComponent):
    def __init__(self, theme: Theme, world: World):
        super().__init__(theme, world.ground, "ground")
        self.__ground = world.ground
        self.__code2rect = self.tileset.getCode8Rects(0, 0)

    def render(self, surface: Surface):
        super().render(surface)
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()

        renderer = self.createRenderer(surface)
        cellsSlice = renderer.cellsSlice
        cellsBox = renderer.cellsBox

        # Ground / Sea
        noise = self.noise[cellsSlice]
        for dest, value, cell in renderer.cellsRel():
            rects = tilesRects[value]
            rectIndex = int(noise[cell]) % len(rects)
            surface.blit(tileset, dest, rects[rectIndex])

        # Sea borders
        neighbors = self.__ground.getAreaNeighbors8(cellsBox)
        masks = neighbors == CellValue.GROUND_SEA
        codes = code8np(masks)

        cells = self.__ground.cells[cellsSlice]
        valid = cells == CellValue.GROUND_SEA
        valid &= codes != 255
        for dest, value, cell in renderer.cellsRel(valid):
            rect = self.__code2rect[codes[cell]]
            surface.blit(tileset, dest, rect)
