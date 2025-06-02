# yalpar/first_follow.py

from collections import defaultdict

def compute_first(productions, non_terminals, tokens):
    """
    productions: lista de tuplas (lhs, rhs_list), por ejemplo:
        [('expression',['expression','PLUS','term']),
         ('expression',['term']),
         ('term',['term','TIMES','factor']),
         ('term',['factor']),
         ('factor',['LPAREN','expression','RPAREN']),
         ('factor',['ID'])]
    non_terminals: set de no terminales = {'expression','term','factor'}
    tokens: set de terminales = {'ID','PLUS','TIMES','LPAREN','RPAREN'}

    Devuelve:
        - first: dict {symbol → set de terminales ∪ {'' (epsilon)} }
        - first_of_rhs: dict { tuple(rhs_list) → set de terminales ∪ {''} }, 
          donde rhs_list es una tupla de símbolos.
    """
    # Inicializar FIRST
    first = {nt: set() for nt in non_terminals}
    # Para cada terminal t, FIRST[t] = {t}
    for t in tokens:
        first[t] = {t}
    # Epsilon lo representaremos como la cadena vacía '' en FIRST

    cambiado = True
    while cambiado:
        cambiado = False
        for lhs, rhs in productions:
            # Caso: producción A → ε  (si tuviera, pero en nuestros .yalp no hay épsilon explícito)
            if len(rhs) == 0:
                if '' not in first[lhs]:
                    first[lhs].add('')
                    cambiado = True
                continue

            # Para A → X1 X2 ... Xn
            i = 0
            anciana = len(first[lhs])
            primera_temp = set()
            while True:
                X = rhs[i]
                # Añadir FIRST[X] \ {ε} a FIRST[A]
                for sym in first[X]:
                    if sym != '':
                        primera_temp.add(sym)
                if '' in first[X]:
                    i += 1
                    if i >= len(rhs):
                        # Si todos los Xi tienen ε, entonces A también puede derivar ε
                        primera_temp.add('')
                        break
                    else:
                        continue
                else:
                    break

            # Unir con FIRST[A]
            if not primera_temp.issubset(first[lhs]):
                first[lhs] |= primera_temp
                if len(first[lhs]) != anciana:
                    cambiado = True

    # Ahora, para conveniencia, guardamos FIRST de cada secuencia RHS
    first_of_rhs = {}
    for lhs, rhs in productions:
        rhs_tuple = tuple(rhs)
        # Calcular FIRST( rhs_tuple ) similar al algoritmo anterior:
        conjunto = set()
        i = 0
        while True:
            X = rhs[i]
            # Añadir FIRST[X]\{ε}
            for sym in first[X]:
                if sym != '':
                    conjunto.add(sym)
            if '' in first[X]:
                i += 1
                if i >= len(rhs):
                    conjunto.add('')
                    break
                else:
                    continue
            else:
                break
        first_of_rhs[rhs_tuple] = conjunto

    return first, first_of_rhs


def compute_follow(productions, non_terminals, tokens, start_symbol, first):
    """
    Recibe:
      - productions (igual que antes)
      - non_terminals, tokens
      - start_symbol: símbolo inicial de la gramática
      - first: el dict FIRST calculado previamente
    Devuelve:
      - follow: dict { no_terminal → conjunto de terminales ∪ {'$'} }
    """
    follow = {nt: set() for nt in non_terminals}
    follow[start_symbol].add('$')  # Fin de cadena

    cambiado = True
    while cambiado:
        cambiado = False
        for lhs, rhs in productions:
            trailer = set(follow[lhs])  # trailer empezará como FOLLOW(LHS)
            # Recorremos RHS de derecha a izquierda
            for symbol in reversed(rhs):
                if symbol in non_terminals:
                    # Agregar trailer a FOLLOW(symbol)
                    anciano = len(follow[symbol])
                    follow[symbol] |= trailer
                    if len(follow[symbol]) != anciano:
                        cambiado = True
                    # Actualizar trailer: trailer = FIRST(symbol) ∪ (si FIRST(symbol) contiene ε se une trailer anterior)
                    if '' in first[symbol]:
                        # trailer = (FIRST(symbol)\{ε}) ∪ trailer
                        trailer = (first[symbol] - {''}) | trailer
                    else:
                        trailer = first[symbol] - {''}
                else:
                    # Si symbol es terminal, trailer = FIRST(symbol) = {symbol}
                    trailer = {symbol}

    return follow


# Si se ejecuta directamente para prueba rápida:
if __name__ == '__main__':
    from grammar_parser import parse_yalp
    g = parse_yalp('slr-1.yalp')
    f, f_rhs = compute_first(g['productions'], g['non_terminals'], g['tokens'])
    fol = compute_follow(g['productions'], g['non_terminals'], g['tokens'], g['start_symbol'], f)
    print("FIRST:")
    for k in f:
        print(f"  {k} → {f[k]}")
    print("\nFOLLOW:")
    for k in fol:
        print(f"  {k} → {fol[k]}")
