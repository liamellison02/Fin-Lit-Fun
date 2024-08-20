from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

from .Notification import Notification

if TYPE_CHECKING:
    from ..mode.GameMode import GameMode


class SetGameModeRequested(Notification):
    def __init__(self, gameMode: Optional[GameMode] = None):
        super().__init__("SetGameModeRequested")
        self.gameMode = gameMode

    def getArgs(self) -> Tuple:
        return self.gameMode,
