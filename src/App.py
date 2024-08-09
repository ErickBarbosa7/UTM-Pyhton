import tkinter as tk
from tkinter import messagebox

class MaquinaDeTuring:
    def __init__(self, estados, alfabeto, funcion_transicion, estado_inicial, estados_aceptacion):
        self.estados = set(estados.split(','))
        self.alfabeto = set(alfabeto.split(','))
        self.funcion_transicion = {}
        for transicion in funcion_transicion.split(';'):
            partes = transicion.split(',')
            clave = (partes[0].strip(), partes[1].strip())
            valor = (partes[2].strip(), partes[3].strip(), partes[4].strip())
            self.funcion_transicion[clave] = valor
        self.estado_actual = estado_inicial
        self.estados_aceptacion = set(estados_aceptacion.split(','))
        self.cinta = []
        self.posicion_cabeza = 0

    def cargar_cinta(self, cadena_entrada):
        self.cinta = list(cadena_entrada) + ['_'] * 1000  

    def paso(self):
        simbolo_actual = self.cinta[self.posicion_cabeza]
        clave = (self.estado_actual, simbolo_actual)
        if clave in self.funcion_transicion:
            estado_siguiente, simbolo_escribir, direccion_mover = self.funcion_transicion[clave]
            self.cinta[self.posicion_cabeza] = simbolo_escribir
            if direccion_mover == 'R':
                self.posicion_cabeza += 1
            elif direccion_mover == 'L':
                self.posicion_cabeza -= 1
            self.estado_actual = estado_siguiente
        else:
            return False
        return True

    def ejecutar(self):
        while self.estado_actual not in self.estados_aceptacion:
            if not self.paso():
                return False
        return True

class GUI_MaquinaDeTuring:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Maquina de Turing")

        self.entradas = {}
        etiquetas = [
            "Estados (separados por comas):",
            "Alfabeto (separado por comas):",
            "Funcion de transicion (estado,simbolo,estado_siguiente,simbolo_escribir,direccion; separados por punto y coma):",
            "Estado inicial:",
            "Estados de aceptacion (separados por comas):",
            "Cadena de entrada:"
        ]

        for i, texto in enumerate(etiquetas):
            self.crear_etiqueta_y_entrada(texto, i)

        self.boton_ejecutar = tk.Button(raiz, text="Ejecutar", command=self.ejecutar_maquina)
        self.boton_ejecutar.grid(row=len(etiquetas), column=0, columnspan=2, pady=10)

        self.etiqueta_resultado = tk.Label(raiz, text="")
        self.etiqueta_resultado.grid(row=len(etiquetas) + 1, column=0, columnspan=2)

    def crear_etiqueta_y_entrada(self, texto, fila):
        etiqueta = tk.Label(self.raiz, text=texto)
        etiqueta.grid(row=fila, column=0, sticky=tk.W, padx=10, pady=5)
        entrada = tk.Entry(self.raiz, width=50)
        entrada.grid(row=fila, column=1, padx=10, pady=5)
        self.entradas[fila] = entrada

    def ejecutar_maquina(self):
        try:
            estados = self.entradas[0].get()
            alfabeto = self.entradas[1].get()
            funcion_transicion = self.entradas[2].get()
            estado_inicial = self.entradas[3].get()
            estados_aceptacion = self.entradas[4].get()
            cadena_entrada = self.entradas[5].get()
            
            maquina = MaquinaDeTuring(estados, alfabeto, funcion_transicion, estado_inicial, estados_aceptacion)
            maquina.cargar_cinta(cadena_entrada)
            
            if maquina.ejecutar():
                self.etiqueta_resultado.config(text="Cadena aceptada")
            else:
                self.etiqueta_resultado.config(text="Cadena no aceptada")
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar la maquina de Turing: {str(e)}")

if __name__ == "__main__":
    raiz = tk.Tk()
    app = GUI_MaquinaDeTuring(raiz)
    raiz.mainloop()
