from typing import Tuple

from .Notification import Notification


class UpdateMouseFocusRequested(Notification):
    def __init__(self):
        super().__init__("UpdateMouseFocusRequested")

    def getArgs(self) -> Tuple:
        return ()
