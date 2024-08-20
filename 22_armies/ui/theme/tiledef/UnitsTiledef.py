from core.constants import UnitClass

unitsTiledef = {
    "imageFile": "toen/units.png",
    "colorKey": (0, 0, 0),
    "tileSize": (16, 16),
    "tiles": {
        UnitClass.NONE: [(0, 0)],
        UnitClass.WORKER: [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 0)],
        UnitClass.FARMER: [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (3, 0)],
        UnitClass.BOWMAN: [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (5, 0)],
        UnitClass.PIKEMAN: [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (6, 0)],
        UnitClass.SWORDSMAN: [(6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (7, 0)],
        UnitClass.KNIGHT: [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (8, 0)],
        UnitClass.CATAPULT: [(8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (9, 0)],
    },
}
