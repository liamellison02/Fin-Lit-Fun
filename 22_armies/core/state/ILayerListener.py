from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from core.state.Layer import Layer


class ILayerListener:

    def contentChanged(self, layer: Layer):
        pass

    def cellChanged(self, layer: Layer, cell: Tuple[int, int]):
        pass
