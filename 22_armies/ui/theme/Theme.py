import os
from typing import Dict, Tuple, Union, Optional, List, cast, Any

import numpy as np
import pygame
from pygame.color import Color
from pygame.font import Font
from pygame.surface import Surface

from .Tileset import Tileset
from .tiledef import impassableTiledef, objectsTiledef, frameTiledef, groundTiledef, \
    unitsTiledef, selectionTiledef, initSelectionTiledef, shadowTiledef, resourcesTiledef


class Theme:
    def __init__(self) -> None:
        self.__viewSize = (1024, 768)

        # Tilesets
        self.__surfaces: Dict[str, Surface] = {}
        self.__tilesets: Dict[str, Tileset] = {}
        for name, tilesDef in tilesDefs.items():
            tileset = Tileset(self, tilesDef["tileSize"], tilesDef["imageFile"], tilesDef["colorKey"])
            tileset.addTiles(tilesDef["tiles"])
            self.__tilesets[name] = tileset
        self.__defaultTileSize = self.__tilesets["ground"].tileSize

        self.__framePadding = self.__tilesets["frame"].tileSize[0]
        self.__frameMargin = self.__tilesets["frame"].tileSize[0] // 2
        self.__playerColors = [
            (128, 128, 128, 255),
            (0, 0, 255, 255),
            (255, 0, 0, 255),
            (255, 255, 0, 255),
            (64, 255, 64, 255),
        ]

        # Text
        self.__fontsDef: Dict[str, Dict[str, Any]] = {
            "default": {
                "file": "font/pixeltype/Pixeltype.ttf",
                "size": 16,
                "crop": None
            },
            "small": {
                "file": "font/lilliputsteps/lilliputsteps.ttf",
                "size": 8,
                "crop": (3, 8)
            }
        }
        self.__colors = {
            "background": Color(180, 130, 90)
        }
        self.__fontColors = {
            "default": Color(100, 75, 50),
            "warning": Color(200, 50, 35),
            "white": Color(255, 255, 255),
            "blue": Color(0, 0, 200),
            "red": Color(255, 0, 0)
        }
        self.__fonts: Dict[Tuple[str, object], Font] = {}

    @property
    def framePadding(self) -> int:
        return self.__framePadding

    @property
    def frameMargin(self) -> int:
        return self.__frameMargin

    @property
    def defaulTileSize(self) -> Tuple[int, int]:
        return self.__defaultTileSize

    @property
    def viewSize(self) -> Tuple[int, int]:
        return self.__viewSize

    @viewSize.setter
    def viewSize(self, size: Tuple[int, int]):
        self.__viewSize = size

    @property
    def playerColors(self) -> List[Tuple[int, int, int, int]]:
        return self.__playerColors

    @property
    def backgroundColor(self) -> Color:
        return self.__colors["background"]

    def init(self):
        # Add numbers to selection tileset
        initSelectionTiledef(self.__tilesets["selection"])

    def createRandomGenerator(self, seedStr: str) -> np.random.Generator:
        seed = sum(map(ord, seedStr))
        return np.random.default_rng(seed)

    def getSurface(self, imageFile: str, colorKey: Optional[Tuple[int, int, int]] = (0, 0, 0)) -> Surface:
        if imageFile not in self.__surfaces:
            fullPath = os.path.join("assets", imageFile)
            if not os.path.exists(fullPath):
                raise ValueError(f"No file '{fullPath}'")
            surface = pygame.image.load(fullPath)
            if colorKey is not None:
                surface = surface.convert()
                surface.set_colorkey(colorKey)
            else:
                surface = surface.convert_alpha()
            self.__surfaces[imageFile] = surface
        return self.__surfaces[imageFile]

    def getTileset(self, name: str) -> Tileset:
        if name not in self.__tilesets:
            raise ValueError(f"No tileset {name}")
        return self.__tilesets[name]

    def getMouseCursor(self, playerId: int) -> Surface:
        tileset = self.getTileset("frame")
        tile = tileset.getTile("cursor", playerId)
        tile = pygame.transform.scale(tile, (32, 32))
        return tile

    def getFont(self, name: Optional[str] = None) -> Font:
        if name is None:
            name = "default"
        if name not in self.__fontsDef:
            raise ValueError("No font {}".format(name))
        fontDef = self.__fontsDef[name]
        file = os.path.join("assets", str(fontDef["file"]))
        size = cast(int, fontDef["size"])
        fontId = file, size
        if fontId not in self.__fonts:
            self.__fonts[fontId] = pygame.font.Font(file, size)
        return self.__fonts[fontId]

    def getFontCrop(self, name: Optional[str] = None) -> Union[None, Tuple[int, int]]:
        if name is None:
            name = "default"
        if name not in self.__fontsDef:
            raise ValueError("No font {}".format(name))
        fontDef = self.__fontsDef[name]
        return fontDef["crop"]

    def getFontColor(self, name: Optional[str] = None) -> Color:
        if name is None:
            name = "default"
        if name not in self.__fontColors:
            raise ValueError("No font color {}".format(name))
        return self.__fontColors[name]


tilesDefs = {
    "ground": groundTiledef,
    "impassable": impassableTiledef,
    "objects": objectsTiledef,
    "units": unitsTiledef,
    "frame": frameTiledef,
    "resources": resourcesTiledef,
    "shadow": shadowTiledef,
    "selection": selectionTiledef,
}
