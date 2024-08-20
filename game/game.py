from state import World
from state.constants import LAYER_GROUND_EARTH
from ui import UserInterface

# Create a basic game state
world = World(16, 10)
for y in range(3, 7):
    for x in range(4, 12):
        world.setValue(x, y, LAYER_GROUND_EARTH)

# Create a user interface and run it
userInterface = UserInterface(world)
userInterface.run()
userInterface.quit()

import pygame
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface

pygame.init()

# Load image and create window with default resolution
window = pygame.display.set_mode((1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("2D Medieval Strategy Game with Python, http://www.patternsgameprog.com")

# The size of our game scene is the one of the image
image = pygame.image.load("assets/image.png")
renderWidth = image.get_width()
renderHeight = image.get_height()

running = True
while running:

    # Handle input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break

    # Render scene in a surface
    renderSurface = Surface((renderWidth, renderHeight))
    renderSurface.blit(image, (0, 0))

    # Scale rendering to window size
    windowWidth, windowHeight = window.get_size()
    renderRatio = renderWidth / renderHeight
    windowRatio = windowWidth / windowHeight
    if windowRatio <= renderRatio:
        rescaledSurfaceWidth = windowWidth
        rescaledSurfaceHeight = int(windowWidth / renderRatio)
        rescaledSurfaceX = 0
        rescaledSurfaceY = (windowHeight - rescaledSurfaceHeight) // 2
    else:
        rescaledSurfaceWidth = int(windowHeight * renderRatio)
        rescaledSurfaceHeight = windowHeight
        rescaledSurfaceX = (windowWidth - rescaledSurfaceWidth) // 2
        rescaledSurfaceY = 0

    # Scale the rendering to the window/screen size
    rescaledSurface = pygame.transform.scale(
        renderSurface, (rescaledSurfaceWidth, rescaledSurfaceHeight)
    )
    window.blit(rescaledSurface, (rescaledSurfaceX, rescaledSurfaceY))
    pygame.display.update()

pygame.quit()