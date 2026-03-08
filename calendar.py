import op_calendar
import json
import os
from colorama import Fore, Style, init

init(autoreset=True) # Inicia colorama para Linux/Windows

c = Fore.LIGHTCYAN_EX # Definimos constantes para evitar funciones hardcodeadas.
y = Fore.LIGHTYELLOW_EX
r = Style.RESET_ALL
w = Fore.LIGHTWHITE_EX
red = Fore.LIGHTRED_EX

print(f"""{y}
 ██████╗░░█████╗░██╗░░░░░███████╗███╗░░██╗██████╗░░█████╗░██████╗░██╗░█████╗░
██╔════╝░██╔══██╗██║░░░░░██╔════╝████╗░██║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗
██║░░░░░░███████║██║░░░░░█████╗░░██╔██╗██║██║░░██║███████║██████╔╝██║██║░░██║
██║░░░░░░██╔══██║██║░░░░░██╔══╝░░██║╚████║██║░░██║██╔══██║██╔══██╗██║██║░░██║
╚██████╗░██║░░██║███████╗███████╗██║░╚███║██████╔╝██║░░██║██║░░██║██║╚█████╔╝
░╚═════╝░╚═╝░░╚═╝╚══════╝╚══════╝╚═╝░░╚══╝╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░╚════╝░
{r}""")

# Definimos una variable que guarde el comando segun el OS.
if os.name == 'nt':
    clst = 'cls'
elif os.name == 'posix':
    clst = 'clear'


# Definimos listas con los dias de cada mes, si le pasamos el [mes] a esta lista devolvera los días que contiene ese mes.
max_dias_por_mes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
max_dias_por_mes_bisiesto = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

patron = r"^([01]\d|2[0-3]):([0-5]\d)$" # Definimos un patron que luego lo usaremos para validar la entrada de la fecha usando regex.

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Evento(): # Definimos la clase Evento.

    # Definimos un método reservado en el que indicamos todos los atributos/propiedades.
    def __init__(self, nombre, hora=None, descripcion=""): # Este método estandar es el constructor de la clase, se encarga de inizializar el objeto. 
        self.nombre = nombre 
        self.hora = hora
        self.descripcion = descripcion
            
    def __str__(self): # Definimos otro método reservado en el que se especifica la representación del string del objeto. Cuando hagas un print del objeto se vera de esta forma:
        return(f"Hora: [{self.hora}] | Nombre: {self.nombre} | Descripción: {self.descripcion}")
    
    def visual_evento(self): # Definimos otro método para estructurar la información en forma de diccionario. Esto es util para almacenarla.
        return {
            "nombre": self.nombre,
            "hora": self.hora,
            "descripcion": self.descripcion
        }
            
    def mod_nombre(self, nuevo_nombre): # Este método se usara para cambiar el nombre del evento.
        self.nombre = nuevo_nombre
    
    def mod_desc(self, nueva_descripcion): # Este método se usara para cambiar la descripción del evento.
        self.descripcion = nueva_descripcion
    
    def mod_hora(self, nueva_hora): # Este método se usara para cambiar la hora del evento.
        self.hora = nueva_hora
                    
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# CREACIÓN ARCHIVO:
# Hay dos condiciones, si el archivo existe lo va a leer y si el archivo no existe lo crea:
if os.path.exists("calendario.json"):
    with open("calendario.json", "r") as archivo:
        datos = json.load(archivo) # Carga variables las cuales su persistencia es necesaria.
        año = datos["año"]
        max_dias = datos["max_dias"]
        calendar = datos["calendar"]
        
    # VAMOS A TRANSFORMAR DE FORMATO DE TEXTO A OBJETO (cargar los diccionarios al objeto).
    # Usamos .items() para que 'fecha' sea la variable key y 'lista_dicts' sea el value (la lista de diccionarios que viene del JSON).
    for fecha, lista_dicts in calendar.items():
        # Con (**d) estamos pasando todas las keys a __init__, seria como hacer esto (Evento(nombre=d["nombre"], hora=d["hora"], desc=d["desc"])). 
        # (**d) le dice a la clase "Extrae cada key y úsala como el atributo", "Extrae cada value y asignalo al parametro".
        # Para que (**d) funcione, los keys y los atributos deben llamarse exactamente igual.
        calendar[fecha] = [Evento(**d) for d in lista_dicts] # "d" itera cada valor de la lista "lista_dicts" y con esos diciconarios son pasados a la clase Evento para que se vuelvan objetos.
    print(f"{y}\n>>> Datos cargados desde el archivo correctamente.\nAbriendo calendario para al año {año}{r}")
