from __future__ import annotations

import logging
from collections import defaultdict
from typing import cast, Dict, Optional, List, Tuple

import numpy as np

from core.constants import ItemProperty, Resource, CellValue
from core.logic.Command import Command, STATE_PRIORITY
from core.logic.Logic import Logic
from core.logic.Rules import addResources
from core.logic.command import AssignCell, UnassignCell
from core.state import Unit, Player, Army


class NextTurn(Command):

    def priority(self) -> int:
        return STATE_PRIORITY

    def check(self, logic: Logic) -> bool:
        state = logic.state
        if state.playerId not in state.playerIds:
            logging.error("Current player id not in state player list!")
            return False
        return True

    def execute(self, logic: Logic):
        state = logic.state

        # Next player id / turn
        playerIds = state.playerIds
        playerIndex = playerIds.index(state.playerId) + 1
        if playerIndex >= len(playerIds):
            playerIndex = 0
            self.updateAll(logic)

        state.playerId = playerIds[playerIndex]

        # Next turn
        state.notifyTurnChanged()

    def updateAll(self, logic: Logic):
        state = logic.state
        rules = logic.rules

        def updateUnit(unit):
            if unit.hasProperty(ItemProperty.MOVE_POINTS):
                points = unit.getIntProperty(ItemProperty.MAX_MOVE_POINTS)
                unit.setIntProperty(ItemProperty.MOVE_POINTS, points)
            if unit.hasProperty(ItemProperty.ACTION_POINTS):
                points = unit.getIntProperty(ItemProperty.MAX_ACTION_POINTS)
                unit.setIntProperty(ItemProperty.ACTION_POINTS, points)

        # Reset unit points
        for itemCells in state.world.units.getItems():
            if not isinstance(itemCells.item, Unit):
                continue
            item = itemCells.item
            if isinstance(item, Unit):
                unit = cast(Unit, item)
                updateUnit(unit)
            elif isinstance(item, Army):
                army = cast(Army, item)
                for unit in army.units:
                    updateUnit(unit)

        # Update resources
        for player in state.players:
            while not self.updatePlayer(logic, player):
                pass

        # Update cities
        for cityCell, city in rules.getCities().items():
            self.updateCity(logic, cityCell, city)

        # Remove unassigned houses
        objects = logic.world.objects
        assigments = logic.world.assignments
        for cell in objects.findValues(CellValue.OBJECTS_HOUSES):
            if not assigments.hasAssignment(cell):
                objects.setValue(cell, CellValue.NONE)
                objects.notifyCellChanged(cell)

        # Reset training camp recruits
        for cell in rules.findTrainingCamps():
            item = objects.getItem(cell)
            if item is None:
                continue
            recruits = item.getUnitClassDictProperty(ItemProperty.RECRUIT)
            for unitClass in recruits:
                recruits[unitClass] = 0

        state.turn = state.turn + 1

    def updatePlayer(self, logic: Logic, player: Player) -> bool:
        rules = logic.rules
        playerCities = rules.getPlayerCities(player)

        # Production for current turn
        balance: Dict[Resource, int] = defaultdict(int)
        for city in playerCities.values():
            cityProduction = rules.computeCityProduction(city)
            addResources(balance, cityProduction["balance"])

        # Compute player resources
        playerResources = player.resources.copy()
        addResources(playerResources, balance)
        if Resource.FOOD in playerResources:
            del playerResources[Resource.FOOD]

        # Check if a player resource goes negative
        negativeResource: Optional[Resource] = None
        for resource, amount in playerResources.items():
            if amount < 0:
                negativeResource = resource

        # Disable a building if we have a negative resource
        if negativeResource is not None:
            for cityCell, city in playerCities.items():
                buildings = rules.getCityBuildings(city)
                buildingsUpkeep = city.getResourcesDictPerValProperty(ItemProperty.BUILDINGS_UPKEEP)
                for building in buildings:
                    value = building[1]
                    if value not in buildingsUpkeep:
                        continue
                    buildingUpkeep = buildingsUpkeep[value]
                    if negativeResource not in buildingUpkeep:
                        continue
                    if buildingUpkeep[negativeResource] <= 0:
                        continue
                    command = UnassignCell(cityCell, building[0], ignorePlayerId=True)
                    if command.check(logic):
                        command.execute(logic)
                        return False

        # Update player resources
        player.resources = playerResources

        # List units with upkeep and cost
        units: List[Tuple[Tuple[int, int], Unit, Dict[Resource, int], int]] = []
        for unitInfo in rules.getPlayerUnits(player):
            unitCell = unitInfo[0]
            unit = unitInfo[1]
            unitUpkeep = unit.getResourcesDictProperty(ItemProperty.UPKEEP)
            costs = unit.getResourcesDictProperty(ItemProperty.COST)
            unitCost = sum(cost for cost in costs.values())
            units.append((unitCell, unit, unitUpkeep, unitCost))

        # Units:
        for unitInfos in sorted(units, key=lambda info: info[3], reverse=True):
            upkeep = unitInfos[2]
            if player.hasResources(upkeep):
                player.removeResources(upkeep)
            else:
                rules.removeUnit(unitInfos[0], unitInfos[1])

        return True

    def updateCity(self, logic: Logic, cityCell, city):
        rules = logic.rules
        world = logic.world
        objects = world.objects

        recruits = city.getProperty(ItemProperty.RECRUIT, {})
        for unitClass in recruits:
            recruits[unitClass] = 0

        production = rules.computeCityProduction(city)
        foodBalance = production["balance"][Resource.FOOD]
        granary = city.getProperty(ItemProperty.GRANARY_FOOD, 0)
        granaryMax = rules.getCityGranarySize(city)
        granary = min(granaryMax, granary + foodBalance)
        if granary >= 0:
            city.setProperty(ItemProperty.GRANARY_FOOD, granary)

            growth = city.getProperty(ItemProperty.GROWTH_POINTS, 0) + 1
            growthMax = rules.getCityGrowthMax(city)
            if growth < growthMax:
                city.setProperty(ItemProperty.GROWTH_POINTS, growth)
                return
            freeCells = rules.findCityTilesforNewHouses(cityCell)
            if not freeCells:
                return

            randomSeed = (3 * cityCell[0] + 7 * cityCell[1]) % len(freeCells)
            freeCell = freeCells[randomSeed]
            objects.setValue(freeCell, CellValue.OBJECTS_HOUSES)
            objects.notifyCellChanged(freeCell)

            assign = AssignCell(cityCell, freeCell, ignorePlayerId=True)
            assert assign.check(logic)
            assign.execute(logic)

            rules.autoAssignCitizens(cityCell)

            city.setProperty(ItemProperty.GROWTH_POINTS, 0)
        else:
            city.setProperty(ItemProperty.GROWTH_POINTS, 0)
            city.setProperty(ItemProperty.GRANARY_FOOD, 0)

            # Remove one citizen per -2 food
            while granary < 0:
                if city.getCitizenCount() <= 0:
                    break

                # Remove a worker if all citizens are workers
                if city.getCitizenCount() == city.getWorkerCount():
                    rules.removeCityWorker(cityCell)

                # Unassign a city house
                for cell in city.cells:
                    if objects.getValue(cell) != CellValue.OBJECTS_HOUSES:
                        continue
                    unassign = UnassignCell(cityCell, cell, ignorePlayerId=True)
                    assert unassign.check(logic)
                    unassign.execute(logic)
                    break
                granary += 2



