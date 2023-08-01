# maze_solver.py
from collections import deque
from queue import PriorityQueue
from math import sqrt

def solve_maze_dfs(maze, start, end):
    width, height = len(maze[0]), len(maze)
    stack = [start]
    visited = set()
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, left, down, up
    came_from = {start: None}

    while stack:
        x, y = stack[-1]
        if (x, y) == end:
            # Reconstruct the path
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = came_from[(x, y)]
            path.append(start)
            path.append(end)  # Explicitly add the end cell
            path.reverse()
            return path

        if (x, y) not in visited:
            visited.add((x, y))
            yield x, y  # Yield the current position

        # Check all neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < width and 0 <= ny < height and  # Within boundary
                maze[ny][nx] != 'WALL' and                # Not a wall
                (nx, ny) not in visited):                 # Not visited yet
                stack.append((nx, ny))
                came_from[(nx, ny)] = (x, y)
                break
        else:
            stack.pop()

    yield None  # Indicate that no solution was found

def solve_maze_bfs(maze, start, end):
    width, height = len(maze[0]), len(maze)
    queue = deque([start])
    visited = set()
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, left, down, up
    came_from = {start: None}

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            # Reconstruct the path
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = came_from[(x, y)]
            path.append(start)
            path.reverse()
            return path

        if (x, y) not in visited:
            visited.add((x, y))
            yield x, y  # Yield the current position

        # Check all neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < width and 0 <= ny < height and  # Within boundary
                maze[ny][nx] != 'WALL' and                # Not a wall
                (nx, ny) not in visited):                 # Not visited yet
                queue.append((nx, ny))
                came_from[(nx, ny)] = (x, y)

    yield None  # Indicate that no solution was found
    
def solve_maze_astar(maze, start, end):
    width, height = len(maze[0]), len(maze)
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, left, down, up

    while not frontier.empty():
        _, current = frontier.get()

        if current == end:
            # Reconstruct the path
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        x, y = current
        yield x, y  # Yield the current position

        # Check all neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < width and 0 <= ny < height and  # Within boundary
                maze[ny][nx] != 'WALL'):                  # Not a wall
                new_cost = cost_so_far[(x, y)] + 1
                if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                    cost_so_far[(nx, ny)] = new_cost
                    priority = new_cost + sqrt((nx - end[0]) ** 2 + (ny - end[1]) ** 2)
                    frontier.put((priority, (nx, ny)))
                    came_from[(nx, ny)] = (x, y)

    yield None  # Indicate that no solution was found