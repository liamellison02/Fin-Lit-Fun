from __future__ import annotations

import typing
from enum import IntEnum, auto
from typing import Union, List, TypeAlias, Dict, Any, cast

from .CellValue import CellValue
from .Resource import Resource
from .UnitClass import UnitClass

ItemPropertyValue: TypeAlias = Union[
    str,
    int,
    List[int],
    List[CellValue],
    List[Resource],
    Dict[Resource, int],
    Dict[UnitClass, int],
    Dict[int, Dict[Resource, int]],
    Dict[CellValue, Dict[Resource, int]]
]


class ItemProperty(IntEnum):
    NAME = 1

    LIFE_POINTS = auto()
    MAX_LIFE_POINTS = auto()
    MOVE_POINTS = auto()
    MAX_MOVE_POINTS = auto()
    ACTION_POINTS = auto()
    MAX_ACTION_POINTS = auto()

    MELEE_ATTACK = auto()
    MELEE_DEFENSE = auto()
    MELEE_RANGE = auto()

    BOW_ATTACK = auto()
    BOW_DEFENSE = auto()
    BOW_RANGE = auto()

    MOUNT_ATTACK = auto()
    MOUNT_DEFENSE = auto()
    MOUNT_RANGE = auto()

    SIEGE_ATTACK = auto()
    SIEGE_DEFENSE = auto()
    SIEGE_RANGE = auto()

    COST = auto()
    UPKEEP = auto()

    WALL_LEVEL = auto()
    WALL_LEVEL_MAX = auto()

    CITIZEN_COUNT = auto()
    CITIZEN_COUNT_MAX = auto()
    WORKER_COUNT = auto()
    WORKER_COUNT_MAX = auto()
    BASE_PRODUCTION = auto()
    MERCHANT_PRODUCTION = auto()
    GRANARY_FOOD = auto()
    GRANARY_FOOD_MAX = auto()
    GROWTH_POINTS = auto()
    GROWTH_POINTS_RATE = auto()
    GROWTH_POINTS_MIN = auto()
    GROWTH_POINTS_MAX = auto()
    CITIZEN_UPKEEP = auto()

    RECRUIT = auto()
    RECRUIT_MAX = auto()
    DISBAND = auto()
    BUILD = auto()
    BUILDINGS_UPKEEP = auto()

    @staticmethod
    def fromName(name: str) -> ItemProperty:
        if name not in itemPropertyName2Id:
            raise ValueError(f"Invalid item property name {name}")
        return itemPropertyName2Id[name]

    def toName(self) -> str:
        return itemPropertyId2Name[self]


itemPropertyId2Name = {}
itemPropertyName2Id = {}
for property in ItemProperty:
    itemPropertyId2Name[property.value] = property.name
    itemPropertyName2Id[property.name] = property


@typing.no_type_check
def encodeProperties(properties: Dict[ItemProperty, ItemPropertyValue]) -> Dict[str, Any]:
    out = {}
    for prop, value in properties.items():
        if type(value) == list:
            container = []
            for item in value:
                if isinstance(item, Resource):
                    resource = cast(Resource, item)
                    container.append(resource.toName())
                elif isinstance(item, CellValue):
                    cellValue = cast(CellValue, item)
                    container.append(cellValue.toName())
                else:
                    raise ValueError(f"Unsupported type {type(item)} in list")
            out[prop.toName()] = container
        elif type(value) == dict:
            dict_ = cast(Dict, value)
            container = {}
            for item, value in dict_.items():
                if isinstance(item, Resource):
                    assert type(value) == int
                    resource = cast(Resource, item)
                    container[resource.toName()] = value
                elif isinstance(item, UnitClass):
                    assert type(value) == int
                    unitClass = cast(UnitClass, item)
                    container[unitClass.toName()] = value
                elif isinstance(item, CellValue):
                    assert isinstance(value, dict), f"Invalid value type {type(value)}"
                    dict2 = cast(dict, value)
                    container2 = {}
                    for item2, value2 in dict2.items():
                        assert isinstance(item2, Resource)
                        assert type(value2) == int
                        resource = cast(Resource, item2)
                        container2[resource.toName()] = value2
                    container[item.toName()] = container2
                else:
                    raise ValueError(f"Unsupported value type {type(item)} of {item}")
            out[prop.toName()] = container
        elif type(value) in [int, bool, str]:
            out[prop.toName()] = value
        else:
            raise ValueError(f"Unsupported value type {type(value)} for {prop.toName()}")
    return out


@typing.no_type_check
def decodeProperties(data: Dict[str, Any]) -> Dict[ItemProperty, ItemPropertyValue]:
    properties = {}

    for name, value in data.items():
        prop = ItemProperty.fromName(name)
        if type(value) == list:
            list_ = cast(List, value)
            container = []
            if "PRODUCTION" in name or "UPKEEP" in name:
                for item in list_:
                    resource = Resource.fromName(item)
                    container.append(resource)
            else:
                for item in list_:
                    cellValue = CellValue.fromName(item)
                    container.append(cellValue)
            properties[prop] = container
        elif type(value) == dict:
            dict_ = cast(Dict, value)
            container = {}
            if name == "BUILDINGS_UPKEEP":
                for item, resources in dict_.items():
                    container2 = {}
                    for item2, count in resources.items():
                        resource = Resource.fromName(item2)
                        container2[resource] = count
                    cellValue = CellValue.fromName(item)
                    container[cellValue] = container2
            elif "RECRUIT" in name:
                for item, count in dict_.items():
                    unitClass = UnitClass.fromName(item)
                    container[unitClass] = count
            else:
                for item, count in dict_.items():
                    resource = Resource.fromName(item)
                    container[resource] = count
            properties[prop] = container
        elif type(value) in [int, bool, str]:
            properties[prop] = value
        else:
            raise ValueError(f"Unsupported value type {type(value)} for {name}")

    return properties


attackProperties = {
    ItemProperty.MELEE_ATTACK: {
        "defense": ItemProperty.MELEE_DEFENSE,
        "range": ItemProperty.MELEE_RANGE,
    },
    ItemProperty.BOW_ATTACK: {
        "defense": ItemProperty.BOW_DEFENSE,
        "range": ItemProperty.BOW_RANGE,
    },
    ItemProperty.MOUNT_ATTACK: {
        "defense": ItemProperty.MOUNT_DEFENSE,
        "range": ItemProperty.MOUNT_RANGE,
    },
    ItemProperty.SIEGE_ATTACK: {
        "defense": ItemProperty.SIEGE_DEFENSE,
        "range": ItemProperty.SIEGE_RANGE,
    },
}
