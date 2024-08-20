from typing import Tuple, Optional

import pygame

from core.logic import Logic
from core.state import World
from tools.vector import vectorMulI, vectorSubI, vectorClampI, vectorAddI
from .GameMode import GameMode
from .. import Mouse
from ..component.IComponentListener import IComponentListener
from ..component.frame import TooltipFrame
from ..component.frame.MinimapFrame import MinimapFrame
from ..component.world.WorldComponent import WorldComponent
from ..notification import Notification
from ..theme.Theme import Theme


class DefaultGameMode(GameMode, IComponentListener):

    def __init__(self, theme: Theme, logic: Logic):
        super().__init__(theme)
        self._logic = logic
        state = logic.state
        self._state = state
        world = logic.world
        self._world = world
        self.__font = theme.getFont("default")

        # Mouse
        mouseTile = theme.getMouseCursor(state.playerId)
        cursor = pygame.cursors.Cursor((0, 0), mouseTile)
        pygame.mouse.set_cursor(cursor)
        self._mouseScrollScreen: Optional[Tuple[int, int]] = None
        self._mouseScrollView: Optional[Tuple[int, int]] = None

        # Components
        self._worldComponent = WorldComponent(theme, logic)
        self._selectionLayer = self._worldComponent.selectionLayer
        self._shadowLayer = self._worldComponent.shadowLayer

        self._minimapFrame = MinimapFrame(theme, world)
        self._minimapFrame.moveRelativeTo("bottomRight", self, "bottomRight")

        self._tooltipFrame = TooltipFrame(self.theme, "tooltip")
        self._tooltipFrame.hide()

        # Components order
        self.addComponent(self._worldComponent)
        self.addComponent(self._minimapFrame)
        self.addComponent(self._tooltipFrame)

        # Notifications
        Notification.addHandlers({
            "ShowTooltipRequested": self.showTooltipRequested,
            "HideTooltipRequested": self.hideTooltipRequested,
        })

        # Listener
        self._worldComponent.registerListener(self)  # worldCellClicked, ...
        self._minimapFrame.registerListener(self)  # viewChanged

    # Game loop

    def dispose(self):
        super().dispose()
        Notification.removeHandler(self)
        self._worldComponent.removeListener(self)
        self._minimapFrame.removeListener(self)

    @property
    def world(self) -> World:
        return self._world

    @property
    def view(self) -> Tuple[int, int]:
        return self._worldComponent.view

    def update(self):
        self._logic.executeCommands()
        super().update()

    # UI Event handler

    def processInput(self) -> bool:
        # Update view using keyboard state
        keys = pygame.key.get_pressed()
        newViewX, newViewY = self._worldComponent.view
        tileset = self.theme.getTileset("ground")
        tileWidth, tileHeight = tileset.tileSize
        speedX = tileWidth * 2
        speedY = tileHeight * 2
        if keys[pygame.K_RIGHT]:
            newViewX += speedX
        if keys[pygame.K_LEFT]:
            newViewX -= speedX
        if keys[pygame.K_UP]:
            newViewY -= speedY
        if keys[pygame.K_DOWN]:
            newViewY += speedY
        newView = (newViewX, newViewY)

        # Clamp new view
        worldSize = vectorMulI(self._world.size, tileset.tileSize)
        maxView = vectorSubI(worldSize, self.theme.viewSize)
        newView = vectorClampI(newView, 0, maxView)

        # Update only if changes
        if newView != self._worldComponent.view:
            self.viewChanged(newView)
            return True
        return False

    def __computeTooltipCoords(self, mouse: Mouse) -> Tuple[int, int]:
        pixel = vectorAddI(mouse.pixel, self.theme.defaulTileSize)
        size = self._tooltipFrame.size
        bottomRight = vectorAddI(pixel, size)
        if bottomRight[0] >= self.theme.viewSize[0] \
                or bottomRight[1] >= self.theme.viewSize[1]:
            pixel = vectorSubI(mouse.pixel, size)
        return pixel

    def mouseButtonDown(self, mouse: Mouse) -> bool:
        if mouse.button2 or mouse.button3:
            self._mouseScrollScreen = mouse.pixel
            self._mouseScrollView = self._worldComponent.view
        return super().mouseButtonDown(mouse)

    def mouseButtonUp(self, mouse: Mouse) -> bool:
        self._mouseScrollScreen = None
        return super().mouseButtonUp(mouse)

    def mouseEnter(self, mouse: Mouse) -> bool:
        self._mouseScrollScreen = None
        return super().mouseEnter(mouse)

    def mouseLeave(self) -> bool:
        self._mouseScrollScreen = None
        return super().mouseLeave()

    def mouseMove(self, mouse: Mouse) -> bool:
        pixel = self.__computeTooltipCoords(mouse)
        self._tooltipFrame.moveTo(pixel)

        if self._mouseScrollScreen is not None and self._mouseScrollView is not None:
            diff = vectorSubI(mouse.pixel, self._mouseScrollScreen)
            newView = self._mouseScrollView
            newView = vectorSubI(newView, diff)

            # Clamp new view
            tileset = self.theme.getTileset("ground")
            worldSize = vectorMulI(self._world.size, tileset.tileSize)
            maxView = vectorSubI(worldSize, self.theme.viewSize)
            newView = vectorClampI(newView, 0, maxView)

            # Update only if changes
            if newView != self._worldComponent.view:
                self.viewChanged(newView)

        return super().mouseMove(mouse)

    # Notifications

    def showTooltipRequested(self, message: str, maxWidth: int, mouse: Optional[Mouse]):
        self._tooltipFrame.setMessage(message, maxWidth)
        if mouse is not None:
            pixel = self.__computeTooltipCoords(mouse)
            self._tooltipFrame.moveTo(pixel)
        self.moveFront(self._tooltipFrame)
        self._tooltipFrame.show()

    def hideTooltipRequested(self):
        self._tooltipFrame.hide()
