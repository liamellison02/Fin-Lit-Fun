import pygame
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface


bg = pygame.image.load('assets/image.png')
window = pygame.display.set_mode((1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE)

renderWidth = bg.get_width()
renderHeight = bg.get_height()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break

    renderSurface = Surface((renderWidth, renderHeight))
    renderSurface.blit(bg, (0, 0))

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