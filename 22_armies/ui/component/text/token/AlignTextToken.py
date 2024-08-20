from .TextToken import TextToken


class AlignTextToken(TextToken):
    __slots__ = ["__x"]

    def __init__(self, x: int):
        self.__x = x

    @property
    def x(self) -> int:
        return self.__x

