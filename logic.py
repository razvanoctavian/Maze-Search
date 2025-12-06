class Node:
    """
    Reprezintă un nod din algoritmul de căutare.

    Atribute:
    - state: poziția curentă (row, col)
    - parent: nodul părinte (pentru reconstrucția drumului)
    - action: acțiunea care a dus la acest nod (nesemnificativă aici)
    """
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


# ---------------------------------------------------------------------

class StackFrontier:
    """
    Frontieră de tip stivă (stack), folosită pentru algoritmul DFS.

    Caracteristică:
    - remove() → scoate ultimul element (LIFO)
    """

    def __init__(self):
        self.frontier = []

    def add(self, node):
        """Adaugă nodul la finalul frontierei."""
        self.frontier.append(node)

    def contains_state(self, state):
        """Verifică dacă starea există deja în frontieră."""
        return any(node.state == state for node in self.frontier)

    def empty(self):
        """True dacă frontiera nu conține noduri."""
        return len(self.frontier) == 0

    def remove(self):
        """Scoate ultimul nod din frontieră (LIFO)."""
        if self.empty():
            raise Exception("empty frontier")
        
        node = self.frontier[-1]        # ultimul nod
        self.frontier = self.frontier[:-1]
        return node


# ---------------------------------------------------------------------

class QueueFrontier(StackFrontier):
    """
    Frontieră de tip coadă (queue), folosită pentru algoritmul BFS.

    Caracteristică:
    - remove() → scoate primul element (FIFO)
    """

    def remove(self):
        """Scoate primul nod din frontieră (FIFO)."""
        if self.empty():
            raise Exception("empty frontier")
        
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node


# ---------------------------------------------------------------------

class GreedyFrontier(StackFrontier):
    """
    Frontieră pentru algoritmul Greedy Best-First Search (GBFS).

    Selectează nodul cu cea mai mică euristică h(n),
    unde h(n) = distanța Manhattan până la celula goal.
    """

    def __init__(self, maze):
        super().__init__()
        self.maze = maze

    def heuristic(self, state):
        """Distanța Manhattan până la goal."""
        r, c = state
        gr, gc = self.maze.goal
        return abs(r - gr) + abs(c - gc)

    def remove(self):
        """
        Scoate nodul cu cea mai mică valoare a euristicii h(n).
        """
        if self.empty():
            raise Exception("empty frontier")

        # presupunem că primul este cel mai bun
        best_index = 0
        best_h = self.heuristic(self.frontier[0].state)

        # căutăm nodul cu h minim
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
    Frontieră pentru algoritmul A*.

    Selectează nodul cu valoarea minimă a funcției:
        f(n) = g(n) + h(n)

    - g(n): costul (număr de pași) de la start la nodul n
    - h(n): distanța Manhattan până la goal
    """

    def g(self, node):
        """Calculează g(n) urcând prin părinți până la start."""
        cost = 0
        current = node

        while current.parent is not None:
            cost += 1
            current = current.parent

        return cost

    def f(self, node):
        """Funcția de evaluare A*: f(n) = g(n) + h(n)."""
        return self.g(node) + self.heuristic(node.state)

    def remove(self):
        """
        Scoate nodul cu cea mai mică valoare a funcției f(n).
        """
        if self.empty():
            raise Exception("empty frontier")

        best_index = 0
        best_f = self.f(self.frontier[0])

        # căutăm nodul cu f minim
        for i in range(len(self.frontier)):
            f_value = self.f(self.frontier[i])
            if f_value < best_f:
                best_f = f_value
                best_index = i

        node = self.frontier[best_index]
        self.frontier.pop(best_index)
        return node
