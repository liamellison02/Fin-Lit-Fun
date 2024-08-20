from __future__ import annotations

from typing import cast, Optional, Tuple

from core.constants import CellValue, checkCellValue, ItemProperty, CellUsage
from core.logic.Logic import Logic
from core.state import City, Item, TrainingCamp
from tools.tilecodes import mask4, code4
from .SetLayerCell import SetLayerCell
from .. import AssignCell


class SetObjectsCell(SetLayerCell):

    def __init__(self, cell: Tuple[int, int], value: CellValue,
                 item: Optional[Item] = None, fill: bool = False):
        super().__init__(cell, value, item, fill)
        self.__city: Optional[City] = None

    def check(self, logic: Logic) -> bool:
        value = self._value
        if not checkCellValue("objects", value):
            return False
        cell = self._cell
        if cell is None:
            return False
        world = logic.world
        if not world.contains(cell):
            return False

        ground = world.ground
        impassable = world.impassable
        objects = world.objects
        rules = logic.rules

        def canBuild(here):
            if not objects.contains(here):
                return False
            if ground.getValue(here) == CellValue.GROUND_SEA:
                self._message = "Can't build on the sea"
                return False
            if impassable.getValue(here) != CellValue.NONE:
                self._message = "Can't build on this land"
                return False
            if objects.getValue(here) != CellValue.NONE:
                self._message = "There is already something here"
                return False
            return True

        objectsValue = objects.getValue(cell)
        if value == CellValue.NONE:
            if objectsValue == CellValue.NONE:  # Value already removed
                return False
        elif value in [CellValue.OBJECTS_ROAD_DIRT, CellValue.OBJECTS_ROAD_STONE]:
            if self._item is not None:
                return False
            impassableValue = impassable.getValue(cell)
            if impassableValue == CellValue.IMPASSABLE_RIVER:  # River case
                neighbors = impassable.getNeighbors4(cell)
                mask = mask4(neighbors, CellValue.IMPASSABLE_RIVER)
                code = code4(mask)
                if code not in [6, 9]:  # Horizontal or vertical river
                    return False
            elif not canBuild(cell):
                return False
        elif value == CellValue.OBJECTS_CITY:
            if self._item is None or not isinstance(self._item, City):
                return False
            x0, y0 = cell
            for y in range(y0, y0 + 2):
                for x in range(x0, x0 + 2):
                    if not canBuild((x, y)):
                        return False
            for y in range(y0 - 1, y0 + 3):
                for x in range(x0 - 1, x0 + 3):
                    if objects.contains((x, y)) and \
                            objects.getValue((x, y)) == CellValue.OBJECTS_CITY:
                        return False
        elif rules.isProductionBuilding(value):
            self.__city, cityCell = rules.findClosestCity(cell)
            if self.__city is None or cityCell is None:
                self._message = "No city found"
                return False
            if not rules.isInCityArea(cityCell, cell):
                self._message = "Tile is not in the area of a city"
                return False
            if self._item is not None:
                self._message = "Production building can't have an item"
                return False
        elif rules.isTrainingCamp(value):
            self.__city, cityCell = rules.findClosestCity(cell)
            if self.__city is None or cityCell is None:
                self._message = "No city found"
                return False
            if not rules.isInCityArea(cityCell, cell):
                self._message = "Tile is not in the area of a city"
                return False
            if self._item is None:
                self._item = TrainingCamp(logic.state.playerId)
                self._item.setProperties(rules.getTrainingCampProperties(value))
        elif not canBuild(cell):
            return False

        return True

    def __handleRemove(self, logic: Logic):
        cell = self._cell
        rules = logic.rules
        objects = logic.world.objects
        assignments = logic.world.assignments

        value = objects.getValue(cell)
        if value == CellValue.OBJECTS_CITY:
            cell = rules.getCityTopLeft(cell)
            item = objects.getItem(cell)
            city = cast(City, item)
            for cityCell in city.cells:
                assignments.setAssignment(cityCell, None)
            city.cells.clear()
            x0, y0 = cell
            for y in range(y0, y0 + 2):
                for x in range(x0, x0 + 2):
                    objects.setValue((x, y), CellValue.NONE)
                    objects.notifyCellChanged((x, y))
        elif assignments.hasAssignment(cell):
            city = assignments.getAssignment(cell)
            city.unassign(cell)
            assignments.setAssignment(cell, None)
            objects.setValue(cell, CellValue.NONE)
            objects.notifyCellChanged(cell)
            logic.state.notifyResourcesChanged()
        else:
            objects.setValue(cell, CellValue.NONE)
            objects.notifyCellChanged(cell)

    def __handleProductionBuilding(self, logic: Logic):
        assert self.__city is not None
        cell = self._cell

        self.__city.assign(cell)
        assignments = logic.world.assignments
        assignments.setAssignment(cell, self.__city)
        objects = logic.world.objects
        objects.setValue(cell, self._value)
        objects.notifyCellChanged(cell)
        logic.state.notifyResourcesChanged()

    def __handleTrainingCamp(self, logic: Logic):
        assert self.__city is not None
        cell = self._cell

        self.__city.assign(cell)
        assignments = logic.world.assignments
        assignments.setAssignment(cell, self.__city)
        objects = logic.world.objects
        objects.setValue(cell, self._value)
        objects.setItem(cell, self._item)
        objects.notifyCellChanged(cell)

    def __handleCity(self, logic: Logic):
        city = cast(City, self._item)
        cityCell = self._cell
        rules = logic.rules

        objects = logic.world.objects
        x0, y0 = cityCell
        for y in range(y0, y0 + 2):
            for x in range(x0, x0 + 2):
                cell = x, y
                objects.setValue(cell, self._value)
                objects.setItem(cell, city)
                objects.notifyCellChanged(cell)

        city.setIntProperty(ItemProperty.CITIZEN_COUNT, 0)
        pos, area = rules.getCityArea(cityCell)
        for y in range(area.shape[1]):
            for x in range(area.shape[0]):
                if area[x, y] == 0:
                    continue
                cell = pos[0] + x, pos[1] + y
                command = AssignCell(cityCell, cell)
                if command.check(logic) and command.mode != CellUsage.WORKER:
                    command.execute(logic)

        city.setIntProperty(ItemProperty.WORKER_COUNT, 0)
        rules.autoAssignCitizens(cityCell)

    def __handleDefault(self, logic: Logic):
        cell = self._cell
        objects = logic.world.objects
        objects.setValue(cell, self._value)
        objects.notifyCellChanged(cell)

    def execute(self, logic: Logic):
        cell = self._cell
        value = self._value
        if value == CellValue.NONE:
            self.__handleRemove(logic)
        elif value == CellValue.OBJECTS_CITY:
            self.__handleCity(logic)
        elif logic.rules.isProductionBuilding(value):
            self.__handleProductionBuilding(logic)
        elif logic.rules.isTrainingCamp(value):
            self.__handleTrainingCamp(logic)
        else:
            self.__handleDefault(logic)

        if self._fill:
            x, y = cell[0], cell[1]
            logic.addCommand(SetObjectsCell((x + 1, y), self._value, self._item, True))
            logic.addCommand(SetObjectsCell((x - 1, y), self._value, self._item, True))
            logic.addCommand(SetObjectsCell((x, y + 1), self._value, self._item, True))
            logic.addCommand(SetObjectsCell((x, y - 1), self._value, self._item, True))

