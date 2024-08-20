from core.constants import CellValue

objectsTiledef = {
    "imageFile": "toen/objects.png",
    "colorKey": (0, 0, 0),
    "tileSize": (16, 16),
    "tiles": {
        CellValue.NONE: (0, 0),
        CellValue.OBJECTS_CITY: [
            (8, 4), (9, 4), (8, 5), (9, 5),
            (10, 4), (11, 4), (10, 5), (11, 5),
            (12, 4), (13, 4), (12, 5), (13, 5),

            (8, 6), (9, 6), (8, 7), (9, 7),
            (10, 6), (11, 6), (10, 7), (11, 7),
            (12, 6), (13, 6), (12, 7), (13, 7),

            (8, 8), (9, 8), (8, 9), (9, 9),
            (10, 8), (11, 8), (10, 9), (11, 9),
            (12, 8), (13, 8), (12, 9), (13, 9),

            (8, 10), (9, 10), (8, 11), (9, 11),
            (10, 10), (11, 10), (10, 11), (11, 11),
            (12, 10), (13, 10), (12, 11), (13, 11),

            (8, 12), (9, 12), (8, 13), (9, 13),
            (10, 12), (11, 12), (10, 13), (11, 13),
            (12, 12), (13, 12), (12, 13), (13, 13),
        ],
        CellValue.OBJECTS_HILL: [(4, 0), (5, 1)],
        CellValue.OBJECTS_ROCKS: [(6, 1), (7, 1)],
        CellValue.OBJECTS_TREES: [(5, 0), (6, 0), (7, 0)],
        CellValue.OBJECTS_HOUSES: [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2)],
        CellValue.OBJECTS_ROAD_DIRT: (0, 3),
        CellValue.OBJECTS_ROAD_STONE: (4, 3),

        CellValue.OBJECTS_FARM: [(8, 0), (9, 0), (10, 0), (11, 0)],
        CellValue.OBJECTS_MILL: [(0, 1), (1, 1), (2, 1), (3, 1)],
        CellValue.OBJECTS_BAKERY: (12, 2),
        CellValue.OBJECTS_SAWMILL: (8, 2),
        CellValue.OBJECTS_FACTORY: (11, 2),
        CellValue.OBJECTS_MARKET: (10, 2),
        CellValue.OBJECTS_BANK: (9, 2),

        CellValue.OBJECTS_CAMP: (8, 1),
        CellValue.OBJECTS_BOWCAMP: (9, 1),
        CellValue.OBJECTS_SWORDCAMP: (10, 1),
        CellValue.OBJECTS_KNIGHTCAMP: (11, 1),
        CellValue.OBJECTS_SIEGECAMP: (12, 1),
        "bridgeDirt": [(0, 7), (1, 7)],
        "bridgeStone": [(4, 7), (5, 7)],
    },
}