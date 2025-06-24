import pygame
import math

pygame.init()
pygame.display.set_caption("2048")
FPS = 60
FONT = pygame.font.SysFont('comicsans', 50, bold = True)
TILE_SIZE = 60
MAZE_HEIGHT = 13
MAZE_WIDTH = 13
HEIGHT = MAZE_HEIGHT * TILE_SIZE
WIDTH = MAZE_WIDTH * TILE_SIZE
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0,0,0)
MAZE_COLOUR = (0,0,255)
PACMAN_IMAGE_UNSCALED = pygame.image.load('pacman.png')
PACMAN_IMAGE = pygame.transform.scale(PACMAN_IMAGE_UNSCALED, (TILE_SIZE-5, TILE_SIZE-5))
PACMAN_VEL = 3

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

class Pacman:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.y = row * TILE_SIZE
        self.x = col * TILE_SIZE
        self.direction = 'right'
        self.dir_x = 0
        self.dir_y = 0
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
        if self.dir_y == 1:
            self.direction = 'down'
        elif self.dir_y == -1:
            self.direction = 'up'
        elif self.dir_x == 1:
            self.direction = 'right'
        elif self.dir_x == -1:
            self.direction = 'left'
        
        next_x = self.x + self.dir_x * PACMAN_VEL
        next_y = self.y + self.dir_y * PACMAN_VEL

        tile_col = next_x // TILE_SIZE
        tile_row = next_y // TILE_SIZE

        if not maze.is_wall(tile_row, tile_col):
            self.x = next_x
            self.y = next_y

def draw(window, maze, pacman):
    window.fill(BLACK)
    maze.draw(window)
    pacman.draw(window)
    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()
    run = True
    maze = Maze([
        [1,1,1,1,0,1,1,1,0,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,1,0,1,0,0,1,0,1],
        [0,0,0,0,1,1,0,1,1,0,0,0,0],
        [1,0,1,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,2,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,1,0,1],
        [0,0,0,0,1,1,0,1,1,0,0,0,0],
        [1,0,1,0,0,1,0,1,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,0,1,1,1,0,1,1,1,1]
        ])
    
    pacman = Pacman(6, 6)
    
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pacman.dir_x = 0
            pacman.dir_y = -1
        elif keys[pygame.K_DOWN]:
            pacman.dir_x = 0
            pacman.dir_y = 1
        elif keys[pygame.K_LEFT]:
            pacman.dir_x = -1
            pacman.dir_y = 0
        elif keys[pygame.K_RIGHT]:
            pacman.dir_x = 1
            pacman.dir_y = 0
        else:
            pacman.dir_x = 0
            pacman.dir_y = 0
        pacman.move(maze)

        draw(window, maze, pacman)
if __name__ == "__main__":
    main(WINDOW)