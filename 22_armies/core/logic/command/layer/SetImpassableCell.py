from __future__ import annotations

from core.constants import CellValue, checkCellValue
from .SetLayerCell import SetLayerCell
from core.logic.Logic import Logic


class SetImpassableCell(SetLayerCell):

    def check(self, logic: Logic) -> bool:
        value = self._value
        if not checkCellValue("impassable", value):
            return False
        if self._item is not None:
            return False
        cell = self._cell
        world = logic.world
        if not world.contains(cell):
            return False

        value = self._value
        impassableValue = world.impassable.getValue(cell)
        if value == CellValue.NONE:
            if impassableValue == CellValue.NONE:  # Value already removed
                return False
            # We can't delete a river if there is a bridge on top
            objectsValue = world.objects.getValue(cell)
            if impassableValue == CellValue.IMPASSABLE_RIVER \
                    and objectsValue in [CellValue.OBJECTS_ROAD_STONE, CellValue.OBJECTS_ROAD_DIRT]:
                return False
        else:
            if impassableValue != CellValue.NONE:  # Value already set
                return False
            if world.ground.getValue(cell) == CellValue.GROUND_SEA:
                return False
            # We can't add a mountain, river etc. below an object
            if world.objects.getValue(cell) != CellValue.NONE:
                return False
            if world.units.getValue(cell) != CellValue.NONE:
                return False

        return True
        
    def execute(self, logic: Logic):
        cell = self._cell
        value = self._value
        world = logic.world
        world.impassable.setValue(cell, value)
        world.impassable.notifyCellChanged(cell)

        if self._fill:
            x, y = cell[0], cell[1]
            logic.addCommand(SetImpassableCell((x + 1, y), self._value, self._item, True))
            logic.addCommand(SetImpassableCell((x - 1, y), self._value, self._item, True))
            logic.addCommand(SetImpassableCell((x, y + 1), self._value, self._item, True))
            logic.addCommand(SetImpassableCell((x, y - 1), self._value, self._item, True))

