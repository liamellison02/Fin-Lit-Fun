from typing import Optional, Tuple, Dict, Any

from pygame.surface import Surface

from core.constants import UnitClass
from core.constants.CellValue import getCellValues, CellValue
from core.state import GameState
from .FrameComponent import FrameComponent
from ..control.Button import Button
from ...theme.Theme import Theme


class PaletteFrame(FrameComponent):

    def __init__(self, theme: Theme, state: GameState, rowCount: int = 2):
        super().__init__(theme)
        self.__state = state
        self.__rowCount = rowCount
        self.__columnIndex = 0
        self.__columnButton: Optional[Button] = None
        self.__previousButton: Optional[Button] = None

        for layerName in ["ground", "impassable", "objects"]:
            self.__newColumn()
            tileset = self.theme.getTileset(layerName)
            for value in getCellValues(layerName):
                tile = tileset.getTile(value)
                if value == CellValue.OBJECTS_CITY:
                    self.__addButton(tile, layerName, {"value": value, "itemType": "city"})
                else:
                    self.__addButton(tile, layerName, {"value": value})

        self.__newColumn()
        tileset = self.theme.getTileset("units")
        for unitClass in UnitClass:
            if unitClass == UnitClass.NONE:
                playerId = 0
            else:
                playerId = state.playerId
            tile = tileset.getTile(unitClass, playerId)
            if unitClass == UnitClass.NONE:
                self.__addButton(tile, "units", {"value": CellValue.NONE})
            else:
                self.__addButton(tile, "units", {"value": CellValue.UNITS_UNIT, "itemType": "unit", "unitClass": unitClass})

        self.pack()

    def __addButton(self, tile: Surface, layerName: str, values: Dict[str, Any]):
        def buttonAction(buttons: Tuple[bool, bool, bool]):
            if buttons[0]:
                self.notifyMainBrushSelected(layerName, values)
            elif buttons[2]:
                self.notifySecondaryBrushSelected(layerName, values)

        button = Button(self.theme, tile, buttonAction)

        if self.__columnButton is None:
            self.__columnButton = button
            button.moveRelativeTo("topLeft", self, "topLeft", borderSize=0)
        elif self.__columnIndex == 0:
            button.moveRelativeTo("left", self.__columnButton, "right", borderSize=0)
        else:
            button.moveRelativeTo("top", self.__previousButton, "bottom", borderSize=0)
        self.addComponent(button)
        self.__previousButton = button
        if self.__columnIndex == 0:
            self.__columnButton = button
        self.__columnIndex += 1
        if self.__columnIndex >= self.__rowCount:
            self.__columnIndex = 0

    def __newColumn(self):
        self.__columnIndex = 0
        self.__previousButton = self.__columnButton

