from typing import Tuple, Union


class Mouse:
    def __init__(self,
                 pixel: Tuple[int, int],
                 buttons: Tuple[bool, bool, bool] = (False, False, False)):
        self.pixel = pixel
        self.buttons = buttons

    @property
    def x(self) -> int:
        return self.pixel[0]

    @property
    def y(self) -> int:
        return self.pixel[1]

    @property
    def button1(self) -> bool:
        return self.buttons[0]

    @property
    def button2(self) -> bool:
        return self.buttons[1]

    @property
    def button3(self) -> bool:
        return self.buttons[2]
