from typing import Optional, Tuple

from .Notification import Notification
from ..Mouse import Mouse


class ShowTooltipRequested(Notification):
    def __init__(self, message: str, maxWidth: int, mouse: Optional[Mouse]):
        super().__init__("ShowTooltipRequested")
        self.mouse = mouse
        self.message = message
        self.maxWidth = maxWidth

    def getArgs(self) -> Tuple:
        return self.message, self.maxWidth, self.mouse
