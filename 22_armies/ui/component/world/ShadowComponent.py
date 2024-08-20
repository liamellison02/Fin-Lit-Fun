from pygame.surface import Surface

from core.state import Layer, GameState
from ui.layer.ShadowValue import ShadowValue
from .LayerComponent import LayerComponent
from ...theme.Theme import Theme


class ShadowComponent(LayerComponent):
    def __init__(self, theme: Theme, state: GameState, layer: Layer):
        super().__init__(theme, layer, "shadow")
        self.__state = state
        self.__shadowLayer = layer

    def render(self, surface: Surface):
        super().render(surface)
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()

        renderer = self.createRenderer(surface)
        cellsSlice = renderer.cellsSlice
        cells = self.__shadowLayer.cells[cellsSlice]

        valid = cells != ShadowValue.NONE
        for dest, value, _ in renderer.cells(valid):
            rects = tilesRects[value]
            surface.blit(tileset, dest, rects[0])
