from tkinter import Tk, Button, Label,Entry, messagebox
import time

class Arco(object):
    def __init__(self, destino, peso=1):
        self.destino = destino
        self.peso = peso
        self.siguiente = None

class ListaAdyacencia(object):
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def listaVacia(self):
        return self.primero == None

    def adyacente(self, dato):
        actual = self.primero
        encontrado = False
        while actual != None and dato != actual.destino:
            actual = actual.siguiente
        if actual != None:
            encontrado = True
        return encontrado

    def nuevaAdyacencia(self, destino):
        if not self.adyacente(destino):
            nodo = Arco(destino)
            self.__insertar(nodo)

    def __insertar(self, nodo):
        if self.listaVacia():
            self.primero = nodo
            self.ultimo = nodo
        else:
            self.ultimo.siguiente = nodo
            self.ultimo = nodo

class Nodo:
    def __init__(self, valor, vecinos=None):
        self.valor = valor
        self.vecinos = ListaAdyacencia() if vecinos is None else vecinos

class Grafo:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.nodos = self.crear_grafo()

    def crear_grafo(self):
        nodos = [[Nodo(' ') for _ in range(self.columnas)] for _ in range(self.filas)]
        for i in range(self.filas):
            for j in range(self.columnas):
                if i > 0: nodos[i][j].vecinos.nuevaAdyacencia(nodos[i-1][j])  # arriba
                if i < self.filas - 1: nodos[i][j].vecinos.nuevaAdyacencia(nodos[i+1][j])  # abajo
                if j > 0: nodos[i][j].vecinos.nuevaAdyacencia(nodos[i][j-1])  # izquierda
                if j < self.columnas - 1: nodos[i][j].vecinos.nuevaAdyacencia(nodos[i][j+1])  # derecha
        return nodos
    

class Conecta4:
  def __init__(self, filas=6, columnas=7):
    self.filas = filas
    self.columnas = columnas
    self.turno_actual = 0
    self.movimientos = 0
    self.tablero = Grafo(filas, columnas)
    self.crear_interfaz()

  def crear_interfaz(self):
    self.raiz = Tk()
    self.raiz.title("Cuatro en Línea")
    self.raiz.configure(bg='blue')
    self.botones = []
    for i in range(self.filas):
      fila_botones = []
      for j in range(self.columnas):
        if i == 0:
          boton = Button(self.raiz, text='\U0001F535', font=('Arial', 20), width=3, height=1, bg='blue', fg='white', command=lambda col=j: self.soltar_ficha(col))
        else:
          boton = Label(self.raiz, text='\U0001F535', font=('Arial', 20), width=3, height=2, bg='blue', fg='white')
        boton.grid(row=i, column=j)
        fila_botones.append(boton)
      self.botones.append(fila_botones)

  def soltar_ficha(self, col):
    fila = self.obtener_fila_vacia(col)
    if fila != -1:
      self.tablero.nodos[fila][col].valor = self.jugadores[self.turno_actual]
      self.movimientos += 1
      self.animar_soltar_ficha(fila, col)
      if self.verificar_ganador(fila, col):
        ganador = self.jugadores[self.turno_actual]
        messagebox.showinfo("Ganador", f"¡{ganador} ha ganado la partida!")
        self.raiz.destroy()
        return

      if self.movimientos == self.filas * self.columnas:
        messagebox.showinfo("Empate", "¡Es un empate!")
        self.raiz.destroy()
        return

      self.turno_actual = (self.turno_actual + 1) % 2

  def obtener_nombres(self):
    self.raiz.withdraw()  # Oculta la ventana principal temporalmente
    self.ventana_nombres = Tk()
    self.ventana_nombres.title("Ingrese los nombres de los jugadores")
    self.ventana_nombres.configure(bg='blue')

    label_jugador1 = Label(self.ventana_nombres, text="Nombre del jugador 1:", font=('Arial', 12), bg='blue', fg='white')
    label_jugador1.grid(row=0, column=0)
    self.entry_jugador1 = Entry(self.ventana_nombres)
    self.entry_jugador1.grid(row=0, column=1)

    label_jugador2 = Label(self.ventana_nombres, text="Nombre del jugador 2:", font=('Arial', 12), bg='blue', fg='white')
    label_jugador2.grid(row=1, column=0)
    self.entry_jugador2 = Entry(self.ventana_nombres)
    self.entry_jugador2.grid(row=1, column=1)

    boton_confirmar = Button(self.ventana_nombres, text="Confirmar", font=('Arial', 12), bg='blue', fg='white', command=self.guardar_nombres)
    boton_confirmar.grid(row=2, columnspan=2)

  def guardar_nombres(self):
      jugador1 = self.entry_jugador1.get()
      jugador2 = self.entry_jugador2.get()
      if jugador1 and jugador2:
          self.jugadores = [jugador1, jugador2]
          self.ventana_nombres.destroy()  # Cierra la ventana de nombres
          self.raiz.deiconify()  # Muestra la ventana principal nuevamente
      else:
          messagebox.showwarning("Error", "Por favor ingrese ambos nombres.")

  def obtener_fila_vacia(self, col):
    for i in range(self.filas - 1, -1, -1):
      if self.tablero.nodos[i][col].valor == ' ':
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
    direcciones = [(1, 0), (0, 1), (1, 1), (-1, 1)]
    jugador_actual = self.jugadores[self.turno_actual]

    for direccion_fila, direccion_col in direcciones:
      contador_fichas = 1
      for i in range(1, 4):
        fila_actual, col_actual = fila + i * direccion_fila, col + i * direccion_col
        if 0 <= fila_actual < self.filas and 0 <= col_actual < self.columnas and self.tablero.nodos[fila_actual][col_actual].valor == jugador_actual:
          contador_fichas += 1
        else:
          break
      for i in range(1, 4):
        fila_actual, col_actual = fila - i * direccion_fila, col - i * direccion_col
        if 0 <= fila_actual < self.filas and 0 <= col_actual < self.columnas and self.tablero.nodos[fila_actual][col_actual].valor == jugador_actual:
          contador_fichas += 1
        else:
          break
      if contador_fichas >= 4:
        return True

    return False

  def iniciar(self):
    self.obtener_nombres()
    self.raiz.mainloop()

if __name__ == "__main__":
  juego = Conecta4()
  juego.iniciar()
