from typing import Optional

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from tools.vector import vectorMulI
from .FrameComponent import FrameComponent
from ..text.TextRenderer import TextRenderer
from ...theme.Theme import Theme


class MessageFrame(FrameComponent):

    def __init__(self, theme: Theme, message: str, portrait: Optional[str] = None):
        frameBorderSize = theme.framePadding
        maxWidth = 300 - 2 * frameBorderSize
        self.__portraitSurface: Optional[Surface] = None
        if portrait is not None:
            tileset = theme.getTileset("frame")
            tile = tileset.getTile(portrait)
            size = vectorMulI(tile.get_size(), (4, 4))
            self.__portraitSurface = pygame.transform.scale(tile, size)
            maxWidth -= self.__portraitSurface.get_width()
            height = self.__portraitSurface.get_height()
            height += 2 * theme.framePadding
        else:
            width, height = 0, 64

        textRenderer = TextRenderer(theme, "default", maxWidth)
        self.__messageSurface = textRenderer.render(message)

        super().__init__(theme, (300, height))

    def render(self, surface: Surface):
        super().render(surface)
        frameBorderSize = self.theme.framePadding
        x, y = self.innerArea.topleft
        if self.__portraitSurface is not None:
            portraitArea = Rect((x, y), self.__portraitSurface.get_size())
            surface.fill(self.theme.backgroundColor, portraitArea)
            surface.blit(self.__portraitSurface, (x, y))
            x += self.__portraitSurface.get_width()
            x += frameBorderSize
            if self.__messageSurface.get_height() < self.__portraitSurface.get_height():
                y += (self.__portraitSurface.get_height() - self.__messageSurface.get_height()) // 2
        surface.blit(self.__messageSurface, (x, y))



