from math import sqrt
from unittest import TestCase

import pygame.image
from pygame.surface import Surface

from core.constants import CellValue
from core.logic import Logic
from core.state import World, GameState
from test.misc import compareSurfaces
from ui import Theme
from ui.component.world import WorldComponent


class TestRender(TestCase):

    def setUp(self) -> None:
        self.theme = Theme()
        tileSize = self.theme.getTileset("ground").tileSize
        self.theme.viewSize = (20 * tileSize[0], 15 * tileSize[1])

        self.world = World((20, 15))
        self.state = GameState(self.world)
        self.logic = Logic(self.state)
        ground = self.world.ground.cells
        for y in range(0, 15):
            for x in range(0, 20):
                x0, y0 = x - 9, y - 6
                d = sqrt(x0 * x0 + 2 * y0 * y0)
                if d < 7:
                    ground[x, y] = CellValue.GROUND_EARTH

        impassable = self.world.impassable.cells
        impassable[6, 3:10] = CellValue.IMPASSABLE_MOUNTAIN
        impassable[12, 3:10] = CellValue.IMPASSABLE_MOUNTAIN
        impassable[3:16, 6] = CellValue.IMPASSABLE_RIVER
        impassable[9, 2:11] = CellValue.IMPASSABLE_RIVER
        impassable[3, 4:9] = CellValue.IMPASSABLE_RIVER
        impassable[15, 4:9] = CellValue.IMPASSABLE_RIVER
        impassable[5:14, 2] = CellValue.IMPASSABLE_RIVER
        impassable[5:14, 10] = CellValue.IMPASSABLE_RIVER

        objects = self.world.objects.cells
        objects[7:12, 4:9] = CellValue.OBJECTS_ROAD_STONE
        objects[8:11, 5:8] = CellValue.OBJECTS_ROAD_DIRT
        objects[9, 6] = CellValue.NONE

    def test_layer(self):
        worldComponent = WorldComponent(self.theme, self.logic)
        worldComponent.viewChanged((35, 18))

        surface = Surface(self.theme.viewSize)
        worldComponent.render(surface)
        worldComponent.dispose()

        if False:  # Update test data
            pygame.image.save(surface, "test/data/world.png")
        #pygame.image.save(surface, "test.png")
        check = pygame.image.load("test/data/world.png")
        self.assertTrue(compareSurfaces(surface, check))

