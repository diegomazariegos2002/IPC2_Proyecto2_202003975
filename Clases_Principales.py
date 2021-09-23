#Clase Nodo para utilizar la herencia y asi no repetir el codigo de siguiente 
# y anterior en cada clase que haga despues.
class NodoLista():
    def __init__(self):
        self.siguiente = None
        self.anterior = None

class LineasProduccion(NodoLista):
    def __init__(self, num_Id, cant_Componentes, tmp_Ensamblaje):
        self.num_Id = num_Id
        self.cant_Componentes = cant_Componentes
        self.tmp_Ensamblaje = tmp_Ensamblaje
        self.contadorComponente = 0
        self.cont_tmp_Ensamblaje = 1
        super().__init__()

#Procedimiento o Elaboraciones que se hacen para fabricar el producto
class Elaboracion(NodoLista):
    def __init__(self, linea, componente):
        self.linea = linea
        self.componente = componente
        self.estado = False #su estado inicial es false puesto que no se han cumplido
        self.ensamblando = False #estado para ver si la elaboracion le toca ensamblar
        
        super().__init__()

class Producto(NodoLista):
    def __init__(self, nombre, listaElaboracion):
        self.nombre = nombre
        #Este atributo es una lista de la clase Elaboracion
        self.listaElaboracion = listaElaboracion #lista de Elaboracion(NodoLista)
        self.listaAccionesProducto = None
        super().__init__()

class ProductoSimulacion(NodoLista):
    def __init__(self, nombreSimulacion, producto):
        self.nombreSimulacion = nombreSimulacion
        self.producto = producto #simplemente un producto
        super().__init__()

class Accion(NodoLista):
    #Atributos: Linea de movimiento, movimiento de accion(componente, ensamblar o no hacer nada), tiempo en que sucede la accion
    def __init__(self, linea, mov, tmp_Accion):
        self.linea = linea
        self.mov = mov
        self.tmp_Accion = tmp_Accion
        super().__init__()
    
    def __str__(self):
        return f"(linea = {str(self.linea)} ,mov = {str(self.mov)}, tmp_Accion = {str(self.tmp_Accion)})"

class Simulacion(NodoLista):
    def __init__(self, nombreSimulacion, nombreProducto,listaAcciones):
        self.nombreSimulacion = nombreSimulacion
        self.nombreProducto = nombreProducto
        self.listaAcciones = listaAcciones
        super().__init__()