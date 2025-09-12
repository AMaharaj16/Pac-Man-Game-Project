import pygame

pygame.init()
pygame.display.set_caption("Pac-Man Game")

TILE_SIZE = 30
TOLERANCE = 25
PACMAN_IMAGE_UNSCALED = pygame.image.load('pacman.png')
PACMAN_IMAGE = pygame.transform.scale(PACMAN_IMAGE_UNSCALED, (TILE_SIZE, TILE_SIZE))

class Pacman:
    def __init__(self, row, col, vel):
        self.row = row
        self.col = col
        self.y = row * TILE_SIZE
        self.x = col * TILE_SIZE
        self.direction = 'right'
        self.dir_x = 0
        self.dir_y = 0
        self.next_dir_x = 0
        self.next_dir_y = 0
        self.vel = vel

    def draw(self, window):
        if self.direction == 'right':
            window.blit(PACMAN_IMAGE, (self.x, self.y))
        elif self.direction == 'up':
            window.blit(pygame.transform.rotate(PACMAN_IMAGE, 90), (self.x, self.y))
        elif self.direction == 'left':
            window.blit(pygame.transform.rotate(PACMAN_IMAGE, 180), (self.x, self.y))
        elif self.direction == 'down':
            window.blit(pygame.transform.rotate(PACMAN_IMAGE, 270), (self.x, self.y))

    def move(self, maze):
        # If moving left or right, snap to y-coord of tile.
        if self.dir_x != 0:
            target_y = round(self.y / TILE_SIZE) * TILE_SIZE
            if abs(self.y - target_y) <= TOLERANCE:
                self.y = target_y
        
        # If moving up or down, snap to x-coord of tile.
        if self.dir_y != 0:
            target_x = round(self.x / TILE_SIZE) * TILE_SIZE
            if abs(self.x - target_x) <= TOLERANCE:
                self.x = target_x

        if self.can_move(maze, self.next_dir_x, self.next_dir_y):
            self.dir_x = self.next_dir_x
            self.dir_y = self.next_dir_y

        self.next_dir_x = 0
        self.next_dir_y = 0

        if self.can_move(maze, self.dir_x, self.dir_y):
            self.x += self.dir_x * self.vel
            self.y += self.dir_y * self.vel

            if self.dir_x == 1:
                self.direction = 'right'
            elif self.dir_x == -1:
                self.direction = 'left'
            elif self.dir_y == 1:
                self.direction = 'down'
            elif self.dir_y == -1:
                self.direction = 'up'
        
        self.row = self.y // TILE_SIZE
        self.col = self.x // TILE_SIZE

    def can_move(self, maze, xdir, ydir):
        # Return whether pacman can move in the given direction

        next_x = self.x + xdir * self.vel
        next_y = self.y + ydir * self.vel

        if ydir == 1:
            row = (next_y + TILE_SIZE) // TILE_SIZE
            col_left = (next_x + TOLERANCE) // TILE_SIZE
            col_right = (next_x + TILE_SIZE - TOLERANCE) // TILE_SIZE
            return not maze.is_wall(row, col_left) and not maze.is_wall(row, col_right)

        elif ydir == -1:
            row = next_y // TILE_SIZE
            col_left = (next_x + TOLERANCE) // TILE_SIZE
            col_right = (next_x + TILE_SIZE - TOLERANCE) // TILE_SIZE
            return not maze.is_wall(row, col_left) and not maze.is_wall(row, col_right)

        elif xdir == 1:
            col = (next_x + TILE_SIZE) // TILE_SIZE
            row_top = (next_y + TOLERANCE) // TILE_SIZE
            row_bottom = (next_y + TILE_SIZE - TOLERANCE) // TILE_SIZE
            return not maze.is_wall(row_top, col) and not maze.is_wall(row_bottom, col)

        elif xdir == -1:
            col = next_x // TILE_SIZE
            row_top = (next_y + TOLERANCE) // TILE_SIZE
            row_bottom = (next_y + TILE_SIZE - TOLERANCE) // TILE_SIZE
            return not maze.is_wall(row_top, col) and not maze.is_wall(row_bottom, col)
        
        return False
    
    # Will look at max 5 tiles ahead of pacman, ghosts will chase there instead.
    def chase_tile_ahead(self, maze):
        targetRow = self.row
        targetCol = self.col

        for _ in range(5):
            nextRow = targetRow + self.dir_y
            nextCol = targetCol + self.dir_x

            if not (0 <= nextRow < len(maze.layout) and 0 <= nextCol < len(maze.layout[0])):
                break

            if maze.is_wall(nextRow, nextCol):
                break

            targetRow = nextRow
            targetCol = nextCol

            if maze.is_intersection(nextRow, nextCol):
                break

        return targetRow, targetCol