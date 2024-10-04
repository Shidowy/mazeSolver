import pygame
import random
import heapq

# Constants for screen dimensions and colors
WIDTH, HEIGHT = 850, 600  # Adjust width to fit buttons and maze
SQUARE_SIZE = 20
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (150, 150, 150)
TEXT_COLOR = (0, 0, 0)

MAZE_WIDTH = (WIDTH - BUTTON_WIDTH - 50) // SQUARE_SIZE  # Leave room for buttons
MAZE_HEIGHT = HEIGHT // SQUARE_SIZE

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver with Dijkstra and A*")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

red_square_x = 0
red_square_y = HEIGHT // 2

# Create buttons
def draw_button(text, x, y, width, height, mouse_pos):
    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        color = BUTTON_HOVER_COLOR
    else:
        color = BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surf = font.render(text, True, TEXT_COLOR)
    screen.blit(text_surf, (x + (width - text_surf.get_width()) // 2, y + (height - text_surf.get_height()) // 2))

# Create the maze
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

# Find valid blue position
def find_valid_blue_position(maze):
    valid_positions = [(x, y) for y in range(MAZE_HEIGHT) for x in range(MAZE_WIDTH) if maze[y][x] == 0]
    return random.choice(valid_positions)

red_square_current_pos = (0, HEIGHT // (2 * SQUARE_SIZE))
visited_positions = set()
visited_positions.add(red_square_current_pos)
stack = []
blue_square_pos = find_valid_blue_position(maze)
blue_square_x, blue_square_y = blue_square_pos[0] * SQUARE_SIZE, blue_square_pos[1] * SQUARE_SIZE

# Dijkstra's algorithm
def dijkstra(start, goal):
    dist = {start: 0}
    prev = {start: None}
    visited = set()  # Track visited cells
    pq = [(0, start)]
    while pq:
        current_dist, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            break
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 0 and (nx, ny) not in visited:
                next_pos = (nx, ny)
                new_dist = current_dist + 1
                if next_pos not in dist or new_dist < dist[next_pos]:
                    dist[next_pos] = new_dist
                    prev[next_pos] = current
                    heapq.heappush(pq, (new_dist, next_pos))
    return reconstruct_path(prev, start, goal)

# A* algorithm
def a_star(start, goal):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    dist = {start: 0}
    prev = {start: None}
    visited = set()  # Track visited cells
    pq = [(heuristic(start, goal), start)]
    while pq:
        _, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            break
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 0 and (nx, ny) not in visited:
                next_pos = (nx, ny)
                new_dist = dist[current] + 1
                if next_pos not in dist or new_dist < dist[next_pos]:
                    dist[next_pos] = new_dist
                    prev[next_pos] = current
                    heapq.heappush(pq, (new_dist + heuristic(next_pos, goal), next_pos))
    return reconstruct_path(prev, start, goal)

# Reconstruct path for both algorithms
def reconstruct_path(prev, start, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    return path

# Function to draw maze and path
def draw_maze():
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    for (x, y) in visited_positions:
        pygame.draw.rect(screen, GREEN, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    pygame.draw.rect(screen, BLUE, (blue_square_x, blue_square_y, SQUARE_SIZE, SQUARE_SIZE))
    pygame.draw.rect(screen, RED, (red_square_x, red_square_y, SQUARE_SIZE, SQUARE_SIZE))

# Reset maze
def reset_maze():
    global maze, red_square_current_pos, visited_positions, blue_square_pos, blue_square_x, blue_square_y
    maze = create_maze(MAZE_WIDTH, MAZE_HEIGHT)
    red_square_current_pos = (0, HEIGHT // (2 * SQUARE_SIZE))
    visited_positions.clear()
    visited_positions.add(red_square_current_pos)
    blue_square_pos = find_valid_blue_position(maze)
    blue_square_x, blue_square_y = blue_square_pos[0] * SQUARE_SIZE, blue_square_pos[1] * SQUARE_SIZE

# Main loop
selected_algorithm = None
running = True
path = []
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if MAZE_WIDTH * SQUARE_SIZE + 50 <= mouse_pos[0] <= MAZE_WIDTH * SQUARE_SIZE + 150 and 50 <= mouse_pos[1] <= 100:
                selected_algorithm = 'dijkstra'
                reset_maze()
                path = []  # Clear path when resetting maze
            elif MAZE_WIDTH * SQUARE_SIZE + 50 <= mouse_pos[0] <= MAZE_WIDTH * SQUARE_SIZE + 150 and 150 <= mouse_pos[1] <= 200:
                selected_algorithm = 'a_star'
                reset_maze()
                path = []  # Clear path when resetting maze

    screen.fill(WHITE)

    if selected_algorithm:
        if not path:  # Only calculate path if it hasn't been calculated yet
            if selected_algorithm == 'dijkstra':
                path = dijkstra(red_square_current_pos, blue_square_pos)
            elif selected_algorithm == 'a_star':
                path = a_star(red_square_current_pos, blue_square_pos)

        if path:
            # Draw the path incrementally
            if visited_positions != set(path):  # Only update if there's new positions in path
                next_pos = path[len(visited_positions)]
                visited_positions.add(next_pos)
                red_square_x, red_square_y = next_pos[0] * SQUARE_SIZE, next_pos[1] * SQUARE_SIZE

    draw_maze()
    draw_button("Dijkstra", MAZE_WIDTH * SQUARE_SIZE + 50, 50, BUTTON_WIDTH, BUTTON_HEIGHT, mouse_pos)
    draw_button("A*", MAZE_WIDTH * SQUARE_SIZE + 50, 150, BUTTON_WIDTH, BUTTON_HEIGHT, mouse_pos)

    pygame.display.flip()
    clock.tick(10)  # Control the speed of the animation

pygame.quit()
