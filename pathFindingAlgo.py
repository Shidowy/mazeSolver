import pygame
import random
import heapq

# Constants for screen dimensions and colors
WIDTH, HEIGHT = 850, 600  # Adjust width to fit buttons and maze
SQUARE_SIZE = 10
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
pygame.display.set_caption("Maze Solver with Dijkstra, A*, DFS, and BFS")
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

# Create the maze using Kruskal's algorithm
def create_maze(width, height):
    # Initialize the maze with walls (1)
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    # Create a list of edges
    edges = []
    for y in range(height):
        for x in range(width):
            if x < width - 1:
                edges.append(((x, y), (x + 1, y)))  # Horizontal edge
            if y < height - 1:
                edges.append(((x, y), (x, y + 1)))  # Vertical edge

    random.shuffle(edges)  # Shuffle edges to ensure randomness

    # Union-Find (Disjoint Set) to track connected components
    parent = {}
    rank = {}

    def find(cell):
        if parent[cell] != cell:
            parent[cell] = find(parent[cell])
        return parent[cell]

    def union(cell1, cell2):
        root1 = find(cell1)
        root2 = find(cell2)
        if root1 != root2:
            # Union by rank
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1

    # Initialize union-find data structure
    for y in range(height):
        for x in range(width):
            cell = (x, y)
            parent[cell] = cell
            rank[cell] = 0

    # Kruskal's Algorithm to create the maze
    for edge in edges:
        cell1, cell2 = edge
        if find(cell1) != find(cell2):
            union(cell1, cell2)
            x1, y1 = cell1
            x2, y2 = cell2
            # Remove wall between cell1 and cell2
            if x1 == x2:  # Vertical wall
                maze[max(y1, y2)][x1] = 0
            else:  # Horizontal wall
                maze[y1][max(x1, x2)] = 0

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

# DFS algorithm
def dfs(start, goal):
    stack = [start]
    visited = set()
    prev = {start: None}
    
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            break
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 0 and (nx, ny) not in visited:
                next_pos = (nx, ny)
                stack.append(next_pos)
                prev[next_pos] = current
    return reconstruct_path(prev, start, goal)

# BFS algorithm
def bfs(start, goal):
    queue = [start]
    visited = set()
    prev = {start: None}
    
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            break
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 0 and (nx, ny) not in visited:
                next_pos = (nx, ny)
                queue.append(next_pos)
                prev[next_pos] = current
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
    global red_square_current_pos, visited_positions, blue_square_pos, blue_square_x, blue_square_y
    red_square_current_pos = (0, HEIGHT // (2 * SQUARE_SIZE))
    visited_positions.clear()
    visited_positions.add(red_square_current_pos)
    blue_square_pos = find_valid_blue_position(maze)
    blue_square_x, blue_square_y = blue_square_pos[0] * SQUARE_SIZE, blue_square_pos[1] * SQUARE_SIZE

# Reset path only
def reset_path():
    global red_square_current_pos, visited_positions
    visited_positions.clear()
    visited_positions.add(red_square_current_pos)
    path.clear()  # Clear the current path

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
            # Check for the buttons
            if MAZE_WIDTH * SQUARE_SIZE + 50 <= mouse_pos[0] <= MAZE_WIDTH * SQUARE_SIZE + 150 and 50 <= mouse_pos[1] <= 100:
                selected_algorithm = 'dijkstra'
                reset_path()  # Only reset the path
            elif MAZE_WIDTH * SQUARE_SIZE + 50 <= mouse_pos[0] <= MAZE_WIDTH * SQUARE_SIZE + 150 and 150 <= mouse_pos[1] <= 200:
                selected_algorithm = 'a_star'
                reset_path()  # Only reset the path
            elif MAZE_WIDTH * SQUARE_SIZE + 50 <= mouse_pos[0] <= MAZE_WIDTH * SQUARE_SIZE + 150 and 250 <= mouse_pos[1] <= 300:
                selected_algorithm = 'dfs'
                reset_path()  # Only reset the path
            elif MAZE_WIDTH * SQUARE_SIZE + 50 <= mouse_pos[0] <= MAZE_WIDTH * SQUARE_SIZE + 150 and 350 <= mouse_pos[1] <= 400:
                selected_algorithm = 'bfs'
                reset_path()  # Only reset the path
            elif MAZE_WIDTH * SQUARE_SIZE + 50 <= mouse_pos[0] <= MAZE_WIDTH * SQUARE_SIZE + 150 and 450 <= mouse_pos[1] <= 500:
                maze = create_maze(MAZE_WIDTH, MAZE_HEIGHT)
                reset_path()

    screen.fill(WHITE)

    if selected_algorithm:
        if not path:  # Only calculate path if it hasn't been calculated yet
            if selected_algorithm == 'dijkstra':
                path = dijkstra(red_square_current_pos, blue_square_pos)
            elif selected_algorithm == 'a_star':
                path = a_star(red_square_current_pos, blue_square_pos)
            elif selected_algorithm == 'dfs':
                path = dfs(red_square_current_pos, blue_square_pos)
            elif selected_algorithm == 'bfs':
                path = bfs(red_square_current_pos, blue_square_pos)

        if path:
            # Draw the path incrementally
            if visited_positions != set(path):  # Only update if there's new positions in path
                next_pos = path[len(visited_positions)]
                visited_positions.add(next_pos)
                red_square_x, red_square_y = next_pos[0] * SQUARE_SIZE, next_pos[1] * SQUARE_SIZE

    draw_maze()
    draw_button("Dijkstra", MAZE_WIDTH * SQUARE_SIZE + 50, 50, BUTTON_WIDTH, BUTTON_HEIGHT, mouse_pos)
    draw_button("A*", MAZE_WIDTH * SQUARE_SIZE + 50, 150, BUTTON_WIDTH, BUTTON_HEIGHT, mouse_pos)
    draw_button("DFS", MAZE_WIDTH * SQUARE_SIZE + 50, 250, BUTTON_WIDTH, BUTTON_HEIGHT, mouse_pos)
    draw_button("BFS", MAZE_WIDTH * SQUARE_SIZE + 50, 350, BUTTON_WIDTH, BUTTON_HEIGHT, mouse_pos)
    draw_button("Reset Path", MAZE_WIDTH * SQUARE_SIZE + 50, 450, BUTTON_WIDTH, BUTTON_HEIGHT, mouse_pos)  # New reset button

    pygame.display.flip()
    clock.tick(30)  

pygame.quit()