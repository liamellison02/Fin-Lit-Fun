from typing import Optional, List

import pygame
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface

from tools.vector import vectorDivF, vectorMulI
from .IUIEventHandler import IUIEventHandler
from .Mouse import Mouse
from .MouseWheel import MouseWheel
from .component.Component import Component
from .component.IComponentListener import IComponentListener
from .mode.GameMode import GameMode
from .notification import Notification
from .theme.Theme import Theme


class UserInterface(IComponentListener):
    def __init__(self, theme: Theme):

        # Create window with default resolution
        pygame.init()
        windowSize = vectorMulI(theme.viewSize, (3, 3))
        self.__window = pygame.display.set_mode(windowSize, HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption("2D Medieval Strategy Game with Python, http://www.patternsgameprog.com")
        pygame.display.set_icon(pygame.image.load("assets/toen/icon.png"))

        # Rendering
        self.__theme = theme
        self.__rescaledShift = (0, 0)
        self.__rescaledScale = (1.0, 1.0)
        self.__font = theme.getFont("default")
        self.__renderSurface = Surface(theme.viewSize)

        # Inputs
        self.__mouseFocus: Optional[Component] = None

        # Notifications
        Notification.addHandlers({
            "UpdateMouseFocusRequested": self.updateMouseFocusRequested,
            "SetGameModeRequested": self.setGameModeRequested,
            "SetOverlayGameModeRequested": self.setOverlayGameModeRequested,
            "ShowMessageRequested": self.showMessageRequested,
        })

        # Other
        self.__gameMode: Optional[GameMode] = None
        self.__overlayGameMode: Optional[GameMode] = None
        self.__running = True
        self.__clock = pygame.time.Clock()
        self.__frameCount = 0
        self.__updateRate = 1

    @property
    def theme(self) -> Theme:
        return self.__theme

    def setGameMode(self, gameMode: Optional[GameMode]):
        if self.__gameMode is not None:
            self.__gameMode.removeListener(self)
            self.__gameMode.dispose()
        self.__gameMode = gameMode
        if self.__gameMode is not None:
            self.__gameMode.registerListener(self)

    def setOverlayGameMode(self, gameMode: Optional[GameMode]):
        if self.__overlayGameMode is not None:
            self.__overlayGameMode.removeListener(self)
            self.__overlayGameMode.dispose()
        self.__overlayGameMode = gameMode
        if self.__overlayGameMode is not None:
            self.__overlayGameMode.registerListener(self)

    def __processKeyEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PRINTSCREEN:
                size = self.__renderSurface.get_size()
                rescaledSurface = pygame.transform.scale(self.__renderSurface, (4*size[0], 4*size[1]))
                pygame.image.save(rescaledSurface, "capture.png")
            else:
                self.handleKeyDown(event.key)
        elif event.type == pygame.KEYUP:
            self.handleKeyUp(event.key)

    def __createMouse(self) -> Mouse:
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX = int((mouseX - self.__rescaledShift[0]) / self.__rescaledScale[0])
        mouseY = int((mouseY - self.__rescaledShift[1]) / self.__rescaledScale[1])
        buttons = pygame.mouse.get_pressed(num_buttons=3)
        return Mouse((mouseX, mouseY), (buttons[0], buttons[1], buttons[2]))

    def __updateMouseFocus(self):
        # Mouse
        if pygame.mouse.get_focused():
            mouse = self.__createMouse()
            newFocus = self.findMouseFocus(mouse)
        else:
            mouse = Mouse((-10000, -10000))
            newFocus = None
        if newFocus != self.__mouseFocus:
            #print("focus", self.__mouseFocus.__class__.__name__, "=>", newFocus.__class__.__name__)
            if self.__mouseFocus is not None \
                    and isinstance(self.__mouseFocus, IUIEventHandler):
                self.__mouseFocus.mouseLeave()
            self.__mouseFocus = newFocus
            if self.__mouseFocus is not None \
                    and isinstance(self.__mouseFocus, IUIEventHandler):
                self.__mouseFocus.mouseEnter(mouse)

    def __processMouseEvent(self, event):
        mouse = self.__createMouse()
        viewSize = self.__theme.viewSize
        if 0 <= mouse.pixel[0] < viewSize[0] \
                and 0 <= mouse.pixel[1] < viewSize[1]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handleMouseButtonDown(mouse)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handleMouseButtonUp(mouse)
            elif event.type == pygame.MOUSEWHEEL:
                wheel = MouseWheel(event.x, event.y, event.flipped)
                self.handleMouseWheel(mouse, wheel)
            elif event.type == pygame.MOUSEMOTION:
                self.handleMouseMove(mouse)

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                break
            elif event.type == pygame.KEYDOWN \
                    or event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.__running = False
                    break
                self.__processKeyEvent(event)
            elif event.type == pygame.MOUSEMOTION:
                self.__updateMouseFocus()
                self.__processMouseEvent(event)
            elif event.type == pygame.MOUSEBUTTONDOWN \
                    or event.type == pygame.MOUSEBUTTONUP \
                    or event.type == pygame.MOUSEWHEEL \
                    or event.type == pygame.MOUSEMOTION:
                self.__processMouseEvent(event)
        if self.__overlayGameMode is not None:
            self.__overlayGameMode.processInput()
        elif self.__gameMode is not None:
            self.__gameMode.processInput()

    def update(self):
        if self.__overlayGameMode is not None:
            self.__overlayGameMode.update()
        elif self.__gameMode is not None:
            self.__gameMode.update()
        Notification.notifyAll()

    def render(self):
        # Render world in a surface
        self.__renderSurface.fill((0, 0, 0))
        if self.__gameMode is not None:
            self.__gameMode.render(self.__renderSurface)
        if self.__overlayGameMode is not None:
            self.__overlayGameMode.render(self.__renderSurface)

        # Scale rendering to window size
        windowWidth, windowHeight = self.__window.get_size()
        viewSize = self.__theme.viewSize
        renderRatio = viewSize[0] / viewSize[1]
        windowRatio = windowWidth / windowHeight
        if windowRatio <= renderRatio:
            rescaledSize = (windowWidth, int(windowWidth / renderRatio))
            self.__rescaledShift = (0, (windowHeight - rescaledSize[1]) // 2)
        else:
            rescaledSize = (int(windowHeight * renderRatio), windowHeight)
            self.__rescaledShift = ((windowWidth - rescaledSize[0]) // 2, 0)

        # Scale the rendering to the window/screen size
        rescaledSurface = pygame.transform.scale(self.__renderSurface, rescaledSize)
        self.__rescaledScale = vectorDivF(rescaledSurface.get_size(), self.__renderSurface.get_size())
        self.__window.blit(rescaledSurface, self.__rescaledShift)

        # Draw frame time
        frameTime = self.__clock.get_rawtime()
        textSurface = self.__font.render(f"{frameTime}ms", False, (255, 255, 255), (0, 0, 0))
        self.__window.blit(
            textSurface, (
                self.__window.get_width() - textSurface.get_width(),
                self.__window.get_height() - textSurface.get_height()
            )
        )

    def run(self):
        # Main game loop
        while self.__running:
            self.processInput()
            if (self.__frameCount % self.__updateRate) == 0:
                self.update()
            self.render()

            pygame.display.update()
            self.__clock.tick(30)
            self.__frameCount += 1

        if self.__gameMode is not None:
            self.__gameMode.removeListener(self)
            self.__gameMode.dispose()
        if self.__overlayGameMode is not None:
            self.__overlayGameMode.removeListener(self)
            self.__overlayGameMode.dispose()

    # Quit

    def quit(self):
        Notification.removeHandler(self)
        pygame.quit()

    # Event handling

    def getEventHandlers(self) -> List[GameMode]:
        if self.__overlayGameMode is not None:
            return [self.__overlayGameMode]
        if self.__gameMode is not None:
            return [self.__gameMode]
        return []

    def handleKeyDown(self, key: int) -> bool:
        for handler in self.getEventHandlers():
            if handler.keyDown(key):
                return True
        return False

    def handleKeyUp(self, key: int) -> bool:
        for handler in self.getEventHandlers():
            if handler.keyUp(key):
                return True
        return False

    def findMouseFocus(self, mouse: Mouse) -> Optional[Component]:
        for handler in self.getEventHandlers():
            focus = handler.findMouseFocus(mouse)
            if focus is not None:
                return focus
        return None

    def handleMouseButtonDown(self, mouse: Mouse) -> bool:
        for handler in self.getEventHandlers():
            if handler.mouseButtonDown(mouse):
                return True
        return False

    def handleMouseButtonUp(self, mouse: Mouse) -> bool:
        for handler in self.getEventHandlers():
            if handler.mouseButtonUp(mouse):
                return True
        return False

    def handleMouseWheel(self, mouse: Mouse, wheel: MouseWheel) -> bool:
        for handler in self.getEventHandlers():
            if handler.mouseWheel(mouse, wheel):
                return True
        return False

    def handleMouseMove(self, mouse: Mouse) -> bool:
        for handler in self.getEventHandlers():
            if handler.mouseMove(mouse):
                return True
        return False

    # Notifications

    def setGameModeRequested(self, gameMode: Optional[GameMode]):
        self.setGameMode(gameMode)

    def setOverlayGameModeRequested(self, gameMode: Optional[GameMode]):
        self.setOverlayGameMode(gameMode)

    def showMessageRequested(self, message: str, portrait: str):
        from .mode.MessageGameMode import MessageGameMode
        gameMode = MessageGameMode(self.theme, message, portrait)
        self.setOverlayGameMode(gameMode)

    def updateMouseFocusRequested(self):
        self.__updateMouseFocus()