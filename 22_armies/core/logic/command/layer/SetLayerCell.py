from __future__ import annotations

from typing import Tuple, Optional

from core.constants import CellValue
from core.logic.Command import Command, WORLD_PRIORITY, WORLD_MAX_WIDTH
from core.state import Item


class SetLayerCell(Command):

    def __init__(self, cell: Tuple[int, int], value: CellValue,
                 item: Optional[Item] = None, fill: bool = False):
        super().__init__()
        self._cell = cell
        self._value = value
        self._item = item
        self._fill = fill

    def priority(self) -> int:
        return WORLD_PRIORITY + self._cell[0] + self._cell[1] * WORLD_MAX_WIDTH


