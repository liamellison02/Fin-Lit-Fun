from __future__ import annotations

from typing import Tuple, cast

from core.logic.Command import Command, WORLD_PRIORITY, WORLD_MAX_WIDTH
from core.logic.Logic import Logic
from core.state import Unit


class DisbandUnit(Command):

    def __init__(self, cell: Tuple[int, int], unit: Unit):
        super().__init__()
        self.__cell = cell
        self.__unit = unit

    def priority(self) -> int:
        return WORLD_PRIORITY + self.__cell[0] + self.__cell[1] * WORLD_MAX_WIDTH

    def check(self, logic: Logic) -> bool:
        world = logic.world
        if not world.contains(self.__cell):
            return False

        item = world.units.getItem(self.__cell)
        if item is None:
            self._message = f"Invalid coordinates {self.__cell}"
            return False
        unit = cast(Unit, item)
        if unit != self.__unit:
            self._message = "Unit not found"
            return False
        if unit.playerId != logic.state.playerId:
            self._message = "Current player does not own this unit"
            return False

        return True

    def execute(self, logic: Logic):
        logic.rules.removeUnit(self.__cell, self.__unit)

