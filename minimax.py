
from __future__ import annotations

import math

from arbol_juego import (
    Coordenada,
    Tablero,
    aplicar_jugada,
    es_terminal,
    obtener_jugador_actual,
    obtener_jugadas_legales,
)
from heuristica import evaluar_estado



# alfa: mejor valor que el jugador MAX tiene garantizado hasta el momento.
# beta: mejor valor que el jugador MIN tiene garantizado hasta el momento.

def minimax_alfa_beta(
    tablero: Tablero,
    jugador_max: str,
    alfa: float = -math.inf,
    beta: float = math.inf,
) -> tuple[int, Coordenada | None]:
    # Caso base:
    if es_terminal(tablero):
        return evaluar_estado(tablero, jugador_max), None

    jugador_en_turno = obtener_jugador_actual(tablero)
    es_turno_de_max = jugador_en_turno == jugador_max

    mejor_jugada: Coordenada | None = None

    if es_turno_de_max:
        # El jugador MAX quiere el valor más alto posible.
        mejor_valor = -math.inf

        for jugada in obtener_jugadas_legales(tablero):
            tablero_hijo = aplicar_jugada(tablero, jugada)
            valor_hijo, _ = minimax_alfa_beta(tablero_hijo, jugador_max, alfa, beta)

            if valor_hijo > mejor_valor:
                mejor_valor = valor_hijo
                mejor_jugada = jugada

            alfa = max(alfa, mejor_valor)
            if beta <= alfa:
        
                break

        return mejor_valor, mejor_jugada

    else:
       
        mejor_valor = math.inf

        for jugada in obtener_jugadas_legales(tablero):
            tablero_hijo = aplicar_jugada(tablero, jugada)
            valor_hijo, _ = minimax_alfa_beta(tablero_hijo, jugador_max, alfa, beta)

            if valor_hijo < mejor_valor:
                mejor_valor = valor_hijo
                mejor_jugada = jugada

            beta = min(beta, mejor_valor)
            if beta <= alfa:
                
                break

        return mejor_valor, mejor_jugada



def elegir_mejor_jugada(tablero: Tablero, jugador_max: str) -> Coordenada:
    _, jugada = minimax_alfa_beta(tablero, jugador_max)

    if jugada is None:

        raise ValueError("No hay jugadas disponibles: el tablero ya es terminal.")

    return jugada
