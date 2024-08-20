from core.state import World
from .GroundComponent import GroundComponent
from .ImpassableComponent import ImpassableComponent
from .LayerComponent import LayerComponent
from .ObjectsComponent import ObjectsComponent
from .UnitsComponent import UnitsComponent
from ...theme.Theme import Theme


class LayerComponentFactory:
    def __init__(self, theme: Theme, world: World):
        self.__name2layer = {
            "ground": lambda name: GroundComponent(theme, world),
            "impassable": lambda name: ImpassableComponent(theme, world),
            "objects": lambda name: ObjectsComponent(theme, world),
            "units": lambda name: UnitsComponent(theme, world),
        }

    def create(self, name: str) -> LayerComponent:
        if name not in self.__name2layer:
            raise ValueError(f"Invalid layer '{name}'")
        return self.__name2layer[name](name)
