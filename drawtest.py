import pygame
import pygame.locals as locals


def eventListener():
    for event in pygame.event.get():
        if event.type == locals.QUIT:
            exit()


SURFACE_WIDTH = 800
SURFACE_HEIGHT = 600
surface = pygame.display.set_mode((SURFACE_WIDTH * 2, SURFACE_HEIGHT * 2))
img = pygame.image.load("./background.png")
while True:
    eventListener()
    surface.blit(img, (0, 0))
    surface.blit(img, (800-100, 0))
    pygame.display.update()
