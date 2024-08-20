import logging
from typing import Tuple, Optional, cast, Union

import pygame

from core.constants import ItemProperty, CellValue, Resource
from core.logic import Logic, DistanceMap
from core.logic.command import MoveUnit, AttackUnit
from core.state import Item, Unit, IGameStateListener, GameState, ILayerListener, Army
from .DefaultGameMode import DefaultGameMode
from ..Mouse import Mouse
from ..component.frame import TurnFrame, ResourcesFrame, UnitFrame, ArmyFrame
from ..layer import SelectionValue
from ..notification import SetGameModeRequested, Notification
from ..theme.Theme import Theme
from ..tools import centerCellView, formatResourceBalance, buildUnitTooltip


class WorldGameMode(DefaultGameMode, IGameStateListener, ILayerListener):

    def __init__(self, theme: Theme, logic: Logic):
        super().__init__(theme, logic)

        # Selection
        self.__targetAction = ""
        self.__targetCell: Optional[Tuple[int, int]] = None
        self.__targetSize: Optional[Tuple[int, int]] = None
        self.__selectedCell: Optional[Tuple[int, int]] = None
        self.__distanceMap: Optional[DistanceMap] = None

        # Components
        self.__resourcesFrame = ResourcesFrame(theme, logic)
        self.__resourcesFrame.moveRelativeTo("topLeft", self, "topLeft")

        self.__unitFrame: Optional[UnitFrame | ArmyFrame] = None

        self.__turnFrame = TurnFrame(theme, logic)
        self.__turnFrame.moveRelativeTo("bottomRight", self._minimapFrame, "topRight")

        self.addComponent(self.__resourcesFrame, cache=True)
        self.addComponent(self.__turnFrame, cache=True)

        # Listener
        Notification.addHandlers({
            "ArmySelectionChanged": self.onArmySelectionChanged
        })
        self._state.registerListener(self)
        self._world.units.registerListener(self)

    def dispose(self):
        super().dispose()
        Notification.removeHandler(self)
        self._state.removeListener(self)
        self._world.units.removeListener(self)

    # UI Event handler

    def keyDown(self, key: int) -> bool:
        if key in [pygame.K_F2]:
            from .EditGameMode import EditGameMode
            gameMode = EditGameMode(self.theme, self._logic)
            gameMode.viewChanged(self.view)
            SetGameModeRequested(gameMode).send()
            return True
        elif key in [pygame.K_F8]:  # Debug / Illustrate
            self._worldComponent.selectionComponent.rollShowMode()
            return True
        elif key == pygame.K_e:
            cell = self.__targetCell
            if cell is not None and self.world.contains(cell):
                objects = self.world.objects
                value = objects.getValue(cell)
                if value == CellValue.OBJECTS_CITY:
                    self.__enterCity(cell)
        return False

    def mouseLeave(self) -> bool:
        super().mouseLeave()
        self.__clearTarget()
        return True

    # Component listener

    def worldCellEntered(self, cell: Tuple[int, int], mouse: Mouse, dragging: bool):
        self.__updateTarget(cell, mouse)

    def worldCellClicked(self, cell: Tuple[int, int], mouse: Mouse):
        if mouse.button1:
            if self.__selectedCell == cell:
                return
            if self.__targetCell is None:
                return
            if self.__targetSize is not None:
                found = False
                rangeX, rangeY = self.__targetSize
                for sizeY in range(rangeY):
                    for sizeX in range(rangeX):
                        if (self.__targetCell[0] + sizeX) == cell[0] \
                                and (self.__targetCell[1] + sizeY) == cell[1]:
                            found = True
                if not found:
                    return
            if self.__targetAction in ["selectUnit"]:
                self.__clearTarget()
                self.__selectUnit(cell)
            elif self.__targetAction == "moveUnit":
                self.__clearTarget()
                self.__moveUnit(cell)
            elif self.__targetAction == "attackUnit":
                self.__attackUnit(cell)
            elif self.__targetAction == "enterCity":
                self.__enterCity(cell)
            else:
                self.__clearSelection()
        elif mouse.button3:
            self.__clearSelection()
            self.__updateTarget(cell, mouse)

    def __clearTarget(self):
        if self.__targetCell is not None:
            self._selectionLayer.setValue(self.__targetCell, SelectionValue.NONE)
            self._selectionLayer.notifyCellChanged(self.__targetCell)
            self.__targetCell = None
            self.__targetSize = None
            self.__targetAction = ""
        self._selectionLayer.clearNumbers()
        self.hideTooltip()

    def __buildUnitTooltip(self, unitOrCell: Union[Item, Unit, Army, Tuple[int, int]]) -> str:
        if type(unitOrCell) == tuple:
            item = self.world.units.getItem(unitOrCell)
            if item is None:
                return ""
            unitOrCell = item
        return buildUnitTooltip(unitOrCell)

    def __updateTarget(self, cell: Tuple[int, int], mouse: Optional[Mouse] = None):
        self.__clearTarget()

        if self.__selectedCell is not None:
            if cell == self.__selectedCell:
                self.disableTooltip()
                return

            attackCommand = AttackUnit(self.__selectedCell, cell)
            if attackCommand.check(self._logic):
                self.__targetCell = cell
                self.__targetSize = (1, 1)
                self.__targetAction = "attackUnit"
                self._selectionLayer.setValue(cell, SelectionValue.ATTACK)
                self._selectionLayer.notifyCellChanged(cell)
                attackUnitTooltip = self.__buildUnitTooltip(cell)
                attackUnitTooltip += '<s color="blue"><leftclick>Attack</s><br>'
                attackUnitTooltip += '<s color="blue"><rightclick>Clear selection</s>'
                self.setTootip(attackUnitTooltip)
                self.showTooltip(mouse)
                return

            path, costs = self.__distanceMap.getPath(cell)
            if self.__unitFrame is not None:
                if isinstance(self.__unitFrame, ArmyFrame):
                    selection = cast(ArmyFrame, self.__unitFrame).getSelection()
                else:
                    selection = [cast(UnitFrame, self.__unitFrame).unit]
            else:
                selection = None

            moveCommand = MoveUnit(self.__selectedCell, path, selection)
            if moveCommand.check(self._logic):
                self.__targetCell = cell
                self.__targetSize = (1, 1)
                self.__targetAction = "moveUnit"
                self._selectionLayer.showPath(path, costs, moveCommand.movePoints)
                self._selectionLayer.notifyContentChanged()
                moveUnitTooltip = '<s color="blue"><leftclick>Move here</s><br>'
                moveUnitTooltip += '<s color="blue"><rightclick>Clear selection</s>'
                self.setTootip(moveUnitTooltip)
                self.showTooltip(mouse)
                return

        unit = self.world.units.getItem(cell)
        if unit is not None and (isinstance(unit, Unit) or isinstance(unit, Army)):
            self.__targetCell = cell
            self.__targetSize = (1, 1)
            self._selectionLayer.setValue(cell, SelectionValue.SELECT)
            self._selectionLayer.notifyCellChanged(cell)

            self.__targetAction = "selectUnit"
            selectUnitTooltip = self.__buildUnitTooltip(unit)
            if isinstance(unit, Unit):
                selectUnitTooltip += '<s color="blue"><leftclick>Select unit</s><br>'
            else:
                selectUnitTooltip += '<s color="blue"><leftclick>Select army</s><br>'

            value = self.world.objects.getValue(cell)
            if value == CellValue.OBJECTS_CITY:
                selectUnitTooltip += '<s color="blue">(E) Enter city</s>'

            self.setTootip(selectUnitTooltip)
            self.showTooltip(mouse)
            return

        value = self.world.objects.getValue(cell)
        if value == CellValue.OBJECTS_CITY:
            rules = self._logic.rules
            mainCell = rules.getCityTopLeft(cell)
            self.__targetCell = mainCell
            self.__targetSize = (2, 2)
            self.__targetAction = "enterCity"
            self._selectionLayer.setValue(mainCell, SelectionValue.SELECT2)
            self._selectionLayer.notifyCellChanged(mainCell)
            city = rules.getCity(mainCell)
            production = rules.computeCityProduction(city)
            balance = production["balance"]
            self.setTootip(
                f'<flag player="{city.playerId}">{city.name}<br>'
                f'{city.getCitizenCount()}<citizen><space>'
                f"{formatResourceBalance(Resource.FOOD, balance)}<food><space>"
                f"{formatResourceBalance(Resource.WOOD, balance)}<wood><space>"
                f"{formatResourceBalance(Resource.STONE, balance)}<stone><space>"
                f"{formatResourceBalance(Resource.GOLD, balance)}<gold><br>"
                '<s color="blue"><leftclick>/(E) Enter city</s>'
            )
            self.showTooltip(mouse)
            return

        self.disableTooltip()

    def __clearSelection(self):
        if self.__selectedCell is not None:
            self._selectionLayer.clear()
            self._selectionLayer.notifyContentChanged()
            self.__selectedCell = None
            self._shadowLayer.clear()
            self._shadowLayer.notifyContentChanged()

        if self.__unitFrame is not None:
            self.removeComponent(self.__unitFrame)

        # Debug / Illustrate
        self._worldComponent.selectionComponent.setDistanceMap(None)

    def __selectUnit(self, cell: Tuple[int, int]):
        if self.__selectedCell is not None:
            self._selectionLayer.setValue(self.__selectedCell, SelectionValue.NONE)
            self._selectionLayer.clearNumbers()
        item = self.world.units.getItem(cell)
        if item is None:
            return
        self.__selectedCell = cell
        self._selectionLayer.setValue(cell, SelectionValue.SELECTED)
        self._selectionLayer.notifyCellChanged(cell)

        # Frame
        if self.__unitFrame is not None:
            self.removeComponent(self.__unitFrame)
        if isinstance(item, Unit):
            unit = cast(Unit, item)
            armySize = 1
            self.__unitFrame = UnitFrame(self.theme, self._logic, cell, unit)
            movePoints = unit.getIntProperty(ItemProperty.MOVE_POINTS, 0)
        elif isinstance(item, Army):
            army = cast(Army, item)
            armySize = len(army)
            self.__unitFrame = ArmyFrame(self.theme, self._logic, cell, army)
            movePoints = army.getLowestIntProperty(ItemProperty.MOVE_POINTS, 0)
        else:
            return
        self.__unitFrame.moveRelativeTo("bottomRight", self._minimapFrame, "bottomLeft")
        self.addComponent(self.__unitFrame)

        # Distance map
        self.__distanceMap = DistanceMap.create(
            self.world, self._state.playerId, cell, radius=31, armySize=armySize, maxArmySize=self._logic.rules.getArmyMaxSize()
        )

        self._shadowLayer.showPaths(self.__distanceMap, movePoints)
        self._shadowLayer.notifyContentChanged()

        # Debug / Illustrate
        self._worldComponent.selectionComponent.setDistanceMap(self.__distanceMap, movePoints)

    def __moveUnit(self, targetCell: Tuple[int, int]):
        if self.__selectedCell is None:
            return
        path, costs = self.__distanceMap.getPath(targetCell)
        if self.__unitFrame is not None:
            if isinstance(self.__unitFrame, ArmyFrame):
                selection = cast(ArmyFrame, self.__unitFrame).getSelection()
            else:
                selection = [cast(UnitFrame, self.__unitFrame).unit]
        else:
            selection = None
        command = MoveUnit(self.__selectedCell, path, selection)
        self._logic.addCommand(command)

    def __attackUnit(self, cell: Tuple[int, int]):
        if self.__selectedCell is None:
            return
        command = AttackUnit(self.__selectedCell, cell)
        self._logic.addCommand(command)

    def __enterCity(self, cell: Tuple[int, int]):
        from .CityGameMode import CityGameMode
        cell = self._logic.rules.getCityTopLeft(cell)
        gameMode = CityGameMode(self.theme, self._logic, cell, self.view)
        view = centerCellView(self.theme, self.world, (cell[0] + 1, cell[1] + 1))
        gameMode.viewChanged(view)
        SetGameModeRequested(gameMode).send()

    # GameState listener

    def turnChanged(self, state: GameState):
        self.__clearSelection()
        tile = self.theme.getMouseCursor(state.playerId)
        cursor = pygame.cursors.Cursor((0, 0), tile)
        pygame.mouse.set_cursor(cursor)

    def unitMoved(self, state: GameState,
                  fromCell: Tuple[int, int], toCell: Tuple[int, int]):
        self.__selectUnit(toCell)

    def unitDamaged(self, state: GameState, cell: Tuple[int, int], damage: int):
        self._worldComponent.animationComponent.addDamage(cell, damage)

    def unitChanged(self, state: GameState, cell: Tuple[int, int], unit: Unit):
        if cell == self.__targetCell:
            self.__updateTarget(cell)

    def unitDied(self, state: GameState, cell: Tuple[int, int]):
        if cell == self.__targetCell:
            self.__updateTarget(cell)
            self._worldComponent.animationComponent.addGrave(cell)
        elif cell == self.__selectedCell:
            self.__clearTarget()
            self.__clearSelection()

    # Notification

    def onArmySelectionChanged(self, cell: Tuple[int, int], army: Army):
        if self.__unitFrame is None:
            return
        if self.__selectedCell != cell:
            return
        if not isinstance(self.__unitFrame, ArmyFrame):
            return
        armyFrame = cast(ArmyFrame, self.__unitFrame)
        movePoints = army.getLowestIntProperty(ItemProperty.MOVE_POINTS, 0, armyFrame.getSelection())
        if movePoints is not None:
            self._shadowLayer.showPaths(self.__distanceMap, movePoints)
            self._shadowLayer.notifyContentChanged()