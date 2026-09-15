
from __future__ import annotations

import networkx


# El tablero tiene nueve posiciones: "X", "O" o un espacio vacío.
Tablero = tuple[str, ...]

JUGADOR_X = "X"
JUGADOR_O = "O"
CASILLA_VACIA = " "

# Índices de las filas, columnas y diagonales que pueden producir una victoria.
LINEAS_GANADORAS = (
    (0, 1, 2),  # Fila superior
    (3, 4, 5),  # Fila central
    (6, 7, 8),  # Fila inferior
    (0, 3, 6),  # Columna izquierda
    (1, 4, 7),  # Columna central
    (2, 5, 8),  # Columna derecha
    (0, 4, 8),  # Diagonal principal
    (2, 4, 6),  # Diagonal secundaria
)


# Crea la raíz cuando la partida todavía no tiene movimientos.
def crear_tablero_vacio() -> Tablero:
    return (CASILLA_VACIA,) * 9


# Calcula el turno contando las fichas que ya existen en el tablero.
def obtener_jugador_actual(tablero: Tablero) -> str:
    cantidad_x = tablero.count(JUGADOR_X)
    cantidad_o = tablero.count(JUGADOR_O)
    return JUGADOR_X if cantidad_x == cantidad_o else JUGADOR_O


# Devuelve los índices de las casillas en las que todavía se puede jugar.
def obtener_jugadas_legales(tablero: Tablero) -> list[int]:
    return [
        posicion
        for posicion, casilla in enumerate(tablero)
        if casilla == CASILLA_VACIA
    ]


# Crea un tablero hijo sin modificar el tablero del que salió la jugada.
def aplicar_jugada(tablero: Tablero, posicion: int) -> Tablero:
    if posicion not in obtener_jugadas_legales(tablero):
        raise ValueError("La jugada debe corresponder a una casilla vacía.")

    jugador_actual = obtener_jugador_actual(tablero)
    return tablero[:posicion] + (jugador_actual,) + tablero[posicion + 1 :]


# Revisa las ocho líneas y devuelve el símbolo ganador cuando existe.
def obtener_ganador(tablero: Tablero) -> str | None:
    for posicion_a, posicion_b, posicion_c in LINEAS_GANADORAS:
        simbolo = tablero[posicion_a]
        if simbolo != CASILLA_VACIA and simbolo == tablero[posicion_b] == tablero[posicion_c]:
            return simbolo
    return None


# Una rama termina cuando alguien gana o cuando ya no quedan movimientos.
def es_terminal(tablero: Tablero) -> bool:
    return obtener_ganador(tablero) is not None or not obtener_jugadas_legales(tablero)


# Genera un tablero sucesor por cada jugada legal del estado actual.
def generar_sucesores(tablero: Tablero) -> list[tuple[int, Tablero]]:
    # Los estados terminales son hojas y no tienen sucesores.
    if es_terminal(tablero):
        return []

    sucesores: list[tuple[int, Tablero]] = []

    # La jugada se conserva junto al tablero para guardarla después en la arista.
    for posicion in obtener_jugadas_legales(tablero):
        tablero_hijo = aplicar_jugada(tablero, posicion)
        sucesores.append((posicion, tablero_hijo))

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
            profundidad=9 - tablero.count(CASILLA_VACIA),
            terminal=es_terminal(tablero),
            ganador=obtener_ganador(tablero),
        )

        # Cada sucesor se convierte en un hijo conectado por su jugada.
        for posicion, tablero_hijo in generar_sucesores(tablero):
            grafo.add_edge(tablero, tablero_hijo, jugada=posicion)
            expandir(tablero_hijo)

    # La primera llamada crea la raíz y desencadena toda la recursión.
    expandir(raiz)
    grafo.graph["raiz"] = raiz
    return grafo
