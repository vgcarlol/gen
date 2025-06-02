# AUTO-GENERADO: Parser SLR(1)

ACTION = \
{
    (0, 'ID'): ('shift', 2),
    (0, 'LPAREN'): ('shift', 4),
    (0, 'NUMBER'): ('shift', 3),
    (1, '$'): ('reduce', 1),
    (1, 'SEMICOLON'): ('shift', 10),
    (2, 'DIV'): ('reduce', 12),
    (2, 'MINUS'): ('reduce', 12),
    (2, 'PLUS'): ('reduce', 12),
    (2, 'RPAREN'): ('reduce', 12),
    (2, 'SEMICOLON'): ('reduce', 12),
    (2, 'TIMES'): ('reduce', 12),
    (3, 'DIV'): ('reduce', 13),
    (3, 'MINUS'): ('reduce', 13),
    (3, 'PLUS'): ('reduce', 13),
    (3, 'RPAREN'): ('reduce', 13),
    (3, 'SEMICOLON'): ('reduce', 13),
    (3, 'TIMES'): ('reduce', 13),
    (4, 'ID'): ('shift', 2),
    (4, 'LPAREN'): ('shift', 4),
    (4, 'NUMBER'): ('shift', 3),
    (5, '$'): ('reduce', 2),
    (5, 'SEMICOLON'): ('reduce', 2),
    (6, '$'): ('accept', None),
    (7, 'DIV'): ('shift', 12),
    (7, 'MINUS'): ('reduce', 7),
    (7, 'PLUS'): ('reduce', 7),
    (7, 'RPAREN'): ('reduce', 7),
    (7, 'SEMICOLON'): ('reduce', 7),
    (7, 'TIMES'): ('shift', 13),
    (8, 'DIV'): ('reduce', 10),
    (8, 'MINUS'): ('reduce', 10),
    (8, 'PLUS'): ('reduce', 10),
    (8, 'RPAREN'): ('reduce', 10),
    (8, 'SEMICOLON'): ('reduce', 10),
    (8, 'TIMES'): ('reduce', 10),
    (9, 'MINUS'): ('shift', 14),
    (9, 'PLUS'): ('shift', 16),
    (9, 'SEMICOLON'): ('shift', 15),
    (10, 'ID'): ('shift', 2),
    (10, 'LPAREN'): ('shift', 4),
    (10, 'NUMBER'): ('shift', 3),
    (11, 'MINUS'): ('shift', 14),
    (11, 'PLUS'): ('shift', 16),
    (11, 'RPAREN'): ('shift', 18),
    (12, 'ID'): ('shift', 2),
    (12, 'LPAREN'): ('shift', 4),
    (12, 'NUMBER'): ('shift', 3),
    (13, 'ID'): ('shift', 2),
    (13, 'LPAREN'): ('shift', 4),
    (13, 'NUMBER'): ('shift', 3),
    (14, 'ID'): ('shift', 2),
    (14, 'LPAREN'): ('shift', 4),
    (14, 'NUMBER'): ('shift', 3),
    (15, '$'): ('reduce', 4),
    (15, 'SEMICOLON'): ('reduce', 4),
    (16, 'ID'): ('shift', 2),
    (16, 'LPAREN'): ('shift', 4),
    (16, 'NUMBER'): ('shift', 3),
    (17, '$'): ('reduce', 3),
    (17, 'SEMICOLON'): ('reduce', 3),
    (18, 'DIV'): ('reduce', 11),
    (18, 'MINUS'): ('reduce', 11),
    (18, 'PLUS'): ('reduce', 11),
    (18, 'RPAREN'): ('reduce', 11),
    (18, 'SEMICOLON'): ('reduce', 11),
    (18, 'TIMES'): ('reduce', 11),
    (19, 'DIV'): ('reduce', 9),
    (19, 'MINUS'): ('reduce', 9),
    (19, 'PLUS'): ('reduce', 9),
    (19, 'RPAREN'): ('reduce', 9),
    (19, 'SEMICOLON'): ('reduce', 9),
    (19, 'TIMES'): ('reduce', 9),
    (20, 'DIV'): ('reduce', 8),
    (20, 'MINUS'): ('reduce', 8),
    (20, 'PLUS'): ('reduce', 8),
    (20, 'RPAREN'): ('reduce', 8),
    (20, 'SEMICOLON'): ('reduce', 8),
    (20, 'TIMES'): ('reduce', 8),
    (21, 'DIV'): ('shift', 12),
    (21, 'MINUS'): ('reduce', 6),
    (21, 'PLUS'): ('reduce', 6),
    (21, 'RPAREN'): ('reduce', 6),
    (21, 'SEMICOLON'): ('reduce', 6),
    (21, 'TIMES'): ('shift', 13),
    (22, 'DIV'): ('shift', 12),
    (22, 'MINUS'): ('reduce', 5),
    (22, 'PLUS'): ('reduce', 5),
    (22, 'RPAREN'): ('reduce', 5),
    (22, 'SEMICOLON'): ('reduce', 5),
    (22, 'TIMES'): ('shift', 13),
}

GOTO = \
{
    (0, 'expression'): 9,
    (0, 'factor'): 8,
    (0, 'program'): 6,
    (0, 'statement'): 5,
    (0, 'statement_list'): 1,
    (0, 'term'): 7,
    (4, 'expression'): 11,
    (4, 'factor'): 8,
    (4, 'term'): 7,
    (10, 'expression'): 9,
    (10, 'factor'): 8,
    (10, 'statement'): 17,
    (10, 'term'): 7,
    (12, 'factor'): 19,
    (13, 'factor'): 20,
    (14, 'factor'): 8,
    (14, 'term'): 21,
    (16, 'factor'): 8,
    (16, 'term'): 22,
}

productions = [
    ("program'", ['program']),
    ('program', ['statement_list']),
    ('statement_list', ['statement']),
    ('statement_list', ['statement_list', 'SEMICOLON', 'statement']),
    ('statement', ['expression', 'SEMICOLON']),
    ('expression', ['expression', 'PLUS', 'term']),
    ('expression', ['expression', 'MINUS', 'term']),
    ('expression', ['term']),
    ('term', ['term', 'TIMES', 'factor']),
    ('term', ['term', 'DIV', 'factor']),
    ('term', ['factor']),
    ('factor', ['LPAREN', 'expression', 'RPAREN']),
    ('factor', ['ID']),
    ('factor', ['NUMBER']),
]

augmented_start = "program'"


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
