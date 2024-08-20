from __future__ import annotations

from typing import Tuple, cast

from core.constants import ItemProperty, CellValue, UnitClass
from core.constants.ItemProperty import attackProperties
from core.logic.Command import Command, WORLD_PRIORITY, WORLD_MAX_WIDTH
from core.logic.Logic import Logic
from core.state import Unit
from tools.vector import vectorDistI


class AttackUnit(Command):

    def __init__(self, cell: Tuple[int, int], targetCell: Tuple[int, int]):
        super().__init__()
        self.__cell = cell
        self.__targetCell = targetCell
        self.__damage = 0

    def priority(self) -> int:
        return WORLD_PRIORITY + self.__cell[0] + self.__cell[1] * WORLD_MAX_WIDTH

    def check(self, logic: Logic) -> bool:
        if self.__cell == self.__targetCell:
            return False

        world = logic.world
        if not world.contains(self.__cell):
            return False
        if not world.contains(self.__targetCell):
            return False

        item = world.units.getItem(self.__cell)
        if item is None:
            return False
        unit = cast(Unit, item)
        if unit.playerId != logic.state.playerId:
            return False
        if not unit.hasProperty(ItemProperty.ACTION_POINTS):
            return False
        actionPoints = unit.getIntProperty(ItemProperty.ACTION_POINTS)
        if actionPoints <= 0:
            return False

        targetUnit = world.units.getItem(self.__targetCell)
        if targetUnit is None:
            return False
        if targetUnit.playerId == logic.state.playerId:
            return False
        if not targetUnit.hasProperty(ItemProperty.LIFE_POINTS):
            return False

        self.__damage = 0
        dist = vectorDistI(self.__cell, self.__targetCell)
        for attack, properties in attackProperties.items():
            range = unit.getIntProperty(properties["range"], 1)
            if dist > range or (dist == 1 and range > 1):
                continue
            damage = unit.getIntProperty(attack, 0)
            damage -= targetUnit.getIntProperty(properties["defense"], 0)
            if damage > self.__damage:
                self.__damage = damage
        if self.__damage <= 0:
            return False

        return True

    def execute(self, logic: Logic):
        state = logic.state
        unitsLayer = logic.world.units

        item = unitsLayer.getItem(self.__cell)
        if item is None:
            raise RuntimeError("No unit")
        unit = cast(Unit, item)
        actionPoints = unit.getIntProperty(ItemProperty.ACTION_POINTS)
        unit.setIntProperty(ItemProperty.ACTION_POINTS, actionPoints - 1)
        state.notifyUnitChanged(self.__cell, unit)

        targetItem = unitsLayer.getItem(self.__targetCell)
        if targetItem is None:
            raise RuntimeError("No target unit")
        targetUnit = cast(Unit, targetItem)
        targetLifePoints = targetUnit.getIntProperty(ItemProperty.LIFE_POINTS)
        targetLifePoints = targetLifePoints - self.__damage
        if targetLifePoints > 0:
            targetUnit.setIntProperty(ItemProperty.LIFE_POINTS, targetLifePoints)
            state.notifyUnitChanged(self.__targetCell, targetUnit)
        elif targetUnit.unitClass == UnitClass.KNIGHT:
            targetUnit = Unit(UnitClass.SWORDSMAN, targetUnit.playerId)
            unitsLayer.setValue(self.__targetCell, CellValue.UNITS_UNIT)
            unitsLayer.setItem(self.__targetCell, targetUnit)
            unitsLayer.notifyCellChanged(self.__targetCell)
            state.notifyUnitChanged(self.__targetCell, targetUnit)
        else:
            logic.rules.removeUnit(self.__targetCell, targetUnit)
        state.notifyUnitDamaged(self.__targetCell, self.__damage)

