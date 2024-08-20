from __future__ import annotations

import logging
import traceback
from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from ui.notification.Notification import Notification, NotificationHandler


class NotificationManager(object):

    def __init__(self) -> None:
        self.__queue: List[Notification] = []
        self.__handlers: Dict[str, List[NotificationHandler]] = {}

    @property
    def queue(self):
        return self.__queue

    @property
    def handlers(self):
        return self.__handlers

    def send(self, notification: Notification):
        name = notification.name
        if name not in self.__handlers:
            return
        self.__queue.append(notification)

    def addHandlers(self, handlers: Dict[str, NotificationHandler]):
        for name, handler in handlers.items():
            assert hasattr(handler, "__self__"), f"'{name}' handler: only method are supported"
            if name not in self.__handlers:
                self.__handlers[name] = []
            queueHandlers = self.__handlers[name]
            queueHandlers.append(handler)

    def removeHandler(self, handlerClass):
        for name in self.__handlers:
            queueHandlers = self.__handlers[name]
            for index, handler in enumerate(queueHandlers):
                if handler.__self__ == handlerClass:
                    del queueHandlers[index]

    def checkEmpty(self):
        for name, queueHandlers in self.__handlers.items():
            for handler in queueHandlers:
                logging.error(f"'{name}' handler was not removed for {handler.__self__.__class__.__name__}")

    def notifyAll(self):
        success = True
        for notification in self.__queue:
            name = notification.name
            if name not in self.__handlers:
                continue
            for handler in self.__handlers[name]:
                try:
                    args = notification.getArgs()
                    handler(*args)
                except Exception as ex:
                    logging.error(f"Error during notification '{name}':\n{ex}")
                    traceback.print_exc()
                    success = False
        self.__queue.clear()
        return success

