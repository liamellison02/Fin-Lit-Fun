from typing import List

from core.constants import Resource
from core.state import Item


class SelectionItem(Item):
    __slots__ = [
        "__resources"
    ]

    def __init__(self, resources: List[Resource], playerId: int):
        super().__init__(playerId)
        self.__resources = resources

    @property
    def resources(self) -> List[Resource]:
        return self.__resources

