import pygame
PELLET_RADIUS = 3
TILE_SIZE = 30

class Pellet:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.y = row * TILE_SIZE + TILE_SIZE / 2
        self.x = col * TILE_SIZE + TILE_SIZE / 2
        self.eaten = False
    def draw(self, window):
        if not self.eaten:
            pygame.draw.circle(window, (255, 255, 0), (self.x, self.y), PELLET_RADIUS)