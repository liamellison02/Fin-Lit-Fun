import random
from unittest import TestCase

from core.constants import CellValue, UnitClass, ItemProperty
from core.state import World, Layer, GameState, Unit


class TestData(TestCase):

    def test_unit(self):
        unit1 = Unit(UnitClass.PIKEMAN, 2)
        unit1.setProperty(ItemProperty.LIFE_POINTS, 2)
        unit1.setProperty(ItemProperty.MOVE_POINTS, 3)
        data = unit1.gatherData()

        unit2 = Unit()
        unit2.takeData(data)
        self.assertEqual(unit1, unit2)

    def test_dense_layer(self):
        layer1 = Layer((4, 5), CellValue.GROUND_SEA)
        for i in range(10):
            x = random.randrange(layer1.width)
            y = random.randrange(layer1.height)
            layer1.setValue((x, y), CellValue.GROUND_EARTH)
        data = layer1.gatherData()
        layer2 = Layer((1, 1), CellValue.GROUND_EARTH)
        layer2.takeData(data)
        self.assertEqual(layer1, layer2)

    def test_sparse_layer(self):
        layer1 = Layer((4, 5), CellValue.GROUND_SEA)
        for i in range(3):
            x = random.randrange(layer1.width)
            y = random.randrange(layer1.height)
            layer1.setValue((x, y), CellValue.GROUND_EARTH)
        data = layer1.gatherData()

        layer2 = Layer((1, 1), CellValue.GROUND_EARTH)
        layer2.takeData(data)
        self.assertEqual(layer1, layer2)

    def test_unit_layer(self):
        layer1 = Layer((4, 5), CellValue.NONE)

        unit = Unit(UnitClass.PIKEMAN, 2)
        unit.setProperty(ItemProperty.LIFE_POINTS, 2)
        unit.setProperty(ItemProperty.MOVE_POINTS, 3)
        x = random.randrange(layer1.width)
        y = random.randrange(layer1.height)
        layer1.setValue((x, y), CellValue.UNITS_UNIT)
        layer1.setItem((x, y), unit)

        unit = Unit(UnitClass.KNIGHT, 2)
        unit.setProperty(ItemProperty.LIFE_POINTS, 7)
        unit.setProperty(ItemProperty.MOVE_POINTS, 13)
        x = random.randrange(layer1.width)
        y = random.randrange(layer1.height)
        layer1.setValue((x, y), CellValue.UNITS_UNIT)
        layer1.setItem((x, y), unit)

        data = layer1.gatherData()

        layer2 = Layer((1, 1), CellValue.GROUND_EARTH)
        layer2.takeData(data)
        self.assertEqual(layer1, layer2)

    def test_state(self):
        world1 = World((4, 5))
        state1 = GameState(world1)

        layer1 = world1.ground
        for i in range(10):
            x = random.randrange(layer1.width)
            y = random.randrange(layer1.height)
            layer1.setValue((x, y), CellValue.GROUND_EARTH)

        layer1 = world1.impassable
        for i in range(3):
            x = random.randrange(layer1.width)
            y = random.randrange(layer1.height)
            layer1.setValue((x, y), CellValue.IMPASSABLE_MOUNTAIN)

        layer1 = world1.units
        unit = Unit(UnitClass.PIKEMAN, 2)
        unit.setProperty(ItemProperty.LIFE_POINTS, 2)
        unit.setProperty(ItemProperty.MOVE_POINTS, 3)
        x = random.randrange(layer1.width)
        y = random.randrange(layer1.height)
        layer1.setValue((x, y), CellValue.UNITS_UNIT)
        layer1.setItem((x, y), unit)

        unit = Unit(UnitClass.KNIGHT, 2)
        unit.setProperty(ItemProperty.LIFE_POINTS, 7)
        unit.setProperty(ItemProperty.MOVE_POINTS, 13)
        x = random.randrange(layer1.width)
        y = random.randrange(layer1.height)
        layer1.setValue((x, y), CellValue.UNITS_UNIT)
        layer1.setItem((x, y), unit)

        data = state1.gatherData()

        world2 = World((1, 1))
        state2 = GameState(world2)
        state2.takeData(data)
        self.assertEqual(state1, state2)
