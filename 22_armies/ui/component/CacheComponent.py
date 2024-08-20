import inspect
from itertools import islice
from typing import Optional, Tuple

import pygame
from pygame.surface import Surface

from .Component import Component
from .IComponentListener import IComponentListener
from ..IUIEventHandler import IUIEventHandler
from ..Mouse import Mouse


class CacheComponent(Component, IComponentListener, IUIEventHandler):

    def __init__(self, component: Component):
        super().__init__(component.theme)
        self.__component = component
        self.__surface: Optional[Surface] = None

    @property
    def component(self) -> Component:
        return self.__component

    @property
    def colorKey(self) -> Optional[Tuple[int, int, int]]:
        return self.__component.colorKey

    # Component

    def dispose(self):
        self.__component.dispose()

    def needRefresh(self) -> bool:
        return self.__component.needRefresh()

    def update(self):
        self.__component.update()

    def render(self, surface: Surface):
        if self.__surface is None or self.__component.needRefresh():
            if self.colorKey is None:
                self.__surface = Surface(surface.get_size(), flags=pygame.SRCALPHA)
            else:
                self.__surface = Surface(surface.get_size())
                self.__surface.set_colorkey(self.colorKey)
            self.__component.render(self.__surface)
            self.resize(self.__component.size)
            self.moveTo(self.__component.topLeft)
        surface.blit(self.__surface, (0, 0))

    def findMouseFocus(self, mouse: Mouse) -> Optional[Component]:
        return self.__component.findMouseFocus(mouse)


# Dynamic creation of UI Event Handler methods
eventHandlerMethods = inspect.getmembers(IUIEventHandler, predicate=inspect.isfunction)
for name, method in eventHandlerMethods:
    if name.startswith("__"):
        continue
    signature = inspect.signature(method)
    functionArguments = ", ".join(signature.parameters)
    methodArguments = ", ".join(islice(signature.parameters, 1, None))
    source = f'''
def CacheComponent_{name}({functionArguments}):
    component = self._CacheComponent__component
    if isinstance(component, IUIEventHandler):
        return component.{name}({methodArguments})
    return False
    '''
    exec(source)
    setattr(CacheComponent, name, globals()['CacheComponent_' + name])

# Dynamic creation of Component listener methods
listenerMethods = inspect.getmembers(IComponentListener, predicate=inspect.isfunction)
for name, method in listenerMethods:
    if name.startswith("__"):
        continue
    signature = inspect.signature(method)
    functionArguments = ", ".join(signature.parameters)
    methodArguments = ", ".join(islice(signature.parameters, 1, None))
    source = f'''
def CacheComponent_{name}({functionArguments}):
    component = self._CacheComponent__component
    if isinstance(component, IComponentListener):
        component.{name}({methodArguments})
    '''
    exec(source)
    setattr(CacheComponent, name, globals()['CacheComponent_' + name])
