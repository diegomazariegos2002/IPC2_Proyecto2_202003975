from Clases_Principales import LineasProduccion


class Lista_Doble:
    def __init__(self, primero = None, ultimo = None):
        self.primero = primero
        self.ultimo = ultimo
    
    def setNodo(self, nuevo):
        if self.primero == None:
            self.primero = nuevo
            self.ultimo = nuevo
        else: 
            actual = self.primero
            while actual.siguiente != None:
                actual = actual.siguiente
            
            actual.siguiente = nuevo
            nuevo.anterior = actual
            self.ultimo = nuevo
    
    def getLineaProduccion(self, num_Id):
        actual = self.primero
        while actual != None:
            if actual.num_Id == num_Id:
                return actual
            actual = actual.siguiente
        return None

    def getProducto(self, nombreProducto):
        actual = self.primero
        while actual != None:
            if actual.nombre == nombreProducto:
                return actual
            actual = actual.siguiente
        return None

    #Metodo para hacer circular mi lista doblemente enlazada este se utiliza
    #Para que despues se pueda recorrer de forma ciclica mi lista cola de Prioridades / lista de Elaboracions
    def hacerCircularLista(self):
        actual = self.primero
        while actual.siguiente != None:
            actual = actual.siguiente
        #aquí le digo al ultimo nodo que su siguiente va a ser el primero para que 
        # se vuelva ciclica la lista.
        actual.siguiente = self.primero

    #Metodo para deshacer lo que realiaza el metodo hacerCircularLista()
    def deshacerCircularLista(self):
        actual = self.primero
        while actual.siguiente != None:
            actual = actual.siguiente
        #aquí le digo al ultimo nodo que su siguiente va a ser None para que 
        # deje de ser ciclica la lista.
        actual.siguiente = None

    def listaNombreProductos(self):
        listaNombreProductos = []
        actual = self.primero
        while actual != None:
            #Agrego los nombres de los productos a una lista
            #OJO aquí se trabajo con listas solo porque el elemento de la interfaz
            #ComboBox solo recibe tuplas o listas.
            listaNombreProductos.append(actual.nombre)
            actual = actual.siguiente
        return listaNombreProductos

    #Metodo recursivo para verificar si ya se completo la lista de Elaboracion osea que si todas
    # las elaboraciones ya son TRUE osea ya fueron completadas para esto se recorre siempre
    # del ultimo en adelante y puesto que todas las Elaboraciones tienen que ser TRUE 
    # lo que hace es que desde que encuentra un FALSE ya retorna porque entonces
    # no todas las elaboraciones son TRUE.
    def verificarListaElaboracion(self, nodoElaboracion):
        actual = nodoElaboracion
        if(actual == None):
            return True

        if actual.estado == False:
            return False
        elif self.verificarListaElaboracion(actual.anterior) == False:
            return False   
        else:
            return True

    #Metodo de busqueda de nodos Elaboracion a partir del nodo que se envia osea hacia el primero
    # esto para verificar si no existe una instruccion antes en la lista de Elaboraciones
    def getNodoElaboracionAntes(self, nodoElaboracion):
        lineaBusqueda = nodoElaboracion.linea
        actual = nodoElaboracion.anterior
        while actual != None:
            if actual.linea == lineaBusqueda:
                return actual
            actual = actual.anterior
        return None

    #Este metodo es similar al de arriba solo que este busca existencias despues del nodo enviado
    def getNodoElaboracionDespues(self, nodoElaboracion):
        lineaBusqueda = nodoElaboracion.linea
        actual = nodoElaboracion.siguiente
        while actual != None:
            if actual.linea == lineaBusqueda:
                return actual
            actual = actual.siguiente
        return None

    def resetearEstadosNodoListaElaboracion(self):
        actual = self.primero
        while actual != None:
            actual.estado = False
            actual = actual.siguiente

    def resetearEstadosNodoListaLineaProduccion(self):
        actual = self.primero
        while actual != None:
            actual.contadorComponente = 0
            actual.cont_tmp_Ensamblaje = 1
            actual = actual.siguiente