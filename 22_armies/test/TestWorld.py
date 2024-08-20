import random
from unittest import TestCase

import numpy as np

from core.constants import CellValue, cellValueRanges
from core.logic import Logic
from core.state import World, Layer, GameState
from tools.tilecodes import mask8, code8, combine8, mask4, combine4, code4, code4np, code8np


class TestWorld(TestCase):

    def test_setget(self):
        world = World((14, 7))
        self.assertEqual(14, world.width)
        self.assertEqual(7, world.height)

        ground = world.ground
        for y in range(world.height):
            for x in range(world.width):
                self.assertEqual(CellValue.GROUND_SEA, ground[x, y])

        ground[3, 4] = CellValue.GROUND_EARTH
        for y in range(world.height):
            for x in range(world.width):
                if x == 3 and y == 4:
                    self.assertEqual(CellValue.GROUND_EARTH, ground[x, y])
                else:
                    self.assertEqual(CellValue.GROUND_SEA, ground[x, y])

    def test_logic(self):
        world = World((13, 11))
        state = GameState(world)
        logic = Logic(state)
        ground = world.ground
        ground.fill(CellValue.GROUND_EARTH)
        for layerName in world.layerNames:
            if layerName in ["ground", "units", "buildings"]:
                continue
            coords = (
                random.randint(0, world.width - 1),
                random.randint(0, world.height - 2)
            )
            valueRange = cellValueRanges[layerName]
            minValue = valueRange[0]
            maxValue = valueRange[1]
            value = CellValue(random.randint(minValue, maxValue - 1))
            Command = logic.getSetLayerCellCommand(layerName)

            command = Command(coords, value)
            logic.addCommand(command)
            logic.executeCommands()
            layer = world[layerName]
            self.assertEqual(value, layer[coords])

            command = Command(coords, CellValue.NONE)
            logic.addCommand(command)
            logic.executeCommands()
            layer = world[layerName]
            self.assertEqual(CellValue.NONE, layer[coords])

    def test_codes4(self):
        # Build world
        layer = Layer((41, 27), CellValue.NONE)
        values = [
            CellValue.NONE,
            CellValue.OBJECTS_HOUSES,
            CellValue.OBJECTS_ROAD_DIRT,
            CellValue.OBJECTS_ROAD_STONE,
        ]
        for y in range(layer.height):
            for x in range(layer.width):
                index = random.randrange(len(values))
                layer[x, y] = values[index]
        # Check
        allNeighbors = layer.getAllNeighbors4()
        masks = np.equal(allNeighbors, CellValue.OBJECTS_ROAD_DIRT)
        masks = np.logical_or(masks, np.equal(allNeighbors, CellValue.OBJECTS_ROAD_STONE))
        codes = code4np(masks)
        for y in range(layer.height):
            for x in range(layer.width):
                code = int(codes[x, y])

                neighbors = layer.getNeighbors4((x, y))
                assert (allNeighbors[x, y] == neighbors).all()
                mask = mask4(neighbors, CellValue.OBJECTS_ROAD_DIRT)
                mask = combine4(mask, mask4(neighbors, CellValue.OBJECTS_ROAD_STONE))
                assert (masks[x, y] == mask).all()
                check = code4(mask)
                self.assertEqual(code, check)

    def test_codes8(self):
        # Build world
        layer = Layer((41, 27), CellValue.NONE)
        values = [
            CellValue.NONE,
            CellValue.OBJECTS_HOUSES,
            CellValue.OBJECTS_ROAD_DIRT,
            CellValue.OBJECTS_ROAD_STONE,
        ]
        for y in range(layer.height):
            for x in range(layer.width):
                index = random.randrange(len(values))
                layer[x, y] = values[index]

        # Check
        allNeighbors = layer.getAllNeighbors8()
        masks = np.equal(allNeighbors, CellValue.OBJECTS_ROAD_DIRT)
        masks = np.logical_or(masks, np.equal(allNeighbors, CellValue.OBJECTS_ROAD_STONE))
        codes = code8np(masks)
        for y in range(layer.height):
            for x in range(layer.width):
                code = int(codes[x, y])

                neighbors = layer.getNeighbors8((x, y))
                mask = mask8(neighbors, CellValue.OBJECTS_ROAD_DIRT)
                mask = combine8(mask, mask8(neighbors, CellValue.OBJECTS_ROAD_STONE))
                check = code8(mask)
                self.assertEqual(code, check)
