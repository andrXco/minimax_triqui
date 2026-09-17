from  __future__ import annotations
import random

from arbol_juego import (
    JUGADOR_O,
    JUGADOR_X,
    Tablero,
    aplicar_jugada,
    crear_tablero_vacio,
    es_terminal,
    obtener_ganador,
    obtener_jugador_actual,
    obtener_jugadas_legales,
)
from minimax import elegir_mejor_jugada

def imprimir_tablero(tablero: Tablero) -> None: #ESTA ES UNA VERSIÓN DE CONSOLA DEL JUEGO, SE PUEDE USAR PARA VERIFICAR QUE SI FUNCIONA
    print("\n  0   1   2")
    for i, fila in enumerate(tablero):
        contenido = " | ".join(fila)
        print(f"{i} {contenido}")
        if i < 2:
            print("  ---------")
    print()

def main():
    t = crear_tablero_vacio()
    ia = JUGADOR_X
    humano = JUGADOR_O
    if random.choice([True, False]):
        humano, ia = JUGADOR_X, JUGADOR_O
        print("=== EMPIEZAS TÚ (Juegas con X) ===")
    else:
        ia, humano = JUGADOR_X, JUGADOR_O
        print("=== EMPIEZA LA IA (Juega con X) ===")

    while not es_terminal(t):
        actual = obtener_jugador_actual(t)

        if actual == humano:
            jugadas_legales = obtener_jugadas_legales(t)

            while True:
                    entrada = input("turno del usuario")
                    
                    if len(entrada) != 2:
                        print("Por favor ingresa 2 numeros pegados.")
                        continue

                    fila, columna = int(entrada[0]), int(entrada[1])
                    jugada = (fila, columna)

                    if jugada in jugadas_legales:
                        break 
                    else:
                        print("Esa casilla no es posible dentro de esta partida")
        else:
            jugada = elegir_mejor_jugada(t, ia)

        t = aplicar_jugada(t, jugada)
        imprimir_tablero(t)

    jugadorGanador = obtener_ganador(t)

    if jugadorGanador == ia:
        print("Gana la IA")
    elif jugadorGanador == humano:
        print("Gana el usuario")
    else:
        print("Empate")


if __name__ == "__main__":
    main()