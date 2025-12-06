from logic import Node, StackFrontier, QueueFrontier, GreedyFrontier, AStarFrontier


def search(maze, frontier):
    """
    Generic graph search algorithm.

    Parameters:
        maze: Maze object that provides:
              - maze.start : start state (row, col)
              - maze.goal  : goal state (row, col)
              - maze.neighbours(state) : returns (action, next_state) pairs
        frontier: one of:
              - StackFrontier  (DFS)
              - QueueFrontier  (BFS)
              - GreedyFrontier (Greedy Best-First Search)
              - AStarFrontier  (A*)

    Algorithm:

        1) Initialize the frontier with the starting state.
        2) Initialize an empty explored set.
        3) Repeat:
            a) If the frontier is empty → no solution.
            b) Remove a node from the frontier.
            c) If node.state is the goal → reconstruct and return the solution.
            d) Add node.state to the explored set.
            e) For each neighbor of node.state:
                   if not in frontier and not in explored → add to frontier.
    """

    # 1) frontier starts with the initial state
    start_node = Node(state=maze.start, parent=None, action=None)
    frontier.add(start_node)

    # 2) explored set (closed set)
    explored = set()

    # 3) main loop
    while True:

        # a) if the frontier is empty → no solution exists
        if frontier.empty():
            raise Exception("No solution")

        # b) choose a node from the frontier
        node = frontier.remove()

        # c) if this node is the goal → reconstruct the path and return
        if node.state == maze.goal:
            actions = []  # list of actions from start to goal
            cells = []    # list of states (positions) from start to goal

            # walk back through parents to reconstruct the path
            while node.parent is not None:
                actions.append(node.action)
                cells.append(node.state)
                node = node.parent

            # we built the path from goal to start, so we reverse it
            actions.reverse()
            cells.reverse()

            return actions, cells

        # d) if not goal, mark the state as explored
        explored.add(node.state)

        # e) expand neighbors and add valid ones to the frontier
        for action, state in maze.neighbours(node.state):
            # add neighbor only if:
            #  - it's not already in the frontier
            #  - it hasn't been explored yet
            if (
                not frontier.contains_state(state)
                and state not in explored
            ):
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)


# ---------------------------------------------------------------------

def create_frontier(name, maze=None):
    """
    Create and return the appropriate frontier object
    based on the algorithm name.

    Parameters:
        name: algorithm name as string:
              "DFS", "BFS", "GBFS", "A*"
        maze: Maze object, required for heuristic-based frontiers
              (GreedyFrontier, AStarFrontier)

    Returns:
        An instance of:
            - StackFrontier
            - QueueFrontier
            - GreedyFrontier
            - AStarFrontier

    Raises:
        ValueError: if the algorithm name is unknown.
    """

    alg = name.upper()

    if alg == "DFS":
        return StackFrontier()
    elif alg == "BFS":
        return QueueFrontier()
    elif alg == "GBFS":
        return GreedyFrontier(maze)
    elif alg in ("A*", "ASTAR", "A-STAR"):
        return AStarFrontier(maze)
    else:
        raise ValueError(f"Unknown algorithm name: {name}")

