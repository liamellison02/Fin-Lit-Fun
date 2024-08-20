from core.constants import CellValue

groundTiledef = {
    "imageFile": "toen/ground.png",
    "colorKey": (0, 0, 0),
    "tileSize": (16, 16),
    "tiles": {
        CellValue.GROUND_SEA: [(4, 7), (5, 7), (6, 7), (7, 7)],
        CellValue.GROUND_EARTH: [(0, 7), (1, 7), (2, 7), (3, 7)],
    }
}