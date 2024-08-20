import logging
import math
from queue import Queue, PriorityQueue
from typing import Tuple, List, Optional, cast

import numpy as np

from core.constants import CellValue, MoveCost
from core.state import World, Unit, Army


class DistanceMap:

    @staticmethod
    def create(world: World, playerId: int, fromCell: Tuple[int, int], toCell: Optional[Tuple[int, int]] = None,
               radius: int = 31, armySize: int = 1, maxArmySize: int = 1):
        fromX, fromY = fromCell
        if toCell is not None:
            toX, toY = toCell
            area = (
                min(fromX, toX) - radius, min(fromY, toY) - radius,
                max(fromX, toX) + radius + 1, max(fromY, toY) + radius + 1
            )
        else:
            area = (
                fromX - radius, fromY - radius,
                fromX + radius + 1, fromY + radius + 1
            )
        distanceMap = DistanceMap(world, area)
        distanceMap.compute(playerId, fromCell, armySize, maxArmySize)
        return distanceMap

    def __init__(self, world: World, area: Tuple[int, int, int, int]):
        self.__world = world
        x1, y1, x2, y2 = area
        self.__area = (
            max(-1, x1 - 1), max(-1, y1 - 1),
            min(world.width + 1, x2 + 1), min(world.height + 1, y2 + 1)
        )
        self.__width = self.__area[2] - self.__area[0]
        self.__height = self.__area[3] - self.__area[1]
        self.__nodes = np.empty([self.__width, self.__height], dtype=np.int32)
        self.__edges = np.empty([self.__width, self.__height, 8], dtype=np.int32)
        self.__map = np.empty([self.__width, self.__height], dtype=np.int32)

    @property
    def area(self) -> Tuple[int, int, int, int]:
        return self.__area

    @property
    def nodes(self) -> np.ndarray:
        return self.__nodes

    @property
    def edges(self) -> np.ndarray:
        return self.__edges

    @property
    def map(self) -> np.ndarray:
        return self.__map

    def compute(self, playerId: int, source: Tuple[int, int], armySize: int = 1, maxArmySize: int = 1):
        world = self.__world
        area = self.__area
        nodes = self.__nodes
        edges = self.__edges
        map = self.__map

        # Default: infinite cost
        nodes.fill(MoveCost.INFINITE)
        map.fill(MoveCost.INFINITE)
        edges.fill(MoveCost.INFINITE)

        # Ground
        ground = world.ground.getArea(area)
        selection = ground == CellValue.GROUND_EARTH
        nodes[selection] = MoveCost.GROUND

        # Impassable
        impassable = world.impassable.getArea(area)
        selection = impassable != CellValue.NONE
        nodes[selection] = MoveCost.INFINITE

        # Objects
        objects = world.objects.getArea(area)
        selection = objects == CellValue.OBJECTS_ROAD_STONE
        nodes[selection] = MoveCost.ROAD_STONE
        selection = objects == CellValue.OBJECTS_ROAD_DIRT
        nodes[selection] = MoveCost.ROAD_DIRT
        selection = objects == CellValue.OBJECTS_HILL
        selection |= objects == CellValue.OBJECTS_ROCKS
        selection |= objects == CellValue.OBJECTS_TREES
        nodes[selection] = MoveCost.OBJECTS

        # Units (but not the source)
        source = (source[0] - area[0], source[1] - area[1])
        if source[0] < 0 or source[0] >= self.__width \
                or source[1] < 0 or source[1] >= self.__height:
            return
        if maxArmySize == 1:
            units = world.units.getArea(area)
            selection = units != CellValue.NONE
            selection[source] = False
            nodes[selection] = MoveCost.INFINITE
        else:
            items = world.units.getItemsArea(area)
            for itemCells in items:
                item = itemCells.item
                block = False
                if item.playerId != playerId:
                    block = True
                elif isinstance(item, Unit):
                    if (armySize + 1) > maxArmySize:
                        block = True
                elif isinstance(item, Army):
                    size = len(cast(Army, item))
                    if (armySize + size) > maxArmySize:
                        block = True
                else:
                    logging.warning(f"Unsupported unit type {type(item)}")
                    block = True
                if block:
                    for cell in itemCells.cells:
                        p = cell[0] - area[0], cell[1] - area[1]
                        nodes[p] = MoveCost.INFINITE
        nodes[source] = 0


        # Border
        nodes[:, 0] = MoveCost.INFINITE
        nodes[:, -1] = MoveCost.INFINITE
        nodes[0, :] = MoveCost.INFINITE
        nodes[-1, :] = MoveCost.INFINITE

        # Compute moves
        edges[1:, 1:, 0] = np.round(np.maximum(nodes[1:, 1:], nodes[:-1, :-1]) * math.sqrt(2))
        edges[1:, :, 1] = np.maximum(nodes[1:, :], nodes[:-1, :])
        edges[1:, :-1, 2] = np.round(np.maximum(nodes[1:, :-1], nodes[:-1, 1:]) * math.sqrt(2))
        edges[:, 1:, 3] = np.maximum(nodes[:, 1:], nodes[:, :-1])
        edges[:, :-1, 4] = np.maximum(nodes[:, :-1], nodes[:, 1:])
        edges[:-1, 1:, 5] = np.round(np.maximum(nodes[:-1, 1:], nodes[1:, :-1]) * math.sqrt(2))
        edges[:-1, :, 6] = np.maximum(nodes[:-1, :], nodes[1:, :])
        edges[:-1, :-1, 7] = np.round(np.maximum(nodes[:-1, :-1], nodes[1:, 1:]) * math.sqrt(2))

        # Dijkstra
        queue: Queue[Tuple[int, Tuple[int, int]]] = PriorityQueue()
        map[source] = 0
        queue.put((0, source))
        while not queue.empty():
            _, cell = queue.get()
            x, y = cell
            costs = map[x, y] + edges[x, y]

            # Top Left
            cellTo = (x - 1, y - 1)
            cost = int(costs[0])
            if map[cellTo] > cost:
                map[cellTo] = cost
                queue.put((cost, cellTo))

            # Left
            cellTo = (x - 1, y)
            cost = int(costs[1])
            if map[cellTo] > cost:
                map[cellTo] = cost
                queue.put((cost, cellTo))

            # Bottom Left
            cellTo = (x - 1, y + 1)
            cost = int(costs[2])
            if map[cellTo] > cost:
                map[cellTo] = cost
                queue.put((cost, cellTo))

            # Top
            cellTo = (x, y - 1)
            cost = int(costs[3])
            if map[cellTo] > cost:
                map[cellTo] = cost
                queue.put((cost, cellTo))

            # Bottom
            cellTo = (x, y + 1)
            cost = int(costs[4])
            if map[cellTo] > cost:
                map[cellTo] = cost
                queue.put((cost, cellTo))

            # Top Right
            cellTo = (x + 1, y - 1)
            cost = int(costs[5])
            if map[cellTo] > cost:
                map[cellTo] = cost
                queue.put((cost, cellTo))

            # Right
            cellTo = (x + 1, y)
            cost = int(costs[6])
            if map[cellTo] > cost:
                map[cellTo] = cost
                queue.put((cost, cellTo))

            # Bottom Right
            cellTo = (x + 1, y + 1)
            cost = int(costs[7])
            if map[cellTo] > cost:
                map[cellTo] = cost
                queue.put((cost, cellTo))

    def getCost(self, cell: Tuple[int, int]) -> int:
        cell = (cell[0] - self.__area[0], cell[1] - self.__area[1])
        if cell[0] < 0 or cell[0] >= self.__width \
                or cell[1] < 0 or cell[1] >= self.__height:
            return MoveCost.INFINITE
        return int(self.__map[cell])

    def getPath(self, target: Tuple[int, int]) -> \
            Tuple[List[Tuple[int, int]], List[int]]:
        area, map = self.__area, self.__map
        target = (target[0] - area[0], target[1] - area[1])
        if target[0] < 0 or target[0] >= self.__width \
                or target[1] < 0 or target[1] >= self.__height:
            return [], []
        if map[target] >= MoveCost.INFINITE:
            return [], []
        costs, path = [], []
        for i in range(100):
            cost = int(map[target])
            if cost == 0:
                break
            costs.append(cost)
            x, y = target
            path.append((x + area[0], y + area[1]))
            neighbors = np.delete(map[x - 1:x + 2, y - 1:y + 2].flatten(), 4)
            neighbors = neighbors[permutation]
            shift = index2shift[neighbors.argmin()]
            target = (x + shift[0], y + shift[1])

        return path, costs


permutation = np.array([1, 3, 4, 6, 0, 2, 5, 7])
index2shift = [(-1, 0), (0, -1), (0, 1), (1, 0),
               (-1, -1), (-1, 1), (1, -1), (1, 1)]