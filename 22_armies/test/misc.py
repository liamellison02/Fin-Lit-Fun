import pygame
from pygame.surface import Surface


def compareSurfaces(surface1: Surface, surface2: Surface) -> bool:
    assert isinstance(surface1, Surface)
    assert isinstance(surface2, Surface)
    if surface1.get_size() != surface2.get_size():
        return False
    array1 = pygame.surfarray.pixels_red(surface1)
    array2 = pygame.surfarray.pixels_red(surface2)
    if (array1 != array2).any():
        return False
    array1 = pygame.surfarray.pixels_green(surface1)
    array2 = pygame.surfarray.pixels_green(surface2)
    if (array1 != array2).any():
        return False
    array1 = pygame.surfarray.pixels_blue(surface1)
    array2 = pygame.surfarray.pixels_blue(surface2)
    if (array1 != array2).any():
        return False
    return True
