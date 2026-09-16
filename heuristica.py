
from __future__ import annotations

from arbol_juego import Tablero, obtener_ganador


VALOR_VICTORIA = 1
VALOR_EMPATE = 0
VALOR_DERROTA = -1



def evaluar_estado(tablero: Tablero, jugador_max: str) -> int:
    ganador = obtener_ganador(tablero)

    if ganador is None:

        return VALOR_EMPATE

    if ganador == jugador_max:
        return VALOR_VICTORIA

    return VALOR_DERROTA
