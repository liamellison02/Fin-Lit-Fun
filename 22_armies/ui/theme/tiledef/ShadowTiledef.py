from typing import Any, Dict

from ui.layer.ShadowValue import ShadowValue

shadowTiledef: Dict[str, Any] = {
    "imageFile": "phylyp/shadow.png",
    "colorKey": None,
    "tileSize": (16, 16),
    "tiles": {
        ShadowValue.NONE: (0, 0),
        ShadowValue.SHADOW_LIGHT: (1, 1),
        ShadowValue.SHADOW_MEDIUM: (1, 0),
        ShadowValue.SHADOW_HIGH: (0, 1),
    },
}
