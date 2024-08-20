from typing import cast, Optional, List, Tuple

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from .TextTokenizer import TextTokenizer
from .token import ReturnTextToken, ContentTextToken, IconTextToken, StyleTextToken, SpaceTextToken, TextStyle, \
    AlignTextToken
from ...theme.Theme import Theme


class TextRenderer:

    def __init__(self, theme: Theme, fontName: Optional[str] = None,
                 maxWidth: int = 0):
        self.__theme = theme
        self.__tokenizer = TextTokenizer(theme)
        self.__style = TextStyle(fontName)
        if maxWidth == 0:
            maxWidth = theme.viewSize[0] - 2 * theme.framePadding
        self.__maxWidth = maxWidth

    def render(self, message: str) -> Surface:
        tokens = self.__tokenizer.parse(message, self.__style)

        # Compute text surfaces and final surface size
        blits: List[Tuple[Surface, Tuple[int, int], Optional[Rect]]] = []
        x, y = 0, 0
        currentStyle = self.__style
        maxWidth = self.__maxWidth
        surfaceWidth, surfaceHeight = 0, 0
        spaceWidth = currentStyle.render(self.__theme, " ").get_width()
        for token in tokens:
            if isinstance(token, ContentTextToken):
                contentToken = cast(ContentTextToken, token)
                words = contentToken.content.split()
                for index, word in enumerate(words):
                    surface = currentStyle.render(self.__theme, word)
                    height = surface.get_height()
                    surfaceHeight = max(surfaceHeight, y + height)
                    if x + surface.get_width() + 1 >= maxWidth:
                        x, y = 0, surfaceHeight + 2
                        surfaceHeight = max(surfaceHeight, y + height)
                    blits.append((cast(pygame.Surface, surface), (x, surfaceHeight - height), None))
                    x += surface.get_width() + 1
                    if index < len(words) - 1:
                        x += spaceWidth
                    surfaceWidth = max(surfaceWidth, x)
            elif isinstance(token, IconTextToken):
                iconToken = cast(IconTextToken, token)
                surface = iconToken.tileset
                rect = iconToken.tile
                if x + rect.width + 1 >= maxWidth:
                    x, y = 0, surfaceHeight + 2
                blits.append((surface, (x, y), rect))
                x += rect.width + 1
                surfaceHeight = max(surfaceHeight, y + rect.height)
            elif isinstance(token, ReturnTextToken):
                if y == surfaceHeight + 2:
                    spaceHeight = currentStyle.render(self.__theme, " ").get_height()
                    surfaceHeight += spaceHeight
                x, y = 0, surfaceHeight + 2
            elif isinstance(token, SpaceTextToken):
                spaceToken = cast(SpaceTextToken, token)
                x += spaceWidth * spaceToken.count
            elif isinstance(token, AlignTextToken):
                alignToken = cast(AlignTextToken, token)
                newX = spaceWidth * alignToken.x
                if newX > x:
                    x = newX
            elif isinstance(token, StyleTextToken):
                styleToken = cast(StyleTextToken, token)
                currentStyle = styleToken.style
            else:
                raise ValueError("Invalid token")
            surfaceWidth = max(surfaceWidth, x)

        # Build the final surface
        textSurface = Surface((surfaceWidth, surfaceHeight))
        textSurface.set_colorkey((0, 0, 0))
        for blit in blits:
            textSurface.blit(*blit)

        return textSurface
