# gui.py
import tkinter as tk

from maze_generator import create_maze_recursive_backtracker, create_maze_randomized_generation
from maze_solver import solve_maze_dfs, solve_maze_bfs, solve_maze_astar

class MazeGUI:
    def __init__(self):
        self.generators = {
            'Recursive Backtracker': create_maze_recursive_backtracker,
            'Randomized generation': create_maze_randomized_generation
        }

        self.solvers = {
            'DFS': solve_maze_dfs,
            'BFS': solve_maze_bfs,  # Add more solver functions as needed
            'A*': solve_maze_astar
        }

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Maze Solver")

        # Create frames for the buttons
        gen_frame = tk.Frame(self.root)
        gen_frame.pack(side=tk.TOP, fill=tk.X)
        solve_frame = tk.Frame(self.root)
        solve_frame.pack(side=tk.TOP, fill=tk.X)

        # Create the "Generate" radio buttons in the generator frame
        self.gen_var = tk.StringVar(value='Recursive Backtracker')  # Variable for the selected generation algorithm
        for gen in self.generators.keys():
            rb = tk.Radiobutton(gen_frame, text=gen, variable=self.gen_var, value=gen)
            rb.pack(side=tk.LEFT)

        # Create the "Generate" button in the generator frame
        self.generate_button = tk.Button(gen_frame, text="Generate", command=self.generate_maze)
        self.generate_button.pack(side=tk.LEFT)

        # Create the "Solve" radio buttons in the solver frame
        self.alg_var = tk.StringVar(value='DFS')  # Variable for the selected solver algorithm
        for alg in self.solvers.keys():
            rb = tk.Radiobutton(solve_frame, text=alg, variable=self.alg_var, value=alg)
            rb.pack(side=tk.LEFT)

        # Create the "Solve" button in the solver frame
        self.solve_button = tk.Button(solve_frame, text="Solve", command=self.solve_maze)
        self.solve_button.pack(side=tk.LEFT)

        # Create the "Reset" button
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_maze)
        self.reset_button.pack(side=tk.TOP)

        # Create the canvas
        self.canvas = tk.Canvas(self.root, width=210, height=210)
        self.canvas.pack(side=tk.TOP)

        self.generate_maze()
    
    def generate_maze(self):
        # Use the selected generator
        generator = self.generators[self.gen_var.get()]

        self.maze = generator(21, 21)
        self.draw_maze()
        self.solve_button.config(state='normal')  # Re-enable the "Solve" button

    def draw_maze(self):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == 'WALL':
                    color = 'black'
                elif (x, y) == (1, 1):  # start square
                    color = 'green'
                elif (x, y) == (len(self.maze[0]) - 2, len(self.maze) - 2):  # end square
                    color = 'red'
                else:
                    color = 'white'
                self.canvas.create_rectangle(x*10, y*10, x*10+10, y*10+10, fill=color)


    def draw_path(self, path, color='red'):
        for x, y in path:
            self.canvas.create_rectangle(x*10, y*10, x*10+10, y*10+10, fill=color)

    def solve_maze(self):
        self.solve_button.config(state='disabled')  # Disable the "Solve" button
        self.generate_button.config(state='disabled')  # Disable the "Generate" button
        self.reset_button.config(state='disabled')  # Disable the "Reset" button

        # Use the selected solver
        solver = self.solvers[self.alg_var.get()]

        self.steps = solver(self.maze, (1, 1), (len(self.maze[0]) - 2, len(self.maze) - 2))
        self.root.after(0, self.animate_solver)

    def animate_solver(self):
        try:
            x, y = next(self.steps)
            if (x, y) != (1, 1):  # Skip the start square
                self.canvas.create_rectangle(x*10, y*10, x*10+10, y*10+10, fill='lightblue')
            self.root.after(100, self.animate_solver)  # Schedule the next animation step
        except StopIteration:
            self.solve_button.config(state='normal')  # Re-enable the "Solve" button
            self.generate_button.config(state='normal')  # Re-enable the "Generate" button
            self.reset_button.config(state='normal')  # Re-enable the "Reset" button

    def show(self):
        # Draw the maze and start the main event loop
        self.draw_maze()
        self.root.mainloop()

    def reset_maze(self):
        self.solve_button.config(state='disabled')  # Disable the "Solve" button
        self.generate_button.config(state='disabled')  # Disable the "Generate" button
        # Clear the path by drawing white squares over it
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell != 'WALL' and (x, y) != (1, 1) and (x, y) != (len(self.maze[0]) - 2, len(self.maze) - 2):
                    self.canvas.create_rectangle(x*10, y*10, x*10+10, y*10+10, fill='white')
        self.solve_button.config(state='normal')  # Re-enable the "Solve" button
        self.generate_button.config(state='normal')  # Re-enable the "Generate" button
