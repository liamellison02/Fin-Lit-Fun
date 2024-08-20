from pygame.surface import Surface
from typing import cast

from core.constants import CellValue
from core.state import World, Unit, Army
from .LayerComponent import LayerComponent
from ..text.token import TextStyle
from ...theme.Theme import Theme


class UnitsComponent(LayerComponent):
    def __init__(self, theme: Theme, world: World):
        super().__init__(theme, world.units, "units")
        self.__units = world.units
        self.__textStyle = TextStyle("small", "white")

    def render(self, surface: Surface):
        super().render(surface)
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()
        tileWidth, tileHeight = self.tileset.tileSize

        renderer = self.createRenderer(surface)
        cellsSlice = renderer.cellsSlice
        cells = self.__units.cells[cellsSlice]

        valid = cells == CellValue.UNITS_UNIT
        for dest, _, item, _ in renderer.items(valid):
            unit = cast(Unit, item)
            rects = tilesRects[unit.unitClass]
            surface.blit(tileset, dest, rects[unit.playerId])

        valid = cells == CellValue.UNITS_ARMY
        for dest, _, item, _ in renderer.items(valid):
            army = cast(Army, item)
            unit = army.findRepresentativeUnit()
            if unit is None:
                surface.blit(tileset, dest, tilesRects[CellValue.NONE][0])
            else:
                rects = tilesRects[unit.unitClass]
                surface.blit(tileset, dest, rects[unit.playerId])

            textSurface = self.__textStyle.render(self.theme, f"{len(army)}")
            textSurface.set_colorkey((0, 0, 0))
            surface.blit(textSurface, (
                dest[0] + tileWidth - textSurface.get_width(),
                dest[1] + tileHeight - textSurface.get_height()
            ))
