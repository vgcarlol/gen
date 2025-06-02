# AUTO-GENERADO: Parser SLR(1)

ACTION = \
{
    (0, 'LPAREN'): ('shift', 1),
    (0, 'NUMBER'): ('shift', 4),
    (1, 'LPAREN'): ('shift', 1),
    (1, 'NUMBER'): ('shift', 4),
    (2, '$'): ('accept', None),
    (3, '$'): ('reduce', 2),
    (3, 'PLUS'): ('shift', 6),
    (3, 'RPAREN'): ('reduce', 2),
    (4, '$'): ('reduce', 4),
    (4, 'PLUS'): ('reduce', 4),
    (4, 'RPAREN'): ('reduce', 4),
    (4, 'TIMES'): ('shift', 7),
    (5, 'RPAREN'): ('shift', 8),
    (6, 'LPAREN'): ('shift', 1),
    (6, 'NUMBER'): ('shift', 4),
    (7, 'LPAREN'): ('shift', 1),
    (7, 'NUMBER'): ('shift', 4),
    (8, '$'): ('reduce', 5),
    (8, 'PLUS'): ('reduce', 5),
    (8, 'RPAREN'): ('reduce', 5),
    (9, '$'): ('reduce', 1),
    (9, 'RPAREN'): ('reduce', 1),
    (10, '$'): ('reduce', 3),
    (10, 'PLUS'): ('reduce', 3),
    (10, 'RPAREN'): ('reduce', 3),
}

GOTO = \
{
    (0, 'expression'): 2,
    (0, 'term'): 3,
    (1, 'expression'): 5,
    (1, 'term'): 3,
    (6, 'expression'): 9,
    (6, 'term'): 3,
    (7, 'term'): 10,
}

productions = [
    ("expression'", ['expression']),
    ('expression', ['term', 'PLUS', 'expression']),
    ('expression', ['term']),
    ('term', ['NUMBER', 'TIMES', 'term']),
    ('term', ['NUMBER']),
    ('term', ['LPAREN', 'expression', 'RPAREN']),
]

augmented_start = "expression'"


def parse(tokens):
    """
    tokens: lista de tuplas (lexema, token), e.g. [('id','ID'), ('+','PLUS'), ..., ('$','$')]
    Simula el parser SLR(1), imprimiendo cada paso (SHIFT, REDUCE, GOTO, ACCEPT).
    Si hay error, lo notifica y devuelve False. Si acepta, devuelve True.
    """
    stack_states = [0]
    stack_symbols = []
    i = 0

    while True:
        estado = stack_states[-1]
        if i >= len(tokens):
            print("Error: no hay más tokens, falta '$'")
            return False
        lexema, tok = tokens[i]
        key = (estado, tok)
        if key not in ACTION:
            print(f"Error sintáctico: estado={estado}, token '{tok}' no esperado.")
            return False
        act = ACTION[key]
        if act[0] == 'shift':
            j = act[1]
            stack_states.append(j)
            stack_symbols.append((lexema, tok))
            print(f"SHIFT: estado={estado} --token '{tok}'--> push estado {j}, símbolo ('{lexema}','{tok}')")
            i += 1
        elif act[0] == 'reduce':
            prod_idx = act[1]
            lhs, rhs = productions[prod_idx]
            # Desapilar |rhs| elementos
            for _ in rhs:
                stack_states.pop()
                stack_symbols.pop()
            print(f"REDUCE: usar producción {prod_idx}: {lhs} → {' '.join(rhs)}")
            estado_prev = stack_states[-1]
            goto_key = (estado_prev, lhs)
            if goto_key not in GOTO:
                print(f"Error GOTO: no hay GOTO[{estado_prev}, {lhs}]")
                return False
            new_state = GOTO[goto_key]
            stack_states.append(new_state)
            stack_symbols.append((lhs, 'NT'))
            print(f"GOTO: estado={estado_prev} con no-term '{lhs}' → push estado {new_state}")
        elif act[0] == 'accept':
            print("ACCEPT: cadena sintácticamente correcta.")
            return True
        else:
            print("Acción desconocida en la tabla ACTION.")
            return False
