
from __future__ import annotations

import networkx


# El tablero contiene tres filas de tres posiciones: "X", "O" o un espacio vacío.
Tablero = tuple[tuple[str, str, str], tuple[str, str, str], tuple[str, str, str]]
Coordenada = tuple[int, int]

JUGADOR_X = "X"
JUGADOR_O = "O"
CASILLA_VACIA = " "

# Coordenadas de las filas, columnas y diagonales que pueden producir una victoria.
LINEAS_GANADORAS = (
    ((0, 0), (0, 1), (0, 2)),  # Fila superior
    ((1, 0), (1, 1), (1, 2)),  # Fila central
    ((2, 0), (2, 1), (2, 2)),  # Fila inferior
    ((0, 0), (1, 0), (2, 0)),  # Columna izquierda
    ((0, 1), (1, 1), (2, 1)),  # Columna central
    ((0, 2), (1, 2), (2, 2)),  # Columna derecha
    ((0, 0), (1, 1), (2, 2)),  # Diagonal principal
    ((0, 2), (1, 1), (2, 0)),  # Diagonal secundaria
)


# Crea la raíz cuando la partida todavía no tiene movimientos.
def crear_tablero_vacio() -> Tablero:
    fila_vacia = (CASILLA_VACIA,) * 3
    return (fila_vacia, fila_vacia, fila_vacia)


# Calcula el turno contando las fichas que ya existen en el tablero.
def obtener_jugador_actual(tablero: Tablero) -> str:
    cantidad_x = sum(fila.count(JUGADOR_X) for fila in tablero)
    cantidad_o = sum(fila.count(JUGADOR_O) for fila in tablero)
    return JUGADOR_X if cantidad_x == cantidad_o else JUGADOR_O


# Devuelve las coordenadas de las casillas en las que todavía se puede jugar.
def obtener_jugadas_legales(tablero: Tablero) -> list[Coordenada]:
    return [
        (fila, columna)
        for fila in range(3)
        for columna in range(3)
        if tablero[fila][columna] == CASILLA_VACIA
    ]


# Crea un tablero hijo sin modificar el tablero del que salió la jugada.
def aplicar_jugada(tablero: Tablero, jugada: Coordenada) -> Tablero:
    if jugada not in obtener_jugadas_legales(tablero):
        raise ValueError("La jugada debe corresponder a una casilla vacía.")

    jugador_actual = obtener_jugador_actual(tablero)
    fila, columna = jugada
    filas_nuevas = [list(fila_actual) for fila_actual in tablero]
    filas_nuevas[fila][columna] = jugador_actual
    return tuple(tuple(fila_actual) for fila_actual in filas_nuevas)  # type: ignore[return-value]


# Revisa las ocho líneas y devuelve el símbolo ganador cuando existe.
def obtener_ganador(tablero: Tablero) -> str | None:
    for (fila_a, columna_a), (fila_b, columna_b), (fila_c, columna_c) in LINEAS_GANADORAS:
        simbolo = tablero[fila_a][columna_a]
        if (
            simbolo != CASILLA_VACIA
            and simbolo == tablero[fila_b][columna_b] == tablero[fila_c][columna_c]
        ):
            return simbolo
    return None


# Una rama termina cuando alguien gana o cuando ya no quedan movimientos.
def es_terminal(tablero: Tablero) -> bool:
    return obtener_ganador(tablero) is not None or not obtener_jugadas_legales(tablero)


# Genera un tablero sucesor por cada jugada legal del estado actual.
def generar_sucesores(tablero: Tablero) -> list[tuple[Coordenada, Tablero]]:
    # Los estados terminales son hojas y no tienen sucesores.
    if es_terminal(tablero):
        return []

    sucesores: list[tuple[Coordenada, Tablero]] = []

    # La jugada se conserva junto al tablero para guardarla después en la arista.
    for jugada in obtener_jugadas_legales(tablero):
        tablero_hijo = aplicar_jugada(tablero, jugada)
        sucesores.append((jugada, tablero_hijo))

    return sucesores


# Construye recursivamente el árbol completo desde el tablero recibido.
def construir_arbol(tablero_inicial: Tablero | None = None) -> networkx.DiGraph:
    # Si no se recibe un tablero, la construcción comienza desde el tablero vacío.
    raiz = crear_tablero_vacio() if tablero_inicial is None else tablero_inicial
    grafo = networkx.DiGraph()
    estados_expandidos: set[Tablero] = set()

    # Esta función interna añade un estado y continúa con todos sus descendientes.
    def expandir(tablero: Tablero) -> None:
        # Un mismo tablero puede aparecer por distintos órdenes de jugadas.
        # Se reutiliza para evitar construir varias veces el mismo subárbol.
        if tablero in estados_expandidos:
            return
        estados_expandidos.add(tablero)

        grafo.add_node(
            tablero,
            jugador_actual=obtener_jugador_actual(tablero),
            profundidad=sum(
                casilla != CASILLA_VACIA
                for fila in tablero
                for casilla in fila
            ),
            terminal=es_terminal(tablero),
            ganador=obtener_ganador(tablero),
        )

        # Cada sucesor se convierte en un hijo conectado por su jugada.
        for jugada, tablero_hijo in generar_sucesores(tablero):
            grafo.add_edge(tablero, tablero_hijo, jugada=jugada)
            expandir(tablero_hijo)

    # La primera llamada crea la raíz y desencadena toda la recursión.
    expandir(raiz)
    grafo.graph["raiz"] = raiz
    return grafo
