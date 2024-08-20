import logging
import os.path
from typing import Dict, Any, cast, Optional, List, Tuple

from .IGameStateListener import IGameStateListener
from .Player import Player
from .World import World
from .item.Unit import Unit
from ..IDataTransfer import IDataTransfer
from ..Listenable import Listenable
from ..constants import CellUsage


class GameState(Listenable[IGameStateListener], IDataTransfer):
    def __init__(self, world: Optional[World] = None):
        super().__init__()
        self.__playerId = 1
        if world is None:
            world = World((10, 10))
        self.__world = world
        self.__turn = 1
        self.__players = [
            Player(1)
        ]

    def __eq__(self, other) -> bool:
        if not isinstance(other, GameState):
            return False
        state = cast(GameState, other)
        if self.__playerId != state.__playerId:
            return False
        if self.__world != state.__world:
            return False
        if self.__turn != state.__turn:
            return False
        if self.__players != state.__players:
            return False
        return True

    @property
    def world(self) -> World:
        return self.__world

    @property
    def turn(self) -> int:
        return self.__turn

    @turn.setter
    def turn(self, turn: int):
        self.__turn = turn

    @property
    def playerId(self) -> int:
        return self.__playerId

    @playerId.setter
    def playerId(self, playerId: int):
        assert playerId in self.playerIds
        self.__playerId = playerId

    @property
    def playerIds(self) -> List[int]:
        return [player.id for player in self.__players]

    @property
    def players(self) -> List[Player]:
        return self.__players.copy()

    def getPlayer(self, playerId: int = -1) -> Player:
        if playerId < 0:
            playerId = self.__playerId
        for player in self.__players:
            if player.id == playerId:
                return player
        raise ValueError(f"No player id {playerId}")

    # Data transfer

    def load(self, fileName: str):
        logging.info(f"Load state from {fileName}...")
        ext = os.path.splitext(fileName)[1]
        if ext == ".json":
            import json
            with open(fileName, encoding='utf-8') as file:
                data = json.load(file)
        elif ext == ".pickle":
            import pickle
            with open(fileName, 'rb') as bfile:
                data = pickle.load(bfile)
        elif ext == ".msgpack":
            import msgpack
            with open(fileName, 'rb') as bfile:
                data = msgpack.load(bfile)
        else:
            raise ValueError(f"Invalid file extension {ext}")

        # Check
        try:
            state = GameState()
            state.takeData(data)
        except Exception as ex:
            import traceback
            traceback.print_exc()
            raise ValueError(f"Error in file {fileName}")

        # Take data
        self.takeData(data)

    def save(self, fileName: str):
        # Build data
        data = self.gatherData()

        # Save
        logging.info(f"Save state to {fileName}...")
        ext = os.path.splitext(fileName)[1]
        if ext == ".json":
            import json
            with open(fileName, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        elif ext == ".pickle":
            import pickle
            with open(fileName, 'wb') as bfile:
                pickle.dump(data, bfile, protocol=4)
        elif ext == ".msgpack":
            import msgpack
            with open(fileName, 'wb') as bfile:
                msgpack.dump(data, bfile)
        else:
            raise ValueError(f"Invalid file extension {ext}")

    def gatherData(self) -> Dict[str, Any]:
        return {
            "currentPlayerId": self.__playerId,
            "players": [player.gatherData() for player in self.__players],
            "turn": self.__turn,
            "world": self.__world.gatherData()
        }

    def takeData(self, data: Dict[str, Any]):
        self.__playerId = int(data["currentPlayerId"])
        self.__players = [Player(playerData) for playerData in data["players"]]
        self.__turn = int(data["turn"])
        self.__world = World((1, 1))
        self.__world.takeData(data["world"])

    # GameState listener

    def notifyTurnChanged(self):
        for listener in self.listeners:
            listener.turnChanged(self)

    def notifyResourcesChanged(self):
        for listener in self.listeners:
            listener.resourcesChanged(self)

    def notifyCityCellAssigned(self, cityCell: Tuple[int, int], cell: Tuple[int, int], mode: CellUsage):
        for listener in self.listeners:
            listener.cityCellAssigned(self, cityCell, cell, mode)

    def notifyCityCellUnassigned(self, cityCell: Tuple[int, int], cell: Tuple[int, int]):
        for listener in self.listeners:
            listener.cityCellUnassigned(self, cityCell, cell)

    def notifyUnitRecruited(self, cell: Tuple[int, int]):
        for listener in self.listeners:
            listener.unitRecuited(self, cell)

    def notifyUnitMoved(self, fromCell: Tuple[int, int], toCell: Tuple[int, int]):
        for listener in self.listeners:
            listener.unitMoved(self, fromCell, toCell)

    def notifyUnitChanged(self, cell: Tuple[int, int], unit: Unit):
        for listener in self.listeners:
            listener.unitChanged(self, cell, unit)

    def notifyUnitDamaged(self, cell: Tuple[int, int], damage: int):
        for listener in self.listeners:
            listener.unitDamaged(self, cell, damage)

    def notifyUnitDied(self, cell: Tuple[int, int]):
        for listener in self.listeners:
            listener.unitDied(self, cell)
