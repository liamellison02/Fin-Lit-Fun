import traceback
from typing import Tuple, Optional, Dict, Any

import pygame

from core.constants import CellValue, UnitClass, CityClass
from core.logic import Logic
from core.state import Unit, City, Item, TrainingCamp
from .DefaultGameMode import DefaultGameMode
from ..Mouse import Mouse
from ..component.frame.PaletteFrame import PaletteFrame
from ..notification import SetGameModeRequested, ShowMessageRequested
from ..theme.Theme import Theme


class EditGameMode(DefaultGameMode):

    def __init__(self, theme: Theme, logic: Logic):
        super().__init__(theme, logic)

        # Components
        self.__paletteFrame = PaletteFrame(theme, logic.state)
        self.__paletteFrame.moveRelativeTo("bottom", self, "bottom")

        # Components order
        self.addComponent(self.__paletteFrame)

        # Brush
        self.__mainBrushLayer = "ground"
        self.__mainBrushValues: Dict[str, Any] = {"value": CellValue.GROUND_EARTH}
        self.__mainBrushUnitClass: Optional[UnitClass] = None
        self.__secondaryBrushLayer = "ground"
        self.__secondaryBrushValues: Dict[str, Any] = {"value": CellValue.GROUND_SEA}
        self.__secondaryBrushUnitClass: Optional[UnitClass] = None

        # Listener
        self.__paletteFrame.registerListener(self)  # mainBrushSelected, ...

    def dispose(self):
        super().dispose()
        self.__paletteFrame.removeListener(self)

    # UI Event handler

    def keyDown(self, key: int) -> bool:
        if key in [pygame.K_e, pygame.K_F2]:
            from .WorldGameMode import WorldGameMode
            playGameMode = WorldGameMode(self.theme, self._logic)
            playGameMode.viewChanged(self.view)
            SetGameModeRequested(playGameMode).send()
            return True
        elif key in [pygame.K_F3]:
            try:
                self._logic.state.load("level.json")
                editGameMode = EditGameMode(self.theme, self._logic)
                editGameMode.viewChanged(self.view)
                SetGameModeRequested(editGameMode).send()
            except Exception as ex:
                traceback.print_exc()
                ShowMessageRequested(str(ex), "elder").send()
        elif key in [pygame.K_F4]:
            try:
                self._logic.state.load("level.pickle")
                gameMode = EditGameMode(self.theme, self._logic)
                gameMode.viewChanged(self.view)
                SetGameModeRequested(gameMode).send()
            except Exception as ex:
                ShowMessageRequested(str(ex), "elder").send()
        elif key in [pygame.K_F5]:
            try:
                self._logic.state.load("level.msgpack")
                gameMode = EditGameMode(self.theme, self._logic)
                gameMode.viewChanged(self.view)
                SetGameModeRequested(gameMode).send()
            except Exception as ex:
                ShowMessageRequested(str(ex), "elder").send()
        elif key in [pygame.K_F6]:
            try:
                self._logic.state.save("level.json")
            except Exception as ex:
                traceback.print_exc()
                ShowMessageRequested(str(ex), "elder").send()
        elif key in [pygame.K_F7]:
            try:
                self._logic.state.save("level.pickle")
            except Exception as ex:
                ShowMessageRequested(str(ex), "elder").send()
        elif key in [pygame.K_F8]:
            try:
                self._logic.state.save("level.msgpack")
            except Exception as ex:
                ShowMessageRequested(str(ex), "elder").send()
        return False

    # Component listener

    def __updateCell(self, cell: Tuple[int, int], mouse: Mouse):
        if mouse.button1 or mouse.button2:
            brushLayer = self.__mainBrushLayer
            brushValues = self.__mainBrushValues
            fill = mouse.button2
        elif mouse.button3:
            brushLayer = self.__secondaryBrushLayer
            brushValues = self.__secondaryBrushValues
            fill = False
        else:
            return
        Command = self._logic.getSetLayerCellCommand(brushLayer)
        brushValue = brushValues["value"]
        brushItem: Optional[Item] = None
        playerId = self._state.playerId
        if "itemType" in brushValues:
            rules = self._logic.rules
            itemType = brushValues["itemType"]
            if itemType == "unit":
                unitClass = brushValues["unitClass"]
                brushItem = Unit(unitClass, playerId)
                brushItem.setProperties(rules.getUnitProperties(unitClass))
            elif itemType == "city":
                brushItem = City(CityClass.DEFAULT, playerId)
                brushItem.setProperties(rules.getCityProperties(CityClass.DEFAULT))
            elif itemType == "trainingCamp":
                brushItem = TrainingCamp(playerId)
                brushItem.setProperties(rules.getTrainingCampProperties(brushValue))
        command = Command(cell, brushValue, brushItem, fill)
        self._logic.addCommand(command)

    def worldCellClicked(self, cell: Tuple[int, int], mouse: Mouse):
        self.__updateCell(cell, mouse)

    def worldCellEntered(self, cell: Tuple[int, int], mouse: Mouse, dragging: bool):
        if dragging:
            self.__updateCell(cell, mouse)

    def mainBrushSelected(self, layerName: str, values: Dict[str, Any]):
        self.__mainBrushLayer = layerName
        self.__mainBrushValues = values

    def secondaryBrushSelected(self, layerName: str, values: Dict[str, Any]):
        self.__secondaryBrushLayer = layerName
        self.__secondaryBrushValues = values
