from core.constants import CellValue

impassableTiledef = {
    "imageFile": "toen/impassable.png",
    "colorKey": (0, 0, 0),
    "tileSize": (16, 16),
    "tiles": {
        CellValue.NONE: (0, 0),
        CellValue.IMPASSABLE_RIVER: (0, 1),
        CellValue.IMPASSABLE_POND: [(1, 0), (2, 0), (3, 0)],
        CellValue.IMPASSABLE_MOUNTAIN: [(4, 0), (5, 0), (6, 0)],
        "riverMouthRight": (4, 1),
        "riverMouthLeft": (4, 2),
        "riverMouthTop": (4, 3),
        "riverMouthBottom": (4, 4),
    }
}
