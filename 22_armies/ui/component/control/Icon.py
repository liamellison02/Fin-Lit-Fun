from pygame.surface import Surface

from ..Component import Component
from ...theme.Theme import Theme


class Icon(Component):

    def __init__(self, theme: Theme,
                 surface: Surface):
        self.__tile = surface
        super().__init__(theme, surface.get_size())

    def render(self, surface: Surface):
        surface.blit(self.__tile, self.topLeft)
        self._needRefresh = False
