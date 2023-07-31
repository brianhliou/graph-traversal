# maze_generator.py
import random
from queue import Queue

def create_maze_recursive_backtracker(width, height):
    # Create a grid filled with walls
    maze = [['WALL' for x in range(width)] for y in range(height)]
    
    # Create a list to hold the cells to be checked, and add the first cell
    stack = [(1, 1)]
    
    # While there are still cells to be checked
    while stack:
        x, y = stack[-1]
        
        # Mark the cell as part of the maze
        maze[y][x] = 'SPACE'
        
        # Identify potential unvisited neighbors
        neighbors = [(x + dx * 2, y + dy * 2) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] 
                     if 0 < x + dx * 2 < width - 1 and 0 < y + dy * 2 < height - 1 and maze[y + dy * 2][x + dx * 2] == 'WALL']
        
        if neighbors:
            # Choose a random neighboring cell and remove the wall between them
            nx, ny = random.choice(neighbors)
            maze[y + (ny - y) // 2][x + (nx - x) // 2] = 'SPACE'
            
            # Add the chosen cell to the stack
            stack.append((nx, ny))
        else:
            # If a cell has no unvisited neighbors, remove it from the stack
            stack.pop()
    
    # Set a start and end point
    maze[1][1] = 'START'
    maze[height - 2][width - 2] = 'END'
    
    return maze

def create_maze_randomized_generation(width, height):
    # Initialize the maze with spaces
    maze = [['SPACE' for _ in range(width)] for _ in range(height)]

    # Set start and end points
    start_x, start_y = 1, 1
    end_x, end_y = width - 2, height - 2
    maze[start_y][start_x] = 'START'
    maze[end_y][end_x] = 'END'

    # Randomly add a few walls in the middle of the map
    num_walls = (width * height) // 8
    for _ in range(num_walls):
        x, y = random.randint(width // 4, 3 * width // 4), random.randint(height // 4, 3 * height // 4)
        maze[y][x] = 'WALL'

    return maze