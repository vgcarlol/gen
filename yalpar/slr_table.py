# yalpar/slr_table.py

from collections import defaultdict

def build_slr_table(C, transitions, productions_aug, aug_start, non_terminals, tokens, first, follow):
    action = dict()
    goto = dict()

    # 1) Recorrer cada item-set I[i] en C
    for i, Ii in enumerate(C):
        # 1.a) Si hay un item (A → α · a β) y a ∈ tokens, shift
        for (A, rhs, dot_pos) in Ii:
            if dot_pos < len(rhs):
                a = rhs[dot_pos]
                # Si 'a' es terminal y existe transición(i, a)
                if a in tokens and (i, a) in transitions:
                    j = transitions[(i, a)]
                    # SHIFT
                    key = (i, a)
                    valor = ('shift', j)
                    if key in action and action[key] != valor:
                        print(f"WARNING: conflicto SHIFT/REDUCE o SHIFT/SHIFT en acción {key}")
                    action[key] = valor

        # 1.b) Si hay un item (A → α ·) (punto al final)...
        for (A, rhs, dot_pos) in Ii:
            if dot_pos == len(rhs):
                # Caso 1: es la producción aumentada: (aug_start → start_symbol ·)
                if A == aug_start:
                    # ACCEPT en símbolo '$'
                    action[(i, '$')] = ('accept', None)
                else:
                    # Encontramos el índice de esta producción en productions_aug
                    prod_index = None
                    for idx, (lhs_p, rhs_p) in enumerate(productions_aug):
                        if lhs_p == A and tuple(rhs_p) == rhs:
                            prod_index = idx
                            break
                    if prod_index is None:
                        raise RuntimeError(f"No hallé la producción index para {A} → {rhs}")

                    # Para cada b ∈ FOLLOW(A), poner REDUCE
                    for b in follow[A]:
                        key = (i, b)
                        valor = ('reduce', prod_index)
                        if key in action and action[key] != valor:
                            print(f"WARNING: conflicto REDUCE/REDUCE en {key}")
                        action[key] = valor

        # 2) Construir GOTO: si (i, A)→j para A ∈ non_terminals
        for A in non_terminals:
            if (i, A) in transitions:
                j = transitions[(i, A)]
                goto[(i, A)] = j

    return action, goto


if __name__ == '__main__':
    from grammar_parser import parse_yalp
    from lr0_items import items_LR0
    from first_follow import compute_first, compute_follow

    g = parse_yalp('slr-1.yalp')
    C, trans, prods_aug, aug = items_LR0(g['productions'], g['non_terminals'], g['start_symbol'])
    # Recalcular FIRST/FOLLOW con la gramática original (sin aumentos)
    first, first_rhs = compute_first(g['productions'], g['non_terminals'], g['tokens'])
    follow = compute_follow(g['productions'], g['non_terminals'], g['tokens'], g['start_symbol'], first)

    action, goto = build_slr_table(C, trans, prods_aug, aug, g['non_terminals'] | {aug}, g['tokens'], first, follow)
    print("\nACTION table:")
    for key in sorted(action):
        print(f"  {key} → {action[key]}")
    print("\nGOTO table:")
    for key in sorted(goto):
        print(f"  {key} → {goto[key]}")