import random
from rich.progress import Progress


class Labyrinth:

    def __init__(
        self, rows: int, columns: int, debug: bool = False
    ):  # Constructor del objeto laberinto

        self.DEBUG = debug
        self.rows = rows
        self.columns = columns
        self.grid = []

        for n in range(rows):

            self.grid.append([])

            for m in range(columns):

                self.grid[n].append(Casilla(n, m))

        self.player = "Not defined"
        self.goal = "Not defined"
        self.bricks = []

        self.resuelto = False

    def set_player(
        self, position_y: int, position_x: int
    ):  # Agrega una instancia del objeto Jugador al laberinto siguiendo unos parámetros definidos

        if (position_y, position_x) in self.bricks:

            print(
                f"La posición ({position_y},{position_x}) está ocupada por un muro. Selecciona otra posición para la casilla de inicio."
            )

        elif not self.goal == "Not defined":

            if self.goal.position == (position_y, position_x):

                print(
                    f"La posición ({position_y},{position_x}) está ocupada por la meta. Selecciona otra posición para la casilla de inicio."
                )

        else:

            self.player = Jugador(position_y, position_x)

    def set_corner_player(
        self,
    ):  # Agrega una instancia del objeto Jugador al laberinto siguiendo unos parámetros definidos

        position_y = 0
        position_x = 0

        if (position_y, position_x) in self.bricks:

            print(
                f"La posición ({position_y},{position_x}) está ocupada por un muro. Selecciona otra posición para la casilla de inicio."
            )

        elif not self.goal == "Not defined":

            if self.goal.position == (position_y, position_x):

                print(
                    f"La posición ({position_y},{position_x}) está ocupada por la meta. Selecciona otra posición para la casilla de inicio."
                )

        else:

            self.player = Jugador(position_y, position_x)

    def set_random_player(
        self,
    ):  # Agrega una instancia del objeto Jugador al laberinto en una posición aleatoria

        if not self.goal == "Not defined":

            position_y: float = random.choice(range(self.rows))
            position_x = random.choice(range(self.columns))

            while (position_y, position_x) in self.bricks or (
                position_y,
                position_x,
            ) == self.goal.position:

                position_y = random.choice(range(self.rows))
                position_x = random.choice(range(self.columns))

        else:

            position_y = random.choice(range(self.rows))
            position_x = random.choice(range(self.columns))

            while (position_y, position_x) in self.bricks:

                position_y = random.choice(range(self.rows))
                position_x = random.choice(range(self.columns))

        self.player = Jugador(position_y, position_x)

    def set_goal(
        self, position_y: int, position_x: int
    ):  # Agrega una instancia del objeto Meta al laberinto siguiendo unos parámetros definidos

        if (position_y, position_x) in self.bricks:

            print(
                f"La posición ({position_y},{position_x}) está ocupada por un muro. Selecciona otra posición para la casilla de meta."
            )

        elif not self.goal == "Not defined":

            if self.goal.position == (position_y, position_x):

                print(
                    f"La posición ({position_y},{position_x}) está ocupada por la meta. Selecciona otra posición para la casilla de inicio."
                )

        else:

            self.goal = Meta(position_y, position_x)

    def set_corner_goal(
        self,
    ):  # Agrega una instancia del objeto Meta al laberinto en la esquina inferior derecha

        position_y = self.rows - 1
        position_x = self.columns - 1

        if (position_y, position_x) in self.bricks:

            print(
                f"La posición ({position_y},{position_x}) está ocupada por un muro. Selecciona otra posición para la casilla de meta."
            )

        elif not self.goal == "Not defined":

            if self.goal.position == (position_y, position_x):

                print(
                    f"La posición ({position_y},{position_x}) está ocupada por la meta. Selecciona otra posición para la casilla de inicio."
                )

        else:

            self.goal = Meta(position_y, position_x)

    def set_random_goal(
        self,
    ):  # Agrega una instancia del objeto Meta al laberinto en una posición aleatoria

        if not self.player == "Not defined":

            position_y = random.choice(range(self.rows))
            position_x = random.choice(range(self.columns))

            while (position_y, position_x) in self.bricks or (
                position_y,
                position_x,
            ) == self.player.position:

                position_y = random.choice(range(self.rows))
                position_x = random.choice(range(self.columns))

        else:

            position_y = random.choice(range(self.rows))
            position_x = random.choice(range(self.columns))

            while (position_y, position_x) in self.bricks:

                position_y = random.choice(range(self.rows))
                position_x = random.choice(range(self.columns))

        self.goal = Meta(position_y, position_x)

    def print_lab(self):  # Saca por pantalla el laberinto

        self.__actualizar_todos__()
        print("________________________")

        for n in range(len(self.grid)):

            for m in range(len(self.grid[n])):

                print(self.grid[n][m].symbol, end="")

            print("")

        print("________________________")

    def __get_lab_weights__(self) -> list[list[int]]:

        weights = [[]]

        for n in range(len(self.grid)):

            for m in range(len(self.grid[n])):

                weights[n].append(self.grid[n][m].peso)

            weights.append([])

        return weights

    def print_lab_weights(
        self,
    ):  # Saca por pantalla los valores de peso de cada casilla

        weights = self.__get_lab_weights__()
        print("________________________")

        for n in range(len(weights)):

            for m in range(len(weights[n])):

                if len(str(weights[n][m])) == 1:

                    print(f" {weights[n][m]}", end=" ")

                else:
                    print(weights[n][m], end=" ")

            print("")

        print("________________________")

    def __get_gpt_bricks__(self) -> list[tuple[int, int]]:

        rows = self.rows + 1
        cols = self.columns + 1

        maze = [[True for _ in range(cols)] for _ in range(rows)]

        # DFS para crear caminos
        start = (0, 0)
        maze[start[0]][start[1]] = False
        stack = [start]
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

        while stack:

            y, x = stack[-1]
            neighbors = []

            for dy, dx in directions:

                ny, nx = y + dy, x + dx

                if 0 <= ny < rows and 0 <= nx < cols and maze[ny][nx]:

                    neighbors.append((ny, nx, dy // 2, dx // 2))

            if neighbors:

                ny, nx, mid_dy, mid_dx = random.choice(neighbors)
                maze[y + mid_dy][x + mid_dx] = False
                maze[ny][nx] = False
                stack.append((ny, nx))

            else:

                stack.pop()

        # Asegurar que jugador y meta no estén bloqueados
        ppos = getattr(self, "player", None)
        gpos = getattr(self, "goal", None)
        ppos = (
            tuple(ppos.position) if ppos and getattr(ppos, "position", None) else (0, 0)
        )
        gpos = (
            tuple(gpos.position)
            if gpos and getattr(gpos, "position", None)
            else (rows - 1, cols - 1)
        )
        maze[ppos[0]][ppos[1]] = False
        maze[gpos[0]][gpos[1]] = False

        # Devolver lista de paredes
        bricks = [(y, x) for y in range(rows) for x in range(cols) if maze[y][x]]

        new_bricks = []

        for n in range(len(bricks)):

            if not bricks[n][0] == rows - 1 and not bricks[n][1] == cols - 1:

                new_bricks.append(bricks[n])

        bricks = new_bricks

        return bricks

    def __get_random_bricks__(
        self, amount_of_bricks: int
    ) -> list[
        tuple[int, int]
    ]:  # Devuelve una lista de tuplas con las coordenadas de los nuevos muros

        bricks = []

        if not self.player == "Not defined" and not self.goal == "Not defined":

            for _ in range(amount_of_bricks):

                position_y = random.choice(range(self.rows))
                position_x = random.choice(range(self.columns))

                while (
                    (position_y, position_x) == self.player.position
                    or (position_y, position_x) == self.goal.position
                    or (position_y, position_x) in bricks
                ):

                    position_y = random.choice(range(self.rows))
                    position_x = random.choice(range(self.columns))

                bricks.append((position_y, position_x))

        elif not self.player == "Not defined":

            for _ in range(amount_of_bricks):

                position_y = random.choice(range(self.rows))
                position_x = random.choice(range(self.columns))

                while (position_y, position_x) == self.player.position or (
                    position_y,
                    position_x,
                ) in bricks:

                    position_y = random.choice(range(self.rows))
                    position_x = random.choice(range(self.columns))

                bricks.append((position_y, position_x))

        elif not self.goal == "Not defined":

            for _ in range(amount_of_bricks):

                position_y = random.choice(range(self.rows))
                position_x = random.choice(range(self.columns))

                while (position_y, position_x) == self.goal.position or (
                    position_y,
                    position_x,
                ) in bricks:

                    position_y = random.choice(range(self.rows))
                    position_x = random.choice(range(self.columns))

                bricks.append((position_y, position_x))

        else:

            for _ in range(amount_of_bricks):

                position_y = random.choice(range(self.rows))
                position_x = random.choice(range(self.columns))

                while (position_y, position_x) in bricks:

                    position_y = random.choice(range(self.rows))
                    position_x = random.choice(range(self.columns))

                bricks.append((position_y, position_x))

        return bricks

    def set_random_bricks(
        self, amount_of_bricks: int
    ):  # Incorpora una cantidad definida de muros en el laberinto aleatoriamente

        self.bricks = self.__get_random_bricks__(amount_of_bricks)
        self.__actualizar_bricks__()

    def set_gpt_bricks(
        self,
    ):  # Incorpora una cantidad definida de muros en el laberinto aleatoriamente

        bricks = []

        if not self.player == "Not defined" and not self.goal == "Not defined":

            bricks = self.__get_gpt_bricks__()

            while self.player.position in bricks or self.goal.position in bricks:

                bricks = self.__get_gpt_bricks__()

        elif not self.player == "Not defined":

            bricks = self.__get_gpt_bricks__()

            while self.player.position in bricks:

                bricks = self.__get_gpt_bricks__()

        elif not self.goal == "Not defined":

            bricks = self.__get_gpt_bricks__()

            while self.goal.position in bricks:

                bricks = self.__get_gpt_bricks__()

        else:

            bricks = self.__get_gpt_bricks__()

        self.bricks = bricks
        self.__actualizar_bricks__()

    def set_corner_bricks(
        self,
    ):  # Incorpora únicamente dos muros que cierran la esquina inferior izquierda

        bricks = [(3, 0), (4, 1)]

        if self.player.position in bricks:

            print(
                f"Uno de los muros se encuentra en la casilla de inicio. Selecciona otros muros."
            )

        elif self.goal.position in bricks:

            print(
                f"Uno de los muros se encuentra en la casilla de meta. Selecciona otros muros."
            )

        else:

            self.bricks = bricks
            self.__actualizar_bricks__()

    def __actualizar_bricks__(self):

        total_muros = len(self.bricks)
        progreso_actual = 0

        if self.DEBUG:

            progress = Progress()
            progress.start()
            task = progress.add_task(
                "[magenta]Actualizando muros...", total=total_muros
            )

        for coords in self.bricks:

            self.__actualizar__(coords[0], coords[1])

            if self.DEBUG:

                progreso_actual += 1
                progress.update(task, completed=progreso_actual)

        if self.DEBUG:

            progress.stop()

    def delete_bricks(self):  # Elimina todos los muros

        self.bricks.clear()
        self.__actualizar_todos__()

    def __actualizar__(self, coord_y: int, coord_x: int):

        if not self.player == "Not defined":

            if (coord_y, coord_x) == self.player.position:

                self.grid[coord_y][coord_x].set_estado_a("player")
                self.grid[coord_y][coord_x].symbol = self.grid[coord_y][
                    coord_x
                ].symbols["player"]

        if not self.goal == "Not defined":

            if (coord_y, coord_x) == self.goal.position:

                self.grid[coord_y][coord_x].set_estado_a("meta")
                self.grid[coord_y][coord_x].symbol = self.grid[coord_y][
                    coord_x
                ].symbols["meta"]

        if self.grid[coord_y][coord_x].estado == "path":

            self.grid[coord_y][coord_x].symbol = self.grid[coord_y][coord_x].symbols[
                "path"
            ]

        if (coord_y, coord_x) in self.bricks:

            self.grid[coord_y][coord_x].set_estado_a("brick")
            self.grid[coord_y][coord_x].symbol = self.grid[coord_y][coord_x].symbols[
                "brick"
            ]

    def __actualizar_todos__(self):  # Actualiza todas las casillas según su estado

        total_casillas = self.rows * self.columns
        progreso_actual = 0

        if self.DEBUG:

            progress = Progress()
            progress.start()
            task = progress.add_task(
                "[magenta]Actualizando casillas...", total=total_casillas
            )

        for n in range(len(self.grid)):

            for m in range(len(self.grid[n])):

                self.__actualizar__(n, m)

                if self.DEBUG:

                    progreso_actual += 1
                    progress.update(task, completed=progreso_actual)

        if self.DEBUG:

            progress.stop()

    def __get_sorrounding_weights__(
        self, coord_y: int, coord_x: int
    ) -> list[
        int
    ]:  # Devuelve una lista de enteros correspondientes a los pesos de las casillas contiguas a una en coordenadas definidas

        pesos = []
        direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for n in range(len(direcciones)):

            if not (
                (n == 0 and coord_y == self.rows - 1)
                or (n == 1 and coord_y == 0)
                or (n == 2 and coord_x == self.columns - 1)
                or (n == 3 and coord_x == 0)
            ):

                pesos.append(
                    self.grid[coord_y + direcciones[n][0]][
                        coord_x + direcciones[n][1]
                    ].peso
                )

        return pesos

    def __nuevo_peso__(
        self, coord_y: int, coord_x: int
    ) -> (
        int
    ):  # Devuelve el nuevo peso de una casilla a partir del peso de las contiguas

        if max(self.__get_sorrounding_weights__(coord_y, coord_x)) >= 0:

            return max(self.__get_sorrounding_weights__(coord_y, coord_x)) + 1

        else:

            return -1

    def set_all_weights(self):  # Otorga valores de peso a todas las casillas

        count = 0
        weights = self.__get_lab_weights__()
        self.grid[self.player.position[0]][self.player.position[1]].peso = 0
        peso_actual = 1
        total = (self.rows * self.columns) - len(self.bricks) - 2

        if self.DEBUG:

            progress = Progress()
            progress.start()
            task = progress.add_task(
                "[cyan]Otorgando pesos...", total=total, completed=count
            )

        while (
            count < total
            and self.grid[self.goal.position[0]][self.goal.position[1]].peso == -1
            and not weights == self.__get_lab_weights__()
        ):

            weights = self.__get_lab_weights__()

            for n in range(len(self.grid)):

                for m in range(len(self.grid[n])):

                    if (
                        (self.__nuevo_peso__(n, m) == peso_actual)
                        and (not self.grid[n][m].estado == "brick")
                        and (self.grid[n][m].peso == -1)
                    ):

                        self.grid[n][m].peso = peso_actual

                        count += 1

            if self.DEBUG:

                progress.update(task, completed=count)  # Actualiza la barra

            peso_actual += 1

        if self.DEBUG:

            progress.stop()

            print(f"Se han otorgado los pesos a {count} casillas del total {total}.")

        self.resuelto = (
            not self.grid[self.goal.position[0]][self.goal.position[1]].peso == -1
        )

    def set_paths(
        self,
    ):  # Define las casillas conforman el trayecto más corto entre la posición del jugador y la posición de meta

        if not self.grid[self.goal.position[0]][self.goal.position[1]].peso == -1:

            direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            next_path = [self.goal.position[0], self.goal.position[1]]

            for _ in range(
                self.grid[self.goal.position[0]][self.goal.position[1]].peso + 1
            ):

                self.grid[next_path[0]][next_path[1]].set_estado_a("path")

                while not self.grid[next_path[0]][next_path[1]].peso == 1:

                    found = False
                    n = 0

                    while not found:

                        if (
                            not (
                                (n == 0 and next_path[0] == self.rows - 1)
                                or (n == 1 and next_path[0] == 0)
                                or (n == 2 and next_path[1] == self.columns - 1)
                                or (n == 3 and next_path[1] == 0)
                            )
                        ) and (
                            self.grid[next_path[0] + direcciones[n][0]][
                                next_path[1] + direcciones[n][1]
                            ].peso
                            == self.grid[next_path[0]][next_path[1]].peso - 1
                        ):

                            next_path = [
                                next_path[0] + direcciones[n][0],
                                next_path[1] + direcciones[n][1],
                            ]
                            self.grid[next_path[0]][next_path[1]].set_estado_a("path")
                            found = True
                            self.__actualizar__(next_path[0], next_path[1])

                        n += 1

        else:

            print("No existe un camino posible.")

            for n in range(len(self.grid)):

                for m in range(len(self.grid[n])):

                    if self.grid[n][m].peso >= 1:

                        self.grid[n][m].set_estado_a("rango")
                        self.__actualizar__(n, m)


class Casilla:

    def __init__(
        self, position_y: int, position_x: int, estado="blank"
    ):  # Constructor del objeto Casilla

        self.symbols = {
            "player": "🟦",
            "meta": "🟩",
            "brick": "⬛",
            "blank": "⬜",
            "path": "🟥",
            "rango": "🟧",
        }
        self.position = [position_y, position_x]
        self.set_estado_a("blank")
        self.set_estado_a(estado)
        self.peso = -1
        self.symbol = self.symbols[estado]

    def set_estado_a(
        self, new_estado: str
    ):  # Define el estado de la casilla, ya sea la casilla de inicio del jugador, la casilla de meta, un muri, una casilla vacía, o una casilla que forma parte del camino óptimo

        if new_estado in self.symbols.keys():

            self.estado = new_estado
            self.symbol = self.symbols[new_estado]

        else:

            print(f"El estado {new_estado} no existe.")


class Jugador:

    def __init__(self, position_y=0, position_x=0):  # Contructor de la clase Jugador

        self.position = (position_y, position_x)


class Meta:

    def __init__(self, position_y=0, position_x=0):  # Constructor de la clase Meta

        self.position = (position_y, position_x)


if __name__ == "__main__":

    # lab = Labyrinth(int(input("Inserte el número de filas que desee: ")),int(input("Inserte el número de columnas que desee: ")),True) # Crea un laberinto
    lab = Labyrinth(100, 300, True)  # Crea un laberinto

    lab.set_gpt_bricks()  # Coloca 50 muros en el laberinto
    lab.set_random_player()  # Define una posición para la casilla de inicio del jugador
    lab.set_random_goal()  # Define una posición para la casilla de meta
    lab.set_all_weights()  # Otorga valores de peso a todas las casillas
    lab.set_paths()  # Define el camino óptimo a partir de los valores de peso
    lab.print_lab()  # Suelta el laberinto por pantalla
