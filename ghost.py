import pygame

TILE_SIZE = 60
GHOST_VEL = 3
GHOST_IMAGE_UNSCALED = pygame.image.load('pacman_ghost.png')
GHOST_IMAGE = pygame.transform.scale(GHOST_IMAGE_UNSCALED, (TILE_SIZE, TILE_SIZE))

class Ghost:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * TILE_SIZE
        self.y = row * TILE_SIZE
        self.dir_x = 0
        self.dir_y = 0
        self.decisionNeeded = False
        self.lastTile = None

    def draw(self, window):
        window.blit(GHOST_IMAGE, (self.x, self.y))
    
    def move(self, pacman, maze):
        
        prevTile = [self.row, self.col]
        self.look_around(maze)
        
        if self.decisionNeeded:
            self.make_decision(pacman, maze)
        
        if self.dir_x != 0:
                self.x += GHOST_VEL * self.dir_x
        elif self.dir_y != 0:
                self.y += GHOST_VEL * self.dir_y
    
        self.row = self.y // TILE_SIZE
        self.col = self.x // TILE_SIZE

        newTile = [self.row, self.col]
        
        if newTile != prevTile:
            self.lastTile = prevTile
    
    def look_around(self, maze):
        if self.dir_x == 0 and self.dir_y == 0:
            self.decisionNeeded = True
        elif self.dir_x != 0:
            self.y = self.row * TILE_SIZE
            if self.col == self.x / TILE_SIZE:
                self.decisionNeeded = True
        elif self.dir_y != 0:
            self.x = self.col * TILE_SIZE
            if self.row == self.y / TILE_SIZE:
                self.decisionNeeded = True

        
    def make_decision(self, pacman, maze):
        bestRoute = ""
        shortestDist = 10000
        if not maze.is_wall(self.row + 1, self.col) and self.lastTile != [self.row + 1, self.col]: # Tile Down
            shortestDist = abs((self.row + 1) - pacman.row) + abs(self.col - pacman.col)
            bestRoute = 'D'
        
        if not maze.is_wall(self.row - 1, self.col) and self.lastTile != [self.row - 1, self.col]: # Tile Up
            dist = abs((self.row - 1) - pacman.row) + abs(self.col - pacman.col)
            if dist < shortestDist:
                shortestDist = dist
                bestRoute = 'U'

        if not maze.is_wall(self.row, self.col + 1) and self.lastTile != [self.row, self.col + 1]: # Tile Right
            dist = abs(self.row - pacman.row) + abs((self.col + 1) - pacman.col)
            if dist < shortestDist:
                shortestDist = dist
                bestRoute = 'R'

        if not maze.is_wall(self.row, self.col - 1) and self.lastTile != [self.row, self.col - 1]: # Tile Left
            dist = abs(self.row - pacman.row) + abs((self.col - 1) - pacman.col)
            if dist < shortestDist:
                shortestDist = dist
                bestRoute = 'L'
        
        if bestRoute == 'D':
            self.dir_x = 0
            self.dir_y = 1
        elif bestRoute == 'U':
            self.dir_x = 0
            self.dir_y = -1
        elif bestRoute == 'R':
            self.dir_x = 1
            self.dir_y = 0
        elif bestRoute == 'L':
            self.dir_x = -1
            self.dir_y = 0

        self.decisionNeeded = False

