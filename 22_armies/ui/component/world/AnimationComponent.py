from typing import Optional, Tuple, List

from pygame.surface import Surface

from core.state import Layer, GameState
from ui.layer.SelectionValue import SelectionValue
from .LayerComponent import LayerComponent
from .LayerRenderer import LayerRenderer
from ..text.token import TextStyle
from ... import Mouse
from ...theme.Theme import Theme


class AnimationComponent(LayerComponent):
    def __init__(self, theme: Theme, state: GameState, layer: Layer):
        super().__init__(theme, layer, "selection")
        self.__state = state
        self.__textStyle = TextStyle("small", "red")

        self.__damageCell: Optional[Tuple[int, int]] = None
        self.__damage = 0
        self.__damageShift = 0

        self.__graveCells: List[Tuple[Tuple[int, int], int]] = []

    def addDamage(self, cell: Tuple[int, int], damage: int):
        self.__damage = damage
        self.__damageCell = cell
        self.__damageShift = 0

    def addGrave(self, cell: Tuple[int, int]):
        self.__graveCells.append((cell, 0))

    def __renderDamage(self, surface: Surface, renderer: LayerRenderer):
        if self.__damageCell is None:
            return
        dest = renderer.computeDest(self.__damageCell)
        if dest is None:
            return
        x, y = dest
        tileWidth, tileHeight = self.tileset.tileSize
        textSurface = self.__textStyle.render(self.theme, f"-{self.__damage}")
        textSurface.set_colorkey((0, 0, 0))
        surface.blit(textSurface, (
            x + (tileWidth - textSurface.get_width()) // 2,
            y + (tileHeight - textSurface.get_height()) // 2 - self.__damageShift
        ))
        self.__damageShift += 1
        if self.__damageShift > 2 * tileHeight:
            self.__damageCell = None

    def __renderGrave(self, surface: Surface, renderer: LayerRenderer):
        newGraveCells = []
        for graveCell in self.__graveCells:
            dest = renderer.computeDest(graveCell[0])
            if dest is None:
                return
            rect = self.tileset.getTileRect(SelectionValue.GRAVE)
            surface.blit(self.tileset.surface, dest, rect)
            graveTime = graveCell[1] + 1
            if graveTime < 100:
                newGraveCells.append((graveCell[0], graveTime))
        self.__graveCells = newGraveCells

    def render(self, surface: Surface):
        super().render(surface)
        renderer = self.createRenderer(surface)
        self.__renderGrave(surface, renderer)
        self.__renderDamage(surface, renderer)


