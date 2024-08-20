from typing import Tuple, List

from core.logic import Logic
from core.state import Unit, IGameStateListener, GameState, Army
from .FrameComponent import FrameComponent
from ..control import Toggle
from ..control.Label import Label
from ...notification import ArmySelectionChanged
from ...theme.Theme import Theme
from ...tools import buildUnitTooltip


class ArmyFrame(FrameComponent, IGameStateListener):

    def __init__(self, theme: Theme, logic: Logic, cell: Tuple[int, int], army: Army):
        super().__init__(theme)
        self.__logic = logic
        self.__cell = cell
        self.__army = army
        self.__unitsLayer = logic.world.units
        self.__icons: List[Toggle] = []

        self.__update()

        # Listeners
        logic.state.registerListener(self)

    def dispose(self):
        self.__logic.state.removeListener(self)

    def getSelection(self) -> List[Unit]:
        selection = []
        for icon, unit in zip(self.__icons, self.__army.units):
            if icon.isEnabled():
                selection.append(unit)
        return selection

    def __update(self):
        self.removeAllComponents()
        theme = self.theme
        army = self.__army

        titleLabel = Label(theme, f'Army<flag player="{army.playerId}">')
        self.addComponent(titleLabel)

        lastAnchor = None
        unitsTileset = theme.getTileset("units")
        self.__icons = []
        for unit in army.units:
            classTile = unitsTileset.getTile(unit.unitClass, unit.playerId)
            icon = Toggle(theme, classTile, lambda: ArmySelectionChanged(self.__cell, army).send())
            if lastAnchor is None:
                icon.moveRelativeTo("topLeft", titleLabel, "bottomLeft")
            else:
                icon.moveRelativeTo("topLeft", lastAnchor, "topRight")
            tooltip = buildUnitTooltip(unit)
            tooltip += '<s color="blue"><leftclick>Select/Unselect</s><br>'
            icon.setTootip(tooltip)
            self.addComponent(icon)
            self.__icons.append(icon)
            lastAnchor = icon

        self.pack()

    # GameState listener

    def unitChanged(self, state: GameState, cell: Tuple[int, int], unit: Unit):
        if unit != self.__army:
            return
        self.__update()

