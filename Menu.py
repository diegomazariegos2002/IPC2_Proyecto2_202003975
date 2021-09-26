#Libreria para interfaz grafica
from tkinter import Button, Tk, Menu, filedialog, messagebox, ttk, Label, Scrollbar, scrolledtext, Frame
import tkinter
from tkinter import *
from tkinter import ttk
#Libreria para la lectura del xml
import xml.etree.ElementTree as ET
#Libreria para expresion regular
import re
from graphviz.dot import Graph
#Librerias del proyecto
from Lista_Doble import Lista_Doble
from Clases_Principales import LineasProduccion, Elaboracion, Producto, ProductoSimulacion, Accion, Simulacion
#Libreria para obtener la direccion del ejecutable
import pathlib
import webbrowser
#Librería para utilizar la herramienta graphviz
from graphviz import Digraph
#Librería necesaria para trabajar con el progressBar
import time
#Librería para extraer imagenes
from PIL import ImageTk, Image

#=======================================Variables globales========================================
#Datos entrada
listaLineasProduccion = Lista_Doble()
listaProductos = Lista_Doble()
#Datos de operaciones
listaAccionesSimulacion = Lista_Doble()
simulacionActual = Simulacion()

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

#====================================Metodos para cargar el archivo XML de Maquina y Simulacion====================================
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
    global listaProductos
    global simulacionActual
    tree = ET.parse(ruta)
    root = tree.getroot()
    #<Simulacion>
    for elemento in root:
        #<Nombre>
        for subElemento1 in elemento.iter('Nombre'):
            nombreSimulacion = subElemento1.text.strip()
            print(nombreSimulacion)
            listaProductosSimulacion = Lista_Doble()
            simulacionActual = Simulacion(str(nombreSimulacion), listaProductosSimulacion) #inicializando la simulacion actual por eso le mandamos una lista vacía
        #<ListadoProductos>
        for subElemento1 in elemento.iter('ListadoProductos'):
            #<Producto>
            for subElemento2 in subElemento1.iter('Producto'):
                #buscando un producto mediante su nombre
                nombreProducto = subElemento2.text.strip()
                print(nombreProducto)
                producto = listaProductos.getProducto(nombreProducto)
                productoAuxiliar = ProductoSimulacion(producto.nombre, producto.listaElaboracion, producto.listaAccionesProducto)#Este producto auxiliar lo genero para no tocar directamente el producto que tengo en la listaProductos
                simulacionActual.listaProductos.setNodo(productoAuxiliar) #Al objeto simulacionActual le añado un producto mas a su lista de productos
    print("Archivo de simulacion cargado con éxito!!!")
    actual = simulacionActual.listaProductos.primero
    while(actual != None):
        realizar_Simulacion(actual.nombre)
        actual = actual.siguiente
    escribirArchivoXml()

