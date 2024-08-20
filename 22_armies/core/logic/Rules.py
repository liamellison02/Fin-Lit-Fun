from __future__ import annotations

from collections import defaultdict
from copy import copy
from typing import Tuple, Optional, List, Dict, cast, Union, TYPE_CHECKING, Any

import numpy as np

from tools.vector import vectorDistI
from ..constants import CellValue, tileProduction, ItemProperty, UnitClass, ItemPropertyValue, UnitProperties, Resource, \
    CityProperties, CityClass, tileCost, CampProperties, CellUsage
from ..constants.Direction import transformCoords, Direction
from ..state import City, Player, Unit
from ..state.GameState import GameState

if TYPE_CHECKING:
    from .Logic import Logic


class Rules:

    def __init__(self, logic: Logic):
        self.__logic = logic
        self.__state = logic.state

    @property
    def logic(self) -> Logic:
        return self.__logic

    @property
    def state(self) -> GameState:
        return self.__state

    # Units

    def getUnitProperties(self, unitClass: UnitClass) -> Dict[ItemProperty, ItemPropertyValue]:
        if unitClass not in UnitProperties:
            raise ValueError(f"Invalid unit class {unitClass.toName()}")
        return UnitProperties[unitClass]

    # Costs

    def getTileCost(self, cellValue: int) -> Dict[Resource, int]:
        if cellValue not in tileCost:
            raise ValueError(f"No cost for {CellValue.getString(cellValue)}")
        return tileCost[cellValue]

    def getTileEffectDescription(self, cellValue: int) -> str:
        if cellValue not in tileEffectDescription:
            return ""
        return tileEffectDescription[cellValue]

    # City

    def getCityProperties(self, cityClass: CityClass) -> Dict[ItemProperty, ItemPropertyValue]:
        if cityClass not in CityProperties:
            raise ValueError(f"Invalid city class {cityClass}")
        return CityProperties[cityClass]

    def getCityTopLeft(self, cell: Tuple[int, int]) -> Tuple[int, int]:
        layer = self.__state.world.objects
        value = layer.getValue(cell)
        if value != CellValue.OBJECTS_CITY:
            raise ValueError(f"No city at {cell}")
        item = layer.getItem(cell)
        tlCell = transformCoords(cell, Direction.TOPLEFT)
        if layer.contains(tlCell) and layer.getValue(tlCell) == value:
            assert layer.getItem(tlCell) == item
            return tlCell
        tlCell = transformCoords(cell, Direction.TOP)
        if layer.contains(tlCell) and layer.getValue(tlCell) == value:
            assert layer.getItem(tlCell) == item
            return tlCell
        tlCell = transformCoords(cell, Direction.LEFT)
        if layer.contains(tlCell) and layer.getValue(tlCell) == value:
            assert layer.getItem(tlCell) == item
            return tlCell
        return cell

    def findCity(self, cityOrCell: Union[City, Tuple[int, int]]) -> Optional[City]:
        world = self.__state.world
        if isinstance(cityOrCell, City):
            city = cast(City, cityOrCell)
        elif type(cityOrCell) == tuple:
            objects = world.objects
            if objects.getValue(cityOrCell) != CellValue.OBJECTS_CITY:
                return None
            item = objects.getItem(cityOrCell)
            if not isinstance(item, City):
                return None
            city = cast(City, item)
        else:
            return None
        return city

    def getCity(self, cityOrCell: Union[City, Tuple[int, int]]) -> City:
        city = self.findCity(cityOrCell)
        if city is None:
            raise ValueError(f"Invalid city")
        return city

    def getCityHouseArea(self, cityCell: Tuple[int, int], valueIn: int = 1, valueOut: int = 0) -> \
            Tuple[Tuple[int, int], np.ndarray]:
        cityCell = self.getCityTopLeft(cityCell)
        area = Rules.houseArea.copy() * valueIn
        if valueOut != 0:
            area += (1 - Rules.houseArea) * valueOut
        pos = (
            cityCell[0] - area.shape[0] // 2 + 1,
            cityCell[1] - area.shape[1] // 2 + 1
        )
        return pos, area

    def getCityArea(self, cityCell: Tuple[int, int], valueIn: int = 1, valueOut: int = 0) \
            -> Tuple[Tuple[int, int], np.ndarray]:
        cityCell = self.getCityTopLeft(cityCell)
        if Rules.cityArea is None:
            import math
            radius = 8

            def circle(i, j):
                x = i - radius + 0.5
                y = j - radius + 0.5
                return 1 if math.sqrt(x * x + y * y) < radius else 0

            Rules.cityArea = np.array(
                [[circle(i, j) for i in range(2 * radius)] for j in range(2 * radius)],
                dtype=np.int32
            )

        area = Rules.cityArea.copy() * valueIn
        if valueOut != 0:
            area += (1 - Rules.cityArea) * valueOut
        pos = (
            cityCell[0] - area.shape[0] // 2 + 1,
            cityCell[1] - area.shape[1] // 2 + 1
        )
        return pos, area

    def isInCityArea(self, cityCell: Tuple[int, int], cell: Tuple[int, int]) -> bool:
        pos, cityArea = self.getCityArea(cityCell)
        posX, posY = pos
        x, y = cell
        if x < posX or x >= posX + cityArea.shape[0]:
            return False
        if y < posY or y >= posY + cityArea.shape[1]:
            return False
        x -= posX
        y -= posY
        return cityArea[x, y] != 0

    def findCityUnassignedHouses(self, cityCell: Tuple[int, int]):
        pos, houseArea = self.getCityHouseArea(cityCell)

        world = self.__state.world
        ground = world.ground
        objects = world.objects
        assigments = world.assignments

        intersection = ground.computeAreaIntersection(pos, houseArea)
        if intersection is None:
            return []
        cells = []
        sourceMinX, sourceMinY, destMinX, destMinY, width, height = intersection
        for y in range(height):
            for x in range(width):
                sourceX, sourceY = sourceMinX + x, sourceMinY + y
                if houseArea[sourceX, sourceY] == 0:
                    continue
                dest = destMinX + x, destMinY + y
                if objects.getValue(dest) != CellValue.OBJECTS_HOUSES:
                    continue
                if assigments.hasAssignment(dest):
                    continue
                cells.append(dest)
        return cells

    def findCityTilesforNewHouses(self, cityCell: Tuple[int, int]) -> List[Tuple[int, int]]:
        pos, houseArea = self.getCityHouseArea(cityCell)

        world = self.__state.world
        ground = world.ground
        impassable = world.impassable
        objects = world.objects

        intersection = ground.computeAreaIntersection(pos, houseArea)
        if intersection is None:
            return []
        cells = []
        sourceMinX, sourceMinY, destMinX, destMinY, width, height = intersection
        for y in range(height):
            for x in range(width):
                sourceX, sourceY = sourceMinX + x, sourceMinY + y
                if houseArea[sourceX, sourceY] == 0:
                    continue
                dest = destMinX + x, destMinY + y
                if ground.getValue(dest) != CellValue.GROUND_EARTH:
                    continue
                if impassable.getValue(dest) != CellValue.NONE:
                    continue
                if objects.getValue(dest) != CellValue.NONE:
                    continue
                cells.append(dest)

        return cells

    def computeCityWorkersProduction(self, cityCell: Tuple[int, int], sortProduction: Optional[Resource]) -> \
            List[Tuple[Tuple[int, int], Dict[Resource, int]]]:
        cityCell = self.getCityTopLeft(cityCell)
        city = self.getCity(cityCell)
        cells: List[Tuple[Tuple[int, int], Dict[Resource, int]]] = []
        for cell in city.cells:
            mode = self.getCityCellUsage(city, cell)
            if mode != CellUsage.WORKER:
                continue
            resources = self.computeCellResources(cityCell, cell)
            production: Dict[Resource, int] = {}
            addResources(production, resources)
            cells.append((cell, production))

        if sortProduction:
            def sortFunc(x: Tuple[Tuple[int, int], Dict[Resource, int]]):
                cell, prod = x[0], x[1]
                if sortProduction in prod:
                    dist = (cell[0] - cityCell[0] - 0.5) ** 2 + (cell[1] - cityCell[1] - 0.5) ** 2
                    return (prod[sortProduction] * 10000 + 10000 - dist) * 10 + (3 * cell[0] + 7 * cell[1]) % 10
                return 0

            cells.sort(key=sortFunc)

        return cells

    def removeCityWorker(self, cityCell: Tuple[int, int]):
        city = self.getCity(cityCell)
        if city.getWorkerCount() == 0:
            return
        workersCell = self.computeCityWorkersProduction(cityCell, Resource.FOOD)
        if not workersCell:
            return
        cell = workersCell[0][0]
        from .command import UnassignCell
        command = UnassignCell(cityCell, cell, ignorePlayerId=True)
        assert command.check(self.__logic)
        command.execute(self.__logic)

    def findCityUnworkedCells(self, cityCell: Tuple[int, int], sortProduction: Optional[Resource]) -> \
            List[Tuple[Tuple[int, int], Dict[Resource, int]]]:
        assignments = self.__state.world.assignments
        cityCell = self.getCityTopLeft(cityCell)
        pos, area = self.getCityArea(cityCell)
        housesPos, housesArea = self.getCityHouseArea(cityCell)
        housesWidth, housesHeight = housesArea.shape[0], housesArea.shape[1]
        city = self.getCity(cityCell)
        cells: List[Tuple[Tuple[int, int], Dict[Resource, int]]] = []
        for y in range(area.shape[1]):
            for x in range(area.shape[0]):
                if area[x, y] == 0:
                    continue
                cell = pos[0] + x, pos[1] + y
                if assignments.hasAssignment(cell):
                    continue
                hX = cell[0] - housesPos[0]
                hY = cell[1] - housesPos[1]
                if 0 <= hX < housesWidth and 0 <= hY < housesHeight:
                    if housesArea[hX, hY] != 0:
                        continue
                if city.isAssigned(cell):
                    continue
                if self.getCityCellUsage(city, cell) != CellUsage.WORKER:
                    continue
                resources = self.computeCellResources(cityCell, cell)
                if not resources:
                    continue
                production: Dict[Resource, int] = {}
                addResources(production, resources)
                cells.append((cell, production))

        if sortProduction:
            def sortFunc(x: Tuple[Tuple[int, int], Dict[Resource, int]]):
                cell, prod = x[0], x[1]
                if sortProduction in prod:
                    dist = (cell[0] - cityCell[0] - 0.5) ** 2 + (cell[1] - cityCell[1] - 0.5) ** 2
                    return (prod[sortProduction] * 10000 + 10000 - dist) * 10 + (3 * cell[0] + 7 * cell[1]) % 10
                return 0

            cells.sort(key=sortFunc, reverse=True)

        return cells

    def autoAssignCitizen(self, cityCell: Tuple[int, int]) -> bool:
        city = self.getCity(cityCell)
        production = self.computeCityProduction(city)
        if production['balance'][Resource.FOOD] >= 0:
            return False
        citizenCount = city.getProperty(ItemProperty.CITIZEN_COUNT, 0)
        workerCount = city.getProperty(ItemProperty.WORKER_COUNT, 0)
        if workerCount == citizenCount:
            return False

        unassignedCells = self.findCityUnworkedCells(cityCell, Resource.FOOD)
        if not unassignedCells:
            return False

        index = 0
        unassignedCell = unassignedCells[index][0]
        assert not city.isAssigned(unassignedCell)
        from .command import AssignCell
        command = AssignCell(cityCell, unassignedCell, ignorePlayerId=True)
        if not command.check(self.__logic):
            return False
        command.execute(self.__logic)
        return True

    def autoAssignCitizens(self, cityCell: Tuple[int, int]):
        while self.autoAssignCitizen(cityCell):
            pass

    def computeCellResources(self, cityOrCell: Union[City, Tuple[int, int]], cell: Tuple[int, int]) -> List[Resource]:
        world = self.__state.world
        if not world.contains(cell):
            return []
        objectValue = world.objects.getValue(cell)
        if self.isProductionBuilding(objectValue):
            return []
        if self.isTrainingCamp(objectValue):
            return []
        groundValue = CellValue(world.ground.getValue(cell))
        impassableValue = CellValue(world.impassable.getValue(cell))
        objectsValue = CellValue(world.objects.getValue(cell))
        if groundValue in tileProduction:
            impassableProduction = tileProduction[groundValue]
            if impassableValue in impassableProduction:
                objectsProduction = impassableProduction[impassableValue]
                if objectsValue in objectsProduction:
                    return objectsProduction[objectsValue]
        return []

    def getCityGranarySize(self, cityOrCell: Union[City, Tuple[int, int]]):
        city = self.getCity(cityOrCell)
        return city.getProperty(ItemProperty.GRANARY_FOOD_MAX, 0)

    def getCityGrowthMax(self, cityOrCell: Union[City, Tuple[int, int]]):
        city = self.getCity(cityOrCell)
        citizenCount = city.getCitizenCount()
        growthMin = cast(int, city.getProperty(ItemProperty.GROWTH_POINTS_MIN, 1))
        growthRate = cast(int, city.getProperty(ItemProperty.GROWTH_POINTS_RATE, 1))
        growthMax = cast(int, city.getProperty(ItemProperty.GROWTH_POINTS_MAX, 10))
        return min(max(int(citizenCount / growthRate), growthMin), growthMax)

    def getCityCellUsage(self, cityOrCell: Union[City, Tuple[int, int]], cell: Tuple[int, int]) -> CellUsage:
        objectValue = self.__state.world.objects.getValue(cell)
        if objectValue == CellValue.OBJECTS_HOUSES:
            return CellUsage.HOUSE
        if self.isProductionBuilding(objectValue):
            return CellUsage.PRODUCTION_BUILDING
        if self.isTrainingCamp(objectValue):
            return CellUsage.TRAINING_CAMP
        city = self.getCity(cityOrCell)
        resources = self.computeCellResources(city, cell)
        if resources:
            return CellUsage.WORKER
        return CellUsage.NONE

    def getCityBuildings(self, cityOrCell: Union[City, Tuple[int, int]]) -> List[Tuple[Tuple[int, int], int]]:
        buildings = []
        city = self.getCity(cityOrCell)
        objects = self.__state.world.objects
        for cell in city.cells:
            mode = self.getCityCellUsage(city, cell)
            if mode == CellUsage.PRODUCTION_BUILDING:
                objectValue = objects.getValue(cell)
                buildings.append((cell, objectValue))
        return buildings

    def computeCityProduction(self, cityOrCell: Union[City, Tuple[int, int]]) -> \
            Dict[str, Dict[Resource, int]]:
        city = self.getCity(cityOrCell)
        base: Dict[Resource, int] = defaultdict(int)
        addResources(base, city.getResourcesListProperty(ItemProperty.BASE_PRODUCTION, []))
        total = base.copy()

        objects = self.__state.world.objects
        workers: Dict[Resource, int] = defaultdict(int)
        buildings: Dict[int, int] = defaultdict(int)
        for cell in city.cells:
            mode = self.getCityCellUsage(city, cell)
            if mode == CellUsage.WORKER:
                resources = self.computeCellResources(city, cell)
                addResources(workers, resources)
                addResources(total, resources)
            elif mode == CellUsage.PRODUCTION_BUILDING:
                objectValue = objects.getValue(cell)
                buildings[objectValue] += 1

        # Merchants production
        merchants: Dict[Resource, int] = defaultdict(int)
        merchantProduction = city.getResourcesListProperty(ItemProperty.MERCHANT_PRODUCTION)
        addResources(merchants, merchantProduction, city.getMerchantCount())
        addResources(total, merchantProduction, city.getMerchantCount())

        # Upkeep
        upkeep: Dict[Resource, int] = defaultdict(int)
        citizenUpkeep = city.getResourcesListProperty(ItemProperty.CITIZEN_UPKEEP, [])
        addResources(upkeep, citizenUpkeep, city.getCitizenCount())

        buildingsUpkeep = city.getResourcesDictPerValProperty(ItemProperty.BUILDINGS_UPKEEP)
        for building, count in buildings.items():
            if building in buildingsUpkeep:
                buildingUpkeep = buildingsUpkeep[building]
                addResources(upkeep, buildingUpkeep, count)

        # Mills / bakery
        mills = {
            Resource.FOOD: min(total[Resource.FOOD], 8 * buildings[CellValue.OBJECTS_MILL])
        }
        if buildings[CellValue.OBJECTS_BAKERY] > 0:
            bakery = {
                Resource.FOOD: mills[Resource.FOOD]
            }
        else:
            bakery = {}
        addResources(total, mills)
        addResources(total, bakery)

        # Sawmills / factory
        sawmills = {
            Resource.WOOD: min(total[Resource.WOOD], 8 * buildings[CellValue.OBJECTS_SAWMILL])
        }
        if buildings[CellValue.OBJECTS_FACTORY] > 0:
            factory = {
                Resource.WOOD: sawmills[Resource.WOOD]
            }
        else:
            factory = {}
        addResources(total, sawmills)
        addResources(total, factory)

        # Markets / bank
        markets = {
            Resource.GOLD: min(total[Resource.GOLD], 8 * buildings[CellValue.OBJECTS_MARKET])
        }
        if buildings[CellValue.OBJECTS_BANK] > 0:
            bank = {
                Resource.GOLD: markets[Resource.GOLD]
            }
        else:
            bank = {}
        addResources(total, markets)
        addResources(total, bank)

        balance = total.copy()
        for resource, count in upkeep.items():
            balance[resource] -= count

        return {
            "base": base,
            "merchants": merchants,
            "workers": workers,
            "mills": mills,
            "bakery": bakery,
            "sawmills": sawmills,
            "factory": factory,
            "markets": markets,
            "bank": bank,
            "total": total,
            "upkeep": upkeep,
            "balance": balance,
        }

    def getCities(self) -> Dict[Tuple[int, int], City]:
        cities = {}
        objects = self.__state.world.objects
        for cell in objects.findValues(CellValue.OBJECTS_CITY):
            item = objects.getItem(cell)
            if not isinstance(item, City):
                continue
            city = cast(City, item)
            cell = self.getCityTopLeft(cell)
            cities[cell] = city
        return cities

    def findClosestCity(self, cell: Tuple[int, int]) -> Tuple[Optional[City], Optional[Tuple[int, int]]]:
        dist = 1000000000
        closestCell = None
        closestCity = None
        objects = self.__state.world.objects
        for cityCell in objects.findValues(CellValue.OBJECTS_CITY):
            item = objects.getItem(cityCell)
            if not isinstance(item, City):
                continue
            city = cast(City, item)
            d = vectorDistI(cell, cityCell)
            if d < dist:
                dist = d
                closestCell = cityCell
                closestCity = city
        return closestCity, closestCell

    def isProductionBuilding(self, cellValue: int) -> bool:
        return cellValue in tileIsProductionBuilding

    # Training camps

    def isTrainingCamp(self, cellValue: int) -> bool:
        return cellValue in tileIsTrainingCamp

    def findTrainingCamps(self) -> List[Tuple[int, int]]:
        return self.__state.world.objects.findValues(list(tileIsTrainingCamp))

    def getTrainingCampProperties(self, cellValue: int) -> Dict[ItemProperty, ItemPropertyValue]:
        if cellValue not in CampProperties:
            raise ValueError(f"Invalid training camp {cellValue}")
        return CampProperties[CellValue(cellValue)]

    def getCityRecruitState(self, cityOrCell: Union[City, Tuple[int, int]]) -> Tuple[Dict[UnitClass, int], Dict[UnitClass, int]]:
        city = self.getCity(cityOrCell)
        objects = self.logic.world.objects
        rules = self.logic.rules

        recruits = copy(city.getUnitClassDictProperty(ItemProperty.RECRUIT))
        recruitsMax = copy(city.getUnitClassDictProperty(ItemProperty.RECRUIT_MAX))
        for cell in city.cells:
            objectValue = objects.getValue(cell)
            if not rules.isTrainingCamp(objectValue):
                continue
            item = objects.getItem(cell)
            if item is None:
                continue
            itemRecruits = item.getUnitClassDictProperty(ItemProperty.RECRUIT)
            for unitClass, count in itemRecruits.items():
                if unitClass not in recruits:
                    recruits[unitClass] = count
                else:
                    recruits[unitClass] += count
            itemRecruitsMax = item.getUnitClassDictProperty(ItemProperty.RECRUIT_MAX)
            for unitClass, count in itemRecruitsMax.items():
                if unitClass not in recruitsMax:
                    recruitsMax[unitClass] = count
                else:
                    recruitsMax[unitClass] += count

        return recruits, recruitsMax

    def setCityRecruitState(self,  cityOrCell: Union[City, Tuple[int, int]], unitClass: UnitClass, count: int = 1):
        city = self.getCity(cityOrCell)
        objects = self.logic.world.objects
        rules = self.logic.rules

        def recruit(counts, maxs):
            if unitClass not in counts:
                return False
            if unitClass not in maxs:
                return False
            if (counts[unitClass] + count) > maxs[unitClass]:
                return False
            counts[unitClass] += count
            return True

        recruits = city.getUnitClassDictProperty(ItemProperty.RECRUIT)
        recruitsMax = city.getUnitClassDictProperty(ItemProperty.RECRUIT_MAX)
        if recruit(recruits, recruitsMax):
            return

        for cell in city.cells:
            objectValue = objects.getValue(cell)
            if not rules.isTrainingCamp(objectValue):
                continue
            item = objects.getItem(cell)
            if item is None:
                continue
            recruits = item.getUnitClassDictProperty(ItemProperty.RECRUIT)
            recruitsMax = item.getUnitClassDictProperty(ItemProperty.RECRUIT_MAX)
            if recruit(recruits, recruitsMax):
                return

    # Player

    def getPlayerCities(self, playerOrId: Union[Player, int]) -> Dict[Tuple[int, int], City]:
        cities = {}
        if isinstance(playerOrId, Player):
            playerId = playerOrId.id
        else:
            playerId = int(playerOrId)
        objects = self.__state.world.objects
        for itemsCell in objects.getItemsByValue(CellValue.OBJECTS_CITY):
            item = itemsCell.item
            if item.playerId != playerId:
                continue
            if not isinstance(item, City):
                continue
            city = cast(City, item)
            cell = self.getCityTopLeft(itemsCell.cells[0])
            cities[cell] = city
        return cities

    def getPlayerUnits(self, playerOrId: Union[Player, int]) -> List[Tuple[Tuple[int, int], Unit]]:
        units = []
        if isinstance(playerOrId, Player):
            playerId = playerOrId.id
        else:
            playerId = int(playerOrId)
        unitsLayer = self.__state.world.units
        for itemCells in unitsLayer.getItemsByPlayers(playerId):
            if not isinstance(itemCells.item, Unit):
                continue
            unit = cast(Unit, itemCells.item)
            units.append((itemCells.cells[0], unit))
        return units

    def computePlayerProduction(self, playerOrId: Union[Player, int]) -> Dict[str, Any]:
        balance: Dict[Resource, int] = defaultdict(int)
        upkeep: Dict[Resource, int] = defaultdict(int)
        total: Dict[Resource, int] = defaultdict(int)
        cities = {}
        for city in self.getPlayerCities(playerOrId).values():
            cityProduction = self.computeCityProduction(city)
            cities[city.name] = {
                "city": city,
                "production": cityProduction
            }
            addResources(total, cityProduction["total"])
            addResources(balance, cityProduction["balance"])

        unitsProduction = []
        for unitInfo in self.getPlayerUnits(playerOrId):
            unit = unitInfo[1]
            unitUpkeep = unit.getResourcesDictProperty(ItemProperty.UPKEEP, {})
            unitsProduction.append({
                "unit": unit,
                "cell": unitInfo[0],
                "upkeep": unitUpkeep
            })
            removeResources(upkeep, unitUpkeep)
            removeResources(balance, unitUpkeep)

        return {
            "total": total,
            "upkeep": upkeep,
            "balance": balance,
            "cities": cities,
            "units": unitsProduction
        }

    # Units

    def removeUnit(self, cell: Tuple[int, int], unit: Unit):
        unitsLayer = self.logic.world.units
        assert unitsLayer.getItem(cell) == unit
        unitsLayer.setValue(cell, CellValue.NONE)
        unitsLayer.notifyCellChanged(cell)
        self.logic.state.notifyUnitDied(cell)

    def getArmyMaxSize(self) -> int:
        return 10

    houseArea = np.array([
        [0, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 0],
    ], dtype=np.int32)

    cityArea: Optional[np.ndarray] = None


