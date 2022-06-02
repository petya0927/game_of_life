import pygame
from pygame.locals import MOUSEBUTTONUP
import numpy as np

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
BLOCK_SIZE = 20
OFFSET = 100

matrix = np.zeros((WINDOW_WIDTH // BLOCK_SIZE + OFFSET, WINDOW_HEIGHT // BLOCK_SIZE + OFFSET), dtype=int)

def draw_units():
    for x in range(OFFSET // 2, matrix.shape[0] - OFFSET // 2):
        for y in range(OFFSET // 2, matrix.shape[1] - OFFSET // 2):
            if matrix[x][y] == 1:
                rect = pygame.Rect((x - OFFSET // 2) * BLOCK_SIZE, (y - OFFSET // 2) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, (0, 0, 0), rect)
            else:
                rect = pygame.Rect((x - OFFSET // 2) * BLOCK_SIZE, (y - OFFSET // 2) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, (255, 255, 255), rect)

def draw_grid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, (100, 100, 100), rect, 1)

def edit_unit(mouse_x, mouse_y):
    unit_pos = (mouse_x // BLOCK_SIZE, mouse_y // BLOCK_SIZE)
    matrix[unit_pos[0] + OFFSET // 2, unit_pos[1] + OFFSET // 2] = int(not matrix[unit_pos[0] + OFFSET // 2, unit_pos[1] + OFFSET // 2])

def neighbours_coords(x, y):
    return [
        (x-1, y-1), (x, y-1), (x+1, y-1),
        (x-1, y), (x+1, y),
        (x-1, y+1), (x, y+1), (x+1, y+1)
    ]

def neighbours_count(x, y):
    return [
        matrix[x-1][y-1], matrix[x][y-1], matrix[x+1][y-1],
        matrix[x-1][y], matrix[x+1][y],
        matrix[x-1][y+1], matrix[x][y+1], matrix[x+1][y+1]
    ].count(1)


def check_neighbours(x, y, new_matrix):
    global matrix
    for cell in neighbours_coords(x, y):
        if matrix[cell] == 0 and neighbours_count(cell[0], cell[1]) == 3:
                new_matrix[cell] = 1

def compute_new_step():
    global matrix
    new_matrix = matrix.copy()
    alive_cells = np.argwhere(matrix == 1)
    
    for cell in alive_cells:
        if cell[0] == WINDOW_WIDTH // BLOCK_SIZE + OFFSET - 2 or cell[1] == WINDOW_HEIGHT // BLOCK_SIZE + OFFSET - 2 or cell[0] == 1 or cell[1] == 1:
            new_matrix[cell] = 0
        else:
            check_neighbours(cell[0], cell[1], new_matrix)
            if neighbours_count(cell[0], cell[1]) == 2 or neighbours_count(cell[0], cell[1]) == 3:
                new_matrix[cell[0]][cell[1]] = 1
            else:
                new_matrix[cell[0]][cell[1]] = 0

    matrix = new_matrix.copy()

def reset():
    matrix.fill(0)

def copy_matrixes(matrix, new_matrix):
    for x in range(0, new_matrix.shape[0] - 1):
        for y in range(0, new_matrix.shape[1] - 1):
            try:
                new_matrix[x][y] = matrix[x][y]
            except:
                new_matrix[x][y] = 0

def resize(w, h):
    global screen, WINDOW_WIDTH, WINDOW_HEIGHT, matrix
    WINDOW_WIDTH = w
    WINDOW_HEIGHT = h
    new_matrix = np.zeros((WINDOW_WIDTH // BLOCK_SIZE + OFFSET, WINDOW_HEIGHT // BLOCK_SIZE + OFFSET), dtype=int)
    copy_matrixes(matrix, new_matrix)
    matrix = new_matrix.copy()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

def show_more():
    global matrix, BLOCK_SIZE
    BLOCK_SIZE -= 1 if BLOCK_SIZE > 3 else 0
    new_matrix = np.zeros((WINDOW_WIDTH // BLOCK_SIZE + OFFSET, WINDOW_HEIGHT // BLOCK_SIZE + OFFSET), dtype=int)
    copy_matrixes(matrix, new_matrix)
    matrix = new_matrix.copy()

def show_less():
    global matrix, BLOCK_SIZE
    BLOCK_SIZE += 1
    new_matrix = np.zeros((WINDOW_WIDTH // BLOCK_SIZE + OFFSET, WINDOW_HEIGHT // BLOCK_SIZE + OFFSET), dtype=int)
    copy_matrixes(matrix, new_matrix)
    matrix = new_matrix.copy()

def init_window():
    global screen
    running = True
    is_editing = True
    is_playing = False
    is_grid_visible = True
    title = 'Game of Life - Editing'

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(title)

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
                    show_more()
                elif pygame.key.name(event.key) == 'l':
                    show_less()
                elif pygame.key.name(event.key) == 'g':
                    is_grid_visible = not is_grid_visible
                elif pygame.key.name(event.key) == 'r':
                    reset()
            elif event.type == MOUSEBUTTONUP and is_editing:
                mouse_x, mouse_y = event.pos
                edit_unit(mouse_x, mouse_y)
        
        if is_playing:
            compute_new_step()

        draw_units()
        if is_grid_visible:
            draw_grid()
        pygame.display.update()

init_window()
pygame.quit()