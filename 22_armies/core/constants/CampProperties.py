from typing import Dict

from .CellValue import CellValue
from .UnitClass import UnitClass
from .ItemProperty import ItemProperty, ItemPropertyValue

CampProperties: Dict[CellValue, Dict[ItemProperty, ItemPropertyValue]] = {
    CellValue.OBJECTS_CAMP: {
        ItemProperty.RECRUIT: {UnitClass.PIKEMAN: 0},
        ItemProperty.RECRUIT_MAX: {UnitClass.PIKEMAN: 1},
    },
    CellValue.OBJECTS_BOWCAMP: {
        ItemProperty.RECRUIT: {UnitClass.BOWMAN: 0},
        ItemProperty.RECRUIT_MAX: {UnitClass.BOWMAN: 1},
    },
    CellValue.OBJECTS_SWORDCAMP: {
        ItemProperty.RECRUIT: {UnitClass.SWORDSMAN: 0},
        ItemProperty.RECRUIT_MAX: {UnitClass.SWORDSMAN: 1},
    },
    CellValue.OBJECTS_KNIGHTCAMP: {
        ItemProperty.RECRUIT: {UnitClass.KNIGHT: 0},
        ItemProperty.RECRUIT_MAX: {UnitClass.KNIGHT: 1},
    },
    CellValue.OBJECTS_SIEGECAMP: {
        ItemProperty.RECRUIT: {UnitClass.CATAPULT: 0},
        ItemProperty.RECRUIT_MAX: {UnitClass.CATAPULT: 1},
    },
}