#Metodos que se encargan de realizar la simulacion de forma individual osea por cada producto mediante su nombre.
def realizar_Simulacion(Nombreproducto):
    global listaAccionesSimulacion
    global listaLineasProduccion
    global listaProductos
    global simulacionActual
    producto = listaProductos.getProducto(Nombreproducto)
    tiempoSimulacion = 0
    estadoEnsamblaje = False
    estadoEnsambleUltimo = False


    #while que me permite recorrer mi listaElaboracion una y otra vez...
    while(True):
        #verificamos si ya se cumplieron todas las elaboraciones
        ultimo = producto.listaElaboracion.ultimo
        if producto.listaElaboracion.verificarListaElaboracion(ultimo) == True:
            break
        else:
            tiempoSimulacion += 1
            actual = producto.listaElaboracion.primero
            while(actual != None):
                #Si no existe una elaboracion antes de la actual entonces la elaboracion actual
                # es la primera en su linea en la cola de prioridades.
                buscarAnterior = producto.listaElaboracion.getNodoElaboracionAntes(actual)
                if buscarAnterior != None: # si, si existe un nodo en la misma linea antes
                    if buscarAnterior.estado == False: #si no se ha completado el otro no hagas nada
                        pass
                    else:
                        busquedaSiguiente = producto.listaElaboracion.getNodoElaboracionDespues(actual)
                        if actual.estado == True and busquedaSiguiente == None: #Si ya se completo la elaboracion no hace nada
                            accion = Accion(actual.linea, "No hacer nada", tiempoSimulacion)
                        elif actual.estado == True and busquedaSiguiente != None: #Si ya se completo pero si existe una instruccion antes no va a hacer nada
                            pass
                        else:
                            if estadoEnsamblaje == False and estadoEnsambleUltimo == False: #Para cuando todas las lineas de produccion tengan que seguir moviendose
                                lineaProduccion = listaLineasProduccion.getLineaProduccion(actual.linea)
                                
                                #Verificar si ya ha llegado al componente destino
                                if int(lineaProduccion.contadorComponente) == int(actual.componente):
                                    #Verificar si la instruccion anterior ya ha sido completada
                                    if actual.anterior == None or actual.anterior.estado == True:
                                        estadoEnsamblaje = True
                                        actual.ensamblando = True
                                        #Funcion de ensamblaje
                                        lineaProduccion = listaLineasProduccion.getLineaProduccion(actual.linea)
                                        #Si tiene que ir sumando
                                        if int(lineaProduccion.cont_tmp_Ensamblaje) == int(lineaProduccion.tmp_Ensamblaje):
                                            accion = Accion(actual.linea, f"Ensamblar - componente {str(actual.componente)}", tiempoSimulacion)
                                            estadoEnsamblaje = False
                                            actual.ensamblando = False
                                            actual.estado = True
                                            lineaProduccion.cont_tmp_Ensamblaje = 1
                                            estadoEnsambleUltimo = True


                                        elif int(lineaProduccion.cont_tmp_Ensamblaje) < int(lineaProduccion.tmp_Ensamblaje):
                                            accion = Accion(actual.linea, f"Ensamblar - componente {str(actual.componente)}", tiempoSimulacion)
                                            lineaProduccion.cont_tmp_Ensamblaje += 1
                                            

                                    else:#Si no ha sido completada se tiene que esperar a que se complete y por ende no se hace nada
                                        accion = Accion(actual.linea, "No hacer nada", tiempoSimulacion)

                                #Si tiene que ir sumando
                                elif int(lineaProduccion.contadorComponente) < int(actual.componente):
                                    lineaProduccion.contadorComponente += 1
                                    accion = Accion(actual.linea, f"Mover brazo a componente {str(lineaProduccion.contadorComponente)}", tiempoSimulacion)
                                    #Verificar si ya ha llegado al componente destino
                                    
                                #Si tiene que ir restando
                                elif int(lineaProduccion.contadorComponente) > int(actual.componente):
                                    lineaProduccion.contadorComponente -= 1
                                    accion = Accion(actual.linea, f"Mover brazo a componente {str(lineaProduccion.contadorComponente)}", tiempoSimulacion)

                            elif estadoEnsamblaje == True and actual.ensamblando == True: #este es el nodo que esta ensamblando
                                lineaProduccion = listaLineasProduccion.getLineaProduccion(actual.linea)
                                #Si tiene que ir sumando
                                if int(lineaProduccion.cont_tmp_Ensamblaje) == int(lineaProduccion.tmp_Ensamblaje):
                                    accion = Accion(actual.linea, f"Ensamblar - componente {str(actual.componente)}", tiempoSimulacion)
                                    estadoEnsamblaje = False
                                    actual.ensamblando = False
                                    actual.estado = True
                                    lineaProduccion.cont_tmp_Ensamblaje = 1
                                    estadoEnsambleUltimo = True

                                elif int(lineaProduccion.cont_tmp_Ensamblaje) < int(lineaProduccion.tmp_Ensamblaje):
                                    accion = Accion(actual.linea, f"Ensamblar - componente {str(actual.componente)}", tiempoSimulacion)
                                    lineaProduccion.cont_tmp_Ensamblaje += 1
                                
                            else: #Para las lineas de produccion que no estan ensamblando
                                accion = Accion(actual.linea, "No hacer nada", tiempoSimulacion)
                else:
                    busquedaSiguiente = producto.listaElaboracion.getNodoElaboracionDespues(actual)
                    if actual.estado == True and busquedaSiguiente == None: #Si ya se completo la elaboracion no hace nada
                        accion = Accion(actual.linea, "No hacer nada", tiempoSimulacion)
                    elif actual.estado == True and busquedaSiguiente != None: #Si ya se completo pero si existe una instruccion antes no va a hacer nada
                        pass
                    else:
                        if estadoEnsamblaje == False and estadoEnsambleUltimo == False: #Para cuando todas las lineas de produccion tengan que seguir moviendose
                            lineaProduccion = listaLineasProduccion.getLineaProduccion(actual.linea)
                            
                            #Verificar si ya ha llegado al componente destino
                            if int(lineaProduccion.contadorComponente) == int(actual.componente):
                                #Verificar si la instruccion anterior ya ha sido completada
                                if actual.anterior == None or actual.anterior.estado == True:
                                    estadoEnsamblaje = True
                                    actual.ensamblando = True
                                    #Funcion de ensamblaje
                                    lineaProduccion = listaLineasProduccion.getLineaProduccion(actual.linea)
                                    #Si tiene que ir sumando
                                    if int(lineaProduccion.cont_tmp_Ensamblaje) == int(lineaProduccion.tmp_Ensamblaje):
                                        accion = Accion(actual.linea, f"Ensamblar - componente {str(actual.componente)}", tiempoSimulacion)
                                        estadoEnsamblaje = False
                                        actual.ensamblando = False
                                        actual.estado = True
                                        lineaProduccion.cont_tmp_Ensamblaje = 1
                                        estadoEnsambleUltimo = True

                                    elif int(lineaProduccion.cont_tmp_Ensamblaje) < int(lineaProduccion.tmp_Ensamblaje):
                                        accion = Accion(actual.linea, f"Ensamblar - componente {str(actual.componente)}", tiempoSimulacion)
                                        lineaProduccion.cont_tmp_Ensamblaje += 1

                                else:#Si no ha sido completada se tiene que esperar a que se complete y por ende no se hace nada
                                    accion = Accion(actual.linea, "No hacer nada", tiempoSimulacion)

                            #Si tiene que ir sumando
                            elif int(lineaProduccion.contadorComponente) < int(actual.componente):
                                lineaProduccion.contadorComponente += 1
                                accion = Accion(actual.linea, f"Mover brazo a componente {str(lineaProduccion.contadorComponente)}", tiempoSimulacion)

                            #Si tiene que ir restando
                            elif int(lineaProduccion.contadorComponente) > int(actual.componente):
                                lineaProduccion.contadorComponente -= 1
                                accion = Accion(actual.linea, f"Mover brazo a componente {str(lineaProduccion.contadorComponente)}", tiempoSimulacion)

                        elif estadoEnsamblaje == True and actual.ensamblando == True: #este es el nodo que esta ensamblando
                            lineaProduccion = listaLineasProduccion.getLineaProduccion(actual.linea)
                            #Si tiene que ir sumando
                            if int(lineaProduccion.cont_tmp_Ensamblaje) == int(lineaProduccion.tmp_Ensamblaje):
                                accion = Accion(actual.linea, f"Ensamblar - componente {str(actual.componente)}", tiempoSimulacion)
                                estadoEnsamblaje = False
                                actual.ensamblando = False
                                actual.estado = True
                                lineaProduccion.cont_tmp_Ensamblaje = 1
                                estadoEnsambleUltimo = True

                            elif int(lineaProduccion.cont_tmp_Ensamblaje) < int(lineaProduccion.tmp_Ensamblaje):
                                accion = Accion(actual.linea, f"Ensamblar - componente {str(actual.componente)}", tiempoSimulacion)
                                lineaProduccion.cont_tmp_Ensamblaje += 1

                            
                        else: #Para las lineas de produccion que no estan ensamblando
                            accion = Accion(actual.linea, "No hacer nada", tiempoSimulacion)

                #agregamos la accion resultante a la lista de acciones
                if accion != None:
                    listaAccionesSimulacion.setNodoAccion(accion)
                accion = None

                actual = actual.siguiente
        estadoEnsambleUltimo = False
    
    producto.listaElaboracion.resetearEstadosNodoListaElaboracion() #Resetear los estados la lista de elaboraciones del producto porque todos estan TRUE al finalizar el metodo
    listaLineasProduccion.resetearEstadosNodoListaLineaProduccion() #Resetear los estados de las lineas de produccion
    listaAccionesSimulacion.showAcciones()
    producto.listaAccionesProducto = listaAccionesSimulacion # Guardar la lista de acciones en la simulacion en las acciones de cada producto
    listaAccionesSimulacion = Lista_Doble() # Reiniciar la lista de acciones de Simulaciones general para poder realizar otras simulaciones a futuro.
    
    #Verificar si se trata de una simulacion individual o una en conjunto
    if simulacionActual.nombreSimulacion == "Simulacion_Individual":
        productoAuxiliar = ProductoSimulacion(producto.nombre, producto.listaElaboracion, producto.listaAccionesProducto)#Este producto auxiliar lo genero para no tocar directamente el producto que tengo en la listaProductos
        simulacionActual.listaProductos.setNodo(productoAuxiliar) #Al objeto simulacionActual le añado un producto mas a su lista de productos
    else:
        simulacionActual.listaProductos.getProducto(producto.nombre).listaAccionesProducto = producto.listaAccionesProducto


    print("funciono")

