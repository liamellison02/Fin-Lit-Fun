from __future__ import annotations

from core.constants import CellValue, checkCellValue
from .SetLayerCell import SetLayerCell
from core.logic.Logic import Logic


class SetGroundCell(SetLayerCell):

    def check(self, logic: Logic) -> bool:
        value = self._value
        if not checkCellValue("ground", value):
            return False
        if self._item is not None:
            return False
        cell = self._cell
        world = logic.world
        if not world.contains(cell):
            return False

        value = self._value
        groundValue = world.ground.getValue(cell)
        if value == groundValue:  # Value already set
            return False
        
        if value == CellValue.GROUND_SEA:  # Sea case
            impassableValue = world.impassable.getValue(cell)
            if impassableValue != CellValue.NONE:
                return False
            objectsValue = world.objects.getValue(cell)
            if objectsValue != CellValue.NONE:
                return False
            unitsValue = world.units.getValue(cell)
            if unitsValue != CellValue.NONE:
                return False

        return True

    def execute(self, logic: Logic):
        cell = self._cell
        value = self._value
        ground = logic.world.ground
        ground.setValue(cell, value)
        ground.notifyCellChanged(cell)

        if self._fill:
            x, y = cell[0], cell[1]
            logic.addCommand(SetGroundCell((x + 1, y), self._value, self._item, True))
            logic.addCommand(SetGroundCell((x - 1, y), self._value, self._item, True))
            logic.addCommand(SetGroundCell((x, y + 1), self._value, self._item, True))
            logic.addCommand(SetGroundCell((x, y - 1), self._value, self._item, True))

