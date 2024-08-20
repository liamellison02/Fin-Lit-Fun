from __future__ import annotations

from typing import Dict, Tuple, TYPE_CHECKING, Union, Optional, List, cast

import numpy as np
import pygame
from pygame.surface import Surface
from pygame.rect import Rect

from core.constants import CellValue
from tools.tilecodes import tilecodes4, decode8, simplify8, code8
from tools.tilecodes import tilecodes8

if TYPE_CHECKING:
    from .Theme import Theme


class Tileset:
    def __init__(self, theme: Theme, tileSize: Tuple[int, int],
                 imageFile: str, colorKey: Optional[Tuple[int, int, int]] = None):
        self.__theme = theme
        self.__tileSize = tileSize
        self.__imageFile = imageFile
        self.__colorKey = colorKey
        self.__surface: Optional[Surface] = None
        self.__tilesRects: Dict[Union[int, str], List[Rect]] = {}

    @property
    def theme(self) -> Theme:
        return self.__theme

    @property
    def colorKey(self) -> Optional[Tuple[int, int, int]]:
        return self.__colorKey

    @property
    def tileSize(self) -> Tuple[int, int]:
        return self.__tileSize

    @property
    def surface(self) -> Surface:
        if self.__surface is None:
            self.__surface = self.__theme.getSurface(self.__imageFile, self.__colorKey)
        return self.__surface

    def addTile(self, value: Union[int, str],
                coords: Union[Tuple[int, int], Tuple[int, int, int, int]]):
        if value not in self.__tilesRects:
            self.__tilesRects[value] = []

        if len(coords) == 4:
            coords = cast(Tuple[int, int, int, int], coords)
            size = (coords[2], coords[3])
        else:
            size = (1, 1)

        self.__tilesRects[value].append(Rect(
            coords[0] * self.__tileSize[0],
            coords[1] * self.__tileSize[1],
            size[0] * self.__tileSize[0],
            size[1] * self.__tileSize[1]
        ))

    def addTiles(self, tilesDefs: Dict[Union[int, str], Union[List[Tuple[int, int]], Tuple[int, int]]]):
        for value, coords in tilesDefs.items():
            if type(coords) == list:
                for coord in coords:
                    self.addTile(value, coord)
            elif type(coords) == tuple:
                self.addTile(value, coords)
            else:
                raise ValueError(f"Invalid coordinates {coords}")

    def hasTileRects(self, value: Union[int, str]) -> bool:
        return value in self.__tilesRects

    def getTileRects(self, value: Union[int, str]) -> List[Rect]:
        if value not in self.__tilesRects:
            raise ValueError(f"No {value} in tileset {self.__imageFile}")
        return self.__tilesRects[value]

    def getTileRect(self, value: Union[int, str]) -> Rect:
        return self.getTileRects(value)[0]

    def getTile(self, value: Union[int, str], index: int = 0) -> Surface:
        rect = self.getTileRects(value)[index]
        surface = Surface(rect.size)
        surface.blit(self.surface, (0, 0), rect)
        surface.set_colorkey((0, 0, 0))
        return surface

    def getTilesColor(self, valueRange: Tuple[int, int]) -> np.ndarray:
        colors = np.zeros([CellValue.MAX_VALUE, 4], dtype=np.int32)
        for value in range(valueRange[0], valueRange[1]):
            if value not in self.__tilesRects:
                raise ValueError("No tile definition for value {}".format(value))
            rects = self.__tilesRects[value]
            tile = self.surface.subsurface(rects[0])
            array = pygame.surfarray.array3d(tile)
            count = np.count_nonzero((array != 0).any(axis=2))
            if count > 0:
                color = array.reshape(-1, 3).sum(axis=0) / count
                colors[value, 0:3] = color
                colors[value, 3] = 255
        return colors

    def blitTile(self, surface: Surface, dest: Tuple[int, int], value: Union[int, str]):
        rect = self.getTileRect(value)
        surface.blit(surface, dest, rect)

    def getTilesId(self) -> List[Union[int, str]]:
        return list(self.__tilesRects.keys())

    def getTilesRect(self) -> Dict[Union[int, str], Rect]:
        return {value: tileRects[0] for value, tileRects in self.__tilesRects.items()}

    def getTilesRects(self) -> Dict[Union[int, str], List[Rect]]:
        return self.__tilesRects

    def getCode4Rects(self, shiftX: int, shiftY: int) -> List[Rect]:
        code2rect = []
        tileWidth, tileHeight = self.tileSize
        for code in range(16):
            tile = tilecodes4[code]
            code2rect.append(Rect(
                (tile[0] + shiftX) * tileWidth,
                (tile[1] + shiftY) * tileHeight,
                tileWidth, tileHeight
            ))
        return code2rect

    def getCode8Rects(self, shiftX: int, shiftY: int) -> List[Rect]:
        code2rect = []
        tileWidth, tileHeight = self.tileSize
        for code in range(256):
            if code in tilecodes8:
                tile = tilecodes8[code]
            else:
                mask = decode8(code)
                mask = simplify8(mask)
                code = code8(mask)
                tile = tilecodes8[code]
            code2rect.append(Rect(
                (tile[0] + shiftX) * tileWidth,
                (tile[1] + shiftY) * tileHeight,
                tileWidth, tileHeight
            ))
        return code2rect
