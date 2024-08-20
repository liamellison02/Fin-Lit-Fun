from typing import Tuple, Optional

from core.constants import UnitClass
from core.logic import Logic
from core.logic.command import RecruitUnit
from .FrameComponent import FrameComponent
from ..control import Button
from ...theme.Theme import Theme
from ...tools import formatResourceCost


class RecruitFrame(FrameComponent):

    def __init__(self, theme: Theme, logic: Logic, cityCell: Tuple[int, int]):
        super().__init__(theme)
        self.__logic = logic
        self.__cityCell = cityCell
        self.updateButtons()

    def updateButtons(self) -> None:
        theme = self.theme
        logic = self.__logic
        rules = logic.rules
        cityCell = self.__cityCell
        city = rules.getCity(cityCell)

        self.removeAllComponents()

        previousButton: Optional[Button] = None
        recruits, recruitsMax = rules.getCityRecruitState(city)
        for unitClass in sorted(recruits.keys()):
            button = RecruitButton(theme, logic, cityCell, unitClass)
            if previousButton is None:
                button.moveRelativeTo("topLeft", self, "topLeft")
            else:
                button.moveRelativeTo("left", previousButton, "right")
            self.addComponent(button)
            previousButton = button

        self.pack()


class RecruitButton(Button):
    def __init__(self, theme: Theme, logic: Logic, cityCell: Tuple[int, int], unitClass: UnitClass):
        self.unitClass = unitClass
        command = RecruitUnit(cityCell, unitClass)

        def action(buttons: Tuple[bool, bool, bool]):
            if buttons[0]:
                logic.addCommand(command)

        tileset = theme.getTileset("units")
        surface = tileset.getTile(unitClass, logic.state.playerId)
        super().__init__(theme, surface, action)
        ok = command.check(logic)
        tooltip = f"Recruit a {unitClass.toName()} ({command.available} available)<br>"
        cost = formatResourceCost(command.cost)
        if cost:
            tooltip += f"{cost}<br>"
        if not ok:
            self.disable()
            tooltip += command.message
        else:
            tooltip += f"<s color='blue'><leftclick>Recruit</s>"
        self.setTootip(tooltip, 200)
