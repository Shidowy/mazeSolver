import pygame
import random

WIDTH, HEIGHT = 800, 600
SQUARE_SIZE = 20
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

MAZE_WIDTH = WIDTH // SQUARE_SIZE
MAZE_HEIGHT = HEIGHT // SQUARE_SIZE

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Backtracking Maze Solver")
clock = pygame.time.Clock()

red_square_x = 0
red_square_y = HEIGHT // 2

def create_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    def carve_passages(x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[y + dy][x + dx] = 0
                maze[ny][nx] = 0
                carve_passages(nx, ny)
    start_x, start_y = random.randint(0, width // 2) * 2, random.randint(0, height // 2) * 2
    maze[start_y][start_x] = 0
    carve_passages(start_x, start_y)
    return maze

maze = create_maze(MAZE_WIDTH, MAZE_HEIGHT)

def find_valid_blue_position(maze):
    valid_positions = []
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 0:
                valid_positions.append((x, y))
    return random.choice(valid_positions)

red_square_current_pos = (0, HEIGHT // (2 * SQUARE_SIZE))
visited_positions = set()
visited_positions.add(red_square_current_pos)
stack = []

blue_square_pos = find_valid_blue_position(maze)
blue_square_x, blue_square_y = blue_square_pos[0] * SQUARE_SIZE, blue_square_pos[1] * SQUARE_SIZE

def solver():
    global red_square_x, red_square_y, stack, red_square_current_pos
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    random.shuffle(directions)
    current_x, current_y = red_square_current_pos
    moved = False
    for dx, dy in directions:
        nx, ny = current_x + dx, current_y + dy
        if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 0 and (nx, ny) not in visited_positions:
            red_square_current_pos = (nx, ny)
            red_square_x = nx * SQUARE_SIZE
            red_square_y = ny * SQUARE_SIZE
            visited_positions.add((nx, ny))
            stack.append((current_x, current_y))
            moved = True
            break
    if not moved and stack:
        red_square_current_pos = stack.pop()
        red_square_x = red_square_current_pos[0] * SQUARE_SIZE
        red_square_y = red_square_current_pos[1] * SQUARE_SIZE

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    solver()

    if red_square_current_pos == blue_square_pos:
        print("Maze Completed!")
        running = False

    screen.fill(WHITE)

    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    for (x, y) in visited_positions:
        pygame.draw.rect(screen, GREEN, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    pygame.draw.rect(screen, BLUE, (blue_square_x, blue_square_y, SQUARE_SIZE, SQUARE_SIZE)) 
    pygame.draw.rect(screen, RED, (red_square_x, red_square_y, SQUARE_SIZE, SQUARE_SIZE))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
