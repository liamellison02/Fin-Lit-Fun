from __future__ import annotations

from typing import Optional, cast

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from ui.theme.Theme import Theme


class TextStyle:
    PLAIN = 0
    BOLD = 1
    ITALIC = 2
    UNDERLINE = 4

    __slots__ = ["__fontName", "__colorName", "__flags"]

    def __init__(self, 
                 fontName: Optional[str] = None,
                 colorName: Optional[str] = None,
                 flags: int = 0):
        self.__fontName = fontName
        self.__colorName = colorName
        self.__flags = flags

    def clone(self) -> TextStyle:
        return TextStyle(self.__fontName, self.__colorName, self.__flags)

    @property
    def colorName(self) -> Optional[str]:
        return self.__colorName

    def styleColor(self, colorName) -> TextStyle:
        if self.colorName == colorName:
            return self
        return TextStyle(self.__fontName, colorName, self.__flags)

    @property
    def italic(self) -> bool:
        return (self.__flags & TextStyle.ITALIC) != 0

    def styleItalic(self, enable: bool = True) -> TextStyle:
        if self.italic == enable:
            return self
        if enable:
            flags = self.__flags | TextStyle.ITALIC
        else:
            flags = self.__flags & (~TextStyle.ITALIC)
        return TextStyle(self.__fontName, self.__colorName, flags)

    @property
    def bold(self) -> bool:
        return (self.__flags & TextStyle.BOLD) != 0

    def styleBold(self, enable: bool = True) -> TextStyle:
        if self.bold == enable:
            return self
        if enable:
            flags = self.__flags | TextStyle.BOLD
        else:
            flags = self.__flags & (~TextStyle.BOLD)
        return TextStyle(self.__fontName, self.__colorName, flags)

    @property
    def underline(self) -> bool:
        return (self.__flags & TextStyle.UNDERLINE) != 0

    def styleUnderline(self, enable: bool = True) -> TextStyle:
        if self.underline == enable:
            return self
        if enable:
            flags = self.__flags | TextStyle.UNDERLINE
        else:
            flags = self.__flags & (~TextStyle.UNDERLINE)
        return TextStyle(self.__fontName, self.__colorName, flags)

    def render(self, theme: Theme, text: str) -> Surface:
        font = theme.getFont(self.__fontName)
        crop = theme.getFontCrop(self.__fontName)
        font.set_bold(self.bold)
        font.set_italic(self.italic)
        color = theme.getFontColor(self.__colorName)
        surface = font.render(str(text), False, color)
        if self.underline:
            ascent = font.get_ascent()
            pygame.draw.line(
                surface, color,
                (0, ascent + 1),
                (surface.get_width(), ascent + 1)
            )
        if crop is not None:
            surface0 = surface
            width = surface0.get_width()
            height = crop[1] - crop[0]
            surface = Surface((width, height))
            area = Rect(0, crop[0], width, height)
            surface.blit(surface0, (0, 0), area)
        return surface

    def __str__(self):
        description = f"{self.__fontName} color:{self.__colorName}"
        if self.italic:
            description += " italic"
        if self.bold:
            description += " bold"
        if self.underline:
            description += " underline"
        return description

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextStyle):
            return False
        other = cast(TextStyle, other)
        return self.__fontName == other.__fontName \
               and self.__colorName == other.__colorName \
               and self.__flags == other.__flags

    def __hash__(self) -> int:
        return hash(self.__fontName) \
               + hash(self.__colorName) \
               + hash(self.__flags)
