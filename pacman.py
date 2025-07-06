import pygame
from maze import Maze
from pellets import Pellet

pygame.init()
pygame.display.set_caption("Pac-Man Game")
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
PACMAN_IMAGE = pygame.transform.scale(PACMAN_IMAGE_UNSCALED, (TILE_SIZE, TILE_SIZE))
PACMAN_VEL = 3
TOLERANCE = 20
PELLET_RADIUS = 3


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

        if self.dir_y == 1:
            self.direction = 'down'
            row = (self.y + TILE_SIZE) // TILE_SIZE
            col_left = (self.x + TOLERANCE) // TILE_SIZE
            col_right = (self.x + TILE_SIZE - TOLERANCE) // TILE_SIZE
            if not maze.is_wall(row, col_left) and not maze.is_wall(row, col_right):
                self.y += PACMAN_VEL
        elif self.dir_y == -1:
            self.direction = 'up'
            row = self.y // TILE_SIZE
            col_left = (self.x + TOLERANCE) // TILE_SIZE
            col_right = (self.x + TILE_SIZE - TOLERANCE) // TILE_SIZE
            if not maze.is_wall(row, col_left) and not maze.is_wall(row, col_right):
                self.y -= PACMAN_VEL
        elif self.dir_x == 1:
            self.direction = 'right'
            col = (self.x + TILE_SIZE) // TILE_SIZE
            row_top = (self.y + TOLERANCE) // TILE_SIZE
            row_bottom = (self.y + TILE_SIZE - TOLERANCE) // TILE_SIZE
            if not maze.is_wall(row_top, col) and not maze.is_wall(row_bottom, col):
                self.x += PACMAN_VEL
        elif self.dir_x == -1:
            self.direction = 'left'
            col = self.x // TILE_SIZE
            row_top = (self.y + TOLERANCE) // TILE_SIZE
            row_bottom = (self.y + TILE_SIZE - TOLERANCE) // TILE_SIZE
            if not maze.is_wall(row_top, col) and not maze.is_wall(row_bottom, col):
                self.x -= PACMAN_VEL
        
        self.row = self.y // TILE_SIZE
        self.col = self.x // TILE_SIZE



def draw(window, maze, pacman, pellets):
    window.fill(BLACK)
    maze.draw(window)
    pacman_center_x = pacman.x + TILE_SIZE / 2
    pacman_center_y = pacman.y + TILE_SIZE / 2
    for pellet in pellets:
            pellet.draw(window)
            if not pellet.eaten and abs(pacman_center_x - pellet.x) < TILE_SIZE/2 and abs(pacman_center_y - pellet.y) < TILE_SIZE/2:
                pellet.eaten = True
    pacman.draw(window)
    pygame.display.update()

def initialize_pellets(maze):
    result = []
    for i in range(MAZE_HEIGHT):
        for j in range(MAZE_WIDTH):
            if maze.layout[i][j] == 0:
                result.append(Pellet(i,j))
    return result

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

    pellets = initialize_pellets(maze)
    
    while run:
        clock.tick(FPS)

        run = False
        for pellet in pellets:
            if pellet.eaten == False:
                run = True
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

        try:
            pacman.move(maze)
        except IndexError:
            if pacman.dir_x == 1:
                pacman.x += PACMAN_VEL
                if pacman.x >= WIDTH:
                    pacman.x = -TILE_SIZE
            if pacman.dir_y == 1:
                pacman.y += PACMAN_VEL
                if pacman.y >= HEIGHT:
                    pacman.y = -TILE_SIZE
        
        
        if pacman.dir_x == -1 and pacman.x <= -TILE_SIZE:
            pacman.x = WIDTH - 1
        if pacman.dir_y == -1 and pacman.y <= -TILE_SIZE:
            pacman.y = WIDTH - 1

        draw(window, maze, pacman, pellets)
if __name__ == "__main__":
    main(WINDOW)