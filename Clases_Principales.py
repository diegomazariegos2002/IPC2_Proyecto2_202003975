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
        super().__init__()

class Procedimiento(NodoLista):
    def __init__(self, linea, componente):
        self.linea = linea
        self.componente = componente
        super().__init__()

class Producto(NodoLista):
    def __init__(self, nombre, listaElaboracion):
        self.nombre = nombre
        #Este atributo es una lista de la clase Procedimiento
        self.listaElaboracion = listaElaboracion
        super().__init__()

class ProductoSimulacion(NodoLista):
    def __init__(self, nombreSimulacion, producto):
        self.nombreSimulacion = nombreSimulacion
        self.producto = producto
        super().__init__()