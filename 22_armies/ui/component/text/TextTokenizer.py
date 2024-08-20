import logging
from html.parser import HTMLParser
from typing import List, Optional, Tuple

from .token import ContentTextToken, IconTextToken, ReturnTextToken, TextToken, StyleTextToken, SpaceTextToken, \
    TextStyle, AlignTextToken
from ...theme.Theme import Theme


class TextTokenizer(HTMLParser):

    def __init__(self, theme: Theme):
        super(TextTokenizer, self).__init__()
        self.__tokens: List[TextToken] = []
        self.__styleStack: List[TextStyle] = []
        self.__frameTileset = theme.getTileset("frame")

    def parse(self, content: str, style: TextStyle) -> List[TextToken]:
        self.__styleStack.clear()
        self.__styleStack.append(style)
        self.__tokens.clear()
        self.feed(content)
        return self.__tokens

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        if tag == "flag":
            for name, value in attrs:
                if name == "player" and value is not None:
                    try:
                        playerId = int(value)
                        assert 0 <= playerId <= 4
                        token = IconTextToken(
                            self.__frameTileset.surface,
                            self.__frameTileset.getTileRects("flag")[playerId]
                        )
                        self.__tokens.append(token)
                    except:
                        logging.warning(f"Invalid value {value} for attribute {name} for <flag>")
                else:
                    logging.warning(f"Invalid attribute {name} for <flag>")
        elif tag == "br":
            self.__tokens.append(ReturnTextToken())
        elif tag == "space":
            count = 1
            for name, value in attrs:
                if name == "count" and value is not None:
                    try:
                        count = int(value)
                    except:
                        logging.warning(f"Invalid value {value} for attribute {name} for <flag>")
                else:
                    logging.warning(f"Invalid attribute {name} for <s>")
            self.__tokens.append(SpaceTextToken(count))
        elif tag == "align":
            x = 1
            for name, value in attrs:
                if name == "x" and value is not None:
                    try:
                        x = int(value)
                    except:
                        logging.warning(f"Invalid value {value} for attribute {name} for <flag>")
                else:
                    logging.warning(f"Invalid attribute {name} for <s>")
            self.__tokens.append(AlignTextToken(x))
        elif self.__frameTileset.hasTileRects(tag):
            token = IconTextToken(
                self.__frameTileset.surface,
                self.__frameTileset.getTileRect(tag)
            )
            self.__tokens.append(token)
        else:
            currentStyle = self.__styleStack[-1]
            newStyle: Optional[TextStyle] = None
            if tag == "i":
                newStyle = currentStyle.styleItalic()
            elif tag == "b":
                newStyle = currentStyle.styleBold()
            elif tag == "u":
                newStyle = currentStyle.styleUnderline()
            elif tag == "s":
                for name, value in attrs:
                    if name == "color":
                        newStyle = currentStyle.styleColor(value)
                    else:
                        logging.warning(f"Invalid attribute {name} for <s>")
            else:
                logging.warning(f"Invalid or unsupported tag '{tag}'")
            if newStyle is not None:
                self.__styleStack.append(newStyle)
                self.__tokens.append(StyleTextToken(newStyle))

    def handle_data(self, content):
        if len(content) > 0:
            self.__tokens.append(ContentTextToken(content))

    def handle_endtag(self, tag):
        currentStyle = self.__styleStack[-1]
        if tag == "i":
            assert currentStyle.italic
        elif tag == "b":
            assert currentStyle.bold
        elif tag == "u":
            assert currentStyle.underline
        elif tag == "s":
            pass
        else:
            logging.warning(f"Invalid or unsupported end tag {tag}")
        self.__styleStack.pop()
        self.__tokens.append(StyleTextToken(self.__styleStack[-1]))


