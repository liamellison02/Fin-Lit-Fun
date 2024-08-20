from .CellValue import CellValue
from .Resource import Resource

tileProduction = {
    CellValue.GROUND_EARTH: {
        CellValue.NONE: {
            CellValue.NONE: [Resource.FOOD, Resource.FOOD],
            CellValue.OBJECTS_HILL: [Resource.FOOD],
            CellValue.OBJECTS_ROCKS: [Resource.STONE, Resource.STONE],
            CellValue.OBJECTS_TREES: [Resource.WOOD, Resource.WOOD, Resource.FOOD],
            CellValue.OBJECTS_MILL: [Resource.FOOD, Resource.FOOD, Resource.FOOD, Resource.GOLD],
            CellValue.OBJECTS_ROAD_DIRT: [Resource.FOOD, Resource.FOOD, Resource.GOLD],
            CellValue.OBJECTS_ROAD_STONE: [Resource.FOOD, Resource.FOOD, Resource.GOLD, Resource.GOLD],
            CellValue.OBJECTS_FARM: [Resource.FOOD, Resource.FOOD, Resource.FOOD, Resource.FOOD],
        },
        CellValue.IMPASSABLE_POND: {
            CellValue.NONE: [Resource.FOOD, Resource.FOOD, Resource.FOOD],
        },
        CellValue.IMPASSABLE_RIVER: {
            CellValue.NONE: [Resource.FOOD, Resource.FOOD, Resource.GOLD],
        },
        CellValue.IMPASSABLE_MOUNTAIN: {
            CellValue.NONE: [Resource.STONE],
        }
    },
    CellValue.GROUND_SEA: {
        CellValue.NONE: {
            CellValue.NONE: [Resource.FOOD, Resource.GOLD]
        }
    }
}