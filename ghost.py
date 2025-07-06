import pygame

TILE_SIZE = 60
GHOST_IMAGE_UNSCALED = pygame.image.load('pacman_ghost.png')
GHOST_IMAGE = pygame.transform.scale(GHOST_IMAGE_UNSCALED, (TILE_SIZE, TILE_SIZE))

class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.row = y // TILE_SIZE
        self.col = x // TILE_SIZE

    def draw(self, window):
        window.blit(GHOST_IMAGE, (self.x, self.y))