import pygame

TILE_SIZE = 30
MAZE_COLOUR = (0,0,255)

class Maze:
    def __init__(self, layout):
        self.layout = layout
    
    def is_wall(self, row, col):
        return self.layout[row][col] == 1
    
    def draw(self, window):
        for r, row in enumerate(self.layout):
            for c, val in enumerate(row):
                x = c * TILE_SIZE
                y = r * TILE_SIZE
                if val == 1:
                    pygame.draw.rect(window, MAZE_COLOUR, (x, y, TILE_SIZE, TILE_SIZE))