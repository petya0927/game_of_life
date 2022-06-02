import pygame
from pygame.locals import MOUSEBUTTONUP
import numpy as np

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
BLOCK_SIZE = 10
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

def edit_unit(x, y):
    unit_pos = (x // BLOCK_SIZE, y // BLOCK_SIZE)
    matrix[unit_pos[0] + OFFSET // 2, unit_pos[1] + OFFSET // 2] = int(not matrix[unit_pos[0] + OFFSET // 2, unit_pos[1] + OFFSET // 2])

def neighbours(unit_x, unit_y):
    return [
        matrix[unit_x-1][unit_y-1], matrix[unit_x][unit_y-1], matrix[unit_x+1][unit_y-1],
        matrix[unit_x-1][unit_y], matrix[unit_x+1][unit_y],
        matrix[unit_x-1][unit_y+1], matrix[unit_x][unit_y+1], matrix[unit_x+1][unit_y+1]
    ].count(1)

def compute_new_step():
    global matrix
    new_matrix = matrix.copy()
    for x in range(0, matrix.shape[0] - 1):
        for y in range(0, matrix.shape[1] - 1):
            if matrix[x][y] == 1:
                if neighbours(x, y) == 2 or neighbours(x, y) == 3:
                    new_matrix[x][y] = 1
                else:
                    new_matrix[x][y] = 0
            
            else:
                if neighbours(x, y) == 3:
                    new_matrix[x][y] = 1

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
    global screen, WINDOW_WIDTH, WINDOW_HEIGHT
    running = True
    is_grid_visible = True
    is_editing = True
    is_playing = False
    title = 'Game of Life - Editing'
    time_delay = 100

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(title)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == 'space':
                    is_playing = not is_playing
                    is_editing = not is_playing
                    title = 'Game of Life - Playing' if is_playing else 'Game of Life'
                    title = 'Game of Life - Editing' if is_editing else title
                    pygame.display.set_caption(title)
                elif pygame.key.name(event.key) == 's':
                    time_delay = time_delay + 30
                elif pygame.key.name(event.key) == 'a':
                    time_delay = time_delay - 30 if time_delay > 0 else 0
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
            elif event.type == pygame.VIDEORESIZE:
                resize(event.w, event.h)
        
        if is_playing:
            compute_new_step()

        draw_units()
        if is_grid_visible:
            draw_grid()
        pygame.display.update()
        if is_playing:
            pygame.time.delay(time_delay)

init_window()
pygame.quit()
