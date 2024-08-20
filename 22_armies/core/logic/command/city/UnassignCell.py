from __future__ import annotations

from typing import Tuple, Optional, cast

from core.constants import CellValue, ItemProperty, CellUsage
from core.logic.Command import Command, WORLD_PRIORITY, WORLD_MAX_WIDTH
from core.logic.Logic import Logic
from core.state import City


class UnassignCell(Command):

    def __init__(self, cityCell: Tuple[int, int], cell: Tuple[int, int], ignorePlayerId: bool = False):
        super().__init__()
        self.__cityCell = cityCell
        self.__cell = cell
        self.__ignorePlayerId = ignorePlayerId

        self.__mode = CellUsage.NONE
        self.__city: Optional[City] = None

    @property
    def mode(self) -> CellUsage:
        return self.__mode

    def priority(self) -> int:
        return WORLD_PRIORITY + self.__cell[0] + self.__cell[1] * WORLD_MAX_WIDTH

    def check(self, logic: Logic) -> bool:
        world = logic.world

        cityCell = self.__cityCell
        if not world.contains(cityCell):
            return False
        value = world.objects.getValue(cityCell)
        if value != CellValue.OBJECTS_CITY:
            return False
        item = world.objects.getItem(cityCell)
        if item is None or not isinstance(item, City):
            return False
        self.__city = city = cast(City, item)
        if not self.__ignorePlayerId and city.playerId != logic.state.playerId:
            self._message = "The current player does not own this tile"
            return False

        cell = self.__cell
        if not world.contains(cell):
            return False
        if not world.assignments.hasAssignment(cell):
            return False
        if not city.isAssigned(cell):
            self._message = "City does not use this tile"
            return False
        self.__mode = logic.rules.getCityCellUsage(city, cell)
        if self.__mode == CellUsage.NONE:
            self._message = "City can not use this tile"
            return False
        return True

    def execute(self, logic: Logic):
        assert self.__city is not None
        cell = self.__cell
        city = self.__city
        state = logic.state

        mode = self.__mode
        if mode == CellUsage.HOUSE:
            citizenCount = city.getIntProperty(ItemProperty.CITIZEN_COUNT, 0) - 1
            city.setIntProperty(ItemProperty.CITIZEN_COUNT, citizenCount)
            workerCount = city.getIntProperty(ItemProperty.WORKER_COUNT, 0)
            if workerCount > citizenCount:
                logic.rules.removeCityWorker(self.__cityCell)
        elif mode == CellUsage.PRODUCTION_BUILDING:
            pass
        elif mode == CellUsage.TRAINING_CAMP:
            pass
        elif mode == CellUsage.WORKER:
            workerCount = city.getIntProperty(ItemProperty.WORKER_COUNT, 0)
            city.setIntProperty(ItemProperty.WORKER_COUNT, workerCount - 1)
        else:
            raise ValueError(f"Invalid mode {mode}")

        assignments = logic.world.assignments
        assignments.setAssignment(cell, None)
        city.unassign(cell)
        state.notifyCityCellUnassigned(self.__cityCell, cell)
        state.notifyResourcesChanged()

