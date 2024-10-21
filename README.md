# Proyecto2-Gramaticas

## Estructura para gramáticas
- % significa epsilom como el proyecto anterior

CFG: {
    "V": ["S","A","B"...],      // Variables
    "T": ["a","b","c"..."%"],   // Símbolos terminales
    "S":"S",                    // Variabl inicial
    "P": {                      // Producciones
        "S": ["A"],         // S -> A
        "A": ["Aa","a"],    // A -> Aa|a
        "B": ["%","b"],     // B -> ε|b
        ...
    }
}