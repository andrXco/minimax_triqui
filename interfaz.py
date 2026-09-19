import tkinter as tk

from flujoPrincipalParaInterfaz import (
    crear_estado_juego,
    procesar_clic_humano
)

estado = crear_estado_juego()

COLOR_FONDO = "#140B1A"          
COLOR_PANEL = "#24112D"         
COLOR_CASILLA = "#32163D"        
COLOR_TEXTO = "#FFF4E6"     

COLOR_SECUNDARIO = "#D6B7FF"     

COLOR_X = "#FF7A00"             
COLOR_O = "#8DFF2F"              

COLOR_BOTON = "#FF4F0F"          
COLOR_BOTON_ACTIVO = "#FF7A3D"   

COLOR_EXITO = "#8DFF2F"         
COLOR_DERROTA = "#FF5C5C"        
COLOR_EMPATE = "#FFD166"         

COLOR_INICIO = "#FFD166"         


ventana = tk.Tk()

ventana.title("Triqui Halloween - Minimax")
ventana.geometry("540x820")
ventana.resizable(False, False)

ventana.configure(bg=COLOR_FONDO)

titulo = tk.Label(
    ventana,
    text="TRIQUI HALLOWEEN",
    font=("Showcard Gothic", 28),
    bg=COLOR_FONDO,
    fg=COLOR_X
)
titulo.pack(pady=(25, 5))

frase = tk.Label(
    ventana,
    text="🎃 Desafía a la IA en una partida terrorífica 👻",
    font=("Bahnschrift SemiBold", 12),
    bg=COLOR_FONDO,
    fg=COLOR_TEXTO
)
frase.pack(pady=(0, 12))

etiqueta_inicio = tk.Label(
    ventana,
    text="",
    font=("Showcard Gothic", 15),
    bg=COLOR_FONDO,
    fg=COLOR_INICIO
)
etiqueta_inicio.pack(pady=5)

panel_jugadores = tk.Frame(
    ventana,
    bg=COLOR_PANEL,
    padx=25,
    pady=16,
    highlightbackground=COLOR_X,
    highlightthickness=2
)
panel_jugadores.pack(pady=10)


etiqueta_jugadores = tk.Label(
    panel_jugadores,
    text="",
    font=("Bahnschrift SemiBold", 14, "bold"),
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO
)
etiqueta_jugadores.pack()

marco_tablero = tk.Frame(
    ventana,
    bg=COLOR_FONDO
)
marco_tablero.pack(pady=25)

botones = []

def actualizar_interfaz():

    tablero = estado["tablero"]

    etiqueta_jugadores.config(
        text=f'🎃 TÚ: {estado["humano"]}        |        💀 IA: {estado["ia"]}'
    )

    if estado["humano"] == "X":
        etiqueta_inicio.config(text="TÚ INICIAS LA NOCHE")
    else:
        etiqueta_inicio.config(text="LA IA COMIENZA EL HECHIZO")

    for fila in range(3):
        for columna in range(3):

            valor = tablero[fila][columna]
            boton = botones[fila][columna]

            boton.config(text=valor)

            if valor == "X":
                boton.config(
                    fg=COLOR_X,
                    disabledforeground=COLOR_X
                )

            elif valor == "O":
                boton.config(
                    fg=COLOR_O,
                    disabledforeground=COLOR_O
                )

            else:
                boton.config(
                    fg=COLOR_TEXTO,
                    disabledforeground=COLOR_TEXTO
                )

            if valor != " ":
                boton.config(state="disabled")
            else:
                boton.config(state="normal")

    if estado["juego_terminado"]:

        for fila in range(3):
            for columna in range(3):
                botones[fila][columna].config(state="disabled")

        ganador = estado["ganador"]

        if ganador == estado["humano"]:
            mensaje.config(
                text="👻 ¡GANASTE! 🎃",
                fg=COLOR_EXITO
            )

        elif ganador == estado["ia"]:
            mensaje.config(
                text="💀 LA IA GANO 💀",
                fg=COLOR_DERROTA
            )

        else:
            mensaje.config(
                text="🕸️ ¡EMPATE! 🕸️",
                fg=COLOR_EMPATE
            )

    else:
        mensaje.config(
            text="Tu turno · Elige una casilla",
            fg=COLOR_SECUNDARIO
        )

def hacer_jugada(fila, columna):

    if estado["juego_terminado"]:
        return

    procesar_clic_humano(
        estado,
        fila,
        columna
    )

    actualizar_interfaz()

for fila in range(3):

    fila_botones = []

    for columna in range(3):

        boton = tk.Button(
            marco_tablero,
            text="",
            width=5,
            height=2,
            font=("Showcard Gothic", 28),
            bg=COLOR_CASILLA,
            fg=COLOR_TEXTO,
            activebackground=COLOR_PANEL,
            activeforeground=COLOR_TEXTO,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=lambda f=fila, c=columna: hacer_jugada(f, c)
        )

        boton.grid(
            row=fila,
            column=columna,
            padx=8,
            pady=8
        )

        fila_botones.append(boton)

    botones.append(fila_botones)


mensaje = tk.Label(
    ventana,
    text="",
    font=("Showcard Gothic", 15),
    bg=COLOR_FONDO,
    fg=COLOR_TEXTO
)
mensaje.pack(pady=(12, 8))

def volver_a_jugar():

    global estado

    estado = crear_estado_juego()
    actualizar_interfaz()

boton_volver = tk.Button(
    ventana,
    text="VOLVER A JUGAR",
    font=("Showcard Gothic", 12),
    width=20,
    height=2,
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    activebackground=COLOR_BOTON_ACTIVO,
    activeforeground=COLOR_TEXTO,
    relief="flat",
    borderwidth=0,
    cursor="hand2",
    command=volver_a_jugar
)
boton_volver.pack(pady=(8, 18))

actualizar_interfaz()

ventana.mainloop()
