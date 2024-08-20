from typing import Tuple

from .Notification import Notification


class ShowMessageRequested(Notification):
    def __init__(self, message: str, portrait: str):
        super().__init__("ShowMessageRequested")
        self.message = message
        self.portrait = portrait

    def getArgs(self) -> Tuple:
        return self.message, self.portrait
