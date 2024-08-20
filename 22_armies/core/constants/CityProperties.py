from typing import Dict

from .CellValue import CellValue
from .CityClass import CityClass
from .ItemProperty import ItemProperty, ItemPropertyValue
from .Resource import Resource
from .UnitClass import UnitClass

CityProperties: Dict[CityClass, Dict[ItemProperty, ItemPropertyValue]] = {
    CityClass.DEFAULT: {
        ItemProperty.NAME: "NoName",
        ItemProperty.CITIZEN_COUNT: 0,
        ItemProperty.CITIZEN_COUNT_MAX: 28,
        ItemProperty.WORKER_COUNT: 0,
        ItemProperty.WORKER_COUNT_MAX: 28,
        ItemProperty.WALL_LEVEL: 0,
        ItemProperty.WALL_LEVEL_MAX: 2,
        ItemProperty.MERCHANT_PRODUCTION: [Resource.GOLD, Resource.GOLD],
        ItemProperty.BASE_PRODUCTION: [Resource.FOOD, Resource.FOOD, Resource.GOLD, Resource.GOLD],
        ItemProperty.GRANARY_FOOD: 0,
        ItemProperty.GRANARY_FOOD_MAX: 5,
        ItemProperty.GROWTH_POINTS: 0,
        ItemProperty.GROWTH_POINTS_RATE: 4,
        ItemProperty.GROWTH_POINTS_MIN: 1,
        ItemProperty.GROWTH_POINTS_MAX: 4,
        ItemProperty.CITIZEN_UPKEEP: [Resource.FOOD, Resource.FOOD],
        ItemProperty.BUILDINGS_UPKEEP: {
            CellValue.OBJECTS_MILL: {Resource.WOOD: 1},
            CellValue.OBJECTS_BAKERY: {Resource.WOOD: 2, Resource.STONE: 1},
            CellValue.OBJECTS_SAWMILL: {Resource.WOOD: 1},
            CellValue.OBJECTS_FACTORY: {Resource.WOOD: 2, Resource.STONE: 1},
            CellValue.OBJECTS_MARKET: {Resource.WOOD: 1},
            CellValue.OBJECTS_BANK: {Resource.WOOD: 2, Resource.STONE: 1},
        },
        ItemProperty.RECRUIT: {UnitClass.WORKER: 0},
        ItemProperty.RECRUIT_MAX: {UnitClass.WORKER: 1},
    }
}
