from typing import Tuple, Dict, Union, cast

import numpy as np
import pygame
from pygame import Surface

from core.constants import Resource, ItemProperty
from core.state import World, Item, Unit, Army
from tools.vector import vectorMulI, vectorSubHalfI, vectorSubI, vectorClampI
from ui.theme import Theme


def centerCellView(theme: Theme, world: World, cell: Tuple[int, int]) -> Tuple[int, int]:
    """
    Compute the top left world coordinates such as the cell is centered on screen.
    """
    tileSize = theme.defaulTileSize
    # Convert cell coordinates into pixel coordinates
    view = vectorMulI(cell, tileSize)
    # Center so the cursor in the middle of the view
    view = vectorSubHalfI(view, theme.viewSize)
    worldSize = vectorMulI(world.size, tileSize)
    maxView = vectorSubI(worldSize, theme.viewSize)
    return vectorClampI(view, 0, maxView)


def formatResourceBalance(resource: Resource, resources: Dict[Resource, int], negate: bool = False) -> str:
    if resource not in resources:
        return "0"
    count = resources[resource]
    if negate:
        count = -count
    if count > 0:
        return f"+{count}"
    else:
        return f"{count}"


resource2tag = {
    Resource.FOOD: "<food>",
    Resource.WOOD: "<wood>",
    Resource.STONE: "<stone>",
    Resource.GOLD: "<gold>",
}


def formatResourceCost(cost: Dict[Resource, int], negative: bool = False) -> str:
    out = ""
    for resource, count in cost.items():
        if out:
            out += "<space>"
        if negative:
            out += f"{-count}{resource2tag[resource]}"
        else:
            out += f"{count}{resource2tag[resource]}"
    return out


def graySurface(surface: Surface):
    colorkey = surface.get_colorkey()
    array = pygame.surfarray.array3d(surface)
    mean = array.mean(axis=2)
    mean = np.expand_dims(mean, axis=2)
    gray = mean.repeat(3, axis=2)
    surface = pygame.surfarray.make_surface(gray).convert()
    surface.set_colorkey(colorkey)
    return surface


def buildUnitTooltip(unitOrCell: Unit|Army) -> str:
    if isinstance(unitOrCell, Unit):
        unit = cast(Unit, unitOrCell)
        unitTooltip = f'<flag player="{unit.playerId}">{unit.unitClass.formatName()}<br>'
        if unit.hasProperty(ItemProperty.LIFE_POINTS) \
                and unit.hasProperty(ItemProperty.MAX_LIFE_POINTS):
            value = unit.getProperty(ItemProperty.LIFE_POINTS)
            maxValue = unit.getProperty(ItemProperty.MAX_LIFE_POINTS)
            unitTooltip += f"{value}/{maxValue}<life><space>"
        if unit.hasProperty(ItemProperty.MOVE_POINTS) \
                and unit.hasProperty(ItemProperty.MAX_MOVE_POINTS):
            value = unit.getProperty(ItemProperty.MOVE_POINTS)
            maxValue = unit.getProperty(ItemProperty.MAX_MOVE_POINTS)
            unitTooltip += f"{value}/{maxValue}<move><space>"
        unitTooltip += '<br>'
        return unitTooltip
    elif isinstance(unitOrCell, Army):
        army = cast(Army, unitOrCell)
        unitTooltip = f'<flag player="{army.playerId}">Army<br>'
        for unit in army.units:
            if unit.hasProperty(ItemProperty.LIFE_POINTS) \
                    and unit.hasProperty(ItemProperty.MAX_LIFE_POINTS):
                value = unit.getProperty(ItemProperty.LIFE_POINTS)
                maxValue = unit.getProperty(ItemProperty.MAX_LIFE_POINTS)
                unitTooltip += f"{value}/{maxValue}<life><space>"
            if unit.hasProperty(ItemProperty.MOVE_POINTS) \
                    and unit.hasProperty(ItemProperty.MAX_MOVE_POINTS):
                value = unit.getProperty(ItemProperty.MOVE_POINTS)
                maxValue = unit.getProperty(ItemProperty.MAX_MOVE_POINTS)
                unitTooltip += f"{value}/{maxValue}<move><space>"
            unitTooltip += f'{unit.unitClass.formatName()}<br>'
        return unitTooltip
    else:
        return ""
