from typing import Tuple, Optional, List, Dict

from core.logic import Logic
from core.state import Layer, ILayerListener
from tools.vector import vectorDivI, vectorAddI
from . import ResourcesComponent
from .AnimationComponent import AnimationComponent
from .LayerComponent import LayerComponent
from .LayerComponentFactory import LayerComponentFactory
from .SelectionComponent import SelectionComponent
from .ShadowComponent import ShadowComponent
from ..CompositeComponent import CompositeComponent
from ...IUIEventHandler import IUIEventHandler
from ...Mouse import Mouse
from ...layer import SelectionLayer, ShadowLayer
from ...theme.Theme import Theme


class WorldComponent(CompositeComponent, IUIEventHandler, ILayerListener):

    def __init__(self, theme: Theme, logic: Logic):
        super().__init__(theme)
        state = logic.state
        self.__world = world = state.world
        self.__view = (0, 0)
        self.__previousCell: Optional[Tuple[int, int]] = None
        self.__mouseButtonDown = False

        self.__layers: List[Layer] = []
        self.__layerComponents: Dict[str, LayerComponent] = {}
        factory = LayerComponentFactory(theme, world)
        for name in world.layerNames:
            layerComponent = factory.create(name)
            self.addComponent(layerComponent, cache=True)
            self.__layerComponents[name] = layerComponent

            layer = world.getLayer(name)
            layer.registerListener(self)
            self.__layers.append(layer)

        # Shadow layer
        self.__shadowLayer = ShadowLayer(world.size)
        self.__shadowComponent = ShadowComponent(theme, state, self.__shadowLayer)
        self.addComponent(self.__shadowComponent, cache=True)

        # Selection layer
        self.__selectionLayer = SelectionLayer(world.size)
        self.__selectionComponent = SelectionComponent(theme, state, self.__selectionLayer)
        self.addComponent(self.__selectionComponent, cache=True)

        # Animation component
        self.__animationComponent = AnimationComponent(theme, state, self.__selectionLayer)
        self.addComponent(self.__animationComponent, cache=False)

        self.__tileSize = theme.getTileset(world.layerNames[0]).tileSize

    def dispose(self):
        for layer in self.__layers:
            layer.removeListener(self)
        super().dispose()

    @property
    def view(self) -> Tuple[int, int]:
        return self.__view

    @property
    def shadowLayer(self) -> ShadowLayer:
        return self.__shadowLayer

    @property
    def selectionLayer(self) -> SelectionLayer:
        return self.__selectionLayer

    @property
    def selectionComponent(self) -> SelectionComponent:
        return self.__selectionComponent

    @property
    def animationComponent(self) -> AnimationComponent:
        return self.__animationComponent

    # Layer listener

    def cellChanged(self, layer: Layer, cell: Tuple[int, int]):
        for layerComponent in self.__layerComponents.values():
            layerComponent.cellChanged(layer, cell)

    # Component listener

    def viewChanged(self, view: Tuple[int, int]):
        super().viewChanged(view)
        self.__view = view

    # UI Event Handler

    def __computeCellCoordinates(self, pixel: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        pixel = vectorAddI(pixel, self.__view)
        cell = vectorDivI(pixel, self.__tileSize)
        if not self.__world.contains(cell):
            return None
        return cell

    def mouseButtonDown(self, mouse: Mouse) -> bool:
        super().mouseButtonDown(mouse)
        cell = self.__computeCellCoordinates(mouse.pixel)
        if cell is None:
            return False
        self.__mouseButtonDown = True
        self.notifyWorldCellClicked(cell, mouse)
        return True

    def mouseMove(self, mouse: Mouse) -> bool:
        cell = self.__computeCellCoordinates(mouse.pixel)
        if cell is None:
            self.__previousCell = None
            return False
        if self.__previousCell is not None and cell == self.__previousCell:
            return False
        self.__previousCell = cell
        self.notifyWorldCellEntered(cell, mouse, self.__mouseButtonDown)
        return True

    def mouseButtonUp(self, mouse: Mouse) -> bool:
        self.__mouseButtonDown = False
        return True

    def mouseEnter(self, mouse: Mouse) -> bool:
        super().mouseEnter(mouse)
        self.__mouseButtonDown = False
        return True

    def mouseLeave(self) -> bool:
        super().mouseLeave()
        self.__mouseButtonDown = False
        self.__previousCell = None
        return True
