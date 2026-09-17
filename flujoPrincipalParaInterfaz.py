from __future__ import annotations

import random
from arbol_juego import (
    JUGADOR_O,
    JUGADOR_X,
    Coordenada,
    Tablero,
    aplicar_jugada,
    crear_tablero_vacio,
    es_terminal,
    obtener_ganador,
    obtener_jugador_actual,
    obtener_jugadas_legales,
)
from minimax import elegir_mejor_jugada


def crear_estado_juego() -> dict:
    tablero = crear_tablero_vacio()

    if random.choice([True, False]):
        humano, ia = JUGADOR_X, JUGADOR_O
    else:
        ia, humano = JUGADOR_X, JUGADOR_O

    estado = {"tablero": tablero,"humano": humano,"ia": ia,"juego_terminado": False,"ganador": None }#La interfaz necesita un estado según la IA. Que se representa como un diccionario
    if obtener_jugador_actual(tablero) == ia:
        _ejecutar_turno_ia(estado)
    return estado


def procesar_clic_humano(estado: dict, fila: int, columna: int) -> bool:
    if estado["juego_terminado"]:
        return False

    if obtener_jugador_actual(estado["tablero"]) != estado["humano"]:
        return False

    jugada_humano: Coordenada = (fila, columna)

    # 1. Validar jugada
    if jugada_humano not in obtener_jugadas_legales(estado["tablero"]):
        return False

    estado["tablero"] = aplicar_jugada(estado["tablero"], jugada_humano)
    _actualizar_estado_final(estado)

    if not estado["juego_terminado"]:
        _ejecutar_turno_ia(estado)

    return True


def _ejecutar_turno_ia(estado: dict) -> None:
    jugada_ia = elegir_mejor_jugada(estado["tablero"], estado["ia"])
    estado["tablero"] = aplicar_jugada(estado["tablero"], jugada_ia)
    _actualizar_estado_final(estado)


def _actualizar_estado_final(estado: dict) -> None:
    """Función auxiliar interna que evalúa si el juego terminó."""
    if es_terminal(estado["tablero"]):
        estado["juego_terminado"] = True
        estado["ganador"] = obtener_ganador(estado["tablero"])