def escribirArchivoXml():
    global simulacionActual
    #<SalidaSimulacion>
    root = ET.Element("SalidaSimulacion")
    #<Nombre>
    ET.SubElement(root, "Nombre").text = f"{str(simulacionActual.nombreSimulacion)}"
    #<ListadoProductos>
    listadoProductos = ET.SubElement(root, "ListadoProductos")
    actual = simulacionActual.listaProductos.primero
    while(actual != None):
        #<Producto>
        producto = ET.SubElement(listadoProductos, "Producto")
        #<Nombre>
        ET.SubElement(producto, "Nombre").text = f"{str(actual.nombre)}"
        #<TiempoTotal>
        ET.SubElement(producto, "TiempoTotal").text = f"{str(actual.listaAccionesProducto.ultimo.tmp_Accion)}"
        #<ElaboracionOptima>
        elaboracionOptima = ET.SubElement(producto, "ElaboracionOptima")

        actual2 = actual.listaAccionesProducto.primero
        while(actual2 != None):
            #<Tiempo>
            tiempoElaboracion = ET.SubElement(elaboracionOptima, "Tiempo", NoSegundo = f"[{str(actual2.tmp_Accion)}]")
            #<LineaEnsamblaje>
            lineaEnsamblaje = ET.SubElement(tiempoElaboracion, "LineaEnsamblaje", NoLinea = f"[{str(actual2.linea)}]").text = f"{str(actual2.mov)}" 
            actual2 = actual2.siguiente
        actual = actual.siguiente
    
    arbol = ET.ElementTree(root)
    arbol.write(f"{pathlib.Path(__file__).parent.absolute()}/{str(simulacionActual.nombreSimulacion)}.xml")
    print("Archivo de salida xml creado con exito.")

