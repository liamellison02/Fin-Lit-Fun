from __future__ import annotations

from abc import abstractmethod
from typing import Tuple, Optional, TYPE_CHECKING, Dict, Any

from pygame.rect import Rect
from pygame.surface import Surface

from core import Listenable
from tools.vector import vectorMulI, vectorAddI, vectorSubI, vectorMulF, vectorFtoI
from .IComponentListener import IComponentListener
from ..IUIEventHandler import IUIEventHandler
from ..theme.Theme import Theme
from ..notification.HideTooltipRequested import HideTooltipRequested
from ..notification.ShowTooltipRequested import ShowTooltipRequested

if TYPE_CHECKING:
    from ..Mouse import Mouse


class Component(Listenable[IComponentListener], IUIEventHandler):
    def __init__(self, theme: Theme,
                 size: Optional[Tuple[int, int]] = None,
                 colorKey: Optional[Tuple[int, int, int]] = (0, 0, 0)):
        super().__init__()
        self.__theme = theme
        if size is None:
            self.__area = Rect(0, 0, theme.viewSize[0], theme.viewSize[1])
        else:
            self.__area = Rect(0, 0, size[0], size[1])
        self.__colorKey = colorKey
        self._needRefresh = True

        self.__tooltipMessage: Optional[str] = None
        self.__tooltipMaxWidth = 300

    @property
    def theme(self) -> Theme:
        return self.__theme

    def contains(self, pixel: Tuple[int, int]) -> bool:
        return self.__area.collidepoint(pixel) != 0

    @property
    def colorKey(self) -> Optional[Tuple[int, int, int]]:
        return self.__colorKey

    @property
    def area(self) -> Rect:
        return self.__area.copy()

    @property
    def topLeft(self) -> Tuple[int, int]:
        return int(self.__area.left), int(self.__area.top)

    @property
    def topRight(self) -> Tuple[int, int]:
        return int(self.__area.right), int(self.__area.top)

    @property
    def bottomLeft(self) -> Tuple[int, int]:
        return int(self.__area.left), int(self.__area.bottom)

    @property
    def bottomRight(self) -> Tuple[int, int]:
        return int(self.__area.right), int(self.__area.bottom)

    @property
    def top(self) -> int:
        return int(self.__area.top)

    @property
    def right(self) -> int:
        return int(self.__area.right)

    @property
    def left(self) -> int:
        return int(self.__area.left)

    @property
    def bottom(self) -> int:
        return int(self.__area.bottom)

    @property
    def size(self) -> Tuple[int, int]:
        return int(self.__area.width), int(self.__area.height)

    def resize(self, size: Tuple[int, int]):
        self.__area.size = size
        self._needRefresh = True

    def setTootip(self, message: str, maxWidth: int = 150):
        self.__tooltipMessage = message
        self.__tooltipMaxWidth = maxWidth

    def showTooltip(self, mouse: Optional[Mouse]):
        if self.__tooltipMessage is not None:
            ShowTooltipRequested(self.__tooltipMessage, self.__tooltipMaxWidth, mouse).send()

    def disableTooltip(self):
        if self.__tooltipMessage is not None:
            self.__tooltipMessage = None
        HideTooltipRequested().send()

    def hideTooltip(self):
        HideTooltipRequested().send()

    # Anchors

    def moveRelativeTo(self,
                       anchor: str,
                       other: Optional[Component] = None,
                       otherAnchor: str = "center",
                       borderX: Optional[int] = None,
                       borderY: Optional[int] = None,
                       borderSize: Optional[int] = None):
        if other is None:
            otherPos = (0, 0)
            otherSize = self.theme.viewSize
        else:
            otherPos = other.topLeft
            otherSize = other.size
        if borderSize is None:
            if anchor == otherAnchor:
                borderSize = self.theme.framePadding
            else:
                borderSize = self.theme.frameMargin

        assert otherAnchor in relativeAnchors, f"Invalid anchor {otherAnchor}"
        otherShift = vectorMulF(relativeAnchors[otherAnchor], otherSize)
        pos = vectorAddI(otherPos, vectorFtoI(otherShift))

        assert anchor in relativeAnchors, f"Invalid anchor {anchor}"
        shift = vectorMulF(relativeAnchors[anchor], self.size)
        pos = vectorSubI(pos, vectorFtoI(shift))

        defaultBorder = defaultBorderShifts[anchor][otherAnchor]
        defaultBorder = vectorMulI(defaultBorder, (borderSize, borderSize))
        if borderX is None:
            borderX = defaultBorder[0]
        if borderY is None:
            borderY = defaultBorder[1]
        pos = vectorAddI(pos, (borderX, borderY))

        self.moveTo(pos)

    def moveTo(self, topLeft: Tuple[int, int]):
        self.__area.update(topLeft, self.size)
        self._needRefresh = True

    def shiftBy(self, shift: Tuple[int, int]):
        self.__area.move_ip(shift)
        self._needRefresh = True

    # Component

    def dispose(self):
        pass

    def needRefresh(self) -> bool:
        return self._needRefresh

    def update(self):
        pass

    @abstractmethod
    def render(self, surface: Surface):
        raise NotImplementedError()

    def findMouseFocus(self, mouse: Mouse) -> Optional[Component]:
        if not isinstance(self, IUIEventHandler):
            return None
        if not self.contains(mouse.pixel):
            return None
        return self

    # Component Listener

    def notifyWorldCellClicked(self, cell: Tuple[int, int], mouse: Mouse):
        for listener in self.listeners:
            listener.worldCellClicked(cell, mouse)

    def notifyWorldCellEntered(self, cell: Tuple[int, int], mouse: Mouse, dragging: bool):
        for listener in self.listeners:
            listener.worldCellEntered(cell, mouse, dragging)

    def notifyViewChanged(self, view: Tuple[int, int]):
        for listener in self.listeners:
            listener.viewChanged(view)

    # Edition

    def notifyMainBrushSelected(self, layerName: str, values: Dict[str, Any]):
        for listener in self.listeners:
            listener.mainBrushSelected(layerName, values)

    def notifySecondaryBrushSelected(self, layerName: str, values: Dict[str, Any]):
        for listener in self.listeners:
            listener.secondaryBrushSelected(layerName, values)

    # UI Event Handler

    def mouseEnter(self, mouse: Mouse) -> bool:
        if self.__tooltipMessage is not None:
            self.showTooltip(mouse)
        else:
            self.hideTooltip()
        return False

    def mouseLeave(self) -> bool:
        self.hideTooltip()
        return False


