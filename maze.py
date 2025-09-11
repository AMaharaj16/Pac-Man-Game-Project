import pygame

TILE_SIZE = 30
MAZE_COLOUR = (0,0,255)

class Maze:
    def __init__(self, layout):
        self.layout = layout
    
    def is_wall(self, row, col):
        return self.layout[row][col] == 1
    
    def is_intersection(self, row, col):
        directions = 0
        for dr, dc in [(1,0), (0,1), (-1,0), (0,-1)]:
            nextRow = row + dr
            nextCol = col + dc
            if 0 <= nextRow < len(self.layout) and 0 <= nextCol < len(self.layout[0]) and not self.is_wall(nextRow, nextCol):
                directions += 1
        return directions > 2
    
    def draw(self, window):
        for r, row in enumerate(self.layout):
            for c, val in enumerate(row):
                x = c * TILE_SIZE
                y = r * TILE_SIZE
                if val == 1:
                    pygame.draw.rect(window, MAZE_COLOUR, (x, y, TILE_SIZE, TILE_SIZE))