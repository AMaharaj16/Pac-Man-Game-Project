import pygame

TILE_SIZE = 60
GHOST_VEL = 2
CHASE_TIME = 600
GHOST_IMAGE_UNSCALED = pygame.image.load('pacman_ghost.png')
GHOST_IMAGE = pygame.transform.scale(GHOST_IMAGE_UNSCALED, (TILE_SIZE, TILE_SIZE))

class Ghost:
    def __init__(self, row, col, chase, time):
        self.row = row
        self.col = col
        self.spawnRow = row
        self.spawnCol = col
        self.x = col * TILE_SIZE
        self.y = row * TILE_SIZE
        self.dir_x = 0
        self.dir_y = 0
        self.decisionNeeded = False
        self.lastTile = None
        self.chase = chase
        self.time = time

    def draw(self, window):
        window.blit(GHOST_IMAGE, (self.x, self.y))
    
    def move(self, pacman, maze):
        if self.chase:
            self.move_chase(pacman, maze)
        else:
            self.move_scatter(maze)
    
    def move_chase(self, pacman, maze):

        prevTile = [self.row, self.col]
        self.look_around()
        self.time += 1
        
        if self.decisionNeeded:
            self.make_decision_chase(pacman, maze)
        
        if self.dir_x != 0:
                self.x += GHOST_VEL * self.dir_x
        elif self.dir_y != 0:
                self.y += GHOST_VEL * self.dir_y
    
        self.row = self.y // TILE_SIZE
        self.col = self.x // TILE_SIZE

        newTile = [self.row, self.col]
        
        if newTile != prevTile:
            self.lastTile = prevTile
        
        if self.time > CHASE_TIME:
            self.chase = False
    
    def make_decision_chase(self, pacman, maze):
        bestRoute = ""
        shortestDist = 10000
        if not maze.is_wall(self.row + 1, self.col) and self.lastTile != [self.row + 1, self.col] and self.row < 11: # Tile Down
            shortestDist = abs((self.row + 1) - pacman.row) + abs(self.col - pacman.col)
            bestRoute = 'D'
        
        if not maze.is_wall(self.row - 1, self.col) and self.lastTile != [self.row - 1, self.col] and self.row > 1: # Tile Up
            dist = abs((self.row - 1) - pacman.row) + abs(self.col - pacman.col)
            if dist < shortestDist:
                shortestDist = dist
                bestRoute = 'U'

        if not maze.is_wall(self.row, self.col + 1) and self.lastTile != [self.row, self.col + 1] and self.col < 11: # Tile Right
            dist = abs(self.row - pacman.row) + abs((self.col + 1) - pacman.col)
            if dist < shortestDist:
                shortestDist = dist
                bestRoute = 'R'

        if not maze.is_wall(self.row, self.col - 1) and self.lastTile != [self.row, self.col - 1] and self.col > 1: # Tile Left
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



    def move_scatter(self, maze):
        self.time = 0
        prevTile = [self.row, self.col]
        self.look_around()
        
        if self.decisionNeeded:
            self.make_decision_scatter(maze)
        
        if self.dir_x != 0:
                self.x += GHOST_VEL * self.dir_x
        elif self.dir_y != 0:
                self.y += GHOST_VEL * self.dir_y
    
        self.row = self.y // TILE_SIZE
        self.col = self.x // TILE_SIZE

        newTile = [self.row, self.col]
        
        if newTile != prevTile:
            self.lastTile = prevTile
        
        if self.row == self.spawnRow and self.col == self.spawnCol:
            self.chase = True
        
    def make_decision_scatter(self, maze):
        bestRoute = ""
        shortestDist = 10000
        if not maze.is_wall(self.row + 1, self.col) and self.lastTile != [self.row + 1, self.col] and self.row < 11: # Tile Down
            shortestDist = abs((self.row + 1) - self.spawnRow) + abs(self.col - self.spawnCol)
            bestRoute = 'D'
        
        if not maze.is_wall(self.row - 1, self.col) and self.lastTile != [self.row - 1, self.col] and self.row > 1: # Tile Up
            dist = abs((self.row - 1) - self.spawnRow) + abs(self.col - self.spawnCol)
            if dist < shortestDist:
                shortestDist = dist
                bestRoute = 'U'

        if not maze.is_wall(self.row, self.col + 1) and self.lastTile != [self.row, self.col + 1] and self.col < 11: # Tile Right
            dist = abs(self.row - self.spawnRow) + abs((self.col + 1) - self.spawnCol)
            if dist < shortestDist:
                shortestDist = dist
                bestRoute = 'R'

        if not maze.is_wall(self.row, self.col - 1) and self.lastTile != [self.row, self.col - 1] and self.col > 1: # Tile Left
            dist = abs(self.row - self.spawnRow) + abs((self.col - 1) - self.spawnCol)
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

         

    def look_around(self):
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