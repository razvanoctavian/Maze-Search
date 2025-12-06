import tkinter as tk

from maze import Maze
from search import search, create_frontier


# Size of each cell in the maze grid
CELL_SIZE = 30


class MazeApp:
    """
    Graphical application for visualizing pathfinding algorithms.

    Responsibilities:
        - Render the maze (walls, start, goal)
        - Provide buttons to choose the algorithm
        - Run the selected algorithm and animate the explored path
        - Draw the final solution path on the canvas
    """

    def __init__(self, root, maze):
        """
        Initialize the GUI window, canvas, buttons, and load the maze.

        Parameters:
            root : Tk root window
            maze : Maze object that provides:
                    .walls, .start, .goal, .height, .width
        """
        self.root = root
        self.maze = maze

        self.root.title("Maze Search Visualizer")

        # Create the drawing canvas 
        self.canvas = tk.Canvas(
            root,
            width=self.maze.width * CELL_SIZE,
            height=self.maze.height * CELL_SIZE
        )
        self.canvas.pack(padx=10, pady=10)

        # Container for algorithm buttons.
        buttons_frame = tk.Frame(root)
        buttons_frame.pack(pady=10)

        # Algorithm selection buttons
        # Each button calls run_algorithm() with its algorithm name
        tk.Button(
            buttons_frame,
            text="DFS",
            bg="#ffcccc",
            command=lambda: self.run_algorithm("DFS")
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            buttons_frame,
            text="BFS",
            bg="#ffcccc",
            command=lambda: self.run_algorithm("BFS")
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            buttons_frame,
            text="GBFS",
            bg="#ffcccc",
            command=lambda: self.run_algorithm("GBFS")
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            buttons_frame,
            text="A*",
            bg="#ffcccc",
            command=lambda: self.run_algorithm("A*")
        ).pack(side=tk.LEFT, padx=5)

        # Draw the initial static maze layout (walls, start, goal).
        self.draw_maze()

    # ---------------------------------------------------------------------

    def draw_maze(self):
        """
        Draw all maze cells on the canvas.

        Walls   → black
        Start   → green
        Goal    → red
        Empty   → white
        """
        self.canvas.delete("all")

        for r in range(self.maze.height):
            for c in range(self.maze.width):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                # Determine cell color
                if self.maze.walls[r][c]:
                    fill = "black"
                elif (r, c) == self.maze.start:
                    fill = "green"
                elif (r, c) == self.maze.goal:
                    fill = "red"
                else:
                    fill = "white"

                # Draw the cell rectangle
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=fill, outline="gray"
                )

    # ---------------------------------------------------------------------

    def color_cell(self, r, c, color):
        """
        Color a specific maze cell.

        Parameters:
            r, c : row and column index
            color : fill color (string)
        """
        x1 = c * CELL_SIZE
        y1 = r * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE

        self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=color, outline="gray"
        )

    # ---------------------------------------------------------------------

    def run_algorithm(self, algo_name):
        """
        Run a selected search algorithm and visualize the resulting path.

        Steps:
            1. Clear the previous path and redraw the maze.
            2. Create the appropriate frontier (DFS/BFS/GBFS/A*).
            3. Run the search() function.
            4. Animate or color the discovered solution path.
        """
        # Reset canvas before drawing a new path
        self.draw_maze()

        # Create algorithm-specific frontier
        frontier = create_frontier(algo_name, self.maze)

        # Run the search algorithm
        actions, cells = search(self.maze, frontier)

        # Animate the final solution path
        for (r, c) in cells:

            # Do not overwrite start/goal colors
            if (r, c) == self.maze.start or (r, c) == self.maze.goal:
                continue

            self.color_cell(r, c, "cyan")

            # Update the GUI to show animation
            self.root.update()
            self.root.after(50)  # delay for animation effect


# ---------------------------------------------------------------------

def main():
    """Create the Maze object, launch the Tkinter window."""
    maze = Maze("MAZE.txt")

    root = tk.Tk()
    app = MazeApp(root, maze)
    root.mainloop()


if __name__ == "__main__":
    main()
