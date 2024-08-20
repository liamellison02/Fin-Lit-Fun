from typing import Optional, Tuple, Callable, NoReturn

import pygame.draw
from pygame.surface import Surface

from ..Component import Component
from ...IUIEventHandler import IUIEventHandler
from ...Mouse import Mouse
from ...MouseWheel import MouseWheel
from ...theme.Theme import Theme
from ...tools import graySurface


class Toggle(Component, IUIEventHandler):

    def __init__(self, theme: Theme,
                 surface: Surface,
                 action: Optional[Callable[[], NoReturn]] = None):
        self.__icon = surface
        self.__highlight = False
        self.__disabled = False
        self.__action = action
        self.__mouseButtons: Optional[Tuple[bool, bool, bool]] = None
        super().__init__(theme, surface.get_size())

    def setSurface(self, surface: Surface):
        self.__icon = surface
        self.resize(surface.get_size())

    def isEnabled(self) -> bool:
        return not self.__disabled

    def enable(self):
        self.__disabled = False

    def disable(self):
        self.__disabled = True

    def render(self, surface: Surface):
        area = self.area
        icon = self.__icon
        if self.__disabled:
            icon = graySurface(icon)
        if self.__mouseButtons is not None:
            area.move_ip((1, 1))
        if self.__highlight:
            color = self.theme.backgroundColor
            pygame.draw.rect(surface, color, area)
        surface.blit(icon, area.topleft)
        self._needRefresh = False

    # UI Event Handler

    def mouseEnter(self, mouse: Mouse) -> bool:
        super().mouseEnter(mouse)
        self.__highlight = True
        self.__mouseButtons = None
        self._needRefresh = True
        return True

    def mouseLeave(self) -> bool:
        super().mouseLeave()
        self.__highlight = False
        self.__mouseButtons = None
        self._needRefresh = True
        return True

    def mouseButtonDown(self, mouse: Mouse) -> bool:
        self.__mouseButtons = mouse.buttons
        self._needRefresh = True
        return True

    def mouseButtonUp(self, mouse: Mouse) -> bool:
        if self.__mouseButtons is not None:
            self.__disabled = not self.__disabled
            self.__mouseButtons = None
            if self.__action:
                self.__action()
        self._needRefresh = True
        return True

    def mouseWheel(self, mouse: Mouse, wheel: MouseWheel) -> bool:
        return True

    def mouseMove(self, mouse: Mouse) -> bool:
        return True