#===================================Metodo para Generar reporte HTML============================================
def generarReporteHtml():
    global simulacionActual
    if simulacionActual.listaProductos != None:
        actual = simulacionActual.listaProductos.primero
        while(actual != None):
            #abrir o crear el reporte
            f = open(f'{actual.nombre}.html','w', encoding='utf-8')
            cuerpo = f'''<!doctype html>
                <html lang="en">

                <head>
                <!-- Required meta tags -->
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">

                <!-- Bootstrap CSS -->
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
                    integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

                <title>REPORTE DE PRODUCTO</title>
                </head>

                <body style="background-color: lightseagreen;">
                <div class="container-fluid container p-3 my-3 bg-dark text-white">
                    <div class="row">
                    <div class="col-12" style="text-align: center; ">
                        <h1>REPORTE DE PRODUCTO</h1>
                    </div>
                    </div>
                </div>
                <div class="container-fluid" style="background-color: rgb(255, 255, 255); ">
                    <div class="row justify-content-md-center">
                    <div>
                        <h3>Nombre del producto: {actual.nombre}</h3>
                    </div>
                    </div>
                    <div class="row justify-content-md-center">
                    <div>
                        <h3>El producto {actual.nombre} se puede elaborar optimamente en {actual.listaAccionesProducto.ultimo.tmp_Accion}</h3>
                    </div>
                    </div>
                    <div class="row justify-content-md-center">
                    <div class="col-md-auto">
                        <h2 style="text-decoration: underline tomato;">Listado de procedimientos</h2>
                    </div>
                    </div>
                    <div class="row justify-content-md-center">
                    <div class="col-md-auto">
                        <table class="table table-bordered table-striped text-center table-hover table-responsive"
                        style="text-align: center; width: 600px;">
                        <thead>
                            <tr class="table-dark">
                            <th>Segundo</th>
                            <th>Movimiento</th>
                            <th>Linea</th>
                            
                            </tr>
                        </thead>
                        <tbody>
                            '''
            actual2 = actual.listaAccionesProducto.primero
            while(actual2 != None):
                cuerpo +=  f'''
                            <tr>
                            <td class="table-info">{actual2.tmp_Accion}</td>
                            <td class="table-success">{actual2.mov}</td>
                            <td class="table-success">{actual2.linea}</td>
                            </tr>'''
                
                actual2 = actual2.siguiente
            
            cuerpo += '''
                        </tbody>
                        </table>
                    </div>
                    </div>
                    </div>
                <div class="container-fluid container p-3 my-3 bg-dark text-white">
                    <div class="row">
                    <div class="col-12" style="text-align: center; ">
                        <h1></h1>
                    </div>
                    </div>
                </div>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
                    integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
                    crossorigin="anonymous"></script>
                </body>

                </html>'''
            

            f.write(cuerpo)
            f.close
            webbrowser.open_new_tab(f'{actual.nombre}.html')
            
            actual = actual.siguiente
    else:
        messagebox.showwarning('ADVERTENCIA', 'No se selecciono ningun archivo.')