def addResources(total: Dict[Resource, int], resources: Union[List[Resource], Dict[Resource, int]], factor: int = 1):
    if type(resources) == defaultdict:
        for resource, count in resources.items():
            total[resource] += count * factor
    elif type(resources) == list:
        for resource in resources:
            if resource in total:
                total[resource] += factor
            else:
                total[resource] = factor
    elif type(resources) == dict:
        for resource, count in resources.items():
            if resource in total:
                total[resource] += count * factor
            else:
                total[resource] = count * factor
    else:
        raise ValueError(f"Invalid type {type(resources)}")


def removeResources(total: Dict[Resource, int], resources: Union[List[Resource], Dict[Resource, int]]):
    if type(resources) == list:
        for resource in resources:
            if resource in total:
                total[resource] -= 1
            else:
                total[resource] = -1
    elif type(resources) == dict:
        for resource, count in resources.items():
            if resource in total:
                total[resource] -= count
            else:
                total[resource] = -count
    else:
        raise ValueError(f"Invalid type {type(resources)}")


tileEffectDescription: Dict[int, str] = {
    CellValue.OBJECTS_HOUSES: "One citizen lives in this house<br>"
                              "If no city handles a house, it will disappear next turn",
    CellValue.OBJECTS_FARM: "Increase food production",
    CellValue.OBJECTS_TREES: "Produce food and wood",
    CellValue.OBJECTS_ROCKS: "Produce stone",
    CellValue.OBJECTS_HILL: "Produce food",

    CellValue.OBJECTS_MILL: "Double food production (up to 8)",
    CellValue.OBJECTS_BAKERY: "Double mills production. Only one bakery can be used by a city.",
    CellValue.OBJECTS_SAWMILL: "Double wood production (up to 8)",
    CellValue.OBJECTS_FACTORY: "Double sawmills production. Only one factory can be used by a city.",
    CellValue.OBJECTS_MARKET: "Double gold production (up to 8)",
    CellValue.OBJECTS_BANK: "Double markets production. Only one bank can be used by a city.",

    CellValue.OBJECTS_CAMP: "Can recruit one spearman per turn",
    CellValue.OBJECTS_BOWCAMP: "Can recruit one bowman per turn",
    CellValue.OBJECTS_SWORDCAMP: "Can recruit one swordman per turn",
    CellValue.OBJECTS_KNIGHTCAMP: "Can recruit one knight per turn",
    CellValue.OBJECTS_SIEGECAMP: "Can recruit one catapult per turn",
}

tileIsProductionBuilding = {
    CellValue.OBJECTS_MILL,
    CellValue.OBJECTS_BAKERY,
    CellValue.OBJECTS_SAWMILL,
    CellValue.OBJECTS_FACTORY,
    CellValue.OBJECTS_MARKET,
    CellValue.OBJECTS_BANK,
}

tileIsTrainingCamp = {
    CellValue.OBJECTS_CAMP,
    CellValue.OBJECTS_BOWCAMP,
    CellValue.OBJECTS_SWORDCAMP,
    CellValue.OBJECTS_KNIGHTCAMP,
    CellValue.OBJECTS_SIEGECAMP,
}
