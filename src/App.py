import tkinter as tk
from tkinter import messagebox



# Clase que define una Maquina de Turing
class MaquinaDeTuring:
    def __init__(self, estados, alfabeto, funcion_transicion, estado_inicial, estados_aceptacion):
        # Inicializa los estados, el alfabeto y la funcion de transicion
        # Conjunto de estados
        self.estados = set(estados.split(','))  
        # Conjunto de simbolos del alfabeto
        self.alfabeto = set(alfabeto.split(','))  
        
        # Inicializa la funcion de transicion a partir de la cadena proporcionada
        self.funcion_transicion = {}
        for transicion in funcion_transicion.split(';'):
            partes = transicion.split(',')
            # Estado actual y simbolo actual
            clave = (partes[0].strip(), partes[1].strip())  
            # Estado siguiente, simbolo a escribir, direccion de movimiento
            valor = (partes[2].strip(), partes[3].strip(), partes[4].strip())  
            self.funcion_transicion[clave] = valor
        
        # Inicializa el estado actual y los estados de aceptacion
        self.estado_actual = estado_inicial
        self.estados_aceptacion = set(estados_aceptacion.split(','))
        # Cinta inicial vacia
        self.cinta = []  
        # Posicion inicial de la cabeza en la cinta
        self.posicion_cabeza = 0  

    # Carga la cinta con la cadena de entrada y anade espacios en blanco adicionales
    def cargar_cinta(self, cadena_entrada):
         # Extiende la cinta con 1000 espacios en blanco
        self.cinta = list(cadena_entrada) + ['_'] * 1000 
    # Ejecuta un solo paso de la maquina de Turing
    def paso(self):
        # Obtiene el simbolo actual bajo la cabeza
        simbolo_actual = self.cinta[self.posicion_cabeza] 
        # Genera la clave para la funcion de transicion
        clave = (self.estado_actual, simbolo_actual) 
        
        # Verifica si existe una transicion valida para la clave actual
        if clave in self.funcion_transicion:
            estado_siguiente, simbolo_escribir, direccion_mover = self.funcion_transicion[clave]
            
            # Escribe el nuevo simbolo en la cinta y mueve la cabeza segun la direccion indicada
            self.cinta[self.posicion_cabeza] = simbolo_escribir
            if direccion_mover == 'R':
                self.posicion_cabeza += 1
            elif direccion_mover == 'L':
                self.posicion_cabeza -= 1 
            
            # Actualiza el estado actual
            self.estado_actual = estado_siguiente
        else:
            return False  # No hay una transicion valida, detiene la ejecucion
        
        return True  # El paso se ejecuta con exito

    # Ejecuta la maquina hasta alcanzar un estado de aceptacion o no puede continuar
    def ejecutar(self):
        while self.estado_actual not in self.estados_aceptacion:
            if not self.paso():
                return False 
        return True  

# Clase que define la interfaz grafica para la Maquina de Turing
class GUI_MaquinaDeTuring:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Maquina de Turing")  

        self.entradas = {}
        # Etiquetas para los campos de entrada
        etiquetas = [
            "Estados (separados por comas):",
            "Alfabeto (separado por comas):",
            "Funcion de transicion (estado,simbolo,estado_siguiente,simbolo_escribir,direccion; separados por punto y coma):",
            "Estado inicial:",
            "Estados de aceptacion (separados por comas):",
            "Cadena de entrada:"
        ]

        # Crea las etiquetas y campos de entrada
        for i, texto in enumerate(etiquetas):
            self.crear_etiqueta_y_entrada(texto, i)

        # Boton para ejecutar la maquina
        self.boton_ejecutar = tk.Button(raiz, text="Ejecutar", command=self.ejecutar_maquina)
        self.boton_ejecutar.grid(row=len(etiquetas), column=0, columnspan=2, pady=10)

        # Etiqueta para mostrar el resultado de la ejecucion
        self.etiqueta_resultado = tk.Label(raiz, text="")
        self.etiqueta_resultado.grid(row=len(etiquetas) + 1, column=0, columnspan=2)

    # Metodo para crear una etiqueta y un campo de entrada en la interfaz
    def crear_etiqueta_y_entrada(self, texto, fila):
        etiqueta = tk.Label(self.raiz, text=texto)
        etiqueta.grid(row=fila, column=0, sticky=tk.W, padx=10, pady=5)
        entrada = tk.Entry(self.raiz, width=50)
        entrada.grid(row=fila, column=1, padx=10, pady=5)
        self.entradas[fila] = entrada

    # Metodo que se ejecuta al presionar el boton "Ejecutar"
    def ejecutar_maquina(self):
        try:
            # Recoge los valores ingresados por el usuario
            estados = self.entradas[0].get()
            alfabeto = self.entradas[1].get()
            funcion_transicion = self.entradas[2].get()
            estado_inicial = self.entradas[3].get()
            estados_aceptacion = self.entradas[4].get()
            cadena_entrada = self.entradas[5].get()
            
            # Crea y configura la maquina de Turing
            maquina = MaquinaDeTuring(estados, alfabeto, funcion_transicion, estado_inicial, estados_aceptacion)
            maquina.cargar_cinta(cadena_entrada)
            
            # Ejecuta la maquina y muestra el resultado
            if maquina.ejecutar():
                self.etiqueta_resultado.config(text="Cadena aceptada")
            else:
                self.etiqueta_resultado.config(text="Cadena no aceptada")
        except Exception as e:
            # Muestra un mensaje de error si ocurre una excepcion
            messagebox.showerror("Error", f"Error al ejecutar la maquina de Turing: {str(e)}")

#Iniciar la interfaz
if __name__ == "__main__":
    raiz = tk.Tk()
    app = GUI_MaquinaDeTuring(raiz)
    raiz.mainloop()
