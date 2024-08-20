from core.constants import Resource

resourcesTiledef = {
    "imageFile": "phylyp/frame.png",
    "colorKey": (0, 0, 0),
    "tileSize": (5, 5),
    "tiles": {
        Resource.FOOD: (0, 4),
        Resource.GOLD: (1, 4),
        Resource.WOOD: (2, 4),
        Resource.STONE: (3, 4),
    },
}
