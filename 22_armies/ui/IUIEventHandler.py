from .Mouse import Mouse
from .MouseWheel import MouseWheel


class IUIEventHandler:

    # Keyboard

    def keyDown(self, key: int) -> bool:
        return False

    def keyUp(self, key: int) -> bool:
        return False

    # Mouse

    def mouseEnter(self, mouse: Mouse) -> bool:
        return False

    def mouseLeave(self) -> bool:
        return False

    def mouseButtonDown(self, mouse: Mouse) -> bool:
        return False

    def mouseButtonUp(self, mouse: Mouse) -> bool:
        return False

    def mouseWheel(self, mouse: Mouse, wheel: MouseWheel) -> bool:
        return False

    def mouseMove(self, mouse: Mouse) -> bool:
        return False

