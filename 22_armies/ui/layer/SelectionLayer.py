from typing import Tuple, List, Optional

from core.state import Layer
from .SelectionValue import SelectionValue


class SelectionLayer(Layer):

    def __init__(self, size: Tuple[int, int]):
        super().__init__(size, SelectionValue.NONE)

    def clear(self):
        self.fill(SelectionValue.NONE)

    def showPath(self, path: List[Tuple[int, int]], costs: List[int], movePoints: Optional[int] = None):
        self.clearNumbers()
        for cell, cost in zip(path, costs):
            if movePoints is not None and cost > movePoints:
                continue
            value = SelectionValue.NUMBER_FIRST + cost
            if value >= SelectionValue.NUMBER_LAST:
                continue
            self.setValue(cell, value)

    def clearNumbers(self):
        cells = self.cells
        valid = cells >= SelectionValue.NUMBER_FIRST
        valid &= cells < SelectionValue.NUMBER_LAST
        cells[valid] = SelectionValue.NONE
