from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from .Logic import Logic

STATE_PRIORITY = 1

WORLD_PRIORITY = 100

WORLD_MAX_WIDTH = 4096
WORLD_MAX_HEIGHT = 4096


class Command(ABC):

    def __init__(self):
        self._message = ""

    @property
    def message(self) -> str:
        return self._message

    @abstractmethod
    def priority(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def check(self, logic: Logic) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def execute(self, logic: Logic):
        raise NotImplementedError()
