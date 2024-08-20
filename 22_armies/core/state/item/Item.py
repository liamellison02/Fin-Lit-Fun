import copy
from typing import Dict, Any, cast, Optional, List

from ...IDataTransfer import IDataTransfer
from ...constants import ItemProperty, ItemPropertyValue, Resource, CellValue, UnitClass
from ...constants.ItemProperty import encodeProperties, decodeProperties


class Item(IDataTransfer):

    __slots__ = [
        "__playerId",
        "_properties"
    ]

    def __init__(self, playerId: int = 0):
        self.__playerId = playerId
        self._properties: Dict[ItemProperty, ItemPropertyValue] = {}

    def __eq__(self, other) -> bool:
        if not isinstance(other, Item):
            return False
        item = cast(Item, other)
        if len(self._properties) != len(item._properties):
            return False
        for prop, value in self._properties.items():
            if prop not in other._properties:
                return False
            if value != other._properties[prop]:
                return False
        return True

    def __repr__(self) -> str:
        return "item"

    @property
    def playerId(self) -> int:
        return self.__playerId

    @playerId.setter
    def playerId(self, playerId: int):
        self.__playerId = playerId

    def hasProperty(self, prop: ItemProperty) -> bool:
        return prop in self._properties

    def setProperty(self, prop: ItemProperty, value: ItemPropertyValue):
        if type(value) != str and type(value) != int and type(value) != list:
            raise ValueError(f"Invalid value type {type(value)} for property {prop.toName()}")
        self._properties[prop] = value

    def setProperties(self, properties: Dict[ItemProperty, ItemPropertyValue]):
        self._properties = copy.deepcopy(properties)

    def setIntProperty(self, prop: ItemProperty, value: int):
        self.setProperty(prop, value)

    def getProperty(self, prop: ItemProperty, defaultValue: Optional[ItemPropertyValue] = None) -> ItemPropertyValue:
        if prop in self._properties:
            return self._properties[prop]
        if defaultValue is None:
            raise ValueError(f"No property {prop.toName()}")
        return defaultValue

    def getStringProperty(self, prop: ItemProperty, defaultValue: Optional[str] = None) -> str:
        return cast(str, self.getProperty(prop, defaultValue))

    def getIntProperty(self, prop: ItemProperty, defaultValue: Optional[int] = None) -> int:
        return cast(int, self.getProperty(prop, defaultValue))

    def getIntListProperty(self, prop: ItemProperty, defaultValue: Optional[List[int]] = None) -> List[int]:
        if defaultValue is None:
            defaultValue = []
        return cast(List[int], self.getProperty(prop, defaultValue))

    def getUnitClassDictProperty(self, prop: ItemProperty, defaultValue: Optional[Dict[UnitClass, int]] = None) -> Dict[UnitClass, int]:
        if defaultValue is None:
            defaultValue = {}
        return cast(Dict[UnitClass, int], self.getProperty(prop, defaultValue))

    def getResourcesListProperty(self, prop: ItemProperty, defaultValue: Optional[List[Resource]] = None) -> List[Resource]:
        if defaultValue is None:
            defaultValue = []
        return cast(List[Resource], self.getProperty(prop, defaultValue))

    def getResourcesDictProperty(self, prop: ItemProperty, defaultValue: Optional[Dict[Resource, int]] = None) -> Dict[Resource, int]:
        if defaultValue is None:
            defaultValue = {}
        return cast(Dict[Resource, int], self.getProperty(prop, defaultValue))

    def getResourcesDictPerValProperty(self, prop: ItemProperty, defaultValue: Optional[Dict[int, Dict[Resource, int]]] = None) -> Dict[int, Dict[Resource, int]]:
        if defaultValue is None:
            defaultValue = {}
        return cast(Dict[int, Dict[Resource, int]], self.getProperty(prop, defaultValue))

    # Data transfer

    def gatherData(self) -> Dict[str, Any]:
        return {
            "playerId": self.__playerId,
            "properties": encodeProperties(self._properties)
        }

    def takeData(self, data: Dict[str, Any]):
        self.__playerId = int(data['playerId'])
        assert 0 <= self.__playerId < 5, f"Invalid player id {self.__playerId} in unit data"
        self._properties = decodeProperties(data['properties'])
