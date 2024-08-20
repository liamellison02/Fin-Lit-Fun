from .GameMode import GameMode
from ..Mouse import Mouse
from ..component.frame.MessageFrame import MessageFrame
from ..notification import SetOverlayGameModeRequested
from ..theme.Theme import Theme


class MessageGameMode(GameMode):

    def __init__(self, theme: Theme, message: str, portrait: str):
        super().__init__(theme)

        self.__messageFrame = MessageFrame(theme, message, portrait)
        self.__messageFrame.moveRelativeTo("center", self, "center")
        self.addComponent(self.__messageFrame)

    # UI Event Handler

    def keyDown(self, key: int) -> bool:
        SetOverlayGameModeRequested().send()
        return True

    def mouseButtonDown(self, mouse: Mouse) -> bool:
        SetOverlayGameModeRequested().send()
        return True
