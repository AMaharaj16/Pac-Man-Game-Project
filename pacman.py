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
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self, window):
        window.blit(PACMAN_IMAGE, (self.x, self.y))
    def move(self, up, down, left, right):
        if up:
            self.y -= PACMAN_VEL
        elif down:
            self.y += PACMAN_VEL
        elif left:
            self.x -= PACMAN_VEL
        elif right:
            self.x += PACMAN_VEL    

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
    
    pacman = Pacman((WIDTH-TILE_SIZE+2.5) // 2, (HEIGHT-TILE_SIZE+2.5) // 2)
    
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        pacman.move(up=keys[pygame.K_UP], 
                    down=keys[pygame.K_DOWN], 
                    left=keys[pygame.K_LEFT], 
                    right=keys[pygame.K_RIGHT])

        draw(window, maze, pacman)
if __name__ == "__main__":
    main(WINDOW)