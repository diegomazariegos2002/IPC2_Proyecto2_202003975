from Clases_Principales import LineasProduccion


class Lista_Doble:
    def __init__(self, primero = None):
        self.primero = primero
    
    def setNodo(self, nuevo):
        if self.primero == None:
            self.primero = nuevo
        else: 
            actual = self.primero
            while actual.siguiente != None:
                actual = actual.siguiente
            
            actual.siguiente = nuevo
            nuevo.anterior = actual
    
    def getLineaProduccion(self, num_Id):
        actual = self.primero
        while actual != None:
            if actual.num_Id == num_Id:
                return actual
            actual = actual.siguiente
        return None