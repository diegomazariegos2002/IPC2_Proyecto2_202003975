#Libreria para interfaz grafica
from tkinter import Button, Tk, Menu, filedialog, messagebox, ttk, Label
#Libreria para la lectura del xml
import xml.etree.ElementTree as ET
#Libreria para expresion regular
import re
#Librerias del proyecto
from Lista_Doble import Lista_Doble
from Clases_Principales import LineasProduccion, Elaboracion, Producto, ProductoSimulacion, Accion


#=======================================Variables globales========================================
#Datos entrada
listaLineasProduccion = Lista_Doble()
listaProductos = Lista_Doble()
listaProductosSimulacion = Lista_Doble()
#Datos de operaciones
listaAccionesSimulacion = Lista_Doble()


#====================================Declarando función para extraer la dirección de un archivo========================================
def extraerDireccionArchivo():
    Tk().withdraw()
    archivo = filedialog.askopenfile(
        title = "Seleccionar un archivo XML",
        initialdir = "./",
        filetypes= (
            ("archivos XML", "*.XML"),
            ("todos los archivos", "*.*")
        )
    )
    if archivo is None:
        print('No se seleccionó ningun archivo\n')
        return None
    else:
        texto = archivo.name
        archivo.close()
        print('Lectura exitosa\n')
        return texto

#====================================Metodo para cargar el archivo XML de Maquina y Simulacion====================================
def cargar_Maquina(ruta):
    global listaLineasProduccion
    global listaProductos
    tree = ET.parse(ruta)
    root = tree.getroot()

    #<Maquina>
    for elemento in root:
        #<CantidadLineasProduccion>
        for subElemento1 in elemento.iter('CantidadLineasProduccion'):
            cantidadLineasProduccion = int(subElemento1.text)
            print(cantidadLineasProduccion)

        #<ListadoLineasProduccion>
        for subElemento1 in elemento.iter('ListadoLineasProduccion'):
            #<LineaProduccion>
            for subElemento2 in subElemento1.iter('LineaProduccion'):
                #<Numero>
                for subElemento3 in subElemento2.iter('Numero'):
                    numeroLinea = int(subElemento3.text)
                    print("Numero de produccion -> ", numeroLinea)
                
                #<CantidadComponentes>
                for subElemento3 in subElemento2.iter('CantidadComponentes'):
                    cantidadComponentes = int(subElemento3.text)
                    print(cantidadComponentes)

                #<TiempoEnsamblaje>
                for subElemento3 in subElemento2.iter('TiempoEnsamblaje'):
                    tiempoEnsamblaje = int(subElemento3.text)
                    print(tiempoEnsamblaje)

                #Creando objeto de Linea de produccion
                linea = LineasProduccion(numeroLinea, cantidadComponentes, tiempoEnsamblaje)
                #Agregando el objeto creado a la lista de lineas de produccion
                listaLineasProduccion.setNodo(linea)
        
        #<ListadoProductos>
        for subElemento1 in elemento.iter('ListadoProductos'):
            #<Producto>
            for subElemento2 in subElemento1.iter('Producto'):
                #<nombre>
                for subElemento3 in subElemento2.iter('nombre'):
                    nombreProducto = subElemento3.text.strip()
                    print(nombreProducto)

                #Creamos una lista para los Elaboracions
                listaElaboracion = Lista_Doble()

                #<elaboracion>
                for subElemento3 in subElemento2.iter('elaboracion'):
                    #Se borran los espacios en blanco del principio y del final
                    texto_Cola = subElemento3.text.strip()
                    texto_Cola += " "
                    #Se mira el patron de la expresion regular
                    patron1 = 'L(.*?)p'
                    patron2 = 'C(.*?) '
                    #Se crean los numeros segun el patron indicado OJO: aquí todavía sigue en string
                    lineas = re.findall(patron1, texto_Cola)
                    componentes = re.findall(patron2, texto_Cola)
                    print(texto_Cola)
                    print(lineas)
                    print(componentes)
                    
                    cont = 0
                    while(cont < len(lineas)):
                        #Creamos los nodos de la lista y los añadimos
                        nodoElaboracion = Elaboracion(int(lineas[cont]), int(componentes[cont]))
                        listaElaboracion.setNodo(nodoElaboracion)
                        cont+=1
                #Creamos el nodo Producto y lo añadimos a su lista
                producto = Producto(nombreProducto,listaElaboracion)
                listaProductos.setNodo(producto)
    print("Archivos de Maquina cargados con éxito")
                
def cargar_Simulacion(ruta):
    global listaProductosSimulacion
    global listaProductos
    tree = ET.parse(ruta)
    root = tree.getroot()
    #<Simulacion>
    for elemento in root:
        #<Nombre>
        for subElemento1 in elemento.iter('Nombre'):
            nombreSimulacion = subElemento1.text.strip()
            print(nombreSimulacion)
        #<ListadoProductos>
        for subElemento1 in elemento.iter('ListadoProductos'):
            #<Producto>
            for subElemento2 in subElemento1.iter('Producto'):
                #buscando un producto mediante su nombre
                nombreProducto = subElemento2.text.strip()
                print(nombreProducto)
                producto = listaProductos.getProducto(nombreProducto)
                #generando el objeto del producto de la simulacion y añadiendolo a la lista
                productoSimulacion = ProductoSimulacion(nombreProducto, producto)
                listaProductosSimulacion.setNodo(productoSimulacion)
    print("Archivo de simulacion cargado con éxito!!!")

