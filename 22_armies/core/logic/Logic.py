from abc import ABCMeta
from typing import Dict

from .Command import Command
from .Rules import Rules
from ..state import World, GameState


class Logic:

    def __init__(self, state: GameState):
        self.__commands: Dict[int, Command] = {}
        self.__state = state
        self.__rules = Rules(self)

    @property
    def state(self) -> GameState:
        return self.__state

    @property
    def rules(self) -> Rules:
        return self.__rules

    @property
    def world(self) -> World:
        return self.__state.world

    def addCommand(self, command: Command):
        self.__commands[command.priority()] = command

    def executeCommands(self):
        commands = self.__commands.copy()
        self.__commands.clear()
        priorities = sorted(commands.keys())
        for priority in priorities:
            command = commands[priority]
            if not command.check(self):
                continue
            command.execute(self)

    def getSetLayerCellCommand(self, layer: str) -> ABCMeta:
        from core.logic.command.layer.SetGroundCell import SetGroundCell
        from core.logic.command.layer.SetImpassableCell import SetImpassableCell
        from core.logic.command.layer.SetObjectsCell import SetObjectsCell
        from core.logic.command.layer.SetUnitsCell import SetUnitsCell
        setLayerValueCommand = {
            "ground": SetGroundCell,
            "impassable": SetImpassableCell,
            "objects": SetObjectsCell,
            "units": SetUnitsCell,
        }
        return setLayerValueCommand[layer]

