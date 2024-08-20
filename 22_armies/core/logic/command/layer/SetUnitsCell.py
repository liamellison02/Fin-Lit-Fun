from __future__ import annotations

from typing import cast

from core.constants import CellValue, WorldType
from .SetLayerCell import SetLayerCell
from core.logic.Logic import Logic
from core.state import Unit, Army


class SetUnitsCell(SetLayerCell):

    def check(self, logic: Logic) -> bool:
        if self._value not in [CellValue.NONE, CellValue.UNITS_UNIT]:
            return False

        cell = self._cell
        world = logic.world
        if not world.contains(cell):
            return False

        unitsValue = world.units.getValue(cell)
        if self._value == CellValue.NONE or self._item is None:
            if unitsValue == CellValue.NONE:  # Unit already removed
                return False
        else:
            if not isinstance(self._item, Unit):
                return False
            if world.type == WorldType.STRATEGIC:
                if unitsValue == CellValue.UNITS_UNIT:
                    item = world.units.getItem(cell)
                    if item.playerId != self._item.playerId:
                        return False
                elif unitsValue == CellValue.UNITS_ARMY:
                    item = world.units.getItem(cell)
                    if item.playerId != self._item.playerId:
                        return False
                    army = cast(Army, item)
                    if len(army.units) >= logic.rules.getArmyMaxSize():
                        return False
                elif unitsValue != CellValue.NONE:
                    return False
            elif world.type == WorldType.TACTIC:
                if unitsValue != CellValue.NONE:
                    return False
            else:
                return False

            # Ground
            if world.ground.getValue(cell) == CellValue.GROUND_SEA:  # Can't put a unit on the sea
                return False
            
            # Impassable
            impassableValue = world.impassable.getValue(cell)
            if impassableValue == CellValue.IMPASSABLE_RIVER:  # River case
                objectsValue = world.objects.getValue(cell)
                if objectsValue not in [CellValue.OBJECTS_ROAD_DIRT, CellValue.OBJECTS_ROAD_STONE]:  # Can walk on bridge
                    return False
            else:  # General case
                if impassableValue != CellValue.NONE:  # Can't walk on mountains etc.
                    return False

        return True

    def execute(self, logic: Logic):
        cell = self._cell
        units = logic.world.units
        unitsValue = units.getValue(cell)
        unit = cast(Unit, self._item)
        if unitsValue == CellValue.NONE:
            units.setValue(cell, CellValue.UNITS_UNIT)
            units.setItem(cell, unit)
        elif unitsValue == CellValue.UNITS_UNIT:
            army = Army(self._item.playerId)
            item = units.getItem(cell)
            army.addUnit(cast(Unit, item))
            army.addUnit(unit)
            units.setValue(cell, CellValue.UNITS_ARMY)
            units.setItem(cell, army)
        elif unitsValue == CellValue.UNITS_ARMY:
            item = units.getItem(cell)
            army = cast(Army, item)
            army.addUnit(unit)
            units.setItem(cell, army)
        else:
            raise RuntimeError("Internal error")
        units.notifyCellChanged(cell)

        if self._fill:
            x, y = cell[0], cell[1]
            logic.addCommand(SetUnitsCell((x + 1, y), self._value, self._item, True))
            logic.addCommand(SetUnitsCell((x - 1, y), self._value, self._item, True))
            logic.addCommand(SetUnitsCell((x, y + 1), self._value, self._item, True))
            logic.addCommand(SetUnitsCell((x, y - 1), self._value, self._item, True))
