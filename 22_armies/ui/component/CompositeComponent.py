import inspect
from itertools import islice
from typing import List, Optional, Tuple, cast

from pygame.surface import Surface

from .CacheComponent import CacheComponent
from .Component import Component
from .IComponentListener import IComponentListener
from ..IUIEventHandler import IUIEventHandler
from ..Mouse import Mouse
from ..MouseWheel import MouseWheel
from ..theme.Theme import Theme


class CompositeComponent(Component, IComponentListener, IUIEventHandler):

    def __init__(self, theme: Theme,
                 size: Optional[Tuple[int, int]] = None):
        super().__init__(theme, size)
        self.__components: List[Component] = []

    def addComponent(self, component: Component, cache: bool = False):
        if cache:
            component = CacheComponent(component)
        self.__components.append(component)

    def removeComponent(self, component: Component):
        for index in range(len(self.__components)):
            if component == self.__components[index]:
                component.dispose()
                del self.__components[index]
                break
            if isinstance(self.__components[index], CacheComponent):
                cacheComponent = cast(CacheComponent, self.__components[index])
                if component == cacheComponent.component:
                    component.dispose()
                    del self.__components[index]
                    break

    def removeAllComponents(self):
        for component in self.__components:
            component.dispose()
        self.__components.clear()

    def moveFront(self, component: Component):
        try:
            index = self.__components.index(component)
            del self.__components[index]
            self.__components.append(component)
        except:
            pass

    def moveTo(self, topLeft: Tuple[int, int]):
        shift = (
            topLeft[0] - self.topLeft[0],
            topLeft[1] - self.topLeft[1]
        )
        self.shiftBy(shift)

    def shiftBy(self, shift: Tuple[int, int]):
        for component in self.__components:
            component.shiftBy(shift)
        super().shiftBy(shift)

    def pack(self):
        minX, minY = 10000, 10000
        maxX, maxY = -10000, -10000
        for component in self.__components:
            x1, y1 = component.topLeft
            x2, y2 = component.bottomRight
            minX, minY = min(minX, x1), min(minY, y1)
            maxX, maxY = max(maxX, x2), max(maxY, y2)
        borderSize = self.theme.framePadding
        super().moveTo((minX - borderSize, minY - borderSize))
        width = maxX - minX + 2 * borderSize
        height = maxY - minY + 2 * borderSize
        super().resize((width, height))

    # Component interface

    def dispose(self):
        for component in self.__components:
            component.dispose()

    def needRefresh(self) -> bool:
        for component in self.__components:
            if component.needRefresh():
                return True
        return self._needRefresh

    def update(self):
        for component in self.__components:
            component.update()

    def render(self, surface: Surface):
        for component in self.__components:
            component.render(surface)

    # UI Event handler

    def keyDown(self, key: int) -> bool:
        for component in reversed(self.__components):
            if not isinstance(component, IUIEventHandler):
                continue
            if component.keyDown(key):
                return True
        return False

    def keyUp(self, key: int) -> bool:
        for component in reversed(self.__components):
            if not isinstance(component, IUIEventHandler):
                continue
            if component.keyUp(key):
                return True
        return False

    def findMouseFocus(self, mouse: Mouse) -> Optional[Component]:
        for component in reversed(self.__components):
            if not isinstance(component, IUIEventHandler):
                continue
            childFocus = component.findMouseFocus(mouse)
            if childFocus is not None:
                return childFocus
        return super().findMouseFocus(mouse)

    def mouseButtonDown(self, mouse: Mouse) -> bool:
        for component in reversed(self.__components):
            if not component.contains(mouse.pixel):
                continue
            if not isinstance(component, IUIEventHandler):
                continue
            if component.mouseButtonDown(mouse):
                return True
        return False

    def mouseButtonUp(self, mouse: Mouse) -> bool:
        for component in reversed(self.__components):
            if not component.contains(mouse.pixel):
                continue
            if not isinstance(component, IUIEventHandler):
                continue
            if component.mouseButtonUp(mouse):
                return True
        return False

    def mouseWheel(self, mouse: Mouse, wheel: MouseWheel) -> bool:
        for component in reversed(self.__components):
            if not component.contains(mouse.pixel):
                continue
            if not isinstance(component, IUIEventHandler):
                continue
            if component.mouseWheel(mouse, wheel):
                return True
        return False

    def mouseMove(self, mouse: Mouse) -> bool:
        for component in reversed(self.__components):
            if not component.contains(mouse.pixel):
                continue
            if not isinstance(component, IUIEventHandler):
                continue
            if component.mouseMove(mouse):
                return True
        return False

    def mouseEnter(self, mouse: Mouse) -> bool:
        for component in reversed(self.__components):
            if not component.contains(mouse.pixel):
                continue
            if not isinstance(component, IUIEventHandler):
                continue
            if component.mouseEnter(mouse):
                return True
        return False

    def mouseLeave(self) -> bool:
        for component in reversed(self.__components):
            if not isinstance(component, IUIEventHandler):
                continue
            if component.mouseLeave():
                return True
        return False

# Dynamic creation of Component listener methods
listenerMethods = inspect.getmembers(IComponentListener, predicate=inspect.isfunction)
for name, method in listenerMethods:
    if name.startswith("__"):
        continue
    signature = inspect.signature(method)
    functionArguments = ", ".join(signature.parameters)
    methodArguments = ", ".join(islice(signature.parameters, 1, None))
    source = f'''
def CompositeComponent_{name}({functionArguments}):
    for component in reversed(self._CompositeComponent__components):
        if isinstance(component, IComponentListener):
            component.{name}({methodArguments})
    '''
    exec(source)
    setattr(CompositeComponent, name, globals()['CompositeComponent_' + name])


