import pygame
from collections import deque

TILE_SIZE = 30
GHOST_VEL = 2
GHOST_IMAGE_UNSCALED = pygame.image.load('pacman_ghost.png')
GHOST_IMAGE = pygame.transform.scale(GHOST_IMAGE_UNSCALED, (TILE_SIZE, TILE_SIZE))

class Ghost:
    def __init__(self, row, col, dir_x, dir_y, chase, time):
        self.row = row
        self.col = col
        self.spawnRow = row
        self.spawnCol = col
        self.x = col * TILE_SIZE
        self.y = row * TILE_SIZE
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.decisionNeeded = False
        self.lastTile = [row, col]
        self.chase = chase
        self.time = time
        self.chaseTime = 300 # Starts chasing time at 5 seconds

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
            self.make_decision(maze, pacman.row, pacman.col)
        
        if self.dir_x == 1:
                nextCol = (self.x + GHOST_VEL + TILE_SIZE - 1) // TILE_SIZE
                if not maze.is_wall(self.row, nextCol):
                    self.x += GHOST_VEL * self.dir_x
                else:
                    self.decisionNeeded = True
        elif self.dir_x == -1:
                nextCol = (self.x - GHOST_VEL) // TILE_SIZE
                if not maze.is_wall(self.row, nextCol):
                    self.x += GHOST_VEL * self.dir_x
                else:
                    self.decisionNeeded = True
        elif self.dir_y == 1:
                nextRow = (self.y + GHOST_VEL + TILE_SIZE - 1) // TILE_SIZE
                if not maze.is_wall(nextRow, self.col):
                    self.y += GHOST_VEL * self.dir_y
                else:
                    self.decisionNeeded = True
        elif self.dir_y == -1:
                nextRow = (self.y - GHOST_VEL) // TILE_SIZE
                if not maze.is_wall(nextRow, self.col):
                    self.y += GHOST_VEL * self.dir_y
                else:
                    self.decisionNeeded = True
    
        self.row = self.y // TILE_SIZE
        self.col = self.x // TILE_SIZE

        newTile = [self.row, self.col]
        
        if newTile != prevTile:
            self.lastTile = prevTile
        
        if self.time > self.chaseTime:
            self.chase = False

    def move_scatter(self, maze):
        self.time = 0
        prevTile = [self.row, self.col]
        self.look_around()
        
        if self.decisionNeeded:
            self.make_decision_scatter(maze, self.spawnRow, self.spawnCol)
        
        if self.dir_x == 1:
                nextCol = (self.x + GHOST_VEL + TILE_SIZE - 1) // TILE_SIZE
                if not maze.is_wall(self.row, nextCol):
                    self.x += GHOST_VEL * self.dir_x
                else:
                    self.decisionNeeded = True
        elif self.dir_x == -1:
                nextCol = (self.x - GHOST_VEL) // TILE_SIZE
                if not maze.is_wall(self.row, nextCol):
                    self.x += GHOST_VEL * self.dir_x
                else:
                    self.decisionNeeded = True
        elif self.dir_y == 1:
                nextRow = (self.y + GHOST_VEL + TILE_SIZE - 1) // TILE_SIZE
                if not maze.is_wall(nextRow, self.col):
                    self.y += GHOST_VEL * self.dir_y
                else:
                    self.decisionNeeded = True
        elif self.dir_y == -1:
                nextRow = (self.y - GHOST_VEL) // TILE_SIZE
                if not maze.is_wall(nextRow, self.col):
                    self.y += GHOST_VEL * self.dir_y
                else:
                    self.decisionNeeded = True
    
        self.row = self.y // TILE_SIZE
        self.col = self.x // TILE_SIZE

        newTile = [self.row, self.col]
        
        if newTile != prevTile:
            self.lastTile = prevTile
        
        if self.row == self.spawnRow and self.col == self.spawnCol:
            self.chase = True
            self.chaseTime += 120 # Chasing again, add 2 seconds to chaseTime
    
    def make_decision(self, maze, targetRow, targetCol):
        path = self.bfs(maze, [targetRow, targetCol])

        if len(path) < 2:
            return  

        nextRow, nextCol = path[1]

        if nextRow > self.row and not maze.is_wall(nextRow, self.col) and nextRow < 20:
            self.dir_x = 0
            self.dir_y = 1
        elif nextRow < self.row and not maze.is_wall(nextRow, self.col) and nextRow > 1:
            self.dir_x = 0
            self.dir_y = -1
        elif nextCol > self.col and not maze.is_wall(self.row, nextCol) and nextCol < 20:
            self.dir_x = 1
            self.dir_y = 0
        elif not maze.is_wall(self.row, nextCol) and nextCol > 1:
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
    
    def bfs(self, maze, target):
        rows = len(maze.layout)
        cols = len(maze.layout[0])
        start = (self.row, self.col)
        prevNode = dict() # (ChildRow, ChildCol): (ParentRow, ParentCol)
        visited = set()
        visited.add(start)
        visited.add(tuple(self.lastTile))

        queue = deque([start])

        while queue:
            r, c = queue.popleft() # Current position in tree

            if (r,c) == (target[0], target[1]):
                path = []
                while (r,c) != start:
                    path.append((r,c)) # Starting from Pac-Man's location, return tiles all the way to start
                    r,c = prevNode[(r,c)]
                path.append(start)
                return path[::-1] # Reverse path so it gives path to Pac-Man, not from

            for dr, dc in [(1,0), (0,1), (-1,0), (0,-1)]: # Check all 4 directions
                rNext = r + dr
                cNext = c + dc

                if 0 <= rNext < rows and 0 <= cNext < cols and maze.layout[rNext][cNext] == 0 and (rNext, cNext) not in visited:
                    prevNode[(rNext, cNext)] = (r, c)
                    queue.append((rNext,cNext))
                    visited.add((rNext,cNext))
        return []





