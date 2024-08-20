from __future__ import annotations

from typing import Tuple, Optional

import numpy as np
from pygame.surface import Surface

from core.state import ILayerListener, Layer
from .LayerRenderer import LayerRenderer
from ..Component import Component
from ..IComponentListener import IComponentListener
from ...Mouse import Mouse
from ...theme.Theme import Theme
from ...theme.Tileset import Tileset


class LayerComponent(Component, ILayerListener, IComponentListener):

    def __init__(self, theme: Theme, layer: Layer, name: str):
        self.__tileset = theme.getTileset(name)
        super().__init__(theme, colorKey=self.__tileset.colorKey)

        self.__layer = layer
        self.__view = (0, 0)

        # Noise for tile generation
        generator = theme.createRandomGenerator(name)
        self.__noise = generator.integers(0, 100000, size=self.__layer.size)
        self.__noise.flags.writeable = False

        # Listener
        self.__layer.registerListener(self)

    def dispose(self):
        super().dispose()
        self.__layer.removeListener(self)

    @property
    def layer(self) -> Layer:
        return self.__layer

    @property
    def view(self) -> Tuple[int, int]:
        return self.__view

    @property
    def tileset(self) -> Tileset:
        return self.__tileset

    @property
    def noise(self) -> np.ndarray:
        return self.__noise

    def createRenderer(self, surface: Surface) -> LayerRenderer:
        tileWidth, tileHeight = self.__tileset.tileSize
        layerWidth, layerHeight = self.__layer.size
        surfaceWidth, surfaceHeight = surface.get_size()
        viewX, viewY = self.__view

        cellMinX, cellMaxX = 100000, -100000
        for x in range(0, surfaceWidth + 1, tileWidth):
            cellX = (x + viewX) // tileWidth
            if cellX < 0 or cellX >= layerWidth:
                continue
            cellMinX = min(cellMinX, cellX)
            cellMaxX = max(cellMaxX, cellX)

        cellMinY, cellMaxY = 100000, -100000
        for y in range(0, surfaceHeight + 1, tileHeight):
            cellY = (y + viewY) // tileHeight
            if cellY < 0 or cellY >= layerHeight:
                continue
            cellMinY = min(cellMinY, cellY)
            cellMaxY = max(cellMaxY, cellY)
        return LayerRenderer(self.__layer,
            cellMinX, cellMinY, cellMaxX + 1, cellMaxY + 1,
            self.__view, self.__tileset.tileSize
        )

    # Component

    def needRefresh(self) -> bool:
        return self._needRefresh

    def render(self, surface: Surface):
        self._needRefresh = False

    def findMouseFocus(self, mouse: Mouse) -> Optional[Component]:
        return None  # Never take focus

    # Layer listener

    def contentChanged(self, layer: Layer):
        self._needRefresh = True

    def cellChanged(self, layer: Layer, cell: Tuple[int, int]):
        self._needRefresh = True

    # Component listener

    def viewChanged(self, view: Tuple[int, int]):
        if view != self.__view:
            self._needRefresh = True
            self.__view = view
