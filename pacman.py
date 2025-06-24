import pygame

pygame.init()
pygame.display.set_caption("2048")
FPS = 60
FONT = pygame.font.SysFont('comicsans', 50, bold = True)
TILE_SIZE = 60
MAZE_HEIGHT = 12
MAZE_WIDTH = 12
HEIGHT = (MAZE_HEIGHT+1) * TILE_SIZE
WIDTH = (MAZE_WIDTH+1) * TILE_SIZE
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
COLOUR = (0,0,0)

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
                    pygame.draw.rect(window, (0, 0, 255), (x, y, TILE_SIZE, TILE_SIZE))

def draw(window, maze):
    maze.draw(window)
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
        [1,0,1,0,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,1,0,1],
        [0,0,0,0,1,1,0,1,1,0,0,0,0],
        [1,0,1,0,0,1,0,1,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,0,1,1,1,0,1,1,1,1]
        ])
    
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        draw(window, maze)
if __name__ == "__main__":
    main(WINDOW)