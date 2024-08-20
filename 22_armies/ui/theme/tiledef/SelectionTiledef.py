from typing import Any, Tuple, Union, Dict

import pygame

from tools.vector import vectorSubDiv2I
from ..Tileset import Tileset
from ui.layer.SelectionValue import SelectionValue

selectionTiledef: Dict[str, Any] = {
    "imageFile": "phylyp/selection.png",
    "colorKey": (0, 0, 0),
    "tileSize": (16, 16),
    "tiles": {
        SelectionValue.NONE: (0, 0),
        SelectionValue.SELECTED: [(0, 1, 3, 3), (3, 1, 3, 3), (6, 1, 3, 3), (9, 1, 3, 3), (12, 1, 3, 3)],
        SelectionValue.SELECTED2: [(0, 4, 4, 4), (4, 4, 4, 4), (8, 4, 4, 4), (12, 4, 4, 4), (16, 4, 4, 4)],
        SelectionValue.ATTACK: [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0)],
        SelectionValue.SELECT: [(6, 0), (7, 0), (8, 0), (9, 0), (10, 0)],
        SelectionValue.SELECT2: [(15, 2, 2, 2), (17, 2, 2, 2), (19, 2, 2, 2), (21, 2, 2, 2), (23, 2, 2, 2)],
        SelectionValue.TARGET: [(11, 0), (12, 0), (13, 0), (14, 0), (15, 0)],
        SelectionValue.GRAVE: (11, 0),
        SelectionValue.ASSIGNED: (14, 0),
        SelectionValue.ASSIGN: (15, 0),
        SelectionValue.UNASSIGN: (16, 0),
        SelectionValue.ASSIGNED2: (17, 0, 2, 2),
        SelectionValue.NUMBER_FIRST: (0, 8)
    },
}


def initSelectionTiledef(tileset: Tileset):
    from ...component.text.token.TextStyle import TextStyle

    textStyle = TextStyle("small", "white")
    tileSize = selectionTiledef["tileSize"]
    tiles = selectionTiledef["tiles"]
    x, y = tiles[SelectionValue.NUMBER_FIRST]
    theme = tileset.theme
    surface = tileset.surface
    for value in range(SelectionValue.NUMBER_FIRST, SelectionValue.NUMBER_LAST):
        # Register tile
        tileset.addTile(value, (x, y))

        # Render
        number = value - SelectionValue.NUMBER_FIRST
        textSurface = textStyle.render(theme, f"{number}")
        rect = tileset.getTileRect(value)
        shift = vectorSubDiv2I(tileSize, textSurface.get_size())
        surface.blit(textSurface, rect.move(shift[0], shift[1]))

        # Update coords
        x += 1
        if (x * tileSize[0]) >= surface.get_width():
            x = 0
            y += 1
        if (y * tileSize[1]) >= surface.get_height():
            print(value)
            raise RuntimeError("Selection tileset overflow")
