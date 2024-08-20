import pygame
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface
import sys

pygame.init()


bg = pygame.image.load('background.jpg')
window = pygame.display.set_mode((1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE)

renderWidth = bg.get_width()
renderHeight = bg.get_height()


# FPS = 60
# FramePerSec = pygame.time.Clock()
#
# # Predefined some colors
# BLUE = (0, 0, 255)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
#
# # Screen information
# SCREEN_WIDTH = 400
# SCREEN_HEIGHT = 600
#
# DISPLAY_SURF = pygame.display.set_mode((400, 600))
# DISPLAY_SURF.fill(WHITE)
# pygame.display.set_caption("Game")

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


# class Enemy(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = pygame.image.load("Enemy.png")
#         self.rect = self.image.get_rect()
#         self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
#
#     def move(self):
#         self.rect.move_ip(0, 10)
#         if self.rect.bottom > 600:
#             self.rect.top = 0
#             self.rect.center = (random.randint(30, 370), 0)
#
#     def draw(self, surface):
#         surface.blit(self.image, self.rect)
#
#
# class Player(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = pygame.image.load("Player.png")
#         self.rect = self.image.get_rect()
#         self.rect.center = (160, 520)
#
#     def update(self):
#         pressed_keys = pygame.key.get_pressed()
#         # if pressed_keys[K_UP]:
#         # self.rect.move_ip(0, -5)
#         # if pressed_keys[K_DOWN]:
#         # self.rect.move_ip(0,5)
#
#         if self.rect.left > 0:
#             if pressed_keys[K_LEFT]:
#                 self.rect.move_ip(-5, 0)
#         if self.rect.right < SCREEN_WIDTH:
#             if pressed_keys[K_RIGHT]:
#                 self.rect.move_ip(5, 0)
#
#     def draw(self, surface):
#         surface.blit(self.image, self.rect)
#
#
# P1 = Player()
# E1 = Enemy()
#
# while True:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#     P1.update()
#     E1.move()
#
#     DISPLAY_SURF.fill(WHITE)
#     P1.draw(DISPLAY_SURF)
#     E1.draw(DISPLAY_SURF)
#
#     pygame.display.update()
#     FramePerSec.tick(FPS)