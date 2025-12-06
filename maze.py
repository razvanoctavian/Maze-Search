class Maze:
    """
    Represents a maze loaded from a text file.

    Based on the file contents, it builds:
        - self.walls : 2D boolean matrix indicating walls
                       True  -> wall (cannot pass)
                       False -> free cell (can pass)
        - self.start : (row, col) position of the 'A' start
        - self.goal  : (row, col) position of the 'B' goal
        - self.height, self.width : maze dimensions
    """

    def __init__(self, filename):
        """
        Load the maze structure from a text file.

        The file is expected to contain:
            - '#' for walls
            - ' ' (space) for free cells
            - exactly one 'A' for the start
            - exactly one 'B' for the goal

        This constructor initializes:
            - self.walls
            - self.start and self.goal
            - self.height and self.width
        """

        # read entire file
        with open(filename, "r") as f:
            contents = f.read()

        # validate that there is exactly one start and one goal
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start 'A'.")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal 'B'.")

        # split into lines
        lines = contents.splitlines()

        # determine dimensions
        self.height = len(lines)                       # number of rows
        self.width = max(len(line) for line in lines)  # length of the longest row

        # initialize walls matrix and start/goal positions
        self.walls = []
        self.start = None
        self.goal = None

        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    col = lines[i][j]
                except IndexError:
                    # if the line is shorter, pad with a free space
                    col = " "

                if col == "A":
                    self.start = (i, j)
                    row.append(False)   # not a wall
                elif col == "B":
                    self.goal = (i, j)
                    row.append(False)
                elif col == " ":
                    row.append(False)
                else:
                    # any other character is treated as a wall
                    row.append(True)

            self.walls.append(row)

        # optional: double-check that start/goal were actually set
        if self.start is None or self.goal is None:
            raise Exception("Maze must contain both 'A' (start) and 'B' (goal).")

    # ---------------------------------------------------------------------

    def neighbours(self, state):
        """
        Return all accessible neighbours of a given state.

        Parameters:
            state: (row, col) tuple representing the current position.

        Returns:
            A list of (action, new_state) pairs, where:
                - action    : 'up', 'down', 'left', or 'right'
                - new_state : (row, col) after applying that move

        A move is valid if:
            - it stays inside the maze boundaries
            - it does not land on a wall
        """

        row, col = state  # unpack state

        # possible moves (action, (new_row, new_col))
        candidates = [
            ("up",    (row - 1, col)),      # move up
            ("down",  (row + 1, col)),      # move down
            ("left",  (row, col - 1)),      # move left
            ("right", (row, col + 1)),      # move right
        ]

        result = []
        for action, (r, c) in candidates:
            if (
                0 <= r < self.height and      # inside row bounds
                0 <= c < self.width and       # inside column bounds
                not self.walls[r][c]          # not a wall
            ):
                result.append((action, (r, c)))

        return result
