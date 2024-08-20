from __future__ import annotations
from enum import IntEnum

from typing import List


class CellValue(IntEnum):
    NONE = 0

    GROUND_SEA = 101
    GROUND_EARTH = 102

    IMPASSABLE_RIVER = 201
    IMPASSABLE_POND = 202
    IMPASSABLE_MOUNTAIN = 203

    OBJECTS_CITY = 301
    OBJECTS_HILL = 302
    OBJECTS_ROCKS = 303
    OBJECTS_TREES = 304
    OBJECTS_HOUSES = 305
    OBJECTS_ROAD_DIRT = 306
    OBJECTS_ROAD_STONE = 307
    OBJECTS_FARM = 308

    OBJECTS_MILL = 309
    OBJECTS_BAKERY = 310
    OBJECTS_SAWMILL = 311
    OBJECTS_FACTORY = 312
    OBJECTS_MARKET = 313
    OBJECTS_BANK = 314

    OBJECTS_CAMP = 315
    OBJECTS_BOWCAMP = 316
    OBJECTS_SWORDCAMP = 317
    OBJECTS_KNIGHTCAMP = 318
    OBJECTS_SIEGECAMP = 319

    UNITS_UNIT = 401
    UNITS_ARMY = 402

    MAX_VALUE = 1000

    @staticmethod
    def fromName(name: str) -> CellValue:
        try:
            return CellValue[name]
        except KeyError:
            raise ValueError(f"Invalid cell value name {name}")

    def toName(self) -> str:
        return self.name

    @staticmethod
    def getString(cellValue: int):
        try:
            cellValue = CellValue(cellValue)
            return cellValueStr[cellValue]
        except:
            return "?"

    def __str__(self):
        if self not in cellValueStr:
            return "?"
        return cellValueStr[self]


cellValueStr = {
    CellValue.NONE: "Empty",

    CellValue.GROUND_SEA: "Sea",
    CellValue.GROUND_EARTH: "Earth",

    CellValue.IMPASSABLE_RIVER: "River",
    CellValue.IMPASSABLE_POND: "Pond",
    CellValue.IMPASSABLE_MOUNTAIN: "Mountain",

    CellValue.OBJECTS_CITY: "City",
    CellValue.OBJECTS_HILL: "Hill",
    CellValue.OBJECTS_ROCKS: "Stones",
    CellValue.OBJECTS_TREES: "Forest",
    CellValue.OBJECTS_HOUSES: "House",
    CellValue.OBJECTS_ROAD_DIRT: "Road",
    CellValue.OBJECTS_ROAD_STONE: "Stone road",
    CellValue.OBJECTS_FARM: "Farm",

    CellValue.OBJECTS_MILL: "Mill",
    CellValue.OBJECTS_BAKERY: "Bakery",
    CellValue.OBJECTS_SAWMILL: "Sawmill",
    CellValue.OBJECTS_FACTORY: "Factory",
    CellValue.OBJECTS_MARKET: "Market",
    CellValue.OBJECTS_BANK: "Bank",

    CellValue.OBJECTS_CAMP: "Pikemen training camp",
    CellValue.OBJECTS_BOWCAMP: "Bowmen training camp",
    CellValue.OBJECTS_SWORDCAMP: "Swordmen training camp",
    CellValue.OBJECTS_KNIGHTCAMP: "Knights training camp",
    CellValue.OBJECTS_SIEGECAMP: "Siege workshop",

    CellValue.UNITS_UNIT: "Unit"
}

cellValueRanges = {
    "ground": (101, 103),
    "impassable": (201, 204),
    "objects": (301, 320),
    "units": (401, 402),
}


def checkCellValue(layer: str, value: CellValue):
    if layer != "ground" and value == CellValue.NONE:
        return True
    valueRange = cellValueRanges[layer]
    return valueRange[0] <= value < valueRange[1]


def getCellValues(layer: str) -> List[int]:
    values: List[int] = []
    if layer != "ground":
        values.append(CellValue.NONE)
    for value in range(*cellValueRanges[layer]):
        values.append(value)
    return values