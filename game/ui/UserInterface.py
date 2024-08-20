import pygame
from pygame import Surface
from state import World
from state.constants import LAYER_GROUND_EARTH, LAYER_GROUND_SEA

class UserInterface:
    def __init__(self, world: World):

        self.__world = world

        pygame.init()
        self.__window = pygame.display.set_mode((1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption("2D Medieval Strategy Game with Python, http://www.patternsgameprog.com")
        pygame.display.set_icon(pygame.image.load("assets/toen/icon.png"))

        self.__tileset = pygame.image.load("assets/toen/ground.png")
        self.__tileWidth = 16
        self.__tileHeight = 16
        self.__tiles = {
            LAYER_GROUND_EARTH: (2, 7),
            LAYER_GROUND_SEA: (5, 7),
        }
        self.__clock = pygame.time.Clock()
    
    def run(self):
        running = True
        while running:
            # Handle input
            ...

            # Render world on a surface
            tileWidth = self.__tileWidth
            tileHeight = self.__tileHeight
            renderWidth = self.__world.width * tileWidth
            renderHeight = self.__world.height * tileHeight
            renderSurface = Surface((renderWidth, renderHeight))
            for y in range(self.__world.height):
                for x in range(self.__world.width):
                    value = self.__world.getValue(x, y)
                    tile = self.__tiles[value]
                    tileRect = Rect(
                        tile[0] * tileWidth, tile[1] * tileHeight,
                        tileWidth, tileHeight
                    )
                    tileCoords = (x * tileWidth, y * tileHeight)
                    renderSurface.blit(self.__tileset, tileCoords, tileRect)

            # Scale rendering to window size
            ...