else: 
    # Vamos a pedir de que año es este calendario
    while True:
        try:
            año = int(input(f"{c}Para que año es este calendario? {r}"))
            break
        except ValueError:
            print(f"{red}El valor ingresado no es valido.{r}")
            continue
    
    # CALCULADORA AÑO BISIESTO
    # Calculamos si [año] es bisiesto:
    es_bisiesto = (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)
    if es_bisiesto:
        max_dias = max_dias_por_mes_bisiesto
        print(f"{y}Este año es bisiesto{r}")
    else:
        max_dias = max_dias_por_mes
        print(f"{y}Este año no es bisiesto{r}")
        
    calendar = {}
    # Nuestro calendar tendra esta estructura:
    # Nuestro calendar se va a componer de una variable (key) y una lista (value). La lisat (value) va a almacenar otros diccionarios.
    #############################################################################################
    # "calendar": {                                                                             #
    #     "1-28": [                                                                             #
    #         {"nombre": "Cena", "hora": "21:00", "descripcion": "Con amigos"},                 #
    #         {"nombre": "Gimnasio", "hora": "08:00", "descripcion": ""}                        #
    #     ],                                                                                    #
    #     "2-14": [                                                                             #
    #         {"nombre": "San Valentín", "hora": "20:00", "descripcion": "Cena romántica"}      #
    #     ]                                                                                     #
    # }                                                                                         #
    #############################################################################################
    
    print(f"{y}\n>>> No se encontró archivo previo. Creando calendario nuevo.{r}")
    

# Inciamos bucle de menu principal:
while True:
    
    print(f"""{c}
****************************
*  1.Añadir Evento         *
*  2.Eliminar Evento       *
*  3.Modificar Evento      *
*  4.Consultar calendario  *
*  5.Buscar evento         *
*  6.Cerrar Calendario     *
****************************
    {r}""")
    
    try:
        op = int(input(f"{c}Que deseas hacer: {r}")) # Indagamos que operación desea.
    except ValueError:
        print(f"{red}El dato ingresado es invalido{r}")
        continue
    
    # Creamos condicionea para llamar a cada función:
    if op == 1:
        op_calendar.añadir_evento(calendar, max_dias, patron, clst, Evento)
        continue
    elif op == 2:
        op_calendar.eliminar_evento(calendar, max_dias, clst)
        continue
    elif op == 3:
        op_calendar.mod_evento(calendar, max_dias, clst, patron)
    elif op == 4:
        op_calendar.consultar_evento(calendar, max_dias, clst)
    elif op == 5: 
        op_calendar.buscar_evento(calendar)
        
    elif op == 6:
        calendar_guardable = {} # Definimos un diccionario vacio donde estructuraremos calendar para ser guardardo.
        # La función ".items()" devuelve el key por un lado y el value por otro.
        for fecha, lista_objetos in calendar.items(): # Creamos un bucle para que a fecha se le asigne el valor de la key y que a lista_objetos se le asigne el valor del value.
            # Para cada fecha (key) en calendar_guardable,  vamos a guardar el objeto tratado usando la función viasual_evento para que se almacene en un formato correcto.
            calendar_guardable[fecha] = [obj.visual_evento() for obj in lista_objetos]  # Por cada iteración del for "obj" se transforma en el objeto que esta iterando.
        
        datos_guardar = { # En datos guardar definimos todo lo que queremos que se guarde y con que estructura.
            "año": año,
            "max_dias": max_dias,
            "calendar": calendar_guardable
        }
        
        with open("calendario.json", "w") as f: # Guardamos las variables que necesitan persistencia en el archivo:
            json.dump(datos_guardar, f)
        print(f"{y}>>> Datos guardados. Saliendo...{r}")
        break
    else:
        print(f"{red}Entrada no valida, solo se permiten numeros del 1-4. Vuelve a intentarlo{r}")
        continue
   