#==================Metodo para generar reporte Graphviz de la lista de elaboración de cada producto=======================================
def generarReporteGraphviz(nombreProducto):
    global listaProductos

    producto = listaProductos.getProducto(nombreProducto)
    if producto != None:
        #Aquí creamos el objeto Digraph en donde le dicimos que su formato de salida sera de png
        dot = Digraph(comment='The Round Table')
        
        dot.attr('node', shape = "underline")
        dot.node('titulo', label= f'{producto.nombre}')
        dot.attr('node', shape = "rectangle")
        actual2 = producto.listaElaboracion.primero
        while(actual2 != None):
            #Creando los nodos donde antes de la "," hace referencia al id del nodo y después de la "," al valor del label osea
            #el valor que aparece impreso en el nodo.
            dot.node(f'{str(actual2)}',f'L{str(actual2.linea)}C{str(actual2.componente)}')
            
            if actual2.siguiente != None:
                #Creando las uniones entre los nodos
                dot.edge(f'{str(actual2)}', f'{str(actual2.siguiente)}',constraint = 'false')

            actual2 = actual2.siguiente
        
        #aquí creamos los archivos tanto el .DOT como el .Output que en este caso le dijimos sería de formato png.
        dot.render(f'Lista_Cola_{producto.nombre}', view = True)
            
    else:
        messagebox.showwarning('ADVERTENCIA', 'No se puede generar un reporte de cola ya que no existe el producto solicitado.')
    

