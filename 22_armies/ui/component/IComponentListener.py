from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Dict, Any

if TYPE_CHECKING:
    from ..Mouse import Mouse


class IComponentListener:

    # World

    def worldCellClicked(self, cell: Tuple[int, int], mouse: Mouse):
        pass

    def worldCellEntered(self, cell: Tuple[int, int], mouse: Mouse, dragging: bool):
        pass

    def viewChanged(self, view: Tuple[int, int]):
        pass

    # Edition

    def mainBrushSelected(self, layerName: str, values: Dict[str, Any]):
        pass

    def secondaryBrushSelected(self, layerName: str, values: Dict[str, Any]):
        pass

