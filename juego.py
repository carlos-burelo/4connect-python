import tkinter as tk
from tkinter import messagebox
import time

class CuatroEnLineaGUI:
    def __init__(self, filas=6, columnas=7):
        self.filas = filas
        self.columnas = columnas
        self.jugadores = ['\U0001F535', '\U0001F7E1']  # Emojis para jugadores X y O (Rojo y Amarillo)
        self.turno_actual = 0
        self.movimientos = 0
        self.tablero = [[' ' for _ in range(columnas)] for _ in range(filas)]
        self.crear_interfaz()

    def crear_interfaz(self):
        self.raiz = tk.Tk()
        self.raiz.title("Cuatro en Línea")
        self.raiz.configure(bg='blue')  # Cambia el color de fondo a azul

        self.botones = []
        for i in range(self.filas):
            fila_botones = []
            for j in range(self.columnas):
                if i == 0:
                    boton = tk.Button(self.raiz, text='\U0001F535', font=('Arial', 20), width=3, height=1, bg='blue', fg='white', command=lambda col=j: self.soltar_ficha(col))
                else:
                    boton = tk.Label(self.raiz, text='\U0001F535', font=('Arial', 20), width=3, height=1, bg='blue', fg='white')
                boton.grid(row=i, column=j)
                fila_botones.append(boton)
            self.botones.append(fila_botones)

    def soltar_ficha(self, col):
        fila = self.obtener_fila_vacia(col)
        if fila != -1:
            self.tablero[fila][col] = self.jugadores[self.turno_actual]
            self.movimientos += 1
            self.animar_soltar_ficha(fila, col)
            if self.verificar_ganador(fila, col):
                ganador = self.jugadores[self.turno_actual]
                messagebox.showinfo("Ganador", f"¡El jugador {ganador} gana!")
                self.raiz.destroy()
                return

            if self.movimientos == self.filas * self.columnas:
                messagebox.showinfo("Empate", "¡Es un empate!")
                self.raiz.destroy()
                return

            self.turno_actual = (self.turno_actual + 1) % 2

    def obtener_fila_vacia(self, col):
        for i in range(self.filas - 1, -1, -1):
            if self.tablero[i][col] == ' ':
                return i
        return -1

    def animar_soltar_ficha(self, fila, col):
        color_jugador = 'red' if self.turno_actual == 0 else 'yellow'
        for i in range(fila + 1):
            self.botones[i][col].config(fg=color_jugador)
            self.botones[i][col].update()
            time.sleep(0.06)
            if i != fila:
                self.botones[i][col].config(fg='white')

    def verificar_ganador(self, fila, col):
    # Direcciones posibles para verificar si hay cuatro en línea
      direcciones = [(1, 0), (0, 1), (1, 1), (-1, 1)]
      jugador_actual = self.jugadores[self.turno_actual]  # Jugador actual (X o O)

      for direccion_fila, direccion_col in direcciones:
          contador_fichas = 1  # Inicia el conteo en 1 para la ficha recién colocada
          for i in range(1, 4):
              # Verifica hacia adelante en la dirección específica
              fila_actual, col_actual = fila + i * direccion_fila, col + i * direccion_col
              # Verifica si está dentro de los límites del tablero y si la ficha pertenece al jugador actual
              if 0 <= fila_actual < self.filas and 0 <= col_actual < self.columnas and self.tablero[fila_actual][col_actual] == jugador_actual:
                  contador_fichas += 1
              else:
                  break  # Rompe el bucle si no coincide la ficha o está fuera del tablero
          for i in range(1, 4):
              # Verifica hacia atrás en la dirección específica
              fila_actual, col_actual = fila - i * direccion_fila, col - i * direccion_col
              # Verifica si está dentro de los límites del tablero y si la ficha pertenece al jugador actual
              if 0 <= fila_actual < self.filas and 0 <= col_actual < self.columnas and self.tablero[fila_actual][col_actual] == jugador_actual:
                  contador_fichas += 1
              else:
                  break  # Rompe el bucle si no coincide la ficha o está fuera del tablero
          if contador_fichas >= 4:  # Si hay cuatro en línea en alguna dirección, se ha encontrado un ganador
              return True

      return False  # Si no se encontraron cuatro en línea en ninguna dirección


    def iniciar(self):
        self.raiz.mainloop()

if __name__ == "__main__":
    juego = CuatroEnLineaGUI()
    juego.iniciar()