class VentanaMenu:
    def __init__(self):
        self.txt = None
        self.ventana = Tk()
        self.ventana.title("Menu Principal")
        #Posicionar ventana en el centro
        self.ancho_ventana = 1300
        self.alto_ventana = 500

        self.x_ventana = self.ventana.winfo_screenwidth() // 2 - self.ancho_ventana // 2
        self.y_ventana = self.ventana.winfo_screenheight() // 2 - self.alto_ventana // 2

        self.posicion = str(self.ancho_ventana) + "x" + str(self.alto_ventana) + "+" + str(self.x_ventana) + "+" + str(self.y_ventana)
        self.ventana.geometry(self.posicion)

        self.ventana.configure(bg = 'sky blue')
        self.ventana.resizable(False, False)

        # Por medio de esto accedo a lo que sucede al dar click sobre la X para cerrar la ventana
        self.ventana.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Se crea el menú de la ventana / el tearoff = 0 es para que no se me cree un submenú al darle click al "----" que me sale en los cascade
        self.miMenu = Menu(self.ventana, tearoff=0)
        self.ventana.configure(menu=self.miMenu)

        #Creando una sección/SubMenú esta es la barrita que aparecere arriba en la ventana
        self.miMenu.add_command(label="Cargar maquina", command=self.cargarMaquina)
        self.miMenu.add_command(label="Cargar simulación", command=self.cargarSimulacion)
        self.miMenu.add_command(label="Reportes", command=self.reporte)
        self.miMenu.add_command(label="Ayuda", command=self.infoEstudiante)

        #ComboBox
        listadoNombreImagenes = []
        self.myComboBox = ttk.Combobox(self.ventana, state= "readonly", value = listadoNombreImagenes)
        self.myComboBox.bind("<<ComboboxSelected>>", self.comboClick)
        self.myComboBox.place(x=200, y = 10)

        #Labels
        self.label1 = Label(self.ventana, text="Escoga un producto ", font = ("Times New Roman", 15))
        self.label1.place(x=10, y = 10)
        # Title Label
        self.Label2 = Label(self.ventana, 
                            text = "Componentes necesarios",
                            font = ("Times New Roman", 15), 
                            background = 'gray', 
                            foreground = "black").place(x = 10,
                                                        y = 50)
        # Table Label
        self.Label3 = Label(self.ventana, 
                            text = "Tabla de resultados simulacion",
                            font = ("Times New Roman", 15), 
                            background = 'gray', 
                            foreground = "black").place(x = 400,
                                                        y = 50)
        # Time Label
        self.Label4 = Label(self.ventana, 
                            text = "Tiempo de ensamblado: ",
                            font = ("Times New Roman", 15), 
                            background = 'SteelBlue1', 
                            foreground = "black")
        self.Label4.place(x = 400,y = 400)

        #Buttons
        self.btnProcesar = Button(self.ventana, text="Procesar", command=self.procesar)
        self.btnProcesar.place(x=400, y = 10)
        self.btnReporte = Button(self.ventana, text = "Generar reporte de cola", command=self.generarReporteCola)
        self.btnReporte.place(x = 500, y = 10)

        #scrolledtext
        # Creating scrolled text 
        # area widget
        self.text_area = scrolledtext.ScrolledText(self.ventana, 
                                                wrap = tkinter.WORD, 
                                                width = 30, 
                                                height = 13, 
                                                font = ("Times New Roman",
                                                        15))
        self.text_area.configure(state = 'disable')
        self.text_area.place(x=10, y = 90) 

        #Frame
        self.wrapper1 = Frame(self.ventana)
        self.wrapper1.place(x = 400, y = 90, width=890, height=300)
        
        #TreeView o tabla dentro del Frame wrapper1
        self.trv = ttk.Treeview()
        self.yScrollball = ttk.Scrollbar()
        self.xScrollball = ttk.Scrollbar()

        #ProgressBar
        self.my_ProgressBar = ttk.Progressbar(self.ventana, orient=HORIZONTAL, length=1200, mode='determinate')
        self.my_ProgressBar.pack(side=BOTTOM, pady = 20)

        self.ventana.mainloop()

    #Metodos para el ProgressBarr
    def step(self):
        self.my_ProgressBar['value'] += 25
        self.ventana.update()
        time.sleep(1)
    def stop(self):
        self.my_ProgressBar.stop()

    #Metodo para procesar individualmente cada producto y mostrarlo en la interfaz
    def procesar(self):
        global simulacionActual
        self.stop()#Reiniciar barra de progreso

        nombreProducto = self.myComboBox.get()

        if nombreProducto != "":
            listaProductosSimulacion = Lista_Doble()
            simulacionActual = Simulacion("Simulacion_Individual", listaProductosSimulacion) # Reiniciar la simulacion Actual
            realizar_Simulacion(nombreProducto) 
            self.step()
            escribirArchivoXml()
            self.step()
            self.text_area.configure(state = 'normal')
            self.text_area.delete("1.0", tkinter.END) 
            self.text_area.configure(state = 'disable')
            self.mostrarComponenteNecesarios()
            self.step()
            self.crearListaAcciones()
            self.Label4["text"] = f"Producto: {nombreProducto} - Tiempo de ensamblado: {str(simulacionActual.listaProductos.primero.listaAccionesProducto.ultimo.tmp_Accion)}"
            self.step()

        else:
            print("El producto seleccionado no existe")
            messagebox.showwarning('ADVERTENCIA', 'El producto seleccionado no existe.')

    def cargarMaquina(self):
        global listaProductos
        global listaLineasProduccion
        listaLineasProduccion = Lista_Doble()
        listaProductos = Lista_Doble()
        direccion = extraerDireccionArchivo()
        if direccion == None:
            messagebox.showwarning('ADVERTENCIA', 'No se ha seleccionado ningun archivo.')
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
        if listaProductos.primero == None:
            print("No se ha cargado la maquina para hacer su simulación.")
            messagebox.showwarning('ADVERTENCIA', 'No se ha cargado la maquina para hacer su simulación.')
        else:
            direccion = extraerDireccionArchivo()
            if direccion == None:
                pass
            else:
                print("Cargando Simulacion")
                cargar_Simulacion(direccion)
                generarReporteHtml()
    
    def reporte(self):
        generarReporteHtml()

    def infoEstudiante(self):
        global my_Image
        self.top = Toplevel()
        self.top.title("Ayuda")
        #Posicionar ventana en el centro
        self.ancho_ventana = 600
        self.alto_ventana = 500

        self.x_ventana = self.top.winfo_screenwidth() // 2 - self.ancho_ventana // 2
        self.y_ventana = self.top.winfo_screenheight() // 2 - self.alto_ventana // 2

        self.posicion = str(self.ancho_ventana) + "x" + str(self.alto_ventana) + "+" + str(self.x_ventana) + "+" + str(self.y_ventana)
        self.top.geometry(self.posicion)

        self.top.configure(bg = 'sky blue')
        self.top.resizable(False, False)

        #Label
        self.Label1Top = Label(self.top, 
                            text = "DIEGO ANDRÉ MAZARIEGOS BARRIENTOS",
                            font = ("Comic Sans MS", 15), 
                            background = 'SteelBlue1', 
                            foreground = "black")
        self.Label1Top.pack(side=TOP)
        self.Label1Top = Label(self.top, 
                            text = "202003975",
                            font = ("Comic Sans MS", 15), 
                            background = 'SteelBlue1', 
                            foreground = "black")
        self.Label1Top.pack(side=TOP)
        self.Label1Top = Label(self.top, 
                            text = "Introducción a la programación y computación 2 sección 'D'",
                            font = ("Comic Sans MS", 15), 
                            background = 'SteelBlue1', 
                            foreground = "black")
        self.Label1Top.pack(side=TOP)
        self.Label1Top = Label(self.top, 
                            text = "Ingenieria en Ciencias y Sistemas",
                            font = ("Comic Sans MS", 15), 
                            background = 'SteelBlue1', 
                            foreground = "black")
        self.Label1Top.pack(side=TOP)
        self.Label1Top = Label(self.top, 
                            text = "4to Semestre",
                            font = ("Comic Sans MS", 15), 
                            background = 'SteelBlue1', 
                            foreground = "black")
        self.Label1Top.pack(side=TOP)

        #Label Image
        my_Image = ImageTk.PhotoImage(Image.open(f"{pathlib.Path(__file__).parent.absolute()}/perfil.jpg"))
        self.my_LabelImg = Label(self.top, image = my_Image).pack(side=TOP)

        
        
        #Label explicacion app

        self.Label1Top = Label(self.top, 
                    text = "Acerca de",
                    font = ("Cambria", 15), 
                    background = 'SteelBlue1', 
                    foreground = "black")
        self.Label1Top.pack(side=TOP)

        self.Label1Top = Label(self.top, 
                            text = '''El software denominado 'Proyecto 2' fue desarrollado para la empresa \n Digital Intelligence, S. A. en busca de simular el funcionamiento de una \nmaquina de ensamblaje en la fabrica  con “n” líneas de ensamblaje y cada línea de ensamblaje con “m” posibles \ncomponentes a seleccionar de forma que pueda predecir el tiempo “óptimo” para elaborar \ncualquier producto que pueda ser ensamblado en la máquina. ''',
                            font = ("Cambria", 9), 
                            background = 'SteelBlue1', 
                            foreground = "black")
        self.Label1Top.pack(side=TOP)


        #Button
        self.btn2 = Button(self.top, text = "Cerrar ventana ayuda", command=self.top.destroy).pack(side=BOTTOM)

    #Metodo para crear una lista dentro del Frame "wrapper1" and show a list of actions.
    def crearListaAcciones(self):
        global simulacionActual
        productoSimulado = simulacionActual.listaProductos.primero
        #Uso el destroy para reiniciar la tabla si es que estuviese alguna de un producto simulado anteriormente
        self.trv.destroy()
        self.yScrollball.destroy()
        self.xScrollball.destroy()
        
        #Creando lista para las columnas OJO aquí se crea una lista porque este widget solo acepta listas
        #tanto para declarar sus columnas como para declarar sus values en cada arrow.
        columns = []
        columns.append("segundo")
        primerSegundo = 1
        actual = productoSimulado.listaAccionesProducto.primero
        while primerSegundo == 1:
            primerSegundo = int(actual.tmp_Accion)
            if primerSegundo != 1:
                break
            columns.append(str(actual.linea))
            actual = actual.siguiente

        #Creando el objeto Treevie o tabla con sus respectivas columnas y propiedades
        self.trv = ttk.Treeview(self.wrapper1, columns=columns,show="headings", height="6")
        self.trv.place(x = 0, y = 0, width=890, height=300)
        
        #Esta parte es basicamente esto -> trv.column( "1", anchor=CENTER)
        primerSegundo = 1
        actual = productoSimulado.listaAccionesProducto.primero
        self.trv.column("segundo", anchor=CENTER) #Esta linea corresponde unicamente para la columna de los segundos
        while primerSegundo == 1:
            primerSegundo = int(actual.tmp_Accion)
            if primerSegundo != 1:
                break
            self.trv.column( str(actual.linea), anchor=CENTER)
            actual = actual.siguiente
        
        #Esta parte es basicamente esto -> trv.heading("1", text="Customer ID1")
        #Header's of our table
        primerSegundo = 1
        actual = productoSimulado.listaAccionesProducto.primero
        self.trv.heading("segundo", text="Segundos")
        while primerSegundo == 1:
            primerSegundo = int(actual.tmp_Accion)
            if primerSegundo != 1:
                break
            self.trv.heading(str(actual.linea), text=f"Linea {str(actual.linea)}")
            actual = actual.siguiente

        #Part llenado of data -> trv.insert('', 'end', values = (1,2,3))
        #Recordar que se inserta por filas
        #here we need to make a list because the values only admitt list's in the moment of instert the arrows
        values = []
        segundoActual = 1
        segundoSiguiente = 1
        actual = productoSimulado.listaAccionesProducto.primero
        while actual != None:
            values = []
            insertar = False
            while actual != None:
                segundoActual = int(actual.tmp_Accion)
                if (segundoActual == segundoSiguiente) and (insertar == False):
                    segundoSiguiente += 1
                    values.append(str(actual.tmp_Accion))
                    insertar = True
                if segundoActual == segundoSiguiente:
                    insertar = False
                    break
                values.append(str(actual.mov))
                actual = actual.siguiente
            #make arrow
            self.trv.insert('', 'end', values = values)
        


        #Part of Scrollbar's
        #Vertical Scrollbar
        self.yScrollball = ttk.Scrollbar(self.wrapper1, orient = "vertical", command=self.trv.yview)
        self.yScrollball.pack(side=RIGHT, fill=Y)

        #Horizontal Scrollbar
        self.xScrollball = ttk.Scrollbar(self.wrapper1, orient = "horizontal", command=self.trv.xview)
        self.xScrollball.pack(side=BOTTOM, fill=X)

        #agregar los scroll a la configuarcion de la tabla
        self.trv.configure(yscrollcommand=self.yScrollball.set, xscrollcommand=self.xScrollball.set)
        
    #Metodo para llenar el text_area de componentes necesarios
    def mostrarComponenteNecesarios(self):
        global simulacionActual
        self.text_area.configure(state = 'normal')
        texto = ""
        #Primer producto en la simulacion actual
        actual = simulacionActual.listaProductos.primero
        while(actual != None):
            #Primera elemento de listaElaboracion de ese producto
            actual2 = actual.listaElaboracion.primero
            while(actual2 != None):
                texto += f"Linea {actual2.linea} -> Componente {actual2.componente} \n"
                actual2 = actual2.siguiente
            actual = actual.siguiente
        self.text_area.insert("1.0", texto)
        self.text_area.configure(state = 'disable')

    def generarReporteCola(self):
        nombreProducto = self.myComboBox.get()

        if nombreProducto != "":
            generarReporteGraphviz(nombreProducto)
        else:
            print("El producto seleccionado no existe")
            messagebox.showwarning('ADVERTENCIA', 'El producto seleccionado no existe.')

    #se manda a llamar cuando se selecciona un item del combo.
    def comboClick(self, event):
        pass

    # Metodo para cerrar la ventana 
    def on_closing(self):
        if messagebox.askokcancel("Cerrar Programa", "Seguro que desea Salir?"):
            self.ventana.quit()
