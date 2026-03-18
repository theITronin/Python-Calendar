from colorama import Fore, Style
import os
import re 

c = Fore.LIGHTCYAN_EX # We define constants to avoid hardcoded values.
y = Fore.LIGHTYELLOW_EX
w = Fore.LIGHTWHITE_EX
red = Fore.LIGHTRED_EX
r = Style.RESET_ALL

# We create this list to iterate using the month "nombres_meses[mes]", it will return the month name.
nombres_meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"] 


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////

# We define a function to request a date to optimize and clean the code; this way we avoid repeating code.
def pedir_fecha(clst, max_dias):
    while True:
        try:
            mes = int(input(f"{c}\nPulse {r}"+ f"{w}0 {r}"+ f"{c}para salir al menu principal.\nMes (1-12): {r}")) # We ask for the month.
            if mes < 0 or mes > 12: # We validate the month range. 0 is included because it will be used to exit to the main menu.                    
                print(f"{red}Mes inválido. Vuelve a intentarlo: {r}")   
                continue
            elif mes == 0:
                os.system(clst)
                return(None)
        except ValueError:  # We use try/except to validate integer-only input.
            print(f"{red}El valor ingresado no es valido.{r}")
            continue
        while True:
            try:
                dia = int(input(f"{c}\nPulse {r}"+ f"{w}0 {r}"+ f"{c}para salir al menu principal.\nDía: {r}")) # We ask for the day.
                if dia < 0 or dia > max_dias[mes]: # We validate the day range using the max_dias list with index [mes].
                    print(f"{red}Día inválido. Vuelve a intentarlo: {r}")
                    continue
                elif dia == 0:
                    os.system(clst)
                    return(None)
                else:
                    fecha = f"{mes}-{dia}" # We define date as a string that should not be modified.
                    return(fecha) # We return the date to work with it already structured as a string.
            except ValueError: # We validate non-integer input.
                print(f"{red}El valor ingresado no es valido.{r}")
                continue

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////

def añadir_evento(calendar, max_dias, patron, clst, Evento): 
    
    fecha = pedir_fecha(clst, max_dias) # We call the pedir_fecha function.
    if fecha is None:
        return(None)
    if fecha not in calendar: # If the date is not in the calendar, we create the key (fecha).
        calendar[fecha] = [] # We assign an empty list as the value.
        
    while True:
        nombre = str(input(f"{c}\nSi quieres salir pulsa" f"{w}'Enter'{r}" f"\n{c}Nombre evento: {r}")).strip() # We ask for the event name.
        if not nombre: # We check if the user pressed Enter.
            os.system(clst)
            return(None)
        duplicado = False # We define the variable as False.
        for evento in calendar[fecha]:  # Loop through events on that date.
            if evento.nombre.lower() == nombre.lower(): #
                print(f"{red}Este evento ya existe. Intentalo de nuevo{r}")
                duplicado = True # If names match, mark as duplicate.
                break
        if duplicado: 
            continue
                    
        descripcion = str(input(f"{c}\nSi quieres salir pulsa" f"{w}'Enter'{r}" f"\n{c}Descripción: {r}")).strip() # We ask for the description.
        if not descripcion: # Check if Enter was pressed.
            os.system(clst)
            return(None)
            
        while True: 
            hora = str(input(f"{c}\nSi quieres salir pulsa" f"{w}'Enter'{r}" f"\n{c}Hora (ej. 14:30): {r}")).strip() # We ask for the time.
            if not hora: # Check if Enter was pressed.
                os.system(clst)
                return(None)
            if re.match(patron, hora): # We use regex to validate the time format.
                nuevo_evento = Evento(nombre, hora, descripcion) # Create event object.
                calendar[fecha].append(nuevo_evento) # Add the object to the list associated with the date.
                os.system(clst)
                return(calendar)
            else:
                print(f"{red}El formato ingresado no es valido. Ingrese un formato de hora valido.{r}")
                continue
            
            
            
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////// 
    
def eliminar_evento(calendar, max_dias, clst):
    
    fecha = pedir_fecha(clst, max_dias) # We call the pedir_fecha function.
    if fecha is None: # Check if user exited.
        return(None)
    if fecha not in calendar or not calendar[fecha]: # Validate if date exists in calendar.
        print(f"{red}No hay eventos en esa fecha{r}")
        return(None)
                
    while True:
        nombre_borrar = str(input(f"{c}\nSi quieres salir pulsa" f"{w}'Enter'{r}"f"\n{c}Que evento deseas eliminar: {r}")).strip() # Ask event name.
        for evento in calendar[fecha]: # Iterate through events.
            # Each time we check if the object's name matches the one to delete.
            if evento.nombre.lower() == nombre_borrar.lower():  
                evento_encontrado = evento # Store found object.
                calendar[fecha].remove(evento_encontrado) # Remove it from calendar.
                os.system(clst)
                return(calendar) # Return updated calendar.
            elif not nombre_borrar: # Check if Enter pressed.
                return(None)
        print(f"{red}El evento '{nombre_borrar}' no existe en esa fecha.{r}") # If not found.
                    
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////// 

