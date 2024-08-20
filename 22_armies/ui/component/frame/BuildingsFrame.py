from typing import Tuple

from core.logic import Logic
from core.state import GameState, IGameStateListener, City
from .FrameComponent import FrameComponent
from ..control import Label
from ...theme.Theme import Theme


class BuildingsFrame(FrameComponent, IGameStateListener):

    def __init__(self, theme: Theme, logic: Logic, city: City):
        super().__init__(theme)
        self.__logic = logic
        self.__city = city

        self.__productionLabel = Label(theme, "Buildings")
        self.__productionLabel.moveRelativeTo("topLeft", self, "topLeft")
        self.addComponent(self.__productionLabel)

        self.__updateValues()

        # Listeners
        self.__logic.state.registerListener(self)

    def dispose(self):
        self.__logic.state.removeListener(self)

    # GameState listener

    def citizenAssigned(self, state: GameState, cityCell: Tuple[int, int], cell: Tuple[int, int]):
        self.__updateValues()

    def citizenUnassigned(self, state: GameState, cityCell: Tuple[int, int], cell: Tuple[int, int]):
        self.__updateValues()

    def turnChanged(self, state: GameState):
        self.__updateValues()

    def resourcesChanged(self, state: GameState):
        self.__updateValues()

    def __updateValues(self):
        city = self.__city




        self.pack()



