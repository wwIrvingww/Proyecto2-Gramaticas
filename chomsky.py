import re

def chomsky(gramatica):
    # Paso 1: Agregar el símbolo inicial adicional S1
    print("***START***")
    previous_starter = gramatica['S']
    gramatica['V'].append("S1")
    gramatica['P']['S1'] = [[gramatica['S']]] 
    gramatica['S'] = "S1"
    print("\n \tSe agrego nuevo estado:" + gramatica['S'])
    print("\n \tSe concluyó el paso START")
    
    
    # Paso 2: Transformar producciones largas en binarias
    print("\n***BIN***")
    nuevas_producciones = {}
    nuevo_simbolo_idx = 1  # Para crear nuevas variables
    
    for variable, producciones in gramatica['P'].items():
        nuevas_producciones[variable] = []
        
        for produccion in producciones:
            # Si la producción tiene más de 2 símbolos, la reducimos a binaria
            if isinstance(produccion, list) and len(produccion) > 2:
                while len(produccion) > 2:
                    # Tomar los dos primeros símbolos
                    primer, segundo = produccion[0], produccion[1]
                    # Crear una nueva variable
                    nuevo_variable = f"X{nuevo_simbolo_idx}"
                    nuevo_simbolo_idx += 1
                    gramatica['V'].append(nuevo_variable)
                    # Añadir la producción de la nueva variable
                    nuevas_producciones[nuevo_variable] = [[primer, segundo]]
                    # Reducir la producción actual
                    produccion = [nuevo_variable] + produccion[2:]
                    print("\n\tSe agrego nueva producción:", [nuevo_variable] + produccion[2:])  # Imprimir la nueva producción generada
                nuevas_producciones[variable].append(produccion)
                print("\tProducción final para", variable, ":", produccion)  # Imprimir la producción binaria final
            else:
                nuevas_producciones[variable].append(produccion)
    
    gramatica['P'].update(nuevas_producciones)
    print("\n\tSe concluyó el paso BIN")
    
    
    # Paso 3: Eliminar producciones a epsilon
    print("\n***DEL-E***")
    variables_nulas = set()
     
    # Verificamos si el símbolo inicial original tiene una producción vacía
    if any(prod == ['%'] for prod in gramatica['P'][previous_starter]):
        variables_nulas.add(previous_starter)

    # Eliminar producciones vacías excepto en el caso del símbolo inicial
    for variable, producciones in gramatica['P'].items():
        if variable == gramatica['S'] and previous_starter in variables_nulas:
            producciones.append(["%"])  # Asegura la producción vacía para el starter actual
            print("\tSe agrego epsilon en", gramatica['S'], "debido a que la gramática acepta cadenas vacías")
        else:
            original_length = len(producciones)
            producciones[:] = [p for p in producciones if p != ["%"]]  # Eliminamos epsilon
            # Verificamos si se eliminó alguna producción
            if len(producciones) < original_length:
                print("\tSe eliminó epsilon en:", variable)
    
    print("\n\tSe concluyó el paso DEL-E")
    
    # Paso 3: Eliminar producciones unitarias
    print("\n***UNIT***")
    producciones_unitarias = {}
    
    # Paso 3A: Encontrar las prodcucciones unitarias
    for variable, producciones in gramatica['P'].items():
        for produccion in producciones:
            if len(produccion) == 1 and produccion[0] in gramatica['P']:  # Es una producción unitaria
                if variable not in producciones_unitarias:
                    producciones_unitarias[variable] = []
                producciones_unitarias[variable].append(produccion[0])  # Guardar la producción unitaria
                
    print("\n\tProducciones Unitarias:", producciones_unitarias)

    # Paso 3B: Reemplazar producciones unitarias con las producciones correspondientes
    for variable, unitaria in producciones_unitarias.items():
        for prod in unitaria:
            if prod in gramatica['P']:
                # Añadir las producciones de la variable unitaria a la variable actual
                for nueva_produccion in gramatica['P'][prod]:
                    if nueva_produccion not in gramatica['P'][variable]:
                        gramatica['P'][variable].append(nueva_produccion)  # Agregar nueva producción
                print(f"\tSe reemplazaron las producciones unitarias de {variable} con las producciones de {prod}")

    # Paso 3C: Eliminar las producciones unitarias de la gramática
    for variable in producciones_unitarias.keys():
        gramatica['P'][variable] = [p for p in gramatica['P'][variable] if len(p) != 1 or p[0] not in gramatica['P']]

    print("\n\tSe concluyó el paso UNIT")
    
    print("\n***USELESS***\n")
    generativas = set()

    # Encontrar todas las producciones que son generativas
    for variable, producciones in gramatica['P'].items():
        for produccion in producciones:
            if all(simbolo not in gramatica['P'] for simbolo in produccion):  # Solo terminales
                generativas.add(variable)
   
   # Repetir hasta que no haya cambios
    cambio = True
    while cambio:
        cambio = False
        for variable, producciones in gramatica['P'].items():
            if variable not in generativas:
                for produccion in producciones:
                    if all(simbolo in generativas or simbolo not in gramatica['P'] for simbolo in produccion):
                        generativas.add(variable)
                        cambio = True
                        break
    
    #  Eliminar variables no generativas
    for variable in list(gramatica['P'].keys()):
        if variable not in generativas:
            del gramatica['P'][variable]
            if variable in gramatica['V']:
                del gramatica['V'][gramatica['V'].index(variable)]
            print(f"\tSe eliminó la variable no generativa: {variable}")
            
    alcanzables = set()
    to_visit = [gramatica['S']]  # Usar una lista como stack

    while to_visit:
        variable = to_visit.pop()  # Obtener la última variable visitada
        if variable not in alcanzables:
            alcanzables.add(variable)  # Marcamos la variable como alcanzable
            # Agregar producciones alcanzables
            for produccion in gramatica['P'].get(variable, []):
                for simbolo in produccion:
                    if simbolo in gramatica['P'] and simbolo not in alcanzables:
                        to_visit.append(simbolo)  # Agregar simbolos no visitados a la lista

    # Eliminar variables no alcanzables
    for variable in list(gramatica['P'].keys()):
        if variable not in alcanzables:
            del gramatica['P'][variable]
            if variable in gramatica['V']:  # Asegúrate de que gramatica['V'] contenga las variables no terminales
                del gramatica['V'][gramatica['V'].index(variable)] 
            print(f"\tSe eliminó la variable no alcanzable: {variable}")
    
    
    
    print("\n\tSe concluyó el paso USELESS \n")
    
    print(gramatica)

                

# Ejemplo de gramática
# gramatica = {
#     'V': ['S', 'VP', 'PP', 'NP', 'V', 'P', 'N', 'Det', 'D', 'DD'],
#     'T': ['cooks', 'drinks', 'eats', 'cuts', 'in', 'with', 'he', 'she', 'a', 'the', 'cat', 'dog', 'beer', 'cake', 'juice', 'meat', 'soup', 'fork', 'knife', 'oven', 'spoon'],
#     'S': 'S',
#     'P': {
#         'S': [['NP', 'VP']],
#         'VP': [['VP', 'PP'], ['V', 'NP'],['DD'],['cooks'], ['drinks'], ['eats'], ['cuts']],
#         'PP': [['P', 'NP']],
#         'NP': [['Det', 'N'], ['he'], ['she']],
#         'V': [['cooks'], ['drinks'], ['eats'], ['cuts']],
#         'P': [['in'], ['with']],
#         'N': [['cat'], ['dog'], ['beer'], ['cake'], ['juice'], ['meat'], ['soup'], ['fork'], ['knife'], ['oven'], ['spoon']],
#         'Det': [['a'], ['the']],
#         'D': [['DD']],
#         'DD': [['D']]
        
#     }
# }

# chomsky(gramatica)