def mod_evento(calendar, max_dias, clst, patron):
    fecha = pedir_fecha(clst, max_dias) # We call the pedir_fecha function.
    
    if fecha not in calendar or not calendar[fecha]: # Validate if date exists.
        print(f"{red}No hay eventos en esa fecha{r}")
        return(None)
            
    while True:
        evento_mod = str(input(f"{c}\nSi quieres salir pulsa " f"{w}'Enter'{r}"f"\n{c}Que evento deseas modificar: {r}")).strip() # Ask which event to modify.
        if fecha not in calendar or not calendar[fecha]:
            print(f"{red}No hay eventos en esa fecha{r}")
            return(None)
        for evento in calendar[fecha]: # Iterate through events.
            # Check if name matches.
            if evento.nombre.lower() == evento_mod.lower():  
                evento_encontrado = evento # Store object.
                os.system(clst)
                break
            elif not evento_mod: # Check if Enter pressed.
                return(None)
            else:
                print(f"{red}El evento '{evento_mod}' no existe en esa fecha.{r}")
                break
        while True: 
            print(
f"""{Fore.LIGHTCYAN_EX}
1. Nombre
2. Hora
3. Descripción
4. Salir
{Style.RESET_ALL}"""
                ) # We print a secondary menu.
            mod = int(input(f"{c}\nPulse "+ f"{w}0 "+ f"{c}Que quieres modificar: {r}")) # Ask what to modify.
            if mod == 0: # Check if user entered 0.
                return(None)
            elif mod == 1:
                nuevo_nombre = str(input(f"{c}\nSi quieres salir pulsa " f"{w}'Enter'" f"\n{c}Ingresa el nuevo nombre: {r}")).strip()  # Ask new name.
                evento_encontrado.mod_nombre(nuevo_nombre) # Call method to modify name.
                return(None)
            elif mod == 2:
                while True: 
                    nueva_hora = str(input(f"{c}\nSi quieres salir pulsa " f"{w}'Enter'" f"\n{c}Hora (ej. 14:30): {r}")).strip() # Ask new time.
                    if not nueva_hora:
                        return(None)
                    if re.match(patron, nueva_hora): # Validate format.
                        evento_encontrado.mod_hora(nueva_hora) # Modify time.
                        return(None)
                    else:
                        print(f"{red}El formato ingresado no es valido. Ingrese un formato de hora valido.{r}")
                        continue
            elif mod == 3:
                nueva_descripcion = str(input(f"{c}\nSi quieres salir pulsa " f"{w}'Enter'" f"\n{c}Descripción: {r}")).strip() # Ask new description
                evento_encontrado.mod_desc(nueva_descripcion) # Modify description.
                return(None)
            elif mod == 4:
                print(f"{y}Saliendo...{r}")
                return(None)
            else:
                print(f"{red}Entrada no valida, solo se permiten numeros del 1-4. Vuelve a intentarlo{r}")
                continue
                
                
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////

def consultar_evento(calendar, max_dias, clst):
    while True:
        try:
            mes = int(input(f"{c}\nPulse {r}"+ f"{w}0 {r}"+ f"{c}para salir al menu principal.\nMes (1-12): {r}")) # Ask month.
            if mes < 0 or mes > 12:      
                print(f"{red}Mes inválido. Vuelve a intentarlo: {r}")
                continue
            elif mes == 0:
                os.system(clst)
                return(None)
        except ValueError:   
            print(f"{red}El valor ingresado no es valido.{r}")
            continue
        while True:
            try:
                dia = int(input(f"{c}\nPulse {r}"+ f"{w}0 {r}"+ f"{c}para salir al menu principal.\n\nDía: {r}")) # Ask day.
                if dia < 0 or dia > max_dias[mes]:
                    print(f"{red}Día inválido. Vuelve a intentarlo: {r}")
                elif dia == 0:
                    os.system(clst)
                    return(None)
                else:
                    fecha = f"{mes}-{dia}" # Define date string.
                    print(f"{c}Eventos para el {dia} de {nombres_meses[mes]}:{r}") # Show events.
                    eventos = calendar.get(fecha, []) # Get events or empty list.
                    for evento in eventos: # Iterate events.
                        print(f"{w}- {evento}{r}") # Print event object.
                    while True:
                        salir = str(input(f"{c}Para salir pulsa {r}"+ f"{w}'Enter'{r}"))
                        if not salir:
                            os.system(clst)
                            return(None)
                        else:
                            print(f"{red}Valor no valido. Solo se puede ingresar Enter.{r}")
                            continue
            except ValueError:
                print(f"{red}El valor ingresado no es valido.{r}")
                continue
            
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////

def buscar_evento(calendar):
    while True:
        nombre_buscar = str(input(f"{c}\nSi quieres salir pulsa " f"{w}'Enter'{r}"f"\n{c}Que evento deseas buscar: {r}")).strip() # Ask event name to search.
        encontrado = False # We define a variable as False. 
        # The ".items()" function returns the key and the value.
        for fecha, lista_eventos in calendar.items(): # Loop through calendar.
            for evento in lista_eventos: # Iterate through events.
                if nombre_buscar.lower() in evento.nombre.lower():
                    m, d = fecha.split("-") # Split string into month and day.
                    print(f"El evento {evento.nombre} ha sido encontrado el {int(d)} de {nombres_meses[int(m)]}") # Print location
                    encontrado = True
                    break
            if encontrado:
                return(None)
        if not encontrado:
            print(f"\n{red}El evento '{nombre_buscar}' no ha sido encontrado.{r}")
            return(None)


