from pygame.rect import Rect
from pygame.surface import Surface

from .TextToken import TextToken


class IconTextToken(TextToken):

    __slots__ = ["__tileset", "__tile"]

    def __init__(self, tileset: Surface, tile: Rect):
        self.__tileset = tileset
        self.__tile = tile

    @property
    def tileset(self) -> Surface:
        return self.__tileset

    @property
    def tile(self) -> Rect:
        return self.__tile

