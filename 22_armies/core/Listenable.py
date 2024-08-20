from __future__ import annotations

import logging
from typing import List, TypeVar, Generic, Iterable

IListener = TypeVar('IListener')


class Listenable(Generic[IListener]):

    def __init__(self) -> None:
        self.__listeners: List[IListener] = []

    @property
    def listeners(self) -> Iterable[IListener]:
        return self.__listeners

    def registerListener(self, listener: IListener):
        self.__listeners.append(listener)

    def removeListener(self, listener: IListener):
        self.__listeners.remove(listener)

    def removeAllListeners(self):
        self.__listeners.clear()

    def __del__(self):
        for listener in self.__listeners:
            logging.warning(f"In {self.__class__.__name__}: a listener {listener.__class__.__name__} was not removed")
