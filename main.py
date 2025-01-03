"""
Proyecto 2 - Gramáticas
V 1.0

Irving Acosta 22
Diego Duarte 22075
José Marchena 22398
"""
from chomsky import chomsky  # Importamos la función de transformación a CNF
from Parse_Tree import create_and_display_parse_tree  # Importamos la función de creación y visualización del Parse Tree

def convertir_a_json(gramatica_str):
    no_terminales = set()
    terminales = set()
    producciones = {}
    
    # Procesamos línea por línea de la gramática
    for regla in gramatica_str.strip().splitlines():
        izquierda, derecha = regla.split('→')
        izquierda = izquierda.strip()  # No terminal
        derechos = [parte.strip() for parte in derecha.split('|')]  # Opciones a la derecha
        
        # Añadir el no terminal de la izquierda a V
        no_terminales.add(izquierda)
        
        # Añadir las producciones al no terminal
        if izquierda not in producciones:
            producciones[izquierda] = []
        
        for derecho in derechos:
            partes_derecho = derecho.split()
            producciones[izquierda].append(partes_derecho)
            
            # Verificamos si las partes son terminales o no terminales
            for parte in partes_derecho:
                if parte.islower():  # Los terminales usualmente están en minúsculas
                    terminales.add(parte)
                else:
                    no_terminales.add(parte)

    # Convertir sets a listas
    gramatica_json = {
        "V": list(no_terminales),  # No terminales
        "T": list(terminales),     # Terminales
        "S": "S",                  # Símbolo inicial
        "P": producciones          # Producciones
    }

    return gramatica_json

# Gramática de ejemplo
gramatica_bnf = """
S → NP VP 
VP → VP PP
VP → V NP
VP → cooks | drinks | eats | cuts
PP → P NP
NP → Det N
NP → he | she
V → cooks | drinks | eats | cuts
P → in | with
N → cat | dog
N → beer | cake | juice | meat | soup
N → fork | knife | oven | spoon
Det → a | the
"""

# Convertir la gramática a JSON
gramatica_json = convertir_a_json(gramatica_bnf)

# Convertir la gramática a Forma Normal de Chomsky
chomsky(gramatica_json)

# Cadenas de entrada:

    # Aceptadas y semanticamente correctas
c1 = ["the", "cat", "drinks", "the","soup"]
c2 = ["he", "cuts", "the", "cake", "with", "a","knife"]

    # Aceptadas y semanticamente incorrectas
c3 = ["a", "beer", "cuts", "she"]
c4 = ["he", "eats", "he", "in", "he"]

    # No aceptadas
c5 = ["she", "sleeps", "with", "the", "cat"]
c6 = ["the", "dog", "eats", "meat"]

# Generar y mostrar el Parse Tree para la cadena dada
create_and_display_parse_tree(gramatica_json, c1)
