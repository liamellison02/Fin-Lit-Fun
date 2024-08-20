from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from core.state.item.Unit import Unit
from ..constants import CellUsage

if TYPE_CHECKING:
    from .GameState import GameState


class IGameStateListener:

    def turnChanged(self, state: GameState):
        pass

    def resourcesChanged(self, state: GameState):
        pass

    def cityCellAssigned(self, state: GameState, cityCell: Tuple[int, int], cell: Tuple[int, int], mode: CellUsage):
        pass

    def cityCellUnassigned(self, state: GameState, cityCell: Tuple[int, int], cell: Tuple[int, int]):
        pass

    def unitRecuited(self, state: GameState, cell: Tuple[int, int]):
        pass

    def unitMoved(self, state: GameState,
                  fromCell: Tuple[int, int], toCell: Tuple[int, int]):
        pass

    def unitChanged(self, state: GameState, cell: Tuple[int, int], unit: Unit):
        pass

    def unitDamaged(self, state: GameState, cell: Tuple[int, int], damage: int):
        pass

    def unitDied(self, state: GameState, cell: Tuple[int, int]):
        pass