#Metodo que se encarga de realizar la simulacion de forma individual osea por cada producto.
def realizar_Simulacion(Nombreproducto):
    global listaAccionesSimulacion
    producto = listaProductos.getProducto(Nombreproducto)
    tiempoSimulacion = 0
    estadoEnsamblaje = False

    #while que me permite recorrer mi listaElaboracion una y otra vez...
    while(True):
        tiempoSimulacion += 1
        #verificamos si ya se cumplieron todas las elaboraciones
        ultimo = producto.listaElaboracion.ultimo
        if producto.listaElaboracion.verificarListaElaboracion(ultimo) == True:
            break
        else:
            actual = producto.listaElaboracion.primero
            while(actual != None):
                print("Ciclo", tiempoSimulacion)
                #Si no existe una elaboracion antes de la actual entonces la elaboracion actual
                # es la primera en su linea en la cola de prioridades.
                buscarAnterior = producto.listaElaboracion.getNodoElaboracionAntes(actual)
                if buscarAnterior != None: # si, si existe un nodo en la misma linea antes
                    if buscarAnterior.estado == False: #si no se ha completado el otro no hagas nada
                        pass
                    else:
                        print("ejecuta tus metodos")
                else:
                    print("ejecuta tus metodos")
                    busquedaSiguiente = producto.listaElaboracion.getNodoElaboracionDespues(actual)
                    if actual.estado == True and busquedaSiguiente == None: #Si ya se completo la elaboracion no hace nada
                        accion = Accion(actual.linea, "No hacer nada", tiempoSimulacion)
                    elif actual.estado == True and busquedaSiguiente != None: #Si ya se completo pero si existe una instruccion antes no va a hacer nada
                        pass
                    else:
                        if estadoEnsamblaje == False: #Para cuando todas las lineas de produccion tengan que seguir moviendose
                            
                            pass
                        elif estadoEnsamblaje == True and actual.ensamblando == True: #este es el nodo que esta ensamblando
                            pass
                        else: #Para las lineas de produccion que no estan ensamblando
                            accion = Accion(actual.linea, "No hacer nada", tiempoSimulacion)

                #agregamos la accion resultante a la lista de acciones
                # listaAccionesSimulacion.setNodo(accion)
                actual = actual.siguiente
        


class VentanaMenu:
    def __init__(self):
        self.txt = None
        self.ventana = Tk()
        self.ventana.title("Menu")
        self.ventana.geometry("800x500")
        self.ventana.configure(bg = 'white')

        # Por medio de esto accedo a lo que sucede al dar click sobre la X para cerrar la ventana
        self.ventana.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Se crea el menú de la ventana / el tearoff = 0 es para que no se me cree un submenú al darle click al "----" que me sale en los cascade
        self.miMenu = Menu(self.ventana, tearoff=0)
        self.ventana.configure(menu=self.miMenu)

        #Creando una sección/SubMenú esta es la barrita que aparecere arriba en la ventana
        self.miMenu.add_command(label="Cargar maquina", command=self.cargarMaquina)
        self.miMenu.add_command(label="Cargar simulación", command=self.cargarSimulacion)
        self.miMenu.add_command(label="Reportes", command=self.prueba)
        self.miMenu.add_command(label="Salir", command=self.on_closing)

        #ComboBox
        listadoNombreImagenes = []
        self.myComboBox = ttk.Combobox(self.ventana, state= "readonly", value = listadoNombreImagenes)
        self.myComboBox.bind("<<ComboboxSelected>>", self.comboClick)
        self.myComboBox.place(x=200, y = 10)

        #Labels
        self.label1 = Label(self.ventana, text="Escoga un producto ")
        self.label1.place(x=10, y = 10)

        #Buttons
        self.btnProcesar = Button(self.ventana, text="Procesar", command=self.procesar)
        self.btnProcesar.place(x=400, y = 10)

        self.ventana.mainloop()

    #Metodo para procesar individualmente cada producto y mostrarlo en la interfaz
    def procesar(self):
        nombreProducto = self.myComboBox.get()
        if nombreProducto != "":
            realizar_Simulacion(nombreProducto)
        else:
            print("El producto seleccionado no existe")

    def cargarMaquina(self):
        global listaProductos
        global listaLineasProduccion
        global listaProductosSimulacion
        listaLineasProduccion = Lista_Doble()
        listaProductos = Lista_Doble()
        listaProductosSimulacion = Lista_Doble()
        direccion = extraerDireccionArchivo()
        if direccion == None:
            pass
        else:
            print("Cargando Maquina")
            cargar_Maquina(direccion)
            listadoNombreProductos = listaProductos.listaNombreProductos()
            #añado la lista de nombres al ComboBox
            self.myComboBox["value"] = listadoNombreProductos
            #Le digo que muestre el ComboBox con el primer elemento
            self.myComboBox.current(0) 
            
    def cargarSimulacion(self):
        global listaProductos
        global listaProductosSimulacion
        listaProductosSimulacion = Lista_Doble()
        if listaProductos.primero == None:
            print("No se ha cargado la maquina para hacer su simulación.")
        else:
            direccion = extraerDireccionArchivo()
            if direccion == None:
                pass
            else:
                print("Cargando Simulacion")
                cargar_Simulacion(direccion)

    def prueba(self):
        print("Hola")

    #se manda a llamar cuando se selecciona un item del combo.
    def comboClick(self, event):
        pass

    # Metodo para cerrar la ventana 
    def on_closing(self):
        if messagebox.askokcancel("Cerrar Programa", "Seguro que desea Salir?"):
            self.ventana.quit()
