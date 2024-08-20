from pygame.surface import Surface

from ..Component import Component
from ..text import TextRenderer
from ...theme.Theme import Theme


class Label(Component):

    def __init__(self, theme: Theme, message: str = ""):
        self.__textRenderer = TextRenderer(theme, "small")
        surface = self.__textRenderer.render(message)
        self.__surface = surface
        super().__init__(theme, surface.get_size())

    def setMessage(self, message: str):
        surface = self.__textRenderer.render(message)
        self.__surface = surface
        self.resize(surface.get_size())

    def render(self, surface: Surface):
        surface.blit(self.__surface, self.topLeft)
        self._needRefresh = False