from typing import List, Tuple, Dict, Any, cast, Optional

from core.state.Layer import Layer
from .Assignments import Assignments
from .item.Army import Army
from .item.City import City
from .item.Item import Item
from .item.TrainingCamp import TrainingCamp
from .item.Unit import Unit
from ..IDataTransfer import IDataTransfer
from ..constants import CellValue, WorldType


class World(IDataTransfer):
    def __init__(self, size: Tuple[int, int], worldType: WorldType = WorldType.STRATEGIC):
        self.__type = worldType
        self.__size = size
        self.__layers = {
            "ground": Layer(size, CellValue.GROUND_SEA),
            "impassable": Layer(size, CellValue.NONE),
            "objects": Layer(size, CellValue.NONE),
            "units": Layer(size, CellValue.NONE),
        }
        self.__assignments = Assignments(size)

    def __eq__(self, other) -> bool:
        if not isinstance(other, World):
            return False
        world = cast(World, other)
        if self.__type != world.__type:
            return False
        if self.__size != world.__size:
            return False
        if len(self.__layers) != len(world.__layers):
            return False
        for name, layer in self.__layers.items():
            if name not in world.__layers:
                return False
            if layer != world.__layers[name]:
                return False
        return True

    @property
    def type(self) -> WorldType:
        return self.__type

    @property
    def size(self) -> Tuple[int, int]:
        return self.__size

    @property
    def width(self) -> int:
        return self.__size[0]

    @property
    def height(self) -> int:
        return self.__size[1]

    def contains(self, coords: Tuple[int, int]) -> bool:
        return 0 <= coords[0] < self.__size[0] and 0 <= coords[1] < self.__size[1]

    @property
    def ground(self) -> Layer:
        return self.__layers["ground"]

    @property
    def impassable(self) -> Layer:
        return self.__layers["impassable"]

    @property
    def objects(self) -> Layer:
        return self.__layers["objects"]

    @property
    def units(self) -> Layer:
        return self.__layers["units"]

    @property
    def layerNames(self) -> List[str]:
        return list(self.__layers.keys())

    @property
    def layers(self) -> List[Layer]:
        return list(self.__layers.values())

    @property
    def assignments(self) -> Assignments:
        return self.__assignments

    def __getitem__(self, name: str) -> Layer:
        return self.getLayer(name)

    def getLayer(self, name: str) -> Layer:
        if name not in self.__layers:
            raise ValueError(f"No layer {name}")
        return self.__layers[name]

    def gatherData(self) -> Dict[str, Any]:
        layersData = {}
        itemsData: Dict[str, Dict[str, Any]] = {}
        for name, layer in self.__layers.items():
            layersData[name] = layer.gatherData(itemsData)
        return {
            "type": self.__type.toName(),
            "width": int(self.__size[0]),
            "height": int(self.__size[1]),
            "items": itemsData,
            "layers": layersData,
            "assignments": self.__assignments.gatherData(itemsData)
        }

    def takeData(self, data: Dict[str, Any]):
        if "type" in data:
            self.__type = WorldType.fromName(data["type"])
        else:
            self.__type = WorldType.STRATEGIC

        self.__size = (int(data["width"]), int(data["height"]))

        itemsData: Dict[int, Item] = {}
        for itemId, itemData in data["items"].items():
            if "type" not in itemData:
                itemType = "unit"
            else:
                itemType = itemData["type"]
            item: Optional[Item] = None
            if itemType == "unit":
                item = Unit()
            elif itemType == "army":
                item = Army()
            elif itemType == "city":
                item = City()
            elif itemType == "trainingCamp":
                item = TrainingCamp()
            else:
                raise ValueError(f"Invalid item type {itemType}")
            item.takeData(itemData)
            itemsData[int(itemId)] = item

        self.__layers.clear()
        for name, layerData in data["layers"].items():
            layer = Layer(self.__size)
            layer.takeData(layerData, itemsData)
            self.__layers[name] = layer

        self.__assignments = Assignments(self.__size)
        self.__assignments.takeData(data["assignments"], itemsData)
