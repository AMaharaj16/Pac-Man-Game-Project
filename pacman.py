import pygame
from maze import Maze
from pellets import Pellet
from ghost import Ghost

pygame.init()
pygame.display.set_caption("Pac-Man Game")
FPS = 60
FONT = pygame.font.SysFont('comicsans', 50, bold = True)
TILE_SIZE = 30
MAZE_HEIGHT = 21
MAZE_WIDTH = 21
HEIGHT = MAZE_HEIGHT * TILE_SIZE
WIDTH = MAZE_WIDTH * TILE_SIZE
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0,0,0)
MAZE_COLOUR = (0,0,255)
PACMAN_IMAGE_UNSCALED = pygame.image.load('pacman.png')
PACMAN_IMAGE = pygame.transform.scale(PACMAN_IMAGE_UNSCALED, (TILE_SIZE, TILE_SIZE))
PACMAN_VEL = 2
TOLERANCE = 25
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
        self.next_dir_x = 0
        self.next_dir_y = 0

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
            self.x += self.dir_x * PACMAN_VEL
            self.y += self.dir_y * PACMAN_VEL

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

        next_x = self.x + xdir * PACMAN_VEL
        next_y = self.y + ydir * PACMAN_VEL

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



def draw(window, maze, pacman, pellets, ghosts):
    window.fill(BLACK)
    maze.draw(window)
    pacman_center_x = pacman.x + TILE_SIZE / 2
    pacman_center_y = pacman.y + TILE_SIZE / 2
    for pellet in pellets:
            pellet.draw(window)
            if not pellet.eaten and abs(pacman_center_x - pellet.x) < TILE_SIZE/2 and abs(pacman_center_y - pellet.y) < TILE_SIZE/2:
                pellet.eaten = True
    pacman.draw(window)
    for ghost in ghosts:
        ghost.draw(window)
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

    maze = Maze([[1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1],
                 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                 [1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1],
                 [1,0,1,1,1,0,1,0,0,0,1,0,0,0,1,0,1,1,1,0,1],
                 [1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1],
                 [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                 [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1],
                 [0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0],
                 [1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1],
                 [1,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,1],
                 [1,0,1,0,1,0,1,0,1,0,2,0,1,0,1,0,1,0,1,0,1],
                 [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
                 [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
                 [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
                 [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1],
                 [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
                 [1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1],
                 [1,0,1,1,1,0,1,0,0,0,1,0,0,0,1,0,1,1,1,0,1],
                 [1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1],
                 [1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
                 [1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1]])
    
    pacman = Pacman(10, 10)

    pellets = initialize_pellets(maze)

    ghosts = [Ghost(1, 1, 1, 0, 0), Ghost(1, 19, 0, 1, 75), Ghost(19, 1, 0, -1, 150), Ghost(19, 19, -1, 0, 225)]
    
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
            pacman.next_dir_x = 0
            pacman.next_dir_y = -1
        elif keys[pygame.K_DOWN]:
            pacman.next_dir_x = 0
            pacman.next_dir_y = 1
        elif keys[pygame.K_LEFT]:
            pacman.next_dir_x = -1
            pacman.next_dir_y = 0
        elif keys[pygame.K_RIGHT]:
            pacman.next_dir_x = 1
            pacman.next_dir_y = 0

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

        for ghost in ghosts:
            ghost.move(pacman, maze)
            
            if abs(ghost.x - pacman.x) < 10 and abs(ghost.y - pacman.y) < 10:
                run = False

        draw(window, maze, pacman, pellets, ghosts)
if __name__ == "__main__":
    main(WINDOW)