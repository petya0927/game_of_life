import pygame
from pygame.locals import MOUSEBUTTONUP

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
BLOCK_SIZE = 20

def draw_units():
    global alive_cells
    for cell in alive_cells:
        if cell[0] >= 0 and cell[1] >= 0 and cell[0] <= WINDOW_WIDTH // BLOCK_SIZE and cell[1] <= WINDOW_HEIGHT // BLOCK_SIZE:
            rect = pygame.Rect(cell[0] * BLOCK_SIZE, cell[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, (0, 0, 0), rect)

def draw_grid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            # rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            # pygame.draw.rect(screen, (255, 255, 255), rect)
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, (100, 100, 100), rect, 1)

def edit_unit(mouse_x, mouse_y):
    global alive_cells
    cell = (mouse_x // BLOCK_SIZE, mouse_y // BLOCK_SIZE)
    if not cell in alive_cells:
        alive_cells.append(cell)
    else:
        alive_cells.remove(cell)

def neighbours_coords(x, y):
    return [
        (x-1, y-1), (x, y-1), (x+1, y-1),
        (x-1, y), (x+1, y),
        (x-1, y+1), (x, y+1), (x+1, y+1)
    ]

def neighbours_count(x, y):
    global alive_cells
    count = 0
    for cell in neighbours_coords(x, y):
        if cell in alive_cells:
            count += 1
    return count

def check_neighbours(x, y, next_alive):
    global alive_cells
    for cell in neighbours_coords(x, y):
        if cell not in alive_cells and neighbours_count(cell[0], cell[1]) == 3 and cell not in next_alive:
            next_alive.append(cell)

def compute_new_step():
    global alive_cells
    next_alive = []
    for cell in alive_cells:
        check_neighbours(cell[0], cell[1], next_alive)
        if neighbours_count(cell[0], cell[1]) == 2 or neighbours_count(cell[0], cell[1]) == 3 and cell not in next_alive:
            next_alive.append(cell)

    next_alive.sort()
    alive_cells = next_alive

def reset():
    global alive_cells
    alive_cells = []

def main():
    global screen, alive_cells, BLOCK_SIZE
    running = True
    is_editing = True
    is_playing = False
    is_grid_visible = True
    title = 'Game of Life - Editing'

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(title)

    alive_cells = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == 'space':
                    is_playing = not is_playing
                    is_editing = not is_playing
                    title = 'Game of Life - Playing' if is_playing else 'Game of Life - Editing'
                    pygame.display.set_caption(title)
                elif pygame.key.name(event.key) == 'm':
                    BLOCK_SIZE = BLOCK_SIZE - 1 if BLOCK_SIZE > 1 else BLOCK_SIZE
                elif pygame.key.name(event.key) == 'l':
                    BLOCK_SIZE += 1
                elif pygame.key.name(event.key) == 'g':
                    is_grid_visible = not is_grid_visible
                elif pygame.key.name(event.key) == 'r':
                    reset()
            elif event.type == MOUSEBUTTONUP and is_editing:
                mouse_x, mouse_y = event.pos
                edit_unit(mouse_x, mouse_y)
        
        if is_playing:
            compute_new_step()

        screen.fill((255, 255, 255))
        draw_units()
        if is_grid_visible:
            draw_grid()
        pygame.display.update()

main()
pygame.quit()