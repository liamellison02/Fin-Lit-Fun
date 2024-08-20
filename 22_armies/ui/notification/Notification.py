from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Dict, Callable, TypeAlias, Tuple

from .NotificationManager import NotificationManager

NotificationHandler: TypeAlias = Callable


class Notification(ABC):

    manager = NotificationManager()

    @classmethod
    def getManager(cls) -> NotificationManager:
        return cls.manager

    @classmethod
    def addHandlers(cls, handlers: Dict[str, NotificationHandler]):
        cls.manager.addHandlers(handlers)

    @classmethod
    def removeHandler(cls, listener):
        cls.manager.removeHandler(listener)

    @classmethod
    def notifyAll(cls):
        return cls.manager.notifyAll()

    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @abstractmethod
    def getArgs(self) -> Tuple:
        raise NotImplementedError()

    def send(self):
        self.manager.send(self)

    def __str__(self) -> str:
        return f"Notification {self.__name}"
