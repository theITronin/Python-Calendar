import op_calendar
import json
import os
from colorama import Fore, Style, init

init(autoreset=True) # Initializes colorama for Linux/Windows

c = Fore.LIGHTCYAN_EX # We define constants to avoid hardcoded values.
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

# We define a variable that stores the command depending on the OS.
if os.name == 'nt':
    clst = 'cls'
elif os.name == 'posix':
    clst = 'clear'


# We define lists with the days of each month; if we pass [month] to this list, it will return the number of days in that month.
max_dias_por_mes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
max_dias_por_mes_bisiesto = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

patron = r"^([01]\d|2[0-3]):([0-5]\d)$" # We define a pattern that we will later use to validate the time input using regex.

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Evento(): # We define the Event class.

    # We define a special method where we declare all attributes/properties.
    def __init__(self, nombre, hora=None, descripcion=""): # This standard method is the class constructor; it initializes the object. 
        self.nombre = nombre 
        self.hora = hora
        self.descripcion = descripcion
            
    def __str__(self): # We define another special method that specifies the string representation of the object. When you print the object, it will look like this:
        return(f"Hora: [{self.hora}] | Nombre: {self.nombre} | Descripción: {self.descripcion}")
    
    def visual_evento(self): # We define another method to structure the information as a dictionary. This is useful for storing it.
        return {
            "nombre": self.nombre,
            "hora": self.hora,
            "descripcion": self.descripcion
        }
            
    def mod_nombre(self, nuevo_nombre): # This method will be used to change the event name.
        self.nombre = nuevo_nombre
    
    def mod_desc(self, nueva_descripcion): # This method will be used to change the event description.
        self.descripcion = nueva_descripcion
    
    def mod_hora(self, nueva_hora): # This method will be used to change the event time.
        self.hora = nueva_hora
                    
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# FILE CREATION:
# There are two cases: if the file exists it will be read, and if it does not exist it will be created:
if os.path.exists("calendario.json"):
    with open("calendario.json", "r") as archivo:
        datos = json.load(archivo) # Loads variables whose persistence is necessary.
        año = datos["año"]
        max_dias = datos["max_dias"]
        calendar = datos["calendar"]
        
    # We are going to transform from text format to object format (load dictionaries into objects).
    # We use .items() so that 'fecha' is the key and 'lista_dicts' is the value (the list of dictionaries from the JSON).
    for fecha, lista_dicts in calendar.items():
        # With (**d) we pass all keys to __init__, it would be like doing this (Evento(nombre=d["nombre"], hora=d["hora"], desc=d["desc"])). 
        # (**d) tells the class: "Extract each key and use it as an attribute", "Extract each value and assign it to the parameter".
        # For (**d) to work, the keys and attributes must have exactly the same names.
        calendar[fecha] = [Evento(**d) for d in lista_dicts] # "d" iterates over each value in the list "lista_dicts" and those dictionaries are passed to the Event class to become objects.
    print(f"{y}\n>>> Datos cargados desde el archivo correctamente.\nAbriendo calendario para al año {año}{r}")
else: 
    # We are going to ask which year this calendar is for
    while True:
        try:
            año = int(input(f"{c}Para que año es este calendario? {r}"))
            break
        except ValueError:
            print(f"{red}El valor ingresado no es valido.{r}")
            continue
    
    # LEAP YEAR CALCULATOR
    # We calculate whether [year] is a leap year:
    es_bisiesto = (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)
    if es_bisiesto:
        max_dias = max_dias_por_mes_bisiesto
        print(f"{y}Este año es bisiesto{r}")
    else:
        max_dias = max_dias_por_mes
        print(f"{y}Este año no es bisiesto{r}")
        
    calendar = {}
    # Our calendar will have this structure:
    # Our calendar will be composed of a key and a list (value). The list (value) will store other dictionaries.
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
    

# We start the main menu loop:
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
        op = int(input(f"{c}Que deseas hacer: {r}")) # We ask which operation the user wants.
    except ValueError:
        print(f"{red}El dato ingresado es invalido{r}")
        continue
    
    # We create conditions to call each function:
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
        calendar_guardable = {} # We define an empty dictionary where we will structure the calendar to be saved.
        # The ".items()" function returns the key on one side and the value on the other.
        for fecha, lista_objetos in calendar.items(): # We create a loop so that 'fecha' gets the key and 'lista_objetos' gets the value.
            # For each date (key) in calendar_guardable, we will save the processed object using the visual_evento function so it is stored in the correct format.
            calendar_guardable[fecha] = [obj.visual_evento() for obj in lista_objetos]  # In each iteration of the loop, "obj" becomes the object being iterated.
        
        datos_guardar = { # In datos_guardar we define everything we want to save and its structure.
            "año": año,
            "max_dias": max_dias,
            "calendar": calendar_guardable
        }
        
        with open("calendario.json", "w") as f: # We save the variables that need persistence into the file:
            json.dump(datos_guardar, f)
        print(f"{y}>>> Datos guardados. Saliendo...{r}")
        break
    else:
        print(f"{red}Entrada no valida, solo se permiten numeros del 1-4. Vuelve a intentarlo{r}")
        continue
   


