from __future__ import annotations

from typing import Tuple, cast, Optional, Dict

from core.constants import CellValue, ItemProperty, UnitClass, Resource
from core.logic.Command import Command, WORLD_PRIORITY, WORLD_MAX_WIDTH
from core.logic.Logic import Logic
from core.state import City, Unit
from tools.vector import vectorAddI


class RecruitUnit(Command):

    def __init__(self, cityCell: Tuple[int, int], unitClass: UnitClass):
        super().__init__()
        self.__cityCell = cityCell
        self.__city: Optional[City] = None
        self.__unitClass = unitClass
        self.__available = 0
        self.__cost: Dict[Resource, int] = {}
        self.__genCell: Optional[Tuple[int, int]] = None

    @property
    def available(self) -> int:
        return self.__available

    @property
    def cost(self) -> Dict[Resource, int]:
        return self.__cost

    def priority(self) -> int:
        return WORLD_PRIORITY + self.__cityCell[0] + self.__cityCell[1] * WORLD_MAX_WIDTH

    def check(self, logic: Logic) -> bool:
        world = logic.world
        rules = logic.rules
        self.__available = 0
        self._message = ""

        unitProperties = rules.getUnitProperties(self.__unitClass)
        if ItemProperty.COST in unitProperties:
            self.__cost = cast(Dict[Resource, int], unitProperties[ItemProperty.COST])
        else:
            self.__cost = {}

        cityCell = self.__cityCell
        if not world.contains(cityCell):
            self._message = f"No city at {self.__cityCell}"
            return False
        item = world.objects.getItem(cityCell)
        if item is None or not isinstance(item, City):
            self._message = f"No city at {self.__cityCell}"
            return False
        self.__city = cast(City, item)
        if self.__city.playerId != logic.state.playerId:
            self._message = f"City is not owned by the current player"
            return False

        recruits, recruitsMax = rules.getCityRecruitState(self.__city)
        if self.__unitClass not in recruits or self.__unitClass not in recruitsMax:
            self._message = f"This city can't recruit this type of unit"
            return False

        self.__available = recruitsMax[self.__unitClass]
        self.__available -= recruits[self.__unitClass]

        if self.__available <= 0:
            self._message = f"We can't recruit more this turn"
            return False

        if self.__cost:
            player = logic.state.getPlayer()
            for resource, count in self.__cost.items():
                if player.getResource(resource) < count:
                    self._message = f"Not enough {resource.formatName()}"
                    return False

        units = world.units
        for y in range(2):
            for x in range(2):
                cell = vectorAddI(cityCell, (x, y))
                if units.getValue(cell) == CellValue.NONE \
                        and units.getItem(cell) is None:
                    self.__genCell = cell
                    return True

        self._message = f"No room"
        return False

    def execute(self, logic: Logic):
        assert self.__city is not None
        assert self.__genCell is not None
        rules = logic.rules

        units = logic.world.units
        unit = Unit(self.__unitClass, logic.state.playerId)
        unit.setProperties(logic.rules.getUnitProperties(self.__unitClass))
        units.setValue(self.__genCell, CellValue.UNITS_UNIT)
        units.setItem(self.__genCell, unit)

        rules.setCityRecruitState(self.__city, self.__unitClass)

        unitProperties = rules.getUnitProperties(self.__unitClass)
        if ItemProperty.COST in unitProperties:
            cost = cast(Dict[Resource, int], unitProperties[ItemProperty.COST])
            player = logic.state.getPlayer()
            for resource, count in cost.items():
                count = player.getResource(resource) - count
                player.setResource(resource, count)

        units.notifyCellChanged(self.__genCell)
        logic.state.notifyUnitRecruited(self.__genCell)
        logic.state.notifyResourcesChanged()


