import pygame
import math

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

class Maze:
    def __init__(self, layout):
        self.layout = layout
    
    def is_wall(self, row, col):
        return self.layout[row][col] == 1
    
    def draw(self, window, pellets):
        pellets = []
        for r, row in enumerate(self.layout):
            for c, val in enumerate(row):
                x = c * TILE_SIZE
                y = r * TILE_SIZE
                if val == 1:
                    pygame.draw.rect(window, MAZE_COLOUR, (x, y, TILE_SIZE, TILE_SIZE))
                elif val == 0:
                    newPellet = Pellet(r,c)
                    pellets.append(newPellet)
                    newPellet.draw(window)

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



class Pellet:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.y = row * TILE_SIZE + TILE_SIZE / 2
        self.x = col * TILE_SIZE + TILE_SIZE / 2
        self.eaten = False
    def draw(self, window):
        if not self.eaten:
            pygame.draw.circle(window, (255, 255, 0), (self.x, self.y), PELLET_RADIUS)
        
    
def draw(window, maze, pacman, pellets):
    window.fill(BLACK)
    maze.draw(window, pellets)
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

    pellets = []
    
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
        pacman.move(maze)

        for pellet in pellets:
            if abs(pacman.x - pellet.x) < TILE_SIZE/2 and abs(pacman.y - pellet.y) < TILE_SIZE/2:
                pellet.eaten = True
                row = pacman.y // TILE_SIZE
                col = pacman.x // TILE_SIZE
                maze[row][col] = 2


        draw(window, maze, pacman, pellets)
if __name__ == "__main__":
    main(WINDOW)