relativeAnchors = {
    None: (0, 0),
    "topLeft": (0, 0),
    "top": (0.5, 0),
    "topRight": (1, 0),
    "left": (0, 0.5),
    "center": (0.5, 0.5),
    "right": (1, 0.5),
    "bottomLeft": (0, 1),
    "bottom": (0.5, 1),
    "bottomRight": (1, 1)
}

defaultBorderShifts = {
    "topLeft": {
        "topLeft": (1, 1),
        "top": (0, 1),
        "topRight": (1, 0),
        "left": (1, 0),
        "center": (0, 0),
        "right": (1, 0),
        "bottomLeft": (0, 1),
        "bottom": (0, 1),
        "bottomRight": (1, 1)
    },
    "top": {
        "topLeft": (0, 1),
        "top": (0, 1),
        "topRight": (0, 1),
        "left": (0, 0),
        "center": (0, 0),
        "right": (0, 0),
        "bottomLeft": (0, 1),
        "bottom": (0, 1),
        "bottomRight": (0, 1)
    },
    "topRight": {
        "topLeft": (-1, 0),
        "top": (0, 1),
        "topRight": (-1, 1),
        "left": (-1, 0),
        "center": (0, 0),
        "right": (-1, 0),
        "bottomLeft": (-1, 1),
        "bottom": (0, 1),
        "bottomRight": (0, 1)
    },
    "left": {
        "topLeft": (1, 0),
        "top": (0, 0),
        "topRight": (1, 0),
        "left": (1, 0),
        "center": (0, 0),
        "right": (1, 0),
        "bottomLeft": (1, 0),
        "bottom": (0, 0),
        "bottomRight": (1, 0)
    },
    "center": {
        "topLeft": (0, 0),
        "top": (0, 0),
        "topRight": (0, 0),
        "left": (0, 0),
        "center": (0, 0),
        "right": (0, 0),
        "bottomLeft": (0, 0),
        "bottom": (0, 0),
        "bottomRight": (0, 0)
    },
    "right": {
        "topLeft": (-1, 0),
        "top": (0, 0),
        "topRight": (-1, 0),
        "left": (-1, 0),
        "center": (0, 0),
        "right": (-1, 0),
        "bottomLeft": (-1, 0),
        "bottom": (0, 0),
        "bottomRight": (-1, 0)
    },
    "bottomLeft": {
        "topLeft": (0, -1),
        "top": (0, -1),
        "topRight": (1, -1),
        "left": (1, 0),
        "center": (0, 0),
        "right": (1, 0),
        "bottomLeft": (1, -1),
        "bottom": (0, -1),
        "bottomRight": (1, 0)
    },
    "bottom": {
        "topLeft": (0, -1),
        "top": (0, -1),
        "topRight": (0, -1),
        "left": (0, 0),
        "center": (0, 0),
        "right": (0, 0),
        "bottomLeft": (0, -1),
        "bottom": (0, -1),
        "bottomRight": (0, -1)
    },
    "bottomRight": {
        "topLeft": (-1, -1),
        "top": (0, -1),
        "topRight": (0, -1),
        "left": (-1, 0),
        "center": (0, 0),
        "right": (-1, 0),
        "bottomLeft": (-1, 0),
        "bottom": (0, -1),
        "bottomRight": (-1, -1)
    },
}