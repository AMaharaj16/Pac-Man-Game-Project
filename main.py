import pygame
from maze import Maze
from pellets import Pellet
from ghost import Ghost
from pacman import Pacman

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
PELLET_RADIUS = 3
PACMAN_VEL = 2

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
    
    pacman = Pacman(10, 10, PACMAN_VEL)

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