from typing import Tuple

from .Notification import Notification


class HideTooltipRequested(Notification):
    def __init__(self):
        super().__init__("HideTooltipRequested")

    def getArgs(self) -> Tuple:
        return ()

