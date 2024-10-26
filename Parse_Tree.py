import nltk
from nltk.tree import Tree
from cyk import cyk_main  # Importamos el algoritmo CYK
from chomsky import chomsky  # Importamos el algoritmo de conversión a CNF

# Función para construir el Parse Tree desde la matriz CYK
def build_parse_tree(matrix, CNF, start_symbol, w, i=0, j=None):
    if j is None:
        j = len(matrix) - 1  # La longitud de la cadena - 1
    
    # Si estamos en un terminal, devolvemos un árbol con el terminal correspondiente
    if i == j:
        terminal = w[i]  # El terminal en la posición actual de la cadena
        return Tree(matrix[i][j][0], [terminal])

    # Encontrar la combinación que generó el símbolo en la posición (i, j)
    for k in range(i, j):
        for var in CNF["V"]:
            for rsltVar in CNF["P"][var]:
                if len(rsltVar) == 2:  # Para producciones binarias
                    if (rsltVar[0] in matrix[i][k]) and (rsltVar[1] in matrix[k + 1][j]):
                        # Crear subárboles recursivamente
                        left_subtree = build_parse_tree(matrix, CNF, start_symbol, w, i, k)
                        right_subtree = build_parse_tree(matrix, CNF, start_symbol, w, k + 1, j)
                        return Tree(var, [left_subtree, right_subtree])

    return Tree(start_symbol, [])  # Devolver un árbol vacío en caso de no encontrar

# Función principal para crear el árbol y validarlo
def create_and_display_parse_tree(CNF, w):
    # Ejecutar el algoritmo CYK para obtener validez y la matriz
    valid, matrix = cyk_main(CNF, w)
    
    if not valid:
        print("La cadena no pertenece al lenguaje.")
        return None

    # Construir el árbol de parseo
    parse_tree = build_parse_tree(matrix, CNF, CNF["S"], w)

    # Mostrar el árbol gráficamente usando nltk
    parse_tree.pretty_print()
    return parse_tree
