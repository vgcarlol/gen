# AUTO-GENERADO: Parser SLR(1)

ACTION = \
{
    (0, 'ID'): ('shift', 2),
    (0, 'LPAREN'): ('shift', 3),
    (1, '$'): ('reduce', 2),
    (1, 'PLUS'): ('reduce', 2),
    (1, 'RPAREN'): ('reduce', 2),
    (1, 'TIMES'): ('shift', 6),
    (2, '$'): ('reduce', 6),
    (2, 'PLUS'): ('reduce', 6),
    (2, 'RPAREN'): ('reduce', 6),
    (2, 'TIMES'): ('reduce', 6),
    (3, 'ID'): ('shift', 2),
    (3, 'LPAREN'): ('shift', 3),
    (4, '$'): ('reduce', 4),
    (4, 'PLUS'): ('reduce', 4),
    (4, 'RPAREN'): ('reduce', 4),
    (4, 'TIMES'): ('reduce', 4),
    (5, '$'): ('accept', None),
    (5, 'PLUS'): ('shift', 8),
    (6, 'ID'): ('shift', 2),
    (6, 'LPAREN'): ('shift', 3),
    (7, 'PLUS'): ('shift', 8),
    (7, 'RPAREN'): ('shift', 10),
    (8, 'ID'): ('shift', 2),
    (8, 'LPAREN'): ('shift', 3),
    (9, '$'): ('reduce', 3),
    (9, 'PLUS'): ('reduce', 3),
    (9, 'RPAREN'): ('reduce', 3),
    (9, 'TIMES'): ('reduce', 3),
    (10, '$'): ('reduce', 5),
    (10, 'PLUS'): ('reduce', 5),
    (10, 'RPAREN'): ('reduce', 5),
    (10, 'TIMES'): ('reduce', 5),
    (11, '$'): ('reduce', 1),
    (11, 'PLUS'): ('reduce', 1),
    (11, 'RPAREN'): ('reduce', 1),
    (11, 'TIMES'): ('shift', 6),
}

GOTO = \
{
    (0, 'expression'): 5,
    (0, 'factor'): 4,
    (0, 'term'): 1,
    (3, 'expression'): 7,
    (3, 'factor'): 4,
    (3, 'term'): 1,
    (6, 'factor'): 9,
    (8, 'factor'): 4,
    (8, 'term'): 11,
}

productions = [
    ("expression'", ['expression']),
    ('expression', ['expression', 'PLUS', 'term']),
    ('expression', ['term']),
    ('term', ['term', 'TIMES', 'factor']),
    ('term', ['factor']),
    ('factor', ['LPAREN', 'expression', 'RPAREN']),
    ('factor', ['ID']),
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
