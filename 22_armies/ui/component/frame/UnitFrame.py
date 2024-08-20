from typing import Tuple, List

from core.constants import ItemProperty, CellValue, UnitClass
from core.logic import Logic
from core.logic.command import DisbandUnit, Build
from core.state import Unit, IGameStateListener, GameState
from .FrameComponent import FrameComponent
from ..control import Button
from ..control.Icon import Icon
from ..control.Label import Label
from ...theme.Theme import Theme
from ...tools import formatResourceCost


class UnitFrame(FrameComponent, IGameStateListener):

    def __init__(self, theme: Theme, logic: Logic, cell: Tuple[int, int], unit: Unit):
        super().__init__(theme)
        self.__logic = logic
        self.__cell = cell
        self.__unit = unit
        self.__unitsLayer = logic.world.units

        # Icon
        if unit is not None:
            unitClass = unit.unitClass
            playerId = unit.playerId
        else:
            unitClass = UnitClass.NONE
            playerId = 0
        unitsTileset = theme.getTileset("units")
        classTile = unitsTileset.getTile(unitClass, playerId)
        self.__icon = Icon(theme, classTile)
        self.__icon.moveRelativeTo("topLeft", self, "topLeft")
        self.addComponent(self.__icon)
        
        # Title
        self.__titleLabel = Label(theme)
        self.addComponent(self.__titleLabel)
        
        # Life points
        self.__lifeLabel = Label(theme)
        self.__lifeLabel.setTootip("Hit points (current/max)")
        self.addComponent(self.__lifeLabel)

        # Move points
        self.__moveLabel = Label(theme)
        self.__moveLabel.setTootip("Move points (current/max)")
        self.addComponent(self.__moveLabel)

        # Action points
        self.__actionLabel = Label(theme)
        self.__actionLabel.setTootip("Action points (current/max)")
        self.addComponent(self.__actionLabel)

        # Attack
        self.__attackLabels: List[Label] = []
        for i in range(2):
            attackLabel = Label(theme)
            self.__attackLabels.append(attackLabel)
            self.addComponent(attackLabel)

        # Melee defense
        self.__meleeLabel = Label(theme)
        self.__meleeLabel.setTootip("Defense against melee attack")
        self.addComponent(self.__meleeLabel)

        # Bow defense
        self.__bowLabel = Label(theme)
        self.__bowLabel.setTootip("Defense against range attack")
        self.addComponent(self.__bowLabel)

        # Mount defense
        self.__mountLabel = Label(theme)
        self.__mountLabel.setTootip("Defense against charge attack")
        self.addComponent(self.__mountLabel)

        # Siege defense
        self.__siegeLabel = Label(theme)
        self.__siegeLabel.setTootip("Defense against siege attack")
        self.addComponent(self.__siegeLabel)

        # Buttons
        self.__buttons: List[Button] = []
        self.__update()

        # Listeners
        logic.state.registerListener(self)

    def dispose(self):
        self.__logic.state.removeListener(self)

    @property
    def unit(self) -> Unit:
        return self.__unit

    def __update(self):
        unit = self.__unit
        if unit is None:
            self.__titleLabel.setMessage("")
            self.__lifeLabel.setMessage("")
            self.__moveLabel.setMessage("")
            self.__actionLabel.setMessage("")
            for attackLabel in self.__attackLabels:
                attackLabel.setMessage("")
            self.__meleeLabel.setMessage("")
            self.__bowLabel.setMessage("")
            self.__mountLabel.setMessage("")
            self.__siegeLabel.setMessage("")
            self.pack()
            return

        title = f'{unit.unitClass.formatName()}<flag player="{unit.playerId}">'
        self.__titleLabel.setMessage(title)

        # Life points
        if unit.hasProperty(ItemProperty.LIFE_POINTS) \
                and unit.hasProperty(ItemProperty.MAX_LIFE_POINTS):
            value = unit.getProperty(ItemProperty.LIFE_POINTS)
            maxValue = unit.getProperty(ItemProperty.MAX_LIFE_POINTS)
            lifeDesc = f"{value}/{maxValue}<life><br>"
        else:
            lifeDesc = ""
        self.__lifeLabel.setMessage(lifeDesc)
            
        # Move points
        if unit.hasProperty(ItemProperty.MOVE_POINTS) \
                and unit.hasProperty(ItemProperty.MAX_MOVE_POINTS):
            value = unit.getProperty(ItemProperty.MOVE_POINTS)
            maxValue = unit.getProperty(ItemProperty.MAX_MOVE_POINTS)
            moveDesc = f"{value}/{maxValue}<move><br>"
        else:
            moveDesc = ""
        self.__moveLabel.setMessage(moveDesc)
            
        # Action points
        if unit.hasProperty(ItemProperty.ACTION_POINTS) \
                and unit.hasProperty(ItemProperty.MAX_ACTION_POINTS):
            value = unit.getProperty(ItemProperty.ACTION_POINTS)
            maxValue = unit.getProperty(ItemProperty.MAX_ACTION_POINTS)
            actionDesc = f"{value}/{maxValue}<attack><br>"
        else:
            actionDesc = ""
        self.__actionLabel.setMessage(actionDesc)

        self.__titleLabel.moveRelativeTo("topLeft", self.__icon, "topRight")
        self.__lifeLabel.moveRelativeTo("topLeft", self.__titleLabel, "bottomLeft")
        self.__moveLabel.moveRelativeTo("topLeft", self.__lifeLabel, "bottomLeft")
        self.__actionLabel.moveRelativeTo("topLeft", self.__moveLabel, "bottomLeft")

        x = max(
            self.__lifeLabel.right,
            self.__moveLabel.right,
            self.__actionLabel.right
        ) + self.theme.framePadding
        y = self.__lifeLabel.top

        self.__attackLabels[0].moveTo((x, y))

        # Attack
        attackCount = 0

        def addAttack(i, message: str, tooltip: str):
            if i >= len(self.__attackLabels):
                return i
            self.__attackLabels[i].setMessage(message)
            self.__attackLabels[i].setTootip(tooltip)
            return i + 1
            
        if unit.hasProperty(ItemProperty.MELEE_ATTACK):
            value = unit.getProperty(ItemProperty.MELEE_ATTACK)
            attackCount = addAttack(attackCount, f"{value}<melee_attack>", "Melee attack")
        if unit.hasProperty(ItemProperty.BOW_ATTACK):
            value = unit.getProperty(ItemProperty.BOW_ATTACK)
            attackCount = addAttack(attackCount, f"{value}<range_attack>", "Range attack")
        if unit.hasProperty(ItemProperty.MOUNT_ATTACK):
            value = unit.getProperty(ItemProperty.MOUNT_ATTACK)
            attackCount = addAttack(attackCount, f"{value}<mount_attack>", "Charge attack")
        if unit.hasProperty(ItemProperty.SIEGE_ATTACK):
            value = unit.getProperty(ItemProperty.SIEGE_ATTACK)
            attackCount = addAttack(attackCount, f"{value}<siege_attack>", "Siege attack")
            
        for i in range(attackCount, len(self.__attackLabels)):
            self.__attackLabels[i].setMessage("")
            self.__attackLabels[i].disableTooltip()

        for i in range(1, len(self.__attackLabels)):
            self.__attackLabels[i].moveRelativeTo("topLeft", self.__attackLabels[i - 1], "topRight")

        # Melee defense
        if unit.hasProperty(ItemProperty.MELEE_DEFENSE):
            value = unit.getProperty(ItemProperty.MELEE_DEFENSE)
            meleeDesc = f"{value}<melee_defense>"
        else:
            meleeDesc = ""
        self.__meleeLabel.setMessage(meleeDesc)
            
        # Bow defense
        if unit.hasProperty(ItemProperty.BOW_DEFENSE):
            value = unit.getProperty(ItemProperty.BOW_DEFENSE)
            bowDesc = f"{value}<range_defense>"
        else:
            bowDesc = ""
        self.__bowLabel.setMessage(bowDesc)

        # Mount defense
        if unit.hasProperty(ItemProperty.MOUNT_DEFENSE):
            value = unit.getProperty(ItemProperty.MOUNT_DEFENSE)
            mountDesc = f"{value}<mount_defense>"
        else:
            mountDesc = ""
        self.__mountLabel.setMessage(mountDesc)
        
        # Siege defense
        if unit.hasProperty(ItemProperty.SIEGE_DEFENSE):
            value = unit.getProperty(ItemProperty.SIEGE_DEFENSE)
            siegeDesc = f"{value}<siege_defense>"
        else:
            siegeDesc = ""
        self.__siegeLabel.setMessage(siegeDesc)

        self.__meleeLabel.moveRelativeTo("topLeft", self.__attackLabels[0], "bottomLeft")
        self.__bowLabel.moveRelativeTo("topLeft", self.__meleeLabel, "topRight")
        self.__mountLabel.moveRelativeTo("topLeft", self.__meleeLabel, "bottomLeft")
        self.__siegeLabel.moveRelativeTo("topLeft", self.__mountLabel, "topRight")

        # Buttons

        for button in self.__buttons:
            self.removeComponent(button)
        self.__buttons.clear()

        theme = self.theme
        # Disband button
        if unit.getProperty(ItemProperty.DISBAND, False):
            disbandCommand = DisbandUnit(self.__cell, self.__unit)

            def disband(buttons):
                if buttons[0]:
                    self.__logic.addCommand(disbandCommand)

            icon = theme.getTileset("units").getTile(CellValue.NONE)
            button = Button(theme, icon, disband)
            if disbandCommand.check(self.__logic):
                button.setTootip('<s color="blue"><leftclick>Disband unit</s>')
            else:
                button.setTootip(disbandCommand.message)
                button.disable()
            self.__buttons.append(button)
            self.addComponent(button)

        # Build buttons
        tileset = theme.getTileset("objects")
        rules = self.__logic.rules
        for value in unit.getIntListProperty(ItemProperty.BUILD):
            cellValue = CellValue(value)

            class BuildAction:
                def __init__(self, logic, command):
                    self.logic = logic
                    self.command = command

                def __call__(self, buttons):
                    if buttons[0]:
                        self.logic.addCommand(self.command)

            command = Build(self.__cell, self.__unit, cellValue)
            ok = command.check(self.__logic)

            icon = tileset.getTile(cellValue)
            action = BuildAction(self.__logic, command)
            button = Button(theme, icon, action)
            if cellValue == CellValue.NONE:
                tooltip = f"Remove<br>"
            else:
                tooltip = f"{cellValue}<br>"
            desc = rules.getTileEffectDescription(cellValue)
            if desc:
                tooltip += f"{desc}<br>"
            if command.cost:
                tooltip += f"Cost: {formatResourceCost(command.cost)}<br>"
            if ok:
                tooltip += '<s color="blue"><leftclick>Build</s>'
            else:
                tooltip += command.message
                button.disable()
            button.setTootip(tooltip, 200)
            self.__buttons.append(button)
            self.addComponent(button)

        # Buttons layout
        if len(self.__buttons) > 0:
            y = self.__titleLabel.top
            x = self.__bowLabel.right + self.theme.framePadding
            self.__buttons[0].moveTo((x, y))
            columnButton = self.__buttons[0]
            columnIndex = 0
            for buttonIndex in range(1, len(self.__buttons)):
                if columnIndex >= 1:
                    self.__buttons[buttonIndex].moveRelativeTo("left", columnButton, "right", borderSize=0)
                    columnButton = self.__buttons[buttonIndex]
                    columnIndex = 0
                else:
                    self.__buttons[buttonIndex].moveRelativeTo("top", self.__buttons[buttonIndex - 1], "bottom", borderSize=0)
                    columnIndex += 1

        self.pack()

    # GameState listener

    def unitChanged(self, state: GameState, cell: Tuple[int, int], unit: Unit):
        if unit != self.__unit:
            return
        self.__update()

    def resourcesChanged(self, state: GameState):
        self.__update()
