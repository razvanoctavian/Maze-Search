class Node:
    """
    Represents a node in the search tree.

    Attributes:
        state: current position in the maze (row, col)
        parent: reference to the previous Node in the path
        action: the move that led from parent.state to this state
                (optional, useful if you want a list of actions)
    """
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


# ---------------------------------------------------------------------

class StackFrontier:
    """
    Frontier implemented as a stack.

    Used for Depth-First Search (DFS).

    Behavior:
        - add(): pushes a node to the end of the list
        - remove(): pops the last node (LIFO: Last-In, First-Out)
    """

    def __init__(self):
        # list of nodes currently in the frontier
        self.frontier = []

    def add(self, node):
        """Add a node to the frontier."""
        self.frontier.append(node)

    def contains_state(self, state):
        """
        Check if there is already a node with the given state
        somewhere in the frontier.
        """
        return any(node.state == state for node in self.frontier)

    def empty(self):
        """Return True if the frontier is empty."""
        return len(self.frontier) == 0

    def remove(self):
        """
        Remove and return the last node in the frontier
        (LIFO behavior, like a stack).

        Raises:
            Exception: if the frontier is empty.
        """
        if self.empty():
            raise Exception("empty frontier")

        node = self.frontier[-1]
        # shrink the list by removing the last element
        self.frontier = self.frontier[:-1]
        return node


# ---------------------------------------------------------------------

class QueueFrontier(StackFrontier):
    """
    Frontier implemented as a queue.

    Used for Breadth-First Search (BFS).

    Behavior:
        - add(): appends to the end (inherited)
        - remove(): removes from the beginning (FIFO)
    """

    def remove(self):
        """
        Remove and return the first node in the frontier
        (FIFO behavior, like a queue).

        Raises:
            Exception: if the frontier is empty.
        """
        if self.empty():
            raise Exception("empty frontier")

        node = self.frontier[0]
        # remove the first element
        self.frontier = self.frontier[1:]
        return node


# ---------------------------------------------------------------------

class GreedyFrontier(StackFrontier):
    """
    Frontier for Greedy Best-First Search (GBFS).

    Instead of using pure LIFO/FIFO, it always selects the node
    with the smallest heuristic value h(n), where:

        h(n) = Manhattan distance from n to the goal cell.
    """

    def __init__(self, maze):
        super().__init__()
        # maze is needed to know where the goal is
        self.maze = maze

    def heuristic(self, state):
        """
        Compute the Manhattan distance between the given state
        and the goal position.

        state: (row, col)
        """
        r, c = state
        gr, gc = self.maze.goal
        return abs(r - gr) + abs(c - gc)

    def remove(self):
        """
        Remove and return the node with the smallest heuristic h(n).

        Raises:
            Exception: if the frontier is empty.
        """
        if self.empty():
            raise Exception("empty frontier")

        # assume the first node is the best
        best_index = 0
        best_h = self.heuristic(self.frontier[0].state)

        # search for a node with a smaller h
        for i in range(len(self.frontier)):
            h_value = self.heuristic(self.frontier[i].state)
            if h_value < best_h:
                best_h = h_value
                best_index = i

        node = self.frontier[best_index]
        self.frontier.pop(best_index)
        return node


# ---------------------------------------------------------------------

class AStarFrontier(GreedyFrontier):
    """
    Frontier for the A* search algorithm.

    Inherits the heuristic from GreedyFrontier and adds a cost function g(n).
    It always selects the node with the smallest evaluation function:

        f(n) = g(n) + h(n)

    where:
        g(n) = cost from start to n (number of steps)
        h(n) = Manhattan distance from n to goal
    """

    def g(self, node):
        """
        Compute g(n): the path cost from the start node to the given node.

        We walk back through the parent chain and count how many steps
        we need to reach the start.
        """
        cost = 0
        current = node

        while current.parent is not None:
            cost += 1
            current = current.parent

        return cost

    def f(self, node):
        """
        A* evaluation function:

            f(n) = g(n) + h(n)
        """
        return self.g(node) + self.heuristic(node.state)

    def remove(self):
        """
        Remove and return the node with the smallest f(n).

        Raises:
            Exception: if the frontier is empty.
        """
        if self.empty():
            raise Exception("empty frontier")

        best_index = 0
        best_f = self.f(self.frontier[0])

        # search for a node with a smaller f
        for i in range(len(self.frontier)):
            f_value = self.f(self.frontier[i])
            if f_value < best_f:
                best_f = f_value
                best_index = i

        node = self.frontier[best_index]
        self.frontier.pop(best_index)
        return node
