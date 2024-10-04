import pygame
import random

# Constants for screen dimensions and colors
WIDTH, HEIGHT = 800, 600
SQUARE_SIZE = 20
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Maze dimensions
MAZE_WIDTH = WIDTH // SQUARE_SIZE
MAZE_HEIGHT = HEIGHT // SQUARE_SIZE

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Red Square")
clock = pygame.time.Clock()

# Starting positions of the squares
red_square_x = 0
red_square_y = HEIGHT // 2
blue_square_x = WIDTH - SQUARE_SIZE
blue_square_y = HEIGHT // 2

# Function to create the maze
def create_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    # Function to carve passages in the maze
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

# Create the maze
maze = create_maze(MAZE_WIDTH, MAZE_HEIGHT)

# Set to track visited positions
visited_positions = set()
visited_positions.add((0, HEIGHT // (2 * SQUARE_SIZE)))  # Add the starting position of the red square

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses for moving the red square
    keys = pygame.key.get_pressed()
    next_x, next_y = red_square_x, red_square_y
    
    if keys[pygame.K_UP]:
        next_y -= SQUARE_SIZE
    elif keys[pygame.K_DOWN]:
        next_y += SQUARE_SIZE
    elif keys[pygame.K_LEFT]:
        next_x -= SQUARE_SIZE
    elif keys[pygame.K_RIGHT]:
        next_x += SQUARE_SIZE

    # Check if the next position is valid
    if (0 <= next_x < WIDTH) and (0 <= next_y < HEIGHT):
        maze_x = next_y // SQUARE_SIZE
        maze_y = next_x // SQUARE_SIZE
        
        if maze[maze_x][maze_y] == 0:
            red_square_x = next_x
            red_square_y = next_y
            visited_positions.add((maze_y, maze_x))  # Add the new position to visited positions

    # Clear the screen
    screen.fill(WHITE)

    # Draw the maze
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Draw the visited positions
    for (x, y) in visited_positions:
        pygame.draw.rect(screen, GREEN, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Draw the blue and red squares
    pygame.draw.rect(screen, BLUE, (blue_square_x, blue_square_y, SQUARE_SIZE, SQUARE_SIZE)) 
    pygame.draw.rect(screen, RED, (red_square_x, red_square_y, SQUARE_SIZE, SQUARE_SIZE))

    # Update the display
    pygame.display.flip()
    clock.tick(30)

# Quit Pygame
pygame.quit()
