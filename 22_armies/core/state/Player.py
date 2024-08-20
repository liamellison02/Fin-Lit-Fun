from collections import defaultdict
from typing import Dict, Any, Union, cast

from ..constants import Resource


class Player:

    def __init__(self, idOrDict: Union[int, Dict[str, Any]]):
        if type(idOrDict) == int:
            self.__id = idOrDict
            self.__name = PlayerId2Name[idOrDict]
            self.__resources: Dict[Resource, int] = defaultdict(int)
        elif type(idOrDict) == dict:
            self.takeData(idOrDict)
        else:
            raise ValueError("Invalid data type")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        player = cast(Player, other)
        if self.__id != player.__id:
            return False
        if self.__resources != player.__resources:
            return False
        return True

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def resources(self) -> Dict[Resource, int]:
        return self.__resources

    @resources.setter
    def resources(self, res: Dict[Resource, int]):
        self.__resources = res

    def getResource(self, resource: Resource) -> int:
        return self.__resources[resource]

    def setResource(self, resource: Resource, amount: int):
        if amount != 0:
            self.__resources[resource] = int(amount)
        elif resource in self.__resources:
            del self.__resources[resource]

    def addResource(self, resource: Resource, amount: int):
        self.__resources[resource] += amount

    def hasResources(self, resources: Dict[Resource, int]) -> bool:
        for resource, amount in resources.items():
            if amount <= 0:
                continue
            if resource not in self.__resources:
                return False
            if self.__resources[resource] - amount < 0:
                return False
        return True

    def removeResources(self, resources: Dict[Resource, int]):
        for resource, amount in resources.items():
            self.__resources[resource] -= amount

    def gatherData(self) -> Dict[str, Any]:
        return {
            "id": self.__id,
            "name": self.__name,
            "resources": {resource.toName(): amount for resource, amount in self.__resources.items()}
        }

    def takeData(self, data: Dict[str, Any]):
        self.__id = int(data["id"])
        self.__name = str(data["name"])
        resources = {Resource.fromName(name): amount for name, amount in data["resources"].items()}
        self.__resources = defaultdict(int, resources)


PlayerId2Name = {
    0: "Gray",
    1: "the blue player",
    2: "the red player",
    3: "the yellow player",
    4: "the green player"
}