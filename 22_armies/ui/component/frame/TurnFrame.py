from typing import Tuple

from core.logic import Logic
from core.logic.command import NextTurn
from core.state import IGameStateListener, GameState
from .FrameComponent import FrameComponent
from ..control.Button import Button
from ..control.Label import Label
from ...theme.Theme import Theme


class TurnFrame(FrameComponent, IGameStateListener):

    def __init__(self, theme: Theme, logic: Logic):
        super().__init__(theme)
        self.__logic = logic

        # Title
        self.__titleLabel = Label(theme, "Turn")
        self.__titleLabel.moveRelativeTo("topLeft", self, "topLeft")
        self.addComponent(self.__titleLabel)

        # Turn number
        self.__turnLabel = Label(theme, f"{logic.state.turn}")
        self.__turnLabel.moveRelativeTo(
            "top", self.__titleLabel, "bottom",
            borderY=2
        )
        self.addComponent(self.__turnLabel)

        # Hourglass button
        def nextAction(buttons: Tuple[bool, bool, bool]):
            if buttons[0]:
                command = NextTurn()
                logic.addCommand(command)

        playerId = logic.state.playerId
        hourglass = theme.getTileset("frame").getTile("hourglass", playerId)
        self.__nextButton = Button(theme, hourglass, nextAction)
        self.__nextButton.setTootip('<s color="blue"><leftclick>End turn</s>')
        self.__nextButton.moveRelativeTo(
            "topLeft", self.__titleLabel, "topRight",
            borderY=1
        )
        self.addComponent(self.__nextButton)

        self.pack()

        # Listeners
        logic.state.registerListener(self)

    def dispose(self):
        self.__logic.state.removeListener(self)

    # GameState listener

    def turnChanged(self, state: GameState):
        self.__turnLabel.setMessage(f"{state.turn}")
        self.__turnLabel.moveRelativeTo("top", self.__titleLabel, "bottom", borderY=2)
        playerId = self.__logic.state.playerId
        hourglass = self.theme.getTileset("frame").getTile("hourglass", playerId)
        self.__nextButton.setSurface(hourglass)
        self.pack()
