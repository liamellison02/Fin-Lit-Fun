from typing import Tuple, List

from core.logic import DistanceMap
from core.state import Layer
from .ShadowValue import ShadowValue


class ShadowLayer(Layer):

    def __init__(self, size: Tuple[int, int]):
        super().__init__(size, ShadowValue.NONE)

    def clear(self):
        self.fill(ShadowValue.NONE)

    def showPaths(self, distanceMap: DistanceMap, maxCost: int):
        ax1, ay1, ax2, ay2 = distanceMap.area
        x, y = (distanceMap.map <= maxCost).nonzero()
        if len(x) < 2:
            self.clear()
        else:
            x += ax1
            y += ay1
            self.fill(ShadowValue.SHADOW_LIGHT)
            self.cells[x, y] = ShadowValue.NONE

    def clearNumbers(self):
        cells = self.cells
        valid = cells >= ShadowValue.NUMBER_FIRST
        valid &= cells < ShadowValue.NUMBER_LAST
        cells[valid] = ShadowValue.NONE
