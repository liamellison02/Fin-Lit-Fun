from __future__ import annotations

from typing import Tuple, Optional, cast

from core.constants import CellValue, ItemProperty, CellUsage
from core.logic.Command import Command, WORLD_PRIORITY, WORLD_MAX_WIDTH
from core.logic.Logic import Logic
from core.state import City


class AssignCell(Command):

    def __init__(self, cityCell: Tuple[int, int], cell: Tuple[int, int], ignorePlayerId: bool = False):
        super().__init__()
        self.__cityCell = cityCell
        self.__cell = cell
        self.__ignorePlayerId = ignorePlayerId

        self.__city: Optional[City] = None
        self.__mode = CellUsage.NONE

    @property
    def mode(self) -> CellUsage:
        return self.__mode

    def priority(self) -> int:
        return WORLD_PRIORITY + self.__cell[0] + self.__cell[1] * WORLD_MAX_WIDTH

    def check(self, logic: Logic) -> bool:
        self._message = ""
        world = logic.world
        rules = logic.rules

        cityCell = self.__cityCell
        if not world.contains(cityCell):
            self._message = "City cell outside the world"
            return False
        value = world.objects.getValue(cityCell)
        if value != CellValue.OBJECTS_CITY:
            self._message = f"There is no city at {cityCell}"
            return False
        item = world.objects.getItem(cityCell)
        if item is None or not isinstance(item, City):
            self._message = f"There is no city at {cityCell}"
            return False
        city = self.__city = cast(City, item)
        if not self.__ignorePlayerId and self.__city.playerId != logic.state.playerId:
            self._message = "The current player does not own this city"
            return False

        cell = self.__cell
        if not world.contains(cell):
            self._message = "Cell outside the world"
            return False
        if world.assignments.hasAssignment(cell):
            self._message = "Tile is already assigned"
            return False
        if city.isAssigned(cell):
            self._message = "City already use this tile"
            return False
        if not rules.isInCityArea(cityCell, cell):
            self._message = "Not in city area"
            return False
        self.__mode = mode = rules.getCityCellUsage(city, cell)
        if mode == CellUsage.HOUSE:
            citizenCount = city.getIntProperty(ItemProperty.CITIZEN_COUNT, 0)
            citizenCountMax = city.getIntProperty(ItemProperty.CITIZEN_COUNT_MAX, 0)
            if citizenCount >= citizenCountMax:
                self._message = "City has reached its maximum size"
                return False
        elif mode == CellUsage.PRODUCTION_BUILDING:
            pass
        elif mode == CellUsage.TRAINING_CAMP:
            pass
        elif mode == CellUsage.WORKER:
            citizenCount = city.getIntProperty(ItemProperty.CITIZEN_COUNT, 0)
            workerCount = city.getIntProperty(ItemProperty.WORKER_COUNT, 0)
            if citizenCount == workerCount:
                self._message = "All citizens work on tiles."
                return False
            workerCountMax = city.getIntProperty(ItemProperty.WORKER_COUNT_MAX, 0)
            if workerCount >= workerCountMax:
                self._message = "We are not allowed to assign more workers"
                return False
        else:
            self._message = "This tile cannot be used by the city"
            return False

        return True

    def execute(self, logic: Logic):
        assert self.__city is not None
        cell = self.__cell
        city = self.__city
        world = logic.world
        state = logic.state

        mode = self.__mode
        if mode == CellUsage.HOUSE:
            citizenCount = city.getIntProperty(ItemProperty.CITIZEN_COUNT, 0)
            city.setIntProperty(ItemProperty.CITIZEN_COUNT, citizenCount + 1)
        elif mode == CellUsage.PRODUCTION_BUILDING:
            pass
        elif mode == CellUsage.TRAINING_CAMP:
            pass
        elif mode == CellUsage.WORKER:
            workerCount = city.getIntProperty(ItemProperty.WORKER_COUNT, 0)
            city.setIntProperty(ItemProperty.WORKER_COUNT, workerCount + 1)
        else:
            raise ValueError(f"Invalid mode {mode}")

        assignments = world.assignments
        assignments.setAssignment(cell, city)
        city.assign(cell)
        state.notifyCityCellAssigned(self.__cityCell, cell, mode)
        state.notifyResourcesChanged()

