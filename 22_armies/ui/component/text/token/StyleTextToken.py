from .TextToken import TextToken
from ui.component.text.token.TextStyle import TextStyle


class StyleTextToken(TextToken):

    __slots__ = ["__style"]

    def __init__(self, style: TextStyle):
        self.__style = style

    @property
    def style(self) -> TextStyle:
        return self.__style
