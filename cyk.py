import json
def printMatrix(matrix, cadena):
    for i in range(len(matrix)):
        tem = cadena[i]+" "
        for j in range(len(matrix[i])):
            tem=tem+str(matrix[i][j])+", "
        print(tem)

def cyk_main(CNF, w):
    n = len(w)
    matrix = []
    
    # Inicialización de la matriz de cyk. 
    # tamaño nxn con todas las entradas siendo listas vacias
    for _ in range(n):
        tem = []
        for _ in range(n):
            tem.append([])
        matrix.append(tem)

    # Se itera por la identidad de la matriz
    for i in range(n):
        for var in CNF["V"]:
            if(w[i] in CNF["P"][var]):
                matrix[i][i].append(var)
            
    # CYK other iteration     
    for l in range(1,n):
        for i in range(n-l):
            j = i+l
            for k in range(i,j):
                for var in CNF["V"]:
                    for rsltVar in CNF["P"][var]:
                        rslt = rsltVar.split(" ")
                        if(len(rslt)>1):
                            if(rslt[0] in matrix[i][k]) and (rslt[1] in matrix[k+1][j]):
                                if not (var in matrix[i][j]):
                                    matrix[i][j].append(var)
            
    printMatrix(matrix, w)
    if(CNF["S"] in matrix[0][n-1]):
        print("la cadena es acepatada")
        return (True, matrix)
    else:
        print("La cadena NO es acepatada")
        return (False, [])
    