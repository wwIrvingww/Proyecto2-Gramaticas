"""
Proyecto 2 - Gramáticas
V 1.0

Irving Acosta 22
Diego Duarte 22075
José Marchena 22

"""

import json

# Leer el archivo JSON
with open('CFG_example.json', 'r') as file:
    gramatica = json.load(file)
    
print(gramatica)
