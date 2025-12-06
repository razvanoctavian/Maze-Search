class Maze:
    """
    Clasa Maze gestioneaza structura labirintului 

    Pornind de la un fisier text va construi:
        -self.walls: matrice bool care spune daca avem perete(nu putem trece) sau daca e liber
        -self.start: tuplu(row,col) pentru A start
        -self.goal: tuplu(row, col) pentru B goal
        -dimensiunile (self.height si self.width)
    """

    def __init__(self, filename):
        """
        Citim labirintul din fisierul dat

        Labirintul ar trebui sa fie de forma:
            -# pentru pereti
            -' ' pentru spatii libere
            - cu exact un A de start si B de goal
        
        Construim:
            -self.walls
            -self.start & self.goal
            -self.height & self.width
        """

        #citim fisierul
        with open(filename, "r") as f:
            contents = f.read()
        
        #validam start si goal
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start 'A'.")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal 'B'.")

        #separam pe linii
        lines=contents.splitlines()

        #width si height
        self.height=len(lines) #numar linii
        self.width= max(len(line) for line in lines) #cea mai lunga linie

        #initializam matricea de pereti si pozitiile de start/goal
        self.walls = []
        self.start = None
        self.goal = None

        for i in range(self.height):
            row=[]
            for j in range(self.width):
                try:
                    col = lines[i][j]
                except IndexError:
                    #daca linia e mai scurta, completam cu spatiu
                    col=" "

                if col =="A":
                    self.start=(i,j)
                    row.append(False) #nu e perete
                elif col == "B":
                    self.goal = (i,j)
                    row.append(False)
                elif col==" ":
                    row.append(False)
                else:
                    row.append(True)#perete
            
            self.walls.append(row)

    
    # ---------------------------------------------------------------------


    def neighbours(self, state):
        """
        Primeste un state (row,col)

        Returneaza vecinii accesibili ai unei stari sub forma de :
            lista de tuple (action, new_state) unde:
                *action: 'up', 'down', 'left', 'right'
                *new_state: tuplu(row,  col)
        
        O mutare e valida daca:
            -ramane in interiorul labirintului
            -nu ajunge intr un perete

        """

        row,col=state #unpack state

        candidates = [
            ("up",    (row - 1, col)),  # sus
            ("down",  (row + 1, col)),  # jos
            ("left",  (row, col - 1)),  # stanga
            ("right", (row, col + 1)),  # dreapta
        ]

        #lista de tupluri
        result = []
        for action, (r, c) in candidates:
            if (
                0 <= r < self.height and #in interval
                0 <= c < self.width and #in interval
                not self.walls[r][c] # nu e perete
            ):
                result.append((action, (r, c)))
        
        return result



