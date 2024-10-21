def chomsky(gramatica):
    print("START")
    gramatica['V'].append("S1")
    gramatica['P']['S1'] = [gramatica['S']] 
    del gramatica['P']['S']
    gramatica['S'] = "S1"
    
    print("BIN")
    
    
chomsky({'V': ['S', 'VP', 'PP', 'NP', 'V', 'P', 'N', 'Det'], 'T': ['cooks', 'drinks', 'eats', 'cuts', 'in', 'with', 'he', 'she', 'a', 'the', 'cat', 'dog', 'beer', 'cake', 'juice', 'meat', 'soup', 'fork', 'knife', 'oven', 'spoon'], 'S': 'S', 'P': {'S': ['NP VP'], 'VP': ['VP PP', 'V NP', 'cooks', 'drinks', 'eats', 'cuts'], 'PP': ['P', 'NP'], 'NP': ['Det N', 'he', 'she'], 'V': ['cooks', 'drinks', 'eats', 'cuts'], 'P': ['in', 'with'], 'N': ['cat', 'dog', 'beer', 'cake', 'juice', 'meat', 'soup', 'fork', 'knife', 'oven', 'spoon'], 'Det': ['a', 'the']}})
    