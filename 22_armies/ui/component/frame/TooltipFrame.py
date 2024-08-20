from typing import Tuple, Optional

from pygame.surface import Surface

from tools.vector import vectorAddI
from .FrameComponent import FrameComponent
from .. import Component
from ..text.TextRenderer import TextRenderer
from ... import Mouse
from ...theme.Theme import Theme


class TooltipFrame(FrameComponent):

    def __init__(self, theme: Theme, message: str, maxWidth: int = 300):
        super().__init__(theme)
        self.__update(message, maxWidth)
        self.__show = True

    def __update(self, message: str, maxWidth: int):
        textRenderer = TextRenderer(self.theme, "small", maxWidth)
        self.__messageSurface = textRenderer.render(message)
        size = self.__messageSurface.get_size()
        borderSize = 2 * self.theme.framePadding
        size = vectorAddI(size, (borderSize, borderSize))
        self.resize(size)

    def setMessage(self, message: str, maxWidth: int = 300):
        self.__update(message, maxWidth)

    def show(self):
        self.__show = True

    def hide(self):
        self.__show = False

    def findMouseFocus(self, mouse: Mouse) -> Optional[Component]:
        return None

    def mouseEnter(self, mouse: Mouse) -> bool:
        return False

    def mouseLeave(self) -> bool:
        return False

    def render(self, surface: Surface):
        if not self.__show:
            return
        super().render(surface)
        x, y = self.innerArea.topleft
        surface.blit(self.__messageSurface, (x, y))



