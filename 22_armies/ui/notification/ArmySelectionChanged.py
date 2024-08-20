from __future__ import annotations

from typing import Optional, Tuple

from core.state import Army
from .Notification import Notification


class ArmySelectionChanged(Notification):
    def __init__(self, cell: Tuple[int, int], army: Optional[Army] = None):
        super().__init__("ArmySelectionChanged")
        self.cell = cell
        self.army = army

    def getArgs(self) -> Tuple:
        return self.cell, self.army
