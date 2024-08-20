from typing import Tuple, cast, Optional, Dict

from core.constants import CellValue, ItemProperty, CellUsage, Resource
from core.logic import Logic, Command
from core.logic.command import AssignCell, UnassignCell
from core.state import IGameStateListener, ILayerListener, City, GameState
from .DefaultGameMode import DefaultGameMode
from ..Mouse import Mouse
from ..component.frame import CityFrame, ResourcesFrame, RecruitFrame
from ..layer import SelectionValue, ShadowValue, SelectionItem
from ..notification import UpdateMouseFocusRequested, SetGameModeRequested
from ..theme.Theme import Theme
from ..tools import formatResourceCost


class CityGameMode(DefaultGameMode, IGameStateListener, ILayerListener):

    def __init__(self, theme: Theme, logic: Logic, cityCell: Tuple[int, int], previousView: Tuple[int, int] = (0, 0)):
        super().__init__(theme, logic)

        self.__logic = logic
        self.__cityCell = cityCell
        self.__city = cast(City, logic.world.objects.getItem(cityCell))
        self.__previousView = previousView

        # Selection
        self.__targetAction = ""
        self.__targetCell: Optional[Tuple[int, int]] = None
        self.__selectedCell: Optional[Tuple[int, int]] = None
        self.__updateSelectionLayer()

        # Shadow
        rules = logic.rules
        self._shadowLayer.fill(ShadowValue.SHADOW_MEDIUM)
        pos, cityArea = rules.getCityArea(cityCell, ShadowValue.SHADOW_LIGHT, ShadowValue.SHADOW_MEDIUM)
        self._shadowLayer.blit(pos, cityArea)
        pos, houseArea = rules.getCityHouseArea(cityCell, ShadowValue.NONE, ShadowValue.SHADOW_LIGHT)
        self._shadowLayer.blit(pos, houseArea)

        # Components
        self.__resourcesFrame = ResourcesFrame(theme, logic)
        self.__resourcesFrame.moveRelativeTo("topLeft", self, "topLeft")
        self.addComponent(self.__resourcesFrame, cache=True)

        self.__cityFrame = CityFrame(theme, logic, self.__city)
        self.__cityFrame.moveRelativeTo("topLeft", self.__resourcesFrame, "bottomLeft")
        self.addComponent(self.__cityFrame, cache=True)

        self.__hireFrame = RecruitFrame(self.theme, self.__logic, self.__cityCell)
        self.__hireFrame.moveRelativeTo("bottomRight", self._minimapFrame, "bottomLeft")
        self.addComponent(self.__hireFrame)

        # Listener
        self._state.registerListener(self)
        self._world.units.registerListener(self)

    def dispose(self):
        super().dispose()
        self._state.removeListener(self)
        self._world.units.removeListener(self)

    @property
    def previousView(self) -> Tuple[int, int]:
        return self.__previousView

    def __updateSelectionLayer(self):
        cityCell = self.__cityCell
        city = self.__city
        selectionLayer = self._selectionLayer
        rules = self.__logic.rules

        selectionLayer.clear()
        selectionLayer.setValue(cityCell, SelectionValue.ASSIGNED2)
        resources = city.getResourcesListProperty(ItemProperty.BASE_PRODUCTION, [])
        selectionLayer.setItem(cityCell, SelectionItem(resources, city.playerId))

        for cell in city.cells:
            selectionLayer.setValue(cell, SelectionValue.ASSIGNED)
            resources = rules.computeCellResources(city, cell)
            if len(resources) > 0:
                selectionLayer.setItem(cell, SelectionItem(resources, city.playerId))

    # GameState listener

    def cityCellAssigned(self, state: GameState, cityCell: Tuple[int, int], cell: Tuple[int, int], mode: CellUsage):
        if cell == self.__targetCell:
            self.__updateTarget(cell)

    def cityCellUnassigned(self, state: GameState, cityCell: Tuple[int, int], cell: Tuple[int, int]):
        if cell == self.__targetCell:
            self.__updateTarget(cell)

    def __updateHireFrame(self):
        self.__hireFrame.updateButtons()
        self.__hireFrame.moveRelativeTo("bottomRight", self._minimapFrame, "bottomLeft")
        UpdateMouseFocusRequested().send()

    def unitRecuited(self, state: GameState, cell: Tuple[int, int]):
        self.__updateHireFrame()

    def turnChanged(self, state: GameState):
        self.__updateHireFrame()

    def resourcesChanged(self, state: GameState):
        self.__updateHireFrame()

    # Component listener

    def worldCellEntered(self, cell: Tuple[int, int], mouse: Mouse, dragging: bool):
        self.__updateTarget(cell, mouse)

    def worldCellClicked(self, cell: Tuple[int, int], mouse: Mouse):
        if mouse.button1:
            command: Optional[Command] = None
            if self.__targetAction == "assignCell":
                command = AssignCell(self.__cityCell, cell)
                self._logic.addCommand(command)
            elif self.__targetAction == "unassignCell":
                command = UnassignCell(self.__cityCell, cell)
                self._logic.addCommand(command)
        elif mouse.button3:
            from .WorldGameMode import WorldGameMode
            gameMode = WorldGameMode(self.theme, self._logic)
            gameMode.viewChanged(self.__previousView)
            SetGameModeRequested(gameMode).send()

    def __clearTarget(self):
        targetCell = self.__targetCell
        city = self.__city
        selectionLayer = self._selectionLayer

        if targetCell is not None:
            if targetCell in city.cells:
                selectionLayer.setValue(targetCell, SelectionValue.ASSIGNED)
                resources = self.__logic.rules.computeCellResources(city, targetCell)
                if len(resources) > 0:
                    selectionLayer.setItem(targetCell, SelectionItem(resources, city.playerId))
            else:
                selectionLayer.setValue(self.__targetCell, SelectionValue.NONE)
            selectionLayer.notifyCellChanged(self.__targetCell)
            self.__targetCell = None
            self.__targetAction = ""
        self._selectionLayer.clearNumbers()
        self.hideTooltip()

    def __updateTarget(self, cell: Tuple[int, int], mouse: Optional[Mouse] = None):
        self.__clearTarget()
        logic = self.__logic
        world = logic.world
        rules = logic.rules
        city = self.__city
        cityCell = self.__cityCell

        assignCommand = AssignCell(cityCell, cell)
        if assignCommand.check(logic):
            self.__targetCell = cell
            self.__targetAction = "assignCell"
            self._selectionLayer.setValue(cell, SelectionValue.ASSIGN)
            self._selectionLayer.notifyCellChanged(cell)
            objectValue = world.objects.getValue(cell)
            if objectValue != CellValue.NONE:
                assignTooltip = f"{CellValue.getString(objectValue)}<br>"
                effect = rules.getTileEffectDescription(objectValue)
                assignTooltip += f"{effect}<br>"
            else:
                assignTooltip = ""
            usage = assignCommand.mode
            if usage == CellUsage.HOUSE:
                assignTooltip += '<s color="blue"><leftclick>Add a citizen</s><br>'
            elif usage == CellUsage.PRODUCTION_BUILDING:
                buildingsUpkeep = city.getResourcesDictPerValProperty(ItemProperty.BUILDINGS_UPKEEP)
                if objectValue in buildingsUpkeep:
                    upkeep = buildingsUpkeep[objectValue]
                    assignTooltip += f"Upkeep: {formatResourceCost(upkeep)}<br>"
                assignTooltip += '<s color="blue"><leftclick>Use this building</s><br>'
            elif usage == CellUsage.WORKER:
                assignTooltip += '<s color="blue"><leftclick>Work this tile</s><br>'
            assignTooltip += '<s color="blue"><rightclick>Close city screen</s>'
            self.setTootip(assignTooltip)
            self.showTooltip(mouse)
            return
        assignMessage = assignCommand.message

        unassignCommand = UnassignCell(cityCell, cell)
        if unassignCommand.check(logic):
            self.__targetCell = cell
            self.__targetAction = "unassignCell"
            self._selectionLayer.setValue(cell, SelectionValue.UNASSIGN)
            self._selectionLayer.notifyCellChanged(cell)
            objectValue = world.objects.getValue(cell)
            if objectValue != CellValue.NONE:
                unassignTooltip = f"{CellValue.getString(objectValue)}<br>"
                effect = rules.getTileEffectDescription(objectValue)
                unassignTooltip += f"{effect}<br>"
            else:
                unassignTooltip = ""
            usage = unassignCommand.mode
            if usage == CellUsage.HOUSE:
                unassignTooltip += '<s color="blue"><leftclick>Abandon house</s><br>'
            elif usage in [CellUsage.PRODUCTION_BUILDING, CellUsage.TRAINING_CAMP]:
                buildingsUpkeep = city.getResourcesDictPerValProperty(ItemProperty.BUILDINGS_UPKEEP)
                if objectValue in buildingsUpkeep:
                    upkeep = buildingsUpkeep[objectValue]
                    unassignTooltip += f"Upkeep: {formatResourceCost(upkeep)}<br>"
                unassignTooltip += '<s color="blue"><leftclick>Stop use this building</s><br>'
            elif usage == CellUsage.WORKER:
                unassignTooltip = '<s color="blue"><leftclick>Stop work this tile</s><br>'
            unassignTooltip += '<s color="blue"><rightclick>Close city screen</s>'
            self.setTootip(unassignTooltip)
            self.showTooltip(mouse)
            return
        unassignMessage = unassignCommand.message

        tooltip = ""
        objects = world.objects
        assignedItem = objects.getItem(cell)
        if assignedItem is not None:
            if isinstance(assignedItem, City):
                assignedCity = cast(City, assignedItem)
                if assignedCity == city:
                    if unassignMessage:
                        tooltip += f"{unassignMessage}<br>"
                else:
                    tooltip += f"Assigned to {assignedCity.name}<br>"
        else:
            if assignMessage:
                tooltip += f"{assignMessage}<br>"

        tooltip += '<s color="blue"><rightclick>Close city screen</s>'
        self.setTootip(tooltip)
        self.showTooltip(mouse)

