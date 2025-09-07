import pygame
import random
from collections import deque
from random import shuffle

TILE_SIZE = 30
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
        self.vel = 2

    def draw(self, window):
        window.blit(GHOST_IMAGE, (self.x, self.y))
    
    def move(self, pacman, maze):
        if self.dir_x == 0 and self.dir_y == 0:
             self.move_anywhere(maze)
        elif self.chase:
            self.time += 1
            self.move_towards(maze, pacman.row, pacman.col)
            if self.time > self.chaseTime:
                self.chase = False
                self.vel = 2
        else:
            self.time = 0
            self.move_towards(maze, self.spawnRow, self.spawnCol)
            if self.row == self.spawnRow and self.col == self.spawnCol:
                self.chase = True
                self.chaseTime += 120 # Chasing again, add 2 seconds to chaseTime
                self.vel = random.randrange(0,4)
        
    def move_anywhere(self, maze):
        nextDirections = [(1,0), (-1,0), (0,1), (0,-1)]
        shuffle(nextDirections)
        for dr, dc in nextDirections:
            nr, nc = self.row + dr, self.col + dc
            if not maze.is_wall(nr, nc) and [nr, nc] != self.lastTile and 0 < nr < 20 and 0 < nc < 20:
                self.dir_x, self.dir_y = dc, dr
                self.decisionNeeded = False
                return
        
        self.lastTile = [self.row, self.col]
    
    def move_towards(self, maze, targetRow, targetCol):
        prevTile = [self.row, self.col]
        self.look_around()

        if self.decisionNeeded:
            self.make_decision(maze, targetRow, targetCol)
        
        if self.dir_x == 1:
                nextCol = (self.x + self.vel + TILE_SIZE - 1) // TILE_SIZE
                if not maze.is_wall(self.row, nextCol):
                    self.x += self.vel * self.dir_x
                else:
                    self.dir_x = 0
                    self.decisionNeeded = True
        elif self.dir_x == -1:
                nextCol = (self.x - self.vel) // TILE_SIZE
                if not maze.is_wall(self.row, nextCol):
                    self.x += self.vel * self.dir_x
                else:
                    self.dir_x = 0
                    self.decisionNeeded = True
        elif self.dir_y == 1:
                nextRow = (self.y + self.vel + TILE_SIZE - 1) // TILE_SIZE
                if not maze.is_wall(nextRow, self.col):
                    self.y += self.vel * self.dir_y
                else:
                    self.dir_y = 0
                    self.decisionNeeded = True
        elif self.dir_y == -1:
                nextRow = (self.y - self.vel) // TILE_SIZE
                if not maze.is_wall(nextRow, self.col):
                    self.y += self.vel * self.dir_y
                else:
                    self.dir_y = 0
                    self.decisionNeeded = True
        
        self.row = self.y // TILE_SIZE
        self.col = self.x // TILE_SIZE

        newTile = [self.row, self.col]
        
        if newTile != prevTile:
            self.lastTile = prevTile

    def make_decision(self, maze, targetRow, targetCol):
        path = self.bfs(maze, [targetRow, targetCol])

        if len(path) < 2:
            self.move_anywhere(maze)
            return  

        nextRow, nextCol = path[1]

        if nextRow > self.row and not maze.is_wall(nextRow, self.col) and nextRow < 20:
            self.dir_x = 0
            self.dir_y = 1
        elif nextRow < self.row and not maze.is_wall(nextRow, self.col) and nextRow > 0:
            self.dir_x = 0
            self.dir_y = -1
        elif nextCol > self.col and not maze.is_wall(self.row, nextCol) and nextCol < 20:
            self.dir_x = 1
            self.dir_y = 0
        elif not maze.is_wall(self.row, nextCol) and nextCol > 0:
            self.dir_x = -1
            self.dir_y = 0
        
        self.decisionNeeded = False

    def look_around(self):
        if self.dir_x == 0 and self.dir_y == 0:
            self.decisionNeeded = True
        elif self.dir_x != 0:
            self.y = self.row * TILE_SIZE
            if self.x % TILE_SIZE == 0:
                self.decisionNeeded = True
        elif self.dir_y != 0:
            self.x = self.col * TILE_SIZE
            if self.y % TILE_SIZE == 0:
                self.decisionNeeded = True
    
    def bfs(self, maze, target):
        rows = len(maze.layout)
        cols = len(maze.layout[0])
        start = (self.row, self.col)
        prevNode = dict() # (ChildRow, ChildCol): (ParentRow, ParentCol)
        visited = {start, tuple(self.lastTile)}

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





