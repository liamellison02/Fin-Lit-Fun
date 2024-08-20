from .TextToken import TextToken


class SpaceTextToken(TextToken):
    __slots__ = ["__count"]

    def __init__(self, count: int):
        self.__count = count

    @property
    def count(self) -> int:
        return self.__count

