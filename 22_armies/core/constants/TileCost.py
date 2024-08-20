from typing import Dict

from .CellValue import CellValue
from .Resource import Resource

tileCost: Dict[int, Dict[Resource, int]] = {
    CellValue.NONE: {Resource.GOLD: 10},

    CellValue.OBJECTS_TREES: {Resource.GOLD: 10},
    CellValue.OBJECTS_ROAD_DIRT: {},
    CellValue.OBJECTS_ROAD_STONE: {Resource.STONE: 1},
    CellValue.OBJECTS_FARM: {},

    CellValue.OBJECTS_MILL: {Resource.WOOD: 10},
    CellValue.OBJECTS_BAKERY: {Resource.STONE: 40},
    CellValue.OBJECTS_SAWMILL: {Resource.WOOD: 10},
    CellValue.OBJECTS_FACTORY: {Resource.STONE: 40},
    CellValue.OBJECTS_MARKET: {Resource.WOOD: 10},
    CellValue.OBJECTS_BANK: {Resource.STONE: 40},

    CellValue.OBJECTS_CAMP: {Resource.WOOD: 10},
    CellValue.OBJECTS_BOWCAMP: {Resource.WOOD: 10},
    CellValue.OBJECTS_SWORDCAMP: {Resource.WOOD: 10, Resource.STONE: 10},
    CellValue.OBJECTS_KNIGHTCAMP: {Resource.WOOD: 20, Resource.STONE: 20},
    CellValue.OBJECTS_SIEGECAMP: {Resource.WOOD: 20, Resource.GOLD: 20},
}