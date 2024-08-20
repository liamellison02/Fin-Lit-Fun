from __future__ import annotations

from typing import Tuple, cast, Optional, Dict

from core.constants import CellValue, cellValueRanges, Resource, ItemProperty
from core.logic.Command import Command, WORLD_PRIORITY, WORLD_MAX_WIDTH
from core.logic.Logic import Logic
from core.logic.command import SetObjectsCell
from core.state import Unit


class Build(Command):

    def __init__(self, cell: Tuple[int, int], unit: Unit, cellValue: CellValue):
        super().__init__()
        self.__cell = cell
        self.__unit = unit
        self.__cellValue = cellValue
        self.__cost: Dict[Resource, int] = {}
        self.__setCommand: Optional[Command] = None

    @property
    def cost(self) -> Dict[Resource, int]:
        return self.__cost

    def priority(self) -> int:
        return WORLD_PRIORITY + self.__cell[0] + self.__cell[1] * WORLD_MAX_WIDTH

    def check(self, logic: Logic) -> bool:
        cellValue = self.__cellValue

        rules = logic.rules
        try:
            self.__cost = rules.getTileCost(cellValue)
        except:
            self._message = "Not buildable"
            return False

        valueRange = cellValueRanges["objects"]
        if valueRange[0] <= cellValue < valueRange[1] or cellValue == CellValue.NONE:
            self.__setCommand = SetObjectsCell(self.__cell, cellValue)
        else:
            self._message = "Not buildable"
            return False

        if not self.__setCommand.check(logic):
            if cellValue == CellValue.NONE:
                self._message = "Can't remove"
            else:
                self._message = self.__setCommand.message
            return False

        player = logic.state.getPlayer()
        if not player.hasResources(self.__cost):
            self._message = "Not enough resources"
            return False

        item = logic.world.units.getItem(self.__cell)
        if item is None:
            return False
        unit = cast(Unit, item)
        if unit.playerId != logic.state.playerId:
            self._message = "Not the current player's unit"
            return False
        if not unit.hasProperty(ItemProperty.ACTION_POINTS):
            self._message = "No action points"
            return False
        actionPoints = unit.getIntProperty(ItemProperty.ACTION_POINTS)
        if actionPoints <= 0:
            self._message = "Not enough action points"
            return False

        return True

    def execute(self, logic: Logic):
        assert self.__setCommand is not None

        self.__setCommand.execute(logic)

        unitsLayer = logic.world.units
        item = unitsLayer.getItem(self.__cell)
        if item is None:
            raise RuntimeError("No unit")
        unit = cast(Unit, item)
        actionPoints = unit.getIntProperty(ItemProperty.ACTION_POINTS)
        unit.setIntProperty(ItemProperty.ACTION_POINTS, actionPoints - 1)
        logic.state.notifyUnitChanged(self.__cell, unit)

        player = logic.state.getPlayer()
        player.removeResources(self.__cost)
        logic.state.notifyResourcesChanged()


