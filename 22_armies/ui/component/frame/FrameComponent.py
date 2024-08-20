from __future__ import annotations

from typing import Optional, Tuple

from pygame.rect import Rect
from pygame.surface import Surface

from ..CompositeComponent import CompositeComponent
from ...IUIEventHandler import IUIEventHandler
from ...Mouse import Mouse
from ...MouseWheel import MouseWheel
from ...theme.Theme import Theme


class FrameComponent(CompositeComponent, IUIEventHandler):

    def __init__(self, theme: Theme,
                 size: Optional[Tuple[int, int]] = None):
        super().__init__(theme, size)
        self.__tileset = tileset = theme.getTileset("frame")
        self.__topLeftTile = tileset.getTileRect("topLeft")
        self.__topTile = tileset.getTileRect("top")
        self.__topRightTile = tileset.getTileRect("topRight")
        self.__leftTile = tileset.getTileRect("left")
        self.__centerTile = tileset.getTileRect("center")
        self.__rightTile = tileset.getTileRect("right")
        self.__bottomLeftTile = tileset.getTileRect("bottomLeft")
        self.__bottomTile = tileset.getTileRect("bottom")
        self.__bottomRightTile = tileset.getTileRect("bottomRight")

    @property
    def innerArea(self) -> Rect:
        x, y = self.topLeft
        w, h = self.size
        s = self.theme.framePadding
        return Rect(x + s, y + s, w - 2*s, h - 2*s)

    def _drawFrame(self, surface: Surface, dest: Optional[Tuple[int, int]] = None):
        if dest is None:
            x1, y1 = self.topLeft
        else:
            x1, y1 = dest
        width, height = self.size

        tileWidth, tileHeight = self.__tileset.tileSize
        x1b = x1 + tileWidth
        x2b = x1 + width - tileWidth
        y1b = y1 + tileHeight
        y2b = y1 + height - tileHeight

        tilesetSurface = self.__tileset.surface
        surface.blit(tilesetSurface, (x1, y1), self.__topLeftTile)
        for x in range(x1b, x2b, tileWidth):
            surface.blit(tilesetSurface, (x, y1), self.__topTile)
        surface.blit(tilesetSurface, (x2b, y1), self.__topRightTile)

        for y in range(y1b, y2b, tileHeight):
            surface.blit(tilesetSurface, (x1, y), self.__leftTile)
        for y in range(y1b, y2b, tileHeight):
            for x in range(x1b, x2b, tileWidth):
                surface.blit(tilesetSurface, (x, y), self.__centerTile)
        for y in range(y1b, y2b, tileHeight):
            surface.blit(tilesetSurface, (x2b, y), self.__rightTile)

        surface.blit(tilesetSurface, (x1, y2b), self.__bottomLeftTile)
        for x in range(x1b, x2b, tileWidth):
            surface.blit(tilesetSurface, (x, y2b), self.__bottomTile)
        surface.blit(tilesetSurface, (x2b, y2b), self.__bottomRightTile)

    def render(self, surface: Surface):
        self._drawFrame(surface)
        super().render(surface)
        self._needRefresh = False

    # UI Event Handler

    def mouseEnter(self, mouse: Mouse) -> bool:
        super().mouseEnter(mouse)
        return True

    def mouseLeave(self) -> bool:
        super().mouseLeave()
        return True

    def mouseButtonDown(self, mouse: Mouse) -> bool:
        super().mouseButtonDown(mouse)
        return True

    def mouseButtonUp(self, mouse: Mouse) -> bool:
        super().mouseButtonUp(mouse)
        return True

    def mouseWheel(self, mouse: Mouse, wheel: MouseWheel) -> bool:
        super().mouseWheel(mouse, wheel)
        return True

    def mouseMove(self, mouse: Mouse) -> bool:
        super().mouseMove(mouse)
        return True
