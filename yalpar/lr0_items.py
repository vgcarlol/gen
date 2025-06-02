# yalpar/lr0_items.py

from collections import defaultdict

def closure(items, productions, non_terminals):
    closure_set = set(items)
    cambiado = True
    while cambiado:
        cambiado = False
        new_items = set()
        for (lhs, rhs, dot_pos) in closure_set:
            # Si el punto está antes de un no terminal B, es decir, rhs[dot_pos] == B
            if dot_pos < len(rhs):
                B = rhs[dot_pos]
                if B in non_terminals:
                    # Por cada producción B → gamma, añadimos (B, gamma, 0)
                    for (lhs2, rhs2) in productions:
                        if lhs2 == B:
                            item = (B, tuple(rhs2), 0)
                            if item not in closure_set:
                                new_items.add(item)
        if new_items:
            closure_set |= new_items
            cambiado = True
    return closure_set


def goto(items, X, productions, non_terminals):
    moved = set()
    for (lhs, rhs, dot_pos) in items:
        if dot_pos < len(rhs) and rhs[dot_pos] == X:
            # Avanzamos dot_pos → dot_pos+1
            moved.add((lhs, rhs, dot_pos + 1))
    # Ahora devolvemos closure(moved)
    return closure(moved, productions, non_terminals)


def items_LR0(productions, non_terminals, start_symbol):
    # 1) Creamos la gramática aumentada: S' → start_symbol
    aug_start = start_symbol + "'"  # Ejemplo: si start_symbol='expression', aug_start="expression'"
    # Insertar al inicio de las producciones la producción aumentada
    productions_aug = [(aug_start, [start_symbol])] + productions

    # 2) El item inicial es closure({ (aug_start, (start_symbol,), 0) })
    I0 = closure({ (aug_start, tuple([start_symbol]), 0) }, productions_aug, non_terminals | {aug_start})

    C = [frozenset(I0)]
    transitions = dict()
    changed = True

    while changed:
        changed = False
        for i, Ii in enumerate(C):
            # Para cada símbolo X (terminal o no-terminal) que aparezca tras un punto en Ii
            todos_simbolos = set()
            for (lhs, rhs, dot_pos) in Ii:
                if dot_pos < len(rhs):
                    todos_simbolos.add(rhs[dot_pos])
            for X in todos_simbolos:
                Ij = frozenset(goto(Ii, X, productions_aug, non_terminals | {aug_start}))
                if not Ij:
                    continue
                if Ij not in C:
                    C.append(Ij)
                    j = len(C) - 1
                    transitions[(i, X)] = j
                    changed = True
                else:
                    j = C.index(Ij)
                    if (i, X) not in transitions:
                        transitions[(i, X)] = j
    return C, transitions, productions_aug, aug_start

# Si se ejecuta directamente, imprime los item-sets de la gramática slr-1
if __name__ == '__main__':
    from grammar_parser import parse_yalp
    g = parse_yalp('slr-1.yalp')
    C, trans, prods_aug, aug = items_LR0(g['productions'], g['non_terminals'], g['start_symbol'])
    print(f"Un total de {len(C)} item-sets LR(0):\n")
    for idx, I in enumerate(C):
        print(f"I{idx}:")
        for item in I:
            lhs, rhs, dot_pos = item
            derecha = list(rhs)
            derecha.insert(dot_pos, '·')
            print(f"  {lhs} → {' '.join(derecha)}")
        print()
    print("Transiciones (i, X) → j:")
    for k, v in trans.items():
        print(f"  {k} -> {v}")