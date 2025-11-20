import random
from rich.progress import Progress
import sys
import copy

argumentos = sys.argv


class Labyrinth:

    def __init__(
        self, rows: int, columns: int, debug: bool = False
    ):  # Constructor del objeto laberinto

        self.DEBUG: bool = debug
        self.resuelto: bool = False
        self.imposible_to_solve: bool = False
        self.rows: int = rows
        self.columns: int = columns
        self.grid: list[list[Casilla]] = []

        for n in range(rows):

            self.grid.append([])

            for m in range(columns):

                self.grid[n].append(Casilla(n, m))

        self.start: Start | None = None
        self.goal: Meta | None = None
        self.player: Player | None = None

        self.bricks: list[tuple[int, int]] = []
        self.path: list[tuple[int, int]] = []
        self.explored: list[tuple[int, int]] = []
        self.decision_positions: list[tuple[int, int]] = []

    def set_start(
        self, position_y: int, position_x: int
    ):  # Agrega una instancia del objeto Start al laberinto siguiendo unos parámetros definidos

        if (position_y, position_x) in self.bricks:

            print(
                f"La posición ({position_y},{position_x}) está ocupada por un muro. Selecciona otra posición para la casilla de inicio."
            )

        elif not self.goal == None:

            if self.goal.position == (position_y, position_x):

                print(
                    f"La posición ({position_y},{position_x}) está ocupada por la meta. Selecciona otra posición para la casilla de inicio."
                )

        else:

            self.start: Start = Start(position_y, position_x)
            self.player: Player = Player(position_y, position_x)

            self.grid[position_y][position_x].set_estado_a("start")
            self.grid[position_y][position_x].explored = True
            self.grid[position_y][position_x].peso = 0

    def set_corner_start(
        self,
    ):  # Agrega una instancia del objeto Start al laberinto siguiendo unos parámetros definidos

        position_y: int = 0
        position_x: int = 0

        if (position_y, position_x) in self.bricks:

            print(
                f"La posición ({position_y},{position_x}) está ocupada por un muro. Selecciona otra posición para la casilla de inicio."
            )

        elif not self.goal == None:

            if self.goal.position == (position_y, position_x):

                print(
                    f"La posición ({position_y},{position_x}) está ocupada por la meta. Selecciona otra posición para la casilla de inicio."
                )

        else:

            self.start: int = Start(position_y, position_x)
            self.player: int = Player(position_y, position_x)

            self.grid[position_y][position_x].set_estado_a("start")
            self.grid[position_y][position_x].explored = True
            self.grid[position_y][position_x].peso = 0

    def set_random_start(
        self,
    ):  # Agrega una instancia del objeto Start al laberinto en una posición aleatoria

        if not self.goal == None:

            position_y: int = random.choice(range(self.rows))
            position_x: int = random.choice(range(self.columns))

            while (position_y, position_x) in self.bricks or (
                position_y,
                position_x,
            ) == self.goal.position:

                position_y = random.choice(range(self.rows))
                position_x = random.choice(range(self.columns))

        else:

            position_y: int = random.choice(range(self.rows))
            position_x: int = random.choice(range(self.columns))

            while (position_y, position_x) in self.bricks:

                position_y = random.choice(range(self.rows))
                position_x = random.choice(range(self.columns))

        self.start = Start(position_y, position_x)
        self.player = Player(position_y, position_x)

        self.grid[position_y][position_x].set_estado_a("start")
        self.grid[position_y][position_x].explored = True
        self.grid[position_y][position_x].peso = 0

    def set_goal(
        self, position_y: int, position_x: int
    ):  # Agrega una instancia del objeto Meta al laberinto siguiendo unos parámetros definidos

        if (position_y, position_x) in self.bricks:

            print(
                f"La posición ({position_y},{position_x}) está ocupada por un muro. Selecciona otra posición para la casilla de meta."
            )

        elif not self.goal == None:

            if self.goal.position == (position_y, position_x):

                print(
                    f"La posición ({position_y},{position_x}) está ocupada por la meta. Selecciona otra posición para la casilla de inicio."
                )

        else:

            self.goal = Meta(position_y, position_x)

    def set_corner_goal(
        self,
    ):  # Agrega una instancia del objeto Meta al laberinto en la esquina inferior derecha

        position_y: int = self.rows - 1
        position_x: int = self.columns - 1

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

        if not self.start == None:

            position_y: int = random.choice(range(self.rows))
            position_x: int = random.choice(range(self.columns))

            while (position_y, position_x) in self.bricks or (
                position_y,
                position_x,
            ) == self.start.position:

                position_y = random.choice(range(self.rows))
                position_x = random.choice(range(self.columns))

        else:

            position_y: int = random.choice(range(self.rows))
            position_x: int = random.choice(range(self.columns))

            while (position_y, position_x) in self.bricks:

                position_y = random.choice(range(self.rows))
                position_x = random.choice(range(self.columns))

        self.goal = Meta(position_y, position_x)

    def print_lab(self, estados: list[str]):  # Saca por pantalla el laberinto

        self.__actualizar_todos__()
        print("________________________")

        for n in range(len(self.grid)):

            for m in range(len(self.grid[n])):

                if self.grid[n][m].estado in estados:

                    print(self.grid[n][m].symbol, end="")

                else:

                    print("⬜", end="")

            print("")

        print("________________________")

    def __get_lab_weights__(
        self,
    ) -> list[
        list[int]
    ]:  # Devuelve una lista de dos dimensiones con los pesos de cada casilla

        weights: list[list[int]] = []

        for n in range(len(self.grid)):

            fila: list[int] = []

            for m in range(len(self.grid[n])):

                fila.append(self.grid[n][m].peso)

            weights.append(fila)

        return weights

    def print_lab_weights(
        self,
    ):  # Saca por pantalla los valores de peso de cada casilla

        weights: list[list[int]] = self.__get_lab_weights__()
        print("________________________")

        for n in range(len(weights)):

            for m in range(len(weights[n])):

                if len(str(weights[n][m])) == 1:

                    print(f" {weights[n][m]}", end=" ")

                else:
                    print(weights[n][m], end=" ")

            print("")

        print("________________________")

    def __get_gpt_bricks__(
        self,
    ) -> list[
        tuple[int, int]
    ]:  # Devuelve la lista de coordenadas de los muros propuestos por gpt

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

        # Asegurar que Start y meta no estén bloqueados
        ppos = getattr(self, "start", None)
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

        bricks: list[tuple[int, int]] = []

        if not self.start == None and not self.goal == None:

            for _ in range(amount_of_bricks):

                position_y: int = random.choice(range(self.rows))
                position_x: int = random.choice(range(self.columns))

                while (
                    (position_y, position_x) == self.start.position
                    or (position_y, position_x) == self.goal.position
                    or (position_y, position_x) in bricks
                ):

                    position_y = random.choice(range(self.rows))
                    position_x = random.choice(range(self.columns))

                bricks.append((position_y, position_x))

        elif not self.start == None:

            for _ in range(amount_of_bricks):

                position_y: int = random.choice(range(self.rows))
                position_x: int = random.choice(range(self.columns))

                while (position_y, position_x) == self.start.position or (
                    position_y,
                    position_x,
                ) in bricks:

                    position_y = random.choice(range(self.rows))
                    position_x = random.choice(range(self.columns))

                bricks.append((position_y, position_x))

        elif not self.goal == None:

            for _ in range(amount_of_bricks):

                position_y: int = random.choice(range(self.rows))
                position_x: int = random.choice(range(self.columns))

                while (position_y, position_x) == self.goal.position or (
                    position_y,
                    position_x,
                ) in bricks:

                    position_y = random.choice(range(self.rows))
                    position_x = random.choice(range(self.columns))

                bricks.append((position_y, position_x))

        else:

            for _ in range(amount_of_bricks):

                position_y: int = random.choice(range(self.rows))
                position_x: int = random.choice(range(self.columns))

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

        bricks: list[tuple[int, int]] = []

        if not self.start == None and not self.goal == None:

            bricks = self.__get_gpt_bricks__()

            while self.start.position in bricks or self.goal.position in bricks:

                bricks = self.__get_gpt_bricks__()

        elif not self.start == None:

            bricks = self.__get_gpt_bricks__()

            while self.start.position in bricks:

                bricks = self.__get_gpt_bricks__()

        elif not self.goal == None:

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

        bricks: list[tuple[int, int]] = [
            (len(self.grid) - 2, 0),
            (len(self.grid) - 1, 1),
        ]

        if not self.start == None:

            if self.start.position in bricks:

                print("Uno de los muros se encuentra en la casilla de inicio. ...")

            elif self.goal.position in bricks:

                print("Uno de los muros se encuentra en la casilla de meta. ...")

            else:

                self.bricks = bricks
                self.__actualizar_bricks__()

        else:

            self.bricks = bricks
            self.__actualizar_bricks__()

    def __actualizar_bricks__(self):  # Actualiza todas las casillas de muros

        progreso_actual: int = 0
        total_bricks: int = len(self.bricks)

        if self.DEBUG:

            progress: Progress = Progress()
            progress.start()
            task = progress.add_task(
                "[magenta]Actualizando muros...", total=total_bricks
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

    def __actualizar__(
        self, coord_y: int, coord_x: int
    ):  # Actualiza una casilla sabiendo sus coordenadas

        if not self.start == None:

            if (coord_y, coord_x) == self.start.position:

                self.grid[coord_y][coord_x].set_estado_a("start")
                self.grid[coord_y][coord_x].symbol = self.grid[coord_y][
                    coord_x
                ].symbols["start"]

        if not self.goal == None:

            if (coord_y, coord_x) == self.goal.position:

                self.grid[coord_y][coord_x].set_estado_a("goal")
                self.grid[coord_y][coord_x].symbol = self.grid[coord_y][
                    coord_x
                ].symbols["goal"]

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

        progreso_actual: int = 0
        total_tiles: int = self.rows * self.columns

        if self.DEBUG:

            progress: Progress = Progress()
            progress.start()
            task = progress.add_task(
                "[magenta]Actualizando casillas...", total=total_tiles
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

        pesos: list[int] = []
        directions: list[tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for n in range(len(directions)):

            coord_y_prime: int = coord_y + directions[n][0]
            coord_x_prime: int = coord_x + directions[n][1]

            if 0 <= coord_y_prime < self.rows and 0 <= coord_x_prime < self.columns:

                if not self.grid[coord_y_prime][coord_x_prime].peso == -1:

                    pesos.append(self.grid[coord_y_prime][coord_x_prime].peso)

        return pesos

    def __nuevo_peso__(
        self, coord_y: int, coord_x: int
    ) -> (
        int
    ):  # Devuelve el nuevo peso de una casilla a partir del peso de las contiguas

        if len(self.__get_sorrounding_weights__(coord_y, coord_x)) > 0:

            if max(self.__get_sorrounding_weights__(coord_y, coord_x)) >= 0:

                return max(self.__get_sorrounding_weights__(coord_y, coord_x)) + 1

            else:

                return -1

        else:

            return -1

    def __tiles_player_can_advance__(
        self,
    ) -> list[
        tuple[int, int]
    ]:  # Devuelve las casillas a las que se puede mover self.player

        directions: list[tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        possible: list[tuple[int, int]] = []

        for direction in directions:
            coord_y: int = self.player.position[0] + direction[0]
            coord_x: int = self.player.position[1] + direction[1]

            # límites correctos
            if (
                (0 <= coord_y < self.rows and 0 <= coord_x < self.columns)
                and (self.grid[coord_y][coord_x].peso == -1)
                and (not (coord_y, coord_x) in self.bricks)
                and (not self.grid[coord_y][coord_x].estado == "explored")
            ):

                possible.append((coord_y, coord_x))

        return possible

    def bfs_weights(self):  # Otorga valores de peso a todas las casillas

        count: int = 0
        total_tiles: int = (self.rows * self.columns) - len(self.bricks) - 2

        weights: list[list[int]] = self.__get_lab_weights__()
        self.grid[self.start.position[0]][self.start.position[1]].peso = 0
        peso_actual: int = 1

        if self.DEBUG:

            progress: Progress = Progress()
            progress.start()
            task = progress.add_task(
                "[cyan]Otorgando pesos...", total=total_tiles, completed=count
            )

        while count < total_tiles and not self.resuelto and not self.imposible_to_solve:

            weights: list[tuple[int, int]] = self.__get_lab_weights__()

            for n in range(len(self.grid)):

                for m in range(len(self.grid[n])):

                    if (
                        (self.__nuevo_peso__(n, m) == peso_actual)
                        and (not self.grid[n][m].estado == "brick")
                        and (self.grid[n][m].peso == -1)
                    ):

                        self.grid[n][m].peso = peso_actual
                        self.grid[n][m].explored = True
                        self.grid[n][m].set_estado_a("explored")

                        count += 1

            if self.DEBUG:

                progress.update(task, completed=count)  # Actualiza la barra

            peso_actual += 1

            self.__actualizar_resuelto__()

            if weights == self.__get_lab_weights__():

                self.imposible_to_solve = True

        if self.DEBUG:

            progress.stop()

            print(
                f"Se han otorgado los pesos a {count} casillas del total {(self.rows * self.columns) - len(self.bricks) - 2}."
            )

    def __actualizar_resuelto__(self) -> bool:

        self.resuelto = (
            not self.grid[self.goal.position[0]][self.goal.position[1]].peso == -1
        )

    def __advance__(
        self,
    ) -> (
        bool
    ):  # Cambia la posición del jugador a la casilla a la que puede avanzar, y si no puede avanzar a las casillas contiguas, la manda a la última casilla en decision_positions[]

        possible: list[tuple[int, int]] = self.__tiles_player_can_advance__()

        if len(possible) > 0:

            if len(possible) > 1:

                if type(self.player.position) == list:

                    current_pos: tuple[int, int] = self.player.position

                else:

                    current_pos: tuple[int, int] = (
                        self.player.position[0],
                        self.player.position[1],
                    )

                self.decision_positions.append(current_pos)

            new_coords: tuple[int, int] = possible[0]
            self.player.position = new_coords

            self.grid[new_coords[0]][new_coords[1]].set_estado_a("explored")
            self.grid[new_coords[0]][new_coords[1]].explored = True

            self.grid[new_coords[0]][new_coords[1]].peso = self.__nuevo_peso__(
                new_coords[0], new_coords[1]
            )

            self.explored.append((new_coords[0], new_coords[1]))
            self.__actualizar__(new_coords[0], new_coords[1])

        else:

            if not len(self.decision_positions) == 0:

                coords: tuple[int, int] = self.decision_positions.pop()
                self.player.position = coords

                if not self.grid[coords[0]][coords[1]].explored:

                    self.grid[coords[0]][coords[1]].set_estado_a("explored")
                    self.grid[coords[0]][coords[1]].explored = True
                    self.grid[coords[0]][coords[1]].peso = (
                        min(self.__get_sorrounding_weights__(coords[0], coords[1])) + 1
                    )
                    self.explored.append(coords)
                    self.__actualizar__(coords[0], coords[1])

            else:

                self.imposible_to_solve = True

        self.__actualizar_resuelto__()

    def dfs_weights(self):

        self.decision_positions: list[tuple[int, int]] = []

        if len(self.__tiles_player_can_advance__()) > 1:

            self.decision_positions.append(
                (self.start.position[0], self.start.position[1])
            )

        if self.DEBUG:

            count: int = 0
            total_tiles: int = (self.rows * self.columns) - len(self.bricks) - 2

            progress: Progress = Progress()
            progress.start()
            task = progress.add_task(
                "[cyan]Explorando...", total=total_tiles, completed=count
            )

        while not self.resuelto and not self.imposible_to_solve:

            self.__advance__()

            if self.DEBUG:

                progress.update(task, completed=count)  # Actualiza la barra

                count = len(self.explored)

        if self.DEBUG:

            progress.stop()

            print(
                f"Se han otorgado los pesos a {count} casillas del total {total_tiles}."
            )

    def set_path(
        self,
    ):  # Define las casillas conforman el trayecto más corto entre la posición del jugador y la posición de meta

        if self.resuelto:

            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            next_path = [self.goal.position[0], self.goal.position[1]]

            for _ in range(
                self.grid[self.goal.position[0]][self.goal.position[1]].peso + 1
            ):

                end = False

                while not self.grid[next_path[0]][next_path[1]].peso == 1 and not end:

                    found = False
                    n = 0

                    while not found and n < len(directions):

                        coord_y = next_path[0] + directions[n][0]
                        coord_x = next_path[1] + directions[n][1]

                        if (
                            (0 <= coord_y < self.rows)
                            and (0 <= coord_x < self.columns)
                            and (
                                self.grid[coord_y][coord_x].peso
                                == self.grid[next_path[0]][next_path[1]].peso - 1
                            )
                        ):

                            next_path = [coord_y, coord_x]
                            self.grid[coord_y][coord_x].set_estado_a("path")
                            found = True
                            self.__actualizar__(next_path[0], next_path[1])

                        n += 1

                    if not found:

                        end = True

        else:

            print("No existe un camino posible.")

    def printResult(self):  # Saca pro pantalla el resultado de la búsqueda

        if self.resuelto:

            self.set_path()  # Define el camino óptimo a partir de los valores de peso
            self.print_lab(
                ["path", "brick", "start", "goal", "explored"]
            )  # Suelta el laberinto por pantalla

        else:

            self.print_lab(
                ["brick", "start", "goal", "explored"]
            )  # Suelta el laberinto por pantalla


class Casilla:

    def __init__(
        self, position_y: int, position_x: int, estado="blank"
    ):  # Constructor del objeto Casilla

        self.symbols: dict = {
            "start": "🟦",
            "goal": "🟩",
            "brick": "⬛",
            "blank": "⬜",
            "path": "🟥",
            "explored": "🟧",
        }

        self.position: list[int, int] = [position_y, position_x]
        self.set_estado_a("blank")
        self.set_estado_a(estado)
        self.peso: int = -1
        self.symbol: str = self.symbols[estado]
        self.explored: bool = False

    def set_estado_a(
        self, new_estado: str
    ):  # Define el estado de la casilla, ya sea la casilla de inicio del Start, la casilla de meta, un muro, una casilla vacía, o una casilla que forma parte del camino óptimo

        if new_estado in self.symbols.keys():

            self.estado: str = new_estado
            self.symbol: str = self.symbols[new_estado]

        else:

            print(f"El estado {new_estado} no existe.")


class Start:

    def __init__(
        self, position_y: int, position_x: int
    ):  # Contructor de la clase Start

        self.position: tuple[int, int] = (position_y, position_x)


class Meta:

    def __init__(
        self, position_y: int, position_x: int
    ):  # Constructor de la clase Meta

        self.position: tuple[int, int] = (position_y, position_x)


class Player:

    def __init__(
        self, position_y: int, position_x: int
    ):  # Constructor de la clase Player

        self.position: tuple[int, int] = [position_y, position_x]


if __name__ == "__main__":

    lab: Labyrinth = Labyrinth(50, 150, True)  # Crea un laberinto

    lab.set_gpt_bricks()
    lab.set_random_start()  # Define una posición para la casilla de inicio del Start
    lab.set_random_goal()  # Define una posición para la casilla de meta

    if len(argumentos) == 1:

        choice: str = input("Indica el método que desee (dfs, bfs, both): ")

    else:

        choice: str = argumentos[1]

    if choice == "dfs":

        lab.dfs_weights()  # Otorga valores de peso según el algoritmo de búsqueda dfs
        lab.printResult()

    elif choice == "bfs":

        lab.bfs_weights()  # Otorga valores de peso según el algoritmo de búsqueda dfs
        lab.printResult()

    elif choice == "both":

        lab1 = copy.deepcopy(lab)
        lab2 = copy.deepcopy(lab)

        print(
            "-------------------------------------------- BFS --------------------------------------------"
        )
        lab1.bfs_weights()  # Otorga valores de peso según el algoritmo de búsqueda dfs
        lab1.printResult()

        print(
            "-------------------------------------------- DFS --------------------------------------------"
        )
        lab2.dfs_weights()
        lab2.printResult()
