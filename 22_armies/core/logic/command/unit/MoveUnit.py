from __future__ import annotations

from typing import Tuple, List, cast, Optional

from core.constants import CellValue, ItemProperty, MoveCost
from core.logic.Command import Command, WORLD_PRIORITY, WORLD_MAX_WIDTH
from core.logic.DistanceMap import DistanceMap
from core.logic.Logic import Logic
from core.state import Unit, Army


class MoveUnit(Command):

    def __init__(self, fromCell: Tuple[int, int], path: List[Tuple[int, int]],
                 selection: Optional[List[Unit]] = None):
        super().__init__()
        self.__fromCell = fromCell
        self.__path: List[Tuple[int, int]] = path
        self.__selection = selection
        self.__cost = MoveCost.INFINITE
        self.__playerId = -1
        self.__movePoints = 0
        self.__fromUnits: List[Unit] = []
        self.__movingUnits: List[Unit] = []
        self.__toUnits: List[Unit] = []

    @property
    def movePoints(self) -> int:
        return self.__movePoints

    def priority(self) -> int:
        return WORLD_PRIORITY + self.__fromCell[0] + self.__fromCell[1] * WORLD_MAX_WIDTH

    def check(self, logic: Logic) -> bool:
        if not self.__path:
            return False
        fromCell = self.__fromCell
        toCell = self.__path[-1]
        if fromCell == toCell:
            return False

        world = logic.world
        if not world.contains(fromCell):
            return False
        if not world.contains(toCell):
            return False

        unitsLayer = logic.world.units
        fromItem = unitsLayer.getItem(fromCell)
        if fromItem is None:
            return False
        self.__playerId = fromItem.playerId
        if self.__playerId != logic.state.playerId:
            return False

        # Units in the origin cell
        selection = self.__selection
        fromUnits: List[Unit] = []
        toUnits: List[Unit] = []
        if isinstance(fromItem, Unit):
            unit = cast(Unit, fromItem)
            armySize = 1
            toUnits.append(unit)
            self.__movePoints = unit.getIntProperty(ItemProperty.MOVE_POINTS, 0)
        elif isinstance(fromItem, Army):
            army = cast(Army, fromItem)
            armySize = len(army)
            self.__movePoints = army.getLowestIntProperty(ItemProperty.MOVE_POINTS, 0, selection)
            if not selection:
                toUnits = army.units.copy()
            else:
                toUnits = [unit for unit in army.units if any(unit is selected for selected in selection)]
                fromUnits = [unit for unit in army.units if not any(unit is selected for selected in selection)]
        else:
            raise RuntimeError("Internal error")

        if armySize == 0:
            return False

        # Compute and check move cost
        distanceMap = DistanceMap.create(
            world, self.__playerId, fromCell, toCell, radius=2, armySize=armySize, maxArmySize=logic.rules.getArmyMaxSize()
        )
        self.__cost = distanceMap.getCost(toCell)
        if self.__cost > self.__movePoints:
            return False
        self.__movingUnits = toUnits.copy()

        # Units in the destination cell
        toValue = unitsLayer.getValue(toCell)
        print(toCell, toValue)
        toItem = unitsLayer.getItem(toCell)
        if toValue == CellValue.NONE:
            pass
        elif toValue == CellValue.UNITS_UNIT:
            unit = cast(Unit, toItem)
            toUnits.append(unit)
        elif toValue == CellValue.UNITS_ARMY:
            army = cast(Army, toItem)
            for unit in army.units:
                toUnits.append(unit)
        else:
            print("error")
            raise RuntimeError("Internal error")

        if len(self.__path) == 1 and len(toUnits) > logic.rules.getArmyMaxSize():
            self._message = f"Max army size: {logic.rules.getArmyMaxSize()}"
            return False

        self.__fromUnits = fromUnits
        self.__toUnits = toUnits

        return True

    def execute(self, logic: Logic):
        unitsLayer = logic.world.units

        cost = self.__cost
        for unit in self.__movingUnits:
            movePoints = unit.getIntProperty(ItemProperty.MOVE_POINTS)
            movePoints -= cost
            unit.setIntProperty(ItemProperty.MOVE_POINTS, movePoints)

        def updateCell(cell, units):
            if len(units) == 0:
                unitsLayer.setValue(cell, CellValue.NONE)
            elif len(units) == 1:
                unitsLayer.setValue(cell, CellValue.UNITS_UNIT)
                unitsLayer.setItem(cell, units[0])
            else:
                army = Army(self.__playerId)
                for unit in units:
                    army.addUnit(unit)
                unitsLayer.setValue(cell, CellValue.UNITS_ARMY)
                unitsLayer.setItem(cell, army)
            unitsLayer.notifyCellChanged(cell)

        fromCell = self.__fromCell
        toCell = self.__path[-1]
        updateCell(fromCell, self.__fromUnits)
        updateCell(toCell, self.__toUnits)
        logic.state.notifyUnitMoved(fromCell, toCell)

        if len(self.__path) > 1:
            path = self.__path.copy()
            fromCell = path.pop(-1)
            command = MoveUnit(fromCell, path, self.__selection)
            logic.addCommand(command)
